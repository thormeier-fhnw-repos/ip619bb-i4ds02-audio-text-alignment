class Struct:
    """
    Class to convert dicts back to object-like structures again,
    see https://stackoverflow.com/a/1305663/2115232
    """

    def __init__(self, **entries):
        """
        Constructor, updates an internal properties dict
        :param entries:
        """
        self.__dict__.update(entries)
