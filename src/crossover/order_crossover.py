from crossover.crossover import Crossover
import random

class OrderCrossover(Crossover):
    def __init__(self, parents, crossover_size_rate):
        super().__init__(parents, crossover_size_rate)
    
    def crossover(self) -> tuple[list[int], list[int]]:
        idx_a, idx_b = self.get_cross_points(self.crossover_size_rate, len(self.parents[0]))
        parent_a, parent_b = self.parents
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
        return (parent_a, parent_b)
    
    def get_cross_points(self, crossover_size_rate, cities_nb) -> tuple[int, int]:
        crossover_lt = (int) (crossover_size_rate * cities_nb)
        idx_a = random.randint(0, cities_nb - crossover_lt)
        idx_b = idx_a + crossover_lt
        return (idx_a, idx_b)