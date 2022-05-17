import os

from sqlalchemy import false
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
'''
 Set variable DATABASE_URL before launch application
 Windows : 
 SET DATABASE_URL= "postgresql://<username>:<password>@localhost:5432/<dbname>"
 
 Mac / Linux :
 export DATABASE_URL="postgresql://postgres:Pa553R@localhost:5432/capstone"

'''
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False