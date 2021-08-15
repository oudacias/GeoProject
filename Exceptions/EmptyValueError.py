class EmptyValueError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.foo = kwargs.get('foo')
