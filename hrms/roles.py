from rest_framework_roles.roles import is_user, is_anon, is_admin


ROLES = {
    'admin': is_admin,
    'user': is_user,
    'anon': is_anon,
}
