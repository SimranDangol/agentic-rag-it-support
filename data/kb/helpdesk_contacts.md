# IT Helpdesk Support Contacts & Escalation — Acme Corp IT

## Overview
The Acme Corp Information Technology Helpdesk provides global technical assistance, hardware provisioning, incident resolution, and access management for all staff worldwide. If self-service guides do not resolve your issue, follow the procedures below to contact support.

## Primary Support Channels

### 1. Telephone Support (Immediate Assistance)
- **Internal VoIP Extension**: Dial **ext. 4357** (spells HELP on standard keypads)
- **Direct Global Toll-Free**: **+1-800-555-4357**
- **International Emergency Line**: **+1-212-555-0199**
- *Operating Hours*: Phone lines are staffed 24/7/365 for Priority 1 (P1) emergencies. Standard inquiries are handled Monday through Friday, 7:00 AM – 8:00 PM EST.

### 2. Email Support
- **General Inquiries**: `helpdesk@acme.example`
- **Security Incident Reporting**: `soc@acme.example` or `security@acme.example`
- **Onboarding Logistics**: `onboarding-it@acme.example`

### 3. Walk-Up Tech Lounges (On-Site Support)
Drop in without an appointment for hardware troubleshooting, monitor adapters, or badge replacements:
- **Headquarters (New York)**: Building 4, 1st Floor, Tech Bar (Mon–Fri 8:30 AM – 5:00 PM EST).
- **San Francisco Office**: 200 Mission St, 8th Floor, Room 802 (Mon–Fri 9:00 AM – 5:00 PM PST).
- **London Office**: 100 Bishopsgate, Floor 12 (Mon–Fri 9:00 AM – 5:00 PM GMT).

## How to Submit an IT Support Ticket

For non-blocking inquiries or software and hardware requests, use the self-service ticketing portal:

1. Open your browser and navigate to `https://helpdesk.acme.example`.
2. Sign in with your corporate Acme Corp credentials via Single Sign-On (SSO).
3. Select **Submit an Incident** or **Request Service** from the main dashboard.
4. Choose the appropriate category (e.g., Network, Hardware, Account, or Email).
5. In the description, include your computer hostname (`ACME-LAP-XXXX`), operating system version, and exact error code or screenshot.
6. Select your urgency level and click **Submit**. You will receive an automated confirmation email with your incident ticket number (`INC-XXXXXXX`).

## How to Escalate an Urgent Priority 1 (P1) Incident

If an issue causes a critical business stoppage (such as whole department downtime, company-wide VPN failure, or security breach):

1. Immediately call the 24/7 emergency dispatch line at **ext. 4357** or **+1-800-555-4357**.
2. Press option **1** to flag the call as a Priority 1 Critical Incident.
3. Inform the dispatcher of the business impact and affected systems.
4. The dispatcher will open a P1 bridge and notify the on-call Site Reliability Engineering (SRE) team within 15 minutes.

## Incident Priority Levels & Target SLAs
- **P1 - Critical**: Company-wide outage, VPN down, security breach. Response: **< 15 minutes**.
- **P2 - High**: User completely blocked from working (e.g., BitLocker locked, corrupt OS). Response: **< 1 hour**.
- **P3 - Medium**: Degraded performance, single application error, printer issues. Response: **< 4 hours**.
- **P4 - Low**: General inquiry, routine hardware upgrade, future software request. Response: **< 24 hours**.
