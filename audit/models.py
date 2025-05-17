from django.db import models
from django.utils.timezone import now


class RequestLog(models.Model):
    timestamp = models.DateTimeField(default=now)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=2048)
    query_string = models.TextField(blank=True)
    remote_ip = models.GenericIPAddressField(null=True, blank=True)
    user = models.ForeignKey(
        "auth.User", null=True, blank=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"[{self.timestamp}] {self.method} {self.path}"
