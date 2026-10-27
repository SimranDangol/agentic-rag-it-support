# Network Printer Setup & FollowMe Badge Printing — Acme Corp IT

## Overview
Acme Corp utilizes a unified enterprise print environment powered by **PaperCut MF** and secure **FollowMe-Print** queues. You do not need to install individual physical printers for each floor or conference room; print jobs are sent to a single centralized virtual queue and released at any multi-function printer (MFP) using your employee NFC badge.

## Connecting to the FollowMe-Print Queue (Windows 11)

### Requirements
- Connected to **Acme-Corp-Secure** Wi-Fi or hardwired office Ethernet (or connected via GlobalProtect VPN).
- Windows 11 Enterprise managed workstation.

### Step-by-Step Installation
1. Press `Win + R` on your keyboard to open the Run prompt.
2. Type the following network print server path and press Enter:
   ```cmd
   \\print.acme.example\FollowMe-Print
   ```
3. A Windows Printer Installation dialog will appear and automatically download the certified HP/Ricoh Universal Print Driver.
4. Alternatively, install via Windows Settings:
   - Go to **Settings** -> **Bluetooth & devices** -> **Printers & scanners**.
   - Click **Add device**.
   - After a few seconds, click **Add manually**.
   - Select **Select a shared printer by name** and enter:
     `http://print.acme.example:631/printers/FollowMe-Print`
   - Click **Next** and finish the wizard.

## How to Release Your Print Jobs at the Printer
1. Print your document from any application (Word, PDF, browser), choosing **FollowMe-Print** as the destination printer.
2. Walk to any corporate multi-function printer located in any Acme Corp office building.
3. Hold your employee NFC badge against the contactless card reader (marked with the card wave symbol).
4. On your first scan, the touch screen will prompt for a one-time badge link: enter your Acme Corp username and password. Subsequent scans log you in instantly.
5. The screen displays your pending print queue. Select **Print All** or choose individual jobs.
6. Press the physical or touch **Logout** button when finished to protect document confidentiality.

## Printing Policy
- All print jobs default to **Black & White, Duplex (Double-Sided)** to reduce paper waste.
- Color printing requires managerial approval in high-volume departments.
- Unclaimed print jobs are automatically purged from the server after **24 hours**.

For toner replacement or printer assistance, contact IT Helpdesk at **ext. 4357**.
