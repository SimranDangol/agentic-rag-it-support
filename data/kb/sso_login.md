# Single Sign-On (SSO) Login Guide — Acme Corp IT

## Overview
Acme Corp uses Okta and Microsoft Entra ID for centralized Single Sign-On (SSO). A single set of corporate credentials provides access to all authorized enterprise applications, including Workday, Slack, Jira, GitHub Enterprise, and Google Workspace.

## Accessing the SSO Portal
1. Open your web browser and navigate to the Acme Corp SSO dashboard:
   `https://sso.acme.example`
2. Enter your primary Acme Corp email address:
   `username@acme.example`
3. Click **Next** and enter your Active Directory password.
4. Complete Multi-Factor Authentication (MFA) via Microsoft Authenticator push notification or number matching.
5. Once authenticated, your personalized dashboard will display your assigned enterprise applications.

## Troubleshooting Common SSO Errors

### Error: "403 Forbidden - User Not Assigned to Application"
- **Cause**: Your account does not possess the required Active Directory security group role for this specific application.
- **Resolution**:
  1. Have your team manager submit a role-assignment request via ServiceNow at `https://service.acme.example`.
  2. Approvals are processed automatically every hour; once approved, log out of SSO and log back in.

### Error: "SAML Response Expired / Clock Skew"
- **Cause**: Your laptop's local system time is out of sync with Acme Corp domain controllers by more than 3 minutes.
- **Resolution**:
  1. Open Windows Settings -> **Time & Language** -> **Date & Time**.
  2. Toggle **Set time automatically** to ON.
  3. Click the button labeled **Sync now** under Additional settings.
  4. Close your browser completely and retry accessing `https://sso.acme.example`.

### Seamless SSO in Google Chrome and Microsoft Edge
To prevent repetitive password prompts on corporate Windows 11 machines:
1. Ensure your browser profile is signed in with your `@acme.example` account.
2. In Edge, enable **Allow single sign-on for work or school sites using this profile** under Settings -> Profiles.

## Escalation
If you experience persistent authentication loops or session timeouts, clear your browser cookies for `*.acme.example` or contact IT Support at **ext. 4357**.
