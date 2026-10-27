# BitLocker Drive Encryption & Recovery Key Guide — Acme Corp IT

## Overview
All corporate Windows 11 laptops issued by Acme Corp are fully encrypted with **Microsoft BitLocker** (AES-256 bit encryption) to protect enterprise data in the event of hardware loss or theft.

## Why is BitLocker Prompting for a Recovery Key?
On rare occasions, your laptop will halt at a blue BitLocker recovery screen requesting a 48-digit numerical recovery key upon boot. Common triggers include:
- A recent BIOS/UEFI firmware update.
- Tampering with TPM (Trusted Platform Module) security chips.
- Changing hardware components (replacing motherboard, RAM, or hard drive).
- Connecting untrusted external docking stations or bootable USB devices.
- Multiple failed Windows startup attempts.

## How to Retrieve Your 48-Digit Recovery Key

### Method 1: Self-Service via Microsoft 365 Account (Fastest)
You can retrieve your key independently using any secondary device (smartphone or tablet):
1. On your phone, open a browser and navigate to:
   `https://myaccount.microsoft.com/device-list`
2. Sign in with your corporate credentials (`username@acme.example`) and complete MFA.
3. Locate your corporate laptop in the device list.
4. Click **View BitLocker Keys**.
5. Find the Key ID matching the beginning characters shown on your laptop screen.
6. Copy the **48-digit Recovery Key** (formatted as eight 6-digit blocks).
7. Type the 48 digits on your laptop using the number keys and press Enter. Windows will boot normally.

### Method 2: Contacting IT Helpdesk
If you cannot access another device to view your recovery key:
1. Call the emergency IT Helpdesk line at **ext. 4357** (or **+1-800-555-4357**).
2. The technician will verify your identity via badge number and employee security questions.
3. Read the first 8 characters of the **Recovery Key ID** displayed on your blue screen.
4. The technician will retrieve the 48-digit key from Microsoft Intune / Entra ID and read it to you.

## CRITICAL CAUTION
**Never attempt to format, reinstall, or wipe the encrypted drive** when prompted by BitLocker. Doing so destroys all local files permanently. Always contact IT Helpdesk first.
