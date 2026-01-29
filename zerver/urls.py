from django.urls import path
from zerver.views.message_recap import message_recap

try:
    urlpatterns += [
        path("json/ai/message_recap", message_recap, name="message_recap"),
    ]
except NameError:
    urlpatterns = [
        path("json/ai/message_recap", message_recap, name="message_recap"),
    ]