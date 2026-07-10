#!/usr/bin/env python3
"""
Diagnostic Tool for KangHunt on Android
Verifies configuration, dependencies, and project setup.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Display a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_env_file():
    """Verify that the .env file exists and contains required API key."""
    print_header("[1] Checking .env File")
    
    env_path = Path(".env")
    
    if env_path.exists():
        print(f"✅ .env file found at: {env_path.absolute()}")
        with open(".env", "r") as f:
            content = f.read()
            print(f"\n📄 Current .env content:")
            print(f"   {content}")
        
        if "CORE_API_KEY" in content:
            print("✅ CORE_API_KEY is set")
            api_key = os.getenv("CORE_API_KEY")
            if api_key:
                print(f"✅ API Key loaded: {api_key[:10]}..." if len(api_key) > 10 else f"✅ API Key loaded: {api_key}")
            else:
                print("❌ ERROR: .env file has CORE_API_KEY but it's not loaded in Python!")
                print("   → Try: pip install --upgrade python-dotenv")
                return False
        else:
            print("❌ ERROR: CORE_API_KEY not found in .env")
            return False
    else:
        print(f"❌ .env file NOT found!")
        print(f"   Current directory: {Path.cwd()}")
        print(f"   Expected path: {env_path.absolute()}")
        return False
    
    return True

def check_dependencies():
    """Verify all required Python packages are installed."""
    print_header("[2] Checking Python Dependencies")
    
    required_packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("httpx", "HTTPX"),
        ("pydantic", "Pydantic"),
        ("dotenv", "python-dotenv"),
    ]
    
    all_installed = True
    for package, display_name in required_packages:
        try:
            __import__(package)
            print(f"✅ {display_name} installed")
        except ImportError:
            print(f"❌ {display_name} NOT installed")
            all_installed = False
    
    return all_installed

def check_project_files():
    """Verify that all required source files exist in the project."""
    print_header("[3] Checking Project Files")
    
    required_files = [
        "main.py",
        "scanner.py",
        "requirements.txt",
        "models/schemas.py",
        "models/__init__.py",
        "plugins/base_plugin.py",
        "plugins/gravatar_plugin.py",
        "plugins/holehe_plugin.py",
        "plugins/breach_plugin.py",
        "plugins/ghunt_plugin.py",
        "plugins/social_plugin.py",
        "plugins/intelbase_plugin.py",
        "plugins/__init__.py",
        "core/security.py",
        "core/__init__.py",
    ]
    
    all_exist = True
    for filepath in required_files:
        if Path(filepath).exists():
            print(f"✅ {filepath}")
        else:
            print(f"❌ {filepath} MISSING")
            all_exist = False
    
    return all_exist

def check_imports():
    """Verify that critical Python modules can be imported successfully."""
    print_header("[4] Checking Python Imports")
    
    try:
        from models.schemas import NormalizedScanReport, UnifiedProfile, PluginResponse
        print("✅ models.schemas imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import models.schemas: {e}")
        return False
    
    try:
        from plugins.base_plugin import BaseOSINTPlugin
        print("✅ plugins.base_plugin imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import plugins.base_plugin: {e}")
        return False
    
    try:
        from plugins.gravatar_plugin import GravatarPlugin
        from plugins.holehe_plugin import HolehePlugin
        from plugins.breach_plugin import BreachPlugin
        from plugins.ghunt_plugin import GHuntPlugin
        from plugins.social_plugin import SocialMediaPlugin
        from plugins.intelbase_plugin import IntelBasePlugin
        print("✅ All plugins imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import plugins: {e}")
        return False
    
    return True

def check_api_server():
    """Verify the FastAPI server and its configuration."""
    print_header("[5] Checking FastAPI Server")
    
    try:
        from fastapi import FastAPI
        from main import app, plugins, API_KEY
        
        print(f"✅ FastAPI app initialized")
        print(f"✅ App title: {app.title}")
        print(f"✅ Number of plugins loaded: {len(plugins)}")
        
        if API_KEY:
            print(f"✅ API_KEY configured: {API_KEY[:10]}..." if len(API_KEY) > 10 else f"✅ API_KEY configured: {API_KEY}")
        else:
            print(f"❌ API_KEY is None or empty!")
            print(f"   → The server will reject all requests")
            return False
        
        # Verify the main scan endpoint is registered
        routes = [route.path for route in app.routes]
        if "/api/v1/scan/{target}" in routes:
            print(f"✅ Scan endpoint registered: /api/v1/scan/{{target}}")
        else:
            print(f"❌ Scan endpoint NOT found!")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Error checking FastAPI server: {e}")
        return False

def print_troubleshooting():
    """Display common issues and their solutions."""
    print_header("[6] Troubleshooting Guide")
    
    print("""
🔧 COMMON ISSUES & FIXES:

1️⃣  "CORE_API_KEY not found in .env"
    → Run: echo "CORE_API_KEY=android_test_key_xyz" > .env
    → Then: cat .env  (verify it was created)

2️⃣  "Access Denied: Subsystem rejected the X-API-Key credentials"
    → You're in the WRONG directory (nested kantHunt_base_v1 folder)
    → Run: cd ~/kangHunt_base_v1
    → Verify: ls -la  (should show main.py, scanner.py, .env)
    → Check: cat .env  (make sure CORE_API_KEY is there)

3️⃣  "ModuleNotFoundError: No module named 'fastapi'"
    → Run: pip install -r requirements.txt

4️⃣  "Connection refused" on port 8000
    → Server isn't running in Terminal 1
    → Start it: python3 -m uvicorn main:app --port 8000

5️⃣  "Port 8000 already in use"
    → Kill old process: pkill -f uvicorn
    → Or use different port: python3 -m uvicorn main:app --port 8001

6️⃣  Still getting errors?
    → Check server logs (Terminal 1) for detailed error messages
    → Run this script again to see all diagnostics
    """)

def main():
    """Execute all diagnostic checks and display summary."""
    print("\n" + "="*60)
    print("  🔍 KangHunt Diagnostic Tool (Android Termux)")
    print("="*60)
    
    checks = [
        ("Environment File", check_env_file),
        ("Dependencies", check_dependencies),
        ("Project Files", check_project_files),
        ("Python Imports", check_imports),
        ("FastAPI Server", check_api_server),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n❌ Error during {name} check: {e}")
            results[name] = False
    
    print_troubleshooting()
    
    print_header("📊 SUMMARY")
    
    all_passed = True
    for name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False
    
    print()
    if all_passed:
        print("✅ All checks passed! Your KangHunt setup is ready.")
        print("\n   Next steps:")
        print("   1. Terminal 1: python3 -m uvicorn main:app --port 8000")
        print("   2. Terminal 2: python3 scanner.py test@example.com")
    else:
        print("❌ Some checks failed. Fix the issues above and run this script again.")
    
    print()

if __name__ == "__main__":
    main()
