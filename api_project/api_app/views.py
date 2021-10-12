# Create your views here.
import logging
import json
import requests
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from urllib.request import urlopen

def get_remote_api(query):
    query_string = f'https://infrastructure.tech/wp-json/{query}'
    logging.info(f"Running query: {query_string}")
    return requests.get(query_string).content.decode("ascii")


def publish_package(request):
    required_vars = ['username', 'password', 'package_name', 'version']
    for var in required_vars:
        if var not in request.POST:
            return HttpResponseBadRequest(f"Please specify {var} in POST")

    if 'package' not in request.FILES:
        return HttpResponseBadRequest(f"Package file not found.")

    url = 'https://infrastructure.tech/wp-json/gf/v2/forms/1/submissions'
    username = request.POST['username']
    password = request.POST['password']
    package_name = request.POST['package_name']
    version = request.POST['version'],
    visibility = 'private'
    if 'visibility' in request.POST:
        visibility = request.POST['visiblity']
    file = request.FILES['package']
    data = {
        'input_1' : package_name,
        'input_2' : version,
        'input_4' : visibility
    }
    files = {
        'input_3' : file
    }

    response = requests.post(url, auth=requests.auth.HTTPBasicAuth(username, password), data=data, files=files)
    return response


def download_package(request):
    required_vars = ['package_name']
    for var in required_vars:
        if var not in request.POST:
            return HttpResponseBadRequest(f"Please specify {var} in POST")

    package_name = request.POST['package_name']
    url = f'https://infrastructure.tech/wp-json/wp/v2/package?slug={package_name}'

    package_query = None

    if ['username', 'password'] in request.POST:
        url = url + '&status=private'
        username = request.POST['username']
        password = request.POST['password']
        package_query = requests.get(url, auth=requests.auth.HTTPBasicAuth(username, password)).content.decode("ascii")
    else:
        package_query = requests.get(url).content.decode("ascii")

    if not package_query:
        return HttpResponseNotFound(f"No package {package_name}")

    package_json = json.loads(package_query)[0]
    file_url = package_json['file']

    response = HttpResponse(urlopen(file_url), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{package_name}.zip"'

def index(request):
    return HttpResponse("It works!")