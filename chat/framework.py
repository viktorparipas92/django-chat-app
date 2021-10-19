from django.db import transaction
from rest_framework import permissions, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response


class ModelPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.can_read(request.user)
        elif request.method == 'POST':
            if getattr(view, 'action', None) == 'create':
                return obj.can_create(request.user)
            else:
                return obj.can_update(request.user)
        elif request.method in ['PUT', 'PATCH']:
            return obj.can_update(request.user)
        elif request.method == 'DELETE':
            return obj.can_delete(request.user)

        return False


class ViewMixIn:
    permission_classes = [permissions.IsAuthenticated, ModelPermissions]

    def dispatch(self, request, *args, **kwargs):
        # Wrap POST, PUT, DELETE, etc in a transaction
        if request.method in permissions.SAFE_METHODS:
            return super().dispatch(request, *args, **kwargs)
        else:
            with transaction.atomic():
                return super().dispatch(request, *args, **kwargs)

    def handle_exception(self, *args, **kwargs):
        response = super().handle_exception(*args, **kwargs)
        if not transaction.get_autocommit() and getattr(response, 'exception') and response.exception is True:
            # We've suppressed the exception but still need to rollback any transaction.
            transaction.set_rollback(True)
        return response


class CreateModelMixInWithObjectPermissionCheck(CreateModelMixin):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)

        # This will be available on viewsets
        self.check_object_permissions(request, instance)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()