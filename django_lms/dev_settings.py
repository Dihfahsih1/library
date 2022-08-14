from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent


DEBUG=True#This is to ensure that the server does not the db of the live server
ALLOWED_HOSTS=["*"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}