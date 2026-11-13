# NetworkWalks Cybersecurity Internship — Week 2 Final Technical Report

## Practical Modules PM1 (Web Footprinting) & PM5 (Zenmap Network Scanning)

---

### Student & Project Metadata

| Field | Detail |
|---|---|
| **Student Name** | **RITHISH S P** |
| **Internship Program** | NetworkWalks Cybersecurity Internship |
| **Module / Week** | Week 2: Information Gathering, Footprinting & Network Scanning |
| **Practical Tasks** | Module PM1 (External Web Footprinting) & Module PM5 (Internal LAN Zenmap Scanning) |
| **Submission Date** | 13 November 2026 |
| **Host System** | Lenovo IdeaPad Slim 3 15IRH10 (13th Gen Intel Core i5-13420H, 16.0 GB RAM, Windows 11) |
| **Secondary OS** | Kali Linux 2026.2 (amd64) on Oracle VirtualBox 7.2.22 |
| **Repository URL** | https://github.com/Ritzz-09/Networkwalks-Internship |
| **Repository Path** | `Networkwalks-Internship/week2/` |

---

## 1. Executive Summary

This comprehensive technical report documents the practical execution, empirical observations, and analytical findings for **Week 2** of the **NetworkWalks Cybersecurity Internship**, conducted by **RITHISH S P**. 

The operational focus of Week 2 centered on foundational cybersecurity reconnaissance, bifurcated into two distinct operational scopes:
1. **Module PM1 — External Domain & Web Application Footprinting:** Conducting passive OSINT and active reconnaissance against the target domain `networkwalks.com` (resolved IP `192.232.216.135`). Six core utilities were deployed: **WHOIS**, **WhatWeb**, **nslookup**, **cURL**, **WAFW00F**, and **DNSRecon**.
2. **Module PM5 — Internal Local Area Network (LAN) Reconnaissance:** Conducting Layer 2 and Layer 3 host discovery, ARP sweeps, and network topology mapping across the private subnet `192.168.1.0/24` using **Zenmap / Nmap 7.993** from an active Wi-Fi interface.

All findings, configurations, and analytical deductions presented in this report are strictly derived from verified empirical artifacts, terminal captures, scan logs, and official task documents present within the repository.

---

## 2. Technical Objectives

* **External Surface Mapping:** Enumerate registrar records, administrative data, authoritative nameservers, and expiration horizons to establish domain provenance.
* **Application Stack Identification:** Detect underlying Web servers, Content Management Systems (CMS), scripting environments, and client-side libraries.
* **Defensive Controls Assessment:** Identify active Web Application Firewalls (WAF) and reverse proxy architectures.
* **DNS Infrastructure Enumeration:** Query Start of Authority (SOA), Nameserver (NS), Mail Exchange (MX), Sender Policy Framework (SPF), and Service (SRV) autodiscovery records.
* **Internal Network Host Discovery:** Execute high-speed ping sweeps across `192.168.1.0/24` to discover active IP endpoints and measure network latency.
* **Hardware Layer (MAC) Resolution:** Map physical Layer 2 MAC addresses to active IPv4 leases and identify network interface card (NIC) hardware manufacturers.
* **Network Topology Graphing:** Model broadcast domain topology and evaluate edge visibility.
* **Defensive Security Analysis:** Identify architectural vulnerabilities inherent in unsegmented flat subnets (ARP spoofing, broadcast storm exposure, lack of 802.1X).

---

## 3. Module PM1 — Web Application & External Domain Footprinting

Module PM1 entailed comprehensive external reconnaissance against the production domain `networkwalks.com`. Reconnaissance was executed from a Kali Linux security environment.

### 3.1 Tool 1: WHOIS Domain Intelligence & Registration Profiling

* **Objective:** Interrogate regional Internet registry databases to extract ownership provenance, registrar identity, registration dates, domain status flags, and authoritative nameserver delegations.
* **Tool Description:** WHOIS is a standard query and response protocol (RFC 3912) used to query databases that store the registered users or assignees of an Internet resource.
* **Command Executed:**
  ```bash
  whois networkwalks.com
  ```
  *(Verified from screenshot prompt `ritzz-07@Aizen-07 ~/Desktop > whois networkwalks.com`)*
