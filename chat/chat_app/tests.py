from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from chat.chat_app import models


TEST_PASSWORD = '1234'


def get_logged_in_client(user):
    client = APIClient()
    user.is_form_authenticated = True
    client.login(username=user.username, password=TEST_PASSWORD)
    return client


class UserViewSetTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='Test')
        self.user.set_password(TEST_PASSWORD)
        self.user.save()
        self.client = get_logged_in_client(self.user)

        self.staff_user = User.objects.create_user(username='admin')
        self.staff_user.set_password(TEST_PASSWORD)
        self.staff_user.is_staff = True
        self.staff_user.save()
        self.staff_client = get_logged_in_client(self.staff_user)

        self.list_url = reverse('user-list')
        self.detail_url = reverse('user-detail', kwargs=dict(pk=self.user.id))

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_list_unauthenticated(self):
        response = APIClient().get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_retrieve_unauthenticated(self):
        response = APIClient().get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create(self):
        data = {
            'username': 'Testname',
            'password': TEST_PASSWORD,
            'first_name': 'Test',
            'last_name': 'Testsson',
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.staff_client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'Test')

    def test_delete(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.staff_client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ConversationViewSetTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='Test')
        self.user.set_password(TEST_PASSWORD)
        self.user.save()
        self.client = get_logged_in_client(self.user)

        self.other_user = User.objects.create_user(username='Other')
        self.other_user.set_password(TEST_PASSWORD)
        self.other_user.save()
        self.other_client = get_logged_in_client(self.other_user)

        self.conversation = models.Conversation.objects.create()
        self.conversation.participants.add(self.user)

        self.list_url = reverse('conversation-list')
        self.detail_url = reverse('conversation-detail', kwargs=dict(pk=self.conversation.id))

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.other_client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_unauthenticated(self):
        response = APIClient().get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['participants'][0], self.user.id)

        response = self.other_client.get(self.detail_url)
        # TODO: Should be 403?
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_unauthenticated(self):
        response = APIClient().get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create(self):
        data = {
            'participants': [self.user.id]
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.other_client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        response = self.other_client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update(self):
        data = {
            'participants': [self.user.id]
        }
        response = self.client.put(self.detail_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class MessageViewSetTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='Test')
        self.user.set_password(TEST_PASSWORD)
        self.user.save()
        self.client = get_logged_in_client(self.user)

        self.friend_user = User.objects.create_user(username='Friend')
        self.friend_user.set_password(TEST_PASSWORD)
        self.friend_user.save()
        self.friend_client = get_logged_in_client(self.friend_user)

        self.other_user = User.objects.create_user(username='Other')
        self.other_user.set_password(TEST_PASSWORD)
        self.other_user.save()
        self.other_client = get_logged_in_client(self.other_user)

        self.conversation = models.Conversation.objects.create()
        self.conversation.participants.add(self.user)
        self.conversation.participants.add(self.friend_user)

        self.message = models.Message.objects.create(sender=self.user, conversation=self.conversation, text='asdasd')

        self.list_url = reverse('message-list')
        self.detail_url = reverse('message-detail', kwargs=dict(pk=self.message.id))

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.friend_client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        response = self.other_client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_list_unauthenticated(self):
        response = APIClient().get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], self.message.text)

        response = self.friend_client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['text'], self.message.text)

        response = self.other_client.get(self.detail_url)
        # TODO: Should be 403?
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_unauthenticated(self):
        response = APIClient().get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create(self):
        data = {
            'conversation': self.conversation.id,
            'sender': self.user.id,
            'text': 'asdasd',
        }
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['text'], 'asdasd')

        response = self.friend_client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        data['sender'] = self.other_user.id
        response = self.other_client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete(self):
        response = self.other_client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.friend_client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)