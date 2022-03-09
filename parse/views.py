from urllib.error import HTTPError
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib.request
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

# TODO: the links can have duplicates
# TODO: separate ajax request to get the links and show progress spinner
# TODO: add some message if the page has no links

def index(request):
    url = request.GET.get('url')
    validate = URLValidator()
    context = dict() 
    context['url'] = url
    try:
        validate(url)
        if url:
            links = []
            # parse the webpage
            domain = urlparse(url).netloc
            scheme = urlparse(url).scheme
            html_page = urllib.request.urlopen(url)
            soup = BeautifulSoup(html_page, "html.parser")
            for link in soup.findAll('a'):
                href = link.get('href')
                if href is not None:
                    if href.startswith('/'):
                        href = f'{scheme}://{domain}{href}'
                    if href.startswith('#'):
                        href = url+href
                    links.append(href)
            context['links'] = links

    except ValidationError as e:
        context['error'] = 'URL is not valid' 
    except HTTPError as e:
        context['error'] = 'Page not found' 

    return render(request, 'parse/index.html', context)