* **Methodology:** The command initiates a TCP port 43 query to the VeriSign Global Registry Services, which directs the client to the sponsoring registrar's WHOIS service (`whois.godaddy.com`).
* **Actual Findings:**
  * **Registrar:** `GoDaddy.com, LLC` (IANA ID: `146`)
  * **Creation Date:** `2019-11-06T22:51:46Z`
  * **Registry Expiry Date:** `2027-11-06T22:51:46Z` (Active registration secured through November 2027)
  * **Updated Date:** `2025-11-12T10:08:43Z`
  * **Authoritative Nameservers:** `NS6135.HOSTGATOR.COM` and `NS6136.HOSTGATOR.COM`
  * **Registrant Privacy:** Shielded by `Domains By Proxy, LLC` (Tempe, Arizona, United States). Direct registrant PII (email, address, telephone) is masked.
  * **Domain Status Flags:** `clientDeleteProhibited`, `clientRenewProhibited`, `clientTransferProhibited`, `clientUpdateProhibited` (standard Extensible Provisioning Protocol (EPP) safeguards against unauthorized domain hijacking).
* **Screenshot Evidence:** `week2/PM1-footprinting/tool1-whois/whois.png`
* **Raw Log File:** `week2/PM1-footprinting/tool1-whois/whois-output.txt`

---

### 3.2 Tool 2: WhatWeb Next-Generation Web Fingerprinting

* **Objective:** Fingerprint the target web application stack, identifying the Content Management System (CMS), web server engine, scripting modules, analytics tags, and active session cookies.
* **Tool Description:** WhatWeb is an advanced web scanner that identifies websites, content management systems, blogging platforms, JavaScript libraries, and web servers using over 1800 plugins.
* **Command Executed:**
  ```bash
  whatweb networkwalks.com | tee ~/whatweb-output.txt
  ```
  *(Verified from screenshot prompt `ritzz-07@Aizen-07 ~/Desktop > whatweb networkwalks.com | tee ~/whatweb-output.txt`)*
* **Methodology:** WhatWeb sends HTTP GET requests, evaluates HTTP response headers, parses HTML `<meta>` generator tags, inspects JavaScript variable references, and tests redirection behavior.
* **Actual Findings:**
  * **Redirect Path:** `http://networkwalks.com` returns `301 Moved Permanently` to `https://networkwalks.com/` (enforcing HTTPS encryption).
  * **Web Server:** `Apache`
  * **Content Management System:** `WordPress 7.1.4`
  * **WordPress Extensions:** `WordPress Download Manager (WPDM) 3.3.76`
  * **Frontend Frameworks:** `Bootstrap 7.1.4`, `jQuery 3.7.1`
  * **Analytics / Tagging:** `Google-Tag-Manager`
  * **Target IP Address:** `192.232.216.135` (Geolocation: United States)
  * **Application Cookies:** `__wpdm_client` (flagged with `HttpOnly` and `Secure`, restricting client-side script access).
  * **Cache Indicators:** `x-endurance-cache-level: 0`, `x-nginx-cache: WordPress`
* **Screenshot Evidence:** `week2/PM1-footprinting/tool2-whatweb/whatweb.png`
* **Raw Log File:** `week2/PM1-footprinting/tool2-whatweb/whatweb-output.txt`

---

### 3.3 Tool 3: nslookup DNS Querying & Address Resolution

* **Objective:** Query domain name system servers to resolve the domain name `networkwalks.com` to its corresponding IPv4 network address.
* **Tool Description:** `nslookup` is a command-line administrative tool for testing and troubleshooting Domain Name System (DNS) servers.
* **Command Executed:**
  ```bash
  nslookup networkwalks.com | tee ~/nslookup-output.txt
  ```
  *(Verified from screenshot prompt `ritzz-07@Aizen-07 ~/Desktop > nslookup networkwalks.com | tee ~/nslookup-output.txt`)*
* **Methodology:** The host issues an A-record query for `networkwalks.com` directed at its locally configured recursive resolver.
* **Actual Findings:**
  * **Local Recursive Server:** `192.168.190.2` (Port `53`)
  * **Response Status:** Non-authoritative answer (retrieved from resolver cache).
  * **Resolved IPv4 Address:** `192.232.216.135`
* **Screenshot Evidence:** `week2/PM1-footprinting/tool3-nslookup/nslookup.png`
* **Raw Log File:** `week2/PM1-footprinting/tool3-nslookup/nslookup-output.txt`

---

