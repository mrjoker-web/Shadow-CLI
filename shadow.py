#!/usr/bin/env python3
# ============================================================
#   Shadow CLI — Full Recon Framework
#   Author  : Mr Joker
#   Version : 1.0
#   GitHub  : https://github.com/mrjoker-web
#
#   Inclui: ShadowSub + ShadowProbe + ShadowScan +
#           ShadowBanner + ShadowFuzz
#
#   Uso:
#     python shadow.py -t example.com --full-recon
#     python shadow.py -t example.com --sub
#     python shadow.py -t example.com --scan
#     python shadow.py -t example.com --banner
#     python shadow.py -t example.com --probe -l hosts.txt
#     python shadow.py -t example.com --fuzz -w wordlist.txt
# ============================================================

import socket
import ssl
import json
import argparse
import threading
import time
import sys
import os
import requests
from datetime import datetime
from queue import Queue
from urllib.parse import urljoin

# ─── Colorama ────────────────────────────────────────────────
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    RED     = Fore.RED
    GREEN   = Fore.GREEN
    YELLOW  = Fore.YELLOW
    CYAN    = Fore.CYAN
    MAGENTA = Fore.MAGENTA
    WHITE   = Fore.WHITE
    BOLD    = Style.BRIGHT
    RESET   = Style.RESET_ALL
except ImportError:
    RED = GREEN = YELLOW = CYAN = MAGENTA = WHITE = BOLD = RESET = ""

# ─── Suprimir avisos SSL ──────────────────────────────────────
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ─── Config ───────────────────────────────────────────────────
VERSION = "1.0"
TIMEOUT = 3

PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS",
    3306: "MySQL", 5432: "PostgreSQL", 6379: "Redis",
    8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB",
}

DEFAULT_WORDLIST_SUB = [
    "www", "mail", "ftp", "admin", "test", "dev", "api",
    "beta", "staging", "portal", "vpn", "remote", "smtp",
    "pop", "imap", "ns1", "ns2", "mx", "shop", "store",
    "blog", "cdn", "media", "static", "app", "dashboard",
]

DEFAULT_WORDLIST_FUZZ = [
    "admin", "login", "dashboard", "panel", "backup",
    "config", "api", "v1", "v2", "uploads", "files",
    "static", "assets", "css", "js", "img", "images",
    "robots.txt", "sitemap.xml", ".env", "wp-admin",
    "phpmyadmin", "manager", "console", "test", "dev",
    "old", "new", "temp", "tmp", "db", "sql", "data",
]

_lock   = threading.Lock()
results = {}

# ─── Banner ASCII ─────────────────────────────────────────────
def print_banner():
    os.system("clear" if os.name == "posix" else "cls")
    print(f"""
{CYAN}{BOLD}
  ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗
  ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║
  ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║
  ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║
  ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝
  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝
{RESET}{MAGENTA}{BOLD}
          ██████╗██╗     ██╗
         ██╔════╝██║     ██║
         ██║     ██║     ██║
         ██║     ██║     ██║
         ╚██████╗███████╗██║
          ╚═════╝╚══════╝╚═╝
{RESET}
{WHITE}{'─'*55}
  {CYAN}Version :{RESET} {VERSION}    {CYAN}Author:{RESET} Mr Joker
  {CYAN}GitHub  :{RESET} github.com/mrjoker-web
  {CYAN}Suite   :{RESET} ShadowSub · ShadowProbe · ShadowScan
             ShadowBanner · ShadowFuzz
{WHITE}{'─'*55}{RESET}
""")

# ─── Progress bar ─────────────────────────────────────────────
def progress_bar(current, total, prefix=""):
    if total == 0:
        return
    bar_len = 28
    filled  = int(bar_len * current / total)
    bar     = "█" * filled + "░" * (bar_len - filled)
    pct     = current / total * 100
    sys.stdout.write(f"\r  {CYAN}{prefix}[{bar}] {pct:.1f}%{RESET}")
    sys.stdout.flush()
    if current == total:
        print()

def section(title: str):
    print(f"\n{CYAN}{BOLD}{'═'*55}")
    print(f"  {title}")
    print(f"{'═'*55}{RESET}\n")

