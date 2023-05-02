from django.core.exceptions import ValidationError
import os


def validate_file_size(value):
    filesize = value.size

    if filesize > 50485760:
        raise ValidationError("You cannot upload file more than 50Mb")
    else:
        return value


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = [".pdf", ".pptx"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported file extension.")


def validate_image_size(value):
    filesize = value.size

    if filesize > 6485760:
        raise ValidationError("You cannot upload logo more than 6Mb")
    else:
        return value


def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = [".jpg", ".png", "gif"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported logo extension.")
