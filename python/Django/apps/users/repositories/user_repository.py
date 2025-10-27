from ..models.user_model import User

class UserRepository:
    """ユーザーモデルのリポジトリ。"""

    @staticmethod
    def get_all_users():
        return User.objects.all()

    @staticmethod
    def get_user_by_id(user_id):
        return User.objects.filter(id=user_id).first()

    @staticmethod
    def create_user(**kwargs):
        return User.objects.create(**kwargs)