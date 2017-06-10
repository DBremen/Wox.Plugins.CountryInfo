import requests
import webbrowser
import os
from wox import Wox

icons_dir = './icons/'
class Main(Wox):
    def request(self, url):
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
            proxies = {
                "http": "http://{}:{}".format(self.proxy.get("server"), self.proxy.get("port")),
                "https": "http://{}:{}".format(self.proxy.get("server"), self.proxy.get("port"))}
            return requests.get(url, proxies=proxies)
        else:
            return requests.get(url)

    def query(self, query):
        results = []
        scriptdir = os.path.dirname(os.path.realpath(__file__)) + "\\icons"
        url = "http://countryapi.gear.host/v1/Country/getCountries?pName=%25" + query + "%25&pLimit=25&pPage=1"
        r = requests.get(url).json()
        results.append({
            "Title": "Name - Region - SubRegion",
            "SubTitle": "Language - Currency - CurrencySymbol",
            "IcoPath": icons_dir + "globe.png"
        })
        for item in r["response"]:
            title = item["name"] + " - " + item["region"] + " - " + item["subRegion"]
            subtitle = item["nativeLanguage"] + " - " + item["currencyName"] + " - " + item["currencySymbol"]
            flagurl = item["flagPng"]
            flagname = flagurl.rsplit('/', 1)[1]
            flagpath = os.path.abspath(os.path.join(scriptdir, flagname))
            latitude = item["latitude"]
            longitude = item["longitude"]
            mapurl = "https://www.google.ie/maps/@" + latitude + "," + longitude +",7z?hl=en"
            if not os.path.isfile(flagpath):
                with open(flagpath, 'wb') as handle:
                    response = requests.get(flagurl, stream=True)
                    if response.ok:
                        for block in response.iter_content(1024):
                            if not block:
                                break
                            handle.write(block)
            results.append({
                "Title": title,
                "SubTitle": subtitle,
                "IcoPath": icons_dir + flagname,
                "JsonRPCAction": {
                    "method": "openUrl",
                    "parameters": [mapurl],
                    # hide the query wox or not
                    "dontHideAfterAction": True
                }
            })
        if not results:
            results.append({
                "Title": 'Not found',
                "SubTitle": '',
                "IcoPath": icons_dir + "globe.png"
            })
        return results

    def openUrl(self, url):
        webbrowser.open(url)
        WoxAPI.change_query(url)

if __name__ == "__main__":
    Main()
