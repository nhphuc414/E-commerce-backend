from rest_framework import permissions


class OwnerAuthenticated(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view) and request.user == obj.user


class StoreOwnerAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        is_permitted = super().has_permission(request, view)
        is_store_owner = request.user.store is not None
        is_store_active = request.user.store.active is True
        print(request.user.store.active)
        return is_permitted and is_store_owner and is_store_active


class StaffOrSuperUserAuthenticated(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        is_permitted = self.has_permission(request, view)
        is_staff_or_superuser = request.user.is_staff or request.user.is_superuser
        return is_permitted and is_staff_or_superuser