# ═══════════════════════════════════════════════════════════════
# 🌐 SHADOWSUB — Subdomain Finder
# ═══════════════════════════════════════════════════════════════
def _check_subdomain(sub: str, domain: str, found: list, counter: list, total: int):
    host = f"{sub}.{domain}"
    try:
        ip = socket.gethostbyname(host)
        with _lock:
            found.append({"subdomain": host, "ip": ip})
            counter[0] += 1
            print(f"\r  {GREEN}[FOUND]{RESET} {host} {YELLOW}({ip}){RESET}         ")
    except Exception:
        with _lock:
            counter[0] += 1
            progress_bar(counter[0], total, "ShadowSub ")

def run_shadowsub(domain: str, wordlist: list, threads: int = 30) -> list:
    section("🌐 SHADOWSUB — Subdomain Finder")
    found   = []
    counter = [0]
    total   = len(wordlist)
    queue   = Queue()
    for w in wordlist:
        queue.put(w)

    def worker():
        while not queue.empty():
            sub = queue.get()
            _check_subdomain(sub, domain, found, counter, total)
            queue.task_done()

    ts = [threading.Thread(target=worker) for _ in range(min(threads, total))]
    for t in ts: t.start()
    for t in ts: t.join()

    print(f"\n  {GREEN}[+]{RESET} Subdomínios encontrados: {BOLD}{len(found)}{RESET}")
    return found

# ═══════════════════════════════════════════════════════════════
# ⚡ SHADOWPROBE — HTTP/HTTPS Probe
# ═══════════════════════════════════════════════════════════════
def _probe_host(host: str) -> dict | None:
    for scheme in ("https", "http"):
        url = f"{scheme}://{host}"
        try:
            r = requests.get(url, timeout=TIMEOUT, verify=False,
                             headers={"User-Agent": "ShadowCLI/1.0"})
            title = ""
            if "<title>" in r.text.lower():
                s = r.text.lower().find("<title>") + 7
                e = r.text.lower().find("</title>", s)
                title = r.text[s:e].strip()[:60]
            return {
                "host"   : host,
                "url"    : url,
                "status" : r.status_code,
                "title"  : title or "N/A",
            }
        except Exception:
            continue
    return None

def run_shadowprobe(hosts: list, threads: int = 20) -> list:
    section("⚡ SHADOWPROBE — HTTP/HTTPS Probe")
    live    = []
    counter = [0]
    total   = len(hosts)
    queue   = Queue()
    for h in hosts:
        queue.put(h)

    def worker():
        while not queue.empty():
            host = queue.get()
            res  = _probe_host(host)
            with _lock:
                counter[0] += 1
                if res:
                    live.append(res)
                    color = GREEN if res["status"] == 200 else YELLOW
                    print(f"\r  {color}[{res['status']}]{RESET} {res['url']} | {res['title']}         ")
                else:
                    progress_bar(counter[0], total, "ShadowProbe ")
            queue.task_done()

    ts = [threading.Thread(target=worker) for _ in range(min(threads, total))]
    for t in ts: t.start()
    for t in ts: t.join()

    print(f"\n  {GREEN}[+]{RESET} Hosts ativos: {BOLD}{len(live)}{RESET}")
    return live

# ═══════════════════════════════════════════════════════════════
# 🔍 SHADOWSCAN — Port Scanner + Recon
# ═══════════════════════════════════════════════════════════════
def run_shadowscan(domain: str) -> dict:
    section("🔍 SHADOWSCAN — Port Scanner & Recon")
    result = {"host": domain, "ip": "N/A", "open_ports": [], "headers": {}}

    try:
        result["ip"] = socket.gethostbyname(domain)
        print(f"  {GREEN}[+]{RESET} IP: {BOLD}{result['ip']}{RESET}")
    except Exception:
        print(f"  {RED}[!]{RESET} Não foi possível resolver {domain}")
        return result

    print(f"\n  {CYAN}[*]{RESET} A fazer scan de {len(PORTS)} portas...")
    for port, service in PORTS.items():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(TIMEOUT)
            if s.connect_ex((result["ip"], port)) == 0:
                result["open_ports"].append({"port": port, "service": service})
                print(f"  {GREEN}[OPEN]{RESET} Porta {port} — {MAGENTA}{service}{RESET}")
            s.close()
        except Exception:
            pass

    # HTTP headers
    for scheme in ("https", "http"):
        try:
            r = requests.get(f"{scheme}://{domain}", timeout=TIMEOUT,
                             verify=False, headers={"User-Agent": "ShadowCLI/1.0"})
            for key in ["Server", "X-Powered-By", "X-Generator", "Via"]:
                val = r.headers.get(key)
                if val:
                    result["headers"][key] = val
                    print(f"  {CYAN}[HDR]{RESET} {key}: {val}")
            break
        except Exception:
            continue

    print(f"\n  {GREEN}[+]{RESET} Portas abertas: {BOLD}{len(result['open_ports'])}{RESET}")
    return result

