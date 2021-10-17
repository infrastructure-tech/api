# Create your views here.
import logging
import json
import requests
import base64
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound


def publish_package(request):
    required_vars = ['package_name', 'version']
    for var in required_vars:
        if var not in request.POST:
            return HttpResponseBadRequest(f"Please specify {var} in POST")

    if 'package' not in request.FILES:
        return HttpResponseBadRequest(f"Package file not found.")

    url = 'https://infrastructure.tech/wp-json/gf/v2/forms/1/submissions'
    username, password = get_auth(request)
    package_name = request.POST['package_name']
    version = request.POST['version'],

    visibility = 'private'
    if 'visibility' in request.POST:
        visibility = request.POST['visibility']
        if visibility not in ['private', 'publish']:
            return HttpResponseBadRequest(f"Visibility must be one of 'private' or 'publish'")

    package_type = ''
    if 'package_type' in request.POST:
        package_type = request.POST['package_type']
    else: #try to guess
        decomposed_name = package_name.split('_')
        if len(decomposed_name) > 1:
            package_type = decomposed_name[0]

    description = ''
    if 'description' in request.POST:
        file = request.FILES['package']
        description = request.POST['description']

    data = {
        'input_1': package_name,
        'input_2': version,
        'input_4': visibility,
        'input_5': package_type,
        'input_6': description
    }
    files = {
        'input_3': file
    }

    response = requests.post(url, auth=requests.auth.HTTPBasicAuth(username, password), data=data, files=files)
    return HttpResponse(content=response.content, status=response.status_code, content_type=response.headers['Content-Type'])


def get_auth(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    token_type, _, credentials = auth_header.partition(' ')

    if token_type != 'Basic':
        return "", ""

    print(f"credentials: {credentials}")
    username, _, password = base64.b64decode(credentials).decode('utf-8').partition(':')
    print(f"username: {username}; password: {password}")
    return username, password


def download_package(request):
    required_vars = ['package_name']
    for var in required_vars:
        if var not in request.GET:
            return HttpResponseBadRequest(f"Please specify {var} in GET")

    package_name = request.GET['package_name']
    url = f'https://infrastructure.tech/wp-json/wp/v2/package?slug={package_name}'

    package_query = None
    username, password = get_auth(request)

    package_json = []

    if username and password:
        private_url = url + '&status=private'
        print(f"Querying {private_url}")
        package_query = requests.get(private_url, auth=requests.auth.HTTPBasicAuth(username, password)).content.decode("ascii")
        package_json = json.loads(package_query)

    if not package_json:
        print(f"Querying {url}")
        package_query = requests.get(url).content.decode("ascii")
        package_json = json.loads(package_query)

    if not package_json:
        return HttpResponseNotFound(f"No package {package_name}")

    #We expect only 1 matching package, so let's ignore the rest.
    #TODO: Error if len(...) > 1?
    package_json = package_json[0]

    file_url = package_json['file']
    file_data = requests.get(file_url)

    response = HttpResponse(file_data, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{package_name}.zip"'
    return response

def index(request):
    return HttpResponse("It works!")
