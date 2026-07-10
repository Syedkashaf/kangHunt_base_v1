# Upgrade Notes: kangHunt_base_v1 v1.1.0

## Overview

Version 1.1.0 introduces **GHunt v2.3.4 integration**, a major enhancement to the reconnaissance capabilities of kangHunt.

---

## What's New

### 🎉 GHunt v2.3.4 Integration (Major Feature)

**Direct Source Integration**
- Complete GHunt source code embedded in `/ghunt/` directory
- No external pip installation required
- All dependencies bundled in `requirements.txt`
- Full source access for customization and debugging

**Enhanced Reconnaissance**
- Google Account investigation (email, profile, contacts)
- Google Drive file analysis
- Google Calendar event extraction
- Google Maps review analysis
- Play Games account information
- Digital Assets Links enumeration

**Authentication Methods**
- OAuth token support
- Master token authentication
- Browser cookie-based auth
- Automatic credential management

### 🔧 Configuration System Improvements

**Unified config.py**
- Centralized settings management
- Environment-based configuration (dev/prod/test)
- GHunt-specific settings
- Easy credential management

**Environment Variables**
- Comprehensive `.env.example` with all options
- GHunt authentication configuration
- OSINT source toggle switches
- Performance tuning parameters

### 📦 Dependency Updates

**Python Version**
- Minimum: Python 3.10
- Recommended: Python 3.11+
- Added: Python 3.12 support

**New Dependencies**
```
httpx[http2]==0.27.2              # Async HTTP/2 client
geopy==2.4.1                      # Geolocation
imagehash==4.3.1                  # Image analysis
pillow==12.1.0                    # Image processing
protobuf==5.28.2                  # Protocol buffers
rich-argparse==1.5.2              # CLI formatting
```

**Updated Dependencies**
- fastapi: 0.100+ → 0.104.1
- beautifulsoup4: 4.11+ → 4.12.3
- rich: 12.0+ → 13.9.1

### 📄 Documentation

**New Files**
- `GHUNT_INTEGRATION.md` - Complete GHunt setup guide
- `UPGRADE_NOTES_v1.1.0.md` - This file
- Enhanced `.env.example` with all configuration options
- Updated `pyproject.toml` with project metadata

**Updated Files**
- `README.md` - GHunt features section, setup instructions
- `requirements.txt` - GHunt dependencies
- `config.py` - New unified configuration system

### 🏗️ Project Structure

**New Directories**
```
kangHunt_base_v1/
└── ghunt/                        # ← NEW: GHunt v2.3.4
    ├── apis/                     # Google APIs
    ├── modules/                  # OSINT modules
    ├── helpers/                  # Utilities
    ├── objects/                  # Data models
    ├── parsers/                  # Response parsers
    ├── knowledge/                # Knowledge base
    ├── lib/                      # Libraries
    └── protos/                   # Protocol buffers
```

**New Files**
- `config.py` - Unified configuration
- `GHUNT_INTEGRATION.md` - GHunt documentation
- `.env.example` - Configuration template
- `UPGRADE_NOTES_v1.1.0.md` - This upgrade guide
- `pyproject.toml` - Enhanced project metadata

---

## Migration Guide

### From v1.0.x to v1.1.0

#### Step 1: Update Repository

```bash
# Fetch latest changes
git fetch origin
git checkout integrate-ghunt
# OR merge to main
git merge integrate-ghunt
```

#### Step 2: Update Virtual Environment

```bash
# Activate environment
source venv/bin/activate  # Linux/macOS
# OR
venv\\Scripts\\activate   # Windows

# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

#### Step 3: Update Configuration

```bash
# Backup old .env (if exists)
cp .env .env.backup

# Create new .env from template
cp .env.example .env

# Update with your settings
vim .env  # or use your editor
```

**Important**: Add GHunt authentication:

```env
# Choose ONE method:
GOOGLE_OAUTH_TOKEN=oauth2_4/...
# OR
GOOGLE_MASTER_TOKEN=aas_et/...
# OR
GOOGLE_COOKIES=...
```

#### Step 4: Verify Installation

```bash
# Run diagnostics
python DIAGNOSTIC.py

# Test API
python -m uvicorn main:app --reload

# Test GHunt (requires auth)
python -m ghunt email test@example.com
```

---

## Breaking Changes

⚠️ **None**: v1.1.0 is backward compatible with v1.0.x

- Existing APIs remain functional
- Configuration files are compatible
- All v1.0.x modules continue to work

---

## New Configuration Options

### GHunt Settings

```env
# Enable/disable GHunt
GHUNT_ENABLED=True

# Credentials storage
GHUNT_CREDS_PATH=.ghunt_creds
GHUNT_CACHE_DIR=.ghunt_cache