# ═══════════════════════════════════════════════════════════════
# 🚩 SHADOWBANNER — Banner Grabber
# ═══════════════════════════════════════════════════════════════
def _grab_banner(host: str, port: int, service: str) -> dict | None:
    if service in ("HTTP", "HTTPS", "HTTP-Alt", "HTTPS-Alt"):
        scheme = "https" if port in (443, 8443) else "http"
        url    = f"{scheme}://{host}:{port}" if port not in (80, 443) else f"{scheme}://{host}"
        try:
            r    = requests.get(url, timeout=TIMEOUT, verify=False,
                                headers={"User-Agent": "ShadowCLI/1.0"})
            info = {}
            for key in ["Server", "X-Powered-By", "X-Generator", "Via"]:
                val = r.headers.get(key)
                if val:
                    info[key] = val
            info["Status-Code"] = str(r.status_code)
            return info if info else None
        except Exception:
            return None
    else:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(TIMEOUT)
            s.connect((host, port))
            banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
            s.close()
            return {"Banner": banner} if banner else None
        except Exception:
            return None

def run_shadowbanner(domain: str, open_ports: list) -> list:
    section("🚩 SHADOWBANNER — Banner Grabber")
    banners = []

    ports_to_scan = open_ports if open_ports else list(PORTS.items())
    if open_ports:
        ports_to_scan = [(p["port"], p["service"]) for p in open_ports]
    else:
        ports_to_scan = list(PORTS.items())

    for port, service in ports_to_scan:
        info = _grab_banner(domain, port, service)
        if info:
            banners.append({"port": port, "service": service, "info": info})
            print(f"  {GREEN}[+]{RESET} Porta {BOLD}{port}{RESET} — {MAGENTA}{service}{RESET}")
            for k, v in info.items():
                print(f"      {CYAN}{k:<18}{RESET} {v}")

    print(f"\n  {GREEN}[+]{RESET} Banners obtidos: {BOLD}{len(banners)}{RESET}")
    return banners

# ═══════════════════════════════════════════════════════════════
# 💣 SHADOWFUZZ — Directory Fuzzer
# ═══════════════════════════════════════════════════════════════
def _fuzz_path(base_url: str, path: str, found: list, counter: list, total: int):
    url = urljoin(base_url + "/", path)
    try:
        r = requests.get(url, timeout=TIMEOUT, verify=False,
                         allow_redirects=False,
                         headers={"User-Agent": "ShadowCLI/1.0"})
        with _lock:
            counter[0] += 1
            if r.status_code not in (404, 400, 410):
                color = GREEN if r.status_code == 200 else YELLOW
                found.append({"url": url, "status": r.status_code})
                print(f"\r  {color}[{r.status_code}]{RESET} {url}         ")
            else:
                progress_bar(counter[0], total, "ShadowFuzz ")
    except Exception:
        with _lock:
            counter[0] += 1
            progress_bar(counter[0], total, "ShadowFuzz ")

