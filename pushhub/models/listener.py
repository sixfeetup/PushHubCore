"""
Copyright (c) 2013, Regents of the University of California
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

  * Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

  * Neither the name of the University of California nor the names of its
    contributors may be used to endorse or promote products derived from this
    software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

"""
Listeners are subscribers that wish to be notified any time
a new topic is added to the hub.
"""

from persistent import Persistent
from repoze.folder import Folder
import requests

from pyramid.threadlocal import get_current_request
from zope.interface import Interface, implements

from .topic import Topics
from ..utils import is_valid_url

import logging
logger = logging.getLogger(__name__)


class Listeners(Folder):
    """Folder to hold listeners"""
    title = "Listeners"


class IListener(Interface):
    """Marker interface for listeners"""
    pass


class Listener(Persistent):
    implements(IListener)

    def __init__(self, callback_url):
        if not is_valid_url(callback_url):
            raise ValueError(
                'Malformed URL: %s'
            )
        self.callback_url = callback_url
        self.topics = Topics()

    def notify(self, topic_urls):
        logger.debug('Notify listener: %s' % self.callback_url)
        request = get_current_request()
        response = requests.get(
            self.callback_url,
            params={"hub.urls": topic_urls,
                    "hub.callback": request.route_url('subscribe')})
        return response
