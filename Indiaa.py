import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
import warnings
import numpy as np
import logging
import requests
import datetime as dt
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
warnings.filterwarnings("ignore", category=UserWarning)

API_KEY = 'ab63f605ff041a5e6010344f594d0e54'
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast?"

def read_weather_data(city):
    try:
        weather = pd.read_csv("india.csv")
        city_data = weather[weather["NAME"] == city].set_index("DATE")
        return city_data
    except Exception as e:
        logging.error(f"Error reading weather data: {e}")
        raise

reg_temp = Ridge(alpha=.1)
reg_precip = Ridge(alpha=.1)

def create_predictions(city, predictors, core_weather, reg_temp, reg_precip):
    try:
        train = core_weather.loc[:"2023-12-31"]
        test = core_weather.loc["2024-01-01":]

        reg_temp.fit(train[predictors], train["target_temp"])
        predictions_temp = reg_temp.predict(test[predictors])

        reg_precip.fit(train[predictors], train["target_precip"])
        predictions_precip = reg_precip.predict(test[predictors])

        error_temp = mean_squared_error(test["target_temp"], predictions_temp)
        error_precip = mean_squared_error(test["target_precip"], predictions_precip)

        combined_temp = pd.concat([test["target_temp"], pd.Series(predictions_temp, index=test.index)], axis=1)
        combined_temp.columns = ["actual_temp", "predictions_temp"]

        combined_precip = pd.concat([test["target_precip"], pd.Series(predictions_precip, index=test.index)], axis=1)
        combined_precip.columns = ["actual_precip", "predictions_precip"]

        return error_temp, error_precip, combined_temp, combined_precip
    except Exception as e:
        logging.error(f"Error creating predictions: {e}")
        raise

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def get_current_weather(city, days_requested):
    url = BASE_URL + "appid=" + API_KEY + "&q=" + city
    try:
        response = requests.get(url).json()
        if response['cod'] != '200':
            logging.error(f"Error fetching weather data: {response['message']}")
            return []

        current_forecast = []
        for forecast in response['list'][:days_requested]:
            forecast_date = dt.datetime.utcfromtimestamp(forecast['dt']).date()
            temp_kelvin = forecast['main']['temp']
            temp_celsius = kelvin_to_celsius(temp_kelvin)

            current_forecast.append({
                "date": forecast_date.strftime('%d-%m-%Y'),
                "temperature": temp_celsius,
                "humidity": forecast['main']['humidity'],
                "wind_speed": forecast['wind']['speed'],
                "description": forecast['weather'][0]['description']
            })

        return current_forecast
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        return []

def plot_temperature_graph(predicted_temps, current_temps):
    plt.figure(figsize=(10, 6))

    if isinstance(predicted_temps, pd.DataFrame):

        plt.plot(predicted_temps.index, predicted_temps['predictions_temp'], label='Predicted Temperature', linestyle='--')
    elif isinstance(predicted_temps, pd.Series):

        plt.plot(predicted_temps.index, predicted_temps.values, label='Predicted Temperature', linestyle='--')
    else:
        logging.warning("Invalid input type for predicted_temps")


    for i, temp in enumerate(current_temps):
        temp_date = dt.datetime.strptime(temp['date'], '%d-%m-%Y')
        plt.scatter(temp_date, temp['temperature'], label=f'Current Temp Day {i+1}', marker='o')

    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title('Past Temperature vs Current Temperature')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def predict_weather(city, core_weather, reg_temp, reg_precip, predictors, start_date, end_date):
    try:
        start_date = pd.to_datetime(start_date, format='%d-%m-%Y')
        end_date = pd.to_datetime(end_date, format='%d-%m-%Y')

        date_range = pd.date_range(start=start_date, end=end_date)
        days_requested = (end_date - start_date).days + 1

        temperatures = []
        precipitations = []
        for date in date_range:
            date_month_day = date.strftime('%d-%m')
            past_data = core_weather[core_weather.index.strftime('%d-%m') == date_month_day]
            if len(past_data) > 0:
                future_weather = past_data[predictors].mean().values.reshape(1, -1)
                future_temperature = reg_temp.predict(future_weather)
                future_precipitation = reg_precip.predict(future_weather)
                temperatures.append((date, future_temperature[0]))
                precipitations.append((date, future_precipitation[0]))
            else:
                logging.warning(f"No past data available for {date.strftime('%d-%m-%Y')}")

        current_weather = get_current_weather(city, days_requested)

        combined_weather = []
        for i in range(len(date_range)):
            combined_weather.append({
                "date": date_range[i].strftime('%d-%m-%Y'),
                "predicted_temp": round(temperatures[i][1], 2) if i < len(temperatures) else None,
                "predicted_precip": round(precipitations[i][1], 2) if i < len(precipitations) else None,
                "humidity": current_weather[i]['humidity'] if i < len(current_weather) else None,
                "wind_speed": current_weather[i]['wind_speed'] if i < len(current_weather) else None,
                "description": current_weather[i]['description'] if i < len(current_weather) else None
            })

        return combined_weather

    except Exception as e:
        logging.error(f"Error predicting weather: {e}")
        raise

