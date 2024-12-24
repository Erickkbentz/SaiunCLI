
class AuraContext:
    def __init__(
            self,
            **kwargs,
    ):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return f"Context({self.__dict__})"