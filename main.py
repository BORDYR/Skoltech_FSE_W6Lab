from random import randint, sample, choices
from Virus import *
from DrugRepository import *
from Hospital import Hospital
from DepartmentOfHealth import DepartmentOfHealth
from GlobalContext import GlobalContext
from Person import create_persons


def create_department_of_health(hospitals, persons):
    return DepartmentOfHealth(hospitals, persons)


def create_hospitals(n_hospitals):
    drug_repository_types = choices([CheapDrugRepository, ExpensiveDrugRepository], k=n_hospitals)
    hospitals = [
        Hospital(capacity=50, drug_repository=drug_repository_types[i]())
        for i in range(n_hospitals)
    ]
    return hospitals

def initialize():
    # our little country
    min_i, max_i = 0, 23
    min_j, max_j = 0, 23

    # our citizen
    n_persons = 500
    persons = create_persons(min_j, max_j, min_i, max_i, n_persons)

    viruses = []
    for virus_type in [InfectableType.SeasonalFlu, InfectableType.SARSCoV2, InfectableType.Cholera]:
        viruses.append(get_infectable(virus_type))

    # our healthcare system
    n_hospitals = 4
    hospitals = create_hospitals(n_hospitals)

    health_dept = create_department_of_health(hospitals, persons)
    health_dept.monitor_situation()

    persons_to_be_infected = sample(persons, 3)
    for person, virus in zip(persons_to_be_infected, viruses):
        person.get_infected(virus)

    # global context
    context = GlobalContext(
        canvas=(min_j, max_j, min_i, max_i),
        persons=persons,
        health_dept=health_dept
    )

    return context

def simulate_day(context):
    persons, health_dept, hospitals = context.persons, context.health_dept, context.health_dept.hospitals

    # health_dept.issue_policy()
    health_dept.new_day()

    for hospital in hospitals:
        hospital.treat_patients()

    for person in persons:
        person.day_actions()

    for person in persons:
        for other in persons:
            if person is not other and person.is_close_to(other):
                person.interact(other)

    for person in persons:
        person.night_actions()

context = initialize()

for day in range(100):
    print('day {}'.format(day + 1))
    simulate_day(context)
