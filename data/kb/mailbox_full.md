# Mailbox Full Quota Management Guide — Acme Corp IT

## Overview
Acme Corp provisions a standard **50 GB mailbox quota** for all employees on Microsoft 365 Exchange Online. When your mailbox approaches or reaches this threshold, email delivery is restricted.

## Warning Signs and Storage Thresholds
- **45 GB (90% Warning)**: You receive an automated warning email from `postmaster@acme.example` notifying you that storage is nearing capacity.
- **49 GB (Prohibit Send)**: Outlook prevents sending new emails. Outgoing messages remain stuck in Outbox.
- **50 GB (Prohibit Send & Receive)**: All incoming emails bounce back to the sender with Non-Delivery Report (NDR) error code `554 5.2.2 mailbox full`.

## How to Check Your Current Mailbox Size
1. Open Outlook on Windows.
2. Click **File** in the top-left corner.
3. Under **Account Information**, inspect the progress bar labeled **Mailbox Cleanup**. It displays used space versus your 50 GB limit.

## Immediate Steps to Free Up Mailbox Space

### Step 1: Empty Deleted Items & Junk Folders
1. Right-click the **Deleted Items** folder in Outlook -> click **Empty Folder**.
2. Click **Recover Deleted Items from Server** at the top of the folder. Select old, unwanted items and choose **Purge Selected Items**.
3. Right-click the **Junk Email** folder -> click **Empty Folder**.

### Step 2: Use the Mailbox Cleanup Tool
1. Click **File** -> **Tools** -> **Mailbox Cleanup**.
2. Select **Find items older than** and enter **180 days**.
3. Click **Find** to review and delete outdated messages.
4. Select **Find items larger than** and enter **10000 KB** (10 MB). Remove emails with bulky video, CAD, or slide deck attachments. Save attachments locally or to OneDrive first.

### Step 3: Request an Online In-Place Archive Mailbox
If your business role requires retaining large volumes of emails beyond 50 GB:
1. Submit an IT request via `https://service.acme.example` for **Exchange Online Archiving (EOA)**.
2. Once provisioned by Helpdesk, an **Online Archive - [Your Name]** mailbox folder will appear in Outlook with an additional 100 GB of auto-expanding storage.
3. Emails older than 2 years will automatically move into your archive folder nightly.

For urgent quota increases during critical deliverables, call IT Helpdesk at **ext. 4357**.
