## About

Inlining CSS is necessary for email generation and sending
but is currently a suprisingly large hassle.

This library aims to make it a breeze for in the Django
template language.

## Usage

#### Step 1: Dependencies

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
        <div style="padding-left: 10px; padding-right: 10px; padding-top: 10px;">
            Something in need of styling.
        </div>
    </body>
</html>
```

## Acknowledgements

Thanks to Tanner Netterville for his efforts on [Pynliner](https://github.com/rennat/pynliner).

Thanks to Thomas Yip for his unit tests on the `soupselect` module. These tests
helped on getting the core CSS2 selectors to work.

## License

MIT license. See LICENSE.md for more detail.
