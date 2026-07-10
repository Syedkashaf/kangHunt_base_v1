# GHunt v2.3.4 Integration Guide

## Overview

This document explains the integration of GHunt v2.3.4 into kangHunt_base_v1.

### What is GHunt?

**GHunt** is an offensive Google framework designed for OSINT (Open Source Intelligence) gathering. It provides comprehensive access to Google-based information sources.

- **Author**: mxrch (@mxrchreborn)
- **Repository**: https://github.com/mxrch/GHunt
- **Version**: 2.3.4 (Spider Edition)
- **License**: AGPL-3.0
- **Python**: 3.10+

### Integration Details

**GHunt is now directly integrated** into kangHunt_base_v1 as a native module:
- No external pip installation required
- All dependencies included in `requirements.txt`
- Direct source code access for customization
- Full compatibility with kangHunt workflow

---

## Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/Syedkashaf/kangHunt_base_v1.git
cd kangHunt_base_v1
```

The `ghunt/` directory contains the complete GHunt source code.

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# OR
venv\\Scripts\\activate   # Windows
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required packages for both kangHunt and GHunt.

### Step 4: Verify Installation

```bash
python DIAGNOSTIC.py
```

---

## Authentication Setup

### GHunt Authentication Methods

GHunt requires authentication to access Google services. You must use ONE method:

#### Option 1: OAuth Token (Recommended ⭐)

**Best for**: Most users, easiest setup

1. Install GHunt Companion extension:
   - **Firefox**: https://addons.mozilla.org/en-US/firefox/addon/ghunt-companion/
   - **Chrome/Chromium**: [Chrome Web Store](https://chrome.google.com/webstore)
   - **Edge/Opera**: Compatible

2. Click extension icon and follow authentication flow

3. Extension generates `oauth_token` (starts with `oauth2_4/`)

4. Add to `.env`:
   ```bash
   GOOGLE_OAUTH_TOKEN=oauth2_4/0ABCDEF1234567890...
   ```

#### Option 2: Master Token

**Best for**: Automation, server deployments

1. Use GHunt Companion to generate Master Token (starts with `aas_et/`)

2. Add to `.env`:
   ```bash
   GOOGLE_MASTER_TOKEN=aas_et/0ABCDEF1234567890...
   ```

#### Option 3: Cookies

**Best for**: Browser-based workflows

1. Export cookies from authenticated Google session

2. Add to `.env`:
   ```bash
   GOOGLE_COOKIES=NID=value1;CONSENT=value2;...
   ```

### Configuration

Edit `.env` file:

```env
# Enable GHunt
GHUNT_ENABLED=True

# Credentials (choose ONE method)
GOOGLE_OAUTH_TOKEN=oauth2_4/...
# GOOGLE_MASTER_TOKEN=aas_et/...
# GOOGLE_COOKIES=...

# Paths
GHUNT_CREDS_PATH=.ghunt_creds
GHUNT_CACHE_DIR=.ghunt_cache
```

---

## Usage

### Python API

```python
from ghunt.objects.base import GHuntCreds
from ghunt.modules import email
import asyncio
import httpx

async def investigate_email():
    # Create async client
    async with httpx.AsyncClient() as client:
        # Create credentials object
        creds = GHuntCreds()
        
        # Hunt email
        is_found, target = await email.hunt(
            client,
            "target@example.com",
            json_file=None
        )
        
        if is_found:
            print(f"Found: {target}")
        else:
            print("Email not found")

# Run
asyncio.run(investigate_email())
```

### GHunt Modules

Available GHunt modules:

```python
from ghunt.modules import (
    email,          # Email/Gaia ID investigation
    gaia,           # Google account by ID
    drive,          # Google Drive file investigation
    geolocate,      # WiFi BSSID geolocation
    spiderdal,      # Digital Assets Links
    login,          # Authentication
)
```

### CLI Usage

```bash
# Email investigation
python -m ghunt email target@example.com

# Gaia ID investigation
python -m ghunt gaia 123456789

# Drive file investigation
python -m ghunt drive FILE_ID

# Export to JSON
python -m ghunt email target@example.com --json results.json
```

---

## Directory Structure

```
kangHunt_base_v1/
└── ghunt/                           # GHunt v2.3.4 (integrated)
    ├── __init__.py                  # Package initialization
    ├── config.py                    # Headers, templates
    ├── errors.py                    # Exception classes
    ├── globals.py                   # Global variables
    ├── version.py                   # Version info
    ├── ghunt.py                     # Entry point
    ├── cli.py                       # CLI interface
    │
    ├── apis/                        # Google API implementations
    │   ├── __init__.py
    │   ├── accounts.py              # Google Accounts API
    │   ├── calendar.py              # Google Calendar API
    │   ├── drive.py                 # Google Drive API
    │   ├── peoplepa.py              # People API
    │   ├── playgames.py             # Play Games API
    │   ├── vision.py                # Vision API
    │   └── ... (other APIs)
    │
    ├── modules/                     # OSINT modules
    │   ├── __init__.py
    │   ├── email.py                 # Email investigation
    │   ├── gaia.py                  # Gaia ID investigation
    │   ├── drive.py                 # Drive investigation
    │   ├── geolocate.py             # Geolocation
    │   ├── spiderdal.py             # Digital Assets
    │   └── login.py                 # Authentication
    │
    ├── helpers/                     # Utility functions
    │   ├── __init__.py
    │   ├── auth.py                  # Authentication helpers
    │   ├── banner.py                # UI banner
    │   ├── gmaps.py                 # Google Maps helpers
    │   ├── playgames.py             # Play Games helpers
    │   └── ... (other helpers)
    │
    ├── objects/                     # Data structures
    │   ├── __init__.py
    │   ├── base.py                  # Base classes
    │   ├── apis.py                  # API objects
    │   ├── session.py               # Session management
    │   └── encoders.py              # JSON encoders
    │
    ├── parsers/                     # Response parsers
    │   ├── __init__.py
    │   ├── calendar.py              # Calendar parser
    │   ├── drive.py                 # Drive parser
    │   ├── people.py                # People parser
    │   └── ... (other parsers)
    │
    ├── knowledge/                   # Knowledge base
    │   ├── __init__.py
    │   ├── drive.py                 # Drive knowledge
    │   ├── iam.py                   # IAM permissions
    │   └── keys.py                  # API keys
    │
    ├── lib/                         # Library utilities
    │   ├── __init__.py
    │   └── httpx.py                 # HTTP client wrapper
    │
    └── protos/                      # Protocol buffers
        └── __init__.py
