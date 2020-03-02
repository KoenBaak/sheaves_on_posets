
from sage.categories.morphism import Morphism

class LocFreeSheafMorphism(Morphism):
    
    def __init__(self, parent, component_dict):
        Morphism.__init__(self, parent)
        self._components = component_dict
        print('in morphism init')
