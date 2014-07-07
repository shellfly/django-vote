from functools import wraps

def instance_required(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        if self.instance is None:
            raise TypeError("Can't call %s with a non-instance manager" % func.__name__)
        return func(self, *args, **kwargs)
    return inner
