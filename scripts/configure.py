"""Generate local credentials once and configure the monitored VM address."""
import ipaddress
import json
import secrets
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
if len(sys.argv) != 2:
    raise SystemExit("Usage: python3 scripts/configure.py VM_IPV4")
address = str(ipaddress.IPv4Address(sys.argv[1]))
env = root / ".env"
if not env.exists():
    with env.open("x") as file:
        env.chmod(0o600)
        file.write(
            f"GRAFANA_ADMIN_PASSWORD={secrets.token_urlsafe(24)}\n"
            "MINIO_ROOT_USER=monitoradmin\n"
            f"MINIO_ROOT_PASSWORD={secrets.token_urlsafe(32)}\n"
        )
    print("Created .env with random passwords")
else:
    print("Existing .env preserved")
targets = [{"targets": [f"{address}:9100"], "labels": {"machine": "monitor-lab"}}]
(root / "prometheus/targets.json").write_text(json.dumps(targets, indent=2) + "\n")
print(f"Monitoring target: {address}:9100")