def process_weather_data(city):
    try:
        weather_data = read_weather_data(city)

        core_weather = weather_data[["PRCP", "TAVG", "TMAX", "TMIN"]].copy()
        core_weather.columns = ["precip", "temp_avg", "temp_max", "temp_min"]

        core_weather["precip"] = core_weather["precip"].fillna(0)
        core_weather = core_weather.ffill()

        core_weather.index = pd.to_datetime(core_weather.index, format='%d-%m-%Y')

        core_weather["target_temp"] = core_weather.shift(-1)["temp_max"]
        core_weather["target_precip"] = core_weather.shift(-1)["precip"]
        core_weather = core_weather.iloc[:-1, :].copy()

        core_weather.sort_index(inplace=True)

        imputer = SimpleImputer(strategy='mean')

        core_weather.replace([np.inf, -np.inf], np.nan, inplace=True)

        core_weather = pd.DataFrame(imputer.fit_transform(core_weather), columns=core_weather.columns, index=core_weather.index)

        core_weather["month_max"] = core_weather["temp_max"].rolling(30).mean()
        core_weather["month_day_max"] = core_weather.groupby(core_weather.index.strftime('%m-%d'))["temp_max"].transform('mean')
        core_weather["max_min"] = core_weather["temp_max"] / core_weather.temp_min

        core_weather.replace([np.inf, -np.inf], np.nan, inplace=True)

        core_weather = pd.DataFrame(imputer.fit_transform(core_weather), columns=core_weather.columns, index=core_weather.index)

        core_weather["monthly_avg"] = core_weather.groupby(core_weather.index.month)["temp_max"].transform(
            lambda x: x.expanding(1).mean())
        core_weather["day_of_year_avg"] = core_weather.groupby(core_weather.index.day_of_year)["temp_max"].transform(
            lambda x: x.expanding(1).mean())

        return core_weather

    except Exception as e:
        logging.error(f"Error processing weather data: {e}")
        raise

def main(city, start_date, end_date):
    try:
        core_weather = process_weather_data(city)

        temp_predictors = ["precip", "temp_max", "temp_min", "month_day_max", "max_min"]
        precip_predictors = ["temp_max", "temp_min", "month_day_max", "max_min"]

        error_temp, error_precip, combined_temp, combined_precip = create_predictions(city, temp_predictors, core_weather, reg_temp, reg_precip)

        weather_forecast = predict_weather(city, core_weather, reg_temp, reg_precip, temp_predictors, start_date, end_date)

        # Fetch current weather forecast for the next few days
        current_weather = get_current_weather(city, 5)

        # Plot the temperature graph
        plot_temperature_graph(combined_temp, current_weather)

        return weather_forecast

    except Exception as e:
        logging.error(f"Error in main: {e}")
        raise

if __name__ == "__main__":
    city = input("Enter the city you are interested in: ").strip().upper()
    start_date = input("Enter  the start date (DD-MM-YYYY): ")
    end_date = input("Enter the end date (DD-MM-YYYY): ")

    weather_forecast = main(city, start_date, end_date)

    print("\nWeather forecast for", city, ":")
    for weather in weather_forecast:
        print(f"Date: {weather['date']}")
        print(f"Predicted Temperature: {weather['predicted_temp']} °C")
        print(f"Predicted Precipitation: {weather['predicted_precip']} mm")
        print(f"Humidity: {weather['humidity']} %")
        print(f"Wind Speed: {weather['wind_speed']} m/s")
        print(f"Description: {weather['description']}")
        print("--------------------------------------------------------")
