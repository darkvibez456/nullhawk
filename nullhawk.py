#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ███╗   ██╗██╗   ██╗██╗     ██╗     ██╗  ██╗ █████╗ ██╗   ██╗██╗  ██╗  ║
║   ████╗  ██║██║   ██║██║     ██║     ██║  ██║██╔══██╗██║   ██║██║ ██╔╝  ║
║   ██╔██╗ ██║██║   ██║██║     ██║     ███████║███████║██║   ██║█████╔╝   ║
║   ██║╚██╗██║██║   ██║██║     ██║     ██╔══██║██╔══██║╚██╗ ██╔╝██╔═██╗  ║
║   ██║ ╚████║╚██████╔╝███████╗███████╗██║  ██║██║  ██║ ╚████╔╝ ██║  ██╗ ║
║   ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝ ║
║                                                              ║
║              Advanced Reconnaissance & OSINT Tool            ║
║                     Version : 1.0.0                          ║
║               Author  : darkvibez456                         ║
║               GitHub  : github.com/darkvibez456             ║
╚══════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import socket
import hashlib
import base64
import random
import string
import struct
import subprocess
import urllib.request
import urllib.error
import urllib.parse
import json
import ssl
import re
import platform
from datetime import datetime

# ─── Colors ───────────────────────────────────────────────────
class C:
    RED     = '\033[91m'
    GREEN   = '\033[92m'
    YELLOW  = '\033[93m'
    BLUE    = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN    = '\033[96m'
    WHITE   = '\033[97m'
    BOLD    = '\033[1m'
    DIM     = '\033[2m'
    RESET   = '\033[0m'
    BG_RED  = '\033[41m'
    BG_BLUE = '\033[44m'

# ─── Helpers ───────────────────────────────────────────────────
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    print(f"""{C.RED}{C.BOLD}
 ███╗   ██╗██╗   ██╗██╗     ██╗     ██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗
 ████╗  ██║██║   ██║██║     ██║     ██║  ██║██╔══██╗██║    ██║██║ ██╔╝
 ██╔██╗ ██║██║   ██║██║     ██║     ███████║███████║██║ █╗ ██║█████╔╝
 ██║╚██╗██║██║   ██║██║     ██║     ██╔══██║██╔══██║██║███╗██║██╔═██╗
 ██║ ╚████║╚██████╔╝███████╗███████╗██║  ██║██║  ██║╚███╔███╔╝██║  ██╗
 ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝
{C.RESET}""")
    print(f"{C.CYAN}{'─'*65}{C.RESET}")
    print(f"{C.YELLOW}   Advanced Reconnaissance & OSINT Tool  {C.DIM}│{C.RESET}{C.GREEN}  v1.0.0{C.RESET}")
    print(f"{C.YELLOW}   Author  : {C.WHITE}darkvibez456{C.RESET}")
    print(f"{C.YELLOW}   GitHub  : {C.BLUE}github.com/darkvibez456/nullhawk{C.RESET}")
    print(f"{C.CYAN}{'─'*65}{C.RESET}\n")

def tag(label, color=C.CYAN):
    t = datetime.now().strftime("%H:%M:%S")
    return f"{C.DIM}[{t}]{C.RESET} {color}[{label}]{C.RESET}"

def info(msg):  print(f"{tag('INFO',  C.CYAN)}    {msg}")
def ok(msg):    print(f"{tag('OK',    C.GREEN)}      {msg}")
def warn(msg):  print(f"{tag('WARN',  C.YELLOW)}    {msg}")
def err(msg):   print(f"{tag('ERROR', C.RED)}   {msg}")
def res(msg):   print(f"{tag('RESULT',C.MAGENTA)} {msg}")

def divider(title=""):
    w = 65
    if title:
        pad = (w - len(title) - 2) // 2
        print(f"\n{C.CYAN}{'─'*pad} {C.BOLD}{title}{C.RESET}{C.CYAN} {'─'*(w-pad-len(title)-2)}{C.RESET}\n")
    else:
        print(f"{C.CYAN}{'─'*w}{C.RESET}")

def pause():
    input(f"\n{C.DIM}[Press Enter to return to menu...]{C.RESET}")

def fetch(url, timeout=8):
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return r.read().decode('utf-8', errors='ignore'), r.status, dict(r.headers)
    except Exception as e:
        return None, 0, {}

