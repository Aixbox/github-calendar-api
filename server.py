# -*- coding: UTF-8 -*-
import requests
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]


def getdata(name):

    headers = {
        'Referer': 'https://github.com/'+ name,
        'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        'X-Requested-With': 'XMLHttpRequest'
    }


    try:
        gitpage = requests.get(
            "https://github.com/" + name + "?action=show&controller=profiles&tab=contributions&user_id=" + name,
            headers=headers)
        data = gitpage.text
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return {"total": 0, "contributions": []}

    datadatereg = re.compile(r'data-date="(.*?)" id="contribution-day-component')
    datacountreg = re.compile(r'<tool-tip .*?class="sr-only position-absolute">(.*?) contribution')

    datadate = datadatereg.findall(data)
    datacount = datacountreg.findall(data)
    datacount = list(map(int, [0 if i == "No" else i for i in datacount]))

    if not datadate or not datacount:
        return {"total": 0, "contributions": []}

    sorted_data = sorted(zip(datadate, datacount))
    datadate, datacount = zip(*sorted_data)

    contributions = sum(datacount)
    datalist = [{"date": item, "count": datacount[index]} for index, item in enumerate(datadate)]
    datalistsplit = list_split(datalist, 7)
    return {
        "total": contributions,
        "contributions": datalistsplit
    }


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # path = self.path
            # spl = path.split('?')[1:]
            # user = None
            # for kv in spl:
            #     key, value = kv.split("=")
            #     if key == "user":
            #         user = value
            #         break
            # if user is None:
            #     raise ValueError("Missing user parameter")
            user = "Aixbox"
            data = getdata(user)
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {"error": str(e)}
            self.wfile.write(json.dumps(error_response).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=handler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()



