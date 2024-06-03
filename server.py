# -*- coding: UTF-8 -*-
import requests
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

def list_split(items, n):
    return [items[i:i + n] for i in range(0, len(items), n)]


def getdata(name):

    headers = {
                            'Accept': 'text/html',
                            'Accept-Encoding': 'gzip, deflate, br, zstd',
                            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                            'Cookie': '_device_id=5a60349d3702beaeb65a023dadaf504c; user_session=SUenDoAA7Z3_d_dj5gCJLPG9Q6nrWWXR3OH0KVV4pBrNfZOL; __Host-user_session_same_site=SUenDoAA7Z3_d_dj5gCJLPG9Q6nrWWXR3OH0KVV4pBrNfZOL; logged_in=yes; dotcom_user=Aixbox; _octo=GH1.1.383271031.1709946270; has_recent_activity=1; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; preferred_color_mode=light; tz=Asia%2FShanghai; _gh_sess=hzx34%2BUs4tt8aTrXmTo%2BrtiCS8sMRIud%2FXimgNOD9yB0fqI0wI4plfP5xfHerMawAkey4m6YHXr0IgiPwHfmRLm2nC5g%2Bua2vZ7tMvaSMtsqPKzu%2F0ygh8VDhALyHLwFpLAANxlGqkdh2UbhxomW6GIV%2F0oySIiUzmrKTTD2MddQ45wGnKF%2FMHtL0MGwOzB5ntXGoe%2B7YLS1%2BlxXit8f%2FgvOAxG%2B6MlN4uFJAbdY0yWAoQkE4GIEDMarqFcMGZiFQ0HGaIJf4RFVJXaD7Ws2%2BMsk%2BNoel%2BtVfssiNmom%2FmD6lmMphi2kUnl0FPNczki%2BxUuNblRJPiTe0HrYK85N4Wa3BjKadoDovY8uTv5f%2BLxFDeAr1hyQnViJqz%2BbAMrwJzftpY8tGuqQHnOSVdzNZxbpDdA%3D--637IKzGyDM0SgQFg--fEBA7kH53mtqbk57MXigEA%3D%3D',
                            #'Cookie': 'logged_in=yes; dotcom_user=Aixbox;  has_recent_activity=1; color_mode=%7B%22color_mode%22%3A%22auto%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark%22%2C%22color_mode%22%3A%22dark%22%7D%7D; preferred_color_mode=light; tz=Asia%2FShanghai;',
                            'If-None-Match': 'W/"0675a6fab4344c254a79c3ed26b28505"',
                            'Priority': 'u=1, i',
                            'Referer': 'https://github.com/Aixbox',
                            'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                            'Sec-Ch-Ua-Mobile': '?0',
                            'Sec-Ch-Ua-Platform': 'Windows',
                            'Sec-Fetch-Dest': 'empty',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Site': 'same-origin',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
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



