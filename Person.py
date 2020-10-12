from abc import ABC, abstractmethod
from ObserverPattern import Subject
from random import randint
from GlobalContext import GlobalContext

class Person(Subject):
    MAX_TEMPERATURE_TO_SURVIVE = 44.0
    LOWEST_WATER_PCT_TO_SURVIVE = 0.4

    LIFE_THREATENING_TEMPERATURE = 40.0
    LIFE_THREATENING_WATER_PCT = 0.5

    def __init__(self, home_position=(0, 0), age=30, weight=70):
        super(Person, self).__init__()
        self.virus = None
        self.antibody_types = set()
        self.temperature = 36.6
        self.weight = weight
        self.water = 0.6 * self.weight
        self.age = age
        self.home_position = home_position
        self.position = home_position
        self.state = Healthy(self)

    def day_actions(self):
        self.state.day_actions()

    def night_actions(self):
        self.state.night_actions()

    def interact(self, other):
        self.state.interact(other)

    def get_infected(self, virus):
        self.state.get_infected(virus)

    def is_close_to(self, other):
        return self.position == other.position

    def fightvirus(self):
        if self.virus:
            self.virus.strength -= (3.0 / self.age)

    def progress_disease(self):
        if self.virus:
            self.virus.cause_symptoms(self)

    def set_state(self, state):
        self.notify('Previous state: ' + str(self.state) + '\nNew state: ' + str(state))
        self.state = state

    def is_life_threatening_condition(self):
        return self.temperature >= Person.LIFE_THREATENING_TEMPERATURE or \
            self.water / self.weight <= Person.LIFE_THREATENING_WATER_PCT

    def is_life_incompatible_condition(self):
        return self.temperature >= Person.MAX_TEMPERATURE_TO_SURVIVE or \
            self.water / self.weight <= Person.LOWEST_WATER_PCT_TO_SURVIVE

class DefaultPerson(Person): pass

class CommunityPerson(Person):
    def __init__(self, community_position=(0, 0), **kwargs):
        super().__init__(**kwargs)
        self.community_position = community_position

class AbstractPersonFactory(ABC):
    def __init__(self, min_j, max_j, min_i, max_i):
        self.min_age, self.max_age = 1, 90
        self.min_weight, self.max_weight = 30, 120
        self.min_j, self.max_j, self.min_i, self.max_i = min_j, max_j, min_i, max_i

    @abstractmethod
    def get_person(self) -> Person:
        pass


class DefaultPersonFactory(AbstractPersonFactory):
    def get_person(self) -> Person:
        return DefaultPerson(
            home_position=(randint(self.min_j, self.max_j), randint(self.min_i, self.max_i)),
            age=randint(self.min_age, self.max_age),
            weight=randint(self.min_weight, self.max_weight),
        )


class CommunityPersonFactory(AbstractPersonFactory):
    def __init__(self, *args, community_position=(0, 0)):
        super().__init__(*args)
        self.community_position = community_position

    def get_person(self) -> Person:
        return CommunityPerson(
            home_position=(randint(self.min_j, self.max_j), randint(self.min_i, self.max_i)),
            age=randint(self.min_age, self.max_age),
            weight=randint(self.min_weight, self.max_weight),
            community_position=self.community_position
        )

def create_persons(min_j, max_j, min_i, max_i, n_persons):
    factory_params = (min_j, max_j, min_i, max_i)

    default_factory = DefaultPersonFactory(*factory_params)
    community_factory = CommunityPersonFactory(*factory_params, community_position=(50, 50))

    n_default_persons = int(n_persons * 0.75)
    n_community_persons = n_persons - n_default_persons

    persons = []
    for i in range(n_default_persons):
        persons.append(default_factory.get_person())

    for i in range(n_community_persons):
        persons.append(community_factory.get_person())

    return persons

class State(ABC):
    def __init__(self, person):
        self.person = person

    @abstractmethod
    def day_actions(self): pass

    @abstractmethod
    def night_actions(self): pass

    @abstractmethod
    def interact(self, other): pass

    @abstractmethod
    def get_infected(self, virus): pass


class Healthy(State):
    def day_actions(self):
        # different for CommunityPerson?!
        if isinstance(self.person, CommunityPerson):
            self.person.position = self.person.community_position
        else:
            min_j, max_j, min_i, max_i = GlobalContext().canvas[:4]
            # I did not figure out they way of accessing canvas that fits with the singleton pattern
            #min_j, max_j, min_i, max_i = GlobalContext.__instance.canvas[:4]
            self.person.position = (randint(min_j, max_j),
                                    randint(min_i, max_i))

    def night_actions(self):
        self.person.position = self.person.home_position

    def interact(self, other: Person): pass

    def get_infected(self, virus):
        if virus.get_type() not in self.person.antibody_types:
            self.person.virus = virus
            self.person.set_state(AsymptomaticSick(self.person))

    def __str__(self):
        return 'Healthy'


class AsymptomaticSick(State):
    DAYS_SICK_TO_FEEL_BAD = 2

    def __init__(self, person):
        super().__init__(person)
        self.days_sick = 0

    def day_actions(self):
        # different for CommunityPerson?!
        if isinstance(self.person, CommunityPerson):
            self.person.position = self.person.community_position
        else:
            min_j, max_j, min_i, max_i = GlobalContext().canvas[:4]
            self.person.position = (randint(min_j, max_j), randint(min_i, max_i))

    def night_actions(self):
        self.person.position = self.person.home_position
        if self.days_sick == AsymptomaticSick.DAYS_SICK_TO_FEEL_BAD:
            self.person.set_state(SymptomaticSick(self.person))
        self.days_sick += 1

    def interact(self, other):
        other.get_infected(self.person.virus)

    def get_infected(self, virus): pass

    def __str__(self):
        return 'Asymptomatic sick'


class SymptomaticSick(State):
    def day_actions(self):
        self.person.progress_disease()

        if self.person.is_life_threatening_condition():
            health_dept = GlobalContext().health_dept
            health_dept.hospitalize(self.person)

        if self.person.is_life_incompatible_condition():
            self.person.set_state(Dead(self.person))

    def night_actions(self):
        # try to fight the virus
        self.person.fightvirus()
        if self.person.virus.strength <= 0:
            self.person.set_state(Healthy(self.person))
            self.person.antibody_types.add(self.person.virus.get_type())
            self.person.virus = None

    def interact(self, other): pass

    def get_infected(self, virus): pass

    def __str__(self):
        return 'Symptomatic sick'


class Hospitalized(SymptomaticSick):
    def day_actions(self):
        self.person.progress_disease()

        if self.person.is_life_incompatible_condition():
            self.person.set_state(Dead(self.person))

    def __str__(self):
        return 'Hospitalized'


class Dead(State):
    def day_actions(self): pass

    def night_actions(self): pass

    def interact(self, other): pass

    def get_infected(self, virus): pass

    def __str__(self):
        return 'Dead'
