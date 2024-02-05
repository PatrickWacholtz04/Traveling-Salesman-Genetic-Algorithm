The purpose of the program is to solve the Traveling Salesperson Problem using a Genetic Algorithm.
The aim of Traveling Salesperson Problem is, given a list of cities and the distance between each pair of cities,
what is the shortest possible route that visits each city exactly once and ends with the city that was started with.

For this implementation, a number of nine cities was assumed. However there is no limit to the amount of cities that
the program can accept.

The cities are read from cities.txt in the format '(x,y)'. 
There is no limit to the range of x and y.

The Genetic Algorithm's chromosomes are decimal digits ranging from 0 to the number of cities - 1. 
Each digit represents a different city.

It implements two-point chromosome crossover. Two points in the chromosome are randomly chosen.
The child will recieve these genes from one parent in the exact position and order as the parent.
The remaning genes will be filled in from the other parent.

Mutation of the child chromosome is attempted each time a new child is generated. A random float is generated
using the random.random() function. If this value is greater than the MUTATION_RATE, two genes within the 
range of the crossover points will be swapped.

This algorithm also implements the principle of elitism. Using elitism, the most fit chromosome from the 
current generation will always be passed on to the next generation.

The results of the program will be output to results.txt in the root folder.
The results of 10 program runs using the values in cities.txt are stored in the folder results.