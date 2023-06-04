import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


# 1 проверка получения первого курса (retrieve-логика)
@pytest.mark.django_db
def test_get_course(client, course_factory):
    course = course_factory()
    url = reverse('courses-list')
    response = client.get(url)

    assert response.status_code == HTTP_200_OK
    assert course.id


# 2 проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_get_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')
    response = client.get(url)

    assert response.status_code == HTTP_200_OK
    assert len(courses) == len(response.data)
    assert all([course.name == response.data[num]['name'] for num, course in enumerate(courses)])


# 3 проверка фильтрации списка курсов по id
@pytest.mark.django_db
def test_get_course_id(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')
    course = courses[2]
    response_id = client.get(url, {'id': course.id})

    assert response_id.status_code == HTTP_200_OK
    assert course.id == response_id.data[0]['id']


# 4 проверка фильтрации списка курсов по name
@pytest.mark.django_db
def test_get_course_name(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')
    course = courses[4]
    response_name = client.get(url, {'name': course.name})

    assert response_name.status_code == HTTP_200_OK
    assert course.name == response_name.data[0]['name']


# 5 тест успешного создания курса
@pytest.mark.django_db
def test_create_course(client):
    url = reverse('courses-list')
    response = client.post(url, data={'name': 'for_test'})
    assert response.status_code == HTTP_201_CREATED

    response = client.get(url)
    assert response.data[0]['name'] == 'for_test'


# 6 тест успешного обновления курса
@pytest.mark.django_db
def test_update_course(client, course_factory):
    course = course_factory(_quantity=1)
    url = reverse('courses-detail', args=[course[0].pk])
    response = client.put(url, data={'name': 'new_course'})
    assert response.status_code == HTTP_200_OK

    response = client.get(url)
    assert response.data['name'] == 'new_course'


# 7 тест успешного удаления курса.
@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory(_quantity=1)
    url = reverse('courses-detail', args=[course[0].pk])
    response = client.delete(url)
    assert response.status_code == HTTP_204_NO_CONTENT
    response = client.get(url)
    assert response.status_code == HTTP_404_NOT_FOUND
