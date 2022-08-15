class dict_contains(dict):
    def __eq__(self, other: dict):
        return self.items() <= other.items()


def is_method_exists(obj, method):
    return hasattr(obj, method) and callable(getattr(obj, method))
