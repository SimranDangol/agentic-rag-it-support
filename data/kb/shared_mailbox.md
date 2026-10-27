# Shared Mailbox Access & Permissions — Acme Corp IT

## Overview
Shared mailboxes (such as `billing@acme.example`, `support@acme.example`, or `sales@acme.example`) permit designated team members to read, send, and manage centralized correspondence from a single shared address without consuming an extra user license.

## Permissions Types Explained
- **Read and Manage (Full Access)**: Allows you to open the shared mailbox, view all folders, mark emails as read/unread, and categorize messages. It does *not* grant permission to send email from the shared address.
- **Send As**: Allows you to send outgoing messages where the "From" header strictly displays the shared mailbox name (`billing@acme.example`).
- **Send on Behalf**: Allows you to send messages where the recipient sees: `username@acme.example on behalf of billing@acme.example`.

## Accessing a Shared Mailbox in Outlook

### Method 1: Automatic Mapping (Default)
When IT assigns you Full Access permissions in Active Directory, Microsoft 365 automatically maps the mailbox into your Outlook left sidebar beneath your primary folders within 60 minutes. Restart Outlook to accelerate discovery.

### Method 2: Manually Adding Shared Mailbox (If Not Auto-Mapped)
If the shared mailbox does not appear automatically after 1 hour:
1. Open Outlook and click **File** -> **Account Settings** -> **Account Settings**.
2. Select your account and click **Change**.
3. Click **More Settings** -> switch to the **Advanced** tab.
4. Under the **Mailboxes** section, click **Add**.
5. Type the alias or email address of the shared mailbox (e.g., `support@acme.example`) and click **OK**.
6. Click **Apply** -> **OK** -> **Next** -> **Finish**. Restart Outlook.

### Method 3: Accessing via Outlook on the Web (OWA)
1. Navigate to `https://outlook.office.com` and sign in.
2. Click your circular profile icon in the top-right corner.
3. Select **Open another mailbox**.
4. Enter the shared mailbox email and click **Open**. The shared mailbox opens in a new dedicated tab.

## Requesting Access or Permission Changes
To request access to an existing shared mailbox:
1. Have your team lead submit an approval ticket at `https://service.acme.example`.
2. Specify whether **Full Access**, **Send As**, or both are required.
3. Helpdesk processes approved tickets within 4 business hours. Contact **ext. 4357** for P1 escalations.
