from rest_framework import serializers
from .models import Email
from organization.models import Employee
from organization.serializers import EmployeeSerializer  # Importáljuk a részletes EmployeeSerializer-t

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
    sender = EmployeeSerializer()  # A küldő részleteit teljes adatvisszaküldéssel biztosítjuk

    class Meta:
        model = Email
        fields = ['id', 'sender_id', 'sender', 'subject', 'sent_at', 'content']  # Hozzáadjuk az 'id'-t
        read_only_fields = ['id', 'sent_at']  # Az 'id' és 'sent_at' csak olvasható

# file: office/serializers.py

from rest_framework import serializers
from .models import WikiPage  # Importáljuk a WikiPage modellt
from organization.models import Employee  # Importáljuk az Employee modellt
from organization.serializers import EmployeeSerializer  # Importáljuk a részletes EmployeeSerializer-t

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
    created_by = EmployeeSerializer()  # A készítő részleteit is visszaküldjük

    class Meta:
        model = WikiPage
        fields = ['title', 'description', 'created_by_id', 'created_by', 'created_at']  # Visszaküldjük a készítőt is
        read_only_fields = ['created_at']  # A 'created_at' mező csak olvasható
