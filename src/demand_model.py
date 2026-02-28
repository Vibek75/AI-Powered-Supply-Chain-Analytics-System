from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

def train_demand_model(df):
    x = df[['Product_ID',
            'Inventory_Level', 
            'Unit_Price',
            'Fuel_Price_Index',
            'Weather_Condition',
            'Lead_Time_Days']]
    y = df['Units_Sold']


    x_train, _, y_train, _ = train_test_split(x, y , test_size = 0.2, random_state = 42)

    model = RandomForestRegressor(n_estimators= 100, random_state = 42, max_depth = 10)

    model.fit(x_train, y_train)

    joblib.dump(model, "Model/demand_model.pkl")

    return model