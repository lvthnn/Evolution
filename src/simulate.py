#!/usr/bin/env python3
from evolution import Evolution
from population import Population

import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
import matplotlib.animation as animation

import seaborn as sns

import csv
from datetime import datetime 

def main():
    print('\n| EVOLUTIONARY ALGORITHM |')
    print('| Kári Hlynsson, 2021    |\n')

    print('INSTRUCTIONS')
    print('\nThis simulation aims to show the general tendency of average fitness within natural')
    print('populations to increase as a result of natural selection in the environment. ')
    print('You will be asked to input the following simulation parameters:')
    print('   - Difficulty: A floating point value from 0 and upwards. By design, the average population')
    print('                 fitness is approximately 0.5 at the start of the simulation.')
    print('   - Difficulty increase: A boolean value of whether to increase difficulty.')
    print('   - Difficulty increment: How much to increase environmental difficulty pr. time interval. ')
    print('                           This requires that difficulty increase is set to Y.')
    print('   - Initial population size: Size of the natural population at the start of the simulation.')
    print('   - Mutation ratio: The probability ranging from 0 to 1 that an individual receives a substantial')
    print('                     boost to their fitness value as a result of beneficial mutations in genetic material.')
    print('   - Selective ratio: The proportion of the population which is subjected to environmental checks pr. time interval.\n')
    DIFFICULTY = float(input('[1/4] (DBL) Enter difficulty             : '))
    print('')

    PROMPT_DIFFICULTY_INCREASE = input('[2/4] (Y/N) Increase difficulty?         : ')
    DIFFICULTY_INCREASE = False
    DIFFICULTY_INCREMENT = 0

    if PROMPT_DIFFICULTY_INCREASE.upper() == 'Y':
        DIFFICULTY_INCREASE = True
        DIFFICULTY_INCREMENT = float(input('      (DBL) Difficulty increment         : '))
    print('')

    POPULATION_SIZE_INIT = int(input('[3/4] (INT) Initial population size      : '))
    print('')

    MUTATION_RATIO = float(input('[4/4] (DBL) Enter mutation ratio         : '))
    print('')

    SELECTIVE_RATIO = float(input('[5/5] (DBL) Input selective ratio        : '))
    print('')

    stamp = datetime.now()
    stamp_str = stamp.strftime('%d%m%Y-%H%M%S')
    filename = 'data/data' + stamp_str + '.csv'
    f = open(filename, 'w')
    writer = csv.writer(f)

    def simulate(i):
        results = algorithm.interval_cycle()
        nonlocal t, t_axis, size, fitness, density, density_initial, writer

        if t == 0:
            density_initial = results['density']

        fitness.append(results['fitness'])
        size.append(results['size'])
        density = results['density']
        t_axis.append(t)

        print(results['difficulty'])

        csv_row = [t, results['size'], results['fitness'], results['difficulty']]
        writer.writerow(csv_row)
        t += 1

        ax1.cla()
        ax2.cla()
        ax3.cla()

        ax1.plot(t_axis, size)
        ax1.set_xlabel('Time elapsed')
        ax1.set_ylabel('Population size')
        ax1.tick_params(top=False, right=False)
        ax1.grid()

        ax2.plot(t_axis, fitness)
        ax2.set_xlabel('Time elapsed')
        ax2.set_ylabel('Fitness value')
        ax2.tick_params(top=False, right=False)
        ax2.grid()

        sns.kdeplot(density, ax=ax3, warn_singular = False)
        ax3.set_xlabel('Fitness value')
        ax3.set_ylabel('Kernel Density Estimate')
        ax3.tick_params(left=False, top=False, right=False)
        ax3.set_yticklabels([])

    # global
    fig = plt.figure(1)
    gridspec = gs.GridSpec(nrows=2, ncols=2)

    t = 0
    t_axis = []
    size = []
    fitness = []
    density = []
    density_initial = []

    population = Population([], MUTATION_RATIO, DIFFICULTY, POPULATION_SIZE_INIT)
    algorithm = Evolution(population, DIFFICULTY, PROMPT_DIFFICULTY_INCREASE, DIFFICULTY_INCREMENT, SELECTIVE_RATIO)

    # set up plots
    ax1 = plt.subplot(gridspec[0, 0:2])
    ax1.set_xlabel('Time elapsed')
    ax1.set_ylabel('Population size')

    ax2 = plt.subplot(gridspec[1, 0])
    ax2.set_xlabel('Time elapsed')
    ax2.set_ylabel('Fitness value')

    ax3 = plt.subplot(gridspec[1, 1])
    ax3.set_xlabel('Fitness value')
    # ax3.set_ylabel(None)
    ax3.ytickparams = []
    ax3.set(yticklabels=[])

    anim = animation.FuncAnimation(fig, simulate, interval=1)
    plt.tight_layout()
    plt.show()

main()
