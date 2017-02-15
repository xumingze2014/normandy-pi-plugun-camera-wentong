'''
Created on 2017年2月15日

@author: xumingze
'''
try:
    from device.camera import Camera
except:
    from wentong import Camera


import socket
import json
import struct
import logging

logger = logging.getLogger('default')


class WenTongCamera(Camera):

    def __init__(self, camera):
        Camera.__init__(self, camera)

    def gate(self):
        self._send_cmd({
            "cmd": "ioctl",
            "io": int(self.camera.deploy['output']) - 1,
            "value": 2,
            "delay": 500
            })
        return True

    def _send_cmd(self, cmd, need_return=False):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.camera.ip_addr, 8131))
            cmd = json.dumps(cmd)
            length = len(cmd)
            header = ['V', 'Z', 0, 0, 0, 0, 0, 0]
            header[4] += ((length >> 24) & 0xFF)
            header[5] += ((length >> 16) & 0xFF)
            header[6] += ((length >> 8) & 0xFF)
            header[7] += (length & 0xFF)
            f = '!ssBBBBBB%ds' % length
            _msg = struct.pack(
                f, "V".encode(), "Z".encode(), 0, 0, header[4],
                header[5], header[6], header[7], cmd.encode()
                )
            sock.send(_msg)
            logger.info('send zhenshi cmd:%s' % cmd)
            if need_return:
                return sock.recv(1024)
        except Exception as e:
            logger.exception(e)
        finally:
            sock.close()
