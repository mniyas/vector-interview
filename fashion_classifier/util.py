"""Utility functions for classifier module."""
from io import BytesIO
from pathlib import Path
from typing import Union
import base64
import random
import string

from PIL import Image


def read_image_pil(image_uri: Union[Path, str], grayscale=False) -> Image:
    with open(image_uri, "rb") as image_file:
        return read_image_pil_file(image_file, grayscale)


def read_image_pil_file(image_file, grayscale=False) -> Image:
    with Image.open(image_file) as image:
        if grayscale:
            image = image.convert(mode="L")
        else:
            image = image.convert(mode=image.mode)
        return image


def read_b64_image(b64_string, grayscale=False):  # pylint: disable=unused-argument
    """Load base64-encoded images."""
    try:
        _, b64_data = b64_string.split(",")  # pylint: disable=unused-variable
        image_file = BytesIO(base64.b64decode(b64_data))
        return read_image_pil_file(image_file, grayscale)
    except Exception as exception:
        raise ValueError("Could not load image from b64 {}: {}".format(b64_string, exception)) from exception


def image_to_byte_array(image: Image) -> bytes:
    # BytesIO is a fake file stored in memory
    imgByteArr = BytesIO()
    # image.save expects a file as a argument, passing a bytes io ins
    image.save(imgByteArr, format="PNG")
    # Turn the BytesIO object back into a bytes object
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


def byte_array_to_image(byte_array: bytes) -> Image:
    # BytesIO is a fake file stored in memory
    imgByteArr = BytesIO(byte_array)
    # image.save expects a file as a argument, passing a bytes io ins
    img = Image.open(imgByteArr)
    return img


def get_random_id():
    # create random id
    id = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return id
