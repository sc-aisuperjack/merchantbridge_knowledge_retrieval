---
document_id: MBFS-POL-09
title: Fraud Prevention and Account Security Policy
version: 2.8
effective_date: 2026-06-01
last_reviewed: 2026-06-01
owner: Fraud & Security Operations
applies_to: All merchant accounts and dashboard users
classification: Public — customer-facing
---

> **Synthetic document.** MerchantBridge Financial Services Ltd is a fictional company created for testing and training purposes. All names, figures, phone numbers, reference numbers and addresses are invented.

# Fraud Prevention and Account Security Policy

## 1. What MerchantBridge will never ask you to do

MerchantBridge staff — by phone, email, SMS, live chat or in person — will **never**:

- ask for your dashboard **password**;
- ask you to read out or forward a **two-factor authentication (2FA) code** or one-time passcode;
- ask for your **secret API key**;
- ask you to **change your payout bank account** by phone or email;
- ask you to **move money to a "safe account"**, or to process a refund to "test" your account;
- ask you to install **remote-access software** on your computer or phone;
- ask for a customer's full card number by email or chat.

If anyone claiming to be from MerchantBridge asks for any of these, **end the contact immediately**. Do not use contact details they give you; call us on the official number in section 3.

## 2. Securing your dashboard

- **Two-factor authentication is mandatory** for every dashboard user, using an authenticator app (recommended) or SMS.
- Passwords must be at least **12 characters** and must not have appeared in known data breaches.
- Give each staff member their **own login** with the lowest role they need (Owner, Admin, Finance, Staff, Developer). Never share logins.
- Only Owners and Admins can change bank details, issue refunds above £500, or create API keys.
- Sessions time out after **30 minutes** of inactivity.

## 3. Reporting suspected fraud or a security incident

| Situation | Contact |
|---|---|
| Suspected fraud, account takeover, a suspicious call or email claiming to be from us, lost or stolen terminal | **24/7 Fraud & Emergency Line: 020 7946 0999** |
| Phishing emails (forward the email) | **security@merchantbridge.example** |
| Anything else | Main support line **020 7946 0800** (see FAQ for opening hours) |

If you have shared a password or 2FA code, or think someone else has access to your account:

1. call the 24/7 line straight away — we can **freeze payouts, refunds and bank detail changes** immediately;
2. change your password from a device you trust;
3. review recent refunds, team members, API keys and bank details.

## 4. Fraud tools for merchants

- **BridgeShield** risk scoring is included on all plans. Each online payment receives a risk score and high-risk payments are blocked automatically.
- **Custom fraud rules** (for example, block by country, velocity limits, require 3D Secure for all payments) are available on **Scale**.
- **3D Secure** is applied to online payments as described in MBFS-POL-07.

## 5. Card testing attacks

Card testing is when fraudsters use your checkout to check whether stolen card numbers work, usually with many small payments. Warning signs include a sudden spike in small or failed payments. If you see this:

- call the 24/7 line — we can temporarily require 3D Secure on all payments or pause your payment links;
- add CAPTCHA to your checkout and enable velocity rules (Scale);
- refund or void any successful test payments only after speaking to us.

## 6. Terminal security

- Check terminals daily for signs of **tampering** (extra devices attached, loose casings, unusual stickers).
- Never let anyone you do not know "service" or swap a terminal. MerchantBridge does not send engineers unannounced — all replacements are sent by courier after you contact us.

## 7. PCI DSS compliance

- All merchants that accept cards must comply with the **Payment Card Industry Data Security Standard (PCI DSS)**.
- You must complete the relevant **Self-Assessment Questionnaire (SAQ)** in the dashboard within **90 days** of your account being activated, and **every 12 months** after that.
- If you have not validated your compliance by the deadline, a **PCI non-compliance fee of £35 per month** is charged until you do (VAT-exempt).
- Never store, write down, photograph or email full card numbers or security codes (CVV/CVC).

## 8. Liability for fraud

You are responsible for losses from fraudulent transactions where liability has not shifted to the card issuer (see MBFS-POL-04, section 7), and for losses caused by sharing your credentials or failing to follow this policy. MerchantBridge is responsible for losses caused by our own errors or failures of our systems.

## 9. Related documents

- MBFS-POL-04 Chargebacks and Disputes Policy
- MBFS-POL-07 Online Payments and API Policy
- MBFS-POL-11 Rolling Reserves and Risk Holds Policy
- FAQ: Disputes, Security and Your Account (faq-disputes-security-and-account.html)
