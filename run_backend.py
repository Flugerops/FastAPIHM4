from uvicorn import run as run_asgi

from backend import app
from backend.db import tasks_db


if __name__ == "__main__":
    tasks_db.migrate()
    run_asgi(app=app, port=8134)
