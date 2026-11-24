#!/usr/bin/env python3
"""
Sanitizes and redacts sensitive PII (National IDs, patient personal details,
cleartext passwords, phone numbers, emails) in screenshots copied for the
M4 penetration testing report. Original evidence files are preserved untouched.
"""

import os
import shutil
from PIL import Image, ImageDraw

SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEST_DIR = os.path.join(SRC_DIR, "M4_Report", "images")
os.makedirs(DEST_DIR, exist_ok=True)

def sanitize_m1_images():
    # M1-01: Login bypass
    src = os.path.join(SRC_DIR, "M1", "login bypass.png")
    dst = os.path.join(DEST_DIR, "M1-01_login_bypass.png")
    shutil.copy2(src, dst)
    print(f"Copied {src} -> {dst}")

    # M1-02: Proof of bypass (portal)
    src = os.path.join(SRC_DIR, "M1", "proof of bypass.png")
    dst = os.path.join(DEST_DIR, "M1-02_proof_of_bypass.png")
    shutil.copy2(src, dst)
    print(f"Copied {src} -> {dst}")

def sanitize_password_cracking():
    src = os.path.join(SRC_DIR, "Screenshots", "password cracking.png")
    dst = os.path.join(DEST_DIR, "M2-02_password_cracking.png")
    im = Image.open(src)
    draw = ImageDraw.Draw(im)
    
    # Redact first cracked list: y in [235, 305], x in [5, 125]
    draw.rectangle([5, 235, 125, 305], fill=(30, 30, 46), outline=(235, 111, 146))
    draw.text((12, 260), "[REDACTED - PASSWORDS]", fill=(235, 111, 146))
    
    # Redact second show list: y in [365, 448], x in [10, 135]
    draw.rectangle([10, 365, 135, 448], fill=(30, 30, 46), outline=(235, 111, 146))
    draw.text((18, 400), "[REDACTED]", fill=(235, 111, 146))
    
    im.save(dst)
    print(f"Sanitized {src} -> {dst}")

def sanitize_patient_reports():
    # Patient 1
    src1 = os.path.join(SRC_DIR, "Screenshots", "patient1.png")
    dst1 = os.path.join(DEST_DIR, "M2-03_patient1.png")
    im1 = Image.open(src1)
    draw1 = ImageDraw.Draw(im1)
    # Redact name, patient ID, DOB
    draw1.rectangle([830, 350, 1030, 422], fill=(230, 235, 245), outline=(180, 50, 50), width=2)
    draw1.text((840, 375), "[REDACTED PATIENT PII]", fill=(180, 50, 50))
    im1.save(dst1)
    print(f"Sanitized {src1} -> {dst1}")

    # Patient 2 (125% zoom)
    src2 = os.path.join(SRC_DIR, "Screenshots", "patient2.png")
    dst2 = os.path.join(DEST_DIR, "M2-04_patient2.png")
    im2 = Image.open(src2)
    draw2 = ImageDraw.Draw(im2)
    # Redact name, patient ID, DOB
    draw2.rectangle([775, 390, 1030, 475], fill=(230, 235, 245), outline=(180, 50, 50), width=2)
    draw2.text((790, 420), "[REDACTED PATIENT PII]", fill=(180, 50, 50))
    im2.save(dst2)
    print(f"Sanitized {src2} -> {dst2}")

    # Patient 3
    src3 = os.path.join(SRC_DIR, "Screenshots", "patient3.png")
    dst3 = os.path.join(DEST_DIR, "M2-05_patient3.png")
    im3 = Image.open(src3)
    draw3 = ImageDraw.Draw(im3)
    # Redact name, patient ID, DOB
    draw3.rectangle([830, 350, 1030, 422], fill=(230, 235, 245), outline=(180, 50, 50), width=2)
    draw3.text((840, 375), "[REDACTED PATIENT PII]", fill=(180, 50, 50))
    im3.save(dst3)
    print(f"Sanitized {src3} -> {dst3}")

def sanitize_exposed_db():
    src = os.path.join(SRC_DIR, "Screenshots", "exposed db.png")
    dst = os.path.join(DEST_DIR, "M3-01_exposed_db.png")
    im = Image.open(src)
    draw = ImageDraw.Draw(im)
    # In exposed db, values are email, phone, national_id
    # From y=625 down to 995, x in [410, 1150]
    draw.rectangle([410, 625, 1150, 995], fill=(245, 245, 245), outline=(200, 30, 30), width=2)
    for y_pos in range(640, 985, 35):
        draw.text((450, y_pos), "--- [CONFIDENTIAL PII: EMAIL / PHONE / NATIONAL ID REDACTED] ---", fill=(180, 30, 30))
    im.save(dst)
    print(f"Sanitized {src} -> {dst}")

if __name__ == "__main__":
    sanitize_m1_images()
    sanitize_password_cracking()
    sanitize_patient_reports()
    sanitize_exposed_db()
    print("All image sanitizations completed successfully.")
