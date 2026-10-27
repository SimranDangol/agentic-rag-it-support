# Self-Service Password Reset (SSPR) Guide — Acme Corp IT

## Overview
All Acme Corp employees are required to manage their corporate Active Directory and Microsoft 365 passwords using the official Self-Service Password Reset (SSPR) portal. The IT Helpdesk does not accept password reset requests over plaintext chat or unverified phone calls.

## Password Requirements & Policy
To comply with Acme Corp security policy:
- Minimum length: **14 characters**.
- Must contain at least three of the following four categories:
  - Uppercase letters (A–Z)
  - Lowercase letters (a–z)
  - Numbers (0–9)
  - Special characters (!, @, #, $, %, etc.)
- Cannot contain your first name, last name, or username.
- Passwords expire every **90 days**.
- Cannot reuse any of your previous **10 passwords**.

## How to Reset a Forgotten Password

### Scenario A: Remote User or Forgotten Windows Login Password
If you are locked out of your Windows laptop or forgot your password:
1. From any secondary device (such as your smartphone or personal tablet), open a web browser and navigate to:
   `https://passwordreset.microsoftonline.com` or `https://sspr.acme.example`.
2. Enter your full corporate email address (`username@acme.example`) and complete the CAPTCHA.
3. Choose your verification method:
   - **Microsoft Authenticator Notification**: Approve the push notification on your phone.
   - **SMS / Verification Code**: Enter the 6-digit code received on your registered mobile number.
4. Enter your new password twice adhering to the 14-character policy.
5. Click **Finish**.

### Scenario B: Synchronizing New Password to Your Laptop
After resetting your password online:
1. Connect your laptop to the internet (via Wi-Fi or mobile hotspot).
2. On the Windows login screen, enter your **NEW** password.
3. If remote, connect to GlobalProtect VPN immediately upon login and press `Ctrl + Alt + Del` -> click **Lock**, then unlock with your new password to synchronize cached Windows domain credentials.

## Changing an Expiring Password
If you receive the 14-day password expiration warning while logged in:
1. Press `Ctrl + Alt + Delete` on your keyboard.
2. Select **Change a password**.
3. Enter your old password, followed by your new password twice.
4. Press Enter. All Microsoft 365 apps will prompt for re-authentication within 15 minutes.

For immediate help or emergency access, contact IT Helpdesk at **ext. 4357**.
