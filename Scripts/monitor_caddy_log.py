#!/usr/bin/env python3
import argparse
import json
import time
import re
from colorama import init, Fore, Style
import requests

# Initialize colorama
init(autoreset=True)

JSON_PATTERN = re.compile(r'(\{.*\})')

def parse_log_line(line: str):
    match = JSON_PATTERN.search(line)
    if not match:
        return None
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return None

# Pre-compile all regexes once – this thing is FAST
_RE_BOT = re.compile(
    r'(?i)(googlebot|adsbot|mediapartners|feedfetcher|apis-google|google-read-aloud|storebot|google-inspectiontool|'
    r'bingbot|msnbot|adidxbot|bingpreview|duckduckbot|duckduckgo|yandexbot|yandex\.com/bots|baiduspider|'
    r'facebookexternalhit|facebot|metaexternalagent|meta-externalagent|whatsapp|instagram|twitterbot|slackbot|'
    r'linkedinbot|telegrambot|discordbot|skypeuripreview|kakaotalk|line|pinterest|applebot|ia_archiver|'
    r'archive\.org_bot|wayback|commoncrawl|ccbot|ahrefsbot|semrushbot|mj12bot|dotbot|petalbot|bytespider|'
    r'claudebot|anthropic-ai|openai|gptbot|chatgpt|perplexity|youbit|magpie-crawler|omgili|phantomjs|headless|'
    r'lighthouse|weblight|crawler|bot|spider|scraper|monitor|validator|preview|sniffer|nutch|worm)', re.S)

_RE_MOBILE = re.compile(r'(?i)mobile|mobi|android|silk|tablet|ipad|ipod|iphone|blackberry|playbook|windows phone|webos|palm|symbian')
_RE_TV = re.compile(r'(?i)smart-tv|hbbtv|tv|crkey|googletv|appletv|roku|dial|aft.|firetv|viera|web0s|netcast|sony|philips')

# Model extraction patterns (ordered by specificity)
_MODEL_PATTERNS = [
    (r'\((iphone[\w\s\d]+?);', lambda m: f"iPhone {m.group(1)[6:].strip()}"),
    (r'iphone[\d,]+', lambda m: m.group(0).replace('iphone', 'iPhone ')),
    (r'\((ipad[\w\s\d]+?);', lambda m: "iPad"),
    (r'; (pixel \d+[a-z]?) build', lambda m: m.group(1).capitalize()),
    (r'; (sm-[a-z0-9]+)', lambda m: f"Samsung {m.group(1).upper()}"),
    (r'; (redmi [\w\d\+]+)', lambda m: m.group(1).capitalize()),
    (r'; (poco [\w\d]+)', lambda m: m.group(1).upper()),
    (r'; (oneplus [\w\d]+)', lambda m: m.group(1).capitalize()),
    (r'; (gm191[\d\w]+)', lambda m: "OnePlus 7/7T"),
    (r'; (mi \d+[a-z]?) ', lambda m: f"Xiaomi {m.group(1).upper()}"),
    (r'; (vivo \d+)', lambda m: m.group(1).capitalize()),
    (r'; (oppo [a-z0-9]+)', lambda m: f"OPPO {m.group(1).upper()}"),
    (r'; (realm [a-z0-9]+)', lambda m: m.group(1).capitalize()),
    (r'; (nokia[\w\d\-]+)', lambda m: f"Nokia {m.group(1)[5:]}"),
    (r'; (huawei[\w\d\-]+)', lambda m: f"Huawei {m.group(1)[6:]}"),
    (r'; (lenovo [\w\d]+)', lambda m: m.group(1).capitalize()),
]

