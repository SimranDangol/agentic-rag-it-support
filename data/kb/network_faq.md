# Corporate Network & Drive Mapping FAQ — Acme Corp IT

## Overview
This guide provides solutions for accessing Acme Corp internal subnets, corporate file shares, mapped drives, and internal web portals. All internal network access requires an active physical office connection or an active **Palo Alto GlobalProtect 6.2** VPN tunnel.

## Mapped Drives Not Showing After Restart

### Symptom
After booting your Windows 11 corporate laptop, mapped network drives (such as `H:` Personal Drive or `S:` Departmental Share) display a red 'X' or do not show up in File Explorer.

### Root Cause
Windows boots faster than the network adapter initializes or VPN connects, causing automatic reconnection to time out.

### Resolution Steps
1. Ensure your GlobalProtect VPN client status indicates **Connected** to `vpn.acme.example`.
2. Open File Explorer (`Win + E`) and navigate to **This PC**.
3. If drive `S:` has a red 'X', double-click it and enter your Acme Corp credentials (`username@acme.example`) if prompted.
4. If the drive is missing completely, remap it via Command Prompt:
   ```cmd
   net use S: \\fileserver.acme.example\shared /persistent:yes
   net use H: \\fileserver.acme.example\home\%USERNAME% /persistent:yes
   ```
5. If command fails with "System error 53 has occurred", verify DNS by pinging `fileserver.acme.example`.

## Cannot Reach Internal Company Website

### Symptom
Browsing to internal applications (such as `https://intranet.acme.example` or `https://jira.acme.example`) returns `DNS_PROBE_FINISHED_NXDOMAIN` or `ERR_CONNECTION_TIMED_OUT`.

### Step-by-Step Fix
1. **Verify VPN Status**: Ensure GlobalProtect 6.2 is connected. Split tunneling directs `*.acme.example` and `10.0.0.0/8` subnets over the secure tunnel.
2. **Flush Local DNS**:
   ```cmd
   ipconfig /flushdns
   ```
3. **Check Routing Table**:
   Run `route print 10.*` in Command Prompt. You should see a route pointing to the Palo Alto virtual interface gateway.
4. **Disable Conflicting Proxies**:
   Open Windows Settings -> **Network & Internet** -> **Proxy**. Ensure **Automatically detect settings** is ON and manual proxy server is OFF unless advised by Network Engineering.
5. **Clear Browser Socket Pool**:
   In Google Chrome or Microsoft Edge, navigate to `edge://net-internals/#sockets` or `chrome://net-internals/#sockets` and click **Flush socket pools**.

## Support Escalation
If internal services remain unreachable after completing these steps, submit a ticket at `https://helpdesk.acme.example` or call **ext. 4357**.
