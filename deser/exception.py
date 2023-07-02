class InvalidArrayInitializer(Exception):
    def __init__(self, expected: int, actual: int) -> None:
        super().__init__(f'Attempt to initialize array of size {expected} with sequence of size {actual}')
