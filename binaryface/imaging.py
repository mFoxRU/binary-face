__author__ = 'mFoxRU'


class ImageSet(object):
    imagesets = {}
    attributes = []

    def __init__(self, name, parent=None, attribute=None):
        """
        ImageSet represents a set of images that visualises selected attribute.
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