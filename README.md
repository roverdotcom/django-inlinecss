## About

Inlining CSS is necessary for email generation and sending
but is currently a suprisingly large hassle.

This library aims to make it a breeze for in the Django
template language.

## Usage

#### Step 1: Dependencies

- BeautifulSoup
- cssutils
- Python 2.7 (for tests anyway)
- Django 1.3 (relies on contrib.staticfiles)

#### Step 2: Install django_inlinecss

Add ```django_inlinecss``` to your ```settings.py```:

```python
INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.webdesign',
        'django.contrib.contenttypes',
        '...',
        '...',
        '...',
        'django_inlinecss')
```

#### Step 3: Use the templatetag

1. Place your CSS file somewhere staticfiles can find it
2. Create your template:

```html
{% load inlinecss %}
{% inlinecss "css/extra-padding.css" %}
    <html>
        <body>
            <div class='lots-o-padding'>
                Something in need of styling.
            </div>
        </body>
    </html>
{% endinlinecss %}
```

#### Step 4: Prepare to be Wowed

```html
<html>
    <body>
        <div style="padding-left: 10px; padding-right: 10px; padding-top: 10px;" class="lots-o-padding">
            Something in need of styling.
        </div>
    </body>
</html>
```

## Acknowledgements

Thanks to Tanner Netterville for his efforts on [Pynliner](https://github.com/rennat/pynliner).

Thanks to Thomas Yip for his hard work on the soupselect module included in this
(specifically on writing extensive unit tests for most of the functionality found in CSS2).
Without his efforts only the most basic selectors would work.

## License

MIT license. See LICENSE.md for more detail.