### 3.4 Tool 4: cURL HTTP Header Inspection & Banner Grabbing

* **Objective:** Inspect HTTP server response headers, caching layers, server software banners, and cookie policies without downloading web page bodies.
* **Tool Description:** cURL is a command-line tool for transferring data using various network protocols, ideal for low-overhead HTTP transactions.
* **Command Executed:**
  ```bash
  curl -I https://networkwalks.com | tee ~/curl-output.txt
  ```
  *(Verified from screenshot prompt `ritzz-07@Aizen-07 ~/Downloads/week-2/PM1/tool4-curl > curl -I https://networkwalks.com | tee ~/curl-output.txt`)*
* **Methodology:** The `-I` (`--head`) switch requests headers only via an HTTP HEAD request.
* **Actual Findings:**
  * **Protocol & Status:** `HTTP/2 200`
  * **Server Header:** `server: Apache`
  * **Cache Hierarchy:** Multi-layer caching identified by `x-nginx-cache: WordPress` and `x-endurance-cache-level: 0`. This reveals that Nginx operates as a reverse proxy accelerator in front of the backend Apache server.
  * **Session Cookie:** `set-cookie: __wpdm_client=f9e5627f5813d42b69e96f0c3a906902; path=/; domain=networkwalks.com; secure; HttpOnly`
  * **Permissions Policy:** Defines token redemption and issuance permissions for Google, Cloudflare, and hCaptcha.
* **Screenshot Evidence:** `week2/PM1-footprinting/tool4-curl/curl.png`
* **Raw Log File:** `week2/PM1-footprinting/tool4-curl/curl-output.txt`

---

### 3.5 Tool 5: WAFW00F Web Application Firewall Fingerprinting

* **Objective:** Probe the target web application to ascertain whether a Web Application Firewall (WAF) intercepts HTTP traffic, and fingerprint the specific WAF vendor.
* **Tool Description:** WAFW00F is an automated fingerprinting toolkit that identifies and fingerprints Web Application Firewall (WAF) products.
* **Command Executed:**
  ```bash
  wafw00f networkwalks.com | tee ~/waf-output.txt
  ```
  *(Verified from screenshot prompt `ritzz-07@Aizen-07 ~/Downloads/week-2/PM1 > wafw00f networkwalks.com | tee ~/waf-output.txt`)*
* **Methodology:** WAFW00F sends standard HTTP requests, observes responses, and subsequently sends provocative payloads (malformed HTTP methods, cross-site scripting vectors, directory traversals). It compares response codes, error pages, and HTTP headers against vendor signatures.
* **Actual Findings:**
  * **Detected Product:** **`ModSecurity (SpiderLabs)`**
  * **Target Analyzed:** `https://networkwalks.com`
  * **Number of Requests:** 2 requests sent
  * **Security Implications:** ModSecurity is an open-source web application firewall deployed on Apache/Nginx. This indicates active inspection of inbound URI queries, POST parameters, and headers against the OWASP Core Rule Set (CRS).
* **Screenshot Evidence:** `week2/PM1-footprinting/tool5-waf/waf.png`
* **Raw Log File:** `week2/PM1-footprinting/tool5-waf/waf-output.txt`

---

### 3.6 Tool 6: DNSRecon Comprehensive DNS Record & Service Enumeration

* **Objective:** Perform zone enumeration against `networkwalks.com` to discover nameservers, BIND software versions, mail exchanges, SPF validation rules, and SRV service autodiscovery records.
* **Tool Description:** DNSRecon is an advanced DNS reconnaissance tool written in Python, designed to perform general enumeration, zone transfers, and service discovery.
* **Command Executed:**
  ```bash
  dnsrecon -d networkwalks.com | tee ~/dnsrecon-output.txt
  ```
  *(Verified from screenshot prompt `ritzz-07@Aizen-07 ~/Downloads/week-2/PM1 > dnsrecon -d networkwalks.com | tee ~/dnsrecon-output.txt`)*
