#!/bin/sh

# Initialize the database
python -u init_db.py

# Start the Flask application
flask run --debug --host=0.0.0.0 --port=5000