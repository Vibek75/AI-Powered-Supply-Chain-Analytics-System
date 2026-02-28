

import pandas as pd


def preprocess_data(df):
    df['Date'] = pd.to_datetime(df['Date'], format = '%d-%m-%Y')


    product_map = {
        "PROD_001": 0,
        "PROD_002": 1,
        "PROD_003": 2,
        "PROD_004": 3,
        "PROD_005": 4
    }
    df['Product_ID'] = df['Product_ID'].map(product_map)
    

    weather_map = {
        "Sunny":0,
        "Cloudy":1,
        "Rainy":2,
        "Storm":3,
        "Snow":4,
    }

    df['Weather_Condition'] = df['Weather_Condition'].map(weather_map)



    df['Delay_Risk'] = df['Shipping_Delay_Days'] > 2

 

    return df
