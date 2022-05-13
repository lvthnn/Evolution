import random


class Organism:
    GT_DOMINANT = "F"
    REPRODUCTION_TIME = 2
    MUTATION_CHANCE = 0.025
    MAX_AGE = 6

    def __init__(self, genotype="f", phenotype="", fitness=0, age=0, reproduction_timer = 6):
        self._genotype = genotype
        self._phenotype = phenotype
        self._fitness = fitness
        self._age = age
        self._reproduction_timer = reproduction_timer

    def introduce_mutants(self, chance):
        """ Determines whether an individual carries the recessive or dominant genotype.
        Chance parameter is passed in to allow for percentage of population to carry specific 
        genotype."""
        if chance >= random.random():
            self._genotype = self.GT_DOMINANT

    def calc_fitness(self):
        """ Only used for individuals making up initial population.
        Calculates individual fitness based on genotype. Individuals
        with dominant genotype acquire a boost to their fitness variable."""
        if self._genotype == self.GT_DOMINANT:
            self._phenotype = "Dominant"

            if random.random() > 0.5:
                fitness = 1 + random.random()
            else:
                fitness = 1 - random.uniform(0.0, 0.1)

        else:
            self._phenotype = "Recessive"

            if random.random() < 0.5:
                fitness = 0.5 + random.uniform(0.0, 0.3)
            else:
                fitness = 0.5 - random.uniform(0.0, 0.3)

        self._fitness = fitness

    def survives_check(self, difficulty):
        """ Check whether an individual survives exposure to enviromental factor. 
        Determined by evaluating whether that individuals fitness value is greater 
        than the numeric value of the difficulty of the environmental factor."""
        return self._fitness >= difficulty

    def reproduce(self):
        """An organism reproduces and passes on genes to offspring. """
        if self._reproduction_timer >= self.REPRODUCTION_TIME:
            self._reproduction_timer = 0
            dice = random.random()

            if dice <= self.MUTATION_CHANCE:  # beneficial mutation of individual during reproduction
                passed_on_fitness = self._fitness + random.uniform(0, 0.1)
            elif dice >= 1 - self.MUTATION_CHANCE:
                passed_on_fitness = self._fitness - random.uniform(0, 0.1)
            else:
                passed_on_fitness = self._fitness
            offspring = Organism(
                self._genotype, self._phenotype, passed_on_fitness, 0)
            return offspring
        return False
