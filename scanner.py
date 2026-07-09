#!/usr/bin/env python3
"""
INTELBASE — Termux Recon Unit
CLI client for the local INTELBASE scan API.
Run with --demo to preview the advanced layout instantly.
"""

import sys
import re
import logging
from datetime import datetime
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# =========================================================================
# LOAD ENVIRONMENT VARIABLES - HANDLE NESTED DIRECTORIES
# =========================================================================
# Try multiple paths to find .env (in case of nested directories)
env_paths = [
    Path(".env"),                    # Current directory
    Path("../.env"),                 # Parent directory
    Path("../../.env"),              # Two levels up
]

for env_file in env_paths:
    if env_file.exists():
        load_dotenv(env_file)
        print(f"[✓] Loaded .env from: {env_file.absolute()}")
        break

# =========================================================================
# COLOR ENGINE — Ultra-Vibrant Neon Cyberpunk Palette (24-bit True Color)
# =========================================================================
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

def rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

# Core Interface Colors
GREEN = rgb(0, 255, 136)    # Neon Lime
RED = rgb(255, 0, 85)       # Neon Crimson
YELLOW = rgb(255, 213, 0)   # Cyber Gold
BLUE = rgb(0, 140, 255)     # Electric Blue
CYAN = rgb(0, 255, 255)     # Pure Cyan
MAGENTA = rgb(255, 0, 212)  # Hot Pink
WHITE = rgb(240, 240, 245)
GRAY = rgb(140, 140, 150)

# Brand-accurate colors for recognized platforms
GITHUB_CLR = rgb(230, 230, 235)
INSTAGRAM_CLR = rgb(225, 48, 108)
DISCORD_CLR = rgb(88, 101, 242)
TWITTER_CLR = rgb(29, 155, 240)
TELEGRAM_CLR = rgb(41, 181, 246)
LINKEDIN_CLR = rgb(10, 102, 194)
REDDIT_CLR = rgb(255, 69, 0)

logging.getLogger("httpx").setLevel(logging.WARNING)

try:
    import httpx
except ImportError:
    print(f"{RED}[!] Missing Dependency: 'httpx' library not found.{RESET}")
    print(f"[*] Resolution: Run 'pip install httpx'{RESET}")
    sys.exit(1)

# =========================================================================
# ADVANCED LAYOUT ENGINE
# =========================================================================
WIDTH = 62 

def section_header(title, color=WHITE):
    print(f" {color}╭── {BOLD}{title}{RESET}")

def row(text, color=WHITE):
    print(f" {color}│{RESET}   {text}")
    
def end_section(color=WHITE):
    print(f" {color}╰{"─" * (WIDTH - 4)}{RESET}\n")

def display_engine_banner():
    # Sleek "Kashif" ASCII Art (Case Sensitive) wrapped in a 6-color Neon Gradient
    print("\n")
    print(f"        {RED}888    d8P{BLUE}         {GREEN}         {YELLOW}888      {CYAN}d8b {MAGENTA} .d888{RESET}")
    print(f"        {RED}888   d8P {BLUE}         {GREEN}         {YELLOW}888      {CYAN}Y8P {MAGENTA}d88P\" {RESET}")
    print(f"        {RED}888  d8P  {BLUE}         {GREEN}         {YELLOW}888      {CYAN}    {MAGENTA}888   {RESET}")
    print(f"        {RED}888d88K   {BLUE} 8888b.  {GREEN} .d8888b{YELLOW} 88888b.  {CYAN}888 {MAGENTA}888888{RESET}")
    print(f"        {RED}8888888b  {BLUE}    \"88b {GREEN} 88K    {YELLOW} 888 \"88b {CYAN}888 {MAGENTA}888   {RESET}")
    print(f"        {RED}888  Y88b {BLUE}.d888888 {GREEN} \"Y8888b.{YELLOW}888  888 {CYAN}888 {MAGENTA}888   {RESET}")
    print(f"        {RED}888   Y88b{BLUE}888  888 {GREEN}      X88{YELLOW}888  888 {CYAN}888 {MAGENTA}888   {RESET}")
    print(f"        {RED}888    Y88b{BLUE}\"Y888888{GREEN}  88888P'{YELLOW}888  888 {CYAN}888 {MAGENTA}888   {RESET}")
    print("\n")
    
    # Ultra-bold, compact social media card
    gh = f"{BOLD}{GITHUB_CLR}GitHub:Syedkahaf{RESET}"
    ig = f"{BOLD}{INSTAGRAM_CLR}Instagram:_bot_0x{RESET}"
    dc = f"{BOLD}{DISCORD_CLR}Discord:Syedkashaf{RESET}"
    
    print(f" {gh} {BOLD}{DIM}|{RESET} {ig} {BOLD}{DIM}|{RESET} {dc}")
    print(f"\n{DIM}  {"─" * (WIDTH - 4)}{RESET}\n")

