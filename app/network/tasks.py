from main.celery import app
from network.utils import ConnectNetwork


@app.task
def connect_network() -> None:
    ConnectNetwork().connect_all()
