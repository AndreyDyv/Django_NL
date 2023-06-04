from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from students.models import Course, Student


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def create(self, validated_data):
        if Student.objects.count() > settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError
