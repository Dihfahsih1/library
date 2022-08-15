from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG=True
ALLOWED_HOSTS=["*"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}