import sys
import os
from datetime import datetime, timedelta
from pypdf import PdfReader, PdfWriter

def printBar(tried, maxEstimate=100000):
    barLen = 40
    progress = tried / maxEstimate
    filled = int(barLen * progress)
    bar = "█" * filled + "░" * (barLen - filled)
    percent = min(100, progress * 100)
    print(f"\r  Progress: |{bar}| {percent:5.1f}%  ({tried:,} tried)", end="", flush=True)

if len(sys.argv) != 2:
    print("Usage: python crack.py \"your_file.pdf\"")
    sys.exit(1)

filePath = sys.argv[1]
base, ext = os.path.splitext(filePath)
outPath = base + "_unlocked" + ext

print("\nPDF Date Password Cracker")
print(f"File: {os.path.basename(filePath)}\n")

print("Enter date format (examples):")
print("  ddmmyyyy  → 12112004")
print("  yyyymmdd  → 20041112")
print("  ddmmyy    → 121104")
print("  mmddyyyy  → 11122004")
print("  mmddyy    → 111204")
formatInput = input("\nYour format: ").strip().lower()

if formatInput not in ["ddmmyyyy", "yyyymmdd", "ddmmyy", "mmddyyyy", "mmddyy"]:
    print("\nInvalid format! Use one of the examples above.")
    sys.exit(1)

print(f"\nUsing format: {formatInput}")
print("Starting from today backwards...\n")

reader = PdfReader(filePath)
if not reader.is_encrypted:
    print("This file is not password protected.")
    sys.exit(0)

def dateFormat(d, m, y, fmt):
    dd = f"{d:02d}"
    mm = f"{m:02d}"
    yy = f"{y % 100:02d}"
    yyyy = f"{y:04d}"
    if fmt == "ddmmyyyy": return dd + mm + yyyy
    if fmt == "yyyymmdd": return yyyy + mm + dd
    if fmt == "ddmmyy":   return dd + mm + yy
    if fmt == "mmddyyyy": return mm + dd + yyyy
    if fmt == "mmddyy":   return mm + dd + yy
    return ""

currentDate = datetime.now()
tried = 0
found = False
printBar(0)

while not found and currentDate.year >= 1900:
    d = currentDate.day
    m = currentDate.month
    y = currentDate.year
    password = dateFormat(d, m, y, formatInput)

    tried += 1
    if tried % 50 == 0:
        printBar(tried)

    if reader.decrypt(password):
        printBar(tried)
        print(f"\n\nSUCCESS! Password: {password}")
        writer = PdfWriter(clone_from=reader)
        with open(outPath, "wb") as f:
            writer.write(f)
        print(f"Decrypted file saved as:\n{os.path.basename(outPath)}")
        found = True
        break
    currentDate -= timedelta(days=1)

if not found:
    printBar(tried)
    print("\n\nNo password found (tried down to year 1900).")
print("\nDone.\n")
