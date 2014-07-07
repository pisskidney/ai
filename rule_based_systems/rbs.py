#!/usr/bin/python


class Concepts():
    def __init__(self, name, value=None, operator=None):
        ''' Initializes the Concept.

        Example concept: name=temperature, value=30, operator=lt, eq, gte etc.
        A value without an operator does not make sense so both or none
        must be present.
        '''
        self.name = name
        if value:
            self.value = value
            self.operator = operator


def main():
    pass


if __name__ == "__main__":
    main()
