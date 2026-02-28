# AI-Powered Supply Chain Risk & Demand Forecasting System

# Overview:

An intelligent AI-powered Supply Chain Analytics System that integrates:

  📦 Demand Forecasting (Regression)

  🚚 Shipping Delay Risk Prediction (Classification)

  ⛽ Fuel Price Sentiment Index (News-based)
  
  🌦 Weather Impact Integration

  📊 Interactive Streamlit Dashboard

This project combines Machine Learning + Economic Signals + Weather Data + Real-Time News Sentiment to create a dynamic supply chain decision system.






# Execution Workflow:

Run main.py

↓

Clean Dataset

↓

Train ML Models

↓

Save Models

↓

Launch Streamlit Dashboard

↓

Live Predictions



# How to Run:

Install Dependencies:

    pip install -r requirements.txt



Train Models Automatically:

    python main.py

✔ Cleans data

✔ Trains Demand Model

✔ Trains Risk Model

✔ Saves models in /Model



Launch Dashboard:

    streamlit run app/dashboard.py

# API Setup:

You must generate your own API keys for:

OpenWeatherMap API

NewsAPI



Add keys inside:

    app/dashboard.py

# Dashboard Features:

• Selected product details

• Live weather condition for entered city

• Predicted units sold (demand forecast)

• Shipping delay risk status (High / Low)

• Multi-day demand forecast table

• Demand trend line chart

• Product-wise total predicted demand (bar chart)

• Demand trend over time (time-series chart)

• Saved product comparison table

• Top fuel-related news headlines

• Top market-related news headlines

# Tech Stack:

• Python 3.10

• Pandas

• NumPy

• Scikit-Learn

• Streamlit

• Joblib

• NewsAPI

• OpenWeatherMap API
