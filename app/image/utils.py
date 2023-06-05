from image.models import File, Image


class Cleaner(object):
    """Вспомогательная утилита для очищения медиафайлов из БД"""

    def __init__(self, object_id: int, new_id: int):
        self.object_id = object_id
        self.new_id = new_id

    def delete_image(self):
        image_obj = Image.objects.filter(id=self.object_id).first()
        if image_obj:
            if image_obj.id != self.new_id:
                image_obj.delete()

    def delete_file(self):
        file_obj = File.objects.filter(id=self.object_id).first()
        if file_obj:
            if file_obj.id != self.new_id:
                file_obj.delete()
