from django.apps import AppConfig as BaseConfig
from django.utils.translation import gettext_lazy as _


class VoteAppConfig(BaseConfig):
    name = 'vote'
    verbose_name = _('Vote')
