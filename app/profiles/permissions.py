from rest_framework import permissions


class OnboardingPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_onboarding:
            return False
