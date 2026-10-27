# Common Windows Errors & Blue Screen Troubleshooting — Acme Corp IT

## Overview
This reference guide details troubleshooting protocols for frequent Windows 11 Enterprise operating system errors encountered on Acme Corp managed laptops, including permission failures, Windows Update issues, and Blue Screen of Death (BSOD) stop codes.

## Troubleshooting Error 0x80070005 (Access Denied)

### Root Cause
Error code `0x80070005` translates directly to `ERROR_ACCESS_DENIED`. It occurs when Windows Update, Microsoft Intune, or a software installer lacks administrative write permissions to critical directories (such as `C:\Program Files` or the Windows Registry `HKLM\SOFTWARE`).

### Resolution Procedure for Error 0x80070005:
1. **Reboot and Re-authenticate**: Often, user tokens are temporarily expired. Reboot the machine and log in while connected to corporate Wi-Fi or GlobalProtect VPN.
2. **Clear the Windows Update Cache**:
   Open Command Prompt as Administrator and run:
   ```cmd
   net stop wuauserv
   net stop bits
   rename %systemroot%\SoftwareDistribution SoftwareDistribution.bak
   rename %systemroot%\System32\catroot2 catroot2.bak
   net start wuauserv
   net start bits
   ```
3. **Reset Component Permissions**:
   Open PowerShell as Administrator and run:
   ```powershell
   wuauclt /resetauthorization /detectnow
   ```
4. If installing approved corporate software, ensure you trigger installation via **Company Portal** rather than running manual setup files that require local admin rights.

## System File Corruption (SFC & DISM)
If Windows applications crash intermittently or throw `0x80004005` or `0x80240020`:
1. Open Command Prompt as Administrator.
2. Run the Deployment Image Servicing and Management repair:
   ```cmd
   DISM /Online /Cleanup-Image /RestoreHealth
   ```
3. Run the System File Checker scan:
   ```cmd
   sfc /scannow
   ```
4. Allow the scan to reach 100%. If corrupted files are found and repaired, restart your computer.

## Blue Screen of Death (BSOD) Protocols
If your laptop encounters a blue screen crash (`CRITICAL_PROCESS_DIED`, `KERNEL_DATA_INPAGE_ERROR`):
1. Note the specific Stop Code displayed on screen.
2. Disconnect external USB docking stations, external monitors, or dongles.
3. Power on the laptop while holding the power button for 10 seconds to initiate a full hardware reset.
4. If the machine fails to boot into Windows, contact IT Helpdesk at **ext. 4357** immediately for hardware diagnostics or laptop replacement.
