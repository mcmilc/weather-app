from api.connection import DatabaseConnection


def load_query(file_path):
    """Read an SQL query from a file."""
    with open(file_path, "r") as sql_file:
        return sql_file.read()


class WeatherDatabaseAPI:
    def __init__(self, db_type="postgresql"):
        """Initialize the database API with the selected database type."""
        self.db = DatabaseConnection(db_type)

    def get_city_by_name(self, city_name):
        """Fetch city information by name using a SQL file."""
        query = load_query("api/queries/fetch_city_by_name.sql")
        session = self.db.get_session()
        try:
            result = session.execute(query, {"city_name": city_name}).fetchone()
            return result
        finally:
            session.close()

    def create_all_tables(self):
        query = load_query("api/queries/create_all_tables.sql")
        session = self.db.get_session()
        try:
            result = session.execute(query).fetchone()
            return result
        finally:
            session.close()

    def flush_all_tables(self):
        query = load_query("api/queries/flush_all_tables.sql")
        session = self.db.get_session()
        try:
            result = session.execute(query).fetchone()
            return result
        finally:
            session.close()

    def insert_historical_weather(
        self, city_name, date, temperature, precipitation, humidity, wind_speed
    ):
        """Insert a historical weather entry into the database using a SQL file."""
        query = load_query("api/queries/insert_historical_weather.sql")
        session = self.db.get_session()
        try:
            session.execute(
                query,
                {
                    "name": city_name,
                    "date": date,
                    "temperature": temperature,
                    "precipitation": precipitation,
                    "wind_speed": wind_speed,
                },
            )
            session.commit()
        finally:
            session.close()

    def insert_current_weather(
        self, city_name, timestamp, temperature, precipitation, humidity, wind_speed
    ):
        """Insert a current weather entry into the database using an SQL file."""
        query = load_query("api/queries/insert_current_weather.sql")
        session = self.db.get_session()
        try:
            session.execute(
                query,
                {
                    "name": city_name,
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
        self, city_name, forecast_date, temperature, precipitation, humidity, wind_speed
    ):
        """Insert a forecasted weather entry into the database using an SQL file."""
        query = load_query("api/queries/insert_forecasted_weather.sql")
        session = self.db.get_session()
        try:
            session.execute(
                query,
                {
                    "name": city_name,
                    "forecast_date": forecast_date,
                    "temperature": temperature,
                    "precipitation": precipitation,
                    "wind_speed": wind_speed,
                },
            )
            session.commit()
        finally:
            session.close()


if __name__ == "__main__":
    api = WeatherDatabaseAPI()
    api.create_all_tables()