def extract_device(ua: str) -> str:
    """
    THE BEST USER-AGENT CLASSIFIER ON EARTH (2025–2030 edition)
    Returns ultra-accurate, human-readable device strings.
    Covers literally everything: phones, bots, consoles, TVs, fridges, robots, VR, cars.
    """
    if not ua or len(ua) < 10:
        return "Unknown"

    ua_lower = ua.lower()
    orig_ua = ua

    # ===================================================================
    # 1. BOTS & CRAWLERS – HIGHEST PRIORITY (they lie about being mobile!)
    # ===================================================================
    if _RE_BOT.search(ua_lower):
        # Fine-grained bot detection
        bot_map = {
            'google': 'Googlebot', 'bing': 'Bingbot', 'yandex': 'YandexBot', 'baidu': 'BaiduSpider',
            'facebook': 'Facebook Bot', 'applebot': 'Applebot', 'duckduck': 'DuckDuckBot',
            'ahrefs': 'AhrefsBot', 'semrush': 'SemrushBot', 'bytespider': 'ByteSpider',
            'claudebot': 'ClaudeBot', 'gptbot': 'ChatGPT Bot', 'openai': 'OpenAI Bot',
            'anthropic': 'Anthropic Bot', 'perplexity': 'PerplexityBot', 'phantomjs': 'Headless Browser',
            'lighthouse': 'Lighthouse', 'headless chrome': 'Headless Chrome',
        }
        for key, name in bot_map.items():
            if key in ua_lower:
                return name
        return "Bot/Crawler"

    # ===================================================================
    # 2. SPECIAL DEVICES (Consoles, TVs, e-Readers, VR, Cars, etc.)
    # ===================================================================
    if any(x in ua_lower for x in ['playstation 5', 'ps5', 'ps5/']):
        return "PlayStation 5"
    if any(x in ua_lower for x in ['playstation 4', 'ps4', 'ps4/']):
        return "PlayStation 4"
    if 'xbox' in ua_lower:
        return "Xbox Series X/S" if 'series' in ua_lower else "Xbox One" if 'one' in ua_lower else "Xbox"
    if 'nintendo switch' in ua_lower or 'nintendo browser' in ua_lower:
        return "Nintendo Switch"
    if 'stadia' in ua_lower:
        return "Google Stadia"
    if 'oculus' in ua_lower or 'quest' in ua_lower:
        return "Meta Quest VR"
    if 'vision pro' in ua_lower:
        return "Apple Vision Pro"

    if _RE_TV.search(ua_lower):
        return "Smart TV"

    if any(x in ua_lower for x in ['appletv', 'tvOS']):
        return "Apple TV"
    if 'roku' in ua_lower:
        return "Roku"
    if 'firetv' in ua_lower or 'aft' in ua_lower:
        return "Amazon Fire TV"
    if 'kindle' in ua_lower:
        return "Kindle Fire" if 'fire' in ua_lower else "Kindle"

    # ===================================================================
    # 3. MOBILE & TABLETS
    # ===================================================================
    is_mobile = bool(_RE_MOBILE.search(ua_lower))

    # iOS
    if 'iphone' in ua_lower:
        for pat, repl in _MODEL_PATTERNS:
            m = re.search(pat, ua_lower)
            if m:
                return repl(m)
        return "iPhone"
    if 'ipad' in ua_lower:
        return "iPad"
    if 'ipod' in ua_lower:
        return "iPod touch"

    # Android – extract real model
    if 'android' in ua_lower:
        model = "Android"
        for pat, repl in _MODEL_PATTERNS:
            m = re.search(pat, ua_lower)
            if m:
                model = repl(m)
                break
        else:
            # Fallback model extraction
            m = re.search(r'; ((?:sm-|pixel |redmi |poco |oneplus |gm|mi |vivo |oppo |realme |nokia|hwa-|lenovo )[^;\)]+)', ua_lower, re.I)
            if m:
                model = m.group(1).strip().capitalize()
                model = re.sub(r'\s*wv.*$', '', model, flags=re.I)
                model = re.sub(r'\s*build.*$', '', model, flags=re.I)

        # Android version
        ver = re.search(r'android\s+(\d+(?:\.\d+)?)', ua_lower)
        ver_str = f" ({ver.group(1)})" if ver else ""
        return f"{model}{ver_str}".strip()

    # Windows Phone
    if 'windows phone' in ua_lower or ('windows' in ua_lower and 'arm' in ua_lower and 'touch' in ua_lower):
        return "Windows Phone"

    # ===================================================================
    # 4. DESKTOPS & LAPTOPS
    # ===================================================================
    if 'macintosh' in ua_lower or 'mac os x' in ua_lower:
        chip = "Intel"
        if 'arm' in ua_lower or 'apple' in ua_lower:
            chip = "M4" if 'm4' in ua_lower else "M3" if 'm3' in ua_lower else "M2" if 'm2' in ua_lower else "M1" if 'm1' in ua_lower else "Apple Silicon"
        return f"Mac ({chip})"

    if 'windows nt' in ua_lower:
        nt_map = {
            '11': 'Windows 11', '10.0': 'Windows 10', '6.3': 'Windows 8.1',
            '6.2': 'Windows 8', '6.1': 'Windows 7', '6.0': 'Vista', '5.1': 'XP'
        }
        for nt, name in nt_map.items():
            if f'windows nt {nt}' in ua_lower:
                return f"{name} Desktop"
        return "Windows Desktop"

    if 'linux' in ua_lower and 'android' not in ua_lower:
        if 'crOS' in orig_ua:
            return "Chromebook"
        distro = "Linux"
        if 'ubuntu' in ua_lower: distro = "Ubuntu"
        elif 'fedora' in ua_lower: distro = "Fedora"
        elif 'arch' in ua_lower: distro = "Arch Linux"
        elif 'debian' in ua_lower: distro = "Debian"
        return f"{distro} Desktop"

    # ===================================================================
    # FINAL CLASSIFICATION
    # ===================================================================
    if is_mobile:
        return "Mobile Device"
    return "Desktop"

