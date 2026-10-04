from django.test import TestCase
from django.db import IntegrityError, transaction
from django.urls import reverse

from accounts.models import CustomUser
from .models import Confession, Reaction


class ReactionTests(TestCase):
  def setUp(self):
    self.user = CustomUser.objects.create_user(
        email='first@example.com',
        password='test-password',
    )
    self.confession = Confession.objects.create(
        author=self.user,
        content='A test confession',
    )
    self.client.force_login(self.user)

  def test_like_and_unlike_are_separate_mutually_exclusive_choices(self):
    url = reverse('upvote', args=[self.confession.pk])

    liked_response = self.client.post(
        url,
        {'reaction': 'like'},
        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
    )
    self.assertEqual(liked_response.status_code, 200)
    self.assertEqual(
        liked_response.json(),
        {
            'upvotes': 1,
            'like_count': 1,
            'unlike_count': 0,
            'reaction': 'like',
            'liked': True,
            'unliked': False,
        },
    )
    self.assertEqual(Reaction.objects.filter(confession=self.confession).count(), 1)

    unlike_response = self.client.post(
        url,
        {'reaction': 'unlike'},
        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
    )
    self.assertEqual(unlike_response.status_code, 200)
    self.assertEqual(
        unlike_response.json(),
        {
            'upvotes': 0,
            'like_count': 0,
            'unlike_count': 1,
            'reaction': 'unlike',
            'liked': False,
            'unliked': True,
        },
    )
    reaction = Reaction.objects.get(confession=self.confession)
    self.assertFalse(reaction.is_like)

    cleared_response = self.client.post(
        url,
        {'reaction': 'unlike'},
        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
    )
    self.assertIsNone(cleared_response.json()['reaction'])
    self.assertFalse(Reaction.objects.filter(confession=self.confession).exists())

  def test_invalid_reaction_choice_is_rejected(self):
    response = self.client.post(
        reverse('upvote', args=[self.confession.pk]),
        {'reaction': 'heart'},
        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
    )

    self.assertEqual(response.status_code, 400)

  def test_user_can_like_own_confession(self):
    response = self.client.post(
        reverse('upvote', args=[self.confession.pk]),
        {'reaction': 'like'},
        HTTP_X_REQUESTED_WITH='XMLHttpRequest',
    )

    self.assertEqual(response.json()['liked'], True)
    self.assertTrue(
        Reaction.objects.filter(
            user=self.user,
            confession=self.confession,
        ).exists()
    )

  def test_database_rejects_duplicate_user_confession_reaction(self):
    Reaction.objects.create(user=self.user, confession=self.confession)

    with self.assertRaises(IntegrityError), transaction.atomic():
      Reaction.objects.create(user=self.user, confession=self.confession)

  def test_wall_renders_user_like_state_and_unique_count(self):
    Reaction.objects.create(user=self.user, confession=self.confession)

    response = self.client.get(reverse('wall'))

    self.assertContains(response, 'class="reaction-button like-button selected"')
    self.assertContains(
        response,
        '<span class="reaction-count like-count">1</span>',
    )
    self.assertContains(response, 'class="reaction-button unlike-button"')
    self.assertContains(
        response,
        '<span class="reaction-count unlike-count">0</span>',
    )
