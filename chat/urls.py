from django.conf.urls import url
from django.urls import path, include
from .views import ConvPartnerView, ConvMessageView


urlpatterns = [
    url('conversation/partners/$', ConvPartnerView.as_view(), name='conv-partners'),
    url('conversation/messages/(?P<pk>\d+)/$', ConvMessageView.as_view(), name='conv-messages'),
]