def head_req(url, timeout=8):
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(url, method='HEAD', headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return r.status, dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, {}
    except Exception:
        return 0, {}

# ══════════════════════════════════════════════════════════════
#  SECTION 1 ── OSINT
# ══════════════════════════════════════════════════════════════

PLATFORMS = {
    "GitHub":       "https://github.com/{}",
    "GitLab":       "https://gitlab.com/{}",
    "Twitter/X":    "https://twitter.com/{}",
    "Instagram":    "https://www.instagram.com/{}",
    "TikTok":       "https://www.tiktok.com/@{}",
    "Reddit":       "https://www.reddit.com/user/{}",
    "Pinterest":    "https://www.pinterest.com/{}",
    "Tumblr":       "https://{}.tumblr.com",
    "Medium":       "https://medium.com/@{}",
    "Dev.to":       "https://dev.to/{}",
    "Hashnode":     "https://hashnode.com/@{}",
    "YouTube":      "https://www.youtube.com/@{}",
    "Twitch":       "https://www.twitch.tv/{}",
    "Dailymotion":  "https://www.dailymotion.com/{}",
    "SoundCloud":   "https://soundcloud.com/{}",
    "Spotify":      "https://open.spotify.com/user/{}",
    "Patreon":      "https://www.patreon.com/{}",
    "Fiverr":       "https://www.fiverr.com/{}",
    "Upwork":       "https://www.upwork.com/freelancers/~{}",
    "Behance":      "https://www.behance.net/{}",
    "Dribbble":     "https://dribbble.com/{}",
    "Flickr":       "https://www.flickr.com/people/{}",
    "500px":        "https://500px.com/p/{}",
    "Steam":        "https://steamcommunity.com/id/{}",
    "Chess.com":    "https://www.chess.com/member/{}",
    "Roblox":       "https://www.roblox.com/user.aspx?username={}",
    "Telegram":     "https://t.me/{}",
    "Keybase":      "https://keybase.io/{}",
    "HackerNews":   "https://news.ycombinator.com/user?id={}",
    "ProductHunt":  "https://www.producthunt.com/@{}",
}

def username_search():
    divider("USERNAME SEARCH")
    uname = input(f"{C.YELLOW}[?]{C.RESET} Enter username: {C.GREEN}").strip()
    print(C.RESET)
    if not uname:
        err("No username entered.")
        pause(); return

    found, nfound = [], []
    total = len(PLATFORMS)
    print(f"{C.CYAN}  Searching {total} platforms...{C.RESET}\n")

    for i, (site, tmpl) in enumerate(PLATFORMS.items(), 1):
        url = tmpl.format(uname)
        sys.stdout.write(f"\r  {C.DIM}[{i}/{total}]{C.RESET} Checking {C.CYAN}{site:<15}{C.RESET}  ")
        sys.stdout.flush()
        code, _ = head_req(url, timeout=6)
        if code in (200, 301, 302):
            found.append((site, url))
        else:
            nfound.append(site)
        time.sleep(0.05)

    print("\n")
    divider("RESULTS")
    if found:
        ok(f"Found on {C.BOLD}{len(found)}{C.RESET}{C.GREEN} platforms:{C.RESET}")
        for site, url in found:
            print(f"  {C.GREEN}✔{C.RESET}  {C.BOLD}{site:<15}{C.RESET}  {C.BLUE}{url}{C.RESET}")
    else:
        warn("Not found on any platform.")

    if nfound:
        print(f"\n  {C.DIM}Not found: {', '.join(nfound)}{C.RESET}")
    pause()

def email_validator():
    divider("EMAIL VALIDATOR")
    email = input(f"{C.YELLOW}[?]{C.RESET} Enter email: {C.GREEN}").strip()
    print(C.RESET)
    if not email:
        err("No email entered."); pause(); return

    pattern = r'^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        err(f"Invalid email format: {email}"); pause(); return

    ok(f"Format valid: {C.BOLD}{email}{C.RESET}")
    domain = email.split('@')[1]
    info(f"Domain : {C.CYAN}{domain}{C.RESET}")

    # MX check via DNS
    try:
        import dns.resolver
        mx = dns.resolver.resolve(domain, 'MX')
        ok(f"MX Records found ({len(mx)}):")
        for r in mx:
            print(f"  {C.GREEN}→{C.RESET} {r.exchange} (priority {r.preference})")
    except ImportError:
        # fallback: socket check
        try:
            ip = socket.gethostbyname(domain)
            ok(f"Domain resolves to: {C.CYAN}{ip}{C.RESET}")
        except:
            warn("Could not resolve domain MX/IP.")
    except Exception as e:
        warn(f"MX lookup failed: {e}")

    # Disposable check (basic list)
    disposable = ["mailinator","guerrillamail","tempmail","10minutemail","throwam","yopmail","maildrop"]
    if any(d in domain for d in disposable):
        warn(f"{C.YELLOW}Likely DISPOSABLE email domain!{C.RESET}")
    else:
        ok("Not a known disposable domain.")
    pause()

def phone_info():
    divider("PHONE NUMBER INFO")
    phone = input(f"{C.YELLOW}[?]{C.RESET} Enter phone (with country code e.g. +91XXXXXXXXXX): {C.GREEN}").strip()
    print(C.RESET)
    if not phone:
        err("No number entered."); pause(); return

    # Country code map
    cc_map = {
        "+1":"USA/Canada","+44":"United Kingdom","+91":"India","+92":"Pakistan",
        "+93":"Afghanistan","+880":"Bangladesh","+86":"China","+81":"Japan",
        "+82":"South Korea","+49":"Germany","+33":"France","+39":"Italy",
        "+34":"Spain","+7":"Russia","+55":"Brazil","+52":"Mexico",
        "+971":"UAE","+966":"Saudi Arabia","+20":"Egypt","+27":"South Africa",
        "+61":"Australia","+64":"New Zealand","+31":"Netherlands","+46":"Sweden",
        "+47":"Norway","+45":"Denmark","+358":"Finland","+41":"Switzerland",
        "+43":"Austria","+48":"Poland","+90":"Turkey","+62":"Indonesia",
        "+60":"Malaysia","+63":"Philippines","+66":"Thailand","+84":"Vietnam",
    }

    matched_country = "Unknown"
    for code, country in sorted(cc_map.items(), key=lambda x: -len(x[0])):
        if phone.startswith(code):
            matched_country = country
            local = phone[len(code):]
            break
    else:
        local = phone

    res(f"Number   : {C.BOLD}{phone}{C.RESET}")
    res(f"Country  : {C.CYAN}{matched_country}{C.RESET}")
    res(f"Local    : {C.WHITE}{local}{C.RESET}")
    res(f"Length   : {C.WHITE}{len(local)} digits{C.RESET}")

    if len(local) == 10:
        ok("Standard 10-digit local number.")
    elif len(local) < 7:
        warn("Number seems too short.")
    elif len(local) > 12:
        warn("Number seems too long.")
    pause()

def social_media_checker():
    divider("SOCIAL MEDIA PROFILE CHECKER")
    handle = input(f"{C.YELLOW}[?]{C.RESET} Enter handle/username: {C.GREEN}").strip()
    print(C.RESET)
    if not handle:
        err("No handle entered."); pause(); return

    socials = {
        "Twitter/X":  f"https://twitter.com/{handle}",
        "Instagram":  f"https://www.instagram.com/{handle}",
        "TikTok":     f"https://www.tiktok.com/@{handle}",
        "YouTube":    f"https://www.youtube.com/@{handle}",
        "Facebook":   f"https://www.facebook.com/{handle}",
        "Snapchat":   f"https://www.snapchat.com/add/{handle}",
        "LinkedIn":   f"https://www.linkedin.com/in/{handle}",
        "Twitch":     f"https://www.twitch.tv/{handle}",
        "Reddit":     f"https://www.reddit.com/user/{handle}",
        "Pinterest":  f"https://www.pinterest.com/{handle}",
    }

    print(f"{C.CYAN}  Checking {len(socials)} social platforms...{C.RESET}\n")
    for site, url in socials.items():
        code, _ = head_req(url)
        status = f"{C.GREEN}✔ FOUND{C.RESET}" if code in (200,301,302) else f"{C.RED}✘ NOT FOUND{C.RESET}"
        print(f"  {status}  {C.BOLD}{site:<14}{C.RESET}  {C.DIM}{url}{C.RESET}")
        time.sleep(0.1)
    pause()

def osint_menu():
    while True:
        banner()
        print(f"  {C.RED}◆{C.RESET}  {C.BOLD}OSINT TOOLS{C.RESET}\n")
        opts = [
            ("01", "Username Search",        "Search 30+ platforms"),
            ("02", "Email Validator",         "Validate & analyze email"),
            ("03", "Phone Number Info",       "Country & format info"),
            ("04", "Social Media Checker",    "Check social profiles"),
            ("00", "Back",                    "Return to main menu"),
        ]
        for num, name, desc in opts:
            c = C.RED if num=="00" else C.GREEN
            print(f"  {c}[{num}]{C.RESET}  {C.BOLD}{name:<25}{C.RESET}  {C.DIM}{desc}{C.RESET}")
        print()
        choice = input(f"{C.CYAN}NullHawk{C.RESET}{C.RED}@osint{C.RESET} ▶ ").strip()
        if choice=="1" or choice=="01": username_search()
        elif choice=="2" or choice=="02": email_validator()
        elif choice=="3" or choice=="03": phone_info()
        elif choice=="4" or choice=="04": social_media_checker()
        elif choice=="0" or choice=="00": break
        else: warn("Invalid option.")

# ══════════════════════════════════════════════════════════════
#  SECTION 2 ── WEB TOOLS
# ══════════════════════════════════════════════════════════════

def website_status():
    divider("WEBSITE STATUS CHECKER")
    url = input(f"{C.YELLOW}[?]{C.RESET} Enter URL (e.g. https://example.com): {C.GREEN}").strip()
    print(C.RESET)
    if not url:
        err("No URL entered."); pause(); return
    if not url.startswith("http"):
        url = "https://" + url

    info(f"Checking: {C.CYAN}{url}{C.RESET}")
    start = time.time()
    code, hdrs = head_req(url)
    elapsed = round((time.time()-start)*1000, 2)

    status_color = C.GREEN if 200<=code<300 else C.YELLOW if 300<=code<400 else C.RED
    res(f"Status Code : {status_color}{C.BOLD}{code}{C.RESET}")
    res(f"Response    : {C.CYAN}{elapsed} ms{C.RESET}")
    if hdrs.get('Server'):
        res(f"Server      : {C.WHITE}{hdrs['Server']}{C.RESET}")
    if hdrs.get('Content-Type'):
        res(f"Content-Type: {C.WHITE}{hdrs['Content-Type']}{C.RESET}")

    if code == 200:      ok("Website is UP and reachable!")
    elif code in (301,302): warn("Website redirects.")
    elif code == 403:    warn("403 Forbidden — server refused.")
    elif code == 404:    err("404 Not Found.")
    elif code == 500:    err("500 Internal Server Error.")
    elif code == 0:      err("Could not reach website.")
    pause()

def ssl_checker():
    divider("SSL CERTIFICATE CHECKER")
    host = input(f"{C.YELLOW}[?]{C.RESET} Enter domain (e.g. google.com): {C.GREEN}").strip()
    print(C.RESET)
    if not host:
        err("No domain entered."); pause(); return
    host = host.replace("https://","").replace("http://","").split("/")[0]

    info(f"Checking SSL for: {C.CYAN}{host}{C.RESET}")
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
            s.settimeout(8)
            s.connect((host, 443))
            cert = s.getpeercert()

        subject = dict(x[0] for x in cert['subject'])
        issuer  = dict(x[0] for x in cert['issuer'])
        exp     = cert['notAfter']
        nbf     = cert['notBefore']

        ok("SSL Certificate is VALID!")
        res(f"Common Name  : {C.CYAN}{subject.get('commonName','N/A')}{C.RESET}")
        res(f"Organization : {C.WHITE}{subject.get('organizationName','N/A')}{C.RESET}")
        res(f"Issued By    : {C.WHITE}{issuer.get('organizationName','N/A')}{C.RESET}")
        res(f"Valid From   : {C.WHITE}{nbf}{C.RESET}")
        res(f"Expires      : {C.YELLOW}{exp}{C.RESET}")

        # SANs
        sans = [v for t,v in cert.get('subjectAltName',[]) if t=='DNS']
        if sans:
            res(f"SANs ({len(sans)})    : {C.DIM}{', '.join(sans[:5])}{C.RESET}")
    except ssl.SSLCertVerificationError as e:
        err(f"SSL Verification Failed: {e}")
    except Exception as e:
        err(f"Could not get SSL info: {e}")
    pause()

def http_headers():
    divider("HTTP HEADERS ANALYZER")
    url = input(f"{C.YELLOW}[?]{C.RESET} Enter URL: {C.GREEN}").strip()
    print(C.RESET)
    if not url:
        err("No URL entered."); pause(); return
    if not url.startswith("http"):
        url = "https://" + url

    info(f"Fetching headers: {C.CYAN}{url}{C.RESET}")
    code, hdrs = head_req(url)
    if not hdrs:
        err("Could not fetch headers."); pause(); return

    ok(f"Status: {code}  |  {len(hdrs)} headers received\n")
    security = ['Strict-Transport-Security','Content-Security-Policy',
                'X-Frame-Options','X-Content-Type-Options',
                'Referrer-Policy','Permissions-Policy','X-XSS-Protection']

    for k, v in hdrs.items():
        color = C.GREEN if k in security else C.WHITE
        print(f"  {C.CYAN}{k:<35}{C.RESET} {color}{v}{C.RESET}")

    print(f"\n{C.BOLD}Security Headers:{C.RESET}")
    for sh in security:
        found = sh in hdrs
        icon  = f"{C.GREEN}✔{C.RESET}" if found else f"{C.RED}✘{C.RESET}"
        print(f"  {icon}  {sh}")
    pause()

def robots_viewer():
    divider("ROBOTS.TXT VIEWER")
    url = input(f"{C.YELLOW}[?]{C.RESET} Enter domain: {C.GREEN}").strip()
    print(C.RESET)
    if not url:
        err("No URL entered."); pause(); return
    if not url.startswith("http"):
        url = "https://" + url
    robots_url = url.rstrip("/") + "/robots.txt"

    info(f"Fetching: {C.CYAN}{robots_url}{C.RESET}\n")
    body, code, _ = fetch(robots_url)
    if code == 200 and body:
        ok(f"robots.txt found! ({len(body)} bytes)\n")
        for line in body.splitlines()[:60]:
            if line.startswith("Disallow"):
                print(f"  {C.RED}{line}{C.RESET}")
            elif line.startswith("Allow"):
                print(f"  {C.GREEN}{line}{C.RESET}")
            elif line.startswith("User-agent"):
                print(f"  {C.YELLOW}{line}{C.RESET}")
            elif line.startswith("Sitemap"):
                print(f"  {C.CYAN}{line}{C.RESET}")
            else:
                print(f"  {C.DIM}{line}{C.RESET}")
    else:
        warn("robots.txt not found or not accessible.")
    pause()

def sitemap_finder():
    divider("SITEMAP FINDER")
    url = input(f"{C.YELLOW}[?]{C.RESET} Enter domain: {C.GREEN}").strip()
    print(C.RESET)
    if not url:
        err("No URL entered."); pause(); return
    if not url.startswith("http"):
        url = "https://" + url

    paths = ["/sitemap.xml","/sitemap_index.xml","/sitemap-index.xml",
             "/wp-sitemap.xml","/news-sitemap.xml","/video-sitemap.xml",
             "/image-sitemap.xml","/post-sitemap.xml","/page-sitemap.xml"]

    found_any = False
    for path in paths:
        full = url.rstrip("/") + path
        code, _ = head_req(full)
        if code == 200:
            ok(f"Found: {C.BLUE}{full}{C.RESET}")
            found_any = True
        else:
            print(f"  {C.DIM}✘ {full}{C.RESET}")

    if not found_any:
        warn("No sitemap files found.")
    pause()

def reverse_ip():
    divider("REVERSE IP LOOKUP")
    ip = input(f"{C.YELLOW}[?]{C.RESET} Enter IP address: {C.GREEN}").strip()
    print(C.RESET)
    if not ip:
        err("No IP entered."); pause(); return

    info(f"Reverse lookup for: {C.CYAN}{ip}{C.RESET}")
    try:
        host = socket.gethostbyaddr(ip)
        ok(f"Hostname : {C.BOLD}{host[0]}{C.RESET}")
        if host[1]:
            res(f"Aliases  : {C.WHITE}{', '.join(host[1])}{C.RESET}")
        res(f"Addresses: {C.WHITE}{', '.join(host[2])}{C.RESET}")
    except socket.herror:
        warn("No hostname found for this IP.")
    except Exception as e:
        err(f"Lookup failed: {e}")
    pause()

def web_menu():
    while True:
        banner()
        print(f"  {C.BLUE}◆{C.RESET}  {C.BOLD}WEB TOOLS{C.RESET}\n")
        opts = [
            ("01", "Website Status Checker", "Check if site is up"),
            ("02", "SSL Certificate Checker","Validate SSL/TLS cert"),
            ("03", "HTTP Headers Analyzer",  "Inspect response headers"),
            ("04", "Robots.txt Viewer",       "View disallowed paths"),
            ("05", "Sitemap Finder",           "Locate sitemap files"),
            ("06", "Reverse IP Lookup",        "IP to hostname"),
            ("00", "Back",                     "Return to main menu"),
        ]
        for num, name, desc in opts:
            c = C.RED if num=="00" else C.GREEN
            print(f"  {c}[{num}]{C.RESET}  {C.BOLD}{name:<26}{C.RESET}  {C.DIM}{desc}{C.RESET}")
        print()
        choice = input(f"{C.CYAN}NullHawk{C.RESET}{C.BLUE}@web{C.RESET} ▶ ").strip()
        if   choice in ("1","01"): website_status()
        elif choice in ("2","02"): ssl_checker()
        elif choice in ("3","03"): http_headers()
        elif choice in ("4","04"): robots_viewer()
        elif choice in ("5","05"): sitemap_finder()
        elif choice in ("6","06"): reverse_ip()
        elif choice in ("0","00"): break
        else: warn("Invalid option.")

# ══════════════════════════════════════════════════════════════
#  SECTION 3 ── UTILITY TOOLS
# ══════════════════════════════════════════════════════════════

def hash_generator():
    divider("HASH GENERATOR")
    text = input(f"{C.YELLOW}[?]{C.RESET} Enter text to hash: {C.GREEN}")
    print(C.RESET)
    if not text:
        err("No text entered."); pause(); return

    enc = text.encode()
    algos = [
        ("MD5",    hashlib.md5(enc).hexdigest()),
        ("SHA1",   hashlib.sha1(enc).hexdigest()),
        ("SHA224", hashlib.sha224(enc).hexdigest()),
        ("SHA256", hashlib.sha256(enc).hexdigest()),
        ("SHA384", hashlib.sha384(enc).hexdigest()),
        ("SHA512", hashlib.sha512(enc).hexdigest()),
    ]
    ok(f"Hashes for: {C.BOLD}\"{text}\"{C.RESET}\n")
    for algo, val in algos:
        print(f"  {C.CYAN}{algo:<8}{C.RESET}  {C.WHITE}{val}{C.RESET}")
    pause()

def qr_generator():
    divider("QR CODE GENERATOR")
    data = input(f"{C.YELLOW}[?]{C.RESET} Enter text/URL for QR: {C.GREEN}").strip()
    print(C.RESET)
    if not data:
        err("No data entered."); pause(); return

    # Try qrcode lib
    try:
        import qrcode
        qr = qrcode.QRCode(border=1)
        qr.add_data(data)
        qr.make(fit=True)
        ok(f"QR Code for: {C.BOLD}{data}{C.RESET}\n")
        qr.print_ascii(invert=True)
    except ImportError:
        # ASCII art fallback using terminal blocks
        warn("qrcode lib not found. Install: pip install qrcode")
        info(f"Encoded data: {C.CYAN}{data}{C.RESET}")
        info("Online QR: https://qrcode.show/"+urllib.parse.quote(data))
    pause()

def base64_tool():
    divider("BASE64 ENCODER / DECODER")
    print(f"  {C.GREEN}[1]{C.RESET} Encode   {C.GREEN}[2]{C.RESET} Decode\n")
    mode = input(f"{C.YELLOW}[?]{C.RESET} Choice: ").strip()
    text = input(f"{C.YELLOW}[?]{C.RESET} Enter text: {C.GREEN}").strip()
    print(C.RESET)
    if not text:
        err("No text entered."); pause(); return

    if mode == "1":
        encoded = base64.b64encode(text.encode()).decode()
        ok("Encoded:")
        print(f"\n  {C.CYAN}{encoded}{C.RESET}\n")
    elif mode == "2":
        try:
            decoded = base64.b64decode(text.encode()).decode()
            ok("Decoded:")
            print(f"\n  {C.CYAN}{decoded}{C.RESET}\n")
        except Exception:
            err("Invalid Base64 string.")
    else:
        err("Invalid choice.")
    pause()

def password_strength():
    divider("PASSWORD STRENGTH CHECKER")
    import getpass
    pwd = getpass.getpass(f"{C.YELLOW}[?]{C.RESET} Enter password (hidden): ")
    if not pwd:
        err("No password entered."); pause(); return

    score = 0
    checks = [
        (len(pwd) >= 8,  "Length ≥ 8 chars"),
        (len(pwd) >= 12, "Length ≥ 12 chars"),
        (len(pwd) >= 16, "Length ≥ 16 chars"),
        (bool(re.search(r'[a-z]',pwd)), "Lowercase letters"),
        (bool(re.search(r'[A-Z]',pwd)), "Uppercase letters"),
        (bool(re.search(r'\d',    pwd)), "Numbers"),
        (bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]',pwd)),"Special chars"),
        (not bool(re.search(r'(.)\1{2,}',pwd)),"No repeated chars"),
        (pwd.lower() not in ["password","123456","qwerty","admin","letmein"],"Not common password"),
    ]

    print()
    for passed, label in checks:
        icon = f"{C.GREEN}✔{C.RESET}" if passed else f"{C.RED}✘{C.RESET}"
        print(f"  {icon}  {label}")
        if passed: score += 1

    print()
    pct = int((score/len(checks))*100)
    bar_filled = int(pct/5)
    bar = f"{C.GREEN}{'█'*bar_filled}{C.DIM}{'░'*(20-bar_filled)}{C.RESET}"
    print(f"  Strength: [{bar}] {pct}%")

    if pct >= 80:   ok("STRONG password!")
    elif pct >= 55: warn("MODERATE password. Improve it.")
    else:           err("WEAK password! Use a stronger one.")
    pause()

def password_generator():
    divider("PASSWORD GENERATOR")
    print(f"  {C.CYAN}Options:{C.RESET}")
    print(f"  {C.GREEN}[1]{C.RESET} Simple (letters+numbers)")
    print(f"  {C.GREEN}[2]{C.RESET} Strong (all chars)")
    print(f"  {C.GREEN}[3]{C.RESET} PIN (digits only)")
    print(f"  {C.GREEN}[4]{C.RESET} Passphrase\n")
    mode   = input(f"{C.YELLOW}[?]{C.RESET} Mode: ").strip()
    length = input(f"{C.YELLOW}[?]{C.RESET} Length (default 16): ").strip()
    count  = input(f"{C.YELLOW}[?]{C.RESET} How many? (default 5): ").strip()
    print()

    length = int(length) if length.isdigit() else 16
    count  = int(count)  if count.isdigit()  else 5

    chars_map = {
        "1": string.ascii_letters + string.digits,
        "2": string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?",
        "3": string.digits,
    }
    words = ["hawk","null","ghost","void","dark","cyber","swift","blade","storm","night",
             "echo","neon","flux","apex","zero","shade","wolf","raven","iron","steel"]

    ok(f"Generated {count} password(s):\n")
    for i in range(count):
        if mode == "4":
            pwd = "-".join(random.choices(words, k=4))
        else:
            chars = chars_map.get(mode, chars_map["2"])
            pwd = ''.join(random.choices(chars, k=length))
        print(f"  {C.GREEN}{i+1}.{C.RESET}  {C.BOLD}{C.CYAN}{pwd}{C.RESET}")
    pause()

def mac_lookup():
    divider("MAC ADDRESS LOOKUP")
    mac = input(f"{C.YELLOW}[?]{C.RESET} Enter MAC (e.g. AA:BB:CC:DD:EE:FF): {C.GREEN}").strip()
    print(C.RESET)
    if not mac:
        err("No MAC entered."); pause(); return

    mac_clean = mac.upper().replace("-",":").replace(".",":")
    if not re.match(r'^([0-9A-F]{2}:){5}[0-9A-F]{2}$', mac_clean):
        err("Invalid MAC format."); pause(); return

    oui = mac_clean[:8]
    res(f"MAC Address : {C.BOLD}{mac_clean}{C.RESET}")
    res(f"OUI Prefix  : {C.CYAN}{oui}{C.RESET}")

    # Multicast/broadcast check
    first_byte = int(mac_clean[:2], 16)
    if first_byte & 1:
        warn("Multicast/Broadcast MAC")
    else:
        ok("Unicast MAC")

    if first_byte & 2:
        warn("Locally Administered (not globally unique)")
    else:
        ok("Globally Unique (IEEE registered)")

    # Try online OUI lookup
    url = f"https://api.macvendors.com/{urllib.parse.quote(oui)}"
    body, code, _ = fetch(url, timeout=5)
    if code == 200 and body:
        ok(f"Vendor: {C.BOLD}{C.GREEN}{body.strip()}{C.RESET}")
    else:
        warn("Vendor not found (offline or unknown OUI).")
    pause()

def fake_identity():
    divider("FAKE IDENTITY GENERATOR")
    print(f"{C.DIM}  For testing & development purposes only.{C.RESET}\n")

    first_names = ["Alex","Jordan","Taylor","Morgan","Casey","Riley","Dakota","Avery",
                   "Quinn","Skyler","Reese","Finley","Emery","Sage","Parker","Blake"]
    last_names  = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis",
                   "Wilson","Moore","Anderson","Taylor","Thomas","Jackson","White","Harris"]
    domains     = ["gmail.com","yahoo.com","hotmail.com","outlook.com","protonmail.com"]
    streets     = ["Main St","Oak Ave","Maple Dr","Cedar Ln","Elm Blvd","Pine Rd"]
    cities      = ["New York","Los Angeles","Chicago","Houston","Phoenix","Philadelphia"]
    states      = ["NY","CA","IL","TX","AZ","PA","FL","OH","MI","WA"]
    jobs        = ["Software Engineer","Graphic Designer","Data Analyst","Teacher",
                   "Marketing Manager","Nurse","Architect","Accountant","Journalist"]

    fn = random.choice(first_names)
    ln = random.choice(last_names)
    age= random.randint(18,65)
    yr = datetime.now().year - age
    mo = random.randint(1,12)
    dy = random.randint(1,28)
    em = f"{fn.lower()}.{ln.lower()}{random.randint(1,999)}@{random.choice(domains)}"
    ph = f"+1{random.randint(200,999)}{random.randint(1000000,9999999)}"
    st = f"{random.randint(1,9999)} {random.choice(streets)}"
    ci = random.choice(cities)
    st2= random.choice(states)
    zp = f"{random.randint(10000,99999)}"
    pw = ''.join(random.choices(string.ascii_letters+string.digits+"!@#$", k=12))
    ua = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/{random.randint(90,120)}.0"

    count = input(f"{C.YELLOW}[?]{C.RESET} How many identities? (default 1): ").strip()
    count = int(count) if count.isdigit() else 1
    print()

    for i in range(count):
        fn = random.choice(first_names)
        ln = random.choice(last_names)
        print(f"  {C.CYAN}{'─'*40}{C.RESET}")
        print(f"  {C.BOLD}Identity #{i+1}{C.RESET}")
        print(f"  {C.YELLOW}Name     :{C.RESET} {fn} {ln}")
        print(f"  {C.YELLOW}DOB      :{C.RESET} {dy:02d}/{mo:02d}/{yr}")
        print(f"  {C.YELLOW}Age      :{C.RESET} {age}")
        print(f"  {C.YELLOW}Email    :{C.RESET} {fn.lower()}.{ln.lower()}{random.randint(1,999)}@{random.choice(domains)}")
        print(f"  {C.YELLOW}Phone    :{C.RESET} +1{random.randint(200,999)}{random.randint(1000000,9999999)}")
        print(f"  {C.YELLOW}Address  :{C.RESET} {random.randint(1,9999)} {random.choice(streets)}, {random.choice(cities)}, {random.choice(states)} {random.randint(10000,99999)}")
        print(f"  {C.YELLOW}Job      :{C.RESET} {random.choice(jobs)}")
        print(f"  {C.YELLOW}Password :{C.RESET} {''.join(random.choices(string.ascii_letters+string.digits+'!@#$',k=12))}")
        print(f"  {C.YELLOW}User-Agent:{C.RESET} {C.DIM}Mozilla/5.0 Chrome/{random.randint(90,120)}.0{C.RESET}")
        print()
    pause()

