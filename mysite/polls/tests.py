from django.test import TestCase

# Create your tests here.
import datetime

from django.utils import timezone
from django.urls import reverse
from .models import Question

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days = days)
    return Question.objects.create(question_text = question_text, pub_date = time)

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days = 30)
        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        # test pub_date is one day more older than now
        time = timezone.now() - datetime.timedelta(days = 1, seconds = 1)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        # test pub_date is one day less older than now
        time = timezone.now() - datetime.timedelta(hours = 23, minutes = 59, seconds = 59)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(), True)

class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        question = create_question(question_text = 'Past question', days = -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])

    def test_future_question(self):
        question = create_question(question_text = 'Future question', days = 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_two_past_question(self):
        question1 = create_question(question_text = 'Past question 1', days = -10)
        question2 = create_question(question_text = 'Past question 2', days = -20)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question1, question2])

    def test_past_future_question(self):
        question1 = create_question(question_text = 'Past question', days = -10)
        create_question(question_text = 'Future question', days = 10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question1])

class QuestionDetailViewTests(TestCase):
    def test_past_question(self):
        question = create_question(question_text = 'Past question', days = -5)
        url = reverse('polls:detail', args = (question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_future_question(self):
        question = create_question(question_text = 'Future question', days = 10)
        url = reverse('polls:detail', args = (question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)