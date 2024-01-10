import requests
from pprint import pprint
import streamlit as st
import pandas as pd

API_KEY = '6258e383fda86a1c201f5e3e76b0f99d'


def get_weather_info(api_key, city_name):
    parameters = {
        'q': city_name,
        'appid': api_key,
        "units": "metric"

    }
    response = requests.get('https://api.openweathermap.org/data/2.5/forecast', parameters)

    weather_data = response.json()

    return weather_data['list']


def display_history(city_history):
    st.subheader('Historia wyszukiwania')

    for search_city in city_history:
        st.write(f"- {search_city}")


def add_city_history(provided_city):
    st.session_state.city_history.append(provided_city)


def convert_data_to_dataframe(hourly_forecast_data):
    st.subheader("Hourly Forecast for 4 days (Every hour)")

    main_metrics = {
        "temp": [],
        "feels_like": [],
        "temp_min": [],
        "temp_max": [],
        "pressure": [],
        "sea_level": [],
        "grnd_level": [],
        "humidity": [],
        "temp_kf": []
    }

    weather_metrics = {
        "id": [],
        "main": [],
        "description": [],
        "icon": [],

    }

    wind_metrics = {
        "speed": [],
        "deg": [],
        "gust": []
    }

    time_metrics = {
        "dt": [],
        "dt_txt": []
    }

    clouds_and_visibility = {
        "clouds": [],
        "visibility": []
    }
    for entry in hourly_forecast_data:
        main = entry['main']

        weather = entry['weather'][0]

        wind = entry['wind']

        for key in main_metrics.keys():
            main_metrics[key].append(main.get(key, "None"))

        for key in weather_metrics.keys():
            weather_metrics[key].append(weather.get(key, "None"))

        for key in wind_metrics.keys():
            wind_metrics[key].append(wind.get(key, "None"))

        clouds = entry['clouds'].get('all', "None")

        clouds_and_visibility['clouds'].append(clouds)

        visibility = entry.get('visibility', "None")

        clouds_and_visibility["visibility"].append(visibility)

        dt = entry["dt"]

        time_metrics["dt"].append(dt)

        dt_txt = entry["dt_txt"]

        time_metrics["dt_txt"].append(dt_txt)

    merged_weather_data = {**main_metrics, **weather_metrics, **wind_metrics, **time_metrics, **clouds_and_visibility}

    df = pd.DataFrame(merged_weather_data)

    df['dt_txt'] = pd.to_datetime(df['dt_txt'])

    lst = []

    for row in df['dt_txt']:
        row = str(row)

        row = row.split('-')

        day, hour = row[2].split(' ')

        lst.append(day)

    df['day'] = lst

    df.to_csv('tabela.csv')

    return df


def display_temp_line_chart(df):
    # chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    chart_data = df[["temp", "temp_min", "temp_max" , "day"]]

    chart_data = chart_data.groupby('day').agg(Avg_temp=('temp' , 'mean'))

    st.write(chart_data)
    st.subheader('Srednia temperatura danego dnia')
    st.line_chart(chart_data)
    st.area_chart(chart_data)


st.title('Aplikacja pogodowa')

city = st.text_input("Wpisz miasto:", "Wroclaw")

if st.button('Znajdz pogode'):

    try:

        weather_data = get_weather_info(API_KEY, city)

        hourly_forecast_df = convert_data_to_dataframe(weather_data)

        st.write(hourly_forecast_df.info())
        st.write(hourly_forecast_df.head(10))

        display_temp_line_chart(hourly_forecast_df)

        if 'city_history' not in st.session_state:
            st.session_state.city_history = []

        # Display weather information
        # st.subheader(f"Weather Information for {city}")
        # st.write(f"**City:** {city}")
        # st.write(f"**Temperature:** {weather_data['main']['temp']} °C")
        # st.write(f"**Description:** {weather_data['weather'][0]['description']}")
        #
        # st.write(f"**Humidity:** {weather_data['main']['humidity']} %")
        # st.write(f"**Wind Speed:** {weather_data['wind']['speed']} km/h")
        # st.write(f"**Clouds:** {weather_data['clouds']['all']} %")
        # st.write(f"**Pressure:** {weather_data['main']['pressure']} hPa")
        # st.write(f"**Visibility:** {weather_data['visibility']} m")
        # st.write(f"**Sunrise:** {weather_data['sys']['sunrise']} UTC")
        # st.write(f"**Sunset:** {weather_data['sys']['sunset']} UTC")
        # st.write(f"**Timezone:** {weather_data['timezone']} s")

        add_city_history(city)
        display_history(st.session_state.city_history)


    except KeyError:
        st.write('Nie ma takiego miasta')
    except Exception as error:
        st.write(error)
