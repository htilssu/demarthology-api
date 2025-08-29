from app.models.symptom import Symptom
from app.repositories.repository import PaginatedRepository


class SymptomRepository(PaginatedRepository[Symptom]):
    document_class = Symptom
