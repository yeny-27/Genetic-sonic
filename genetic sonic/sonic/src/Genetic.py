import numpy as np
import random

mutation_chance = 0.03
poblacion = 10
pressure = 2  # cantidad de individuos seleccionados para reproduccion

class Gene:
    # pos_target = 9546
    len_gene = 5000

    def __init__(self):
        # self.mov = [1, 1, 1, 1, 1, 0, 0, 0]
        self.mov = [1, 1, 0, 0]
        # self.pos_list = [0, 1, 2, 3, 4, 5, 6, 7]
        self.pos_list = [0, 1, 2, 3]
    def generate_parent(self):
        # min_mov = np.array([[0, 0, 0, 0, 0, 0, 0, 0]])
        min_mov = np.array([[0, 0, 0, 0]])
        for i in np.arange(self.len_gene):
            # temp = np.array([0, 0, 0, 0, 0, 0, 0, 0])
            temp = np.array([0, 0, 0, 0])
            pos1 = random.sample(self.pos_list, 1)
            mov_ = random.sample(self.mov, 1)
            temp[pos1] = mov_[0]
            # temp[pos2] = mov_[1]
            # temp[pos3] = mov_[2]
            # temp[pos4] = mov_[3]

            temp = np.array([temp])
            min_mov = np.concatenate((min_mov, temp), axis=0)
        min_mov = np.delete(min_mov, 0, 0)
        return min_mov


class Chromosome:
    Genes = None
    Fitness = None

    def __init__(self, genes, fitness, pos_max):
        self.Genes = genes
        self.Fitness = fitness
        self.pos_max = pos_max

def generate_population():
    global poblacion
    nueva_pobla = []
    for i in range(poblacion):
        nueva_pobla.append(Chromosome(Gene().generate_parent(), 0, pos_max=0))

    return nueva_pobla


def selection_parent(population, target=None):
    global poblacion
    posiciones = []
    winer = []

    for pos in range(poblacion-1):
        posiciones.append(pos)

    parti_len = poblacion - 2

    participante = random.sample(posiciones, parti_len)
    part = len(participante)

    while part > 0:
        if len(participante) > 1:
            indi_1, indi_2 = random.sample(participante, 2)
            # Calculo el porcentaje de exito de cata individuo
            part1 = population[indi_1]
            part2 = population[indi_2]
            if part1.Fitness is None:
                print("Objeto sin fitness")

            if part1.Fitness >= part2.Fitness:
                winer.append(part1)
                # Tengo al reves el problema
            else:
                winer.append(part2)

            # Eliminacion de los 2 participantes
            del_index = participante.index(indi_1)
            participante.pop(del_index)
            del_index = participante.index(indi_2)
            participante.pop(del_index)

        if len(winer) == 2 and len(participante) > 1:
            # print("winer 1 {} vs winer 2 {}".format(winer[0].Fitness, winer[1].Fitness))
            if winer[0].Fitness > winer[1].Fitness:
                perderdor = winer.pop(1)
                # print(f'perdedor===>  {perderdor} {len(winer)}')
            else:
                perderdor = winer.pop(0)
                # print(f'perdedor===>  {perderdor} {len(winer)}')
        part = len(participante)
        # print(iter)
        # iter += 1
    return winer


def crossover(parents):
    global pressure
    len_gene_parent = parents[0].Genes.shape[0]
    new_polutation = [None]*poblacion

    for i in range(poblacion - pressure):  # longitud de la poblacion - los padres
        new_polutation[i] = createChild(parents[0].Genes, parents[1].Genes)

    new_polutation[poblacion-2] = parents[0]
    new_polutation[poblacion-1] = parents[1]
    return new_polutation

def createChild(first_chromosm, second_chromosm):
    rand = 0
    # child = np.array([[0, 0, 0, 0, 0, 0, 0, 0]])
    child = np.array([[0, 0, 0, 0]])
    for col in range(first_chromosm.shape[0]):
        rand = random.randint(1, first_chromosm.shape[1])
        slice_gene1 = first_chromosm[col][0:rand]
        slice_gene2 = second_chromosm[col][rand:]
        nuevo_gene = np.concatenate((slice_gene1, slice_gene2), axis=0)
        child = np.concatenate((child, [nuevo_gene]), axis=0)
    child = np.delete(child, 0, 0)
    return Chromosome(child, 0, 0)


