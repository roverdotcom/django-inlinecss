from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from builtins import object

import pynliner


class EngineBase(object):
    def __init__(self, html, css):
        self.html = html
        self.css = css

    def render(self):
        raise NotImplementedError()


class PynlinerEngine(EngineBase):
    def render(self):
        inliner = pynliner.Pynliner().from_string(self.html)
        inliner = inliner.with_cssString(self.css)
        return inliner.run()


class NullEngine(EngineBase):
    def render(self):
        return self.html
