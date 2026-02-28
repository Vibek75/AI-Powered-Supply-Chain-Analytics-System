import streamlit as st
import pandas as pd
import joblib
from service.api_data import get_news_fuel, get_fuel_price_index, get_market_news, get_weather


weather_api = "WeatherAPIKey" # OpenWeatherMap API Key
news_api = "NewsAPIKey" # NewsAPI Key

df = pd.read_csv("Data/supply_chain_data_10000_rows.csv")

base_index = 1





weather_map = {
    "Clear": 0,
    "Clouds": 1,
    "Rain": 2,
    "Thunderstorm": 3,
    "Snow":4
}

product_map = {
    "PROD_001": 0,
    "PROD_002": 1,
    "PROD_003": 2,
    "PROD_004": 3,
    "PROD_005": 4
}
  
demand_model = joblib.load("Model/demand_model.pkl")
risk_model = joblib.load("Model/risk_model.pkl")

st.title("Supply Chain Demand And Risk Dashboard")
city = st.text_input("Enter City Name", value="Kolkata")



news_df = get_news_fuel(city, news_api)

fuel_index, fuel_news = get_fuel_price_index(news_df, base_index)


market_news = get_market_news(news_df)


weather_forcast = get_weather(weather_api, city)
forcast_dates = list(weather_forcast.keys())
date_range = pd.to_datetime(forcast_dates)


product_list = sorted(df['Product_ID'].unique())
selected_product = st.selectbox("Select Product", product_list)
product_encoded = product_map.get(selected_product, 0)



inventory = st.number_input(f"Enter inventory Level for {selected_product}", min_value= 0, value = 200, step = 1)
unit_price = st.number_input(f"Enter Unit Price for {selected_product}", min_value = 0.0, value = 30.0, step = 0.5)
lead_time = st.number_input(f"Enter Lead Time(Days) for {selected_product}", min_value = 0, value = 4, step = 1)




final_data= []



for single_date in date_range:

    date_str = single_date.strftime("%Y-%m-%d")

    weather_today = weather_forcast.get(date_str, "Clear")
    weather_encoded = weather_map.get(weather_today, 0)



    units_pred = demand_model.predict([[
        product_encoded,
        inventory, 
        unit_price,
        float(fuel_index), 
        weather_encoded, 
        lead_time
    ]])

    risk_pred = risk_model.predict([[
        product_encoded,
        fuel_index,
        weather_encoded,
        lead_time
    ]])[:, 1]



    row = {
        "Product": selected_product,
        "Date": date_str,
        "Inventory": inventory,
        "Unit_Price": unit_price,
        "Lead_Time": lead_time,
        "weather": weather_today,
        "Predicted_Units": int(units_pred[0]),
        "Risk": "High" if risk_pred[0] > 0.6 else "Low",
        }

    final_data.append(row)




forcast_df = pd.DataFrame(final_data)








st.subheader(f" Today's Demand And Risk for {selected_product} ")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Live Weather: ", weather_today)
with col2:
    st.metric("Units Sold Prediction:", int(units_pred[0]))
with col3:
    if risk_pred[0] > 0.6:
        st.error("High Risk")
    else:
        st.success("Low Risk")



st.subheader(f"Demand and Risk Forecast For {selected_product} with Inventory {inventory}, Unit Price {unit_price} and Lead Time {lead_time} days")
st.dataframe(forcast_df[["Date", "weather", "Predicted_Units", "Risk"]])
st.subheader(f"Line Chart Demand For {selected_product}")
st.line_chart(forcast_df.set_index("Date")["Predicted_Units"])



if "product_forcasts" not in st.session_state:
    st.session_state.product_forcasts = pd.DataFrame(columns=[
        "Product", "Date","Inventory", "Unit_Price", "Lead_Time", "weather", "Predicted_Units", "Risk"
        ])
    

existing_df = st.session_state.product_forcasts
if st.button("Add to Comparison"):
    if selected_product not in existing_df["Product"].unique():
        st.session_state.product_forcasts = pd.concat([existing_df, forcast_df], ignore_index = True)
        st.success(f"{selected_product} Added to Table")
    else:
        st.warning(f"{selected_product} Already in Table")

save_df = st.session_state.product_forcasts



st.subheader("Saved Product Forecasts")
remove_product = st.selectbox("Remove Product", st.session_state.product_forcasts["Product"].unique())

if st.button("Remove"):
    st.session_state.product_forcasts = \
        st.session_state.product_forcasts[
            st.session_state.product_forcasts["Product"] != remove_product
        ]
st.dataframe(st.session_state.product_forcasts)




st.subheader("Predicted Demand Of Product")
bar_df = save_df.groupby("Product")["Predicted_Units"].sum().reset_index()
st.bar_chart(bar_df.set_index("Product"))

st.subheader("Units Demand Trend Over Time")
trend_df = save_df.groupby("Date")["Predicted_Units"].sum().reset_index() 
st.line_chart(trend_df.set_index("Date"))


st.subheader("Fuel Related News")

if fuel_news is not None :
    for h in fuel_news['Headline'][:5]:
        st.write("-", h)
else:
    st.write("No Fuel Related News Found")


st.subheader("Market Related News")

if market_news is not None:
    for h in market_news['Headline'][:5]:
        st.write("-", h)
else:
    st.write("No Market Related News Found")


