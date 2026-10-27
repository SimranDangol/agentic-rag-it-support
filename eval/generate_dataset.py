import json
from pathlib import Path

# 24 Knowledge Base documents x 3 test questions each = 72 in-domain questions
KB_QUESTIONS = {
    "account_lockout.md": [
        "My account got locked out after multiple failed password attempts",
        "How long do I have to wait for my account to automatically unlock?",
        "How do I clear stored stale credentials in Windows Credential Manager to prevent repeated lockouts?",
    ],
    "authenticator_migration.md": [
        "How do I switch from Google Authenticator to Microsoft Authenticator?",
        "How do I migrate my two-factor authentication to the new Authenticator app?",
        "How do I remove the legacy authenticator app after registering Microsoft Authenticator?",
    ],
    "bitlocker_recovery.md": [
        "BitLocker recovery key where do I find it?",
        "My computer is stuck on the blue BitLocker recovery screen asking for a 48-digit key",
        "How do I retrieve my BitLocker recovery key from the Microsoft 365 portal?",
    ],
    "calendar_sync.md": [
        "Outlook calendar not syncing with my mobile device",
        "How do I clear the offline calendar cache in Outlook desktop?",
        "Shared calendar appointments are missing or not updating in Outlook",
    ],
    "helpdesk_contacts.md": [
        "What is the IT helpdesk phone number and extension?",
        "Where are the walk-up Tech Lounges located and what are their hours?",
        "How do I submit an urgent Priority 1 ticket to the IT helpdesk?",
    ],
    "laptop_slow.md": [
        "My laptop is running extremely slow and freezing",
        "How do I disable heavy startup programs in Windows Task Manager?",
        "Laptop fan is running loud and CPU is thermal throttling",
    ],
    "mailbox_full.md": [
        "My mailbox is full and I cannot send or receive new emails",
        "How do I use the Mailbox Cleanup tool to find large emails?",
        "How do I request an Online In-Place Archive mailbox for extra storage?",
    ],
    "mfa_lost_phone.md": [
        "I lost my phone and cannot receive MFA authentication codes",
        "How do I request an emergency Temporary Access Pass (TAP)?",
        "My smartphone with Microsoft Authenticator was stolen what is the protocol?",
    ],
    "mfa_setup.md": [
        "How do I set up MFA on my smartphone for the first time?",
        "How do I add a backup secondary phone number for MFA authentication?",
        "What is the number matching prompt in Microsoft Authenticator?",
    ],
    "network_faq.md": [
        "Mapped network drives (Z drive or S drive) disappeared after restart",
        "Cannot access internal company intranet websites or file shares",
        "How do I reconnect persistent network drives using net use?",
    ],
    "new_joiner_setup.md": [
        "How do I set up my corporate laptop on my first day as a new employee?",
        "What is the initial default password for new joiners at Acme Corp?",
        "How do I install required company software from the Acme Company Portal on day one?",
    ],
    "outlook_setup.md": [
        "How do I configure Outlook on a new Windows 11 laptop?",
        "How do I set up corporate email in Outlook Mobile on my iPhone or Android?",
        "How do I enable Cached Exchange Mode in Outlook settings?",
    ],
    "password_reset.md": [
        "How do I reset my forgotten Windows domain password?",
        "What are the Acme Corp password complexity requirements?",
        "How do I synchronize my newly reset password to my laptop while remote?",
    ],
    "phishing_report.md": [
        "I received a suspicious email that looks like phishing what should I do?",
        "How do I report a phishing email using the Outlook Report Phishing button?",
        "What should I do if I accidentally clicked a link or entered my password on a suspicious site?",
    ],
    "printer_offline.md": [
        "Network printer shows offline in Windows 11 even though the printer is powered on",
        "How do I restart the Windows Print Spooler service to clear offline status?",
        "Print jobs are stuck in queue and printer will not print",
    ],
    "printer_setup.md": [
        "How do I connect to the FollowMe-Print network printer queue?",
        "How do I release my held print job using my employee badge at the printer?",
        "What is the network path for adding Acme office printers?",
    ],
    "scan_to_email.md": [
        "How do I use the office MFP scanner to send documents to my email?",
        "Why is my scanned document not arriving in my Outlook inbox?",
        "What is the maximum attachment file size limit for scan-to-email?",
    ],
    "shared_mailbox.md": [
        "How do I access a shared team mailbox in Outlook desktop?",
        "How do I open a shared mailbox in Outlook on the web (OWA)?",
        "Difference between Send As and Send on Behalf permissions for shared mailboxes",
    ],
    "software_install.md": [
        "How do I install approved software from the Acme Company Portal?",
        "How do I request commercial or unlisted third-party software?",
        "Is personal file-sharing or torrent software allowed on company computers?",
    ],
    "sso_login.md": [
        "How do I log in to corporate apps using Single Sign-On (SSO)?",
        "How to fix SSO error 403 Forbidden - User Not Assigned to Application",
        "SSO error SAML Response Expired or clock skew troubleshooting",
    ],
    "vpn_error_codes.md": [
        "VPN Error 619: A connection to the remote computer could not be established",
        "GlobalProtect Error 514: Network connection disconnected by user or tunnel lost",
        "VPN Error 1024: Could not connect to portal vpn.acme.example",
    ],
    "vpn_guide.md": [
        "My GlobalProtect VPN keeps disconnecting every few minutes",
        "How do I reconnect the VPN client after my laptop wakes from sleep?",
        "Does Acme Corp VPN use split tunnelling for personal internet traffic?",
    ],
    "wifi_setup.md": [
        "How do I connect my laptop to the Acme-Corp-Secure office Wi-Fi?",
        "Getting error Can't connect to this network on corporate Wi-Fi",
        "How do visitors or guests connect to Acme-Guest wireless internet?",
    ],
    "windows_errors.md": [
        "How do I fix Windows Error 0x80070005 Access Denied?",
        "How to run SFC /scannow and DISM restorehealth to fix system file corruption",
        "What to do if my Windows 11 laptop encounters a Blue Screen of Death (BSOD)?",
    ],
}

