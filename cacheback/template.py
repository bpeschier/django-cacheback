from django.utils.encoding import force_text
from .base import Job


class TemplateJob(Job):
    """
    Job for executing a template render and caching the result
    """

    def __init__(self, fragment_name, vary_on, lifetime=None, fetch_on_miss=None):
        super(TemplateJob, self).__init__()
        self.fragment_name = fragment_name
        self.vary_on = vary_on
        if lifetime is not None:
            self.lifetime = int(lifetime)
        if fetch_on_miss is not None:
            self.fetch_on_miss = fetch_on_miss

    def key(self, *args, **kwargs):
        return "%s-%s" % (
            self.fragment_name,
            '.'.join([force_text(v) for v in self.vary_on])
        )

    def get_constructor_kwargs(self):
        return {
            'fragment_name': self.fragment_name,
            'vary_on': self.vary_on,
            'lifetime': self.lifetime
        }

    def fetch(self, nodelist, context):
        return nodelist.render(context)
