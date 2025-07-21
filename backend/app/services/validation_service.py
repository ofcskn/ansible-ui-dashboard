from app.helpers.validators import Validator
from typing import List

class ValidationService:
    def __init__(self, validators: List[Validator]):
        self.validators = validators

    def validate(self, data):
        for validator in self.validators:
            is_valid, message = validator.validate(data)
            if not is_valid:
                return False, message
        return True, ""
