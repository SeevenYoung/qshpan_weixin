# coding: UTF-8
import os
import sys

import sae
import web

app_root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(app_root, 'virtualenv.bundle.zip'))
from weixinInterface import WeixinInterface


def app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html; charset=utf-8')]
    start_response(status, response_headers)
    return ['<strong>Welcome to SAE!</strong>']


templates_root = os.path.join(app_root, 'templates') 
render = web.template.render(templates_root)

import config
import discuz
urls = (
'/weixin','WeixinInterface',
'/','Hello'
)

class Hello:
    def GET(self):
        my_account = discuz.Discuz()
        url = r'http://bbs.stuhome.net/'
        my_account.login(config.username, config.password)
        my_account.refresh(url)
        return render.hello("你好")

app = web.application(urls, globals()).wsgifunc()        
application = sae.create_wsgi_app(app)
