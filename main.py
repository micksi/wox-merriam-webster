# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import webbrowser
from wox import Wox, WoxAPI


class MerriamWebster(Wox):

    def request(self, url):
        # If user set the proxy, you should handle it.
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
            proxies = {
                "http": "http://{}:{}".format(self.proxy.get("server"), self.proxy.get("port")),
                "https": "http://{}:{}".format(self.proxy.get("server"), self.proxy.get("port"))}
            return requests.get(url, proxies=proxies)
        else:
            return requests.get(url)

    # A function named query is necessary, we will automatically invoke this
    # function when user query this plugin
    def query(self, key):
        if key.strip() == '':
            return [{
                "Title": "Merriam Webster",
                "SubTitle": "Start querying by typing a word",
                "IcoPath": "Images/mw_logo.png"
            }]

        r = self.request('https://www.merriam-webster.com/dictionary/' + key)
        bs = BeautifulSoup(r.text, 'html.parser')
        results = []
        for i in bs.select(".def-text .definition-list .definition-inner-item"):
            title = key
            url = 'https://www.merriam-webster.com/dictionary/' + key
            results.append({
                "Title": key,
                "SubTitle": i.text.encode('utf-8').replace(':', '').strip(),
                "IcoPath": "Images/mw_logo.png",
                "JsonRPCAction": {
                    # You can invoke both your python functions and Wox public APIs .
                    # If you want to invoke Wox public API, you should invoke as following format: Wox.xxxx
                    # you can get the public name from https://github.com/qianlifeng/Wox/blob/master/Wox.Plugin/IPublicAPI.cs,
                    # just replace xxx with the name provided in this url
                    "method": "openUrl",
                    # you MUST pass parater as array
                    "parameters": [url],
                    # hide the query wox or not
                    "dontHideAfterAction": True
                }
            })

        return sorted(results, key=lambda k: k['SubTitle'])

    def openUrl(self, url):
        webbrowser.open(url)
        WoxAPI.change_query(url)


if __name__ == "__main__":
    MerriamWebster()
