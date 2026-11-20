# Password Cracking, Hash Extraction & Cryptanalysis

### *Practical Cryptanalysis Suite: Offline Recovery with John the Ripper & Online Hash Analysis*
**Networkwalks Cybersecurity Internship — Week 3 Project Module**

[![John the Ripper](https://img.shields.io/badge/JTR-John_the_Ripper-red?logo=kalilinux&logoColor=white)](https://www.openwall.com/john/)
[![Kali Linux](https://img.shields.io/badge/Kali-Linux-557C94?logo=kalilinux&logoColor=white)](https://www.kali.org/)
[![Wordlist](https://img.shields.io/badge/Wordlist-RockYou.txt-orange)](https://github.com/praetorian-inc/Hob0Rules)
[![Cryptanalysis](https://img.shields.io/badge/Attack-Dictionary_%26_Hash_Extraction-darkblue)](#1-executive-summary)
[![Status](https://img.shields.io/badge/Flags-Captured_2%2F2-brightgreen)](#3-captured-flags-summary)
[![Author](https://img.shields.io/badge/Author-Rithish_S_P-black?logo=github)](https://github.com/Ritzz-09)

---

## Visual Overview

<p align="center">
  <img src="PM1-%20password%20cracking%20with%20JTR/password%20cracked%20with%20JTR.png" width="48%" alt="JTR Terminal Execution" />
  <img src="PM1-%20password%20cracking%20with%20JTR/cracked%20pdf.png" width="48%" alt="Cracked PDF 1 Flag" />
</p>
<p align="center">
  <em>Figure 1: Left: John the Ripper performing dictionary attack on PDF hash using RockYou. Right: Unlocked PDF revealing Flag 1.</em>
</p>

<p align="center">
  <img src="PM2-%20password%20cracking%20with%20nw%20tools/password-cracker.png" width="48%" alt="Networkwalks Password Cracker" />
  <img src="PM2-%20password%20cracking%20with%20nw%20tools/opened%20pdf.png" width="48%" alt="Cracked PDF 2 Flag" />
</p>
<p align="center">
  <em>Figure 2: Left: Networkwalks web-based dictionary attack cracking PDF hash. Right: Unlocked PDF revealing Flag 2.</em>
</p>

---

## 1. Executive Summary

During **Week 3** of the **Networkwalks Cybersecurity Internship**, practical cryptanalysis, cryptographic hash extraction, and dictionary-based password recovery were conducted across two practical modules:

1. **PM1 — Password Cracking with John the Ripper (JTR)**:
   - Target: Encrypted PDF document (`My Locked PDF1.pdf`) protected with 128-bit key length (Revision 4).
   - Tooling: Extracted hash formatted for `pdf2john`, cracked via **John the Ripper** on Kali Linux using the **RockYou** wordlist (`/usr/share/wordlists/rockyou.txt`).
   - Outcome: Password recovered in ~7 seconds (`good-luck`). Document successfully unlocked to extract **Flag 1**.

2. **PM2 — Password Cracking with Networkwalks Web Tools**:
   - Target: Encrypted PDF document (`My Locked PDF1 (for NW Tools Lab WK3-PM2).pdf`).
   - Tooling: Utilized the **Networkwalks Hash Calculator** to extract the cryptographic `$pdf$` hash in-browser, followed by the **Networkwalks Password Cracker** web suite to run a targeted dictionary attack.
   - Outcome: Password recovered (`password1`). Document unlocked to extract **Flag 2**.

---

## 2. Assessment Targets & Environmental Context

| Parameter | Practical Module 1 (PM1) | Practical Module 2 (PM2) |
|---|---|---|
| **Target File** | `My Locked PDF1.pdf` | `My Locked PDF1 (for NW Tools Lab WK3-PM2).pdf` |
| **Encryption Standard** | PDF Revision 4, 128-bit Key (MD5-RC4 / SHA2-AES) | PDF Revision 4, 128-bit Key (V4 / R4) |
| **Operating Platform** | Kali Linux 2026.2 (Security Workstation) | Web Browser / Networkwalks Academy Platform |
| **Extraction Utility** | `pdf2john.py` / CLI extraction | Networkwalks Hash Calculator (`/hash-calculator/`) |
| **Cracking Engine** | John the Ripper (v1.9.0-jumbo-1) | Networkwalks Web Cracker (`/password-cracker/`) |
| **Dictionary Source** | `/usr/share/wordlists/rockyou.txt` | Built-in top-common dictionary list |
| **Cracked Password** | `good-luck` | `password1` |
| **Flag Status** | Captured (`nw{cybersecurity_flag_captured_2608}`) | Captured (`nw{networkwalks_flag1_jtr_270521_1}`) |

---

## 3. Captured Flags Summary

| Module | Recovered Password | Captured Flag | Status |
|:---:|:---:|:---:|:---:|
| **PM1** | `good-luck` | `nw{cybersecurity_flag_captured_2608}` | ✅ Verified |
| **PM2** | `password1` | `nw{networkwalks_flag1_jtr_270521_1}` | ✅ Verified |

---

## 4. Module PM1 — Password Cracking with John the Ripper (JTR)

### 4.1 Cryptographic Hash Extraction & Inspection
The encrypted PDF was processed to extract the hash signature into `hash1.txt`:

```text
$pdf$4*4*128*-1028*1*16*ca7f72f11459cba469f1005a8765ed51*32*f32d8fa1bfbe2648226dffc39f7909ea0021446990b9e4114071a4d9104984c1*32*9322f50c29569712067a775264635e4954ccb1b99e209d664984054ffad30a6a
```

* **Format Breakdown:**
  * `$pdf$`: JTR identifier for PDF encryption hash structure.
  * `4*4*128`: PDF Revision 4, Version 4, 128-bit key length.
  * `-1028`: Permissions flag.
  * Hex strings: Initialization vector, document ID, owner/user password hashes.

### 4.2 Executing Dictionary Attack with RockYou
John the Ripper was invoked targeting the extracted hash using Kali Linux's standard wordlist:

```bash
john --wordlist=/usr/share/wordlists/rockyou.txt hash1.txt
```

**Execution Output:**
```text
Using default input encoding: UTF-8
Loaded 1 password hash (PDF, PDF encrypted document [MD5-RC4 / SHA2-AES 32/64])
Cost 1 (revision) is 4 for all loaded hashes
Cost 2 (key length) is 128 for all loaded hashes
Will run 2 OpenMP threads
good-luck        (?)
1g 0:00:00:07 DONE (2026-11-20 14:56) 0.1389g/s 130631p/s 130631c/s 130631C/s good8888..gonzo72
Use the "--show --format=PDF" options to display all of the cracked passwords reliably
Session completed
```

### 4.3 Verifying Cracked Credentials
```bash
john --show hash1.txt
# Output:
# ?:good-luck
# 1 password hash cracked, 0 left
```

Entering `good-luck` into `My Locked PDF1.pdf` decrypted the document, presenting:
> **Flag 1:** `nw{cybersecurity_flag_captured_2608}`

---

## 5. Module PM2 — Password Cracking with Networkwalks Web Tools

### 5.1 Online Hash Extraction
Using the **Networkwalks Hash Calculator** (`https://networkwalks.com/hash-calculator/`):
1. `My Locked PDF1 (for NW Tools Lab WK3-PM2).pdf` (65.2 KB) was parsed locally in the browser.
2. The cryptographic hash was extracted:
   ```text
   $pdf$4*4*128*-1060*1*16*55d1a5c14175da449753199e44971d32*32*777fd021a7f3c5ae598c0c6495c7f76e00000000000000000000000000000000*32*ceecdac74b19b5a62688d3b3524e1374c955cbb9cc3c45316494d9446ef81af1
   ```

### 5.2 Web-Based Dictionary Attack
Using the **Networkwalks Password Cracker** (`https://networkwalks.com/password-cracker/`):
1. The extracted `$pdf$` hash was supplied to the web tool.
2. The dictionary attack evaluated candidate passwords at ~9 pw/s.
3. At 91% completion, the engine matched:
   ```text
   [+] MATCH password1 ✓
   PASSWORD CRACKED SUCCESSFULLY: password1
   ```

Entering `password1` into `My Locked PDF1 (for NW Tools Lab WK3-PM2).pdf` decrypted the document, presenting:
> **Flag 2:** `nw{networkwalks_flag1_jtr_270521_1}`

---

## 6. Security Analysis & Remediation Recommendations

1. **Weak / Dictionary-Exposed Passwords:**
   Both `good-luck` and `password1` are prevalent in standard wordlists (`rockyou.txt` and top 1,000 common passwords), enabling recovery in under 10 seconds.
2. **Defensive Password Complexity Policy:**
   Organizations must enforce passphrases containing at least 14-16 alphanumeric and special characters with high Shannon entropy, making dictionary and hybrid brute-force attacks computationally infeasible.
3. **Upgrade PDF Encryption Standards:**
   PDF Revision 4 (128-bit RC4/AES) is vulnerable to high-speed hardware-accelerated cracking (e.g., Hashcat with GPU clusters). Documents should enforce PDF 2.0 (ISO 32000-2) standard utilizing **256-bit AES** with PBKDF2/SHA-256 key derivation.
