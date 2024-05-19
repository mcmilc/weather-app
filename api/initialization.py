from api.database_api import WeatherDatabaseAPI


def init_db():
    db_api = WeatherDatabaseAPI()
    db_api.drop_tables()
    db_api.create_all_tables()

    db_api.populate_city_type_table()
    db_api.populate_city_table()


if __name__ == "__main__":
    init_db()
