__author__ = 'mFoxRU'

from PIL import Image


class ImageItem(object):

    def __init__(self, image, align=None, offset=None):
        """
        This class represents individual images stored in ImageSet
        :param image: Image file
        Following image parameters are optional. They override parent values.
        In case of absence parent ImageSet values will be used. Useful when
        images in one imageset have different size
        :param align: See ImageSet description
        :param offset: See ImageSet description
        """
        try:
            self.image = Image.open(image)
        except Exception as e:
            exit('Could not load file "{0}". {1}'.
                 format(image, e))
        self.align = align
        self.offset = offset


class ImageSet(object):
    imagesets = {}
    attributes = {}

    def __init__(self, name, imagesets, attribute=None, parent=None,
                 align=None, offset=None):
        """
        This class contains a set of images that visualises selected attribute.
        :param name: Images set name
        :param imagesets: Dictionary of images, where keys are attribute values
        (i.e. 0, 1) and values are dictionaries of ImageItem __init__
        parameters
        :param attribute: Attribute that is visualised by the current image set
        :param parent: Images set parent object. This parameter is used for
        image positioning. If parent is None then image will be positioned
        against the top left corner
        If parent is not None, the following parameters will be used to
        position image:
        :param align: Determines align point of the parent image. 1 is top left
        pixel (0,0), 2 is top middle pixel, 5 is center, etc. See table for
        reference. When calculating points 2, 4, 5, 6, 8 values a rounded
        down (i.e. 100.5 -> 100)
        :param offset: tuple (X, Y) of int representing offset of top left
        point of image from the parent image align point. Can be negative
        Table:
            1---2---3------> X
            |       |
            4   5   6
            |       |
            7---8---9
            |
            v Y
        """
        if name in self.imagesets:
            exit('Name conflict. Image set "{}" already exists'.format(name))
        self.name = name
        if parent is None:
            self.parent = None
        else:
            if parent in self.imagesets:
                self.parent = self.imagesets[parent]
                self.parent.add_child(self)
            else:
                exit(
                    'Could not find parent "{}" for set "{}". Check if parent'
                    ' exists and is placed before child in template config.'.
                    format(parent, name))
        self.children = None
        if attribute is None:
            if self.attributes:
                self.attribute = len(self.attributes)
            else:
                self.attribute = 0
        else:
            self.attribute = attribute
        if self.attribute not in self.attributes:
            self.attributes[self.attribute] = [self]
        else:
            self.attributes[self.attribute].append(self)
        self.align = align
        self.offset = offset
        self.images = {}
        for image_name, params in imagesets.iteritems():
            self.images[image_name] = ImageItem(**params)
        self.imagesets[name] = self

    def add_child(self, child):
        if self.children is None:
            self.children = [child]
        else:
            self.children.append(child)
