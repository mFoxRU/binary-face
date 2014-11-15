__author__ = 'mFoxRU'

import operator

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
        if self.image.mode != 'RGBA':
            self.image = self.image.convert('RGBA')
        self.width, self.height = self.image.size
        self.align = align
        self.offset = offset

    @property
    def has_align(self):
        return True if self.align is not None else False

    @property
    def has_offset(self):
        return True if self.offset is not None else False


class ImageSet(object):
    imagesets = {}
    attributes = {}
    composed = {}

    # x is ImageSet object, y is ImageItem name (in ImageSet.imagesets dict)
    _align_formula = {
        1: lambda x, y: (0,                     0),
        2: lambda x, y: (x.images[y].width/2,   0),
        3: lambda x, y: (x.images[y].width-1,   0),
        4: lambda x, y: (0,                     x.images[y].height/2),
        5: lambda x, y: (x.images[y].width/2,   x.images[y].height/2),
        6: lambda x, y: (x.images[y].width-1,   x.images[y].height/2),
        7: lambda x, y: (0,                     x.images[y].height-1),
        8: lambda x, y: (x.images[y].width/2,   x.images[y].height-1),
        9: lambda x, y: (x.images[y].width-1,   x.images[y].height-1),
    }

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
        image positioning. If parent is None then image's top left corner will
        be positioned at (0, 0)
        If parent is not None, the following parameters will be used to
        position image:
        :param align: Determines align point of the parent image. 1 is top left
        pixel (0,0), 2 is top middle pixel, 5 is center, etc. See table for
        reference. When calculating points 2, 4, 5, 6, 8 values a rounded
        up (i.e. 100.5 -> 101)
        :param offset: tuple (X, Y) of int representing offset of top left
        point of image from the parent image align point. Can be negative.
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
            else:
                exit(
                    'Could not find parent "{}" for set "{}". Check if parent'
                    ' exists and is placed before child in template config.'.
                    format(parent, name))
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

    def offset_from_parent(self, values):
        """
        Calculates image offset from parent top-left edge
        :param values: List of values for current image
        :return: Tuple of [X, Y] offset
        """
        if self.parent is None:
            return [0, 0]

        # Calculate align point coordinates
        value = values[self.attribute]
        parent_value = values[self.parent.attribute]
        if self.images[value].has_align:
            align = self.images[value].align
        elif self.align is not None:
            align = self.align
        else:
            align = 1
        formula = self._align_formula[int(align)]
        align_point = formula(self.parent, parent_value)

        # Calculate coordinates with offset from align point
        if self.images[value].has_offset:
            offset = map(operator.add, align_point, self.images[value].offset)
        elif self.offset is not None:
            offset = map(operator.add, align_point, self.offset)
        else:
            offset = align_point
        return offset

    def calculate(self, values):
        """
        Calculates image coordinates
        :param values: List of values for current image
        """
        if self.parent is not None and self.parent.name not in self.composed:
            self.parent.calculate(values)

        # Top-left coordinates are used for positioning
        top_left = self.offset_from_parent(values)

        # Bottom-right coordinates are used co calculate final image size
        value = values[self.attribute]
        bottom_right = [
            top_left[0] + self.images[value].width - 1,
            top_left[1] + self.images[value].height - 1,
        ]
        self.composed[self.name] = [top_left, bottom_right]

    @classmethod
    def make_image(cls, values, fill_value, filename):
        if len(cls.imagesets) < len(values):
            exit('Not enough attributes in template to visualize data')
        elif len(cls.imagesets) > len(values):
            attr_max = max(cls.attributes.iterkeys())
            values.extend([fill_value for _ in xrange(attr_max-len(values)+1)])
        cls.composed = {}
        if not cls.imagesets:
            exit('No imagesets loaded')
        for name, imageset in cls.imagesets.iteritems():
            if name not in cls.composed:
                imageset.calculate(values)

        fnd = lambda x, y: (v[x][y] for v in cls.composed.itervalues())
        # Adjust images coordinates so that final image will be positioned
        # against the top-left side
        adjust = [min(fnd(0, 0)), min(fnd(0, 1))]
        image_size = [max(fnd(1, 0))-adjust[0]+1, max(fnd(1, 1))-adjust[1]+1]
        image = Image.new('RGBA', image_size)
        for name, imageset in cls.imagesets.iteritems():
            image.paste(
                imageset.images[values[imageset.attribute]].image,
                (
                    cls.composed[name][0][0] - adjust[0],
                    cls.composed[name][0][1] - adjust[1]
                ),
                imageset.images[values[imageset.attribute]].image
            )
        image.save(filename+'.png')