from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import load_db_config


class DatabaseConnection:
    def __init__(self, db_type="postgresql"):
        """Initialize a database connection pool based on the selected type (PostgreSQL/MySQL)."""
        config = load_db_config(db_type)
        if db_type == "postgresql":
            self.db_url = f"postgresql://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
        elif db_type == "mysql":
            self.db_url = f"mysql+pymysql://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

        self.engine = create_engine(self.db_url, pool_size=10, max_overflow=5)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        """Return a new session from the connection pool."""
        return self.Session()

    def close(self):
        """Dispose of the engine."""
        self.engine.dispose()
