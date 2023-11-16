from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Profile

class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Profile
        fields = ('email', 'username', 'address', 'phone')



class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2', 'profile')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data


    def create(self, validated_data):
        validated_data.pop('password2')

        profile_data = validated_data.pop('profile')

        user = User.objects.create_user(**validated_data)

        existing_profile = user.profile

        if existing_profile:
            existing_profile.address = profile_data.get('address', existing_profile.address)
            existing_profile.phone = profile_data.get('phone', existing_profile.phone)
            existing_profile.save()
        else:
            Profile.objects.create(user=user, **profile_data)

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if email and password:
            user = User.objects.filter(email=email).first()

            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                data['refresh'] = str(refresh)
                data['access'] = str(refresh.access_token)
                self.user = user
            else:
                raise serializers.ValidationError("Invalid credentials. Please try again.")
        else:
            raise serializers.ValidationError("Both email and password are required.")

        return data


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'confirm_password', 'profile', 'token')
        extra_kwargs = {
            'profile': {'read_only': True},
            'username': {'required': False},
            'email': {'required': False},
        }

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def validate(self, data):
        if 'password' in data and 'confirm_password' in data:
            if data['password'] != data['confirm_password']:
                raise serializers.ValidationError("Passwords do not match.")
        return data

    def update(self, instance, validated_data): # to display on User Model
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)

        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()

        return instance


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    def validate(self, attrs):
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        fields = ['email']



class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)

    def validate(self, data):
        if not data.get('new_password'):
            raise serializers.ValidationError("New password is required.")
        return data

