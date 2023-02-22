from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)


def get_response(url):
    r = requests.get(url)
    while r.status_code != 200:
        r = requests.get(url)
    return r.text


def prepare_urls(matches):
    list = []
    for match in matches:
        if match.startswith("https:") and "scontent.cdninstagram.com" in match or "scontent-fra3-1.cdninstagram.com" in match:
            list.append(match.replace("\\", ""))
    return list


@app.route('/findUrls')
def find_urls():
    url = request.args.get("url")
    response = get_response(url)
    img_matches = re.findall('"url":"([^"]+)"', response)
    img_urls = prepare_urls(img_matches)
    return jsonify(img_urls)


if __name__ == '__main__':
    app.run()
