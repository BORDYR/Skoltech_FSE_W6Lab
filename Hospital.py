from DrugPrescriptor import get_prescription_method

class Hospital:
    def __init__(self, capacity, drug_repository):
        self.drug_repository = drug_repository
        self.capacity = capacity
        self.patients = []

    def _treat_patient(self, patient):
        # 1. identify disease
        if patient.virus is not None:
            disease_type = patient.virus.get_type()
        else:
            self.patients.remove(patient)
            return
        prescription_method = get_prescription_method(disease_type, self.drug_repository)

        # 2. understand dose

        # 3. compose treatment
        prescription_drugs = prescription_method.create_prescription()

        # 4. apply treatment
        for drug in prescription_drugs:
            drug.apply(patient)

    def treat_patients(self):
        for patient in self.patients:
            self._treat_patient(patient)
