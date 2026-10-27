# Laptop Performance Optimization Guide — Acme Corp IT

## Overview
If your corporate Dell Latitude or Lenovo ThinkPad laptop is running slowly, experiencing application freezing, or exhibiting high fan noise, follow this diagnostic checklist before requesting hardware replacement.

## Step 1: Diagnose Resource Consumption (Task Manager)
1. Press `Ctrl + Shift + Esc` to open **Task Manager**.
2. Click **More details** if in compact view.
3. On the **Processes** tab, click the **CPU** and **Memory** headers to sort processes by highest utilization.
4. Identify runaway processes:
   - If Google Chrome or Microsoft Edge consumes excessive memory, close unused tabs or restart the browser.
   - If `MsMpEng.exe` (Microsoft Defender) is utilizing high CPU, an automated antivirus background scan is in progress; allow 15 minutes for completion.
   - If a background application is frozen, right-click it and select **End task**.

## Step 2: Manage Startup Programs
Too many background programs launching during system boot significantly degrades performance:
1. In Task Manager, switch to the **Startup apps** tab.
2. Review the list of enabled programs.
3. Right-click non-essential applications (e.g., Spotify, personal chat apps, secondary cloud utilities) and click **Disable**.
4. *Do not disable* security components: GlobalProtect, CrowdStrike Falcon, Microsoft Intune Agent, or audio drivers.

## Step 3: Run Windows Disk Cleanup
1. Press `Win + R`, type `cleanmgr.exe`, and press Enter.
2. Select drive `C:` and click **OK**.
3. Click **Clean up system files**.
4. Check **Temporary files**, **Recycle Bin**, and **Thumbnails**.
5. Click **OK** to purge accumulated cached files. Aim to maintain at least **20 GB of free space** on drive `C:`.

## Step 4: Check for Thermal Throttling
Modern laptops automatically drop processor clock speeds when vents are obstructed:
- Ensure laptop intake vents on the bottom and sides are unobstructed.
- Never use laptops resting directly on beds, blankets, or soft cushions.
- Use a laptop cooling stand or elevated docking surface.

## Step 5: System Reboot Frequency
Corporate Windows laptops should be restarted at least **once every 7 days** to flush memory leaks and apply mandatory security patches.

If performance remains degraded after these steps, contact Helpdesk at **ext. 4357** to initiate an automated remote hardware diagnostic.
