from setuptools import setup
from setuptools import find_namespace_packages

setup(
    name="WeatherAppPackages",
    version="0.1",
    packages=find_namespace_packages(
        include=[
            "databaseapi",
            "databaseapi.*",
            "weatherapi",
            "weatherapi.*",
            "config",
            "config.*",
        ]
    ),
    include_package_data=True,
    package_data={
        "config": ["*.json"],
        "databaseapi": ["queries/*.sql"],
        "weatherapi": ["*.json"],
    },
    install_requires=[],
    author="MC Milc",
    author_email="mcmilc@mail.com",
    description="Database, Weather APIs and Configuration Readers",
)
