from image.utils import Cleaner
from main.celery import app


@app.task
def cleaner(object_image_id: int, new_image_id: int):
    Cleaner(object_image_id, new_image_id).delete_image()


@app.task
def cleaner_file(object_image_id: int, new_image_id: int):
    Cleaner(object_image_id, new_image_id).delete_file()
