from abc import ABC, abstractmethod
from typing import List
from Drug import Drug

class AbstractPrescriptor(ABC):
    def __init__(self, drug_repository):
        self.drug_repository = drug_repository

    @abstractmethod
    def create_prescription(self) -> List[Drug]:
        pass


class SeasonalFluPrescriptor(AbstractPrescriptor):
    def __init__(self, drug_repository, antifever_dose=1.0, antivirus_dose=1.0):
        super().__init__(drug_repository)
        self.antifever_dose = antifever_dose
        self.antivirus_dose = antivirus_dose

    def create_prescription(self) -> List[Drug]:
        return [
            self.drug_repository.get_antifever(self.antifever_dose),
            self.drug_repository.get_seasonal_antivirus(self.antivirus_dose)
        ]


class CovidPrescriptor(AbstractPrescriptor):
    def __init__(self, drug_repository, antifever_dose=1.0, antivirus_dose=1.0):
        super().__init__(drug_repository)
        self.antifever_dose = antifever_dose
        self.antivirus_dose = antivirus_dose

    def create_prescription(self) -> List[Drug]:
        return [
            self.drug_repository.get_antifever(self.antifever_dose),
            self.drug_repository.get_sars_antivirus(self.antivirus_dose)
        ]


class CholeraPrescriptor(AbstractPrescriptor):
    def __init__(self, drug_repository, rehydradation_dose=1.0, antivirus_dose=1.0):
        super().__init__(drug_repository)
        self.rehydradation_dose = rehydradation_dose
        self.antivirus_dose = antivirus_dose

    def create_prescription(self) -> List[Drug]:
        return [
            self.drug_repository.get_rehydration(self.rehydradation_dose),
            self.drug_repository.get_cholera_antivirus(self.antivirus_dose)
        ]


def get_prescription_method(disease_type, drug_repository):
    if InfectableType.SeasonalFlu == disease_type:
        return SeasonalFluPrescriptor(drug_repository)

    elif InfectableType.SARSCoV2 == disease_type:
        return CovidPrescriptor(drug_repository)

    elif InfectableType.SARSCoV2 == disease_type:
        return CholeraPrescriptor(drug_repository)

    else:
        raise ValueError()
