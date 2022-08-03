from container import Container


class TestClass:
    def __init__(self, param1: Container, param2: str, param3: str = None):
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3

    @staticmethod
    def do_something() -> str:
        return 'something'
