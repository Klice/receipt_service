class dict_contains(dict):
    def __eq__(self, other: dict):
        return self.items() <= other.items()
