from django.contrib.auth import get_user_model
from rest_framework import serializers
from hwork.models import Note, User, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username']


class NoteSerializer(serializers.ModelSerializer):

    tags = serializers.ListField(child=serializers.CharField(), write_only=True)
    user = UserSerializer(read_only=True)


    class Meta:
        model = Note
        fields = ['uuid', 'title', "content", 'created_at', "user", "image", "tags"]
        write_only_fields = ["content", 'title', "image", "tags"]

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        note = Note.objects.create(**validated_data)

        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            note.tags.add(tag)

        return note


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
