# kangHunt_base_v1

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GHunt v2.3.4](https://img.shields.io/badge/GHunt-v2.3.4-red.svg)](https://github.com/mxrch/GHunt)
[![Status: Active Development](https://img.shields.io/badge/Status-Active%20Development-brightgreen.svg)](#)
[![Platform: Linux/macOS/Windows/Termux](https://img.shields.io/badge/Platform-Linux%2FmacOS%2FWindows%2FTermux-blue.svg)](#)

**A Modular, Production-Grade OSINT Intelligence Gathering Framework with integrated GHunt v2.3.4**

🔍 Unified reconnaissance | 📊 Multiple data sources | ⚡ Async processing | 🔐 Secure by default | 🕷️ GHunt Integration

[Features](#features) • [Installation](#installation) • [Quick Start](#quick-start) • [GHunt Setup](#ghunt-setup) • [Documentation](#usage-guide) • [Contributing](#contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [What's New in v1.1.0](#whats-new-in-v110)
- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [GHunt Setup & Configuration](#ghunt-setup--configuration)
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
- [Credits & Attribution](#credits--attribution)
- [License](#license)

---

## Overview

**kangHunt_base_v1** is an advanced, modular OSINT (Open Source Intelligence) framework designed for comprehensive intelligence gathering, reconnaissance, and digital footprint analysis.

### What It Does

kangHunt_base_v1 aggregates intelligence from multiple specialized OSINT services and presents a unified, threat-aware profile of any target. It combines:

- **Google Account Reconnaissance**: GHunt-based intelligence extraction (OAuth, Cookies, Master tokens)
- **Email Intelligence**: Gravatar profile data, email existence validation
- **Account Detection**: Holehe platform enumeration across 100+ services
- **Data Breach Monitoring**: XposedOrNot breach database integration
- **Social Media Footprinting**: Multi-platform presence detection
- **Comprehensive Breach Analysis**: IntelBase exposure aggregation

### Why It Exists

Modern threat intelligence requires correlation across multiple independent data sources. Manual research is time-consuming, error-prone, and incomplete. kangHunt_base_v1 automates this process with:

- **Integrated GHunt v2.3.4**: Full Google OSINT framework
- **Parallel Processing**: All queries run simultaneously
- **Automatic Correlation**: Unified intelligence profile
- **Production-Ready**: FastAPI REST API + CLI
- **Extensible Architecture**: Easy plugin system

---

## What's New in v1.1.0

### 🎉 Major Upgrades

✅ **GHunt v2.3.4 Integration**
- Direct GHunt source code integration (no external dependencies)
- Full Google account reconnaissance capabilities
- Email, Gaia ID, Drive, Calendar, and Maps intelligence
- OAuth token support and credential management

✅ **Enhanced Configuration System**
- Unified config.py for all settings
- Environment-based configuration (dev/prod/test)
- GHunt-specific configuration options
- Credentials management for Google authentication

✅ **Updated Dependencies**
- All GHunt v2.3.4 dependencies included
- Python 3.10+ support
- Async HTTP/2 support via httpx
- Enhanced rich terminal output

✅ **Project Structure Improvements**
- Added GHUNT_INTEGRATION.md documentation
- Enhanced pyproject.toml with project metadata
- Comprehensive .env.example with all options
- Modular package organization

✅ **Documentation Updates**
- GHunt authentication guide
- Integration examples
- API documentation
- Security best practices

---

## Features

### 🎯 Core Intelligence Gathering

| Feature | Description | Data Source | Version |
|---------|-------------|-------------|----------|
| **Google Account Reconnaissance** | Extract profile, emails, drive, calendar, maps data | GHunt v2.3.4 | 1.1.0+ |
| **Email Investigation** | Verify email with OAuth tokens and cookies | GHunt | 1.1.0+ |
| **Gravatar Reconnaissance** | Extract profile info, avatars, display names | Gravatar API | 1.0.0+ |
| **Email Existence Validation** | Verify email presence across 100+ platforms | Holehe | 1.0.0+ |
| **Data Breach Intelligence** | Monitor email in known breaches | XposedOrNot | 1.0.0+ |
| **Social Media Detection** | Identify GitHub, Reddit, Twitter, LinkedIn presence | Multiple APIs | 1.0.0+ |
| **Breach Database Aggregation** | Comprehensive breach exposure data | IntelBase | 1.0.0+ |

### 🚀 Technical Features

- **Direct GHunt Integration**: No pip installation needed
- **Parallel Plugin Execution**: All OSINT queries run simultaneously
- **Unified Profile Generation**: Automatically correlate data from 7+ sources
- **Threat Level Assessment**: Intelligent risk calculation
- **REST API Gateway**: FastAPI-based HTTP interface
- **CLI Client**: Beautiful terminal UI with neon colors
- **API Key Authentication**: Secure header-based auth with rate limiting
- **Async Processing**: High-performance concurrent requests
- **Error Handling**: Graceful degradation across plugins
- **Multiple Output Formats**: JSON, HTML, CSV, TXT

---

## System Requirements

### Minimum Requirements
- **Python**: 3.10+ (3.11+ recommended)
- **Memory**: 512 MB available RAM (1+ GB recommended)
- **Disk Space**: 1 GB (includes GHunt)
- **Network**: Internet connectivity required

### Supported Platforms
- ✅ Linux (Ubuntu 20.04+, Debian 11+, CentOS 8+)
- ✅ macOS (10.15+, M1/M2 supported)
- ✅ Windows 10/11 (via WSL2 recommended)
- ✅ Termux (Android 7.0+)

---

## Installation

### Quick Start (All Platforms)

```bash
# 1. Clone repository (including GHunt)
git clone https://github.com/Syedkashaf/kangHunt_base_v1.git
cd kangHunt_base_v1

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS/WSL
# OR
venv\\Scripts\\activate     # Windows

# 3. Install dependencies (includes GHunt v2.3.4)
pip install -r requirements.txt

# 4. Configure
cp .env.example .env
echo "CORE_API_KEY=your_secure_key_here" >> .env

# 5. Verify installation
python DIAGNOSTIC.py
```

### Platform-Specific Instructions

<details>
<summary><b>Windows Setup</b></summary>

1. Install Python 3.10+ from https://www.python.org/downloads/ (check "Add Python to PATH")
2. Install Git from https://git-scm.com/download/win
3. Open Command Prompt and run:
```bash
git clone https://github.com/Syedkashaf/kangHunt_base_v1.git
cd kangHunt_base_v1
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
echo CORE_API_KEY=your_key_here > .env
python DIAGNOSTIC.py
```

</details>

<details>
<summary><b>Linux/macOS Setup</b></summary>

```bash
# Ubuntu/Debian:
sudo apt update && sudo apt install -y python3.10 python3.10-venv git

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

# Clone and setup
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

## GHunt Setup & Configuration

### Authentication Methods

GHunt requires authentication to access Google services. Choose one method:

#### Method 1: OAuth Token (Recommended)
```bash
# 1. Install GHunt Companion extension:
#    Firefox: https://addons.mozilla.org/en-US/firefox/addon/ghunt-companion/
#    Chrome/Edge: Chrome Web Store

# 2. Use extension to generate OAuth token
# 3. Add to .env:
echo "GOOGLE_OAUTH_TOKEN=oauth2_4/..." >> .env
```

#### Method 2: Master Token
```bash
# Via GHunt Companion extension
echo "GOOGLE_MASTER_TOKEN=aas_et/..." >> .env
```

#### Method 3: Cookies
```bash
# Export cookies from browser
echo "GOOGLE_COOKIES=key1=value1;key2=value2" >> .env
```

### Configuration

Edit `.env` file:

```bash
# GHunt Settings
GHUNT_ENABLED=True
GHUNT_CREDS_PATH=.ghunt_creds
GHUNT_CACHE_DIR=.ghunt_cache

# Google Authentication (choose one method)
GOOGLE_OAUTH_TOKEN=oauth2_4/...
# OR
GOOGLE_MASTER_TOKEN=aas_et/...
# OR
GOOGLE_COOKIES=...
```

---

## Configuration

### Environment Variables

See `.env.example` for all options. Key variables:

```bash
# Security
CORE_API_KEY=your_api_key

# GHunt
GHUNT_ENABLED=True
GOOGLE_OAUTH_TOKEN=...

# OSINT Sources
GRAVATAR_ENABLED=True
HOLEHE_ENABLED=True
XPOSED_ENABLED=True
INTELBASE_ENABLED=True

# Performance
WORKERS=4
ASYNC_WORKERS=10
```

---

## Usage Guide

### REST API

```bash
# Start server
python -m uvicorn main:app --reload

# Query API
curl -X POST http://localhost:8000/api/v1/investigate \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"email": "target@example.com"}'
```

### CLI Client

```bash
# Simple query
python cli.py -e target@example.com

# Full investigation
python cli.py -e target@example.com --full

# Save results
python cli.py -e target@example.com -o results.json
```

---

## Architecture

```
kangHunt_base_v1/
├── ghunt/                    # GHunt v2.3.4 (integrated)
│   ├── apis/                 # Google API implementations
│   ├── modules/              # OSINT modules
│   ├── helpers/              # Utility functions
│   ├── objects/              # Data models
│   └── ...
├── kangHunt/                 # kangHunt modules
│   ├── providers/            # OSINT providers
│   ├── models/               # Data models
│   └── utils/                # Utilities
├── config.py                 # Unified configuration
├── main.py                   # FastAPI application
├── cli.py                    # CLI interface
└── requirements.txt          # Dependencies
```

---

## Credits & Attribution

### GHunt Integration
- **GHunt v2.3.4**: [mxrch/GHunt](https://github.com/mxrch/GHunt)
- **License**: AGPL-3.0
- **Author**: mxrch (@mxrchreborn)

### Original kangHunt
- **Author**: Syed Kashaf
- **Repository**: https://github.com/Syedkashaf/kangHunt_base_v1

---

## License

This project is dual-licensed:

- **kangHunt components**: MIT License
- **GHunt components**: AGPL-3.0 License (see GHUNT_INTEGRATION.md)

When using this project, ensure compliance with both licenses.

---

## Disclaimer

**For Educational and Authorized Testing Only**

This tool is designed for:
- ✅ Security research
- ✅ Authorized penetration testing
- ✅ Personal digital footprint analysis
- ✅ Authorized law enforcement investigations

Not for:
- ❌ Unauthorized access
- ❌ Privacy violations
- ❌ Illegal activities
- ❌ Harassment or stalking

---

**Version**: 1.1.0  
**Last Updated**: 2026-07-10  
**Status**: Active Development ✨
