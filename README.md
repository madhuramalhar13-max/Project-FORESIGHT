# 🚀 Project FORESIGHT

## AI-Powered Demand & Inventory Intelligence Platform

Project FORESIGHT is an AI-powered demand forecasting and inventory intelligence platform designed to help businesses predict product demand, identify inventory risks, and generate actionable recommendations.

The system combines historical sales data, inventory information, machine learning forecasting, and rule-based risk analysis into a single dashboard and API.

---

## 🎯 Problem Statement

Businesses often face two major inventory problems:

- **Stockouts** – insufficient inventory to satisfy future demand.
- **Overstocking** – excess inventory that increases holding costs and the risk of unsold products.

Project FORESIGHT addresses these problems by:

1. Forecasting product demand.
2. Evaluating forecast performance.
3. Analyzing current inventory.
4. Detecting stockout and overstock risks.
5. Generating inventory recommendations.
6. Providing an interactive dashboard.
7. Exposing results through REST APIs.

---

## 🏗️ System Architecture

```text
Raw Data
   ↓
Data Validation & Cleaning
   ↓
Weekly Demand Aggregation
   ↓
Feature Engineering
   ↓
 ┌───────────────────────────┐
 │      Forecasting Models   │
 │                           │
 │ Seasonal Naive            │
 │ LightGBM                  │
 └───────────────────────────┘
   ↓
Model Evaluation / Backtesting
   ↓
Future Demand Forecast
   ↓
Inventory Risk Engine
   ↓
Decision & Recommendation Engine
   ↓
 ┌───────────────────────┐
 │                       │
 │  FastAPI    Streamlit │
 │     API      Dashboard│
 │                       │
 └───────────────────────┘