def utility_menu():
    while True:
        banner()
        print(f"  {C.YELLOW}◆{C.RESET}  {C.BOLD}UTILITY TOOLS{C.RESET}\n")
        opts = [
            ("01","Hash Generator",        "MD5/SHA1/SHA256/SHA512"),
            ("02","QR Code Generator",     "Generate QR from text/URL"),
            ("03","Base64 Encoder/Decoder","Encode or decode Base64"),
            ("04","Password Strength",     "Check password strength"),
            ("05","Password Generator",    "Generate secure passwords"),
            ("06","MAC Address Lookup",    "Vendor from MAC address"),
            ("07","Fake Identity Gen",     "Generate test identities"),
            ("00","Back",                  "Return to main menu"),
        ]
        for num, name, desc in opts:
            c = C.RED if num=="00" else C.GREEN
            print(f"  {c}[{num}]{C.RESET}  {C.BOLD}{name:<26}{C.RESET}  {C.DIM}{desc}{C.RESET}")
        print()
        choice = input(f"{C.CYAN}NullHawk{C.RESET}{C.YELLOW}@util{C.RESET} ▶ ").strip()
        if   choice in ("1","01"): hash_generator()
        elif choice in ("2","02"): qr_generator()
        elif choice in ("3","03"): base64_tool()
        elif choice in ("4","04"): password_strength()
        elif choice in ("5","05"): password_generator()
        elif choice in ("6","06"): mac_lookup()
        elif choice in ("7","07"): fake_identity()
        elif choice in ("0","00"): break
        else: warn("Invalid option.")