# General IT queries out-of-scope for internal KB (Expected to trigger Web Search or Fallback)
OUT_OF_DOMAIN_QUESTIONS = [
    {"q": "What is the latest release version of macOS Sonoma?", "type": "it", "expected_source": None},
    {"q": "How do I permanently delete my personal Google account?", "type": "it", "expected_source": None},
    {"q": "What are the hardware system requirements for Windows 12?", "type": "it", "expected_source": None},
    {"q": "What is ChatGPT and how does generative AI work?", "type": "it", "expected_source": None},
    {"q": "How do I fix a paper jam in an HP LaserJet 4000 home printer?", "type": "it", "expected_source": None},
]

# Conversational small talk queries (Expected to route to small_talk)
SMALL_TALK_QUESTIONS = [
    {"q": "Hello, good morning!", "type": "small_talk", "expected_source": None},
    {"q": "Hi there, can you help me?", "type": "small_talk", "expected_source": None},
    {"q": "Thank you so much, that solved my problem!", "type": "small_talk", "expected_source": None},
    {"q": "Who created you?", "type": "small_talk", "expected_source": None},
    {"q": "Tell me a funny joke about IT support", "type": "small_talk", "expected_source": None},
    {"q": "What is the weather outside today?", "type": "small_talk", "expected_source": None},
    {"q": "How can I invest in the stock market?", "type": "small_talk", "expected_source": None},
    {"q": "Bye, have a great day!", "type": "small_talk", "expected_source": None},
    {"q": "You are super helpful, thanks!", "type": "small_talk", "expected_source": None},
    {"q": "asdfghjkl qwerty", "type": "small_talk", "expected_source": None},
]


def generate_dataset():
    dataset = []

    # 1. Add 72 internal IT questions (3 per doc)
    for source, questions in sorted(KB_QUESTIONS.items()):
        for q in questions:
            dataset.append({
                "q": q,
                "type": "it",
                "expected_source": source,
            })

    # 2. Add out-of-domain IT questions
    dataset.extend(OUT_OF_DOMAIN_QUESTIONS)

    # 3. Add small talk questions
    dataset.extend(SMALL_TALK_QUESTIONS)

    target_path = Path(__file__).resolve().parent / "dataset.jsonl"
    with open(target_path, "w", encoding="utf-8") as f:
        for entry in dataset:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"Generated {len(dataset)} evaluation rows in {target_path}")
    print(f"  - In-domain KB questions: {len(KB_QUESTIONS) * 3} ({len(KB_QUESTIONS)} docs x 3)")
    print(f"  - Out-of-domain / Web questions: {len(OUT_OF_DOMAIN_QUESTIONS)}")
    print(f"  - Small-talk questions: {len(SMALL_TALK_QUESTIONS)}")


if __name__ == "__main__":
    generate_dataset()
