from testClass.TestClass import TestClass
from container import Container


class TestClass2:
    def __init__(self, testClass: TestClass, container: Container):
        self.testClass = testClass
        self.container = container