* **Methodology:** DNSRecon executes a standard enumeration battery: checking for DNSSEC support, querying SOA records, nameserver records, BIND software version queries (`version.bind`), MX records, A/AAAA records, TXT records, and standard SRV service records.
* **Actual Findings:**
  * **DNSSEC:** No answer for DNSSEC query (zone is unsigned).
  * **Start of Authority (SOA):** `ns6135.hostgator.com` (IP: `50.87.144.87`)
  * **Authoritative Nameservers:**
    * `ns6135.hostgator.com` (`50.87.144.87`) — BIND Version: `"9.16.23-RH"`
    * `ns6136.hostgator.com` (`192.232.216.131`) — BIND Version: `"9.16.23-RH"`
  * **Mail Exchange (MX):** `mail.networkwalks.com` (`192.232.216.135`)
  * **A Record:** `networkwalks.com` -> `192.232.216.135`
  * **TXT Records:**
    * `v=spf1 +a +mx +ip4:50.87.144.87 +include:websitewelcome.com ~all`
    * `google-site-verification=rr04eRmqHoWY3XemnizDNVK4q75X-Ij-mjgEeg-UsYI`
  * **SRV Service Records:** 8 autodiscover records identified for `_autodiscover._tcp.networkwalks.com` pointing to `cpanelemaildiscovery.cpanel.net:443` across IP block `184.94.203.x / 184.94.204.x`.
* **Screenshot Evidence:** `week2/PM1-footprinting/tool6-dnsrecon/dnsrecon.png`
* **Raw Log File:** `week2/PM1-footprinting/tool6-dnsrecon/dnsrecon-output.txt`
* **CRITICAL EVIDENCE VERIFICATION NOTE:** 
  > [!IMPORTANT]
  > In the repository's initial commit (`98774e9`), the file `dnsrecon-output.txt` was recorded as 0 bytes. Inspection of the screenshot `dnsrecon.png` reveals that the command was executed with `| tee ~/dnsrecon-output.txt`. The `~` syntax redirected stdout to the host user's home directory (`/home/ritzz-07/dnsrecon-output.txt`), rather than the local repository folder. The terminal screenshot conclusively verifies the full successful execution, and the output text has been verified against the terminal capture.

---

## 4. Module PM5 — Zenmap Based Local Network Scanning

### 4.1 Environmental Parameters & Audit Context

Module PM5 transitioned the assessment from external surface mapping to internal broadcast domain reconnaissance. The scan was conducted on the student's physical host workstation connected to an active wireless local area network.

| Environmental Metric | Verified Parameter | Source / Verification Method |
|---|---|---|
| **Auditing Software** | **Zenmap GUI / Nmap Engine 7.993** | Scan header / Task PDF |
| **Operating System** | **Microsoft Windows 11 Home** | Task report & host specifications |
| **Physical Adapter** | **Wi-Fi (Wireless Interface)** | Host network configuration |
| **Local IPv4 Address** | **`192.168.1.36`** | Task 2 & Windows `ipconfig /all` |
| **Subnet Mask** | **`255.255.255.0` (`/24`)** | Task 2 & Windows `ipconfig /all` |
| **LAN Subnet Range** | **`192.168.1.0/24`** (`192.168.1.1` – `192.168.1.254`) | Task 2 specification |
| **Default Gateway** | **`192.168.1.1`** | Task 2 & routing table |
| **Scan Profile** | **Ping scan** | Zenmap profile dropdown |
| **Executed Command** | **`nmap -sn 192.168.1.0/24`** | Zenmap command field |
| **Addresses Evaluated** | **256 IP Addresses** | Nmap scan summary |
| **Live Hosts Discovered** | **8 Hosts Active** | Nmap output & Task 4 |
| **Scan Duration** | **11.43 seconds** | Nmap scan summary |

---

### 4.2 Scanning Methodology & Protocol Mechanics

The command executed was `nmap -sn 192.168.1.0/24`:
1. **The `-sn` Flag (No Port Scan):** Formerly known as `-sP`, this instruction disables transport-layer port scanning. Nmap focuses exclusively on host discovery.
2. **Layer 2 ARP Discovery Mechanics:** Because the scanning interface resides on the same Ethernet broadcast domain (`192.168.1.0/24`), Nmap overrides standard ICMP echo requests with native **ARP (Address Resolution Protocol) requests**.
3. **Efficiency:** ARP requests cannot be firewalled by host operating systems (e.g., Windows Defender Firewall) without severing local Layer 2 communications. This ensures 100% discovery accuracy across the local subnet.
4. **Local Host Exception:** Nmap cannot query its own interface via ARP. Consequently, the local scanning host (`192.168.1.36`) is identified as "Host is up" via internal loopback queries without a MAC address in Nmap's raw output. The physical MAC for `192.168.1.36` was retrieved via Windows `ipconfig /all`.

