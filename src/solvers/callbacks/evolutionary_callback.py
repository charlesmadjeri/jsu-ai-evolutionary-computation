from typing import Optional, Callable

StartCallback = Callable[[list[tuple[float, float]], list[int]], None]
ElitesCallback = Callable[[list[tuple[list[int], float]]], None]
GenerationCallback = Callable[[list[list[int]]], None]
EndCallback = Callable[[tuple[list[int], float]], None]

class EvolutionaryCallback():
    def __init__(self, 
        on_start: Optional[StartCallback] = None, 
        on_new_elite: Optional[ElitesCallback] = None, 
        on_new_generation: Optional[GenerationCallback] = None,
        on_end: Optional[EndCallback] = None
    ):
        self.on_start = on_start
        self.on_new_elite = on_new_elite
        self.on_new_generation = on_new_generation
        self.on_end = on_end
