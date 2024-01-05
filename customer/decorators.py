from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def user_type_required(user_type_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.user_type == user_type_name:
                return redirect("not_allowed")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
