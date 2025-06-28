from web.users.shemas import User

def create_user(user: User) -> dict:

    user = user.model_dump()

    return {
        'message': 'success',
        'user': user
    }
