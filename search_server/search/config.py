"""Insta485 development configuration."""


import pathlib


# Added based on the p5 spec
SEARCH_INDEX_SEGMENT_API_URLS = [
    "http://localhost:9000/api/v1/hits/",
    "http://localhost:9001/api/v1/hits/",
    "http://localhost:9002/api/v1/hits/",
]

#Copied from the p2 project, may need to change later
# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'


# Secret key for encrypting cookies
SECRET_KEY = b'\xc3\n>\xe7)\xfe#\xf3N\x83\x89\xc1\xd6\
x89\xae4\xd0L\x9aI\x0e\xa6\xd2P'
SESSION_COOKIE_NAME = 'login'


# File Upload to var/uploads/
SEARCH_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = SEARCH_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024


# Database file is var/insta485.sqlite3
DATABASE_FILENAME = SEARCH_ROOT/'var'/'search.sqlite3'
