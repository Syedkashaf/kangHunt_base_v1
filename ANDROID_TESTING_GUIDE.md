#!/usr/bin/env python3
# TESTING GUIDE - KangHunt on Android (Termux)
# This guide provides step-by-step instructions for testing KangHunt on Android devices

"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║           🔥 KANGHUNT — COMPLETE ANDROID TERMUX SETUP GUIDE 🔥            ║
║                                                                            ║
║              Testing OSINT Intelligence Engine on Mobile                   ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

ANDROID_SETUP_GUIDE = """

╔════════════════════════════════════════════════════════════════════════════╗
║  PHASE 1: INSTALLING TERMUX & DEPENDENCIES                               ║
╚════════════════════════════════════════════════════════════════════════════╝

[STEP 1.1] Install Termux on Your Android Device
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

There are 3 ways to install Termux:

Option A: Google Play Store (Recommended for beginners)
  1. Open Google Play Store
  2. Search: "Termux"
  3. Install by "Fredrik Fornwall"
  4. Launch the app

Option B: F-Droid (Open Source Alternative - RECOMMENDED)
  1. Download F-Droid from: https://f-droid.org
  2. Install the APK on your device
  3. Open F-Droid → Search "Termux" → Install

Option C: GitHub Release (Latest Version)
  1. Visit: https://github.com/termux/termux-app/releases
  2. Download latest APK (termux-app-v0.x.x.apk)
  3. Install on device (Enable "Install from Unknown Sources")

⚠️ IMPORTANT: Use F-Droid or GitHub if Google Play version has issues
             Google Play version may not receive updates regularly

[STEP 1.2] Grant Termux Storage Permissions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ termux-setup-storage
→ Press "ALLOW" when permission dialog appears
→ This enables access to Android's storage


[STEP 1.3] Update Termux Package Manager
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ apt update
$ apt upgrade -y

Expected output:
  Reading package lists... Done
  Building dependency tree... Done
  The following packages will be upgraded: ...


[STEP 1.4] Install Python 3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ apt install python3 -y
$ apt install python3-pip -y

Verify installation:
$ python3 --version
$ pip --version

Expected:
  Python 3.11.x
  pip 23.x.x


[STEP 1.5] Install Git (For Repository Cloning)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ apt install git -y

Verify:
$ git --version

Expected:
  git version 2.40.x


[STEP 1.6] Install Essential Build Tools
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ apt install clang -y
$ apt install build-essential -y

(Optional but recommended for compiling packages)


╔════════════════════════════════════════════════════════════════════════════╗
║  PHASE 2: CLONING KANGHUNT PROJECT                                        ║
╚════════════════════════════════════════════════════════════════════════════╝

[STEP 2.1] Navigate to Home Directory
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ cd ~
$ pwd

Expected output:
  /data/data/com.termux/files/home


[STEP 2.2] Clone KangHunt Repository
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ git clone https://github.com/Syedkashaf/kangHunt_base_v1
$ cd kangHunt_base_v1

Verify:
$ ls -la

Expected files:
  main.py
  scanner.py
  requirements.txt
  README.md
  plugins/
  models/
  core/


[STEP 2.3] Check Directory Structure
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ tree . -L 2

Expected:
  .
  ├── main.py
  ├── scanner.py
  ├── requirements.txt
  ├── plugins/
  │   ├── base_plugin.py
  │   ├── gravatar_plugin.py
  │   ├── holehe_plugin.py
  │   ├── breach_plugin.py
  │   ├── ghunt_plugin.py
  │   ├── social_plugin.py
  │   └── intelbase_plugin.py
  ├── models/
  │   ├── schemas.py
  │   └── db_models.py
  └── core/
      ├── security.py
      └── database.py


╔════════════════════════════════════════════════════════════════════════════╗
║  PHASE 3: INSTALLING PYTHON DEPENDENCIES                                  ║
╚════════════════════════════════════════════════════════════════════════════╝

[STEP 3.1] Upgrade pip First (Recommended)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ pip install --upgrade pip

Expected:
  Successfully installed pip-24.x


[STEP 3.2] Install Project Requirements
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ pip install -r requirements.txt

⏳ This will install:
  • fastapi >= 0.100.0
  • uvicorn >= 0.22.0
  • httpx[http2] >= 0.24.0
  • pydantic >= 2.0
  • python-dotenv >= 1.0.0

⚠️ WAIT: On slower connections, this may take 5-15 minutes
        The build process may show progress bars


[STEP 3.3] Verify Installation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ pip list | grep -E "fastapi|uvicorn|httpx|pydantic|python-dotenv"

Expected output:
  fastapi                      0.100.x
  httpx                        0.24.x
  pydantic                     2.x.x
  python-dotenv                1.0.x
  uvicorn                      0.22.x


[STEP 3.4] Import Test (Make Sure Everything Works)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ python3 -c "from fastapi import FastAPI; from pydantic import BaseModel; print('✅ All dependencies loaded successfully!')"

Expected:
  ✅ All dependencies loaded successfully!

If you get import errors, run:
$ pip install --upgrade -r requirements.txt --force-reinstall


╔════════════════════════════════════════════════════════════════════════════╗
║  PHASE 4: CONFIGURING ENVIRONMENT VARIABLES                               ║
╚════════════════════════════════════════════════════════════════════════════╝

[STEP 4.1] Create .env Configuration File
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ nano .env

(Or use: cat > .env << 'EOF' ... EOF)

⚠️ Add this content to your .env file:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FastAPI Security
CORE_API_KEY=your_super_secret_android_key_12345xyz

# Optional: Third-party API Keys (Leave blank if not using)
INTELBASE_API_KEY=
GRAVATAR_API_KEY=
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Save and Exit:
  • If using nano: Press Ctrl+X → Y → Enter


[STEP 4.2] Verify .env File was Created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ cat .env

Expected:
  CORE_API_KEY=your_super_secret_android_key_12345xyz
  INTELBASE_API_KEY=
  GRAVATAR_API_KEY=


[STEP 4.3] Secure .env Permissions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ chmod 600 .env

(Only allows current user to read/write)


╔════════════════════════════════════════════════════════════════════════════╗
║  PHASE 5: TESTING KANGHUNT (Demo Mode - No Server Needed)                ║
╚════════════════════════════════════════════════════════════════════════════╝

[STEP 5.1] Quick Demo Test (Recommended First Step)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ python3 scanner.py --demo

Expected Output:
  ┌────────────────────────────────────────────────┐
  │         🔥 KangHunt OSINT Engine 🔥            │
  │                                                 │
  │  GitHub: Syedkashaf | Discord: Syedkashaf    │
  └────────────────────────────────────────────────┘

  ╭────────────────────────────────────────╮
  │ SUBJECT IDENTITY: Redacted Identity    │
  ╰────────────────────────────────────────╯

  ╭── SUBJECT OVERVIEW
  │   Target Locator  : anon_target@example.com
  │   Risk Assessment : [█░░░] LOW
  │   Google GAIA ID  : 000000000000000000000
  │   Avatar Resource : https://lh3.googleusercontent.com/...
  ╰────────────────────────────────────────╯

  ╭── LINKED IDENTITIES
  │   🐙 GitHub      ──►  Syedkashaf
  │   📸 Instagram   ──►  _bot_0x
  │   💬 Discord     ──►  Syedkashaf
  ╰────────────────────────────────────────╯

  ╭── BREACH INTELLIGENCE
  │   Total exposures found: 0
  │   ✔ Zero data leaks monitored in public indices.
  ╰────────────────────────────────────────╯

✅ SUCCESS! If you see this, the CLI is working perfectly.


╔════════════════════════════════════════════════════════════════════════════╗
║  PHASE 6: RUNNING DUAL TERMINAL MODE (Full Testing)                      ║
╚════════════════════════════════════════════════════════════════════════════╝

⚠️ IMPORTANT: Termux on Android is single-app, so we need multiple sessions.
             Use Termux's "NEW SESSION" feature or split-screen mode.

[STEP 6.1] Open Terminal 1 (Backend Server)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Option A: Create New Session in Termux
  1. Press Volume-Up + N simultaneously
  2. You'll get a new terminal session

Option B: Use tmux (Advanced)
  $ apt install tmux -y
  $ tmux new-session -s kanghunt
  $ tmux new-window -t kanghunt

In Terminal 1, run:

$ cd ~/kangHunt_base_v1
$ python3 -m uvicorn main:app --host 0.0.0.0 --port 8000

Expected Output:
  INFO:     Uvicorn running on http://0.0.0.0:8000
  INFO:     Application startup complete
  INFO:     Waiting for application startup complete

🟢 Status: Backend is running! Leave this running.


[STEP 6.2] Open Terminal 2 (CLI Client)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Volume-Up + N again to create another session, then:

$ cd ~/kangHunt_base_v1
$ python3 scanner.py

You'll be prompted:
  [?] Enter Target Intelligence Email: 

Enter a test email:
  test@example.com

Expected Response:
  ✅ Connection successful
  ✅ Scanning plugins running in parallel
  ✅ Results aggregating
  → Profile display renders on screen


[STEP 6.3] Test With Different Emails
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Try scanning multiple emails to see different results:

$ python3 scanner.py john.doe@gmail.com
$ python3 scanner.py contact@techcompany.com
$ python3 scanner.py user@university.edu


╔════════════════════════════════════════════════════════════════════════════╗
║  PHASE 7: ADVANCED ANDROID TESTING SCENARIOS                              ║
╚════════════════════════════════════════════════════════════════════════════╝

[SCENARIO 1] Testing API Directly with curl
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ apt install curl -y

Test the API endpoint directly:

$ curl -X GET "http://127.0.0.1:8000/api/v1/scan/test@example.com" \
  -H "X-API-Key: your_super_secret_android_key_12345xyz"

Expected:
  {
    "target": "test@example.com",
    "status": "success",
    "profile": {
      "full_name": "...",
      "threat_level": "Low",
      "registered_platforms": [...],
      "breached_sources": [...]
    }
  }


[SCENARIO 2] Testing with Different API Keys
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Test invalid API key (should fail):

$ curl -X GET "http://127.0.0.1:8000/api/v1/scan/test@example.com" \
  -H "X-API-Key: wrong_api_key"

Expected Error:
  {
    "detail": "Unauthorized: Invalid API Key"
  }
  HTTP Status: 401


[SCENARIO 3] Testing Rate Limiting
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Rapidly send multiple requests:

$ for i in {1..10}; do
    curl -s -X GET "http://127.0.0.1:8000/api/v1/scan/test$i@example.com" \
      -H "X-API-Key: your_super_secret_android_key_12345xyz" | head -c 50
    echo "Request $i"
    sleep 0.5
  done

After 5 requests per 60 seconds, you should see:
  HTTP 429: Too Many Requests


[SCENARIO 4] Export Reports (Data Persistence)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Terminal 2 (Scanner) will automatically create reports:

$ ls -la reports/

Expected output:
  total 12
  -rw-r--r-- 1 user user 4256 Jul  9 15:32 test@example.com_20260709_153200.json
  -rw-r--r-- 1 user user 4512 Jul  9 15:33 john.doe@gmail.com_20260709_153300.json

View a report:

$ cat reports/test@example.com_*.json | python3 -m json.tool


╔════════════════════════════════════════════════════════════════════════════╗
║  PHASE 8: TROUBLESHOOTING ANDROID-SPECIFIC ISSUES                         ║
╚════════════════════════════════════════════════════════════════════════════╝

[ISSUE 1] "ModuleNotFoundError: No module named 'fastapi'"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Solution:
$ pip install --upgrade --force-reinstall fastapi uvicorn httpx pydantic

Or reinstall everything:
$ pip install -r requirements.txt --no-cache-dir


[ISSUE 2] "Address already in use" (Port 8000)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This means port 8000 is already occupied.

Solution A: Kill the old process
$ pkill -f uvicorn

Solution B: Use a different port
$ python3 -m uvicorn main:app --port 8001
Then update scanner.py: gateway_url = "http://127.0.0.1:8001/..."

Solution C: Check what's using the port
$ netstat -tulpn | grep 8000


[ISSUE 3] "Network Failure: Core FastAPI infrastructure is offline"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This means the scanner can't connect to the backend.

Check if backend is running:
$ ps aux | grep uvicorn

If not, start it in Terminal 1:
$ python3 -m uvicorn main:app --host 0.0.0.0 --port 8000


[ISSUE 4] "CORE_API_KEY not found in .env"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Solution:
$ cat .env  # Verify it exists
$ echo "CORE_API_KEY=android_test_key_xyz" > .env
$ cat .env


[ISSUE 5] ImportError During Scanner Execution
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Solution - Check Python version:
$ python3 --version

Must be Python 3.8 or higher. If using Python 3.7:
$ apt install python3.9 -y
$ python3.9 -m pip install -r requirements.txt


[ISSUE 6] Low Storage Space
━━━━━━━━━━━━━━━━━━━━━━━━

Check available space:
$ df -h

If low (<500MB), clear Termux cache:
$ pkg clean
$ apt clean
$ rm -rf ~/.cache/*


[ISSUE 7] Connection Timeout (Plugins Taking Too Long)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Some APIs may be slow on mobile networks.

Option A: Increase timeout in scanner.py (line 270)
  with httpx.Client(timeout=180.0) as bridge:  # 180 seconds

Option B: Run locally without external APIs
  $ python3 scanner.py --demo


╔════════════════════════════════════════════════════════════════════════════╗
║  PHASE 9: PERFORMANCE OPTIMIZATION FOR ANDROID                            ║
╚════════════════════════════════════════════════════════════════════════════╝

[TIP 1] Running in Background
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Use nohup to keep running even if terminal closes:

$ nohup python3 -m uvicorn main:app --port 8000 > server.log 2>&1 &

Check logs:
$ tail -f server.log


[TIP 2] Memory Management
━━━━━━━━━━━━━━━━━━━━━━━━

Check memory usage:
$ free -h

If low, close other apps before running scans.


[TIP 3] Faster Cloning with SSH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ apt install openssh -y
$ ssh-keygen -t ed25519  # Generate SSH key
# Add public key to GitHub settings
$ git clone git@github.com:Syedkashaf/kangHunt_base_v1


[TIP 4] Using Persistent Sessions with Tmux
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ apt install tmux -y
$ tmux new-session -d -s backend "python3 -m uvicorn main:app --port 8000"
$ tmux new-session -d -s scanner "cd ~/kangHunt_base_v1 && bash"

Reconnect anytime:
$ tmux attach-session -t backend
$ tmux attach-session -t scanner


[TIP 5] Creating Android Shortcuts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Create a script: ~/run_kanghunt.sh

#!/bin/bash
cd ~/kangHunt_base_v1
python3 scanner.py

Make it executable:
$ chmod +x ~/run_kanghunt.sh

Run anytime:
$ ~/run_kanghunt.sh


╔════════════════════════════════════════════════════════════════════════════╗
║  PHASE 10: TESTING CHECKLIST                                              ║
╚════════════════════════════════════════════════════════════════════════════╝

Run through this checklist to verify everything works:

Testing Checklist:
  ☐ Step 1: Termux installed and updated
  ☐ Step 2: Python 3.8+ installed
  ☐ Step 3: All dependencies installed (pip list check)
  ☐ Step 4: .env file created with CORE_API_KEY
  ☐ Step 5: Demo mode runs (python3 scanner.py --demo)
  ☐ Step 6: Backend server starts (uvicorn main:app)
  ☐ Step 7: Scanner connects to backend
  ☐ Step 8: Basic email scan completes
  ☐ Step 9: Reports generated in reports/ folder
  ☐ Step 10: API responds to curl requests
  ☐ Step 11: Invalid API key returns 401
  ☐ Step 12: Multiple emails tested
  ☐ Step 13: No Python import errors
  ☐ Step 14: Backend logs show requests
  ☐ Step 15: All plugins execute (check raw_intel)

✅ If all boxes checked, KangHunt is fully operational on Android!


╔════════════════════════════════════════════════════════════════════════════╗
║  PHASE 11: NETWORK TESTING (Optional but Recommended)                     ║
╚════════════════════════════════════════════════════════════════════════════╝

[TEST 1] Local Network (Same WiFi)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Get your Termux device IP:
$ ifconfig | grep "inet " | grep -v 127.0.0.1

Find your IP (e.g., 192.168.1.100)

From another device on same network:
$ curl -X GET "http://192.168.1.100:8000/api/v1/scan/test@example.com" \
  -H "X-API-Key: your_super_secret_android_key_12345xyz"

✅ You can now query KangHunt from another device!


[TEST 2] Network Latency
━━━━━━━━━━━━━━━━━━━━━━

Measure request time:

$ time curl -X GET "http://127.0.0.1:8000/api/v1/scan/test@example.com" \
  -H "X-API-Key: your_super_secret_android_key_12345xyz" > /dev/null

Check real (wall clock) time - typical: 2-5 seconds


[TEST 3] Concurrent Requests
━━━━━━━━━━━━━━━━━━━━━━━━━━

Test if server handles multiple simultaneous scans:

Terminal 1:
$ python3 scanner.py email1@test.com &
$ python3 scanner.py email2@test.com &
$ python3 scanner.py email3@test.com &

All should complete without crashing.


╔════════════════════════════════════════════════════════════════════════════╗
║  QUICK START (TL;DR FOR EXPERIENCED USERS)                                ║
╚════════════════════════════════════════════════════════════════════════════╝

For users who just want to get it running fast:

$ apt update && apt upgrade -y
$ apt install python3 python3-pip git -y
$ git clone https://github.com/Syedkashaf/kangHunt_base_v1
$ cd kangHunt_base_v1
$ pip install -r requirements.txt
$ echo "CORE_API_KEY=test123" > .env
$ python3 scanner.py --demo              # Test 1: Demo mode
$ python3 -m uvicorn main:app &          # Terminal 1: Start server
$ sleep 2
$ python3 scanner.py test@example.com    # Terminal 2: Run scan


╔════════════════════════════════════════════════════════════════════════════╗
║  FAQ & ADDITIONAL RESOURCES                                               ║
╚════════════════════════════════════════════════════════════════════════════╝

Q: Can I run KangHunt 24/7 on my Android phone?
A: Yes! Use tmux or nohup to keep it running in background.
   But battery drainage will be significant. Consider using a tablet.

Q: What's the minimum Android version required?
A: Android 7.0+ is recommended. Termux works on most modern devices.

Q: Can I access KangHunt from the internet (not local only)?
A: Yes, but expose port 8000 carefully. Use a VPN or firewall.
   NEVER expose without proper security!

Q: How do I update KangHunt?
A: $ cd ~/kangHunt_base_v1
   $ git pull origin main
   $ pip install -r requirements.txt --upgrade

Q: Can I use real API keys for plugins?
A: Yes! Edit .env and add real keys for:
   - IntelBase API key
   - Gravatar API key
   But keep .env secure and never commit to git!

Q: My internet is slow. Can I disable certain plugins?
A: Edit main.py and comment out plugins you don't need.
   Example: # plugins.append(SocialMediaPlugin())

Q: How do I see server logs?
A: $ tail -f server.log
   Or add --log-level debug to uvicorn command


Useful Resources:
  📚 Termux Documentation: https://termux.com
  📚 FastAPI Docs: https://fastapi.tiangolo.com
  📚 OSINT Resources: https://osintframework.com
  📚 Python Requests: https://requests.readthedocs.io


═══════════════════════════════════════════════════════════════════════════════

                    🎉 Happy Hunting! 🎉
            Report issues at: https://github.com/Syedkashaf/kangHunt_base_v1

═══════════════════════════════════════════════════════════════════════════════
"""

if __name__ == "__main__":
    print(ANDROID_SETUP_GUIDE)
