from sklearn.ensemble import RandomForestClassifier 
import joblib

def train_risk_model(df):
    X = df[['Product_ID',
            'Fuel_Price_Index',
            'Weather_Condition',
            'Lead_Time_Days']]
    

    Y = df['Delay_Risk']

    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced', max_depth = 8)

    model.fit(X,Y)

    joblib.dump(model, "Model/risk_model.pkl")

    return model