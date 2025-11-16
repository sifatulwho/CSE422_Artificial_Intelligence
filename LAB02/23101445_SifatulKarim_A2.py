#Task_1


import random
import math

class Chip_comp:
    def __init__(self, block_name, width, height):
        self.block_name = block_name
        self.width = width
        self.height = height

class Interconnection:
    def __init__(self, comp1_idx, comp2_idx):
        self.comp1_idx = comp1_idx
        self.comp2_idx = comp2_idx

class Chromosome:
    def __init__(self, coordinate, chip_comp):
        self.coordinate = coordinate  
        self.chip_comp = chip_comp
        self.fitness = None
        self.overlap = 0
        self.length = 0
        self.bound_area = 0

    def comp_overlap(self, idx1, idx2):
        x1, y1 = self.coordinate[idx1]
        w1, h1 = self.chip_comp[idx1].width, self.chip_comp[idx1].height
        x2, y2 = self.coordinate[idx2]
        w2, h2 = self.chip_comp[idx2].width, self.chip_comp[idx2].height
        
        return not (x1 + w1 <= x2 or x2 + w2 <= x1 or
                   y1 + h1 <= y2 or y2 + h2 <= y1)
    
    def overlap_count(self):
        self.overlap = 0
        for i in range(len(self.chip_comp)):
            for j in range(i+1, len(self.chip_comp)):
                if self.comp_overlap(i, j):
                    self.overlap += 1
    
    def wire_lengthcalc(self, interconn):
        for i in interconn:
            x1, y1 = self.centretocentre(i.comp1_idx)
            x2, y2 = self.centretocentre(i.comp2_idx)
            self.length+= math.sqrt((x2-x1)**2 + (y2-y1)**2)
    
    def centretocentre(self, idx):
        x, y = self.coordinate[idx]
        w, h = self.chip_comp[idx].width, self.chip_comp[idx].height
        return (x + w/2, y + h/2)
    
    def boundingareacalc(self):
        x1, y1 = self.coordinate[0]
        comp = self.chip_comp[0]
        x_min = x1
        y_min = y1
        x_max = x1 + comp.width
        y_max = y1 + comp.width
        
        for i in range(1, len(self.chip_comp)):
            x, y = self.coordinate[i]
            comp = self.chip_comp[i]

            if x < x_min:
                x_min = x
            if x + comp.width > x_max:
                x_max = x + comp.width
            if y < y_min:
                y_min = y
            if y + comp.height > y_max:
                y_max = y + comp.height

        width = x_max - x_min
        height = y_max - y_min
        self.bound_area = width * height

    def calculate_fitness(self, abg, interconn):
        self.overlap_count()
        self.wire_lengthcalc(interconn)
        self.boundingareacalc()
        
        self.fitness = - (abg['alpha'] * self.overlap + abg['beta'] * self.length + abg['gamma'] * self.bound_area)
        
        return self.fitness

def selection(population):
    return random.sample(population, 2)

def crossover(parent1, parent2):
    crossover_point = random.randint(1, 2)
    child1_pos = parent1.coordinate[:crossover_point] + parent2.coordinate[crossover_point:]
    child2_pos = parent2.coordinate[:crossover_point] + parent1.coordinate[crossover_point:]
    child1 = Chromosome(child1_pos, parent1.chip_comp)
    child2 = Chromosome(child2_pos, parent1.chip_comp)

    return child1, child2

def mutation(chromosome, grid_size, mutation_rate = 0.1):
    for i in range(len(chromosome.coordinate)):
        if random.random() < mutation_rate:
            chromosome.coordinate[i] = (random.randint(0, grid_size - 1), random.randint(0, grid_size - 1))

    return chromosome

def new_gen(population, abg, interconn, grid_size, mutation_rate, elitism_count):
    new_population = population[:elitism_count]

    while len(new_population) < len(population):
        parent1, parent2 = selection(population)
        child1, child2 = crossover(parent1, parent2)

        mutation(child1, grid_size, mutation_rate)
        mutation(child2, grid_size, mutation_rate)
        
        child1.calculate_fitness(abg, interconn)
        child2.calculate_fitness(abg, interconn)
        new_population.append(child1)
        if len(new_population) < len(population):  
            new_population.append(child2)
    
    return new_population


chip_comp =  [
    Chip_comp("ALU", 5, 5),
    Chip_comp("Cache", 7, 4),
    Chip_comp("Control Unit", 4, 4),
    Chip_comp("Register File", 6, 6),
    Chip_comp("Decoder", 5, 3),
    Chip_comp("Floating Unit", 5, 5),
]

comp_idx = {}
for i in range(len(chip_comp)):
    comp_idx[chip_comp[i].block_name] = i

interconn = []
interconn.append(Interconnection(comp_idx["Register File"], comp_idx["ALU"]))
interconn.append(Interconnection(comp_idx["Control Unit"], comp_idx["ALU"]))
interconn.append(Interconnection(comp_idx["ALU"], comp_idx["Cache"]))
interconn.append(Interconnection(comp_idx["Register File"], comp_idx["Floating Unit"]))
interconn.append(Interconnection(comp_idx["Cache"], comp_idx["Decoder"]))
interconn.append(Interconnection(comp_idx["Decoder"], comp_idx["Floating Unit"]))

abg = {'alpha': 1000, 'beta': 2, 'gamma': 1}
population_size = 6
max_generation = 15
mutation_rate = 0.1
elitism_count = 1
grid_size = 25

population = []  
for _ in range(population_size):
    new_pos = []
    for _ in chip_comp:
        x = random.randint(0, grid_size - 1)
        y = random.randint(0, grid_size - 1)
        new_pos.append((x, y))

    chromosome = Chromosome(new_pos, chip_comp)
    chromosome.calculate_fitness(abg, interconn)
    population.append(chromosome)

for generation in range(max_generation):
    population = new_gen(population, abg, interconn, grid_size, mutation_rate, elitism_count)

best = population[0]
for i in population:
    if i.fitness > best.fitness:
        best = i

print(f"{best.fitness}\n{best.length}\n{best.bound_area}\n{best.overlap}")




#Task_02

def two_point_crossover(parent1, parent2):
    parent1_gene = parent1.coordinate
    parent2_gene = parent2.coordinate
    size = len(parent1_gene)

    crossover_point = sorted(random.sample(range(1, size), 2))
    point1, point2 = crossover_point

    child1_gene = (parent1_gene[:point1] + parent2_gene[point1:point2] + parent1_gene[point2:])
    child2_gene = (parent2_gene[:point1] + parent1_gene[point1:point2] + parent2_gene[point2:])

    child1 = Chromosome(child1_gene, parent1.chip_comp)
    child2 = Chromosome(child2_gene, parent1.chip_comp)

    print(child1)
    print(child2)

