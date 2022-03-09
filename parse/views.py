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
            context['links'] = get_links(url, 2)

    except ValidationError as e:
        context['error'] = 'URL is not valid' 

    return render(request, 'parse/index.html', context)


def get_links(url, max_level=4):
    if max_level == 0:
        return dict() 
    
    domain = urlparse(url).netloc
    scheme = urlparse(url).scheme
    try:
        html_page = urllib.request.urlopen(url)
    except HTTPError as e:
        # skip the page
        return dict() 
    soup = BeautifulSoup(html_page, "html.parser")
    links = dict()
    for link in soup.findAll('a'):
        href = link.get('href')
        if href is not None:
            if href.startswith('/'):
                href = f'{scheme}://{domain}{href}'
            if href.startswith('#'):
                href = url+href
            links[href] = get_links(href, max_level=max_level-1)
    return links
