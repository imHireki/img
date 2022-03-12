#!/usr/bin/env python3
from typing import Tuple, Dict, List, Union
from abc import ABC, abstractmethod
from io import BytesIO

import PIL.Image, PIL.ImageSequence

from .exception import ImageSupportError


def open(fp, mode="r", formats=None):
    return PIL.Image.open(fp, mode, formats)

def is_animated(image):
    return getattr(image, 'is_animated', False)


class Image:
    def __init__(self, image, size, format='WEBP', fp=None):
        self.image = image
        self.size = size
        self.format = format
        self.fp = fp

    def resize(self): pass

    def save(self, at):
        """ Save image, on a BytesIO object or path """
        self.img.save(at,
                      format=self.img_format,
                      quality=self.quality,
                      optimize=True)


class Icon(_Image):
    def improve_consistency(self):
        """ Improve the image's consistency to avoid problems
        TODO: call other functions from here, maybe also check the image here
        """

        # Create a white image with the same size as the image
        white_background = PIL.Image.new(
            mode='RGBA',
            size=self.img.size,
            color=(255, 255, 255)
            )

        # Patch the alpha layer with the white_background and convert to RGB
        self.img = PIL.Image.alpha_composite(
            im1=white_background,
            im2=self.img
            ).convert('RGB')

    def resize(self):
        """ Perform the resize of the image """
        self.img = self.img.resize(
            size=self.size,
            resample=self.resample,
            reducing_gap=2.0
            )


class Wallpaper(_Image): pass


class Bulk:
    def __init__(self, objs):
        self.objs = objs

    def resize(self, path=''):
        """ Resize image objects as a batch
        Return its bytes objects, if path is specified, also save it.

        path -- the path for save the image (default: '')
        """
        batch = []

        for obj in self.objs:
            if obj.img.mode == 'RGBA':
                obj.improve_consistency()

            obj.resize()

            if path:
               obj.save('{}{}'.format(path, obj.name))

            bytes_img = BytesIO()
            obj.save(bytes_img)
            batch.append(bytes_img)

        return batch

