import django.dispatch

comment_done = django.dispatch.Signal(providing_args=["comment_id"])
comment_delete = django.dispatch.Signal(providing_args=["comment_id"])