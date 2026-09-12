# Project FORESIGHT – System Architecture

## 1. Project Overview

Project FORESIGHT is an AI-powered demand forecasting and inventory intelligence platform designed to help businesses make better inventory planning decisions.

The system forecasts future SKU-level demand, identifies stockout and overstock risks, calculates business impact, and recommends appropriate inventory actions.

---

# 2. Business Problem

Businesses often face two major inventory problems:

1. Stockouts – High-demand products run out of stock, resulting in lost sales.
2. Overstock – Slow-moving products occupy inventory and lock working capital.

Project FORESIGHT helps solve these problems by forecasting future demand and combining those predictions with current inventory information.

---

# 3. System Workflow

```text
Raw Data
    │
    ▼
Data Pipeline
    │
    ▼
Data Cleaning & Validation
    │
    ▼
Analysis-Ready Dataset
    │
    ▼
Weekly Demand Aggregation
    │
    ▼
Feature Engineering
    │
    ▼
Forecasting Engine
    │
    ├── Seasonal Naive Baseline
    │
    └── Machine Learning Model
    │
    ▼
Rolling-Origin Backtesting
    │
    ▼
Best Forecasting Model
    │
    ▼
Future Demand Forecast
    │
    ▼
Inventory Risk Engine
    │
    ├── Stockout Risk
    │
    └── Overstock Risk
    │
    ▼
Business Impact Calculation
    │
    ▼
Decision Engine
    │
    ├── Reorder Now
    ├── Markdown / Clear
    ├── Watch / Volatile
    └── Healthy
    │
    ▼

# Project FORESIGHT – System Architecture

## 1. Project Overview

Project FORESIGHT is an AI-powered demand forecasting and inventory intelligence platform designed to help businesses make better inventory planning decisions.

The system forecasts future SKU-level demand, identifies stockout and overstock risks, calculates business impact, and recommends appropriate inventory actions.

---

# 2. Business Problem

Businesses often face two major inventory problems:

1. Stockouts – High-demand products run out of stock, resulting in lost sales.
2. Overstock – Slow-moving products occupy inventory and lock working capital.

Project FORESIGHT helps solve these problems by forecasting future demand and combining those predictions with current inventory information.

---

# 3. System Workflow

```text
Raw Data
    │
    ▼
Data Pipeline
    │
    ▼
Data Cleaning & Validation
    │
    ▼
Analysis-Ready Dataset
    │
    ▼
Weekly Demand Aggregation
    │
    ▼
Feature Engineering
    │
    ▼
Forecasting Engine
    │
    ├── Seasonal Naive Baseline
    │
    └── Machine Learning Model
    │
    ▼
Rolling-Origin Backtesting
    │
    ▼
Best Forecasting Model
    │
    ▼
Future Demand Forecast
    │
    ▼
Inventory Risk Engine
    │
    ├── Stockout Risk
    │
    └── Overstock Risk
    │
    ▼
Business Impact Calculation
    │
    ▼
Decision Engine
    │
    ├── Reorder Now
    ├── Markdown / Clear
    ├── Watch / Volatile
    └── Healthy
    │
    ▼

Dashboard & Scoring Service