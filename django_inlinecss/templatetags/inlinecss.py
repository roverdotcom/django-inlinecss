from django import template

from django.contrib.staticfiles.storage import staticfiles_storage

from django_inlinecss import pynliner

register = template.Library()


class InlineCssNode(template.Node):
    def __init__(self, nodelist, *args):
        self.nodelist = nodelist
        self.paths = args

    def render(self, context):
        rendered_contents = self.nodelist.render()
        css = ''
        for arg in self.args:
            css_path = staticfiles_storage.path(arg)
            with open(css_path) as css_file:
                ''.join((css, css_file.read()))

        inliner = Pynliner().from_string(rendered_contents)
        inliner = inliner.with_cssString(css)
        return inliner.run()


@register.tag
def inlinecss(parser, token):
    nodelist = parser.parse(('endinlinecss',))
    parser.delete_first_token()

    args = token.split_contents()

    return InlineCssNode(nodelist, *args)
