# Outlook Calendar Synchronization Troubleshooting — Acme Corp IT

## Overview
This troubleshooting guide addresses synchronization discrepancies between your Microsoft 365 Outlook desktop client, Outlook Web Access (OWA), and mobile devices (iOS / Android).

## Common Synchronization Symptoms
- Meeting invitations accepted on your mobile device do not appear on your desktop Outlook calendar.
- Updates or cancellations to recurring meetings are missing.
- Calendar displays the status message "This folder was last updated at [outdated date/time]" or "Update Failed".

## Troubleshooting Desktop Outlook Calendar

### Step 1: Force Full Folder Update
1. Open Outlook and navigate to the **Calendar** view (`Ctrl + 2`).
2. Switch to the **Send / Receive** tab on the ribbon.
3. Click **Update Folder** to force immediate synchronization with Exchange Online.
4. Click **Send/Receive All Folders** (`F9`).

### Step 2: Clear Offline Calendar Cache
If specific meetings are corrupted or desynchronized:
1. Right-click the **Calendar** under your account in the left pane -> click **Properties**.
2. In the General tab, click **Clear Offline Items**.
3. Click **OK**. Your calendar pane will temporarily appear empty.
4. Press `F9` or click **Update Folder**. Outlook will download a fresh copy of all calendar events directly from Exchange Online.

### Step 3: Turn Off Shared Calendar Improvements
If synchronization issues involve a colleague's or executive's shared calendar:
1. Go to **File** -> **Account Settings** -> **Account Settings**.
2. Select your email and click **Change** -> **More Settings**.
3. Click the **Advanced** tab.
4. Under Microsoft 365 Features, uncheck **Turn on shared calendar improvements**.
5. Click **OK**, restart Outlook, and re-test.

## Troubleshooting Mobile Device Calendar Sync
1. Open the **Outlook Mobile** app on your smartphone.
2. Tap your profile icon (top left) -> tap the **Settings** gear icon (bottom left).
3. Under Mail Accounts, tap your Acme Corp account (`username@acme.example`).
4. Tap **Reset Account**. The app will purge its local cache and re-sync your calendar and contacts.
5. If the issue persists, ensure background data and calendar permissions are enabled in your phone's operating system settings.

For unresolved calendar synchronization errors, call IT Helpdesk at **ext. 4357**.
