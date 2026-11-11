# MerchantBridge Financial Services: synthetic customer support corpus and evaluation set

**Everything in this pack is synthetic.** MerchantBridge Financial Services Ltd is a fictional UK merchant-services company. All names, prices, phone numbers (Ofcom drama range 020 7946 0xxx), email domains (`.example`), company and FCA reference numbers, and addresses are made up. Nothing here is legal, financial or regulatory guidance.

Reference date for the pack: **11 November 2026**. Several answers depend on dates.

## What's included

```
merchantbridge/
├── README.md                         ← this file (not part of the corpus)
├── corpus/                           ← the 25 knowledge-base documents
│   ├── policies/   15 × Markdown     MBFS-POL-01 … MBFS-POL-15
│   ├── faqs/        5 × HTML         MBFS-FAQ-01 … MBFS-FAQ-05
│   ├── data/        1 × CSV          MBFS-DATA-01 fee-and-rate schedule (64 rows)
│   └── notices/     4 × TXT          MBFS-NTC-00 … MBFS-NTC-03
└── eval/
    └── tricky_queries.json           ← 20 queries with expected answers
```

**Why 25 documents?** The breakdown you specified (15 MD + 5 HTML + 1 CSV) comes to 21. To reach the 25 total, I added **4 plain-text documents**: a precedence/contact/glossary sheet and three dated Service Notices. These notices are where most of the time-based and source-conflict tests come from. If you only want the 21, delete `corpus/notices/`. Queries MB-Q04, Q05, Q10 and Q13 depend on the notices.

### Policies (Markdown, with YAML front matter)

| ID | File | Topic |
|---|---|---|
| POL-01 | 01_account-opening-and-verification-policy.md | Eligibility, KYB documents, £2,000 pre-verification limit |
| POL-02 | 02_pricing-plans-and-billing-policy.md | Plans, fee structure, VAT, MMSC, price changes, surcharging |
| POL-03 | 03_settlement-and-payouts-policy.md | Cut-off, T+1/T+2, Instant Payouts, returned payouts |
| POL-04 | 04_chargebacks-and-disputes-policy.md | Process, 7-day response, fees, ratio thresholds |
| POL-05 | 05_refunds-and-reversals-policy.md | Voids vs refunds, 180-day window, no cash refunds |
| POL-06 | 06_payment-terminal-hardware-policy.md | Mini/Go/Counter, rentals, ETF, lost/stolen, offline mode |
| POL-07 | 07_online-payments-and-api-policy.md | SCA, payment links, API limits, webhooks |
| POL-08 | 08_multi-currency-and-fx-policy.md | Settlement currencies, FX markup formula |
| POL-09 | 09_fraud-prevention-and-account-security-policy.md | "We will never ask", 24/7 line, PCI DSS |
| POL-10 | 10_prohibited-and-restricted-businesses-policy.md | Prohibited list, restricted conditions |
| POL-11 | 11_rolling-reserves-and-risk-holds-policy.md | Reserves, holds, closing reserve |
| POL-12 | 12_contract-term-cancellation-and-account-closure-policy.md | Terms, ETFs, closure |
| POL-13 | 13_complaints-handling-policy.md | Timescales, FOS, vulnerability, accessibility |
| POL-14 | 14_data-protection-and-privacy-policy.md | UK GDPR, retention, rights |
| POL-15 | 15_bridgeadvance-merchant-cash-advance-policy.md | Merchant cash advance: factor rate, holdback |

### FAQs (HTML)

`faq-getting-started.html`, `faq-payments-and-payouts.html`, `faq-terminals-and-hardware.html`, `faq-fees-and-billing.html`, `faq-disputes-security-and-account.html`. Each Q&A is a `<section class="faq-item" id="…">`, so citations can point to a specific anchor.

### Fee and rate schedule (CSV)

`fee-and-rate-schedule.csv` has 64 rows with these columns: `fee_id, category, item, plan, channel, card_type, card_region, percentage_rate, fixed_fee_gbp, minimum_fee_gbp, maximum_fee_gbp, billing_unit, vat_treatment, effective_from, effective_to, notes`. Some rows are effective-dated: the chargeback fee changes on 2027-01-01 and Starter Instant Payouts start on 2026-09-01.

## Built-in traps

These are deliberate. They test retrieval, source precedence and reasoning about dates.

1. **Outdated FAQ.** `faq-payments-and-payouts.html` (last updated 14 Mar 2026) says Instant Payouts are only for Growth and Scale. Service Notice NTC-01 extended them to Starter from 1 Sep 2026.
2. **Scheduled fee change.** The chargeback fee is £15 today and £20 from 1 Jan 2027 (NTC-02, CSV rows DSP-003/004). The policy and FAQ only show £15.
3. **Hidden free exit.** NTC-02 is a price increase, so merchants can leave free of early termination fees before 1 Jan 2027.
4. **Substitute bank holiday.** Boxing Day 2026 is a Saturday, so the bank holiday moves to Monday 28 Dec.
5. **Look-alike worked example.** POL-12 has a worked ETF example (1 June start) that resembles MB-Q13 but has different dates.

`corpus/notices/00_document-precedence-and-glossary.txt` sets the order of precedence: **Notices (from their effective date) > CSV schedule > Policies > FAQs**. It also lists what is out of scope.

## Evaluation set (`eval/tricky_queries.json`)

The file has 20 queries. Each one includes `expected_answer`, `key_facts`, `source_documents` (path, section, and role: primary, supporting or distractor), `edge_case_handling` and `failure_modes`. Where arithmetic is involved there is also a verified `calculation` block. Coverage:

| Theme | Queries |
|---|---|
| Table lookups / calculations | Q01, Q02, Q09, Q12, Q19 |
| Multi-document synthesis | Q06, Q10, Q12, Q13, Q20 |
| Out of scope (fully or partly) | Q07, Q08, Q14 |
| Ambiguous phrasing / clarification | Q02, Q03, Q11, Q17 |
| Temporal / conflicting sources | Q04, Q05, Q10, Q13 |
| Eligibility & policy boundaries | Q15, Q17 |
| Security, data protection, complaints | Q16, Q18, Q20 |

The dataset header also includes category definitions, per-category counts and a suggested scoring rubric (0–10 per query, plus automatic-fail conditions).
