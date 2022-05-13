from organism import Organism

import random
import math

class Population:

    def __init__(self, members, init_genotype_distribution, difficulty, n):
        self._members = members
        self._init_genotype_distribution = init_genotype_distribution
        self._difficulty = difficulty
        self._n = n

        for _ in range(n):
            i = Organism()
            i.introduce_mutants(self._init_genotype_distribution)
            i.calc_fitness()
            i._age = random.randint(0, Organism.MAX_AGE / 2)
            i._reproduction_timer = random.randrange(
                0, i.REPRODUCTION_TIME + 1)
            self._members.append(i)

    def __str__(self):
        """ Return a string representation of population members. """
        result_str = ""
        for i in self._members:
            result_str += "Organism [GT] %s [PT] %s | Fitness: %.2f | Age: %s \n" % (
                i._genotype, i._phenotype, i._fitness, i._age)
        return result_str

    def check_population(self, difficulty, percent):
        """ Expose a population to an environmental factor. Difficulty is a numeric value ranging from 0 and up
        so that if an individual's fitness is lower than the difficulty, the individual dies and is removed 
        from the population. Percentage specifies how much of the population (ranging from 0 to 1) is exposed to the environmental
        factor. Note that a single individual CAN be exposed to an environmetal factor several times."""

        if percent == 1.0:
            for i in self._members:
                if not i.survives_check(difficulty):
                    self._members.remove(i)
        else:
            n_selected = math.floor(len(self._members) * percent)
            for _ in range(n_selected):
                i = random.choice(self._members)
                if not i.survives_check(difficulty):
                    self._members.remove(i)

    def population_reproduction(self):
        """ All individuals whose reproduction cooldown has expired reproduce. """

        offspring_produced = []
        for i in self._members:
            offspring = i.reproduce()

            if not offspring:
                break

            offspring_produced.append(offspring)
        for thing in offspring_produced:
            self._members.append(thing)

    def tick(self):
        """ Increase age of all organisms and decrease their reproduction cooldown. """

        for i in self._members:
            i._age += 1
            i._reproduction_timer += 1

            if i._age >= Organism.MAX_AGE:
                self._members.remove(i)

    def mean_fitness(self):
        """ Returns mean fitness of the population. """

        n = 0.0

        for i in self._members:
            n += i._fitness

        mean_fitness = n / len(self._members)
        return mean_fitness

    def cycle(self, difficulty, percent):
        """ Equates to what happens in one time interval in the algorithm. """

        # At the start of the turn, make everyone 1 year older. Those who are
        # at the organism's max age die. Rest get their reproductive timer (cooldown)
        # increased (shorter until reproduces next).
        self.tick()

        # Selected population are exposed to environmental factor
        # which determines whether they live or die.
        self.check_population(difficulty, percent)

        # All surviving individuals will attempt to reproduce, but only those who have
        # finished reproduction cooldown can reproduce.
        self.population_reproduction()

