from injector import Module, Binder, singleton, Injector, inject
from flask_injector import inject

class InjectionContext:
    def __init__(self, inject: inject):
        self.inject = inject

    def get(self):
        return self.inject    
