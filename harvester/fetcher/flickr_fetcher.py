# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import urllib
import re
from .fetcher import Fetcher


class Flickr_Fetcher(Fetcher):
    '''A fetcher for the Flicr API.
    Currently, it takes a user id and grabs the flickr.people.getPublicPhotos
    to get the list of all photos.
    It then proceeds to use flickr.photos.getInfo to get metadata for the
    photos
    '''

    url_get_photos_template = 'https://api.flickr.com/services/rest/' \
        '?api_key={api_key}&user_id={user_id}&per_page={per_page}&method=' \
        'flickr.people.getPublicPhotos&page={page}'
    url_get_photo_info_template = 'https://api.flickr.com/services/rest/' \
        '?api_key={api_key}&method=flickr.photos.getInfo&photo_id={photo_id}'

    def __init__(self, url_harvest, extra_data, page_size=500):
        self.url_base = url_harvest
        self.user_id = extra_data
        self.api_key = os.environ.get('FLICKR_API_KEY', 'boguskey')
        self.page_size = page_size
        self.page_current = 1
        self.doc_current = 1
        self.docs_fetched = 0
        xml = urllib.urlopen(self.url_current).read()
        total = re.search('total="(?P<total>\d+)"', xml)
        self.docs_total = int(total.group('total'))

    @property
    def url_current(self):
        return self.url_get_photos_template.format(
            api_key=self.api_key,
            user_id=self.user_id,
            per_page=self.page_size,
            page=self.page_current)

    def next(self):
        if self.doc_current == self.docs_total:
            if self.docs_fetched != self.docs_total:
                raise ValueError(
                   "Number of documents fetched ({0}) doesn't match \
                    total reported by server ({1})".format(
                        self.docs_fetched,
                        self.docs_total)
                    )
            else:
                raise StopIteration
        return None


# Copyright © 2017, Regents of the University of California
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# - Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# - Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# - Neither the name of the University of California nor the names of its
#   contributors may be used to endorse or promote products derived from this
#   software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