---

### 4.3 Live Hosts Inventory & Hardware Addressing

The table below catalogs all 8 discovered endpoints on `192.168.1.0/24`:

| Index | IPv4 Address | Hardware MAC Address | Vendor / Discovery Source | Latency | Device Role & Network Function |
|:---:|---|---|---|:---:|---|
| **1** | `192.168.1.1` | `54:47:E8:A6:B2:D3` | **Syrotech Networks.** (Zenmap) | 0.0070s | **Default Gateway / Wireless Router / ONT** |
| **2** | `192.168.1.33` | `5A:5A:02:5B:74:8D` | Unknown / Private MAC (Zenmap) | 0.0150s | Active LAN Client / Mobile Device |
| **3** | `192.168.1.35` | `C6:BC:B3:DD:A7:B3` | Unknown / Private MAC (Zenmap) | 0.0710s | Active LAN Client / Laptop / Smart Device |
| **4** | `192.168.1.36` | `B8:F7:75:AB:8C:2C` | **Windows `ipconfig /all`** | 0.0000s | **Local Scanning Workstation (Lenovo IdeaPad)** |
| **5** | `192.168.1.197` | `5A:5A:00:DE:4F:CB` | Unknown / Private MAC (Zenmap) | 6.4000s | High-Latency Wireless Client / IoT Endpoint |
| **6** | `192.168.1.208` | `5A:5A:00:DE:49:93` | Unknown / Private MAC (Zenmap) | 0.0280s | Active LAN Client |
| **7** | `192.168.1.230` | `5A:5A:00:DE:49:9D` | Unknown / Private MAC (Zenmap) | 1.2000s | Active LAN Client |
| **8** | `192.168.1.237` | `5A:5A:00:DE:49:BD` | Unknown / Private MAC (Zenmap) | 1.0000s | Active LAN Client |

#### Analysis of MAC Vendors & Latency Variance:
* **Gateway Identity:** MAC prefix `54:47:E8` identifies the manufacturer **Syrotech Networks**, indicating a GPON Optical Network Terminal (ONT) / fiber broadband gateway.
* **Locally Administered Addresses (LAA):** Six devices display MAC addresses starting with `5A:5A:...` and `C6:BC:...`. The second least-significant bit of the first octet is set to `1` (binary `xx..xx1x`), signifying **Locally Administered / Randomized MAC Addresses**. Modern Android, iOS, and Windows 11 endpoints utilize MAC randomization by default to prevent tracking.
* **Latency Profile:** Low latency (<30ms) observed on nodes `.1`, `.33`, and `.208` reflects strong wireless link quality. Node `.197` exhibits extreme latency (6.4 seconds), typical of deep power-save sleep states in IoT devices or weak Wi-Fi edge coverage.

---

### 4.4 Network Topology Visualization & Label Crowding Assessment

Zenmap generates radial and spring-loaded topology graphs using the Graphviz engine:
* **Central Anchor:** `localhost` (`192.168.1.36`).
* **Outer Ring:** Radial dashed links connecting `localhost` directly to all 8 discovered endpoints.

#### Topology Label Collision Flag:
> [!WARNING]
> **Deficiency Flagged for Correction:** As documented in Page 4 of `PM5_Task_Answers_and_Evidence_RITHISH_SP.pdf` and verified in `topology.pdf`, the exported Zenmap radial layout exhibits severe label crowding and overlap:
> 1. `192.168.1.35` heavily collides with `192.168.1.230` on the upper perimeter.
> 2. `192.168.1.1` heavily collides with `192.168.1.36` on the lower perimeter.
> 
> **Evaluation Recommendation:** This exported topology layout should **not** be accepted as a final engineering schematic. A repositioned, non-overlapping spring or hierarchical graph must be generated before executive publication.

---

## 5. Security & Privacy Audit Findings

A rigorous security and privacy audit was conducted across all files, terminal logs, and Git history in the repository.

### 5.1 Audit Findings Matrix

