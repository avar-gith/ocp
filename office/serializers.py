# file: office/serializers.py

from rest_framework import serializers
from .models import Email
from organization.models import Employee

class EmailSerializer(serializers.ModelSerializer):
    """
    Serializer az e-mailek modellhez.
    """
    sender_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        source='sender',
        write_only=True,
        required=True,
        label='Küldő'
    )

    class Meta:
        model = Email
        fields = ['sender_id', 'sent_at', 'content']
        read_only_fields = ['sent_at']  # A 'sent_at' mező csak olvasható, nem szerkeszthető

# file: office/serializers.py

from rest_framework import serializers
from .models import WikiPage
from organization.models import Employee

class WikiPageSerializer(serializers.ModelSerializer):
    """
    Serializer a wiki oldalak modellhez.
    """
    created_by_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        source='created_by',
        write_only=True,
        required=True,
        label='Készítő'
    )

    class Meta:
        model = WikiPage
        fields = ['title', 'description', 'created_by_id', 'created_at']
        read_only_fields = ['created_at']  # A 'created_at' mező csak olvasható, nem szerkeszthető
