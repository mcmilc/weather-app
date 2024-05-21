from setuptools import setup
from setuptools import find_namespace_packages

setup(
    name="WeatherAppPackages",
    version="0.1",
    packages=find_namespace_packages(include=["api", "api.*", "config", "config.*"]),
    include_package_data=True,
    package_data={
        "api": ["queries/*.sql"],
        "config": ["*.json"],
    },
    install_requires=[],  # Add any dependencies if needed
    author="MC Milc",
    author_email="mcmilc@mail.com",
    description="Project description",
)
