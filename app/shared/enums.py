from enum import Enum

class ResponseCode(str, Enum):
    # 2xx Success codes
    SUCCESS = "200"
    CREATED = "201"
    ACCEPTED = "202"
    
    # 4xx Client error codes
    BAD_REQUEST = "400"
    UNAUTHORIZED = "401"
    FORBIDDEN = "403"
    NOT_FOUND = "404"
    CONFLICT = "409"
    UNPROCESSABLE_ENTITY = "422"
    
    # 5xx Server error codes
    INTERNAL_SERVER_ERROR = "500"
    SERVICE_UNAVAILABLE = "503"
    
class PracticeState(str, Enum):
    COMPLETED = "COMPLETED" # Audio/video analysis and report done
    ANALYZED = "ANALYZED" # Audio/video analysis done, report pending
    IN_PROGRESS = "IN_PROGRESS" # Audio/video analysis or report in progress
    FINISHED = "FINISHED" # Audio/video analysis and report done and user deleted video in local
    
class Figure(Enum):
    BLANCA = 0.5
    NEGRA = 1
    CORCHEA = 2

    @classmethod
    def to_str(cls, value):
        mapping = {
            cls.BLANCA.value: "Blanca",
            cls.NEGRA.value: "Negra",
            cls.CORCHEA.value: "Corchea",
        }
        return mapping.get(value, "Desconocido")