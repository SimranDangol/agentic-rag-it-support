# Outlook Desktop & Mobile Client Configuration — Acme Corp IT

## Overview
Acme Corp utilizes Microsoft 365 Exchange Online for corporate email, calendars, and contacts. All corporate devices must use Microsoft Outlook for desktop (Windows 11) or Outlook Mobile (iOS / Android) secured via Microsoft Intune.

## Setting Up Outlook on Windows 11 Laptops

### Automatic Setup (Modern Authentication)
1. Click the Windows Start menu and launch **Outlook** (or run `outlook.exe`).
2. When prompted, enter your Acme Corp email address:
   `username@acme.example`
3. Click **Connect**.
4. Modern Authentication will detect your Microsoft 365 tenant automatically.
5. In the sign-in prompt, enter your corporate password.
6. Complete the number-matching challenge in your Microsoft Authenticator app.
7. Ensure the checkbox **Allow my organization to manage my device** is checked, then click **OK**.
8. Outlook will initialize your local mailbox cache (`.ost` file). This takes 5–15 minutes depending on your mailbox volume.

## Recommended Performance Settings
- **Cached Exchange Mode**: Go to **File** -> **Account Settings** -> **Account Settings**. Double-click your account and confirm **Use Cached Exchange Mode** is enabled with the slider set to **1 year**.
- **Hardware Acceleration**: If Outlook stutters during scrolling, navigate to **File** -> **Options** -> **Advanced** -> **Display** and check **Disable hardware graphics acceleration**.

## Configuring Outlook Mobile (iOS & Android)
Personal mobile mail clients (such as native iOS Apple Mail or Samsung Email) are blocked by Conditional Access policies. You must use official Outlook Mobile:
1. Install **Microsoft Outlook** from the App Store or Google Play Store.
2. Open Outlook and tap **Add Account**.
3. Enter `username@acme.example` and tap **Add Account**.
4. You will be redirected to the Acme SSO login screen. Enter your password and approve MFA.
5. Register device management via **Microsoft Intune Company Portal** when prompted.
6. Set a mandatory 6-digit PIN for the application.

## Getting Support
If Outlook displays "Disconnected" in the bottom status bar or fails to pass autodiscover, contact IT Helpdesk at **ext. 4357** or email **helpdesk@acme.example**.