def mutation(population):
    global pressure, mutation_chance
    len_y = population[0].Genes.shape[0]
    for i in range(len(population) - pressure):
        if random.random() <= mutation_chance:
            punto_y = random.randint(0, len_y)
            # punto_x = random.randint(1, 8)
            punto_x = random.randint(1, 4)
            punto = population[i].Genes[:punto_y, (punto_x - 1): punto_x]
            flit = np.where((punto == 0) | (punto == 1), punto ^ 1, punto)
            population[i].Genes[:punto_y, (punto_x - 1): punto_x] = flit #Regresa el cambio de bit a la posiciones originales

    return population

def display(generation, n_individuo, individuo, fitness, iteration):
    print("Generacion={}, #individuo={}, individuo={}, fitness={} "
          "iteracion={}".format(generation, n_individuo, individuo, fitness, iteration))


# poblacion = []
# move = []
# for i in range(10):
#     move.append(Gene().generate_parent())
#
# gene = Chromosome(move[0], 248, 120)
# poblacion.append(gene)
# gene = Chromosome(move[1], 123, 120)
# poblacion.append(gene)
# gene = Chromosome(move[2], 14798, 120)
# poblacion.append(gene)
# gene = Chromosome(move[3], 1005, 120)
# poblacion.append(gene)
# gene = Chromosome(move[4], 996, 120)
# poblacion.append(gene)
# gene = Chromosome(move[5], 1500, 120)
# poblacion.append(gene)
# gene = Chromosome(move[6], 7015, 120)
# poblacion.append(gene)
# gene = Chromosome(move[7], 4562, 120)
# poblacion.append(gene)
# gene = Chromosome(move[8], 6789, 120)
# poblacion.append(gene)
# gene = Chromosome(move[9], 3458, 120)
# poblacion.append(gene)
#
# print(poblacion)
#
# print("------------------------------------------------------------")
# parent = selection_parent(poblacion)
# nuevos_poblacion = crossover(parent)
# mutados = mutation(nuevos_poblacion)
#
# print(len(nuevos_poblacion))
# print(len(mutados))

# poblar = generate_population()
# print(poblar[0].Genes.shape)
    # TODO : esto podemos pasarlo como parametro

    # TODO: Cambiarlo a dinamico
    """
    Fase 1 seleccion de participante
    - Definimos n participantes
    - Creamos un ciclo para seleccionar los n
    - generamos aleatoriamente participante 
    - se comprueba que no se haya seleccionado anteriormente
        - si se selecciono anteriormente (ciclo de verificación)
        - se genera nuevamente un numero aleatorio

    Fase 2 Torneo de individuo

    mutation = 0.3
    """
# parent = generate_population()
# winer = selection_parent(parent)
# po = crossover(winer)
# print(winer[0].Genes.shape)
# print(len(po))
# print(po[0].Genes.shape)
# mut = mutation(po)
# print(len(mut))
# print(mut[0].Genes.shape)

'''temp
    * *- Generamos una poblacion de 10 individuos
    - Cada individuo tiene una matriz de movimiento [X][Y]
    - Cada individuo tiene una posición maxima de recorrido
    - Cada individuo tiene un fitness basado en
    la distancia que recorre.

    - Seleccionamos 2 padrestemp
    - Utilizaremo seleccion por torneo
    - de la población se escogen los 2 con mejor (noc)
    - estos 2 escogidos pelearan a muerte (SANGREEE)
        Escoger k (la cantidad de individuos participantes en el torneo) individuos de la población aleatoriamente.
        Escoger el individuo más apto del torneo con probabilidad p
        Escoger el segundo individuo más apto con probabilidad p(1-p)
        Escoger el k-esimo individuo más apto con probabilidad p(1-p)^k
    -

      -los papa tienen un tiempo de vida dentro  de un cliclo while y for
      -
    TODO: Apartir de los 2 padres escogidos, generamos los hijos
    TODO: Con Crossover de un unico punto


    -remplazo generacional se realizara con un Gap Generacional se evaluan los dos esquemas anteriores y la poblacion no cambia si el mismo es > de 3%
    '''

'''
TODO: calculamos el erro absoluto de la posición de maxima del jugador
TODO: Error absoluto = 9546 - la posición maxima
TODO: Error realtivo = Erro absoluto/ 9546
'''
# TODO Action = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# TODO rew = 0.0  done = False
# TODO info = {'level_end_bonus': 0, 'rings': 71,
