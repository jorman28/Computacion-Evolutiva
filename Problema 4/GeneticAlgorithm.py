import random
import operator
import time

'''
POBLACIÓN, total de 20 personas.

Los mejores serán aquellos que coincidan con más validaciones y que fmin sea el más bajo.

El cruce se realizará entre 10 personas, más del 70%, en un punto
y cruzan primero con segundo, tercero con cuarto, y así sucesivamente

La mutación va a superar el 80%. Pueden mutar los 2 primeros genotipos, o los otros 4.
Cada grupo debe ser mutado para mantener las siguientes condiciones:
a) La suma de los 2 primeros genotipos debe ser menor o igual que 1000
b) La suma de los otros 4 genotipos debe ser menor o igual que 2000

La mutación asegurará que estos valores se mantengan después del cruce de todos modos.

El castigo ocurre si hay algún valor negativo en el individuo o
cualquier individuo bajo bestCountValidations
'''
population = [
    [51, 856, 84, 522, 102, 1024],
    [956, 209, 789, 1020, 100, 49],
    [689, 125, 693, 482, 1536, 93],
    [785, 964, 125, 175, 466, 1320],
    [99, 856, 586, 250, 479, 945],
    [26, 450, 148, 963, 1322, 485],
    [596, 485, 20, 785, 845, 1452],
    [365, 452, 136, 726, 95, 1154],
    [22, 564, 88, 471, 122, 502],
    [451, 568, 412, 895, 652, 125],
    [154, 9, 365, 124, 789, 1210],
    [956, 154, 745, 694, 1482, 149],
    [148, 412, 985, 741, 1020, 96],
    [298, 845, 756, 951, 1852, 269],
    [55, 321, 584, 981, 1126, 784],
    [956, 741, 1520, 645, 742, 222],
    [365, 154, 878, 652, 442, 121],
    [845, 8, 452, 103, 202, 654],
    [746, 685, 15, 669, 1025, 652],
    [28, 1203, 485, 784, 452, 1269],
]


'''
FUNCIONES Y RESTRICCIONES
'''

def multiplyAndSumVarsForCoefs(vars, coefs):
    total = 0

    for i in range(0, len(coefs)):
        total += coefs[i] * vars[i]
    # End for

    return total
# End f

def fmin(idv):
    fminCoefs = [3.9, 3.0, 3.6, 4.3, 3.65, 4.35]
    return multiplyAndSumVarsForCoefs(idv, fminCoefs)
# End f

def validateRestriction(idv, coefs, op, compareTo):
    val = multiplyAndSumVarsForCoefs(idv, coefs)
    return op(val, compareTo)
# End validateRestriction

def countValidRestrictions(idv):
    totalValid = 0

    totalValid += 0 | validateRestriction(idv, [4, 4, 0, 0, 0, 0], operator.le, 8800) # Dpto D1
    totalValid += 0 | validateRestriction(idv, [1, 1, 3, 3, 3, 3], operator.le, 8800) # Dpto D2
    totalValid += 0 | validateRestriction(idv, [6, 0, 2, 2, 0, 0], operator.le, 8800) # Dpto E1
    totalValid += 0 | validateRestriction(idv, [0, 2, 0, 0, 3, 3], operator.le, 8800) # Dpto E2
    totalValid += 0 | validateRestriction(idv, [0, 0, 6, 0, 6, 0], operator.le, 8800) # Dpto F1
    totalValid += 0 | validateRestriction(idv, [4, 4, 0, 4, 0, 4], operator.le, 8800) # Dpto F2
    
    totalValid += 0 | validateRestriction(idv, [0.1, 0.1, 0.5, 0.5, 0.5, 0.5], operator.le, 2400) # Dpto F2
    totalValid += 0 | validateRestriction(idv, [0, 0, 1, 1, 1, 1], operator.eq, 2000) # Dpto F2
    totalValid += 0 | validateRestriction(idv, [1, 1, 0, 0, 0, 0], operator.eq, 1000) # Dpto F2

    return totalValid

# End validateAllRestrictions


'''
ALGORITMO GENETICO
'''

bestValue = 0
bestCountValidations = 0
bestAllTime = None

def orderAscMaxValidRestrictionsAndDescMinValue(population):
    sortCriteria = lambda idv:(countValidRestrictions(idv), -fmin(idv))
    population.sort(key = sortCriteria, reverse = True)
# End orderByMinValueAndMaxValidRestrictions

