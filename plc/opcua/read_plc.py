"""
read_plc.py - read live values from the CODESYS conveyor PLC over OPC UA.

Connects with encryption (Basic256Sha256, Sign & Encrypt) and a PLC user,
then prints MOTOR, LAMP, JAM, RUN and the box count twice per second and
saves every reading to logs/plc_log_<date>_<time>.csv (a small "historian").

First run: the script creates its own certificate in ./pki. The PLC puts it
in quarantine, so the first connection fails. Trust it in CODESYS
(Security Screen > Devices > Quarantined > drag to Trusted), then run again.

Run:  python read_plc.py      (Ctrl+C to stop)
Optional: set the password once per terminal so you don't type it blind:
      $env:PLC_PASSWORD = "your-password"   (PowerShell, not saved to disk)
"""
import asyncio
import csv
import getpass
import os
from datetime import datetime
from pathlib import Path

from asyncua import Client, ua
from asyncua.crypto.cert_gen import setup_self_signed_certificate
from asyncua.crypto.security_policies import SecurityPolicyBasic256Sha256
from cryptography.x509.oid import ExtendedKeyUsageOID

URL = "opc.tcp://localhost:4840"
USER = "admin"
NS = 4  # namespace index shown in UaExpert (ns=4)
PREFIX = "|var|CODESYS Control Win V3 x64.Application.PLC_PRG."
VARIABLES = ["MOTOR", "LAMP", "JAM", "RUN", "C1.CV"]
PERIOD_S = 0.5  # sampling period

HERE = Path(__file__).parent
PKI = HERE / "pki"
CERT = PKI / "python_client_cert.der"
KEY = PKI / "python_client_key.pem"
APP_URI = "urn:fbz8:python:conveyor-reader"


async def make_certificate():
    """Create a self-signed client certificate once (kept in ./pki, not in Git)."""
    if CERT.exists() and KEY.exists():
        return
    PKI.mkdir(exist_ok=True)
    await setup_self_signed_certificate(
        KEY,
        CERT,
        APP_URI,
        "localhost",
        [ExtendedKeyUsageOID.CLIENT_AUTH],
        {"countryName": "TR", "organizationName": "Student", "commonName": "PythonConveyorReader"},
    )
    print(f"Created client certificate: {CERT}")


async def main():
    await make_certificate()
    # Password from the environment (set once per terminal session), else ask hidden.
    password = os.environ.get("PLC_PASSWORD") or getpass.getpass(f"PLC password for '{USER}': ")

    client = Client(URL)
    client.application_uri = APP_URI
    client.set_user(USER)
    client.set_password(password)
    await client.set_security(
        SecurityPolicyBasic256Sha256,
        certificate=str(CERT),
        private_key=str(KEY),
        mode=ua.MessageSecurityMode.SignAndEncrypt,
    )

    async with client:
        print(f"Connected to {URL}\n")
        nodes = {name: client.get_node(f"ns={NS};s={PREFIX}{name}") for name in VARIABLES}
        logs = HERE / "logs"
        logs.mkdir(exist_ok=True)
        log_file = logs / f"plc_log_{datetime.now():%Y%m%d_%H%M%S}.csv"
        print(f"Logging to {log_file}\n")
        print("time      " + "".join(f"{n:>8}" for n in VARIABLES))
        with open(log_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp"] + VARIABLES)
            while True:
                values = [await nodes[n].read_value() for n in VARIABLES]
                now = datetime.now()
                # booleans stored as 0/1 so the CSV is easy to plot and to use for ML later
                writer.writerow([now.isoformat(timespec="milliseconds")] + [int(v) for v in values])
                f.flush()
                row = "".join(f"{str(v):>8}" for v in values)
                print(f"{now:%H:%M:%S}  {row}")
                await asyncio.sleep(PERIOD_S)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped.")