# ══════════════════════════════════════════════════════════════
#  SECTION 4 ── NETWORK TOOLS
# ══════════════════════════════════════════════════════════════

def ping_tool():
    divider("PING TOOL")
    host = input(f"{C.YELLOW}[?]{C.RESET} Enter host/IP: {C.GREEN}").strip()
    count= input(f"{C.YELLOW}[?]{C.RESET} Ping count (default 4): ").strip()
    print(C.RESET)
    if not host:
        err("No host entered."); pause(); return

    count = int(count) if count.isdigit() else 4
    info(f"Pinging {C.CYAN}{host}{C.RESET} ({count} times)...\n")

    param = "-n" if platform.system().lower()=="windows" else "-c"
    try:
        result = subprocess.run(
            ["ping", param, str(count), host],
            capture_output=True, text=True, timeout=20
        )
        output = result.stdout or result.stderr
        for line in output.splitlines():
            if "ttl" in line.lower() or "time" in line.lower():
                print(f"  {C.GREEN}{line}{C.RESET}")
            elif "loss" in line.lower() or "unreachable" in line.lower():
                print(f"  {C.RED}{line}{C.RESET}")
            else:
                print(f"  {C.DIM}{line}{C.RESET}")
    except FileNotFoundError:
        err("ping command not found.")
    except subprocess.TimeoutExpired:
        err("Ping timed out.")
    pause()

