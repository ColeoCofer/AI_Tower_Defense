# general constants
X   = 0
Y   = 1
ON  = True
OFF = False


# AI general constants
NUMBER_OF_STARTING_TOWERS = 30

# Q-Learning constants
DISCOUNT_RATE  = 0.9
EPSILON        = 0.1
EPSILON_STEP   = 0.004
EPSILON_PERIOD = 100
LEARN_RATE     = 0.1
N_EPISODES     = 20000
M_STEPS        = 500

# GA constants
FITTEST_POPULATION_FRACTION = 5                             # Take 1/5th of the population size for survival of the fittest
POPULATION_SIZE = (FITTEST_POPULATION_FRACTION * 1) * 2   # Must be a multiple of FITTEST_POPULATION_FRACTION, and divisible by 2
MAX_GENERATIONS = 100
MUTATION_PCT = 0.1
SURVIVAL_OF_THE_FITTEST = True
NUMBER_OF_CHILDREN = 2

# Deep Q-Learning constants
DEEP_BUYING_THRESHOLD = 200
DEEP_STARTING_COINS = 600