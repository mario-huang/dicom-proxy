# dicom-proxy

DICOM DIMSE proxy.

## Supported DIMSE services

-   C-Echo
-   C-Find
-   C-Move

## Features

-   simple to use
-   docker support

## What is it for

If you only have a single AE (for example, from a hospital) but have multiple applications that need to access the PACS system, this proxy tool can help you.

## How to run

You can clone the repo and run `python src/main.py`
Or use docker `docker compose up -d`

## How to config

Edit the `config.json` file

```json
{
    // open debug log or not
    "debug": true,
    // set the proxy
    "proxy": {
        "aet": "DicomProxy",
        "address": "0.0.0.0",
        "port": 11112
    },
    // set your original pacs server
    "server": {
        "aet": "UpstreamPacs",
        "address": "192.168.1.1",
        "port": 4242
    },
    // set your clients
    "clients": [
        {
            "aet": "ClientAET",
            "address": "192.168.1.2",
            "port": 6000
        }
    ]
}
```
