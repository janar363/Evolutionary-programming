from random import randint

MEAN_BMI = 21.7

max_mean = 0.0
max_intelligence = 0.0
chromosomes = []
gen = 1


def bmi(height, weight):
    bmi_value = float(weight) / ((height * 0.3) ** 2)

    if bmi_value >= 1:
        return bmi_value
    else:
        return 1.0


def get_mutation_factor():
    return randint(30, 100) / 100.0


class Chromosome:
    def __init__(self, **kwargs):
        global max_mean
        global max_intelligence

        if len(kwargs) == 0:
            self.height = randint(1, 10) + 1.0 / randint(1, 100)  # height in feet
            self.weight = randint(1, 300)  # weight in kg
            self.intelligence = randint(0, 100)
        else:
            self.height = kwargs['height']
            self.weight = kwargs['weight']
            self.intelligence = kwargs['intelligence']

        self.mutation_factor = get_mutation_factor()
        self.Bmi = bmi(self.height, self.weight)
        self.meanBmi = abs(self.Bmi - MEAN_BMI)
        self.fitness = 0
        self.intel_score = 0
        self.bmi_score = 0

        if self.meanBmi > max_mean:
            max_mean = self.meanBmi
        if self.intelligence > max_intelligence:
            max_intelligence = self.intelligence


def get_meanBmi(person):
    return person.meanBmi


def get_fitness(person):
    return person.fitness


def init_chromosomes(count):
    for i in range(count):
        chromosomes.append(Chromosome())


def mutate_height(height, mf):
    prob = randint(0, 1)

    if prob:
        ht = height * mf * 2
        if ht > 10.0:
            return 10.0
        else:
            return ht
    else:
        try:
            return height / (mf * 2)
        except ZeroDivisionError:
            return height


def mutate_weight(weight, mf):
    prob = randint(0, 1)

    if prob:
        return weight * mf * 2
    else:
        try:
            return weight / (mf * 2)
        except ZeroDivisionError:
            return weight


def mutate_intelligence(intelligence, mf):
    prob = randint(0, 1)

    if prob:
        intel = intelligence * mf * 2

        if intel > 300.0:
            return 300.0
        else:
            return intel
    else:
        try:
            if mf >= 0.5:
                return intelligence / (mf * 2)
            else:
                return intelligence
        except ZeroDivisionError:
            return intelligence


def mutate():
    global chromosomes
    mutated_chromosomes = []
    for chromo in chromosomes:
        height = mutate_height(chromo.height, chromo.mutation_factor)
        weight = mutate_weight(chromo.weight, chromo.mutation_factor)
        intelligence = mutate_intelligence(chromo.intelligence, chromo.mutation_factor)
        new_chromosome = Chromosome(height=height, weight=weight, intelligence=intelligence)
        mutated_chromosomes.append(new_chromosome)

    chromosomes.extend(mutated_chromosomes)


def cal_fitness():
    for chromo in chromosomes:
        chromo.intel_score = chromo.intelligence / max_intelligence * 100
        chromo.bmi_score = 100.0 - chromo.meanBmi / max_mean * 100

        chromo.fitness = chromo.intel_score + chromo.bmi_score

    


def print_gen():
    global max_bmi
    current_gen = []
    print(f'Gen {gen}')
    for chromo in chromosomes:
        print(
            f'intel_score={round(chromo.intel_score, 2)}  bmi_score={round(chromo.bmi_score, 2)} intel={round(chromo.intelligence, 2)} bmi={round(chromo.Bmi, 2)}')

    print(current_gen)


# --------------------------------------------------------------------------------------------------------------------

# initialize chromosomes
n = int(input('Enter the size of the initial population size : '))
itr = int(input('Enter no of iteration : '))

init_chromosomes(n)
print_gen()


# evolve

def evolve():
    global chromosomes
    global gen

    gen += 1

    # mutate chromosomes
    mutate()

    # fitness calculation
    cal_fitness()
    

    # survivor selection
    chromosomes = sorted(chromosomes, key=get_fitness, reverse=True)
    chromosomes = chromosomes[0:n]

    # display current generation data
    print_gen()

    if gen < itr:
        evolve()


evolve()
