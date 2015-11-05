from rest_framework import permissions


class IMDBUserPermission(permissions.IsAuthenticated):
    """
    Custom User permission
    """
    def has_permission(self, request, view):
        """
        Check user permission with different role
        Admin user if is_staff flag is set otherwise its an normal user
        Ignoring the django super admin flag :).
        """
        is_allowed = False
        # Call super to get user authentication
        is_authentic = super(IMDBUserPermission, self).has_permission(request, view)
        req_method = request.method

        # Check if user has admin permission i.e is_staff flag set
        admin_user = getattr(request.user, 'is_staff', False) if request.user else False
        if is_authentic and req_method == 'GET':
            is_allowed = True
        elif is_authentic and admin_user and req_method in ('POST', 'PUT', 'DELETE',):
            is_allowed = True
        return is_allowed
