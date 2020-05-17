from django.dispatch import Signal


post_voted = Signal(providing_args=["obj", "user", "action"])
