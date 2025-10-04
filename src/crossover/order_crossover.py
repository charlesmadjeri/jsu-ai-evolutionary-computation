from src.crossover.crossover import Crossover

class OrderCrossover(Crossover):
    def __init__(self, crossover_size_rate):
        super().__init__(crossover_size_rate)
    
    def crossover(self, parents: tuple[list[int], list[int]]) -> tuple[list[int], list[int]]:
        idx_a, idx_b = self.get_cross_points(len(parents[0]))
        parent_a = parents[0].copy()
        parent_b = parents[1].copy()
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