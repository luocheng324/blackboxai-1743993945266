from rest_framework import serializers

class ComponentSerializer(serializers.Serializer):
    id = serializers.CharField()
    type = serializers.CharField()
    parameters = serializers.JSONField()
    connections = serializers.ListField(
        child=serializers.DictField()
    )

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    analysis_type = serializers.CharField()