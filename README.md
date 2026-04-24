<div align="center">

```
  ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗
  ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║
  ███████╗███████║███████║██║  ██║██║   ██║██║ █╗ ██║
  ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██║███╗██║
  ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝╚███╔███╔╝
  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚══╝╚══╝

          ██████╗██╗     ██╗
         ██╔════╝██║     ██║
         ██║     ██║     ██║
         ██║     ██║     ██║
         ╚██████╗███████╗██║
          ╚═════╝╚══════╝╚═╝
```

### `// Full Recon Framework — Shadow Suite`

**ShadowSub · ShadowProbe · ShadowScan · ShadowBanner · ShadowFuzz**

[![Python](https://img.shields.io/badge/Python-3.6+-3776AB?style=for-the-badge&logo=python&logoColor=white)](.)
[![Requests](https://img.shields.io/badge/requests-required-e8734a?style=for-the-badge)](.)
[![Colorama](https://img.shields.io/badge/colorama-required-f0c94d?style=for-the-badge)](.)
[![License](https://img.shields.io/badge/license-MIT-52c98b?style=for-the-badge)](.)
[![Shadow Suite](https://img.shields.io/badge/Shadow-Suite-e05260?style=for-the-badge)](https://github.com/mrjoker-web)

</div>

---

## `> about`

**Shadow CLI** é o centro de comando da Shadow Suite — um framework de recon completo que encadeia 5 ferramentas num único pipeline automatizado.

Um alvo. Um comando. Relatório completo.

```bash
python shadow.py -t example.com --full-recon
```

---

## `> pipeline`

```
                        TARGET
                           │
                           ▼
          ┌────────────────────────────┐
          │  🌐 ShadowSub               │  Subdomain enumeration
          │  Descobre subdomínios       │  via wordlist + threads
          └──────────────┬─────────────┘
                         │  [subdomínios encontrados]
                         ▼
          ┌────────────────────────────┐
          │  ⚡ ShadowProbe             │  HTTP/HTTPS probing
          │  Filtra hosts ativos       │  status + título
          └──────────────┬─────────────┘
                         │  [hosts vivos]
                         ▼
          ┌────────────────────────────┐
          │  🔍 ShadowScan              │  Port scanning
          │  Analisa portas e headers  │  + HTTP headers
          └──────────────┬─────────────┘
                         │  [portas abertas]
                         ▼
          ┌────────────────────────────┐
          │  🏷️  ShadowBanner           │  Banner grabbing
          │  Identifica serviços       │  FTP/SSH/HTTP/DB...
          └──────────────┬─────────────┘
                         │
                         ▼
          ┌────────────────────────────┐
          │  💣 ShadowFuzz              │  Directory fuzzing
          │  Descobre paths ocultos    │  .env / admin / backup...
          └──────────────┬─────────────┘
                         │
                         ▼
                ┌─────────────────┐
                │  📄 RELATÓRIO   │  shadow_report.txt
                │                 │  shadow_report.json
                └─────────────────┘
```

---

## `> modules`

```
┌──────────────────────────────────────────────────────────────┐
│                         MÓDULOS                              │
├──────────────┬───────────────────────────────────────────────┤
│ 🌐 ShadowSub  │ Subdomain finder via wordlist multi-thread    │
│ ⚡ ShadowProbe │ HTTP/HTTPS probe — status code + título      │
│ 🔍 ShadowScan  │ Port scanner — 14 portas críticas + headers  │
│ 🏷️  ShadowBanner│ Banner grabbing — FTP, SSH, HTTP, DB        │
│ 💣 ShadowFuzz  │ Directory fuzzer — paths ocultos e sensíveis │
│ 📄 Report      │ Export TXT + JSON automático                 │
└──────────────┴───────────────────────────────────────────────┘
```

**Portas scaneadas por default:**

| Porta | Serviço | Porta | Serviço |
|-------|---------|-------|---------|
| 21 | FTP | 443 | HTTPS |
| 22 | SSH | 3306 | MySQL |
| 23 | Telnet | 5432 | PostgreSQL |
| 25 | SMTP | 6379 | Redis |
| 80 | HTTP | 8080 | HTTP-Alt |
| 110 | POP3 | 8443 | HTTPS-Alt |
| 143 | IMAP | 27017 | MongoDB |

---

## `> requirements`

```bash
pip install requests colorama
```

---

## `> install`

```bash
git clone https://github.com/mrjoker-web/ShadowCLI.git
cd ShadowCLI
pip install -r requirements.txt
python shadow.py --help
```

---

## `> usage`

```bash
python shadow.py -t <target> [módulos] [opções]
```

### Exemplos

```bash
# Full recon — pipeline completo automático
python shadow.py -t example.com --full-recon

# Full recon + relatório custom
python shadow.py -t example.com --full-recon -o cliente_audit

# Só subdomain finder
python shadow.py -t example.com --sub

# Subdomain + probe (hosts ativos)
python shadow.py -t example.com --sub --probe

# Port scan + banner grabbing
python shadow.py -t example.com --scan --banner

# Directory fuzzing com wordlist custom
python shadow.py -t example.com --fuzz -w /usr/share/wordlists/dirb/common.txt

# Mais threads para maior velocidade
python shadow.py -t example.com --full-recon --threads 50

# Wordlist externa para sub + fuzz
python shadow.py -t example.com --full-recon -w wordlist.txt -o report
```

### Todas as opções

```
-t, --target        Domínio ou IP alvo (obrigatório)
--full-recon        Executa todos os módulos em sequência
--sub               ShadowSub — Subdomain Finder
--probe             ShadowProbe — HTTP/HTTPS Probe
--scan              ShadowScan — Port Scanner + Headers
--banner            ShadowBanner — Banner Grabber
--fuzz              ShadowFuzz — Directory Fuzzer
-w, --wordlist      Wordlist externa (para --sub e --fuzz)
--threads INT       Threads concorrentes (default: 20)
-o, --output        Nome base do relatório (default: shadow_report)
-h, --help          Mostrar ajuda
```

---

## `> output example`

```
  ══════════════════════════════════════════════════════
    🌐 SHADOWSUB — Subdomain Finder
  ══════════════════════════════════════════════════════

  [FOUND] api.example.com (93.184.216.34)
  [FOUND] mail.example.com (93.184.216.35)
  [FOUND] dev.example.com (93.184.216.36)
  ShadowSub [████████████████████████████] 100.0%

  [+] Subdomínios encontrados: 3

  ══════════════════════════════════════════════════════
    ⚡ SHADOWPROBE — HTTP/HTTPS Probe
  ══════════════════════════════════════════════════════

  [200] https://api.example.com | Example API
  [301] https://mail.example.com | N/A
  [200] https://dev.example.com | Dev Portal

  [+] Hosts ativos: 3

  ══════════════════════════════════════════════════════
    🔍 SHADOWSCAN — Port Scanner
  ══════════════════════════════════════════════════════

  [OPEN] Porta 22  — SSH
  [OPEN] Porta 80  — HTTP
  [OPEN] Porta 443 — HTTPS

  ══════════════════════════════════════════════════════
    💣 SHADOWFUZZ — Directory Fuzzer
  ══════════════════════════════════════════════════════

  [200] https://example.com/admin
  [200] https://example.com/.env        ← 🔴 CRÍTICO
  [200] https://example.com/backup

  ══════════════════════════════════════════════════════
    [✓] Shadow CLI — Scan Concluído!
  ══════════════════════════════════════════════════════

  Target         : example.com
  Subdomínios    : 3
  Hosts ativos   : 3
  Portas abertas : 3
  Banners        : 2
  Paths found    : 3
  Output TXT     : shadow_report.txt
  Output JSON    : shadow_report.json
```

---

## `> json report`

```json
{
  "target": "example.com",
  "timestamp": "2025-01-15 22:31:04",
  "shadowsub": [
    { "subdomain": "api.example.com", "ip": "93.184.216.34" },
    { "subdomain": "mail.example.com", "ip": "93.184.216.35" }
  ],
  "shadowprobe": [
    { "host": "api.example.com", "url": "https://api.example.com",
      "status": 200, "title": "Example API" }
  ],
  "shadowscan": {
    "host": "example.com",
    "ip": "93.184.216.34",
    "open_ports": [
      { "port": 22, "service": "SSH" },
      { "port": 443, "service": "HTTPS" }
    ]
  },
  "shadowfuzz": [
    { "url": "https://example.com/.env", "status": 200 },
    { "url": "https://example.com/admin", "status": 200 }
  ]
}
```

---

## `> wordlists`

O Shadow CLI tem wordlists built-in para funcionar sem configuração:

**Subdomínios (built-in):** `www, mail, ftp, admin, api, dev, staging, vpn, portal, cdn, app, dashboard` + mais 14

**Fuzzing (built-in):** `admin, login, dashboard, .env, backup, config, api, uploads, wp-admin, phpmyadmin` + mais 20

**Wordlists externas recomendadas:**
```bash
# SecLists (recomendado)
git clone https://github.com/danielmiessler/SecLists.git

# Uso com Shadow CLI
python shadow.py -t example.com --sub \
  -w SecLists/Discovery/DNS/subdomains-top1million-5000.txt

python shadow.py -t example.com --fuzz \
  -w SecLists/Discovery/Web-Content/common.txt
```

---

## `> roadmap`

```
✅ ShadowSub   — Subdomain finder multi-thread
✅ ShadowProbe — HTTP/HTTPS probe com título
✅ ShadowScan  — Port scanner + HTTP headers
✅ ShadowBanner — Banner grabbing por protocolo
✅ ShadowFuzz  — Directory fuzzer
✅ Export TXT + JSON
✅ Pipeline --full-recon encadeado
🔄 Integração com ShadowScanner (deep network scan)
🔄 Integração com ShadowDroid (mobile recon)
🔄 Report HTML automático para clientes
🔄 CVE lookup por serviço e versão detectada
🔄 Rate limiting e evasão de WAF
🔄 Output em Markdown para relatórios
```

---

## `> shadow suite`

| Tool | Descrição | Repo |
|------|-----------|------|
| 🌐 ShadowSub | Subdomain finder | [mrjoker-web/ShadowSub](https://github.com/mrjoker-web/ShadowSub) |
| ⚡ ShadowProbe | HTTP/HTTPS probe | [mrjoker-web/ShadowProbe](https://github.com/mrjoker-web/ShadowProbe) |
| 🔍 ShadowScan | Recon tool | [mrjoker-web/ShadowScan-Tool](https://github.com/mrjoker-web/ShadowScan-Tool) |
| 🛡️ ShadowScanner | Network scanner | [mrjoker-web/ShadowScanner](https://github.com/mrjoker-web/ShadowScanner) |
| 📱 ShadowDroid | Android ADB audit | [mrjoker-web/ShadowDroid-](https://github.com/mrjoker-web/ShadowDroid-) |
| ⚙️ ShadowSetup | Terminal setup | [mrjoker-web/ShadowSetup](https://github.com/mrjoker-web/ShadowSetup) |
| 🖥️ Shadow CLI | Full recon framework | **este repo** |

---

## `> disclaimer`

```
⚠  AVISO LEGAL

Esta ferramenta foi desenvolvida exclusivamente para:
  • Auditorias profissionais em sistemas autorizados
  • Testes em ambientes próprios ou de laboratório
  • Fins educacionais e de investigação em segurança

A utilização em sistemas sem autorização é ilegal.
O autor não se responsabiliza por qualquer uso indevido.
```

---

## `> author`

<div align="center">

Feito por **[Mr Joker](https://github.com/mrjoker-web)** — Aspiring Pentester & Python Tools Developer · Lisboa, PT

[![GitHub](https://img.shields.io/badge/GitHub-mrjoker--web-181717?style=for-the-badge&logo=github)](https://github.com/mrjoker-web)
[![Telegram](https://img.shields.io/badge/Telegram-mr__joker78-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/mr_joker78)
[![Twitter/X](https://img.shields.io/badge/X-mrjoker3790-000000?style=for-the-badge&logo=x&logoColor=white)](https://x.com/mrjoker3790)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Mr%20Joker-0e76a8?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mr-joker-951ab2357)

*Se achares útil, deixa uma ⭐ — ajuda a Shadow Suite a crescer!*

</div>
