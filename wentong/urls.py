'''
Created on 2017年2月15日

@author: xumingze
'''
from django.conf.urls import url
from wentong.views import push_recognize_result


urlpatterns = [
    url(r'devices/(?P<device_id>[\w]+)/car_info/wentong$',
        push_recognize_result)
]
