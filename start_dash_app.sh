#!/bin/sh
# Initialize the database or any other setup steps
python3 -m api.initialization
# Start the Dash app
python3 -m dash_app.app
