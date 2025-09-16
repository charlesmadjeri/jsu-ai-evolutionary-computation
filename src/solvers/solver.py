"""
Abstract solver class - all solvers must inherit from this class.
"""
class Solver():
    """
    Solver main method with solve algorithm implementation.
    Returns: list of coordinates and the distance traveled
    """
    def solve(self, coordinates: list[tuple[float, float]])  -> [list[tuple[float, float]], float]:
        raise NotImplementedError

    def mutate(self) -> bool:
        return False