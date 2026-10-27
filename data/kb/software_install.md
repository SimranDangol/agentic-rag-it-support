# Software Installation & Approval Policy — Acme Corp IT

## Overview
To safeguard intellectual property, protect customer data, and maintain SOC 2 Type II compliance, standard user accounts on Acme Corp laptops do not possess local administrative privileges. All software installations must proceed through authorized channels.

## Installing Pre-Approved Software via Company Portal
Acme Corp maintains a vast library of pre-packaged, pre-approved software ready for one-click installation without needing administrative rights:
1. Click the Windows Start menu.
2. Type **Company Portal** and press Enter.
3. Browse the application catalog or use the search bar (top right).
4. Popular pre-approved applications available:
   - **Productivity**: Notion, Miro, Zoom, Slack, Microsoft Power BI.
   - **Development**: Visual Studio Code, Git for Windows, Node.js LTS, Docker Desktop, PyCharm Community, Postman.
   - **Browsers**: Google Chrome Enterprise, Mozilla Firefox Enterprise.
5. Click on the desired software and click **Install**.
6. The Microsoft Intune agent will download, verify signatures, and install the package quietly in the background.

## Requesting Unlisted or Commercial Software
If your day-to-day workflow requires software not currently present in the Company Portal catalog:
1. Navigate to the IT Service Catalog at `https://service.acme.example/software-request`.
2. Complete the software request form:
   - Exact software name and vendor URL.
   - Justification and team business case.
   - Number of required licenses and cost center billing code.
3. Your direct manager will receive an automated approval notification.
4. The IT Security and Legal teams will review the vendor's EULA, SOC 2 report, and data privacy policies (typically 3–5 business days).
5. Once approved, IT Engineering packages the software into Company Portal or dispatches an engineer to install it.

## Strictly Prohibited Software
The following application classes are strictly forbidden on Acme Corp devices:
- Unauthorized peer-to-peer (P2P) file sharing utilities (e.g., BitTorrent).
- Unapproved third-party VPNs or proxy bypassers (e.g., NordVPN, ExpressVPN).
- Cryptocurrency miners and unauthorized remote access tools (e.g., TeamViewer, AnyDesk).

Questions regarding software compliance should be directed to `security@acme.example` or **ext. 4357**.