def traceroute_tool():
    divider("TRACEROUTE")
    host = input(f"{C.YELLOW}[?]{C.RESET} Enter host/IP: {C.GREEN}").strip()
    print(C.RESET)
    if not host:
        err("No host entered."); pause(); return

    cmd = "tracert" if platform.system().lower()=="windows" else "traceroute"
    info(f"Traceroute to {C.CYAN}{host}{C.RESET}...\n")
    try:
        result = subprocess.run(
            [cmd, host], capture_output=True, text=True, timeout=60
        )
        output = result.stdout or result.stderr
        for line in output.splitlines():
            print(f"  {C.DIM}{line}{C.RESET}")
    except FileNotFoundError:
        err(f"'{cmd}' not found. Install: pkg install traceroute")
    except subprocess.TimeoutExpired:
        err("Traceroute timed out.")
    pause()

def banner_grab():
    divider("BANNER GRABBING")
    host = input(f"{C.YELLOW}[?]{C.RESET} Enter host/IP: {C.GREEN}").strip()
    port = input(f"{C.YELLOW}[?]{C.RESET} Enter port (default 80): ").strip()
    print(C.RESET)
    if not host:
        err("No host entered."); pause(); return

    port = int(port) if port.isdigit() else 80
    info(f"Grabbing banner from {C.CYAN}{host}:{port}{C.RESET}...")

    try:
        s = socket.socket()
        s.settimeout(8)
        s.connect((host, port))

        # Send HTTP request for port 80/443
        if port in (80, 8080, 8000):
            s.send(b"HEAD / HTTP/1.0\r\nHost: " + host.encode() + b"\r\n\r\n")
        elif port == 21:
            pass  # FTP sends banner automatically
        elif port == 22:
            pass  # SSH sends banner automatically
        else:
            s.send(b"\r\n")

        banner_data = s.recv(1024).decode('utf-8', errors='replace')
        s.close()

        if banner_data:
            ok(f"Banner received ({len(banner_data)} bytes):\n")
            for line in banner_data.splitlines()[:20]:
                print(f"  {C.CYAN}{line}{C.RESET}")
        else:
            warn("No banner returned.")
    except ConnectionRefusedError:
        err(f"Port {port} is CLOSED.")
    except socket.timeout:
        err("Connection timed out.")
    except Exception as e:
        err(f"Error: {e}")
    pause()

