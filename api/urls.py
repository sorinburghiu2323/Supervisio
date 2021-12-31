from django.urls import path, include
from django.http import HttpResponse
from django.conf.urls import url


def generate_api_urls(name):
    regex = r"^{}/".format(name)
    to_include = include("api.{}.urls".format(name))
    namespace = "api.{}".format(name)
    return url(regex, to_include, name=namespace)


api_namespaces = [
    "users",
    "interests",
    "projects",
]

urlpatterns = [
    path("", lambda _: HttpResponse("Supervisio API", status=200)),
    url(
        r"",
        include(
            [url(r"", include([generate_api_urls(name) for name in api_namespaces]))]
        ),
    ),
]
