import pygad
import structural_similarity_modified as sst
from skimage import io
import numpy as np


im_original = io.imread('original/C0003.bmp')
im_pgbz = io.imread('places2/C0003_comp_pgbz_output.png')
im_wavelet = io.imread('Wavelet/C0003_comp_wavlet.png')

def fitness_func(ga_instance, solution, solution_idx):
    alpha, beta, gamma = solution
    ssim_pgbz = sst.structural_similarity(im_original, im_pgbz, alpha=alpha, beta=beta, gamma=gamma, multichannel=True)
    ssim_wavelet = sst.structural_similarity(im_original, im_wavelet, alpha=alpha, beta=beta, gamma=gamma,
                                             multichannel=True)
    fitness = ssim_pgbz - ssim_wavelet
    return fitness


fitness_function = fitness_func
num_generations = 40
num_parents_mating = 4
sol_per_pop = 10
num_genes = 3

init_range_low = 0
init_range_high = 5

parent_selection_type = "sss"
keep_parents = -1

crossover_type = "single_point"
mutation_type ="random"
mutation_percent_genes = 10
gene_space = [{'low': 0, 'high': 5}, {'low': 0, 'high': 5}, {'low': 0, 'high': 5}]

def on_generation(ga_instance):
    print(f"Generation {ga_instance.generations_completed}")
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    alpha, beta, gamma = solution
    print(f"Current alpha: {alpha}")
    print(f"Current beta: {beta}")
    print(f"Current gamma: {gamma}")
    print(f"Fitness value: {solution_fitness}")



ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_function,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       init_range_low=init_range_low,
                       init_range_high=init_range_high,
                       parent_selection_type=parent_selection_type,
                       keep_parents=keep_parents,
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       mutation_percent_genes=mutation_percent_genes,
                       on_generation=on_generation,
                       gene_space=gene_space)


ga_instance.run()

solution, solution_fitness, solution_idx = ga_instance.best_solution()
print(f"Best solution (alpha, beta, gamma): {solution}")
print(f"Best solution fitness value: {solution_fitness}")

alpha, beta, gamma = solution
ssim_pgbz = sst.structural_similarity(im_original, im_pgbz, alpha=alpha, beta=beta, gamma=gamma, multichannel=True)
ssim_wavelet = sst.structural_similarity(im_original, im_wavelet, alpha=alpha, beta=beta, gamma=gamma, multichannel=True)
difference = (ssim_pgbz - ssim_wavelet)

print(f"SSIM (PGBZ): {ssim_pgbz}")
print(f"SSIM (Wavelet): {ssim_wavelet}")
print(f"Difference: {difference}")
