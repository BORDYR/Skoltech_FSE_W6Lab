from ObserverPattern import Observer
import re

class DepartmentOfHealth(Observer):
    def __init__(self, hospitals, people):
        if(self.__initialized): return
        self.__initialized = True

        self.hospitals = hospitals
        self.people = people

        self.infected_counts = [0]
        self.hospitalized_counts = [0]
        self.dead_counts = [0]
        self.recovered_counts = [0]
        self.antibodies_counts = [0]

        self.day = 0

    def monitor_situation(self):
        for person in self.people:
            person.attach(self)

    def issue_policy(self):
        pass

    def new_day(self):
        self.day += 1

        for arr in [self.infected_counts,
                    self.hospitalized_counts,
                    self.dead_counts,
                    self.recovered_counts,
                    self.antibodies_counts]:
            # if no new infected/hospitalized/etc. people during the last day,
            # update the lists to reflect that new day has come
            if len(arr) < self.day:
                arr.append(arr[-1])

    def update(self, message):
        _, previous_state, _, new_state = re.split(': |\n', message)
        if new_state == 'Asymptomatic sick':
            self.infected_counts[-1] += 1
        elif new_state == 'Hospitalized':
            self.hospitalized_counts[-1] += 1
        elif new_state == 'Dead':
            self.dead_counts[-1] += 1
        elif new_state == 'Healthy':
            self.recovered_counts[-1] += 1
            self.antibodies_counts[-1] += 1
            if previous_state == 'Hospitalized':
                self.hospitalized_counts[-1] -= 1

    def hospitalize(self, person):
        for hospital in self.hospitals:
            if hospital.capacity >= len(hospital.patients):
                hospital.patients.append(person)
                person.set_state(Hospitalized(person))

    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(DepartmentOfHealth, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance
