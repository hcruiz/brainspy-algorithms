# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 13:14:52 2019

@author: HCRuiz
"""
import numpy as np
from bspyalgo.utils.performance import perceptron

# TODO: implement corr_lin_fit (AF's last fitness function)?


def choose_fitness_function(fitness):
    '''Gets the fitness function used in GA from the module FitnessFunctions
    The fitness functions must take two arguments, the outputs of the black-box and the target
    and must return a numpy array of scores of size len(outputs).
    '''
    if fitness == 'corr_fit':
        return corr_fit
    elif fitness == 'accuracy_fit':
        return accuracy_fit
    elif fitness == 'corrsig_fit':
        return corrsig_fit
    else:
        raise NotImplementedError(f"Fitness function {fitness} is not recognized!")

# %% Accuracy of a perceptron as fitness: meanures separability


def accuracy_fit(outputpool, target, clipvalue=np.inf):
    genomes = len(outputpool)
    fitpool = np.zeros(genomes)
    for j in range(genomes):
        output = outputpool[j]

        if np.any(np.abs(output) > clipvalue):
            acc = 0
            # print(f'Clipped at {clipvalue} nA')
        else:
            x = output[:, np.newaxis]
            y = target[:, np.newaxis]
            acc, _, _ = perceptron(x, y)

        fitpool[j] = acc
    return fitpool

# %% Correlation between output and target: measures similarity


def corr_fit(outputpool, target, clipvalue=np.inf):
    genomes = len(outputpool)
    fitpool = np.zeros(genomes)
    for j in range(genomes):
        output = outputpool[j]
        if np.any(np.abs(output) > clipvalue):
            # print(f'Clipped at {clipvalue} nA')
            corr = -1
        else:
            x = output[:, np.newaxis]
            y = target[:, np.newaxis]
            X = np.stack((x, y), axis=0)[:, :, 0]
            corr = np.corrcoef(X)[0, 1]

        fitpool[j] = corr
    return fitpool

# %% Combination of a sigmoid with pre-defined separation threshold (2.5 nA) and
# the correlation function. The sigmoid can be adapted by changing the function 'sig( , x)'


def corrsig_fit(outputpool, target, clipvalue=np.inf):
    genomes = len(outputpool)
    fitpool = np.zeros(genomes)
    for j in range(genomes):
        output = outputpool[j]
        if np.any(np.abs(output) > clipvalue):
            # print(f'Clipped at {clipvalue} nA')
            fit = -1
        else:
            X = np.stack((output, target), axis=0)[:, :, 0]
            corr = np.corrcoef(X)[0, 1]
            buff0 = target == 0
            buff1 = target == 1
            sep = np.mean(output[buff1]) - np.mean(output[buff0])
            sig = 1 / (1 + np.exp(-2 * (sep - 2)))
            fit = corr * sig
        fitpool[j] = fit
    return fitpool