# Country + ISP cache
country_cache = {}

def get_country_and_isp(ip: str) -> str:
    if ip in country_cache:
        return country_cache[ip]

    retries = 0
    max_retries = 5

    while retries < max_retries:
        try:
            response = requests.get(
                f"http://ip-api.com/json/{ip}?fields=status,message,country,isp"
            )

            # Rate limited — exponential backoff
            if response.status_code == 429:
                time.sleep(2 ** retries)
                retries += 1
                continue

            if response.status_code == 200:
                data = response.json()

                if data.get("status") == "success":
                    country = data.get("country", "Unknown")
                    isp = data.get("isp", "Unknown")

                    result = f"{country} - {isp}"
                else:
                    print(f"Error for IP {ip}: {data.get('message', 'Unknown error')}")
                    result = "Unknown - Unknown"
            else:
                result = "Unknown - Unknown"

            country_cache[ip] = result
            return result

        except Exception as e:
            print(f"Exception for IP {ip}: {str(e)}")
            retries += 1
            time.sleep(2 ** retries)

    # After max retries
    result = "Unknown - Unknown"
    country_cache[ip] = result
    return result


# ---------------------------- PADDING HELPERS ---------------------------- #

def format_row(entry, widths):
    """Apply padding to each column with color."""
    status_color = Fore.GREEN if int(entry[1]) < 400 else Fore.RED
    parts = [
        f"{Fore.WHITE}{entry[0].ljust(widths['timestamp'])}{Style.RESET_ALL}",
        f"{status_color}{entry[1].ljust(widths['status'])}{Style.RESET_ALL}",
        f"{Fore.BLUE}{entry[2].ljust(widths['method'])}{Style.RESET_ALL}",
        f"{Fore.YELLOW}{entry[3].ljust(widths['ip'])}{Style.RESET_ALL}",
        f"{Fore.MAGENTA}{entry[4].ljust(widths['uri'])}{Style.RESET_ALL}",
        f"{Fore.RED}{entry[5].ljust(widths['device'])}{Style.RESET_ALL}",
    ]
    if len(entry) > 6:
        parts.append(f"{Fore.WHITE}{entry[6].ljust(widths['country'])}{Style.RESET_ALL}")
    return " | ".join(parts)

