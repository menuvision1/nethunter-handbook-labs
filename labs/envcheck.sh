#!/usr/bin/env bash
for t in python3 curl nmap tshark git; do
  if command -v "$t" >/dev/null 2>&1; then echo "OK    $t -> $(command -v "$t")"; else echo "MISS  $t"; fi
done
