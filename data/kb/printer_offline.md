# Resolving Printer Offline Errors — Acme Corp IT

## Overview
This document guides users through troubleshooting "Printer Offline" errors on Windows 11 workstations when attempting to print to local departmental printers or the **FollowMe-Print** queue (`\\print.acme.example\FollowMe-Print`).

## Common Root Causes
- Windows Print Spooler service hung or stopped.
- "Use Printer Offline" toggle mistakenly enabled in Windows.
- Stale print jobs jammed in the local Windows spool queue.
- Disconnected network connection or lack of VPN connectivity when printing remotely.

## Step-by-Step Resolution Procedures

### Step 1: Verify Network & VPN Connection
Network printers require connectivity to the corporate subnet:
1. Ensure your laptop is connected to **Acme-Corp-Secure** Wi-Fi or hardwired Ethernet.
2. If working remotely from home, connect to **GlobalProtect VPN** (`vpn.acme.example`). The print queue server is not accessible over public internet.

### Step 2: Uncheck "Use Printer Offline"
1. Open Windows **Settings** -> **Bluetooth & devices** -> **Printers & scanners**.
2. Select your printer (e.g., **FollowMe-Print**).
3. Click **Open print queue**.
4. In the print queue window, click **Printer** in the top menu bar.
5. Ensure there is **NO checkmark** next to **Use Printer Offline**. If checked, click it to disable offline mode.
6. Also ensure **Pause Printing** is unchecked.

### Step 3: Restart Windows Print Spooler Service
If the printer remains unresponsive, clear and restart the Print Spooler:
1. Press `Win + X` and select **Terminal (Admin)** or **Command Prompt (Admin)**.
2. Execute the following commands in sequence:
   ```cmd
   net stop spooler
   del /Q /F /S "%systemroot%\System32\spool\PRINTERS\*.*"
   net start spooler
   ```
3. This purges any stuck, corrupted print jobs from memory and restarts the printing subsystem.

### Step 4: Re-add the Print Queue
If the offline status persists:
1. Return to **Printers & scanners**, select the problematic printer, and click **Remove**.
2. Restart your laptop.
3. Re-install the printer by pressing `Win + R` and entering:
   `\\print.acme.example\FollowMe-Print`

If the physical printer displays hardware errors (e.g., paper jam, out of toner, door open), call Facilities or the IT Helpdesk at **ext. 4357**.
