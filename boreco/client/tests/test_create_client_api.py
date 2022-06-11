# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient
#
# from client.serializers import ClientSerializer
# from core.models import Client
#
# CLIENT_URL = reverse('client:client-list')
#
#
# # CLIENT_URL_DETAIL = reverse('client:client_detail')
#
#
# # def detail_url(client_id):
# #     """Return client detail url"""
# #     return reverse(CLIENT_URL_DETAIL, args=[client_id])
#
#
# def sample_client(user, **params):
#     """Create and return a sample recipe"""
#     defaults = {
#         "client_name": "boreco",
#         "cvr": "123445",
#         "version": 1
#
#     }
#     defaults.update(params)
#     return Client.objects.create(user=user, **defaults)
#
#
# class TestPublicApiRecipeTest(TestCase):
#     def setUp(self) -> None:
#         self.client = APIClient()
#
#     def test_auth_required(self):
#         """Test that authentication is required"""
#         res = self.client.get(CLIENT_URL)
#         self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
#
#
# class TestPrivateClientApiTests(TestCase):
#     """Test unauthenticated clients api access"""
#
#     def setUp(self) -> None:
#         self.client = APIClient()
#         self.user = get_user_model().objects.create_user(
#             "paco@gmail.com", "pacc1234"
#         )
#         self.client.force_authenticate(self.user)
#
#     def test_retrieve_Clients(self):
#         """Test retrieve a list of clients"""
#         sample_client(user=self.user)
#         sample_client(user=self.user)
#
#         res = self.client.get(CLIENT_URL)
#         clients = Client.objects.all().order_by('id')
#         serializer = ClientSerializer(clients, many=True)
#         self.assertEqual(res.data, serializer.data)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#
#     def test_clients_limited_to_user(self):
#         """Test retrieve client for user"""
#         user2 = get_user_model().objects.create_user(
#             "man@gmail.com", "man12344"
#         )
#         sample_client(user=user2)
#         sample_client(user=self.user)
#         res = self.client.get(CLIENT_URL)
#         clients = Client.objects.filter(user=self.user)
#         serializer = ClientSerializer(clients, many=True)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(res.data), 1)
#         self.assertEqual(res.data, serializer.data)
#
#     def test_create_client(self):
#         """Test creating a client"""
#         payload = {
#             "client_name": "boreco",
#             "cvr": "123445",
#             "version": 1
#         }
#         res = self.client.post(CLIENT_URL, payload)
#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)
#         client = Client.objects.get(id=res.data['id'])
#         for key in payload.keys():
#             self.assertEqual(payload[key], getattr(client, key))