def ip_geolocation():
    divider("IP GEOLOCATION")
    ip = input(f"{C.YELLOW}[?]{C.RESET} Enter IP (blank = your IP): {C.GREEN}").strip()
    print(C.RESET)

    url = f"http://ip-api.com/json/{ip}" if ip else "http://ip-api.com/json/"
    info(f"Looking up: {C.CYAN}{ip or 'your IP'}{C.RESET}")
    body, code, _ = fetch(url)
    if code == 200 and body:
        try:
            data = json.loads(body)
            if data.get('status') == 'success':
                fields = [
                    ("IP",          data.get('query','')),
                    ("Country",     data.get('country','')),
                    ("Region",      data.get('regionName','')),
                    ("City",        data.get('city','')),
                    ("ZIP",         data.get('zip','')),
                    ("Latitude",    str(data.get('lat',''))),
                    ("Longitude",   str(data.get('lon',''))),
                    ("Timezone",    data.get('timezone','')),
                    ("ISP",         data.get('isp','')),
                    ("Org",         data.get('org','')),
                    ("AS",          data.get('as','')),
                ]
                print()
                for label, val in fields:
                    print(f"  {C.CYAN}{label:<12}{C.RESET}  {C.WHITE}{val}{C.RESET}")
            else:
                err(f"Lookup failed: {data.get('message','unknown error')}")
        except:
            err("Could not parse response.")
    else:
        err("Could not reach IP lookup service.")
    pause()

