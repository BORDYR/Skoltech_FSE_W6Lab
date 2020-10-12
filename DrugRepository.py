from abc import ABC, abstractmethod
from typing import List
from Drug import Drug

class DrugRepository(ABC):
    def __init__(self):
        self.treatment = []

    @abstractmethod
    def get_antifever(self, dose) -> Drug: pass

    @abstractmethod
    def get_rehydration(self, dose) -> Drug: pass

    @abstractmethod
    def get_seasonal_antivirus(self, dose) -> Drug: pass

    @abstractmethod
    def get_sars_antivirus(self, dose) -> Drug: pass

    @abstractmethod
    def get_cholera_antivirus(self, dose) -> Drug: pass

    def get_treatment(self):
        return self.treatment


class CheapDrugRepository(DrugRepository):
    def get_antifever(self, dose) -> Drug:
        return Aspirin(dose)

    def get_rehydration(self, dose) -> Drug:
        return Glucose(dose)

    def get_seasonal_antivirus(self, dose) -> Drug:
        return Placebo(dose)

    def get_sars_antivirus(self, dose) -> Drug:
        return Placebo(dose)

    def get_cholera_antivirus(self, dose) -> Drug:
        return Placebo(dose)


class ExpensiveDrugRepository(DrugRepository):
    def get_antifever(self, dose) -> Drug:
        return Ibuprofen(dose)

    def get_rehydration(self, dose) -> Drug:
        return Rehydron(dose)

    def get_seasonal_antivirus(self, dose) -> Drug:
        return AntivirusSeasonalFlu(dose)

    def get_sars_antivirus(self, dose) -> Drug:
        return AntivirusSARSCoV2(dose)

    def get_cholera_antivirus(self, dose) -> Drug:
        return AntivirusCholera(dose)
