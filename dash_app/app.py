import datetime as dt
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
from api.database_api import WeatherDatabaseAPI
from config.utilities import tuples_to_dataframe

app = dash.Dash(
    __name__, external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"]
)

weather_api = WeatherDatabaseAPI()


def fetch_current_weather(city):
    """Fetch the current weather data for a given city."""
    city_data = weather_api.fetch_current_weather(city)
    return {
        "city": city,
        "temperature": city_data["temperature"],
        "humidity": city_data["humidity"],
        "wind_speed": city_data["wind_speed"],
    }


def fetch_average_temperature_data(city, start_year, end_year):
    temp_data = weather_api.fetch_average_temperatures(
        city, start_date=f"{start_year}-01-01", end_date=f"{end_year}-12-31"
    )
    temp_df = tuples_to_dataframe(temp_data, columns=["date", "avg_temperature"])
    return temp_df


def fetch_average_wind_data(city, start_year, end_year):
    wind_data = weather_api.fetch_average_wind_speeds(
        city, start_date=f"{start_year}-01-01", end_date=f"{end_year}-12-31"
    )
    wind_df = tuples_to_dataframe(wind_data, columns=["date", "avg_wind_speed"])
    return wind_df


def fetch_forecast_data(city):
    forecast_data = weather_api.fetch_forecasted_weather(city)
    fc_df = tuples_to_dataframe(forecast_data, columns=list(forecast_data[0].keys()))
    return fc_df


def determine_tick_spacing(start_year, end_year):
    # start_year = dt.datetime.strptime(start_year, "%Y").year
    # end_year = dt.datetime.strptime(end_year, "%Y").year
    years_diff = end_year - start_year
    if years_diff > 50:
        return "M60"  # every 5 years
    elif years_diff > 20:
        return "M24"  # every 2 years
    else:
        return "M12"  # every year


def generate_current_weather_card(city, temperature, humidity, wind_speed):
    return html.Div(
        className="card",
        children=[
            html.H3(city),
            html.P(f"Temperature: {temperature}°C"),
            html.P(f"Humidity: {humidity}%"),
            html.P(f"Wind Speed: {wind_speed} km/h"),
        ],
    )


def plot_average_daily_temperature(data, start_year, end_year):
    tick_spacing = determine_tick_spacing(start_year, end_year)
    fig = px.line(
        data,
        x="date",
        y="avg_temperature",
        title="Historical Average Temperature",
        labels={"date": "Date", "avg_temperature": "Average Temperature (°C)"},
    )
    fig.update_xaxes(dtick=tick_spacing)  # set dynamic tick spacing
    return dcc.Graph(figure=fig)


def plot_average_wind_speed(data, start_year, end_year):
    tick_spacing = determine_tick_spacing(start_year, end_year)
    fig = px.line(
        data,
        x="date",
        y="avg_wind_speed",
        title="Historical Average Wind Speed",
        labels={"date": "Date", "avg_wind_speed": "Average Wind Speed (km/h)"},
    )
    fig.update_xaxes(dtick=tick_spacing)  # set dynamic tick spacing
    return dcc.Graph(figure=fig)


def generate_forecast_cards(forecast_data):
    return html.Div(
        [
            html.Div(
                [
                    html.H4(f"Date: {day[1]['date']}"),
                    html.P(f"Temp: {day[1]['temperature']} °C"),
                    html.P(f"Precipitation: {day[1]['precipitation']} mm"),
                    html.P(f"Wind: {day[1]['wind_speed_10m']} km/h"),
                ]
            )
            for day in forecast_data.iterrows()
        ],
        className="forecast-container",
    )


app.layout = html.Div(
    children=[
        html.H1("Weather Dashboard"),
        dcc.Dropdown(
            id="city-dropdown",
            options=[
                {"label": city, "value": city}
                for city in ["Manhattan Beach", "Hawthorne", "Redondo Beach"]
            ],
            value="Manhattan Beach",
        ),
        html.Div(id="current-weather-display"),
        html.Div(id="temperature-graph"),
        html.Div(id="wind-speed-graph"),
        html.Div(id="forecast-display"),
        dcc.Input(id="start-year", type="number", value=2010),
        dcc.Input(id="end-year", type="number", value=2011),
    ]
)


@app.callback(
    [
        Output("current-weather-display", "children"),
        Output("temperature-graph", "children"),
        Output("wind-speed-graph", "children"),
        Output("forecast-display", "children"),
    ],
    [
        Input("city-dropdown", "value"),
        Input("start-year", "value"),
        Input("end-year", "value"),
    ],
)
def update_dashboard(city, start_year, end_year):
    current_weather = fetch_current_weather(city)
    temp_data = fetch_average_temperature_data(
        city, start_year=start_year, end_year=end_year
    )
    wind_data = fetch_average_wind_data(city, start_year=start_year, end_year=end_year)
    forecast_data = fetch_forecast_data(city)
    return (
        generate_current_weather_card(**current_weather),
        plot_average_daily_temperature(
            temp_data, start_year=start_year, end_year=end_year
        ),
        plot_average_wind_speed(wind_data, start_year=start_year, end_year=end_year),
        generate_forecast_cards(forecast_data),
    )


if __name__ == "__main__":
    app.enable_dev_tools(debug=True)
    app.run_server(debug=True)