def open_port_history():
    divider("OPEN PORT HISTORY CHECK")
    host = input(f"{C.YELLOW}[?]{C.RESET} Enter IP/domain: {C.GREEN}").strip()
    print(C.RESET)
    if not host:
        err("No host entered."); pause(); return

    common_ports = {
        21:"FTP", 22:"SSH", 23:"Telnet", 25:"SMTP", 53:"DNS",
        80:"HTTP", 110:"POP3", 143:"IMAP", 443:"HTTPS", 445:"SMB",
        3306:"MySQL", 3389:"RDP", 5432:"PostgreSQL", 6379:"Redis",
        8080:"HTTP-Alt", 8443:"HTTPS-Alt", 27017:"MongoDB",
    }

    info(f"Scanning {len(common_ports)} common ports on {C.CYAN}{host}{C.RESET}...\n")
    open_ports = []

    for port, service in common_ports.items():
        try:
            s = socket.socket()
            s.settimeout(1)
            r = s.connect_ex((host, port))
            s.close()
            if r == 0:
                open_ports.append((port, service))
                print(f"  {C.GREEN}[OPEN]  {port:<6}{C.RESET}  {C.BOLD}{service}{C.RESET}")
            else:
                print(f"  {C.DIM}[----]  {port:<6}  {service}{C.RESET}")
        except:
            print(f"  {C.DIM}[ERR ]  {port:<6}  {service}{C.RESET}")

    print(f"\n  {C.BOLD}Total open: {C.GREEN}{len(open_ports)}{C.RESET}")
    pause()

