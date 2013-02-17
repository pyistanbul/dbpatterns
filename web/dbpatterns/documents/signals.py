import django.dispatch

assignment_done = django.dispatch.Signal(providing_args=["instance", "user_id"])
star_done = django.dispatch.Signal(providing_args=["instance", "user"])
fork_done = django.dispatch.Signal(providing_args=["instance"])
document_done = django.dispatch.Signal(providing_args=["instance"])
document_delete = django.dispatch.Signal(providing_args=["instance"])
fork_delete = django.dispatch.Signal(providing_args=["instance"])