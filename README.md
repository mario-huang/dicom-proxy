# dicom-proxy

English · [日本語](./README_ja.md) · [中文](./README_zh.md)

DICOM DIMSE Proxy Service

## Supported DIMSE Services

- C-Echo
- C-Find
- C-Move

## Features

- Simple and easy to use
- Docker deployment support
- Multi-client configuration
- Debug logging switch

## Use Case

When you only have one AE (e.g. from hospital PACS) but need multiple applications to access:
- Acts as intermediate proxy to receive requests from multiple clients
- Forwards requests to upstream PACS system uniformly
- Manages different clients' AE Titles and network configurations

## Running the Service

### Method 1: Run from Source
1. Clone repository and enter directory:
```bash
git clone git@github.com:mario-huang/dicom-proxy.git
cd dicom-proxy
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start service:
```bash
python src/main.py
```

### Method 2: Docker Deployment
```bash
docker compose up -d
```

## Configuration

Edit `config.json`:

```json
{
    // Enable debug logging
    "debug": true,
    
    // Proxy server configuration
    "proxy": {
        "aet": "DicomProxy",     // Proxy AE Title
        "address": "0.0.0.0",    // Listening address
        "port": 11112            // Listening port
    },
    
    // Upstream PACS configuration
    "server": {
        "aet": "UpstreamPacs",   // PACS AE Title 
        "address": "192.168.1.1",// PACS IP address
        "port": 4242             // PACS port
    },
    
    // Client configuration list
    "clients": [
        {
            "aet": "ClientAET",  // Client AE Title
            "address": "192.168.1.2", // Client IP
            "port": 6000         // Client port
        }
    ]
}
```

## Important Notes
1. Ensure firewall allows proxy port (default 11112)
2. Client configurations must match DICOM settings of application endpoints
3. Recommended to disable debug mode in production