FIRST_PART_GENOTYPE_ALLOWED = 1000
SECOND_PART_GENOTYPE_ALLOWED = 2000

MUTATION_THRESHOLD = 0.8
CROSSOVER_THRESHOLD = 0.7
SAMPLE_SIZE = 10 # This must be pair
def getPopulationForNewGeneration(population):
    newPop = []

    sample = population[:SAMPLE_SIZE]
    for i in range(0, SAMPLE_SIZE // 2):
        kids = crossoverIndividuals(sample[i*2], sample[(i+1)*2 - 1])

        if len(kids) > 0: # Proceed with mutation
            kids = mutateIndividuals(kids)
            newPop += punishIndividuals(kids)
        # End if
    # End for

    return newPop + population[len(newPop):]
# End crossoverPopulation

def crossoverIndividuals(dad, mom):

    lenParent = len(dad)
    idx = 1
    while idx < lenParent:
        rdm = random.random()
        if (rdm >= CROSSOVER_THRESHOLD): break
        idx += 1
    # End while

    newIdvs = []
    if (idx < lenParent): # crossover happens
        first = dad[0:idx] + mom[idx:]
        second = mom[0:idx] + dad[idx:]
        newIdvs = [first, second]
    # End if
    
    return newIdvs
# End crossoverIndividuals

def mutateIndividuals(idvs):
    for idv in idvs:

        lenIdv = len(idv)
        idx = 0
        while idx < lenIdv:
            rdm = random.random()
            if (rdm >= MUTATION_THRESHOLD): break
            idx += 1
        # End while

        if (idx < lenIdv): mutateIndividualAtIdx(idv, idx)
        ensureMinimunConditionsAreReached(idv)
    # End for

    return idvs
# End mutateIndividuals

def mutateIndividualAtIdx(idv, idx):
    tot = comparableValue = 0

    if (idx < 2):
        tot = sum(idv[:2])
        comparableValue != FIRST_PART_GENOTYPE_ALLOWED
    else:
        tot = sum(idv[2:])
        comparableValue != SECOND_PART_GENOTYPE_ALLOWED
    # End if

    if tot > comparableValue:
        idv[idx] -= tot - comparableValue
    # End if

    return idv
# End mutateIndividualAtIdx

def ensureMinimunConditionsAreReached(idv):
    opt = list(idv)
    if sum(idv[:2]) != FIRST_PART_GENOTYPE_ALLOWED: 
        mutateToKeepSumFromTo(idv, FIRST_PART_GENOTYPE_ALLOWED, 0, 1)
    # End if

    if sum(idv[2:]) != SECOND_PART_GENOTYPE_ALLOWED: 
        mutateToKeepSumFromTo(idv, SECOND_PART_GENOTYPE_ALLOWED, 2, 5)
    # End if

    return idv
# End ensureMinimunConditionsAreReached


def mutateToKeepSumFromTo(idv, tot, start, end):
    for i in range(start, end):
        rdm = random.randint(0, tot)
        idv[i] = rdm
        tot -= rdm
    # End for

    idv[end] = tot
    return idv
# End mutateToKeepSumFromTo


def punishIndividuals(idvs):
    validIdvs = []

    for idv in idvs:
        filtered = list(filter(lambda g: g < 0, idv))
        if (len(filtered) == 0): validIdvs.append(idv)
    # End for

    return validIdvs
# End punishIndividuals

def init():
    global bestValue, bestCountValidations, bestAllTime, population

    orderAscMaxValidRestrictionsAndDescMinValue(population)

    bestAllTime = population[0]
    bestValue = fmin(bestAllTime)
    bestCountValidations = countValidRestrictions(bestAllTime)

    for gen in range(0, 1000000):
        # print("Running generation:", gen)
        population = getPopulationForNewGeneration(population)
        orderAscMaxValidRestrictionsAndDescMinValue(population)
        
        bestGeneration = population[0]
        minValue = fmin(bestGeneration)
        counValidations = countValidRestrictions(bestGeneration)
        # print("Best result for current gen", bestGeneration, minValue, counValidations , "\n")

        if (bestCountValidations < counValidations 
            or (bestCountValidations == counValidations and bestValue >= minValue)):

            bestCountValidations = counValidations
            bestValue = minValue
            bestAllTime = bestGeneration
        # End if

    # End for
# End init
start = time.time()
init()
print("LA MEJOR DE TODAS las generaciones para la generación actual", bestAllTime, bestValue, bestCountValidations, "\n")
print('Terminado en: ' + str(time.time() - start) + ' sec')