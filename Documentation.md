# Comprehensive Project Documentation & Data Cleaning Report

## 1. Overview & Objectives
This document provides full technical details for the E-Commerce Sales Cleaning Project. The goal of this pipeline was to transform raw checkout logs into a structured, reliable dataset for exploratory analysis and business intelligence.

## 2. Dataset Specs & Schema
- **Data Period:** July 24,2026– July 29, 2026
- **Total Records:** 1,200 transactions
- **Total Columns:** 14

### Data Dictionary
| Field | Data Type | Notes |
| :--- | :--- | :--- |
| `OrderID` | Text | Primary key (e.g., `ORD200000`) |
| `Date` | Datetime | Transaction timestamp |
| `CustomerID` | Text | Unique identifier for buyers |
| `Product` | Text | Item category (7 unique values) |
| `Quantity` | Integer | Volume purchased (1–5) |
| `UnitPrice` | Float | Unit price ($11.39–$699.93) |
| `ShippingAddress` | Text | Customer street address |
| `PaymentMethod` | Text | Method used (Online, Cash, Credit Card, Debit Card, Gift Card) |
| `OrderStatus` | Text | Fulfillment status (Delivered, Shipped, Pending, Cancelled, Returned) |
| `TrackingNumber` | Text | Logistics tracking code |
| `ItemsInCart` | Integer | Total items in cart during checkout |
| `CouponCode` | Text | Applied coupon (`FREESHIP`, `SAVE10`, `WINTER15`, `No Coupon`) |
| `ReferralSource` | Text | Marketing origin (`Instagram`, `Email`, `Google`, `Facebook`, `Referral`) |
| `TotalPrice` | Float | Calculated monetary output (`Quantity * UnitPrice`) |

## 3. Data Cleaning Audit Log
1. **Missing Value Treatment (`CouponCode`):**
   - Imputed 309 missing entries with `"No Coupon"`.
2. **Field Verification:**
   - Validated mathematical integrity: `TotalPrice = Quantity * UnitPrice`.
   - Verified zero duplicate keys for `OrderID` and `TrackingNumber`.
## 4. Project Details
1. **Project Name:** Ecommerce Analysis
2. **Company:** DecodeLab
3. **Email** jshahram2382005@gmail.com
4. **Developer** Shahram Hussain
5. **Linkedin** www.linkedin.com/in/shahram-hussain-b39244399

## 4. Key Metrics Summary
- **Gross Revenue:** $1,264,761.96
- **Average Order Value (AOV):** $1,053.97
- **Coupon Usage Rate:** 74.25%
