from django.test import TestCase, Client
from .models import RequestLog


class RequestLoggingMiddlewareTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.logs_url = "/audit/logs/"

    def test_request_logging(self):
        response = self.client.get(self.logs_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(RequestLog.objects.count(), 1)
        log = RequestLog.objects.first()
        self.assertEqual(log.method, "GET")
        self.assertEqual(log.path, self.logs_url)

    def test_request_logging_with_query_params(self):
        response = self.client.get(self.logs_url, {"param": "value"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(RequestLog.objects.count(), 1)
        log = RequestLog.objects.last()
        self.assertEqual(log.method, "GET")
        self.assertEqual(log.path, self.logs_url)
        self.assertEqual(log.query_string, "param=value")
