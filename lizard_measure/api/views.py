from django.core.urlresolvers import reverse

from djangorestframework.views import View


class RootView(View):
    """
    Startpoint.
    """
    def get(self, request):
        return {
            "measure": reverse("lizard_measure_api_measure_list"),
            }
