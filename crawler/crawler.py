#!/usr/bin/python

from utils import http_utils


def fetch_content(url):
    r = http_utils.send_request(url, "GET")
    content = r.text
    #print content
    return content

