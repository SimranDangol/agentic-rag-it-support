# Account Lockout Resolution Guide — Acme Corp IT

## Overview
To defend against unauthorized brute-force attacks, Acme Corp enforces an automated account lockout policy across Active Directory, Microsoft Entra ID, and Okta SSO.

## Account Lockout Policy Rules
- **Lockout Threshold**: 5 consecutive incorrect password attempts within a 15-minute window.
- **Lockout Duration**: Accounts automatically unlock after **30 minutes** of zero authentication attempts.
- **Scope**: A lockout prevents access to Windows login, GlobalProtect VPN, Microsoft 365 (Outlook, Teams), and corporate web applications.

## Immediate Resolution Steps

### Step 1: Wait for Automatic Unlock
If your lockout was caused by a mistyped password, wait 30 minutes without typing any credentials. If an attempt is made during the lockout window, the 30-minute timer resets.

### Step 2: Clear Stored Stale Credentials
The most frequent cause of repeated account lockouts is an old, cached password stored in Windows Credential Manager or a smartphone syncing corporate email:
1. Click the Windows Start menu, type **Credential Manager**, and press Enter.
2. Select **Windows Credentials**.
3. Under **Generic Credentials**, look for entries starting with:
   - `MicrosoftOffice16_Data`
   - `git:https://github.acme.example`
   - `GlobalProtect`
   - `SSO:acme.example`
4. Expand each item and click **Remove**.
5. Check your mobile device (iPhone/Android mail apps). If your phone tries to fetch emails using an outdated password, it will repeatedly trigger lockouts. Update the password in your mobile mail client.

### Step 3: Self-Service Account Unlock via SSPR
1. On your smartphone or a functioning workstation, visit:
   `https://sspr.acme.example`
2. Enter `username@acme.example`.
3. Complete MFA authentication via Microsoft Authenticator.
4. Select the option: **Unlock my account without changing password**.

## When to Contact IT Helpdesk
If your account remains locked out or repeatedly locks every few minutes:
1. Call **ext. 4357** (or **+1-800-555-4357** from an external line).
2. The technician will verify your identity via employee badge ID or manager confirmation.
3. The technician will identify the lockout source IP/workstation using Active Directory event logs (Event ID 4740) and terminate the offending background process.