def run_shadowfuzz(domain: str, wordlist: list, threads: int = 20) -> list:
    section("💣 SHADOWFUZZ — Directory Fuzzer")

    # Determinar base URL
    base_url = None
    for scheme in ("https", "http"):
        try:
            r = requests.get(f"{scheme}://{domain}", timeout=TIMEOUT, verify=False)
            base_url = f"{scheme}://{domain}"
            break
        except Exception:
            continue

    if not base_url:
        print(f"  {RED}[!]{RESET} Não foi possível ligar a {domain}")
        return []

    print(f"  {CYAN}[*]{RESET} Base URL: {base_url}")
    print(f"  {CYAN}[*]{RESET} Wordlist: {len(wordlist)} entradas\n")

    found   = []
    counter = [0]
    total   = len(wordlist)
    queue   = Queue()
    for w in wordlist:
        queue.put(w)

    def worker():
        while not queue.empty():
            path = queue.get()
            _fuzz_path(base_url, path, found, counter, total)
            queue.task_done()

    ts = [threading.Thread(target=worker) for _ in range(min(threads, total))]
    for t in ts: t.start()
    for t in ts: t.join()

    print(f"\n  {GREEN}[+]{RESET} Paths encontrados: {BOLD}{len(found)}{RESET}")
    return found

