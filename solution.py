import random
import math

#read txt file containing city data and return as list
def readCities(filePath):
    #open the file, read the data, and then close the file
    input = open(filePath, 'r')
    readFile = input.readlines()
    input.close()

    #init cities list
    cities = []
    #iterate through readFile
    for city in readFile:
        #remove formating and save city integer locations into variables
        xStart = 1                                #save starting position for x coordinate
        for char in range( len(city) ):
            #find and save x
            if (city[char] == ','):
                cityX = int( city[xStart:char] )  #typecast char to int
                yStart = char + 1                 #save starting position for y coordinate
            elif (city[char] == ')'):
                cityY = int ( city[yStart:char] ) #typecast char to int
        #pass the saved x and y values into the list cities as a tuple
        cities.append( (cityX, cityY) )
    #return the list of cities
    return cities

#create the initial population
def initPopulation(POPULATION_SIZE, NUM_CITIES):
    #init empty list to return the initial population of chromosomes
    population = []
    #iterate from 0 to POPULATION_SIZE - 1 to generate the desired number of chromosomes
    for _ in range(POPULATION_SIZE):
        #generate a random order of 0-NUM_CITIES using random.sample()
        population.append( random.sample( range(NUM_CITIES), NUM_CITIES) )
    #return the list of chromosomes
    return population

#distance formula calculation
def distance(city1, city2):
    #sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
    calcX = (city2[0] - city1[0]) ** 2
    calcY = (city2[1] - city1[1]) ** 2
    return math.sqrt( calcX + calcY )

#total chromosome route distance calculation
def totalDistance(cities, route):
    total = 0
    for city in range( len(route) ):
        #modulus operator allows eas calculation from the last city to the first city
        total += distance( cities[route[city] ], cities[route[(city + 1) % len(route) ] ] )
    #return the calculated total distance of the route
    return total

#calculate f(x) value of each chromosome, the total distance of the route
def calculateFX(cities, population):
    #init empty list to return the calculted f(x) values
    distanceList = []
    #iterate through each chromosome in the population and insert its f(x) value into distanceList
    for chromosome in population:
        distanceList.append( totalDistance(cities, chromosome) )
    #return the list of distances
    return distanceList

#calculate the adjusted norm of each chromosome. Since the goal is to find 
#the shortest path we want the smallest f(x) values to have the highest norm
def calculateAdjustedNorm(POPULATION_SIZE, distanceList):
    #init empty lists to hold calculated norms and var to hold the total of the norms
    totalNorm = 0
    adjustedNorms = []
    norms = []
    #iterate through each chromosome's f(x) value saved in distnaceList
    for chromosome in range(POPULATION_SIZE):
        #calculate the adjusted norm and add it to the norms list
        norms.append(1 / distanceList[chromosome]) 
        totalNorm += 1 / distanceList[chromosome]
    #adjust the norms
    adjustedNorms = [norms / totalNorm for norms in norms]
    #return the adjusted norms
    return adjustedNorms   

#calculate the cumulative norm using the adjusted norms list
def calculateCumulativeNorm(POPULATION_SIZE, norms):
    #init list to return the calculated cumulative norm values and a var to hold the total of the norms
    cumulativeNorms = []
    normTotal = 0
    #iterate through each chromosome's norm and add it to both the norm total
    for chromosome in range(POPULATION_SIZE):
        normTotal += norms[chromosome]
        #insert the running norm total into the cumualitve norms list
        cumulativeNorms.append(normTotal)
    #return the list of cumulative norms
    return cumulativeNorms

#select the chromosomes to use for the next generation based on the cumulative norms 
def generationSelection(POPULATION_SIZE, cumulativeNorms):
    #use random.choices() to return a list of index values using cumulativeNorms as the weight
    return random.choices(range(POPULATION_SIZE), weights=cumulativeNorms, k=POPULATION_SIZE ) 

#output the generation to console and write data to the output file
def outputData(output, OUTPUT_FREQUENCY, POPULATION_SIZE, generation, population, distanceList, norms, cumulativeNorms):
    #increment generation since it starts from 0
    generation += 1
    #write values to file and terminal every OUTPUT_FREQUENCY generations
    if (generation == 1 or generation % OUTPUT_FREQUENCY == 0):
        print("Generation: " + str(generation) )
        output.write("Generation: ")
        output.write( str(generation) )
        output.write("\n")
        output.write('%-13s %35s %25s %30s\n' % ("chromosome", "f(x)", "norm", "cumulative norm") )
        for chromosome in range(POPULATION_SIZE):
            output.write('%3s %-10s %25s %25s %25s\n' % (chromosome, population[chromosome], distanceList[chromosome], norms[chromosome], cumulativeNorms[chromosome] ) )

