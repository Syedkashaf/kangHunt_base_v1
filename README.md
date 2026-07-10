# kangHunt_base_v1

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Status: Active Development](https://img.shields.io/badge/Status-Active%20Development-brightgreen.svg)](#)
[![Platform: Linux/macOS/Windows/Termux](https://img.shields.io/badge/Platform-Linux%2FmacOS%2FWindows%2FTermux-blue.svg)](#)

**A Modular, Production-Grade OSINT Intelligence Gathering Framework**

🔍 Unified reconnaissance | 📊 Multiple data sources | ⚡ Async processing | 🔐 Secure by default

[Features](#features) • [Installation](#installation) • [Quick Start](#quick-start) • [Documentation](#usage-guide) • [Contributing](#contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [Architecture](#architecture)
- [Examples](#examples)
- [Output & Results](#output--results)
- [Troubleshooting](#troubleshooting)
- [Security](#security)
- [Performance & Optimization](#performance--optimization)
- [Development](#development)
- [Contributing](#contributing)
- [Frequently Asked Questions](#frequently-asked-questions)
- [Credits & Attribution](#credits--attribution)
- [License](#license)

---

## Overview

**kangHunt_base_v1** is an advanced, modular OSINT (Open Source Intelligence) framework designed for comprehensive intelligence gathering, reconnaissance, and digital footprint analysis.

### What It Does

kangHunt_base_v1 aggregates intelligence from multiple specialized OSINT services and presents a unified, threat-aware profile of any target email address. It combines:

- **Email Intelligence**: Gravatar profile data, email existence validation
- **Account Detection**: Holehe platform enumeration across 100+ services
- **Data Breach Monitoring**: XposedOrNot breach database integration
- **Google Account Reconnaissance**: GHunt-based intelligence extraction
- **Social Media Footprinting**: Multi-platform presence detection
- **Comprehensive Breach Analysis**: IntelBase exposure aggregation

### Why It Exists

Modern threat intelligence requires correlation across multiple independent data sources. Manual research is time-consuming, error-prone, and incomplete. kangHunt_base_v1 automates this process, running all reconnaissance tasks **in parallel** and consolidating results into a single, actionable profile.

---

## Features

### 🎯 Core Intelligence Gathering

| Feature | Description | Data Source |
|---------|-------------|-------------|
| **Gravatar Reconnaissance** | Extract profile info, avatars, display names | Gravatar API |
| **Email Existence Validation** | Verify email presence across 100+ platforms | Holehe |
| **Data Breach Intelligence** | Monitor email in known breaches | XposedOrNot |
| **Google Account Analysis** | Extract Google profile, Maps, YouTube data | GHunt |
| **Social Media Detection** | Identify GitHub, Reddit, Twitter, LinkedIn presence | Multiple APIs |
| **Breach Database Aggregation** | Comprehensive breach exposure data | IntelBase |

### 🚀 Technical Features

- **Parallel Plugin Execution**: All OSINT queries run simultaneously
- **Unified Profile Generation**: Automatically correlate data from 6+ sources
- **Threat Level Assessment**: Intelligent risk calculation
- **REST API Gateway**: FastAPI-based HTTP interface
- **CLI Client**: Beautiful terminal UI with neon colors
- **API Key Authentication**: Secure header-based auth with rate limiting
- **Async Processing**: High-performance concurrent requests
- **Error Handling**: Graceful degradation across plugins

---

## System Requirements

### Minimum Requirements
- **Python**: 3.8+ (3.10+ recommended)
- **Memory**: 256 MB available RAM
- **Disk Space**: 500 MB
- **Network**: Internet connectivity required

### Supported Platforms
- ✅ Linux (Ubuntu, Debian, CentOS, Fedora)
- ✅ macOS (10.15+)
- ✅ Windows 10/11 (via WSL2 recommended)
- ✅ Termux (Android 7.0+)

---

## Installation

### Quick Start (All Platforms)

```bash
# 1. Clone repository
git clone https://github.com/Syedkashaf/kangHunt_base_v1.git
cd kangHunt_base_v1

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS/WSL
# OR
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure
echo "CORE_API_KEY=your_secure_key_here" > .env

# 5. Verify
python DIAGNOSTIC.py
```

### Platform-Specific Instructions

<details>
<summary><b>Windows Setup</b></summary>

1. Install Python 3.8+ from https://www.python.org/downloads/ (check "Add Python to PATH")
2. Install Git from https://git-scm.com/download/win
3. Open Command Prompt and run:
```bash
git clone https://github.com/Syedkashaf/kangHunt_base_v1.git
cd kangHunt_base_v1
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
echo CORE_API_KEY=your_key_here > .env
python DIAGNOSTIC.py
```

</details>

<details>
<summary><b>Linux/macOS Setup</b></summary>

```bash
# Ubuntu/Debian:
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git

# macOS:
brew install python@3.11 git

# Then:
git clone https://github.com/Syedkashaf/kangHunt_base_v1.git
cd kangHunt_base_v1
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "CORE_API_KEY=your_secure_key_here" > .env
python DIAGNOSTIC.py
```

</details>

<details>
<summary><b>Termux (Android) Setup</b></summary>

```bash
# Install Termux from F-Droid (not Google Play)
termux-setup-storage  # Grant storage permission
pkg update && pkg upgrade -y
pkg install python3 python3-pip git -y

# Then follow standard installation
git clone https://github.com/Syedkashaf/kangHunt_base_v1.git
cd kangHunt_base_v1
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "CORE_API_KEY=your_secure_key_here" > .env
python DIAGNOSTIC.py
```

</details>

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Core API authentication
CORE_API_KEY=your_secure_admin_key_here

# Optional: IntelBase API access
INTELBASE_API_KEY=your_intelbase_api_key_here
```

### Best Practices

1. **Generate Strong Keys**:
   ```bash
   # Linux/macOS:
   openssl rand -hex 32
   ```

2. **Protect .env File**:
   ```bash
   chmod 600 .env
   ```

3. **Never commit .env** (already in .gitignore)

---

## Usage Guide

### Terminal 1: Start Server

```bash
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate     # Windows

python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

### Terminal 2: Run Scans

```bash
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate     # Windows

# Scan an email
python scanner.py target@example.com

# Demo mode
python scanner.py --demo

# Interactive mode
python scanner.py
```

### API Access

```bash
# Using curl
curl -H "X-API-Key: your_key_here" \
  "http://127.0.0.1:8000/api/v1/scan/target@example.com"
```

---

## Architecture

### System Flow

```
User Input
    ↓
[scanner.py - CLI Client]
    ↓
[HTTP Request with X-API-Key header]
    ↓
[main.py - FastAPI Gateway]
    ├─ Validate API key
    ├─ Apply rate limiting (5 req/min)
    └─ Orchestrate plugins
    ↓
[Parallel Plugin Execution via asyncio]
    ├─ GravatarPlugin
    ├─ HolehePlugin
    ├─ BreachPlugin
    ├─ GHuntPlugin
    ├─ SocialMediaPlugin
    └─ IntelBasePlugin
    ↓
[normalize_intelligence_payload()]
    ├─ Merge results
    ├─ Deduplicate data
    ├─ Calculate threat score
    └─ Create UnifiedProfile
    ↓
[HTTP Response - JSON]
    ↓
[render_profile()]
    └─ Beautiful terminal output
```

### Project Structure

```
kangHunt_base_v1/
├── main.py              # FastAPI REST gateway
├── scanner.py           # CLI client
├── DIAGNOSTIC.py        # Configuration checker
├── requirements.txt     # Python dependencies
├── .env                 # Configuration (create this)
├── LICENSE              # MIT License
├── README.md            # This file
│
├── core/
│   ├── security.py      # API authentication & rate limiting
│   └── database.py      # Database utilities
│
├── models/
│   ├── schemas.py       # Pydantic data models
│   └── db_models.py     # Database models
│
└── plugins/
    ├── base_plugin.py           # Abstract base class
    ├── gravatar_plugin.py       # Gravatar reconnaissance
    ├── holehe_plugin.py         # Email platform detection
    ├── breach_plugin.py         # Data breach check
    ├── ghunt_plugin.py          # Google account analysis
    ├── social_plugin.py         # Social media detection
    └── intelbase_plugin.py      # Breach database aggregation
```

---

## Examples

### Basic Usage

```bash
# Setup
git clone https://github.com/Syedkashaf/kangHunt_base_v1.git
cd kangHunt_base_v1
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "CORE_API_KEY=test_key_12345" > .env

# Run
python DIAGNOSTIC.py  # Verify setup
python -m uvicorn main:app --port 8000  # Terminal 1
python scanner.py john@example.com      # Terminal 2
```

### Creating Custom Plugin

```python
# plugins/custom_plugin.py
import httpx
from models.schemas import PluginResponse
from .base_plugin import BaseOSINTPlugin

class CustomPlugin(BaseOSINTPlugin):
    def __init__(self):
        self.source_name = "CustomSource"
    
    async def execute(self, target: str) -> PluginResponse:
        try:
            # Your reconnaissance logic
            return PluginResponse(
                source_name=self.source_name,
                status="success",
                raw_data={},
                message="Success"
            )
        except Exception as e:
            return PluginResponse(
                source_name=self.source_name,
                status="failed",
                message=str(e)
            )
```

Then register in `main.py`:

```python
from plugins.custom_plugin import CustomPlugin

plugins = [
    # ... existing plugins ...
    CustomPlugin(),
]
```

---

## Output & Results

### Terminal Output Example

```
        888    d8P         8888b.  .d8888b
        888   d8P             "88b 88K
        888  d8P  .d8888b .d888888 "Y8888b.
        888d88K   888  888 888  888      X88
        8888888b  "Y888888 "Y888888  88888P'

 ╭── SUBJECT OVERVIEW
 │   Target: john.doe@gmail.com
 │   Risk: [████] CRITICAL
 │   Google GAIA ID: 123456789
 ├── LINKED IDENTITIES
 │   🐙 GitHub ──► username
 │   📸 Instagram ──► username
 │   💼 LinkedIn ──► username
 ├── BREACH INTELLIGENCE
 │   Total exposures: 3
 │   ✘ LinkedIn 2021 Breach
 │   ✘ Facebook Data Leak
```

### API Response Format

```json
{
  "target": "target@example.com",
  "status": "success",
  "profile": {
    "full_name": "User Name",
    "avatar_url": "https://...",
    "gaia_id": "123456...",
    "threat_level": "Critical",
    "total_breaches_found": 3,
    "breached_sources": ["LinkedIn", "Facebook"],
    "registered_platforms": ["GitHub", "Instagram", "Gmail"]
  },
  "raw_intel": [...]
}
```

---

## Troubleshooting

### Common Issues

**Python not found**
```bash
python3 --version  # Use python3
# If not installed: apt install python3 (Linux) or brew install python@3.11 (macOS)
```

**Module not found**
```bash
source venv/bin/activate  # Activate virtual environment
pip install -r requirements.txt  # Install dependencies
```

**Connection refused**
```bash
# Ensure server running in Terminal 1:
python -m uvicorn main:app --port 8000
# Check with: netstat -an | grep 8000
```

**Port already in use**
```bash
pkill -f uvicorn  # Kill existing process
# Or use different port: python -m uvicorn main:app --port 8001
```

**API Key issues**
```bash
cat .env  # Verify CORE_API_KEY exists
python DIAGNOSTIC.py  # Run full diagnostic
```

**Permission denied**
```bash
chmod +x scanner.py DIAGNOSTIC.py main.py
```

---

## Security

### Safe Usage

1. **Protect API Keys**: Treat CORE_API_KEY like a password
2. **Use Virtual Environment**: Isolates dependencies
3. **Keep .env Local**: Never commit to git (in .gitignore)
4. **Localhost Only**: API binds to 127.0.0.1 by default
5. **Rate Limiting**: Built-in 5 requests/minute per key

### Privacy & Ethics

- Gathers **publicly available** information only
- Use only for authorized security research
- Comply with local OSINT regulations
- Respect platform terms of service
- Follow data protection laws (GDPR, CCPA)

---

## Performance & Optimization

### Performance Metrics

| Metric | Value |
|--------|-------|
| Avg Scan Time | 3-8 seconds |
| Parallel Plugins | 6 simultaneous |
| Memory Usage | 50-100 MB per scan |
| Max Throughput | 5 scans/minute |

### Optimization Tips

- All plugins run in parallel via `asyncio`
- Results automatically cached (optional)
- Use wired connection for Termux/Android
- Disable bandwidth-heavy applications

---

## Development

### Adding New Plugins

1. Create `plugins/your_plugin.py` inheriting from `BaseOSINTPlugin`
2. Implement `async def execute(target: str) -> PluginResponse`
3. Register in `main.py` by adding to `plugins` list
4. Update `normalize_intelligence_payload()` if needed

### Code Standards

- Use type hints for all parameters
- Write docstrings for classes/methods
- Handle exceptions gracefully
- Use async/await for I/O
- Follow PEP 8 style guide

---

## Contributing

We welcome contributions! 

1. Fork repository
2. Create feature branch: `git checkout -b feature/name`
3. Make changes with clear commits
4. Push and submit Pull Request

### Ideas for Contribution

- 🐛 Bug fixes
- ✨ New plugins for other OSINT services
- 📚 Documentation improvements
- 🎨 UI/UX enhancements
- 🧪 Tests and validation

---

## Frequently Asked Questions

**Q: Is this legal?**
A: The tool uses only publicly available data. Legal use depends on your jurisdiction, purpose, and compliance with platform terms of service. Always ensure authorized use.

**Q: Can I use this commercially?**
A: Yes, under MIT license. Must include license copy and attribution.

**Q: What about privacy?**
A: kangHunt_base_v1 gathers public OSINT only. It doesn't store data—each scan is independent. External APIs follow their own privacy policies.

**Q: How accurate are results?**
A: Results depend on API freshness, whether targets have public profiles, and each service's accuracy. Use as part of due diligence, not sole evidence.

**Q: Can I scan without internet?**
A: No. The framework requires internet to access external OSINT APIs.

**Q: How do I batch process emails?**
A: Create a file with emails, then loop:
```bash
while read email; do
    python scanner.py "$email"
done < emails.txt
```

---

## Credits & Attribution

### Author
- **Syed Kashaf** (@Syedkashaf) - Creator and Maintainer

### Third-Party Services

kangHunt_base_v1 integrates with:

- **Gravatar**: Profile reconnaissance via official API
- **Holehe**: Email platform detection  
- **XposedOrNot**: Data breach database
- **GHunt**: Google account intelligence (GPL-3.0 licensed)
- **IntelBase**: Breach exposure aggregation
- **GitHub API**: Social media detection

### Dependencies

All Python dependencies are MIT or BSD licensed:
- FastAPI (MIT)
- Uvicorn (BSD)
- Pydantic (MIT)
- httpx (BSD)
- python-dotenv (BSD)

### License Notice

**IMPORTANT**: This project integrates GHunt, which is GPL-3.0 licensed. If you distribute kangHunt_base_v1, you must:
- Include GHunt license
- Provide source code
- License derivative works under GPL-3.0

See LICENSE file for MIT license details.

---

## License

```
MIT License

Copyright (c) 2026 syedkashaf

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## Support

- 📖 Documentation: See README sections above
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions
- 📧 Contact: Check GitHub profile

### Getting Help

1. Read Troubleshooting section
2. Run `python DIAGNOSTIC.py`
3. Check existing GitHub Issues
4. Create new issue with environment details

---

<div align="center">

**Made with ❤️ for the OSINT community**

[⬆ Back to Top](#kangHunt_base_v1)

</div>
