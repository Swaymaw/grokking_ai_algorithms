import random


class Item:
    def __init__(self, weight: int, value: int, name: str):
        self.weight = weight
        self.value = value
        self.name = name


KNAPSACK_CAPACITY = 6404180

KNAPSACK_ITEMS = [
    Item(weight=32252, value=68674, name="Axe"),
    Item(weight=225790, value=471010, name="Bronze coin"),
    Item(weight=468164, value=944620, name="Crown"),
    Item(weight=489494, value=962094, name="Diamond statue"),
    Item(weight=35384, value=78344, name="Emerald belt"),
    Item(weight=265590, value=579152, name="Fossil"),
    Item(weight=497911, value=902698, name="Gold coin"),
    Item(weight=800493, value=1686515, name="Helmet"),
    Item(weight=823576, value=1688691, name="Ink"),
    Item(weight=552202, value=1056157, name="Jewel box"),
    Item(weight=323618, value=677562, name="Knife"),
    Item(weight=382846, value=833132, name="Longsword"),
    Item(weight=44676, value=99192, name="Mask"),
    Item(weight=169738, value=376418, name="Necklace"),
    Item(weight=610876, value=1253986, name="Opal badge"),
    Item(weight=854190, value=1853562, name="Pearls"),
    Item(weight=671123, value=1320297, name="Quiver"),
    Item(weight=698180, value=1301637, name="Ruby ring"),
    Item(weight=446517, value=859835, name="Silver bracelet"),
    Item(weight=909620, value=1677534, name="Timepiece"),
    Item(weight=904818, value=1910501, name="Uniform"),
    Item(weight=730061, value=1528646, name="Venom potion"),
    Item(weight=931932, value=1827477, name="Wool scarf"),
    Item(weight=952360, value=2068204, name="Crossbow"),
    Item(weight=926023, value=1746556, name="Yesteryear book"),
    Item(weight=978724, value=2100851, name="Zinc cup"),
]


def generate_initial_population(population_size: int):
    population = []
    for _ in range(population_size):
        individual = "".join([random.choice("01") for _ in range(26)])
        population.append([individual, 0, 0])
    return population


def calculate_individual_fitness(individual: str):
    total_individual_weight = 0
    total_individual_value = 0

    for gene_index in range(len(individual)):
        if individual[gene_index] == "1":
            total_individual_weight += KNAPSACK_ITEMS[gene_index].weight
            total_individual_value += KNAPSACK_ITEMS[gene_index].value

    if total_individual_weight > KNAPSACK_CAPACITY:
        return 0

    return total_individual_value


def calculate_global_fitness(population: list[list]):
    best_score = 0
    best_chromosome = None
    for i in range(len(population)):
        fitness = calculate_individual_fitness(population[i][0])
        population[i][1] = fitness
        if fitness > best_score:
            best_score = fitness
            best_chromosome = population[i][0]

    return best_chromosome, best_score


def set_probabilities(population: list[list]):
    population_sum = sum([individual[1] for individual in population])
    for individual in population:
        individual[2] = individual[1] / population_sum


def roulette_wheel_selection(population: list[list], number_of_selections: int):
    set_probabilities(population)

    slices = []
    total = 0
    for r in range(len(population)):
        individual = population[r]
        slices.append([r, total, total + individual[2]])
        total += individual[2]

    chosen_ones = []
    for r in range(number_of_selections):
        spin = random.random()
        result = [s[0] for s in slices if s[1] < spin <= s[2]]
        chosen_ones.append(population[result[0]])

    return chosen_ones


def one_point_crossover(parent_a: str, parent_b: str, xoverpoint: int):
    children = [
        parent_a[:xoverpoint] + parent_b[xoverpoint:],
        parent_b[:xoverpoint] + parent_a[xoverpoint:],
    ]
    return children


def bit_string_mutation(children: list[list], mutation_rate: float):
    for child in children:
        if random.random() < mutation_rate:
            random_index = random.randint(0, 25)
            if child[0][random_index] == "1":
                mutated_child = list(child[0])
                mutated_child[random_index] = "0"
                child[0] = "".join(mutated_child)
            else:
                mutated_child = list(child[0])
                mutated_child[random_index] = "1"
                child[0] = "".join(mutated_child)

    return children


def reproduce_children(population: list[list], total_children: int = 100):
    children = []
    while len(children) < total_children:
        parent1 = random.choice(population)
        parent2 = random.choice(population)

        if parent1 == parent2:
            continue

        cur_children = one_point_crossover(parent1[0], parent2[0], len(parent1[0]) // 2)
        children.extend([[cur_children[0], 0, 0], [cur_children[1], 0, 0]])

    return children


def merge_population_and_children(
    global_population: list[list], the_children: list[list]
):
    return the_children


def run_ga(initial_population_size: int = 100, number_of_generations: int = 1000):
    best_global_fitness = 0
    best_global_chromosome = None

    global_population = generate_initial_population(initial_population_size)

    for generation in range(number_of_generations):
        current_best_chromosome, current_best_score = calculate_global_fitness(
            global_population
        )
        population_scores = []
        for i in global_population:
            population_scores.append(i[1])

        if generation % 100 == 0:
            print(
                f"Generation: {generation + 1} Population Average:",
                sum(population_scores) / len(population_scores),
            )
        if current_best_score > best_global_fitness:
            best_global_fitness = current_best_score
            best_global_chromosome = current_best_chromosome

        the_chosen = roulette_wheel_selection(global_population, 100)
        the_children = reproduce_children(the_chosen)
        the_children = bit_string_mutation(the_children, mutation_rate=0.4)
        global_population = merge_population_and_children(
            global_population, the_children
        )

    return best_global_chromosome, best_global_fitness


if __name__ == "__main__":
    print(f"{'-' * 10}Starting Generations{'-' * 10}\n")
    best_chromosome, best_score = run_ga(number_of_generations=1000)

    if best_chromosome is None:
        print("No Good Solution Found")
        exit(0)

    print(f"\n{'-' * 10}Generations Completed{'-' * 10}\n")
    print("Best Chromosome:", best_chromosome)
    print("Best Score:", best_score)
    print("Selected Items:")
    total_weight = 0
    for i in range(len(best_chromosome)):
        if best_chromosome[i] == "1":
            print(KNAPSACK_ITEMS[i].name)
            total_weight += KNAPSACK_ITEMS[i].weight

    print("Total Weight:", total_weight)
