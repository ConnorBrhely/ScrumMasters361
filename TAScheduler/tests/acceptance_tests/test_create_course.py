from TAScheduler.models import Course
from django.test import TestCase, Client


class TestCreateCourse(TestCase):

    def setUp(self):
        self.monkey = Client()
        self.name = "Test"
        self.number = '001'
        self.term_year = '2024'
        self.term_season = 'Spring'
        self.monkey.post("/create_course/", {
            "name": "Test",
            "number": "001",
            "term_year": "2024",
            "term_season": "Spring"
        }, follow=True)

    def test_create_course(self):
        resp = self.monkey.post("/create_course/", {
            "name": self.name,
            "number": self.number,
            "term_year": self.term_year,
            "tern_season": self.term_season
        }, follow=True)
        self.assertEqual(Course.objects.count(), 1, msg="Course not created successfully, invalid information entered")

    def test_no_name(self):
        self.name = ""
        resp = self.monkey.post("/create_course/", {
            "name": self.name,
            "number": self.number,
            "term_year": self.term_year,
            "tern_season": self.term_season
        }, follow=False)
        self.assertEqual(Course.objects.count(), 0, msg="Course object created with blank name field")

    def test_no_number(self):
        self.number = ""
        resp = self.monkey.post("/create_course/", {
            "name": self.name,
            "number": self.number,
            "term_year": self.term_year,
            "tern_season": self.term_season
        }, follow=False)
        self.assertEqual(Course.objects.count(), 0, msg="Course object created with blank number field")

    def test_no_term_year(self):
        self.term_year = ""
        resp = self.monkey.post("/create_course/", {
            "name": self.name,
            "number": self.number,
            "term_year": self.term_year,
            "tern_season": self.term_season
        }, follow=False)
        self.assertEqual(Course.objects.count(), 0, msg="Course object created with blank term year field")

    def test_no_term_season(self):
        self.term_season = ""
        resp = self.monkey.post("/create_course/", {
            "name": self.name,
            "number": self.number,
            "term_year": self.term_year,
            "tern_season": self.term_season
        }, follow=False)
        self.assertEqual(Course.objects.count(), 0, msg="Course object created with blank term season field")
