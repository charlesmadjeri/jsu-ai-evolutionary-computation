from src.crossover.crossover import Crossover

class PartiallyMappedCrossover(Crossover):
    def __init__(self, parents, crossover_size_rate):
        super().__init__(parents, crossover_size_rate)
    
    def crossover(self) -> tuple[list[int], list[int]]: 
        idx_a, idx_b = self.get_cross_points(len(self.parents[0]))
        parent_a, parent_b = self.parents
        crossover_pts1 = parent_b[idx_a:idx_b]
        crossover_pts2 = parent_a[idx_a:idx_b]
        crossover_position_vector = []
        for parent_node in parent_a:
            crossover_position_vector.append(-1)
        for i in range(len(crossover_pts2)):
            parent_a.remove(crossover_pts2[i])
            crossover_position_vector[idx_a + i] = crossover_pts1[i]
        for i in range(len(parent_a)):
            try:
                while(crossover_position_vector.index(parent_a[i]) != -1):
                    parent_a[i] = crossover_pts2[crossover_pts1.index(parent_a[i])]
            except ValueError:
                pass
        for i in range(len(crossover_pts2)):
            parent_a.insert(idx_a + i, crossover_pts1[i])
        crossover_position_vector.clear()
        for parent_node in parent_b:
            crossover_position_vector.append(-1)
        for i in range(len(crossover_pts1)):
            parent_b.remove(crossover_pts1[i])
            crossover_position_vector[idx_a + i] = crossover_pts2[i]
        for i in range(len(parent_b)):
            try:
                while(crossover_position_vector.index(parent_b[i]) != -1):
                    parent_b[i] = crossover_pts1[crossover_pts2.index(parent_b[i])]
            except ValueError:
                pass
        for i in range(len(crossover_pts1)):
            parent_b.insert(idx_a + i, crossover_pts2[i])
        return parent_a, parent_b

    def get_cross_points(self, cities_nb) -> tuple[int, int]:
        return super().get_cross_points(cities_nb)