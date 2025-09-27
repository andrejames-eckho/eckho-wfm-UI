from .user_service import UserService
from .time_record_service import TimeRecordService

# Initialize services
user_service = UserService()
time_record_service = TimeRecordService()

__all__ = [
    'user_service',
    'time_record_service',
    'UserService',
    'TimeRecordService'
]