def network_menu():
    while True:
        banner()
        print(f"  {C.MAGENTA}◆{C.RESET}  {C.BOLD}NETWORK TOOLS{C.RESET}\n")
        opts = [
            ("01","Ping Tool",            "Ping a host"),
            ("02","Traceroute",           "Trace network path"),
            ("03","Banner Grabbing",      "Grab service banner"),
            ("04","IP Geolocation",       "Locate an IP address"),
            ("05","Open Port History",    "Scan common ports"),
            ("00","Back",                 "Return to main menu"),
        ]
        for num, name, desc in opts:
            c = C.RED if num=="00" else C.GREEN
            print(f"  {c}[{num}]{C.RESET}  {C.BOLD}{name:<26}{C.RESET}  {C.DIM}{desc}{C.RESET}")
        print()
        choice = input(f"{C.CYAN}NullHawk{C.RESET}{C.MAGENTA}@net{C.RESET} ▶ ").strip()
        if   choice in ("1","01"): ping_tool()
        elif choice in ("2","02"): traceroute_tool()
        elif choice in ("3","03"): banner_grab()
        elif choice in ("4","04"): ip_geolocation()
        elif choice in ("5","05"): open_port_history()
        elif choice in ("0","00"): break
        else: warn("Invalid option.")

# ══════════════════════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════════════════════

def main():
    while True:
        banner()
        print(f"  {C.BOLD}MAIN MENU{C.RESET}\n")
        sections = [
            ("01", C.RED,     "🔍 OSINT Tools",    "Username, Email, Phone, Social"),
            ("02", C.BLUE,    "🌐 Web Tools",       "Status, SSL, Headers, Robots"),
            ("03", C.YELLOW,  "🛠  Utility Tools",   "Hash, QR, Base64, Passwords"),
            ("04", C.MAGENTA, "📡 Network Tools",   "Ping, Trace, Banner, GeoIP"),
            ("00", C.DIM,     "🚪 Exit",             ""),
        ]
        for num, color, name, desc in sections:
            arrow = f"{C.DIM}{desc}{C.RESET}" if desc else ""
            print(f"  {color}[{num}]{C.RESET}  {C.BOLD}{name:<22}{C.RESET}  {arrow}")
        print()
        choice = input(f"{C.CYAN}NullHawk{C.RESET}{C.RED}@tool{C.RESET} ▶ ").strip()

        if   choice in ("1","01"): osint_menu()
        elif choice in ("2","02"): web_menu()
        elif choice in ("3","03"): utility_menu()
        elif choice in ("4","04"): network_menu()
        elif choice in ("0","00"):
            banner()
            print(f"\n  {C.RED}Shutting down NullHawk...{C.RESET}")
            print(f"  {C.DIM}Stay sharp. Stay legal. — darkvibez456{C.RESET}\n")
            sys.exit(0)
        else:
            warn("Invalid option. Try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {C.RED}[!]{C.RESET} Interrupted by user. Exiting...\n")
        sys.exit(0)