```

---

## Dependencies

### Core Dependencies

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-dotenv==1.0.0
requests==2.31.0
```

### GHunt Dependencies

```
httpx[http2]==0.27.2        # Async HTTP client with HTTP/2 support
geopy==2.4.1                # Geolocation library
imagehash==4.3.1            # Image hashing
pillow==12.1.0              # Image processing
python-dateutil==2.9.0      # Date utilities
rich==13.9.1                # Terminal formatting
beautifulsoup4==4.12.3      # HTML parsing
alive-progress==3.1.5       # Progress bars
protobuf==5.28.2            # Protocol buffers
autoslot==2022.12.1        # Memory optimization
humanize==4.10.0            # Human-readable formatting
inflection==0.5.1           # String transformations
jsonpickle==3.3.0           # JSON serialization
packaging==24.1             # Package version handling
rich-argparse==1.5.2        # Rich CLI arguments
dnspython==2.7.0            # DNS library
```

---

## Configuration Reference

### Environment Variables

See `.env.example` for all options:

```env
# GHunt Settings
GHUNT_ENABLED=True                    # Enable/disable GHunt
GHUNT_CREDS_PATH=.ghunt_creds        # Credentials file location
GHUNT_CACHE_DIR=.ghunt_cache         # Cache directory

# Google Authentication (choose ONE)
GOOGLE_OAUTH_TOKEN=...               # OAuth2 token
GOOGLE_MASTER_TOKEN=...              # Master token
GOOGLE_COOKIES=...                   # Browser cookies

# Other OSINT Sources
GRAVATAR_ENABLED=True
HOLEHE_ENABLED=True
XPOSED_ENABLED=True
INTELBASE_ENABLED=True
```

### Python Configuration

Access configuration in code:

```python
from config import config

# Get GHunt config
ghunt_config = config.get_ghunt_config()
print(f"GHunt enabled: {ghunt_config['enabled']}")
print(f"Version: {ghunt_config['version']}")

# Get OSINT sources
sources = config.get_osint_sources()
for source, enabled in sources.items():
    print(f"{source}: {enabled}")
```

---

## Troubleshooting

### Authentication Issues

**Error**: "Not logged in"
```
Solution: Verify Google credentials in .env
- Check GOOGLE_OAUTH_TOKEN format (should start with oauth2_4/)
- Or check GOOGLE_MASTER_TOKEN format (should start with aas_et/)
- Use GHunt Companion extension to regenerate tokens
```

**Error**: "Invalid credentials"
```
Solution: Tokens may have expired
- Regenerate using GHunt Companion extension
- Update .env with new credentials
- Restart application
```

### Connection Issues

**Error**: "Connection timeout"
```
Solution:
- Check internet connectivity
- Verify firewall settings
- Increase API_TIMEOUT in .env
```

### Module Import Issues

**Error**: "No module named 'ghunt'"
```
Solution:
- Verify virtual environment is activated
- Run: pip install -r requirements.txt
- Check Python version (3.10+ required)
```

---

## Security Considerations

### Best Practices

1. **Keep credentials secure**:
   - Never commit `.env` to version control
   - Use `.gitignore` to exclude sensitive files
   - Rotate tokens regularly

2. **API Key management**:
   - Use strong, unique API keys
   - Implement rate limiting
   - Monitor API usage

3. **Data privacy**:
   - Comply with local privacy laws
   - Obtain proper authorization
   - Protect collected data

### Important Notes

⚠️ **GHunt is AGPL-3.0 licensed**
- Must comply with AGPL-3.0 requirements
- Source code modifications must be shared
- For commercial use, consult legal advice

---

## Performance Tips

1. **Enable caching**:
   ```env
   CACHE_ENABLED=True
   CACHE_TTL=3600
   ```

2. **Increase workers**:
   ```env
   ASYNC_WORKERS=20
   ```

3. **Batch requests**:
   - Group multiple investigations
   - Avoid rate limiting

---

## Support & Resources

### Documentation
- GHunt Wiki: https://github.com/mxrch/GHunt/wiki
- kangHunt Docs: [See main README.md](README.md)

### Community
- GHunt Issues: https://github.com/mxrch/GHunt/issues
- kangHunt Issues: https://github.com/Syedkashaf/kangHunt_base_v1/issues

### License
- GHunt: AGPL-3.0
- kangHunt: MIT

---

**Last Updated**: 2026-07-10  
**GHunt Version**: 2.3.4 (Spider Edition)  
**kangHunt Version**: 1.1.0  
