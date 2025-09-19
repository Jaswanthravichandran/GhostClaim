#!/usr/bin/bash

sudo apt update
pip install -r requirements.txt

if [ -f "subdomains.txt"]; then
    rm -rf subdomains.txt
else
    echo "[*] Installation Completed"
fi