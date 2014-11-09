__author__ = 'mFoxRU'

from PIL import Image


class ImageItem(object):

    def __init__(self, image_file, align=None, align_point=None, offset=None):
        """
        This class represents individual images stored in ImageSet
        :param image_file: Image file
        Following image parameters are optional. They override parent values.
        In case of absence parent ImageSet values will be used. Useful when
        images in one imageset have different size
        :param align:
        :param align_point:
        :param offset: tuple of (x, y)
        """
        try:
            self.image = Image.open(image_file)
        except Exception as e:
            exit('Could not load file "{0}". {1}'.
                 format(image_file, e))
        self.align = align
        self.align_point = align_point
        self.offset = offset


class ImageSet(object):
    imagesets = {}
    attributes = []

    def __init__(self, name, parent=None, attribute=None):
        """
        This class contains a set of images that visualises selected attribute.
        :param name: Images set name
        :param parent: Images set parent name. This parameter is used for
        image positioning. If parent is None then image will be positioned
        to the top left corner
        :param attribute: Attribute that is visualised by the current image set
        """
        if name in self.imagesets:
            exit('Name conflict. Image set "{}" already exists'.format(name))
        self.name = name
        self.parent = parent
        if attribute is not None:
            self.attribute = attribute
        else:
            if len(self.attributes):
                self.attribute = max(self.attributes) + 1
            else:
                self.attribute = 0
        if self.attribute not in self.attributes:
            self.attributes.append(self.attribute)

        self.imagesets[name] = self