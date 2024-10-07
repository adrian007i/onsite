from django.contrib.auth.decorators import user_passes_test

def role_required(role):
    def in_role(u): 
        return u.is_authenticated and u.role == role

    return user_passes_test(in_role)
