from functools import wraps
from typing import Callable


class Utils:

    @staticmethod
    def singleton(cls):
        instance = None

        class Wrapper(cls):
            def __new__(cls_, *args, **kwargs):
                nonlocal instance
                if instance is None:
                    instance = super().__new__(cls_, *args, **kwargs)
                else:
                    raise Exception(f"Instance of {cls.__name__} already created")
                return instance

        return Wrapper
