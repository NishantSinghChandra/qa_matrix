import requests
from bs4 import BeautifulSoup as BS
from resource.qa_constants import *
def get_rows_from_gap_analysys(endpoint):
    try:
        resp = requests.get(endpoint)
        if resp.status_code == 200:
            page = BS(resp.text, "lxml")
            allRows = page.findAll("table")[1].findAll("tr")
            head = allRows[0].prettify().replace('tr', 'thead')
            releventRows = []
            for row in allRows[-7:-1]:
                releventRows.append(row)
            return head + ''.join([row.prettify() for row in releventRows])
        else:
            raise Exception
    except:
        return '<p>Gap analysis page is not accessible</p>'


def get_rows_from_eureka(endpoint):
    # service_to_monitor_list = service_to_monitor_list
    try:
        resp = requests.get(endpoint)
        if resp.status_code == 200:
            page = BS(resp.text, "lxml")
            allRows = page.find("table").findAll("tr")
            head = allRows[0].prettify().replace('tr', 'thead')
            releventRows = []
            page.find("table").findAll("tr")[3].findAll('td')[0].text
            for row in allRows:
                if len(row.findAll('td')) == 0:
                    continue
                if row.findAll('td')[0].text in service_to_monitor_list:
                    releventRows.append(row)
            return head + ''.join([row.prettify() for row in releventRows])
        else:
            raise Exception
    except:
        return '<p>Eureka page is not accessible</p>'

if __name__=="__main__":
    from resource.qa_constants import *
    url = qa_constants('QAAR').tp_gap_analysis
    # html = get_rows_from_gap_analysys(url)
    # print html