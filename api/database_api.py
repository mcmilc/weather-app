from api.connection import DatabaseConnection
from config.settings import load_query
from config.settings import load_cities


class WeatherDatabaseAPI:
    """API for interacting with the weather database."""

    def __init__(self, db_type="postgresql"):
        """Initialize the database API with the selected database type."""
        self.db = DatabaseConnection(db_type)

    def drop_tables(self):
        """Drop all tables in the database using an SQL file."""
        query = load_query("api/queries/delete_tables.sql")
        session = self.db.get_session()
        try:
            session.execute(query)
            session.commit()
        finally:
            session.close()

    def get_city_type_id(self, city_type):
        """Fetch all city types from the database using an SQL file."""
        query = load_query("api/queries/fetch_city_type.sql")
        session = self.db.get_session()
        try:
            result = session.execute(query, {"city_type": city_type}).fetchall()
            return result
        finally:
            session.close()

    def get_city_data(self, city_name):
        """Fetch city information by name using a SQL file."""
        query = load_query("api/queries/fetch_city_by_name.sql")

        session = self.db.get_session()
        try:
            result = session.execute(query, {"city_name": city_name}).fetchone()
        finally:
            session.close()
        return result

    def create_all_tables(self):
        """Create all tables in the database using an SQL file."""
        query = load_query("api/queries/create_tables.sql")
        session = self.db.get_session()
        try:
            session.execute(query)
            session.commit()
        finally:
            session.close()

    def flush_all_tables(self):
        """Flush all tables in the database using an SQL file."""
        query = load_query("api/queries/flush_all_tables.sql")
        session = self.db.get_session()
        try:
            session.execute(query)
            session.commit()
        finally:
            session.close()

    def insert_daily_historical_weather(
        self,
        city_name,
        date,
        temperature_max,
        temperature_min,
        temperature_avg,
        precipitation_sum,
        wind_speed_max,
    ):
        """Insert a historical weather entry into the database using a SQL file."""
        query = load_query("api/queries/insert_daily_historical_weather.sql")
        session = self.db.get_session()
        city_id = self.get_city_data(city_name)[0]
        try:
            session.execute(
                query,
                {
                    "city_id": city_id,
                    "date": date,
                    "temperature_min": temperature_min,
                    "temperature_max": temperature_max,
                    "temperature_avg": temperature_avg,
                    "precipitation_sum": precipitation_sum,
                    "wind_speed_max": wind_speed_max,
                },
            )
            session.commit()
        except Exception as e:
            if "UniqueViolation" not in str(e):
                print(f"Error inserting city: {city_name}")
                print(e)
        finally:
            session.close()

    def insert_hourly_historical_weather(
        self,
        city_name,
        timestamp,
        temperature,
        precipitation,
        humidity,
        wind_speed_10m,
    ):
        """Insert a historical weather entry into the database using a SQL file."""
        query = load_query("api/queries/insert_hourly_historical_weather.sql")
        session = self.db.get_session()
        city_id = self.get_city_data(city_name)[0]
        try:
            session.execute(
                query,
                {
                    "city_id": city_id,
                    "timestamp": timestamp,
                    "temperature": temperature,
                    "humidity": humidity,
                    "precipitation": precipitation,
                    "wind_speed_10m": wind_speed_10m,
                },
            )
            session.commit()
        except Exception as e:
            if "UniqueViolation" not in str(e):
                print(f"Error inserting city: {city_name}")
                print(e)
        finally:
            session.close()

    def data_quality_check_historical_weather_hourly(self):
        """Check the data quality of the hourly historical weather data."""
        query = load_query(
            "api/queries/check_historical_weather_hourly_time_inteval.sql"
        )
        session = self.db.get_session()
        try:
            result = session.execute(query).fetchall()
            return result
        finally:
            session.close()

    def insert_current_weather(
        self, city_name, timestamp, temperature, precipitation, humidity, wind_speed
    ):
        """Insert a current weather entry into the database using an SQL file."""
        query = load_query("api/queries/insert_current_weather.sql")
        session = self.db.get_session()
        city_id = self.get_city_data(city_name)[0]
        try:
            session.execute(
                query,
                {
                    "city_id": city_id,
                    "timestamp": timestamp,
                    "temperature": temperature,
                    "precipitation": precipitation,
                    "humidity": humidity,
                    "wind_speed": wind_speed,
                },
            )
            session.commit()
        finally:
            session.close()

    def insert_forecasted_weather(
        self, city_name, date, temperature, precipitation, wind_speed
    ):
        """Insert a forecasted weather entry into the database using an SQL file."""
        query = load_query("api/queries/insert_daily_forecasted_weather.sql")
        session = self.db.get_session()
        city_id = self.get_city_data(city_name)[0]
        try:
            session.execute(
                query,
                {
                    "city_id": city_id,
                    "date": date,
                    "temperature": temperature,
                    "precipitation": precipitation,
                    "wind_speed_10m": wind_speed,
                },
            )
            session.commit()
        finally:
            session.close()

    def populate_city_table(self):
        """Insert all city data into db."""
        cities = load_cities()
        query = load_query("api/queries/insert_city.sql")
        for city in cities:
            session = self.db.get_session()
            city_type_id = self.get_city_type_id(city["type"])
            try:
                session.execute(
                    query,
                    {
                        "name": city["name"],
                        "latitude": city["latitude"],
                        "longitude": city["longitude"],
                        "city_type_id": city_type_id[0][0],
                    },
                )
                session.commit()
            except Exception as e:
                if "UniqueViolation" in str(e):
                    continue
                print(f"Error inserting city: {city['name']}")
                print(e)

            finally:
                session.close()

    def populate_city_type_table(self):
        """Insert all city types into db."""
        cities = load_cities()
        query = load_query("api/queries/insert_city_type.sql")
        for city in cities:
            session = self.db.get_session()
            try:
                session.execute(query, {"city_type": city["type"]})
                session.commit()
            except Exception as e:
                if "UniqueViolation" in str(e):
                    continue
                print(f"Error inserting city type: {city['type']}")
                print(e)
            finally:
                session.close()

    def fetch_current_weather(self, city_name):
        """Fetch current weather for a given city."""
        query = load_query("api/queries/fetch_current_weather.sql")
        session = self.db.get_session()
        city_id = self.get_city_data(city_name)[0]
        try:
            result = session.execute(query, {"city_id": city_id}).fetchone()
            return result
        finally:
            session.close()

    def fetch_forecasted_weather(self, city_name):
        """Fetch forecasted weather for a given city."""
        query = load_query("api/queries/fetch_daily_forecasted_weather.sql")
        session = self.db.get_session()
        city_id = self.get_city_data(city_name)[0]
        try:
            result = session.execute(query, {"city_id": city_id}).fetchall()
            return result
        finally:
            session.close()

    def fetch_historical_temperatures(self, city_name, start_date, end_date):
        """Fetch historical temperatures for a given city."""
        query = load_query("api/queries/fetch_hourly_historical_weather.sql")
        session = self.db.get_session()
        city_id = self.get_city_data(city_name)[0]
        try:
            result = session.execute(
                query,
                {
                    "city_id": city_id,
                    "start_date": start_date,
                    "end_date": end_date,
                },
            ).fetchall()
            return result
        finally:
            session.close()

    def fetch_average_temperatures(self, city_name, start_date, end_date):
        """Fetch average temperatures for a given city."""
        query = load_query("api/queries/fetch_average_temperature.sql")
        session = self.db.get_session()
        city_id = self.get_city_data(city_name)[0]
        try:
            result = session.execute(
                query,
                {
                    "city_id": city_id,
                    "start_date": start_date,
                    "end_date": end_date,
                },
            ).fetchall()
            return result
        finally:
            session.close()

    def fetch_average_wind_speeds(self, city_name, start_date, end_date):
        """Fetch average wind speeds for a given city."""
        query = load_query("api/queries/fetch_average_wind_speed.sql")
        session = self.db.get_session()
        city_id = self.get_city_data(city_name)[0]
        try:
            result = session.execute(
                query,
                {
                    "city_id": city_id,
                    "start_date": start_date,
                    "end_date": end_date,
                },
            ).fetchall()
            return result
        finally:
            session.close()


if __name__ == "__main__":
    api = WeatherDatabaseAPI()
    api.create_all_tables()
