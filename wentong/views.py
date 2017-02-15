'''
Created on 2017年2月15日

@author: xumingze
'''
from django.http import HttpResponse
import json
import logging
import requests


logger = logging.getLogger('default')


def push_recognize_result(request, device_id):
    try:
        data = json.loads(request.body.decode())
    except Exception as e:
        print(e)
    data = _transfrom(data['AlarmInfoPlate'])
    _notice_pi(device_id, data)
    return HttpResponse(status=204)


def _notice_pi(device_id, data, retry=3):
    _notice_session = requests.Session()
    for _ in range(retry):
        try:
            _notice_session.post(
                'http://127.0.0.1/devices/%s/car_info' % device_id,
                data=json.dumps(data)
                )
            break
        except BaseException as e:
            _notice_session.close()
            _notice_session = requests.Session()
            logger.exception(e)


def _transfrom(data):
    ipaddr = data['ipaddr']
    data = data['result']
    transfrom_data = {}
    transfrom_data['recognized_id'] = data[
        'PlateResult']['timeStamp']['Timeval']['sec']

    image = {}
    image['image_path'] = 'http://%s/%s' % (
        ipaddr, data['PlateResult']['imagePath']
        )
    image['location_x'] = 0
    image['location_y'] = 0
    image['width'] = 0
    image['height'] = 0
    transfrom_data['images'] = [image]

    car = {}
    car['confidence'] = data['PlateResult']['confidence']
    color_map = ['蓝', '蓝', '黄', '白', '黑', '蓝']
    try:
        car['color'] = color_map[data['PlateResult']['colorType']]
    except IndexError:
        car['color'] = '蓝'
    car['id_info'] = {'car_id': data['PlateResult']['license']}
    transfrom_data['car'] = car
    transfrom_data['imgscap'] = 'data:image;base64,%s' % (
        data['PlateResult']['imageFragmentFile']
        )
    transfrom_data['direction'] = 'unknow'
    return transfrom_data
