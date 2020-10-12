from abc import abstractmethod, ABC

class Subject(ABC):
    def __init__(self):
        self.subscribers = set()

    def attach(self, o):
        self.subscribers.add(o)

    def detach(self, o):
        self.subscribers.remove(o)

    def notify(self, message):
        for subscriber in self.subscribers:
            subscriber.update(message)

class Observer(ABC):
    @abstractmethod
    def update(message):
        pass