#execute two-point crossover with mutation and elitism
def crossover(POPULATION_SIZE, population, selections):
    #init list to return the newly generated population
    newPopulation = []

    #iterate through the population by twos
    for i in range(0, POPULATION_SIZE, 2):
        #select the parents
        parent1 = population[selections[i] ]
        parent2 = population[selections[i+1] ]

        #generate two random crossover points
        point1 = random.randint(0, len(parent1) - 1)
        point2 = random.randint(point1, len(parent1) - 1)

        child1 = generateChild(parent1, parent2, point1, point2)
        child2 = generateChild(parent2, parent1, point1, point2)

        #add the newly generated children to the new population
        newPopulation.append(child1)
        newPopulation.append(child2)

    #use elitism to carry over best chromosome of current generation to the next
    newPopulation = elitism(population, newPopulation)

    #return the newly generated population
    return newPopulation


#generate child using the generated crossover points
def generateChild(parentA, parentB, point1, point2):
    #init child list to generate chromosome
    child = []

    #insert genes from parent between the two crossover points into child
    for i in range(point1 - 1, point2):
        child.append(parentA[i] )
    #create a set of the added values to avoid duplication
    presentGenes = set(child)

    for i in range( len(parentA) ):
        #when between the crossover points, iterate without inserting new data
        if i >= point1 - 1 and i <= point2 - 1:
            continue
        for j in range( len(parentB) ):
            #only insert genes from parentB if they are not present in child
            if parentB[j] not in presentGenes:
                child.insert(i, parentB[j] )
                presentGenes.add(parentB[j] )
                break

    #attempt to mutate the child chromosome
    child = mutate(child, point1, point2)
    
    #return the the new child chromosome after crossover has occured
    return child

#attemp to mutate a child chromosome 
def mutate(child, point1, point2):
    #mutate the chromosome, if the randomly generated number is greater than MUTATION_RATE
    if (random.random() > MUTATION_RATE):
        #generate two random points between point1 and point2
        mutatePoint1 = random.randint(point1, point2)
        mutatePoint2 = random.randint(mutatePoint1, point2)
        #swap the two genes
        hold = child[mutatePoint1]
        child[mutatePoint1] = child[mutatePoint2]
        child[mutatePoint2] = hold
    #return the child, mutation or not
    return child
    
#implement elitism. Save the most fit from each generation and pass it onto the next
def elitism(population, newPopulation):
    newPopulation[0] = population[ norms.index( max(norms) ) ]
    return newPopulation

def checkConvergence(MAX_GENERATIONS, POPULATION_SIZE, generation, distanceList):
    numEqual = 0
    for i in range(POPULATION_SIZE - 1):
        if distanceList[i] == distanceList[i + 1]:
            numEqual += 1
    if (generation  >= MAX_GENERATIONS / 2 and numEqual == POPULATION_SIZE - 1):
        return True
    else:
        return False
    
#output the final results of the program
def outputFinal(output, POPULATION_SIZE, generation, population, distanceList, norms, cumulativeNorms, cities):
    outputData(output, 1, POPULATION_SIZE, generation, population, distanceList, norms, cumulativeNorms)
    finalTour = ""
    numCity = 0
    for city in population[0]:
        finalTour += str( cities[population[0][city] ] )
        numCity += 1
        if numCity <= len( population[0] ) - 1:
            finalTour += " -> "
    output.write("\nFinal Tour:\n")
    output.write(finalTour)

    output.write("\nTour Cost:\n")
    output.write( str(distanceList[0] ) )

    output.write("\nGenerations:\n")
    output.write( str(generation + 1) )

    output.write("\nPopulation Size:\n")
    output.write( str(POPULATION_SIZE) )
    return

#----------------------------------------MAIN----------------------------------------
#create cities list
cities = readCities("cities.txt")

#define paramaters of simulation
NUM_CITIES = len(cities)
POPULATION_SIZE = 8
MAX_GENERATIONS = 10000
MUTATION_RATE = 0.99
OUTPUT_FREQUENCY = 5 #output every _ generations.

#create initial population
population = initPopulation(POPULATION_SIZE, NUM_CITIES)

#open results.txt in write mode to ouput data into
output = open("results.txt", 'w')

#Generational Loop
for generation in range(MAX_GENERATIONS):
    #calculate the f(x) values for each chromosome and save into distanceList
    distanceList = calculateFX(cities, population)

    #calculate the adjusted norms and save into norms
    norms = calculateAdjustedNorm(POPULATION_SIZE, distanceList)

    #calculate the cumulative norm and save into cumulativeNorms
    cumulativeNorms = calculateCumulativeNorm(POPULATION_SIZE, norms)

    #output the data to terminal and output file
    outputData(output, OUTPUT_FREQUENCY, POPULATION_SIZE, generation, population, distanceList, norms, cumulativeNorms)

    selections = generationSelection(POPULATION_SIZE, cumulativeNorms)

    #Check for convergence
    if (checkConvergence(MAX_GENERATIONS, POPULATION_SIZE, generation, distanceList) ):
        #output the convergence population
        outputFinal(output, POPULATION_SIZE, generation, population, distanceList, norms, cumulativeNorms, cities)
        break

    population = crossover(POPULATION_SIZE, population, selections)


#close output file results.txt
output.close()