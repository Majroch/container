import unittest
from container import Container
from testClass.TestClass import TestClass
from testClass.TestClass2 import TestClass2
from testClass.TestClass3 import TestClass3


class ContainerTest(unittest.TestCase):
    def test_package_import(self):
        container = Container()

        self.assertIsInstance(container, Container)

    def test_get_container(self):
        container = Container()

        service = container.get(Container)

        self.assertIsNotNone(service)
        self.assertIsInstance(service, Container)
        self.assertEqual(service, container)

    def test_get_test_class(self):
        container = Container({
            'param2': 'someData'
        })

        service = container.get(TestClass)

        self.assertIsNotNone(service)
        self.assertIsInstance(service, TestClass)
        self.assertEqual(service.param1, container)
        self.assertEqual(service.param2, 'someData')
        self.assertEqual(service.param3, None)
        self.assertEqual('something', service.do_something())

    def test_get_class_with_multiple_classes(self):
        container = Container({
            'param2': 'someData'
        })

        service = container.get(TestClass2)

        self.assertIsNotNone(service)
        self.assertIsInstance(service, TestClass2)
        self.assertEqual(service.container, container)
        self.assertIsInstance(service.testClass, TestClass)
        self.assertEqual('something', service.testClass.do_something())

    def test_get_class_without_documentation(self):
        container = Container({
            'test': 'test'
        })

        service = container.get(TestClass3)

        self.assertIsNotNone(service)
        self.assertIsInstance(service, TestClass3)
        self.assertEqual(service.container, container)
        self.assertEqual(service.test, 'test')

    def test_set_param(self):
        container = Container()

        container.set('test', 'test')

        self.assertEqual(container.get('test'), 'test')

    def test_set_class(self):
        container = Container()

        container.set('container2', container)

        self.assertEqual(container.get('container2'), container)

    def test_set_class_as_typeof(self):
        container = Container()
        newClass = TestClass3(container, 'test')

        container.set(type(newClass), newClass)

        self.assertEqual(container.get(TestClass3), newClass)


if __name__ == '__main__':
    unittest.main()
