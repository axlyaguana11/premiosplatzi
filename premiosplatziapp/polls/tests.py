import datetime 

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from polls.models import Question

class QuestionModelTest(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for whose pub_date is in the future.
        """

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for whose pub_date is older than 1 day.
        """

        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    
    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for whose pub_date is within the last day.
        """

        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIdexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropiate message is shown.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question(self):
        """
        Questions with pub_date in the future aren't shown.
        """
        create_question(question_text='Future question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are shown.
        """
        q = create_question(question_text='Past question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [q])

    def test_future_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions are shown.
        """
        future_question = create_question(question_text='Future question', days=100)
        past_question = create_question(question_text='Past question', days=-100)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question])

    def test_two_past_questions(self):
        """
        Multiple questions can be shown.
        """
        past_question_1 = create_question(question_text='Past question 1', days=-60)
        past_question_2 = create_question(question_text='Past question 2', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [past_question_2, past_question_1])


class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        """
        If a question with pub_date in the future exists, it returns a 404 error.
        """
        future_question = create_question(question_text='Future question', days=30)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_past_question(self):
        """
        The detail of a quiestion with pub_date in the past is shown.
        """
        past_question = create_question(question_text='Past question', days=-30)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)