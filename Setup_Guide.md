#!/usr/bin/env python3
# SETUP GUIDE - INTELBASE (OSINT_Advanced_Core) on Android (Termux PRoot Ubuntu)
# This guide provides foolproof, step-by-step instructions for deploying the framework inside a virtualized Ubuntu container on Android.

"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║       🔥 INTELBASE OSINT CORE — COMPLETE PROOT UBUNTU SETUP GUIDE 🔥       ║
║                                                                            ║
║            Production-Grade Deployment for Mobile Environments             ║
║                                                                            ║
╚════════════════════════════════════════════════════════���═══════════════════╝
"""

ANDROID_SETUP_GUIDE = """

╔════════════════════════════════════════════════════════════════════════════╗
║  PHASE 1: TERMUX HOST PREPARATION & VIRTUALIZATION                        ║
╚════════════════════════════════════════════════════════════════════════════╝
⚠️ WARNING: We do not run this framework directly on native Termux to avoid 
Android execution limitations. We will build a full Ubuntu container.

[STEP 1.1] Install Termux Securely
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DO NOT install Termux from the Google Play Store (it is deprecated).
  1. Download F-Droid from: https://f-droid.org
  2. Install the APK, open F-Droid, search "Termux", and install.

[STEP 1.2] Update Native Termux & Grant Storage
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Open Termux and run:
$ termux-setup-storage
→ Press "ALLOW" on the popup.
$ pkg update && pkg upgrade -y

[STEP 1.3] Install and Deploy PRoot Ubuntu
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$ pkg install proot-distro -y
$ proot-distro install ubuntu


╔════════════════════════════════════════════════════════════════════════════╗
║  PHASE 2: ENTERING UBUNTU & OS CONFIGURATION                              ║
╚════════════════════════════════════════════════════════════════════════════╝

[STEP 2.1] Login to the Ubuntu Container
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$ proot-distro login ubuntu

(Your prompt should change from '$' to 'root@localhost:~#'. You are now 
inside a full Linux environment).

[STEP 2.2] Update Ubuntu & Install Core Dependencies
━━━━━━━━━━━━━━━━━���━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Since this is a fresh Ubuntu install, we must update its internal repos:
$ apt update && apt upgrade -y

Install Python, Virtual Environment tools, and Git:
$ apt install python3 python3-pip python3-venv git nano curl -y


╔════════════════════════════════════════════════════════════════════════════╗
║  PHASE 3: CLONING THE REPOSITORY & ISOLATING THE ENVIRONMENT              ║
╚════════════════════════════════════════════════════════════════════════════╝

[STEP 3.1] Clone the Advanced Core
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$ cd ~
$ git clone https://github.com/Syedkashaf/OSINT_Advanced_Core.git
$ cd OSINT_Advanced_Core

[STEP 3.2] Create a Virtual Environment (Mandatory)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ubuntu enforces PEP-668, preventing global pip installs. We must isolate.
$ python3 -m venv venv
$ source venv/bin/activate

(You should now see '(venv) root@localhost' at the prompt).


╔════════════════════════════════════════════════════════════════════════════╗
║  PHASE 4: INSTALLING DEPENDENCIES & EXTERNAL ENGINES                      ║
╚════════════════════════════════════════════════════════════════════════════╝

[STEP 4.1] Install Project Requirements
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$ pip install --upgrade pip
$ pip install -r requirements.txt

[STEP 4.2] Install & Authenticate GHunt (Google OSINT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
The framework relies heavily on GHunt for advanced footprints.
1. Install GHunt:
$ pip install ghunt

2. Authenticate your Google Account:
$ ghunt login
→ Follow the on-screen instructions to provide your Base64 Google Cookies.


╔════════════════════════════════════════════════════════════════════════════╗
║  PHASE 5: SECRETS & CONFIGURATION MANAGEMENT                              ║
╚════════════════════════════════════════════════════════════════════════════╝

[STEP 5.1] Create .env Configuration File
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$ nano .env

Add the exact variables needed for the gateway:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Core Authentication (Required)
CORE_API_KEY=your_secure_admin_key_here

# External Services (Required for full data mapping)
INTELBASE_API_KEY=your_intelbase_key_here
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Save and Exit nano:
  • Press Ctrl+O (to output/save)
  • Press Enter (to confirm file name)
  • Press Ctrl+X (to exit)


╔════════════════════════════════════════════════════════════════════════════╗
║  PHASE 6: RUNNING THE DECOUPLED ARCHITECTURE (DUAL TERMINAL)              ║
╚════════════════════════════════════════════════════════════════════════════╝
You need TWO active Termux sessions logged into Ubuntu.

[STEP 6.1] Terminal 1: Boot the API Gateway
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$ proot-distro login ubuntu
$ cd ~/OSINT_Advanced_Core
$ source venv/bin/activate
$ python3 -m uvicorn main:app --host 127.0.0.1 --port 8000

🟢 Status: Backend is now listening. Swipe from the left edge of your screen 
and tap "New Session".

[STEP 6.2] Terminal 2: Execute the CLI Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
$ proot-distro login ubuntu
$ cd ~/OSINT_Advanced_Core
$ source venv/bin/activate

Execute a target scan:
$ python3 scanner.py target_email@gmail.com


╔════════════════════════════════════════════════════════════════════════════╗
║  TROUBLESHOOTING & RECOVERY PROCEDURES                                    ║
╚════════════════════════════════════════════════════════════════════════════╝

[ISSUE 1] "Command 'python3' not found" or "apt error"
→ You forgot to log into Ubuntu.
→ Fix: Run `proot-distro login ubuntu` before running any commands.

[ISSUE 2] "error: externally-managed-environment (PEP 668)"
→ You forgot to activate your virtual environment. 
→ Fix: Run `source venv/bin/activate`.

[ISSUE 3] "Address already in use" (Port 8000)
→ A previous backend session crashed but kept the port open.
→ Fix: Run `pkill -f uvicorn`.

[ISSUE 4] Subprocess bypasses / No Google Data Found
→ GHunt lost its authentication session.
→ Fix: Run `ghunt login` again.


═══════════════════════════════════════════════════════════════════════════════
                    🎉 Deployment Complete! 🎉
         Report issues at: https://github.com/Syedkashaf/OSINT_Advanced_Core
═══════════════════════════════════════════════════════════════════════════════
"""

if __name__ == "__main__":
    print(ANDROID_SETUP_GUIDE)
