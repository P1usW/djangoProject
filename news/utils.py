from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import SingleObjectMixin


class ErrorMessageMixin:
    """
    Add an error message when the form was submitted unsuccessfully.
    """

    error_message = ""

    def form_invalid(self, form):
        response = super().form_invalid(form)
        error_message = self.get_error_message()
        if error_message:
            messages.error(self.request, error_message)
        return response

    def get_error_message(self):
        return self.error_message


class SuccessAndErrorMessageMixin(SuccessMessageMixin, ErrorMessageMixin):
    """
    Use success and error message mixin
    """


class WithVisitCounterMixin(SingleObjectMixin):
    """
    Add a list of views.
    """

    def get_object(self, *args, **kwargs):
        obj = super().get_object(*args, **kwargs)
        if self.request.user.is_anonymous:
            return obj
        obj.visitors.add(self.request.user)
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['visits'] = self.object.visitors.count()
        return context
