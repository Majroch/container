import inspect


class Container:
    TYPES_AS_PARAMS: list = [
        int,
        str,
        tuple,
        list,
        float,
        bool,
    ]

    def __init__(self, services: dict = None):
        if services is None:
            services = {}

        services[type(self)] = self
        services['container'] = self
        self.services = services

    def _is_builtin_type(self, _type: inspect.Parameter) -> bool:
        for builtin in self.TYPES_AS_PARAMS:
            if _type.annotation == builtin or _type.annotation == _type.empty:
                return True

        return False

    def get(self, _classType) -> object | None:
        if _classType in self.services.keys():
            return self.services.get(_classType)

        if not inspect.isclass(_classType):
            return None

        # Initialize class that does not exist in current services tuple
        signature = inspect.signature(_classType.__init__)

        params = []
        for param in signature.parameters.keys():
            if param == 'self':
                continue

            sig = signature.parameters.get(param)

            if self._is_builtin_type(sig):
                # Builtin type, like str, list, tuple, int, etc...
                # Try to retrieve value for it from container by param name
                autowireParam = self.get(sig.name)
            else:
                # Get class type from container
                autowireParam = self.get(sig.annotation)

            if autowireParam is None:
                if sig.default == inspect.Parameter.empty:
                    raise Exception(
                        'Cannot autowire argument "{}" with type "{}" to class "{}". This parameter does not exists.'
                        .format(
                            sig.name,
                            sig.annotation,
                            _classType
                        )
                    )

                autowireParam = sig.default

            params.append(autowireParam)

        return _classType(*params)

    def set(self, key, value) -> None:
        if key in self.services.keys():
            raise Exception(
                'Cannot redeclare "{}"'.format(
                    key
                )
            )

        self.services[key] = value
