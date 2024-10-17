# Author: Mariia Maksymenko
# Description: Simulating a genetic algorithm that populates a list of random ASCII characters with
# the same length as a paragraph of text in a txt file it reads, and crosses and mutates the characters 
# to eventually get a matching string.
import random

# The main function for the genetic algorithm
def genetic_algorithm(target):
    population_size = 500 # Bigger populations produces faster results
    # Setting the mutation rate to a really low number works the best
    mutation_rate = 0.01
    generations = 5500
    
    population = []

    # Creates a list of random strings (individuals in a population) with the same length as the target string
    for _ in range(population_size):
        individual = ''
        
        # Generates random characters for each gene
        for _ in range(len(target)):
            individual += chr(random.randint(0, 255))
        
        population.append(individual)

    
    for generation in range(generations):
        
        fitness_scores = []

        # Populates a list of tuples with individuals and their corresponding fitness scores
        for individual in population:

            score = fitness(individual, target)
            fitness_scores.append((individual, score))

        
        """To select the best fitted individual, this line sorts, in descending order, the second
        element [1] (the fitness score of each individual) of each tuple, so the best individual is
        at the top of the list"""
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Prints the best individual and their score to track the progress of the algorithm
        print(f"Generation {generation}, best individual = {fitness_scores[0][0]}")

        # Checks if the fitness score equals the length of the target, if it's the same then it's a 100% match
        # and it stops the algorithm
        if fitness_scores[0][1] == len(target):
            print(f"FOUND THE MATCH! The string is: {fitness_scores[0][0]} from generation {generation}")
            break
        
        new_population = []
        
        # The best individual from previous generation goes in the next generation first
        new_population.append(fitness_scores[0][0])
        
        while len(new_population) < population_size:
            
            # Elitism section: the only parents that make it to the new generation are the 
            # top 50% of the previous generation (easy to track because the fitness scores are sorted)
            parent1 = random.choice(fitness_scores[:50])[0]
            parent2 = random.choice(fitness_scores[:50])[0]
            
            # Creating and mutating children
            child = crossover(parent1, parent2)

            child = mutate(child, mutation_rate)

            new_population.append(child)
        
        population = new_population


"""This is the fitness function. It loops through the pairs of characters in the individual and target strings
and checks if they match, and tracks those matches to give a string its fitness score at the end.
"""
def fitness(individual, target):
    matches = 0
    
    for i, j in zip(individual, target):
        if i == j:
            matches += 1
    
    return matches



"""This is the crossover function, it just chooses a random point in the first parent, and takes 
the characters before that point from the first parent, and the rest from the second parent."""
def crossover(parent1, parent2):
    point = random.randint(0, len(parent1) - 1)
    # Just uses slicing + concatenation
    return parent1[:point] + parent2[point:]


"""This function is the mutatiomn function. It converts the string into a list so it can be modified,
loops through every character, and it has a chance to replace a character with a random ASCII character.
Then it just converts the string back to the original form."""
def mutate(individual, mutation_rate):

    new_individual = list(individual)

    for i in range(len(individual)):
        # Applies mutation with the probability = mutation rate
        if random.random() < mutation_rate:
            new_individual[i] = chr(random.randint(0, 255))

    return ''.join(new_individual)

# Text file input
target_file = input("Enter file name: ")
with open(target_file, 'r') as f:
    text = f.read().strip()

genetic_algorithm(text)
