"""Query only Store Gateway and restore the normal Query configuration on exit."""
import json
import subprocess
import time
import urllib.parse
import urllib.request
from pathlib import Path

root = Path(__file__).resolve().parents[1]
def compose(*args):
    subprocess.run(["docker", "compose", *args], cwd=root, check=True)

try:
    compose("-f", "compose.yaml", "-f", "compose.archive-check.yaml",
            "up", "-d", "--no-deps", "thanos-query")
    end = int(time.time())
    params = urllib.parse.urlencode({"query": 'up{job="node"}',
                                     "start": end - 86400, "end": end, "step": 60})
    url = "http://127.0.0.1:10904/api/v1/query_range?" + params
    for attempt in range(30):
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                payload = json.load(response)
            if payload.get("status") != "success":
                raise RuntimeError(payload.get("error", "Query failed"))
            points = sum(len(item["values"]) for item in payload["data"]["result"])
            if not points:
                raise RuntimeError("No archived samples in the last 24 hours yet")
            print(f"Archive check passed: {points} samples via Store Gateway only")
            break
        except Exception:
            if attempt == 29:
                raise
            time.sleep(2)
finally:
    compose("up", "-d", "--no-deps", "thanos-query")
