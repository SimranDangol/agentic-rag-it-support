# Multi-Factor Authentication (MFA) Setup Guide — Acme Corp IT

## Overview
Multi-Factor Authentication (MFA) is strictly mandatory for all Acme Corp personnel to access cloud resources, VPN tunnels, and email. Acme Corp has standardized on **Microsoft Authenticator** with number matching enabled. SMS and voice call verification are restricted to backup methods only.

## Initial Setup Instructions

### Prerequisites
- An iOS device running iOS 15+ or Android device running Android 10+.
- A computer with internet access to view the registration portal.

### Step-by-Step Registration
1. On your computer, open an incognito browser window and visit:
   `https://aka.ms/mfasetup` or `https://mfa.acme.example`.
2. Sign in with your corporate email (`username@acme.example`) and password.
3. When prompted "More information required", click **Next**.
4. On your mobile phone, open the **Apple App Store** or **Google Play Store**, search for **Microsoft Authenticator**, and install it (published by Microsoft Corporation).
5. Open Microsoft Authenticator on your mobile phone, accept privacy notices, and tap **Add account** -> **Work or school account**.
6. Select **Scan a QR code**.
7. Return to your computer screen, click **Next** until the QR code appears, and scan it with your phone camera.
8. A 2-digit number will appear on your computer screen. Enter that exact 2-digit number into the prompt on your phone and tap **Yes**.
9. Once verified, click **Done** on your computer.

## Adding a Backup Method (Secondary Phone)
To avoid lockouts if your primary mobile phone is misplaced:
1. In the security info portal (`https://mysignins.microsoft.com/security-info`), click **+ Add sign-in method**.
2. Select **Phone** from the dropdown.
3. Enter your personal mobile or desk phone number and choose **Text me a code**.
4. Enter the 6-digit confirmation code.

## Number Matching Security Note
Whenever you sign in to Acme Corp systems, the login screen presents a unique 2-digit number. You must type this number into Microsoft Authenticator. Never approve an authentication prompt that you did not actively initiate; report unexpected prompts immediately to Security.

For MFA assistance or temporary bypass codes, call IT Helpdesk at **ext. 4357**.
