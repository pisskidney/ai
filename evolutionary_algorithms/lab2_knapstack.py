#!/usr/bin/python
import random


class Population:
    def __init__(self, size, alg, init=True):
        '''Initialize the population'''
        self.individuals = list()
        self.algorithm = alg
        self.generation = 1
        self.size = size
        if init:
            for i in range(size):
                self.individuals.append(Individual(alg))
            print 'Population initialized with: '
            for i in self.individuals:
                print ''.join([str(x) for x in i.genotype])

    @property
    def fittest(self):
        return sorted(self.individuals, key=lambda i: i.fitness).pop()


class Individual:
    def __init__(self, algorithm, init=True):
        '''Initialize an individual'''
        self.genotype = list()
        if init:
            self.genotype = algorithm.generate_genotype()
        self.algorithm = algorithm

    @property
    def fitness(self):
        return self.algorithm.calculate_fitness(self.genotype)


class Algorithm():
    tournament_size = 3
    crossover_uniformity = 0.5
    mutation_rate = 0.05

    sack = 50  # 20 Kg

    def __init__(self, data):
        self.nr_genes = len(data)
        self.data = data

    def selection(self, population):
        #Tournament selection
        tournament_pop = Population(
            self.tournament_size, self, init=False
        )
        old_pop = list(population.individuals)
        random.shuffle(old_pop)
        for i in range(self.tournament_size):
            tournament_pop.individuals.append(old_pop.pop())
        return tournament_pop.fittest

    def evolve(self, population):
        new_pop = Population(population.size, self, init=False)
        for i in range(population.size):
            i1 = self.selection(population)
            i2 = self.selection(population)
            new_i = self.crossover(i1, i2)
            new_i.genotype = self.mutate(new_i.genotype)
            new_pop.individuals.append(new_i)
        return new_pop

    def crossover(self, i1, i2):
        #Uniform crossover
        new_i = Individual(self, init=False)
        for i in range(self.nr_genes):
            if random.random() < self.crossover_uniformity:
                new_i.genotype.append(i1.genotype[i])
            else:
                new_i.genotype.append(i2.genotype[i])
        return new_i

    def mutate(self, genes):
        new_genes = [
            gene if random.random() > self.mutation_rate
            else 1 ^ gene for gene in genes
        ]

        return new_genes

    def generate_genotype(self):
        return [random.randint(0, 1) for i in range(self.nr_genes)]

    def calculate_fitness(self, genes):
        '''Calculates the fitness of the individual.'''
        weight = 0
        price = 0
        for index, gene in enumerate(genes):
            if gene == 1:
                price += self.data[index][1]
                weight += self.data[index][0]
        return price if weight <= self.sack else 0


def get_input():
    jewelery = list()
    print 'Enter a weight of 0 to stop.'
    while(1):
        w = raw_input('Please enter weight of jewelery: ')
        if w == '0':
            break
        p = raw_input('Price: ')
        jewelery.append((int(w), int(p)))
    return jewelery


def main():
    data = get_input()

    algo = Algorithm(data)
    p = Population(10, algo)

    generation = 1

    while(generation < 100):
        print 'Generation: %s, Fitness: %s, Genes: %s' % (
            str(generation), str(p.fittest.fitness),
            ''.join([str(gene) for gene in p.fittest.genotype])
        )
        generation += 1
        p = algo.evolve(p)


if __name__ == "__main__":
    main()
