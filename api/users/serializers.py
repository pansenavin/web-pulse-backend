from rest_framework import serializers
from users.models import User, Role

class UserSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField()
    role_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'dial_code', 'mobile', 'role', 'role_id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        role_id = validated_data.pop('role_id', None)
        
        # Django's AbstractUser requires a username, so we fallback to email
        if 'username' not in validated_data:
            validated_data['username'] = validated_data.get('email')
            
        user = User.objects.create_user(**validated_data)
        if role_id:
            try:
                user.role = Role.objects.get(id=role_id)
            except Role.DoesNotExist:
                pass
        else:
            # Default to "user" role
            role, created = Role.objects.get_or_create(role_name='user')
            user.role = role
        user.save()
        return user
