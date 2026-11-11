---
document_id: MBFS-POL-05
title: Refunds and Reversals Policy
version: 2.3
effective_date: 2026-06-01
last_reviewed: 2026-06-01
owner: Payments Operations
applies_to: All merchant accounts
classification: Public — customer-facing
---

> **Synthetic document.** MerchantBridge Financial Services Ltd is a fictional company created for testing and training purposes. All names, figures, phone numbers, reference numbers and addresses are invented.

# Refunds and Reversals Policy

## 1. Voids versus refunds

| | **Void** | **Refund** |
|---|---|---|
| When | Before the batch cut-off (**22:00 UK time**) on the processing day | Any time after the batch has closed, up to **180 days** after the original transaction |
| Effect for the customer | The pending payment disappears from their statement, usually within 1–3 business days | The money is credited back to their card, usually within **3–10 business days** |
| Fee | No transaction fee is charged | No refund fee, but the **original transaction fee is not returned** |
| Where | Dashboard, terminal (manager PIN), or API | Dashboard, terminal (manager PIN), or API |

## 2. Refund rules

- Refunds must be made **to the card used for the original payment**. Refunds cannot be sent to a different card or bank account.
- You must **not refund card payments in cash**. Cash refunds of card transactions are a recognised money-laundering and fraud risk and breach card scheme rules.
- Refunds can be **full or partial**. The total of all refunds on a transaction cannot exceed the original amount.
- The refund window is **180 days** from the original transaction. After that, you must arrange repayment with the customer outside MerchantBridge.
- Refunds are processed in the **original transaction currency**. If you settle in a different currency, the refund is converted at the rate on the refund date and you bear any difference from the original conversion (see MBFS-POL-08).
- **Do not refund a transaction that is subject to a chargeback** (see MBFS-POL-04, section 4).
- Once a refund has been processed it **cannot be cancelled**.

## 3. How refunds are funded

Refunds are deducted from your MerchantBridge balance. If your balance is insufficient, you can still issue refunds up to **£1,000 per day** from a negative balance; we recover the shortfall from future settlements or by Direct Debit. Refunds above this amount require a positive balance.

## 4. Refund monitoring

To protect against fraud and errors, refunds may be **held for review** (usually for no more than 1 business day) if, in a single day, they exceed **£5,000** or **25%** of your card volume over the previous 30 days. We will notify you if a refund is held.

## 5. Refunds when your account is closing or closed

- While your account is in its notice period you can continue to issue refunds as normal.
- After closure, refunds can only be issued by contacting support and while funds remain in your closing reserve (MBFS-POL-11). Otherwise you must refund the customer directly.

## 6. Customer enquiries about refunds

If a customer says they have not received a refund, give them the **Acquirer Reference Number (ARN)** shown on the refund in the dashboard. Their bank can use the ARN to trace the refund. MerchantBridge cannot speed up how quickly a card issuer credits the cardholder.

## 7. Related documents

- MBFS-POL-04 Chargebacks and Disputes Policy
- MBFS-POL-08 Multi-Currency and FX Policy
- MBFS-POL-02 Pricing Plans and Billing Policy