def risk_meter(level):
    lvl = str(level).strip().lower()
    tiers = {
        "low": (1, GREEN),
        "moderate": (2, YELLOW),
        "medium": (2, YELLOW),
        "high": (3, RED),
        "critical": (4, RED),
    }
    filled, color = tiers.get(lvl, (1, GREEN))
    bar = "█" * filled + "░" * (4 - filled)
    label = level.upper() if isinstance(level, str) else str(level)
    return f"{color}{BOLD}[{bar}] {label}{RESET}"

# =========================================================================
# PLATFORM RECOGNITION
# =========================================================================
KNOWN_PLATFORMS = {
    "github": {"label": "GitHub", "icon": "🐙", "color": GITHUB_CLR},
    "instagram": {"label": "Instagram", "icon": "📸", "color": INSTAGRAM_CLR},
    "discord": {"label": "Discord", "icon": "💬", "color": DISCORD_CLR},
    "twitter": {"label": "Twitter/X", "icon": "🐦", "color": TWITTER_CLR},
    "x": {"label": "Twitter/X", "icon": "🐦", "color": TWITTER_CLR},
    "telegram": {"label": "Telegram", "icon": "📡", "color": TELEGRAM_CLR},
    "linkedin": {"label": "LinkedIn", "icon": "💼", "color": LINKEDIN_CLR},
    "reddit": {"label": "Reddit", "icon": "👾", "color": REDDIT_CLR},
}

_URL_PATTERNS = {
    "github": re.compile(r"github\.com/([\w\-.]+)", re.I),
    "instagram": re.compile(r"instagram\.com/([\w.]+)", re.I),
    "discord": re.compile(r"discord(?:app)?\.(?:com|gg)/(?:users/)?([\w\-#]+)", re.I),
    "twitter": re.compile(r"(?:twitter|x)\.com/([\w]+)", re.I),
    "telegram": re.compile(r"t(?:elegram)?\.me/([\w]+)", re.I),
    "linkedin": re.compile(r"linkedin\.com/in/([\w\-]+)", re.I),
    "reddit": re.compile(r"reddit\.com/u(?:ser)?/([\w\-]+)", re.I),
}

def parse_platform_entry(entry):
    if isinstance(entry, dict):
        key = str(entry.get("platform") or entry.get("site") or entry.get("name") or "").strip().lower()
        user = entry.get("username") or entry.get("user") or entry.get("handle") or entry.get("url") or "N/A"
        if key in KNOWN_PLATFORMS:
            return key, str(user)
        label = entry.get("platform") or entry.get("site") or "Unknown"
        return None, f"{label}: {user}"

    text = str(entry).strip()
    for sep in (":", " - ", "→"):
        if sep in text:
            label, _, value = text.partition(sep)
            if label.strip().lower() in KNOWN_PLATFORMS:
                return label.strip().lower(), value.strip()

    for key, pattern in _URL_PATTERNS.items():
        match = pattern.search(text)
        if match:
            return key, match.group(1)

    return None, text