| Finding Category | Severity | Item Identified | File / Location | Exposure Context & Risk Assessment | Mitigation / Recommendation |
|---|:---:|---|---|---|---|
| **Session Cookies** | **Medium** | `__wpdm_client=f9e5627f...` | `curl-output.txt`, `whatweb-output.txt`, `curl.png` | Client tracking cookie for WordPress Download Manager. While `HttpOnly` and `Secure`, exposed session tokens can be replayed if not expired. | Redact session hashes in public documentation (`__wpdm_client=[REDACTED]`). |
| **Personal Email** | **Low** | `sprithish1409@gmail.com` | Git commit author history | Personal email address baked into Git commits (`98774e9`, `b70e0d9`, `153a296`, `3622eb2`). | Do not attempt destructive history rewrites. Maintain private repo visibility or use GitHub privacy email (`@users.noreply.github.com`) for future commits. |
| **Target Contacts** | **Info** | `info@networkwalks.com`, `abuse@godaddy.com` | `whatweb-output.txt`, `whois-output.txt` | Public organizational contact addresses. | Public data; no remediation needed. |
| **Internal IP Addressing** | **Low** | `192.168.1.36`, `192.168.1.0/24`, `192.168.190.2` | Zenmap report, PM5 logs, nslookup | Private RFC 1918 addresses. Non-routable on the public Internet, but reveals internal subnet structure. | Mask the 3rd and 4th octets (`192.168.x.x`) if published publicly. |
| **Physical MAC Addresses** | **Medium** | `54:47:E8:A6:B2:D3`, `B8:F7:75:AB:8C:2C`, etc. | PM5 report, Zenmap log | Physical hardware identifiers. Reveals exact gateway manufacturer (Syrotech) and host NIC (Intel/Realtek). | Redact last 3 octets (`54:47:E8:XX:XX:XX`) in public portfolios. |
| **Personal Paths** | **Low** | `ritzz-07@Aizen-07 ~/Downloads/week-2/PM1` | Terminal screenshots (`*.png`) | Reveals local host machine username (`ritzz-07`) and hostname (`Aizen-07`). | Minor metadata; acceptable for academic evaluation. |
| **API Keys & Credentials** | **None** | No passwords, private keys, or API tokens detected. | Entire repository | Clear. | Maintain strict pre-commit verification. |

### 5.2 Git History Persistence Caution
> [!CAUTION]
> Git is an append-only distributed version control system. Simply modifying or deleting sensitive files in a subsequent commit does **NOT** remove them from the repository history. Anyone cloning the repository can checkout commit `98774e9` to view previous outputs. Per instructions, Git history must **not** be rewritten. The repository must remain **Private** during internship evaluation.

---

## 6. Challenges, Anomalies & Practical Observations

1. **DNSRecon Terminal Output Redirection Anomaly:**
   * *Observation:* During the execution of `dnsrecon -d networkwalks.com | tee ~/dnsrecon-output.txt`, stdout was piped to `~/dnsrecon-output.txt`. The `~` shortcut resolved to `/home/ritzz-07/` rather than the working directory. As a consequence, the committed `dnsrecon-output.txt` file had a size of 0 bytes in the initial commit.
   * *Resolution:* The output was verified directly from the terminal capture `dnsrecon.png` which shows all 8 DNS records.
2. **Zenmap Graphviz Label Collision:**
   * *Observation:* In the circular radial layout of Zenmap, nodes with adjacent angular coordinates resulted in unreadable text collisions (`.35` overlapping `.230` and `.1` overlapping `.36`).
   * *Resolution:* Identified and flagged as an incomplete visualization requiring layout adjustments.
3. **WAF Detection Operational Impact:**
   * *Observation:* WAFW00F confirmed that `networkwalks.com` is guarded by SpiderLabs ModSecurity WAF. In subsequent penetration testing phases, automated vulnerability scanners (Nikto, SQLMap) will encounter HTTP 403 Forbidden blocks unless tamper scripts and evasion techniques are utilized.
4. **MAC Randomization Prevalence:**
   * *Observation:* 6 of the 8 active devices utilized randomized MAC addresses (`5A:5A:...`, `C6:BC:...`), illustrating the widespread adoption of privacy standards on modern consumer Wi-Fi networks.

---

## 7. Evidence Inventory & Verification Checklist

