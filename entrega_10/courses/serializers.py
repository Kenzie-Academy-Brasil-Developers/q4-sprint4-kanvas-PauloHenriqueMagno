from rest_framework import serializers
from datetime import datetime

from users.serializers import UserSerializer

class CreateCourseSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    name = serializers.CharField()
    demo_time = serializers.TimeField()
    link_repo = serializers.URLField()

    def validate(self, data):
        data['created_at'] = datetime.now()

        return data

class CourseSerializer(serializers.Serializer):
    uuid = serializers.CharField(read_only=True)
    name = serializers.CharField()
    demo_time = serializers.TimeField()
    created_at = serializers.DateTimeField(read_only=True)
    link_repo = serializers.URLField()
    
    instructor = UserSerializer()

    students = UserSerializer(many = True)

class UpdateCourseSerializer(serializers.Serializer):
    name = serializers.CharField(required = False)
    demo_time = serializers.TimeField(required = False)
    link_repo = serializers.CharField(required = False)

class RegisterInstructorInCourseSerializer(serializers.Serializer):
    instructor_id = serializers.UUIDField()

class RegisterStudentsInCourseSerializer(serializers.Serializer):
    students_id = serializers.ListField(
        child = serializers.UUIDField()
    )