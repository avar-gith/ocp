# file: adan/serializers.py

from rest_framework import serializers
from .models import Model, Type, Personality, LearningPath, API

class APISerializer(serializers.ModelSerializer):
    class Meta:
        model = API
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class PersonalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Personality
        fields = '__all__'

class LearningPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningPath
        fields = '__all__'

class ModelSerializer(serializers.ModelSerializer):
    type = TypeSerializer(read_only=True)
    personality = PersonalitySerializer(read_only=True)
    learning_paths = LearningPathSerializer(many=True, read_only=True)
    apis = APISerializer(many=True, read_only=True)

    class Meta:
        model = Model
        fields = ['name', 'type', 'personality', 'learning_paths', 'apis', 'is_active']
