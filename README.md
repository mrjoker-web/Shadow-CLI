<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Version-1.0-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Type-Full%20Recon%20Framework-red?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Termux-Compatible-black?style=for-the-badge&logo=android"/>
</p>

<h1 align="center">🖤 Shadow CLI</h1>
<p align="center"><b>Full Recon Framework — Shadow Suite Unificada</b></p>

---

## 📖 Sobre

**Shadow CLI** é o comando central que unifica toda a **Shadow Suite** numa única ferramenta.

Em vez de correr 4 ferramentas separadas, com um único comando tens toda a fase de reconnaissance executada em sequência, de forma automática e organizada.

Criado por **Mr Joker**. Compatível com **Linux** e **Termux**.

---

## ⚡ Tools Incluídas

| Tool | Função |
|------|--------|
| 🌐 ShadowSub | Subdomain Finder |
| ⚡ ShadowProbe | HTTP/HTTPS Probe |
| 🔍 ShadowScan | Port Scanner + Headers |
| 🚩 ShadowBanner | Banner Grabber |
| 💣 ShadowFuzz | Directory Fuzzer |

---

## 🔗 Pipeline Completo

```
ShadowSub    →  encontra subdomínios
     ↓
ShadowProbe  →  verifica hosts ativos
     ↓
ShadowScan   →  scan de portas + headers
     ↓
ShadowBanner →  identifica versões de serviços
     ↓
ShadowFuzz   →  descobre paths e directorias
```

---

## ⚙️ Instalação

### Linux

```bash
git clone https://github.com/mrjoker-web/ShadowCLI.git
cd ShadowCLI
pip install requests colorama urllib3
```

### Termux (Android)

```bash
pkg update && pkg upgrade
pkg install python git
git clone https://github.com/mrjoker-web/ShadowCLI.git
cd ShadowCLI
pip install requests colorama urllib3
```

---

## ▶️ Como usar

### Full Recon (todas as tools em sequência)

```bash
python shadow.py -t example.com --full-recon
```

### Tools individuais

```bash
python shadow.py -t example.com --sub        # Subdomain Finder
python shadow.py -t example.com --probe      # HTTP Probe
python shadow.py -t example.com --scan       # Port Scanner
python shadow.py -t example.com --banner     # Banner Grabber
python shadow.py -t example.com --fuzz       # Directory Fuzzer
```

### Com wordlist personalizada e threads

```bash
python shadow.py -t example.com --full-recon -w wordlist.txt --threads 50
```

### Com nome de output personalizado

```bash
python shadow.py -t example.com --full-recon -o relatorio_exemplo
```

---

## 📸 Exemplo de Output

```
═══════════════════════════════════════════════════════
  🌐 SHADOWSUB — Subdomain Finder
═══════════════════════════════════════════════════════
  [FOUND] admin.example.com (93.184.216.10)
  [FOUND] api.example.com   (93.184.216.11)
  [+] Subdomínios encontrados: 2

═══════════════════════════════════════════════════════
  ⚡ SHADOWPROBE — HTTP/HTTPS Probe
═══════════════════════════════════════════════════════
  [200] https://admin.example.com | Admin Panel
  [200] https://api.example.com   | API Gateway
  [+] Hosts ativos: 2

═══════════════════════════════════════════════════════
  🔍 SHADOWSCAN — Port Scanner & Recon
═══════════════════════════════════════════════════════
  [+] IP: 93.184.216.34
  [OPEN] Porta 22  — SSH
  [OPEN] Porta 80  — HTTP
  [OPEN] Porta 443 — HTTPS
  [HDR] Server: Apache/2.4.52 (Ubuntu)

═══════════════════════════════════════════════════════
  🚩 SHADOWBANNER — Banner Grabber
═══════════════════════════════════════════════════════
  [+] Porta 22 — SSH
      Banner             SSH-2.0-OpenSSH_8.2p1
  [+] Porta 80 — HTTP
      Server             Apache/2.4.52

═══════════════════════════════════════════════════════
  💣 SHADOWFUZZ — Directory Fuzzer
═══════════════════════════════════════════════════════
  [200] https://example.com/admin
  [403] https://example.com/backup
  [200] https://example.com/api
  [+] Paths encontrados: 3

═══════════════════════════════════════════════════════
  [✓] Shadow CLI — Scan Concluído!
  Target         : example.com
  Subdomínios    : 2
  Hosts ativos   : 2
  Portas abertas : 3
  Banners        : 2
  Paths found    : 3
  Output TXT     : shadow_report.txt
  Output JSON    : shadow_report.json
═══════════════════════════════════════════════════════
```

---

## 📁 Ficheiros de Output

| Ficheiro | Formato | Conteúdo |
|---|---|---|
| `shadow_report.txt` | Texto simples | Relatório completo legível |
| `shadow_report.json` | JSON estruturado | Todos os dados para automação |

---

## 📌 Roadmap

- [ ] ShadowWhois — OSINT Tool
- [ ] ShadowHash — Hash Identifier & Cracker
- [ ] ShadowSSL — SSL/TLS Analyzer
- [ ] Exportação em HTML
- [ ] Modo silencioso (`--silent`)

---

## ⚠️ Disclaimer

> Esta ferramenta foi desenvolvida **apenas para fins educacionais e testes em sistemas autorizados**.  
> O uso indevido é da **inteira responsabilidade do utilizador**.  
> Nunca uses esta ferramenta em sistemas sem autorização explícita.

---

## 👨‍💻 Autor

**Mr Joker**  
🔗 [github.com/mrjoker-web](https://github.com/mrjoker-web)  
🔒 Cybersecurity Enthusiast | Pentesting Tools Developer
