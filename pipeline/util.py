from io import BytesIO
import json
import random
import time
import base64
import random
import string
from PIL import Image
from fashion_classifier.util import read_image_pil_file


class BytesEncoder(json.JSONEncoder):
    """JSON encoder for bytes objects."""

    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        return json.JSONEncoder.default(self, obj)


def image_to_base64(image: Image) -> str:
    # BytesIO is a fake file stored in memory
    imgByteArr = BytesIO()
    # image.save expects a file as a argument, passing a bytes io ins
    image.save(imgByteArr, format="PNG")
    # Turn the BytesIO object back into a bytes object
    imgByteArr = imgByteArr.getvalue()
    # Convert the bytes object to a base64 string
    base64_string = base64.b64encode(imgByteArr)
    return base64_string


def read_b64_image(b64_string, grayscale=False):  # pylint: disable=unused-argument
    """Load base64-encoded images."""
    try:
        image_file = BytesIO(base64.b64decode(b64_string))
        return read_image_pil_file(image_file, grayscale)
    except Exception as exception:
        raise ValueError("Could not load image from b64 {}: {}".format(b64_string, exception)) from exception


def get_random_id() -> str:
    """Generate a random id."""
    id = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return id
