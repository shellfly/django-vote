from django.apps import AppConfig as BaseConfig
from django.utils.translation import ugettext_lazy as _


class VoteAppConfig(BaseConfig):
    name = 'vote'
    verbose_name = _('Vote')
