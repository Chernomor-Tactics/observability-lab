#!/usr/bin/env bash
set -euo pipefail
vm="${MONITOR_VM:-monitor-lab}"
case "${1:-}" in
  cpu) multipass exec "$vm" -- stress-ng --cpu 2 --timeout 90s --metrics-brief ;;
  memory) multipass exec "$vm" -- stress-ng --vm 1 --vm-bytes 256M --vm-keep --timeout 60s --metrics-brief ;;
  disk)
    multipass exec "$vm" -- bash -s <<'VM_SCRIPT'
      set -euo pipefail
      set -o noclobber
      file=/var/tmp/monitor-load/demo.bin
      if [[ -e "$file" ]]; then echo "Demo file already exists; remove it before retrying" >&2; exit 1; fi
      trap 'rm -f -- "$file"' EXIT
      dd if=/dev/zero bs=1M count=256 status=progress > "$file"
      sync
      sleep 60
VM_SCRIPT
    ;;
  *) echo "Usage: bash scripts/load.sh cpu|memory|disk" >&2; exit 1 ;;
esac
