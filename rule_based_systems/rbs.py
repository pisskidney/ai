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
        if self.concept2 is None:
            return bool(self.concept1)
        elif self.operator == 'OR':
            return bool(self.concept1) or bool(self.concept2)
        elif self.operator == 'AND':
            return bool(self.concept1) and bool(self.concept2)
    __nonzero__ = __bool__

    def __str__(self):
        aditional = ''
        if self.concept2 is not None:
            aditional = '%s %s %s %s' % (
                self.operator,
                self.concept2.name,
                self.concept2.operator,
                self.concept2.value
            )
        return 'From %s %s %s %s we deduce that %s %s %s.' % (
            self.concept1.name,
            self.concept1.operator,
            self.concept1.value,
            aditional,
            self.then.name,
            self.then.operator,
            self.then.value,
        )


class KnowledgeBase():
    def __init__(self):
        ''' The class that keeps track of all the rules. '''
        self.rules = list()

    @classmethod
    def from_file(cls, filename):
        ''' We initialize from the facts we get. '''
        new = cls()
        f = open(filename, "r")
        for line in f:
            line = line.rstrip('\n')
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
                r = Rule(c, then_concept)
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

    def print_state(self):
        print '----' * 10
        for _, concept in self.concepts.iteritems():
            print concept.name, concept.operator, concept.value


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
            if self.operator == '=':
                return self.value == cm.concepts[self.name].value
            elif self.operator == '<':
                cmc = cm.concepts[self.name]
                if cmc.operator == '<':
                    return float(self.value) == float(cmc.value)
                return float(self.value) > float(cm.concepts[self.name].value)
            elif self.operator == '>':
                cmc = cm.concepts[self.name]
                if cmc.operator == '>':
                    return float(self.value) == float(cmc.value)
                return float(self.value) < float(cm.concepts[self.name].value)
            elif self.operator == '><':
                l, r = self.value.split(',')
                val = cm.concepts[self.name].value
                return float(l) < float(val) and float(r) > float(val)
            else:
                return False
    __nonzero__ = __bool__


class InferenceEngine():
    def __init__(self, kb, cm, goal, max_inferences=None):
        ''' The main logic handler of the rbs. '''
        self.kb = kb
        self.cm = cm
        self.goal = goal
        self.max_inferences = max_inferences
        self.inferences = 0

    def infer(self):
        if (self.inferences == self.max_inferences):
            raise Exception('Too many inferences!')
        for rule in self.kb.rules:
            if rule:
                print rule
                self.update_fact(rule.then)
                self.kb.rules.remove(rule)

    def update_fact(self, fact):
        if fact.name in self.cm.concepts.keys():
            self.cm.concepts[fact.name].value = fact.value
            self.cm.concepts[fact.name].operator = fact.operator
        else:
            self.cm.concepts[fact.name] = fact


    def done(self):
        return bool(self.goal)


cm = ConceptManager.from_file("facts.txt")


def main():
    kb = KnowledgeBase.from_file("kb.txt")
    goal = Concept('dis', '-1', '>')
    ie = InferenceEngine(kb, cm, goal, max_inferences=10)

    while(not ie.done()):
        ie.infer()
    print 'Conclusion reached!'
    print 'Drip Irrigation System needs to run for %s %s minutes!' % (
        cm.concepts['dis'].operator,
        cm.concepts['dis'].value
    )


if __name__ == "__main__":
    main()
