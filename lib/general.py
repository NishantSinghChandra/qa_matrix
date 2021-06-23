import requests
from bs4 import BeautifulSoup as BS
#from resource.qa_constants import *
from collections import OrderedDict

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


def get_rows_from_eureka(endpoint, service_list):
    # try:
    for link in endpoint:
        try:
            resp = requests.get(link)
            if resp.status_code == 200:
                page = BS(resp.text, "lxml")
                allRows = page.find("table").findAll("tr")
                head = allRows[0].prettify().replace('tr', 'thead')
                releventRows = []
                #page.find("table").findAll("tr")[3].findAll('td')[0].text
                for row in allRows:
                    if len(row.findAll('td')) == 0:
                        continue
                    if any(map(lambda service: str(row.findAll('td')[0].text).startswith(service), service_list)):
                        releventRows.append(row)
                return head + ''.join([row.prettify() for row in releventRows])
        except:
            pass
    else:
        raise Exception
    # except:
    #     return '<p>Eureka page is not accessible</p>'


def get_regression_status(url):
    result = OrderedDict()
    try:
        resp = requests.get(url)
    except:
        result = {'test execution status': 'Jenkins page is not accessible'}
    try:
        page = BS(resp.text, 'lxml')
        table = page.find('table', id='robot-summary-table')
        rows = table.findAll('tr')[-1].findAll('td')
        result['Total'] = rows[0].text
        result['Failed'] = rows[1].text
        result['Passed'] = rows[2].text
        result['Passed %'] = rows[3].text

    except:
        result = {'test execution': 'jenkin page missing execution details'}
    return result

if __name__=="__main__":
    from resource.qa_constants import *
    url = qa_constants('QAAR').tp_gap_analysis
    # html = get_rows_from_gap_analysys(url)
    # print html