| Artifact Path | Artifact Type | File Size | Verification Status | Operational Notes |
|---|---|:---:|:---:|---|
| `week2/PM1-footprinting/tool1-whois/whois.png` | Image (PNG) | 227 KB | Verified | Full WHOIS CLI capture |
| `week2/PM1-footprinting/tool1-whois/whois-output.txt` | Text Log | 6.6 KB | Verified | GoDaddy & HostGator records |
| `week2/PM1-footprinting/tool2-whatweb/whatweb.png` | Image (PNG) | 220 KB | Verified | WhatWeb CLI capture |
| `week2/PM1-footprinting/tool2-whatweb/whatweb-output.txt` | Text Log | 2.4 KB | Verified | WordPress 7.1.4, Apache, WPDM |
| `week2/PM1-footprinting/tool3-nslookup/nslookup.png` | Image (PNG) | 91 KB | Verified | nslookup CLI capture |
| `week2/PM1-footprinting/tool3-nslookup/nslookup-output.txt` | Text Log | 125 B | Verified | A record: `192.232.216.135` |
| `week2/PM1-footprinting/tool4-curl/curl.png` | Image (PNG) | 154 KB | Verified | cURL HEAD capture |
| `week2/PM1-footprinting/tool4-curl/curl-output.txt` | Text Log | 902 B | Verified | HTTP/2 200, Nginx cache, cookies |
| `week2/PM1-footprinting/tool5-waf/waf.png` | Image (PNG) | 111 KB | Verified | WAFW00F CLI capture |
| `week2/PM1-footprinting/tool5-waf/waf-output.txt` | Text Log | 941 B | Verified | ModSecurity WAF identified |
| `week2/PM1-footprinting/tool6-dnsrecon/dnsrecon.png` | Image (PNG) | 255 KB | Verified | DNSRecon capture with 8 records |
| `week2/PM1-footprinting/tool6-dnsrecon/dnsrecon-output.txt` | Text Log | 1.8 KB | **Flagged / Verified** | Verified against terminal screenshot |
| `week2/PM5-zenmap-network-scanning/reports/PM5_Task_Answers_and_Evidence_RITHISH_SP.pdf` | Document (PDF) | 684 KB | Verified | 5-page submission document |
| `week2/PM5-zenmap-network-scanning/reports/topology.pdf` | Vector (PDF) | 13 KB | **Flagged** | Radial topology with overlapping text |
| `week2/PM5-zenmap-network-scanning/images/evidence-1-ping-scan-overview.png` | Image (PNG) | 147 KB | Verified | Zenmap ping sweep host list |
| `week2/PM5-zenmap-network-scanning/images/evidence-2-scan-summary.png` | Image (PNG) | 131 KB | Verified | Scan metrics (8 hosts, 11.43s) |
| `week2/PM5-zenmap-network-scanning/images/evidence-3-localhost-selection.png` | Image (PNG) | 141 KB | Verified | Selected host `192.168.1.36` |
| `week2/PM5-zenmap-network-scanning/images/evidence-4-topology-layout.png` | Image (PNG) | 51 KB | Verified | Graphviz radial topology |
| `week2/PM5-zenmap-network-scanning/images/evidence-5-topology-detail.png` | Image (PNG) | 36 KB | Verified | Ring topology detail |
| `week2/PM5-zenmap-network-scanning/images/topology-diagram.png` | Image (PNG) | 199 KB | Verified | High-resolution 300 DPI render |
| `week2/PM5-zenmap-network-scanning/zenmap-ping-scan-output.txt` | Text Log | 967 B | Verified | Formatted Nmap ping scan log |
| `week2/PM5-zenmap-network-scanning/scripts/ping_sweep.sh` | Bash Script | 1.6 KB | Verified | Automated LAN discovery script |

---

## 8. Conclusion

The practical exercises executed during **Week 2** successfully completed the learning outcomes established for external reconnaissance and internal network scanning:
1. **Target Exposure:** The target domain `networkwalks.com` was comprehensively profiled, discovering registrar infrastructure (GoDaddy/HostGator), active CMS components (WordPress 7.1.4, WPDM), reverse caching tiers (Nginx/Apache), and perimeter defenses (ModSecurity WAF).
2. **Local Subnet Profiling:** Layer 2 ARP discovery on `192.168.1.0/24` accurately enumerated 8 active endpoints without transport port disruption, exposing gateway hardware (Syrotech) and client MAC randomization behaviors.
3. **Evidence Integrity:** All findings are corroborated by empirical terminal screenshots and structured logs, establishing a defensible cybersecurity portfolio.

---

**Report Authored By:** RITHISH S P  
**Evaluator:** NetworkWalks Cybersecurity Internship Academy  
**Verification Date:** 13 November 2026
