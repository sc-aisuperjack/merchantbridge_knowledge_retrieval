---
document_id: MBFS-POL-07
title: Online Payments and API Policy
version: 3.0
effective_date: 2026-06-01
last_reviewed: 2026-06-01
owner: Platform & Developer Experience
applies_to: All merchants accepting card-not-present payments
classification: Public — customer-facing
---

> **Synthetic document.** MerchantBridge Financial Services Ltd is a fictional company created for testing and training purposes. All names, figures, phone numbers, reference numbers and addresses are invented.

# Online Payments and API Policy

## 1. Online products

| Product | Description | Plans |
|---|---|---|
| **Hosted Checkout** | A secure payment page hosted by MerchantBridge that you link to from your website | All |
| **Payment Links** | Shareable links for a fixed or customer-entered amount, sent by email, SMS or social media | All |
| **Invoicing** | Branded invoices with a pay-by-card button | Starter: up to 20 per month; Growth and Scale: unlimited |
| **Virtual Terminal (MOTO)** | Key in card details taken by phone or post | Growth and Scale |
| **REST API** | Full programmatic access to payments, refunds, payouts and reporting | All |
| **E-commerce plugins** | Ready-made integrations for popular e-commerce platforms | All |

All online transactions are charged at the **online / card-not-present** rates in the Fee and Rate Schedule. Virtual Terminal (MOTO) transactions carry an additional 0.50%.

## 2. Strong Customer Authentication (3D Secure)

- Online payments by UK and EEA cardholders must meet **Strong Customer Authentication** (SCA) requirements. MerchantBridge applies **3D Secure 2** automatically on Hosted Checkout, Payment Links and Invoicing.
- API integrations must support the 3D Secure challenge flow.
- Exemptions (for example, low-value transactions under £30, or merchant-initiated recurring payments after the first authenticated payment) are applied automatically where permitted. The card issuer can always require authentication.
- MOTO transactions are outside the scope of SCA and do **not** benefit from fraud liability shift.

## 3. Payment links

- Payment links **expire after 30 days** by default. You can set an expiry of between 1 and **90 days**.
- A single-use link closes after one successful payment; a multi-use link stays open until it expires or you deactivate it.

## 4. Recurring and stored-card payments

- You may store a customer's card (as a token — never the card number) only with the customer's **explicit agreement** to the terms of future charges.
- Subscription terms must clearly state the amount, frequency and how to cancel.
- The **Card Account Updater** service automatically refreshes stored card details when a card is reissued (Growth and Scale).
- You must stop charging a customer as soon as they cancel. Charging after cancellation is a common cause of chargebacks.

## 5. API access

- API keys are available in the dashboard. **Publishable keys** may be used in browser or app code; **secret keys** must be kept on your server and never shared, emailed or committed to code repositories.
- MerchantBridge staff will **never** ask for your secret API key.
- **Test mode** keys work with test card numbers only and never move real money.
- **Rate limits:** **100 requests per second** in live mode and **25 requests per second** in test mode, per account. Requests above the limit receive an HTTP **429** response and should be retried with back-off.
- **Idempotency keys** can be sent with POST requests to prevent duplicate payments. Keys are stored for **24 hours**.
- **API versions** are supported for at least **12 months** after a newer version is released. We give at least 12 months' notice before retiring a version.

## 6. Webhooks

- Webhooks notify your system of events such as successful payments, refunds, chargebacks and payouts.
- Every webhook is signed. You must **verify the signature** before acting on it.
- If your endpoint does not return an HTTP 2xx response within **10 seconds**, we retry with exponential back-off for up to **3 days** (a maximum of **15 attempts**). After that the event is marked as failed but remains available through the API for 30 days.

## 7. Availability

- We aim for **99.95%** monthly availability of the payments API. This is a target, not a contractual guarantee, except for Enterprise customers with a signed service level agreement.
- Live service status and incident updates are published at **status.merchantbridge.example**.
- Scheduled maintenance is announced at least **5 business days** in advance and is carried out between 00:00 and 05:00 UK time where possible.

## 8. Developer support

Developer support is provided by email at **developers@merchantbridge.example**. We aim to reply within **1 business day**. We can help with how our API behaves, but we cannot write, debug or host merchants' own website code.

## 9. Related documents

- MBFS-POL-09 Fraud Prevention and Account Security Policy
- MBFS-POL-04 Chargebacks and Disputes Policy
- MBFS-POL-08 Multi-Currency and FX Policy
