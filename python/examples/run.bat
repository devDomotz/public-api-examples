@ECHO OFF
setlocal
set PYTHONPATH=%PYTHONPATH%;src
python  -m domotz_api_client.device_status_change %*
endlocal