# =========================================================================
# PROFILE RENDERER — Zero Truncation, Dynamic Word Wrap
# =========================================================================
def render_profile(payload):
    profile = payload.get("profile", {})
    name = (profile.get("display_name") or profile.get("full_name")
            or profile.get("username") or "Unknown Identity")
            
    # High-tech standalone identifier block
    print(f" {CYAN}╭{"─" * (WIDTH - 4)}╮{RESET}")
    print(f" {CYAN}│{RESET} {BOLD}{WHITE}SUBJECT IDENTITY:{RESET} {name}") 
    print(f" {CYAN}╰{"─" * (WIDTH - 4)}╯{RESET}\n")

    threat = profile.get("threat_level", "Low")
    gaia = profile.get("gaia_id") or "Not Linked / Hidden"
    avatar = profile.get("avatar_url") or "None"

    section_header("SUBJECT OVERVIEW", GREEN)
    # Outputting full unmodified text for absolute accuracy (links will wrap natively in Termux)
    row(f"{BOLD}Target Locator{RESET}  : {payload.get('target')}", GREEN)
    row(f"{BOLD}Risk Assessment{RESET} : {risk_meter(threat)}", GREEN)
    row(f"{BOLD}Google GAIA ID{RESET}  : {GRAY}{gaia}{RESET}", GREEN)
    row(f"{BOLD}Avatar Resource{RESET} : {GRAY}{avatar}{RESET}", GREEN)
    end_section(GREEN)

    platforms = profile.get("registered_platforms", [])
    section_header("LINKED IDENTITIES", CYAN)
    if not platforms:
        row(f"{YELLOW}o{RESET} No public application accounts mapped.", CYAN)
    else:
        for entry in platforms:
            key, value = parse_platform_entry(entry)
            if key:
                meta = KNOWN_PLATFORMS[key]
                row(f"{meta['icon']}  {meta['color']}{BOLD}{meta['label']:<10}{RESET} ──►  {BOLD}{value}{RESET}", CYAN)
            else:
                row(f"{GREEN}✔{RESET} {value}", CYAN)
    end_section(CYAN)

    breaches = profile.get("breached_sources", [])
    total = profile.get("total_breaches_found", len(breaches))
    section_header("BREACH INTELLIGENCE", RED)
    row(f"Total exposures found: {BOLD}{total}{RESET}", RED)
    if breaches:
        for source in breaches:
            row(f"{RED}✘{RESET} Compromised Source: {BOLD}{source}{RESET}", RED)
    else:
        row(f"{GREEN}✔{RESET} Zero data leaks monitored in public indices.", RED)
    end_section(RED)

    print(f"{DIM}  [✓] Intelligence gathering completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}\n")

# =========================================================================
# DEMO DATA (ANONYMIZED TEST FIXTURE)
# =========================================================================
DEMO_PAYLOAD = {
    "target": "anon_target@example.com",
    "profile": {
        "full_name": "Redacted Identity",
        "gaia_id": "000000000000000000000",
        "avatar_url": "https://lh3.googleusercontent.com/a/default-placeholder-identity-string",
        "threat_level": "Low",
        "registered_platforms": [
            {"platform": "github", "username": "Syedkashaf"},
            {"platform": "instagram", "username": "_bot_0x"},
            {"platform": "discord", "username": "Syedkashaf"},
        ],
        "breached_sources": [],
        "total_breaches_found": 0,
    },
}

# =========================================================================
# CLIENT ENTRYPOINT
# =========================================================================
def run_client():
    display_engine_banner()

    if "--demo" in sys.argv:
        print(f"  {YELLOW}[*] Demo mode — rendering a sample profile, no network call made.{RESET}\n")
        render_profile(DEMO_PAYLOAD)
        return

    try:
        if len(sys.argv) < 2:
            target_email = input(f"  {BOLD}[?] Enter Target Intelligence Email: {RESET}").strip()
        else:
            target_email = sys.argv[1]

        if not target_email:
            print(f"  {RED}{BOLD}[!] Execution Error: Target specification cannot be null.{RESET}")
            return
            
        print(f"\n  {BLUE}[*] Establishing socket connection to local gateway api...{RESET}")
        print(f"  {BLUE}[*] Orchestrating asynchronous intelligence tasks... (Please wait){RESET}\n")

        gateway_url = f"http://127.0.0.1:8000/api/v1/scan/{target_email}"
        request_headers = {"X-API-Key": os.getenv("CORE_API_KEY")}

        with httpx.Client(timeout=105.0) as bridge:
            api_response = bridge.get(gateway_url, headers=request_headers)

        if api_response.status_code == 401:
            print(f"  {RED}{BOLD}[!] Access Denied: Subsystem rejected the X-API-Key credentials.{RESET}")
            print(f"  {YELLOW}[*] Debugging: Check that CORE_API_KEY in .env matches what's running on the server.{RESET}")
            return
        elif api_response.status_code != 200:
            print(f"  {RED}{BOLD}[!] Pipeline Failure: Node communication exception (Code: {api_response.status_code}).{RESET}")
            print(f"  {YELLOW}[*] Response: {api_response.text}{RESET}")
            return

        payload = api_response.json()
        render_profile(payload)

    except httpx.ConnectError:
        print(f"  {RED}{BOLD}[!] Network Failure: Core FastAPI infrastructure is offline.{RESET}")
        print(f"  {YELLOW}[*] Fix: Ensure 'uvicorn main:app' is running in your separate server session tab.{RESET}")
    except KeyboardInterrupt:
        print(f"\n  {RED}[!] Aborted by user.{RESET}")
    except Exception as hardware_exception:
        print(f"  {RED}{BOLD}[!] Fatal Client Parsing Exception: {str(hardware_exception)}{RESET}")

if __name__ == "__main__":
    run_client()
