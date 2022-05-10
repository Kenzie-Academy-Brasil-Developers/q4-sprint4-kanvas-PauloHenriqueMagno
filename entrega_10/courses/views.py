from django.db.utils import IntegrityError

from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from courses.models import Courses
from courses.serializers import (
    CourseSerializer,
    CreateCourseSerializer,
    UpdateCourseSerializer,
    RegisterInstructorInCourseSerializer,
    RegisterStudentsInCourseSerializer
)
from courses.permissions import IsInstructor

from users.models import Users

class CourseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInstructor]

    def get(self, request: Request):
        courses = Courses.objects.all()

        serializer = CourseSerializer(courses, many = True)

        return Response(serializer.data, 200)

    def post(self, request: Request):
        try:
            serializer = CreateCourseSerializer(data = request.data)
            serializer.is_valid(raise_exception = True)

            newCourse = Courses.objects.create(**serializer.validated_data)

            courseSerializer = CourseSerializer(newCourse)

            return Response( courseSerializer.data, 201 )

        except IntegrityError as error:
            if 'UNIQUE' in str(error):
                return Response({"message": "Course already exists"}, 422)

            return Response({ 'message': str(error) }, 400)

class CourseByIdView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInstructor]

    def get(self, request: Request, course_id):
        course = Courses.objects.filter(**{ 'uuid': course_id }).first()

        if not course:
            return Response({ "message": "Course does not exist" }, 404)

        courseSerializer = CourseSerializer(course)

        return Response( courseSerializer.data, 200 )


    def patch(self, request: Request, course_id):
        try:
            serializer = UpdateCourseSerializer(data = request.data)
            serializer.is_valid(raise_exception = True)

            changed = Courses.objects.filter(**{ 'uuid': course_id }).update(**serializer.validated_data)

            if changed == 0:
                return Response({ "message": "Course does not exist" }, 404)

            course = Courses.objects.filter(**{ 'uuid': course_id }).first()

            courseSerializer = CourseSerializer(course)

            return Response( courseSerializer.data, 200)

        except IntegrityError as error:
            if "unique" in str(error).lower():
                return Response({ 'message': 'This course name already exists' }, 422)

            return Response({ 'message': str(error) }, 400)


    def delete(self, request: Request, course_id):
        delete = Courses.objects.filter(**{ 'uuid': course_id }).delete()

        if delete[0] == 0:
            return Response({ "message": "Course does not exist" }, 404)

        return Response( '', 204)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsInstructor])
def registerInstructorInCourse(request: Request, course_id):
    serializer = RegisterInstructorInCourseSerializer(data = request.data)
    serializer.is_valid(raise_exception = True)

    course = Courses.objects.filter(**{ 'uuid': course_id }).first()

    if not course:
        return Response({ "message": "Course does not exist" }, 404)

    instructor = Users.objects.filter(**{ 'uuid': serializer.validated_data['instructor_id'] }).first()

    if not instructor:
        return Response({ "message": "Invalid instructor_id" }, 404)

    if not instructor.is_admin:
        return Response({ "message": "Instructor id does not belong to an admin" }, 422)

    courseWithSelectedInstructor = Courses.objects.filter(**{ 'instructor': instructor }).first()

    if courseWithSelectedInstructor:
        if str(courseWithSelectedInstructor.uuid) != course_id:
            courseWithSelectedInstructor.instructor = None
            courseWithSelectedInstructor.save()

    course.instructor = instructor
    course.save()

    courseSerializer = CourseSerializer(course)

    return Response( courseSerializer.data, 200)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsInstructor])
def registerStudentsInCourse(request: Request, course_id):
    try:
        serializer = RegisterStudentsInCourseSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)

        course = Courses.objects.filter(**{ 'uuid': course_id }).first()

        if not course:
            return Response({ 'message': 'Course does not exist' }, 404)

        for user in serializer.data["students_id"]:
            user = Users.objects.filter(**{ 'uuid': user }).first()

            if not user:
                return Response({ 'message': 'Invalid students_id list'}, 404)

            if user.is_admin:
                return Response({ 'message': 'Some student id belongs to an Instructor'}, 422)

        course.students.set(serializer.data["students_id"])

        courseSerializer = CourseSerializer(course)

        return Response( courseSerializer.data, 200)

    except IntegrityError as error:
        return Response({ 'message': str(error) }, 400)
