---
document_id: MBFS-POL-08
title: Multi-Currency and Foreign Exchange Policy
version: 1.4
effective_date: 2026-06-01
last_reviewed: 2026-06-01
owner: Treasury Operations
applies_to: All merchant accounts
classification: Public — customer-facing
---

> **Synthetic document.** MerchantBridge Financial Services Ltd is a fictional company created for testing and training purposes. All names, figures, phone numbers, reference numbers and addresses are invented.

# Multi-Currency and Foreign Exchange Policy

## 1. Key terms

- **Presentment currency** — the currency the customer is charged in.
- **Settlement currency** — the currency we pay out to your bank account.
- **Mid-market rate** — the midpoint between buy and sell rates on global currency markets, taken from our rate provider at the time of conversion.
- **FX markup** — the percentage we apply to the mid-market rate when we convert money for you.

## 2. Accepting payments in other currencies

- **Online:** you can charge customers in any of **30 presentment currencies** listed in the dashboard.
- **In person:** BridgePay terminals charge in **GBP only**.
- MerchantBridge does **not** offer Dynamic Currency Conversion (DCC). Foreign cardholders paying in GBP may be charged a foreign transaction fee by their own card issuer; MerchantBridge has no control over this.
- Note that the currency the customer pays in is different from the **origin of the card**. A card issued outside the UK and EEA attracts the 1.50% international card surcharge even if the payment is in GBP (see MBFS-POL-02).

## 3. Settlement currencies

| Plan | Settlement currencies |
|---|---|
| Starter | GBP only |
| Growth | GBP, EUR, USD |
| Scale | GBP, EUR, USD |
| Enterprise | GBP, EUR, USD and others by agreement |

- EUR and USD payouts require a bank account **in that currency**, held in the name of the business, located in the **UK or EEA**.
- You can choose to settle each presentment currency into a settlement currency (for example, EUR sales settled in EUR, everything else in GBP).
- Instant Payouts are available in GBP only.
- Payout timing for EUR and USD follows your plan's schedule, but USD payouts may take **one extra business day** to arrive because they are sent by international transfer.

## 4. How conversion works

Conversion happens when your batch closes (22:00 UK time on the processing day). We apply the mid-market rate adjusted by the FX markup **in MerchantBridge's favour**:

> **Converted amount = original amount × mid-market rate × (1 − FX markup)**

| Plan | FX markup |
|---|---|
| Starter | Not applicable (GBP only) |
| Growth | **1.25%** |
| Scale | **0.90%** |
| Enterprise | Bespoke |

The FX markup is VAT-exempt and is shown separately on your statement.

**Worked example (Growth):** you sell goods for **$500** online and settle in GBP. The mid-market rate at batch close is **$1 = £0.7900**.
£ received before transaction fees = 500 × 0.7900 × (1 − 0.0125) = **£390.06**.
Transaction fees are calculated on the $500 in USD and converted in the same way.

If no conversion is needed (for example, GBP sales settled in GBP, or EUR sales settled in EUR) no FX markup is charged.

## 5. Refunds and chargebacks in other currencies

Refunds and chargebacks are converted at the rate applying on the date of the refund or chargeback, not the original rate. Any gain or loss from exchange rate movements is yours.

## 6. Exchange rate information

The rate applied to each batch is shown in your dashboard and statement. We cannot provide forward rates, hedge currency risk, or give advice on when to convert currency.

## 7. Related documents

- MBFS-POL-02 Pricing Plans and Billing Policy
- MBFS-POL-03 Settlement and Payouts Policy
- MBFS-DATA-01 Fee and Rate Schedule
