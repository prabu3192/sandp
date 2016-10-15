import itertools
import re

from django.utils import six
try:
    from PIL import Image, ImageChops, ImageFilter
except ImportError:
    import Image
    import ImageChops
    import ImageFilter

from easy_thumbnails import utils


def scale_and_resize(im, size, crop=False, upscale=False, zoom=None, target=None,
                   **kwargs):

    source_x, source_y = [float(v) for v in im.size]
    target_x, target_y = [int(v) for v in size]
	
    im = im.resize((int(target_x),int(target_y)),resample=Image.ANTIALIAS)
    return im
