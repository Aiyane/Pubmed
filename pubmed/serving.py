#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from wsgiref import WSGIServer, WSGIRequestHandler


def make_server(
        host, port, app, server_class=WSGIServer, handler_class=WSGIRequestHandler):
    """
    创建服务器
    """
    pass
