# VPN Connection Guide — Acme Corp IT

## Overview
Acme Corp uses **Palo Alto GlobalProtect 6.2** as its VPN client. All remote employees must connect via VPN to access internal systems, shared drives, and the intranet.

## Prerequisites
- GlobalProtect 6.2 installed on your laptop (contact helpdesk ext. 4357 if not installed)
- Valid Acme Corp credentials (username@acme.example)
- MFA set up on Microsoft Authenticator

## Connecting to VPN

1. Click the **GlobalProtect icon** in the system tray (bottom-right, looks like a globe).
2. In the portal address field, enter: `vpn.acme.example`
3. Click **Connect**.
4. Enter your Acme Corp username and password.
5. Approve the MFA push notification on your Microsoft Authenticator app.
6. Wait for the status to show **Connected**. This takes 5–15 seconds.

## VPN Keeps Disconnecting

If your VPN disconnects repeatedly (every few minutes), follow these steps:

1. **Check your internet connection** — open a browser and visit a public site. If that also fails, the issue is your network, not VPN.
2. **Switch networks** — if on public Wi-Fi, switch to a mobile hotspot or home network. Public networks often block VPN protocols.
3. **Restart GlobalProtect** — right-click the tray icon → **Disable** → wait 10 seconds → **Enable**.
4. **Check the gateway** — open GlobalProtect → click the gear icon → confirm Gateway is set to `vpn.acme.example`.
5. **Flush DNS** — open Command Prompt as Administrator and run:
   ```
   ipconfig /flushdns
   ```
6. **Reinstall the client** — if disconnections persist, uninstall GlobalProtect, restart your laptop, then reinstall from `\\acme-software\VPN\GlobalProtect-6.2.msi`.

## Reconnecting After Sleep or Hibernate

Windows sometimes drops the VPN tunnel when the laptop wakes from sleep.

1. Click the GlobalProtect tray icon.
2. If status shows **Disconnected**, click **Connect**.
3. If Connect is greyed out, click **Disable**, wait 5 seconds, then **Enable**.
4. Re-enter credentials if prompted.

## Split Tunnelling

Acme Corp uses **split tunnelling** — only traffic to internal resources (10.0.0.0/8 and acme.example domains) goes through VPN. All other traffic (YouTube, Spotify, etc.) uses your local internet connection.

## When to Contact Helpdesk

Call **ext. 4357** or email **helpdesk@acme.example** if:
- You receive an error code (see `vpn_error_codes.md`)
- VPN connects but you cannot reach internal resources
- You need GlobalProtect installed on a new device
- You are travelling internationally and VPN is blocked in your country
