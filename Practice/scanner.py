#!/usr/bin/env python
import requests
from BeatifulSoap import BeatifulSoap
import urlparse

def request(url):
    try:
        return requests.get("http://" + url)
    except requests.exceptions.ConnectionError:
        pass

target_url = ""
response = request(target_url)

parsed_html = BeatifulSoap(response.content)
form_list = parsed_html.findAll("form")

for form in form_list:
    action = form.get("action")
    post_url = urlparse.urljoin(target_url, action)
    print(post_url)
    print(action)
    method = form.get("method")
    print(method)

    inputs_list = form.findAll("input")
    post_data = {}
    for input in inputs_list:
        input_name = input.get("name")
        input_type = input.get("type")
        input_value = input.get("value")
        if input_type == "text":
            input_value = "test"
        post_data[input_name] = input_value
    result = requests.post(post_url, data=post_data)
    print(result.content)