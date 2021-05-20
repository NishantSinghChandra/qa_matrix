import requests
from bs4 import BeautifulSoup as BS

def get_rows_from_gap_analysys(endpoint):
    try:
        resp = requests.get(endpoint)
        if resp.status_code == 200:
            page = BS(resp.text, "lxml")
            allRows = page.findAll("table")[1].findAll("tr")
            releventRows = [allRows[0]]
            for row in allRows[-6:-1]:
                releventRows.append(row)
            return ''.join([row.prettify() for row in releventRows])
        else:
            raise Exception
    except:
        return '<p>Gap analysis page is not accessible</p>'


def load_monitor_json(url):
    tmp = {"hosts": {}}
    # from BeautifulSoup import BeautifulSoup as BS
    # from urllib.request import urlopen
    try:
        b = BS(requests.get(url).content, features="lxml")
    except requests.exceptions.ConnectionError:
        # logger.warn("ignorning the url:" + str(url))
        return {}
    except:
        # logger.warn("ignorning the url:" + str(url))
        return {}
    env_info = {}
    for _ in b.findAll("tr")[1:]:
        component = _.findAll("td")[0].text
        if (component == 'None') or (component == 'ekg'):
            component = _.findAll("td")[2].text
        row = _.findAll("td")[1:]
        if component not in env_info:
            env_info[component] = {}
        if str(row[0].text) in ['None','default','ekg'] :
            env_info[component][str(row[2].text)] = str(row[1].text)
        else:
            env_info[component][str(row[2].text)] = str(row[0].text)
    tmp["hosts"] = env_info
    # self._load_census_json()
    return tmp

if __name__=="__main__":
    from resource.qa_constants import *
    url = qa_constants('QAAR').tp_gap_analysis
    # html = get_rows_from_gap_analysys(url)
    # print html
    ekg=load_monitor_json('http://ekg-euprod.shared.int.shn.io/v1/html')
    print(ekg)