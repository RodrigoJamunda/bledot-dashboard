from .auth_handler import authenticate, logout
from .db_manager import add_user, change_password, list_users, delete_user, get_user_role

# Exportar funções relevantes
__all__ = [
    'authenticate',
    'logout',
    'add_user',
    'change_password',
    'list_users', 
    'delete_user',
    'get_user_role'
]