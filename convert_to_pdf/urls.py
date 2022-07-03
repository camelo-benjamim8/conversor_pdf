from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from convert_to_pdf.views import converter_pdf
urlpatterns = [
    path('',converter_pdf)
]
