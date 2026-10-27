# Wi-Fi Setup and Troubleshooting — Acme Corp IT

## Overview
Acme Corp provides two secure wireless networks across all global offices: **Acme-Corp-Secure** (for enterprise-managed laptops) and **Acme-Guest** (for visitors and personal mobile devices).

## Connecting to Acme-Corp-Secure (Windows 11)

### Requirements
- Managed Acme Corp laptop running Windows 11 Enterprise.
- Active Directory domain credentials (`username@acme.example`).
- Valid machine certificate issued by Acme Corp Internal Certificate Authority.

### Step-by-Step Connection Instructions
1. Click the **Network / Wi-Fi** icon on the bottom right of the Windows taskbar (`Win + A`).
2. Select the arrow next to the Wi-Fi icon to view available wireless networks.
3. Select **Acme-Corp-Secure** and ensure **Connect automatically** is checked.
4. Click **Connect**.
5. When prompted for credentials:
   - Username: Enter your corporate email (`username@acme.example`).
   - Password: Enter your current Active Directory password.
6. If prompted to accept the certificate issued by `radius.acme.example`, click **Connect**.
7. Once connected, your IP address will automatically be assigned from the corporate DHCP subnet (`10.20.x.x`).

## Troubleshooting Wi-Fi Connection Failures

### Symptom: "Can't connect to this network"
If Windows reports an inability to connect to Acme-Corp-Secure:
1. **Forget the Network**:
   - Go to **Settings** -> **Network & Internet** -> **Wi-Fi** -> **Manage known networks**.
   - Find **Acme-Corp-Secure** and click **Forget**.
   - Restart your Wi-Fi adapter using the toggle switch.
   - Re-select **Acme-Corp-Secure** and enter your credentials again.
2. **Reset Network Stack**:
   Open Command Prompt as Administrator and execute:
   ```cmd
   netsh winsock reset
   netsh int ip reset
   ipconfig /release
   ipconfig /renew
   ```
   Restart your computer when finished.
3. **Verify Machine Certificate**:
   Press `Win + R`, enter `certmgr.msc`. Under **Personal** -> **Certificates**, verify that a valid certificate from `Acme-Root-CA` exists and is not expired. If missing, connect via Ethernet cable to receive Group Policy certificate updates.

## Guest Wi-Fi Usage
For contractors and guests, connect to **Acme-Guest**. Upon connection, a captive portal opens automatically. Enter your sponsor's email to generate an SMS access PIN. Bandwidth is limited to 20 Mbps and internal intranet resources are blocked.

For assistance, contact the on-site technician or call IT Helpdesk at **ext. 4357**.
