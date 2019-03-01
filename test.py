from __future__ import print_function

import json
from io import BytesIO

from twisted.internet import reactor
from twisted.web.client import Agent, FileBodyProducer
from twisted.web.http_headers import Headers

agent = Agent(reactor)

d = agent.request(
    b'POST',
    b'http://localhost:8080',
    Headers({'User-Agent': ['Twisted Web Client Example']}),
    FileBodyProducer(BytesIO(bytes(json.dumps(['user', 'register', 'nick', 'login', 'password']), "utf-8"))))


def cbResponse(ignored):
    print('Response received')
    print(ignored.code)
d.addCallback(cbResponse)


def cbShutdown(ignored):
    print(ignored)
    reactor.stop()
d.addBoth(cbShutdown)

reactor.run()