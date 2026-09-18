# Project FORESIGHT

AI-Powered Demand & Inventory Intelligence Platform

## Overview
Project FORESIGHT is an AI-driven demand forecasting and inventory risk management platform.

## Features
- Demand forecasting
- LightGBM model
- Seasonal Naive baseline
- 12-week future forecasting
- Stockout and overstock risk detection
- Inventory recommendations
- FastAPI backend
- Streamlit dashboard

## Technology Stack
Python, Pandas, NumPy, Scikit-learn, LightGBM, FastAPI, Streamlit, Matplotlib, Seaborn

## Run Pipeline
python -m src.pipeline

## Run API
uvicorn service.main:app --reload

## Run Dashboard
streamlit run app/dashboard.py

## API Documentation
http://127.0.0.1:8000/docs

## Model Evaluation
Seasonal Naive WAPE: 19.68%
LightGBM WAPE: 18.13%

## Current Results
50 SKUs analyzed, 600 future forecast records generated, and inventory risks calculated.

