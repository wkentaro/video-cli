import math

import imgviz


def resize_to_even(image):
    height, width = image.shape[:2]
    height = math.ceil(height / 2) * 2
    width = math.ceil(width / 2) * 2
    image = imgviz.centerize(image, (height, width))
    return image
