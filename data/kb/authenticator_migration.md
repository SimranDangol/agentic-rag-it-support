# Migrating to Microsoft Authenticator — Acme Corp IT

## Overview
Acme Corp IT has decommissioned support for legacy authentication apps (including Google Authenticator, Authy, and hardware SMS tokens) in favor of **Microsoft Authenticator** with cryptographic number matching. All personnel must complete migration to prevent access disruption.

## Why Migrate?
- **Phishing-Resistant MFA**: Number matching eliminates accidental prompt fatigue and push attacks.
- **Single Sign-On Integration**: Microsoft Authenticator provides conditional access and compliance checks directly with Microsoft 365 and Acme VPN.
- **Cloud Backup**: Enables encrypted cloud backup for fast phone replacement.

## Step-by-Step Migration Guide

### Step 1: Prepare Your Workstation and New App
1. On your smartphone, install **Microsoft Authenticator** from the Apple App Store or Google Play Store.
2. On your corporate laptop, open a browser window and go to:
   `https://mysignins.microsoft.com/security-info`
3. Sign in with your corporate credentials (`username@acme.example`). Authenticate with your existing legacy authenticator app one final time.

### Step 2: Register Microsoft Authenticator
1. Click **+ Add sign-in method** at the top of the methods list.
2. Select **Authenticator app** from the dropdown menu and click **Add**.
3. Follow the wizard: open Microsoft Authenticator on your phone, tap **+** -> **Work or school account** -> **Scan QR code**.
4. Scan the QR code presented on your laptop screen.
5. Complete the 2-digit number verification test.

### Step 3: Set Default Sign-in Method
1. Still on the Security Info page, find **Default sign-in method** near the top.
2. Click **Change**.
3. Select **App based authentication - notification (Microsoft Authenticator)**.
4. Click **Confirm**.

### Step 4: Remove the Legacy App
1. Locate **Google Authenticator** or **Authy** in your methods table.
2. Click **Delete** next to it to permanently remove it from your account.
3. You may now delete the corporate account profile from the legacy app on your phone.

For migration questions or issues during verification, contact Helpdesk at **ext. 4357**.
