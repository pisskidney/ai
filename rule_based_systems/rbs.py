#!/usr/bin/python


class Rule():
    def __init__(self, concept1, then, concept2=None, operator=None):
        ''' Concept can be a Concept or a Rule class that can be cast to
        boolean. Then is the state Concept that results from a true rule.
        '''

        self.concept1 = concept1
        self.concept2 = concept2
        self.operator = operator
        self.then = then

        if concept2 and not operator:
            raise Exception('Error')

    def __bool__(self):
        if not self.concept2:
            return bool(self.concept1)
        elif self.operator == 'OR':
            return bool(self.concept1) or bool(self.concept1)
        elif self.operator == 'AND':
            return bool(self.concept1) and bool(self.concept2)

    __nonzero__ = __bool__


class KnowledgeBase():
    def __init__(self):
        self.rules = list()

    @classmethod
    def from_file(cls, filename):
        ''' We initialize from the facts we get. '''
        new = cls()
        f = open(filename, "r")
        for line in f:
            rule, then = line.split(' THEN ')
            then_name, then_operator, then_value = then.split(' ')
            then_concept = Concept(then_name, then_value, then_operator)

            if rule.find('AND') != -1:
                lrule, rrule = rule.split(' AND ')
                op = 'AND'
            elif rule.find('OR') != -1:
                lrule, rrule = rule.split(' OR ')
                op = 'OR'
            else:
                _, rule_name, rule_operator, rule_value = rule.split(' ')
                c = Concept(rule_name, rule_value, rule_operator)
                r = Rule(c, then)
                new.rules.append(r)
                continue

            _, lrule_name, lrule_operator, lrule_value = lrule.split(' ')
            rrule_name, rrule_operator, rrule_value = rrule.split(' ')

            c1 = Concept(lrule_name, lrule_value, lrule_operator)
            c2 = Concept(rrule_name, rrule_value, rrule_operator)
            r = Rule(c1, then_concept, concept2=c2, operator=op)
            new.rules.append(r)

        return new


class ConceptManager():
    def __init__(self):
        ''' The ConceptManager manages the states of Concepts.'''
        self.concepts = dict()

    @classmethod
    def from_file(cls, filename):
        ''' We initialize from the facts we get. '''
        new = cls()
        f = open(filename, "r")
        for line in f:
            line = line.rstrip('\n')
            name, operator, value = line.split(' ')
            new.concepts[name] = Concept(name, value, operator)
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

    def __bool__(self):
        if self.name not in cm.concepts.keys():
            return False
        else:
            print self.operator
            if self.operator == '=':
                return self.value == cm.concepts[self.name].value
            elif self.operator == '<':
                return float(self.value) < float(cm.concepts[self.name].value)
            elif self.operator == '>':
                return float(self.value) > float(cm.concepts[self.name].value)
            elif self.operator == '><':
                l, r = self.value.split(',')
                val = cm.concepts[self.name].value
                return float(l) < float(val) and float(r) > float(val)
            else:
                return False
    __nonzero__ = __bool__


cm = ConceptManager.from_file("facts.txt")


def main():
    kb = KnowledgeBase.from_file("kb.txt")
    for r in kb.rules:
        print r.concept1.name, ' ', r.concept1.operator, ' ', r.concept1.value
        print bool(r)
        print ''


if __name__ == "__main__":
    main()
