#!/usr/bin/python


class Rule():
    pass


class KnowledgeBase():
    pass


class ConceptManager():
    def __init__(self):
        self.concepts = dict()

    @classmethod
    def from_file(cls, filename):
        ''' We initialize from the facts we get. '''
        new = cls()
        f = open(filename, "r")
        for line in f:
            name, operator, value = line.split(' ')
            new.concept[name] = Concept(name, value, operator)
        f.close()
        return new


class Concept():
    def __init__(self, name, value=None, operator=None):
        ''' Initializes the Concept.

        Example concept: name=temperature, value=30, operator='<'. '=' etc.
        A value without an operator does not make sense so both or none
        must be present.
        '''
        self.name = name
        if value:
            self.value = value
            self.operator = operator


def main():
    kb = KnowledgeBase.from_file("kb.txt")
    cm = ConceptManager(kb)


if __name__ == "__main__":
    main()
