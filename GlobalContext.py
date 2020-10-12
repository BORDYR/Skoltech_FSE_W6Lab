class GlobalContext:
    def __init__(self, canvas=None, persons=None, health_dept=None):
        if(self.__initialized): return
        self.__initialized = True

        self.canvas = canvas
        self.persons = persons
        self.health_dept = health_dept

    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(GlobalContext, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance
