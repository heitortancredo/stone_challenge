from os import getenv

DATABASE_HOSTNAME = getenv("DATABASE_HOSTNAME", "localhost")
DATABASE_NAME = getenv("DATABASE_NAME", "postgres")
DATABASE_PASSWORD = getenv("DATABASE_PASSWORD", "my_password")
DATABASE_USERNAME = getenv("DATABASE_USERNAME", "user")
