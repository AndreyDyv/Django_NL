import pytest
from django.urls import reverse
from model_bakery import baker
from rest_framework.status import HTTP_200_OK
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


# 1 проверка получения первого курса (retrieve-логика):
# создаем курс через фабрику;
# строим урл и делаем запрос через тестовый клиент;
# проверяем, что вернулся именно тот курс, который запрашивали;
@pytest.mark.django_db
def test_get_course(client, course_factory):
    courses = course_factory(_quantity=5)
    url = reverse('courses-list')
    course = courses[2]
    response_name = client.get(url, {'name': course.name})
    response_id = client.get(url, {'id': course.id})

    assert response_name.status_code == HTTP_200_OK
    assert response_id.status_code == HTTP_200_OK
    assert course.name == response_name.data[0]['name']


# 2 проверка получения списка курсов (list-логика):
# аналогично — сначала вызываем фабрики, затем делаем запрос и проверяем результат;

def test_get_courses(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse("courses-list")
    response = client.get(url)

    assert response.status_code == HTTP_200_OK
    # assert courses.id
    assert len(courses) == len(response.data)
    assert all([course.name == response.data[num]['name'] for num, course in enumerate(courses)])
    ...

# 3 проверка фильтрации списка курсов по id:
# создаем курсы через фабрику, передать ID одного курса в фильтр, проверить результат запроса с фильтром;

# 4 проверка фильтрации списка курсов по name;

# 5 тест успешного создания курса:
# здесь фабрика не нужна, готовим JSON-данные и создаём курс;

# 6 тест успешного обновления курса:
# сначала через фабрику создаём, потом обновляем JSON-данными;

# 7 тест успешного удаления курса.
