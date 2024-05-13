from api.database_api import WeatherDatabaseAPI

db_api = WeatherDatabaseAPI()
db_api.drop_tables()
db_api.create_all_tables()

db_api.populate_city_type_table()
db_api.populate_city_table()