# ═══════════════════════════════════════════════════════════════
# 💾 Guardar resultados
# ═══════════════════════════════════════════════════════════════
def save_txt(data: dict, filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("Shadow CLI — Full Recon Report\n")
        f.write(f"Target    : {data['target']}\n")
        f.write(f"Generated : {data['timestamp']}\n")
        f.write("=" * 55 + "\n\n")

        if "shadowsub" in data:
            f.write("[ SHADOWSUB — Subdomínios ]\n")
            for s in data["shadowsub"]:
                f.write(f"  {s['subdomain']} ({s['ip']})\n")
            f.write("\n")

        if "shadowprobe" in data:
            f.write("[ SHADOWPROBE — Hosts Ativos ]\n")
            for h in data["shadowprobe"]:
                f.write(f"  [{h['status']}] {h['url']} | {h['title']}\n")
            f.write("\n")

        if "shadowscan" in data:
            scan = data["shadowscan"]
            f.write(f"[ SHADOWSCAN — {scan['host']} ({scan['ip']}) ]\n")
            for p in scan["open_ports"]:
                f.write(f"  [OPEN] Porta {p['port']} — {p['service']}\n")
            for k, v in scan.get("headers", {}).items():
                f.write(f"  {k}: {v}\n")
            f.write("\n")

        if "shadowbanner" in data:
            f.write("[ SHADOWBANNER — Banners ]\n")
            for b in data["shadowbanner"]:
                f.write(f"  [{b['port']}] {b['service']}\n")
                for k, v in b["info"].items():
                    f.write(f"    {k}: {v}\n")
            f.write("\n")

        if "shadowfuzz" in data:
            f.write("[ SHADOWFUZZ — Paths ]\n")
            for p in data["shadowfuzz"]:
                f.write(f"  [{p['status']}] {p['url']}\n")
            f.write("\n")

def save_json(data: dict, filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ═══════════════════════════════════════════════════════════════
# 🚀 MAIN
# ═══════════════════════════════════════════════════════════════
def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="Shadow CLI — Full Recon Framework by Mr Joker",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Exemplos:
  python shadow.py -t example.com --full-recon
  python shadow.py -t example.com --sub
  python shadow.py -t example.com --scan
  python shadow.py -t example.com --banner
  python shadow.py -t example.com --fuzz
  python shadow.py -t example.com --probe
        """
    )

    parser.add_argument("-t", "--target", required=True,
                        help="Domínio ou IP alvo")
    parser.add_argument("--full-recon", action="store_true",
                        help="Executa todas as ferramentas em sequência")
    parser.add_argument("--sub",    action="store_true", help="ShadowSub — Subdomain Finder")
    parser.add_argument("--probe",  action="store_true", help="ShadowProbe — HTTP/HTTPS Probe")
    parser.add_argument("--scan",   action="store_true", help="ShadowScan — Port Scanner")
    parser.add_argument("--banner", action="store_true", help="ShadowBanner — Banner Grabber")
    parser.add_argument("--fuzz",   action="store_true", help="ShadowFuzz — Directory Fuzzer")
    parser.add_argument("-w", "--wordlist",
                        help="Ficheiro de wordlist (para --sub e --fuzz)")
    parser.add_argument("--threads", type=int, default=20,
                        help="Número de threads (default: 20)")
    parser.add_argument("-o", "--output", default="shadow_report",
                        help="Nome base dos ficheiros de output (default: shadow_report)")

    args   = parser.parse_args()
    target = args.target.strip().replace("https://", "").replace("http://", "").rstrip("/")

    # Carregar wordlist externa ou usar defaults
    wordlist_sub  = DEFAULT_WORDLIST_SUB
    wordlist_fuzz = DEFAULT_WORDLIST_FUZZ
    if args.wordlist:
        try:
            with open(args.wordlist) as f:
                custom = [l.strip() for l in f if l.strip()]
            wordlist_sub  = custom
            wordlist_fuzz = custom
        except FileNotFoundError:
            print(f"  {RED}[!]{RESET} Wordlist '{args.wordlist}' não encontrada. A usar defaults.\n")

    data = {
        "target"    : target,
        "timestamp" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    print(f"  {CYAN}[*]{RESET} Target  : {BOLD}{target}{RESET}")
    print(f"  {CYAN}[*]{RESET} Threads : {BOLD}{args.threads}{RESET}")
    print(f"  {CYAN}[*]{RESET} Output  : {BOLD}{args.output}.txt / .json{RESET}")
    time.sleep(0.5)

    open_ports_cache = []

    # ── Full Recon ──────────────────────────────────────────
    if args.full_recon:
        subs        = run_shadowsub(target, wordlist_sub, args.threads)
        hosts       = [s["subdomain"] for s in subs] + [target]
        probe       = run_shadowprobe(hosts, args.threads)
        scan        = run_shadowscan(target)
        open_ports_cache = scan.get("open_ports", [])
        banners     = run_shadowbanner(target, open_ports_cache)
        fuzz        = run_shadowfuzz(target, wordlist_fuzz, args.threads)
        data.update({
            "shadowsub"    : subs,
            "shadowprobe"  : probe,
            "shadowscan"   : scan,
            "shadowbanner" : banners,
            "shadowfuzz"   : fuzz,
        })

    else:
        if args.sub:
            data["shadowsub"]   = run_shadowsub(target, wordlist_sub, args.threads)
        if args.probe:
            hosts = [s["subdomain"] for s in data.get("shadowsub", [])] + [target]
            data["shadowprobe"] = run_shadowprobe(hosts, args.threads)
        if args.scan:
            scan = run_shadowscan(target)
            open_ports_cache    = scan.get("open_ports", [])
            data["shadowscan"]  = scan
        if args.banner:
            data["shadowbanner"] = run_shadowbanner(target, open_ports_cache)
        if args.fuzz:
            data["shadowfuzz"]   = run_shadowfuzz(target, wordlist_fuzz, args.threads)

    # ── Guardar ─────────────────────────────────────────────
    txt_file  = f"{args.output}.txt"
    json_file = f"{args.output}.json"
    save_txt(data, txt_file)
    save_json(data, json_file)

    # ── Resumo final ────────────────────────────────────────
    print(f"\n{WHITE}{'═'*55}{RESET}")
    print(f"  {GREEN}{BOLD}[✓] Shadow CLI — Scan Concluído!{RESET}")
    print(f"  {CYAN}Target         :{RESET} {target}")
    if "shadowsub"    in data: print(f"  {CYAN}Subdomínios    :{RESET} {len(data['shadowsub'])}")
    if "shadowprobe"  in data: print(f"  {CYAN}Hosts ativos   :{RESET} {len(data['shadowprobe'])}")
    if "shadowscan"   in data: print(f"  {CYAN}Portas abertas :{RESET} {len(data['shadowscan']['open_ports'])}")
    if "shadowbanner" in data: print(f"  {CYAN}Banners        :{RESET} {len(data['shadowbanner'])}")
    if "shadowfuzz"   in data: print(f"  {CYAN}Paths found    :{RESET} {len(data['shadowfuzz'])}")
    print(f"  {CYAN}Output TXT     :{RESET} {txt_file}")
    print(f"  {CYAN}Output JSON    :{RESET} {json_file}")
    print(f"{WHITE}{'═'*55}{RESET}\n")


if __name__ == "__main__":
    main()
