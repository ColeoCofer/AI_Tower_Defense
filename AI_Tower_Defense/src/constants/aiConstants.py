# general constants
X   = 0
Y   = 1
ON  = True
OFF = False


# AI general constants
NUMBER_OF_STARTING_TOWERS = 20

# Q-Learning constants
GAMMA          = 0.9
EPSILON        = 0.1
EPSILON_STEP   = 0.004
EPSILON_PERIOD = 100
ETA            = 0.1
N_EPISODES     = 50000
M_STEPS        = 500

# GA constants
FITTEST_POPULATION_FRACTION = 5                     # Take 1/5th of the population size for survival of the fittest
POPULATION_SIZE = FITTEST_POPULATION_FRACTION * 2  # Must be a multiple of FITTEST_POPULATION_FRACTION
MAX_GENERATIONS = 10
MUTATION_PCT = 0.05
SURVIVAL_OF_THE_FITTEST = True
NUMBER_OF_CHILDREN = 2

