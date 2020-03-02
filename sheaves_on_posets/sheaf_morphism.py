
from sage.structure.element import Element

class LocFreeSheafMorphism(Element):
    
    def __init__(self, parent, component_dict):
        Element.__init__(self, parent)
        self._components = component_dict
        print('in morphism init')
