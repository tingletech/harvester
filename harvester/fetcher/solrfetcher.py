# -*- coding: utf-8 -*-
import solr
import pysolr
from ..collection_registry_client import Collection
from .fetcher import Fetcher

class SolrFetcher(Fetcher):
    def __init__(self, url_harvest, query, **query_params):
        super(SolrFetcher, self).__init__(url_harvest, query)
        self.solr = solr.Solr(url_harvest)  # , debug=True)
        self.query = query
        self.resp = self.solr.select(self.query)
        self.numFound = self.resp.numFound
        self.index = 0

    def next(self):
        if self.index < len(self.resp.results):
            self.index += 1
            return self.resp.results[self.index-1]
        self.index = 1
        self.resp = self.resp.next_batch()
        if not len(self.resp.results):
            raise StopIteration
        return self.resp.results[self.index-1]


class PySolrFetcher(Fetcher):
    def __init__(self, url_harvest, query, **query_params):
        super(PySolrFetcher, self).__init__(url_harvest, query)
        self.solr = pysolr.Solr(url_harvest, timeout=1)
        self.queryParams = {'q':query, 'sort':'id asc', 'wt':'json',
                'cursorMark':'*'}
        self.get_next_results()
        self.numFound = self.results['response'].get('numFound')
        self.index = 0

    def set_select_path(self):
        '''Set the encoded path to send to Solr'''
        queryParams_encoded = pysolr.safe_urlencode(self.queryParams)
        self.selectPath = 'query?{}'.format(queryParams_encoded)

    def get_next_results(self):
        self.set_select_path()
        resp = self.solr._send_request('get', path=self.selectPath)
        self.results = self.solr.decoder.decode(resp)
        self.nextCursorMark = self.results.get('nextCursorMark')
        self.iter = self.results['response']['docs'].__iter__()

    def next(self):
        try:
            next_result = self.iter.next()
            self.index += 1
            return next_result
        except StopIteration:
            if self.index >= self.numFound:
                raise StopIteration
        self.queryParams['cursorMark'] = self.nextCursorMark
        self.get_next_results()
        if self.nextCursorMark == self.queryParams['cursorMark']:
            if self.index >= self.numFound:
                raise StopIteration
        if len(self.results['response']['docs']) == 0:
            raise StopIteration
        self.index += 1
        return self.iter.next()



# Copyright © 2016, Regents of the University of California
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

