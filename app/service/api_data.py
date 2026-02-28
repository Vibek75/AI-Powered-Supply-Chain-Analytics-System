import requests
import pandas as pd

def get_news_fuel(city, API):

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q=({city}) AND (fuel OR oil OR economy)"
        f"&apiKey={API}"
    )

    response = requests.get(url)
    data = response.json()

    articles = data['articles']
    news_list = []
    for article in articles:
        news_list.append({
            "Date":article['publishedAt'][:10],
            "Headline": article['title']
        })

    news_df = pd.DataFrame(news_list)

    return news_df



   


def get_fuel_price_index(df,base_index):
    
    
    score = 0
    try:
        fuel_news_df =df[df['Headline'].str.contains('fuel|oil|petrol|diesel', case = False, na = False)]
        if fuel_news_df.empty:
            raise ValueError ("No Headlines related to Fuel")
            
        negative = ['rise', 'surge', 'increase', 'strike', 'crisis']
        positive = ['drop', 'decrease', 'relief', 'stable']

        for h in fuel_news_df['Headline']:
            h=str(h).lower()
            neg_count = sum(1 for w in negative if w in h)
            pos_count = sum(1 for w in positive if w in h)
            score += neg_count
            score -= pos_count

        sentiment_strength = score/ max(len(fuel_news_df), 1)
        adjustment = sentiment_strength*0.2
        fuel_index = base_index*(1+adjustment)


        return round(fuel_index, 2), fuel_news_df
    except Exception as e:
        ValueError(f"Error in get fuel price index: {e}")
        return round(base_index, 2) , None





def get_market_news(df):
    market_news_df = df[df['Headline'].str.contains('economy|market|GDP|inflation', case = False)]
    #not use in predction 
    return market_news_df

   
def get_weather(API, City):

    url =(
        f"https://api.openweathermap.org/data/2.5/forecast?q={City}&appid={API}&units=metric"
    )

    responce = requests.get(url)
    data= responce.json()

    daily_weather = {}
    if "list" in data:
        for item in data["list"]:
            date = item["dt_txt"][:10]
            weather = item ['weather'][0]["main"]

            if date not in daily_weather:
                daily_weather[date]= weather

    return daily_weather