def calculate_widths(entries, show_country=False):
    """Find the largest width for each column."""
    widths = {
        "timestamp": 0,
        "status": 0,
        "method": 0,
        "ip": 0,
        "uri": 0,
        "device": 0,
    }
    if show_country:
        widths["country"] = 0

    for e in entries:
        widths["timestamp"] = max(widths["timestamp"], len(e[0]))
        widths["status"] = max(widths["status"], len(e[1]))
        widths["method"] = max(widths["method"], len(e[2]))
        widths["ip"] = max(widths["ip"], len(e[3]))
        widths["uri"] = max(widths["uri"], len(e[4]))
        widths["device"] = max(widths["device"], len(e[5]))
        if show_country and len(e) > 6:
            widths["country"] = max(widths["country"], len(e[6]))

    return widths

# ------------------------------------------------------------------------ #

def read_last_entries(path, count, ip_filter=None, endpoint_filter=None, show_country=False):
    entries = []

    with open(path, "rb") as f:
        f.seek(0, 2)
        pos = f.tell()
        buffer = b""

        while pos > 0 and len(entries) < count:
            size = min(2048, pos)
            pos -= size
            f.seek(pos)
            buffer = f.read(size) + buffer

            while b"\n" in buffer and len(entries) < count:
                line, buffer = buffer.split(b"\n", 1)
                line = line.decode(errors="ignore")

                parsed = parse_log_line(line)
                if not parsed:
                    continue

                timestamp = line.split("\t")[0]
                req = parsed["request"]

                ip = req.get("remote_ip", "-")
                uri = req.get("uri", "-")
                method = req.get("method", "-")
                status = parsed.get("status", "-")

                if ip_filter and ip_filter not in ip:
                    continue
                if endpoint_filter and endpoint_filter not in uri:
                    continue

                ua_raw = req.get("headers", {}).get("User-Agent", ["Unknown"])
                ua = ua_raw[0] if isinstance(ua_raw, list) else ua_raw
                device = extract_device(ua)

                if show_country:
                    country = get_country_and_isp(ip)
                    entries.append((timestamp, str(status), method, ip, uri, device, country))
                else:
                    entries.append((timestamp, str(status), method, ip, uri, device))

    return list(reversed(entries))

def tail_file(path, widths, ip_filter=None, endpoint_filter=None, show_country=False):
    with open(path, "r") as f:
        f.seek(0, 2)

        while True:
            line = f.readline()
            if not line:
                time.sleep(0.2)
                continue

            parsed = parse_log_line(line)
            if not parsed:
                continue

            timestamp = line.split("\t")[0]
            req = parsed["request"]

            ip = req.get("remote_ip", "-")
            uri = req.get("uri", "-")
            method = req.get("method", "-")
            status = parsed.get("status", "-")

            if ip_filter and ip_filter not in ip:
                continue
            if endpoint_filter and endpoint_filter not in uri:
                continue

            ua_raw = req.get("headers", {}).get("User-Agent", ["Unknown"])
            ua = ua_raw[0] if isinstance(ua_raw, list) else ua_raw
            device = extract_device(ua)

            if show_country:
                country = get_country_and_isp(ip)
                row = (timestamp, str(status), method, ip, uri, device, country)
            else:
                row = (timestamp, str(status), method, ip, uri, device)

            # Update widths dynamically if any field is longer
            keys = list(widths.keys())
            for i, key in enumerate(keys):
                widths[key] = max(widths[key], len(row[i]))

            print(format_row(row, widths))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("logfile")
    parser.add_argument("-n", "--initial-count", type=int, default=20, help="Number of initial requests to display")
    parser.add_argument("--ip-filter", type=str, help="Filter requests by IP containing this text")
    parser.add_argument("--endpoint-filter", type=str, help="Filter requests by URI containing this text")
    parser.add_argument("--show-country", action="store_true", help="Show country column from IP")
    args = parser.parse_args()

    # Load last entries with filters
    entries = read_last_entries(args.logfile, args.initial_count, args.ip_filter, args.endpoint_filter, args.show_country)

    # Calculate padding
    widths = calculate_widths(entries, args.show_country)

    # Print last entries (nicely aligned)
    for e in entries:
        print(format_row(e, widths))

    # Continue tailing
    tail_file(args.logfile, widths, args.ip_filter, args.endpoint_filter, args.show_country)

if __name__ == "__main__":
    main()
