from blog.models import Blog
from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"

    # Override update to update the field for a user profile
    # since the password need hashing
    def update(self, instance, validated_data):

        for attr, value in validated_data.items():

            if attr != "password":
                setattr(instance, attr, value)

        # password need special hashing.
        password = validated_data.get("password")
        if password:
            instance.set_password(password)

        instance.save()
        return instance


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"
