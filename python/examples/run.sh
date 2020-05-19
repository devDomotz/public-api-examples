#!/bin/bash
export PYTHONPATH=./src

python -m domotz_api_client.device_status_change "$@"
