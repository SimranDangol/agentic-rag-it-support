# Phishing Identification & Incident Reporting — Acme Corp IT Security

## Overview
Phishing and social engineering attacks are the primary vector used by adversaries to compromise corporate networks. Every employee is Acme Corp's first line of defense. This policy defines how to identify malicious communications and report them immediately.

## Common Indicators of Phishing Emails
Always inspect emails carefully for these red flags:
- **Artificial Urgency**: Demands immediate action with threats of account suspension, unpaid invoices, or missed deliveries.
- **Mismatched Sender Address**: Display name claims to be "Acme IT Helpdesk" or "Executive Leadership", but the underlying email domain is `@gmail.com`, `@acme-support.net`, or other external domains.
- **Suspicious Attachments**: Unsolicited `.html`, `.iso`, `.zip`, `.exe`, or password-protected archives claiming to be invoices or wire instructions.
- **Deceptive Hyperlinks**: Hover your mouse cursor over hyperlinks without clicking. Verify the actual destination URL matches legitimate corporate portals (`*.acme.example`).
- **Requests for Sensitive Information**: Acme IT will never ask for your password or MFA code via email.

## How to Report a Phishing Email in Outlook

### Using the One-Click "Report Phishing" Button (Preferred)
1. In Outlook Desktop or Outlook on the Web, open or select the suspicious message.
2. In the top ribbon (or action bar), click the **Report Phishing** button (represented by a fishhook or shield icon).
3. Confirm submission in the dialog box.
4. The message will be forwarded automatically to the Security Operations Center (`soc@acme.example`), removed from your inbox, and submitted to Microsoft Defender for tenant-wide blocklisting.

## What to Do If You Accidentally Clicked a Link or Entered Credentials
If you entered your password on a suspicious site or opened an untrusted attachment:
1. **Disconnect from the Network Immediately**:
   - Disconnect Wi-Fi (`Win + A` -> toggle Wi-Fi OFF) or unplug your Ethernet cable. Do not power off the laptop.
2. **Call IT Security Emergency Hotline**:
   - Immediately call **ext. 4357** or dial **+1-800-555-4357**. Select option 1 for Security Incident.
3. The SOC team will immediately revoke your active sessions, reset your domain password, and isolate the machine for forensic inspection.
