from ..repositories.user_repository import UserRepository

class UserService:
    """Service layer for User operations."""

    @staticmethod
    def list_users():
        return UserRepository.get_all_users()

    @staticmethod
    def get_user(user_id):
        return UserRepository.get_user_by_id(user_id)

    @staticmethod
    def create_user(data):
        return UserRepository.create_user(**data)