from abc import ABC, abstractmethod
import random

class Crossover(ABC):
    @abstractmethod
    def __init__(self, input_data: list[int], crossover_size_rate: float):
        self.input_data = input_data
        self.crossover_size_rate = crossover_size_rate
    
    def crossover(self, parents: list[list[int]], nr_generations: int) -> list[list[list[int]]]:
        idx_a, idx_b = self.get_cross_points(self.crossover_size_rate, parents[0].length)
        offsprings = []
        generations = []
        for i in range(nr_generations):
            while parents != []:
                parent_a = parents[random.randint(0, len(parents) - 1)]
                parents.remove(parent_a)
                parent_b = parents[random.randint(0, len(parents) - 1)]
                parents.remove(parent_b)
                crossover_pts1 = parent_b[idx_a:idx_b]
                crossover_pts2 = parent_a[idx_a:idx_b]
                for point in crossover_pts1:
                    parent_a.remove(point)
                for point in crossover_pts2:
                    parent_b.remove(point)
                for i in range(len(crossover_pts1)):
                    parent_a.insert(idx_a + i, crossover_pts1[i])
                for i in range(len(crossover_pts2)):
                    parent_b.insert(idx_a + i, crossover_pts2[i])
                offsprings.append(parent_a)
                offsprings.append(parent_b)
            print(offsprings)    
            generations.append(offsprings.copy())
            for i in range(len(offsprings)):
                parents.append(offsprings.copy()[i])
            offsprings.clear()
        return generations

    
    def get_cross_points(crossover_size_rate: float, cities_nb: int) -> tuple[int, int]:
        crossover_lt = crossover_size_rate * cities_nb
        idx_a = random.randint(0, cities_nb - crossover_lt)
        idx_b = idx_a + crossover_lt
        return (idx_a, idx_b)
