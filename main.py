from src.data_loader import load_data
from src.data_preprocess import preprocess_data
from src.demand_model import train_demand_model
from src.risk_model import train_risk_model

df = load_data('Data\Raw_data.csv') 


df = preprocess_data(df)

df.to_csv("Data\cleaned_data.csv", index=False)

train_demand_model(df)
train_risk_model(df)


print("All model training completed and saved successfully.")