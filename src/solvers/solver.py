class Solver():
    def solve(self, coordinates: list[tuple[float, float]])  -> list[tuple[float, float]]:
        raise NotImplementedError

    def mutate(self) -> bool:
        return False