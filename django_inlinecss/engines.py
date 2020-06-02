import pynliner


class EngineBase:
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
