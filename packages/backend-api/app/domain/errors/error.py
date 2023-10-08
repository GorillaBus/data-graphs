from app.domain.errors.error_codes import ERROR_CODES


class Error(Exception):
    def __init__(self, error_type: str):
        error_data = ERROR_CODES.get(
            error_type, ERROR_CODES['UNKNOWN_ERROR_TYPE'])
        self.error_code = error_data['code']
        self.description = error_data['description']
        super().__init__(self.description)