# Authentication (choose ONE)
GOOGLE_OAUTH_TOKEN=...
GOOGLE_MASTER_TOKEN=...
GOOGLE_COOKIES=...
```

### OSINT Source Toggles

```env
GRAVATAR_ENABLED=True
HOLEHE_ENABLED=True
XPOSED_ENABLED=True
INTELBASE_ENABLED=True
```

### Performance Tuning

```env
ASYNC_WORKERS=10
CACHE_ENABLED=True
CACHE_TTL=3600
```

---

## Feature Compatibility

### Existing Features (v1.0.x)

✅ **Still Available**
- REST API gateway
- CLI client
- Email investigation
- Gravatar integration
- Holehe enumeration
- XposedOrNot integration
- IntelBase aggregation
- Multiple output formats

### New Features (v1.1.0)

✨ **Now Available**
- GHunt email investigation
- Google account reconnaissance
- Google Drive analysis
- Google Calendar extraction
- Google Maps review analysis
- Gaia ID investigation
- OAuth token authentication
- Master token authentication
- Enhanced configuration system
- Improved documentation

---

## Performance Improvements

### Speed
- ⚡ Parallel async processing (GHunt modules)
- 🚀 HTTP/2 support via httpx
- 💾 Response caching with TTL

### Scalability
- 📊 Configurable worker pools
- 🔄 Automatic retry logic
- ⚙️ Rate limiting support

### Resource Usage
- 💻 Memory optimization with autoslot
- 📦 Efficient protocol buffers
- 🎯 Selective module loading

---

## Security Enhancements

### Authentication
- ✅ OAuth 2.0 token support
- ✅ Secure credential storage
- ✅ Token expiration handling

### Data Protection
- 🔐 HTTPS/TLS enforcement
- 🔒 API key validation
- 🛡️ Rate limiting

---

## Known Issues & Limitations

### GHunt Limitations

1. **Authentication Required**: GHunt modules require valid Google credentials
2. **Token Expiration**: OAuth tokens expire and need regeneration
3. **Rate Limiting**: Google APIs have rate limits
4. **AGPL License**: GHunt is AGPL-3.0, affects derivative works

### Workarounds

```python
# Catch authentication errors
try:
    result = await ghunt_module.query()
except GHuntLoginError:
    print("Re-authenticate required")
    # Regenerate token using GHunt Companion
```

---

## Rollback Instructions

If you need to rollback to v1.0.x:

```bash
# Switch to previous version
git checkout main
git reset --hard HEAD~1

# Reinstall dependencies
pip install -r requirements.txt
```

---

## Testing

### Unit Tests

```bash
pytest tests/ -v
pytest tests/ -v --cov=kangHunt
```

### Integration Tests

```bash
pytest tests/integration/ -v
pytest tests/integration/ -v -m "ghunt"
```

### Manual Testing

```bash
# Test GHunt
python -m ghunt email user@example.com

# Test API
curl -X POST http://localhost:8000/api/v1/investigate \
  -H "X-API-Key: test_key" \
  -d '{"email": "user@example.com"}'
```

---

## Support & Resources

### Documentation
- [GHunt Integration Guide](GHUNT_INTEGRATION.md)
- [Main README](README.md)
- [GHunt Wiki](https://github.com/mxrch/GHunt/wiki)

### Community
- GitHub Issues: Report bugs and request features
- GitHub Discussions: Ask questions and share ideas

### Contributing
- See [CONTRIBUTING.md] for guidelines
- Submit pull requests with improvements
- Help improve documentation

---

## Changelog

### v1.1.0 (2026-07-10)

**Added**
- ✨ GHunt v2.3.4 integration
- ✨ Unified configuration system (config.py)
- ✨ Google account reconnaissance
- ✨ OAuth token authentication
- ✨ Master token authentication
- ✨ Enhanced documentation
- ✨ GHUNT_INTEGRATION.md guide
- ✨ pyproject.toml project metadata
- ✨ Comprehensive .env.example

**Updated**
- 🔄 Python 3.10+ requirement
- 🔄 Enhanced README.md
- 🔄 Updated requirements.txt
- 🔄 Improved error handling

**Fixed**
- 🐛 Configuration management
- 🐛 Async processing
- 🐛 Error handling

### v1.0.0 (2026-07-06)

**Initial Release**
- Core OSINT framework
- Gravatar integration
- Holehe enumeration
- XposedOrNot integration
- IntelBase aggregation
- REST API gateway
- CLI client

---

## Questions?

📧 **Email**: syedkashaf2@gmail.com  
🐛 **Issues**: https://github.com/Syedkashaf/kangHunt_base_v1/issues  
💬 **Discussions**: https://github.com/Syedkashaf/kangHunt_base_v1/discussions  

---

**Version**: 1.1.0  
**Release Date**: 2026-07-10  
**Status**: Stable ✅  
