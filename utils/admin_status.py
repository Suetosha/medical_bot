from database.repositories.user_repository import UserRepository


async def change_admin_status(session, user_id):
    user_repo = UserRepository(session)
    await user_repo.update_admin_status(user_id=user_id)
    new_admin_status = await user_repo.get_admin_status(user_id)
    return new_admin_status
