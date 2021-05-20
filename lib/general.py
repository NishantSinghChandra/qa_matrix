import requests
from bs4 import BeautifulSoup

def get_rows_from_gap_analysys(endpoint):
    try:
        resp = requests.get(endpoint)
        if resp.status_code == 200:
            page = BeautifulSoup(resp.text, "lxml")
            allRows = page.findAll("table")[1].findAll("tr")
            releventRows = [allRows[0]]
            for row in allRows[-13:-1]:
                releventRows.append(row)
            return ''.join([row.prettify() for row in releventRows])
        else:
            raise Exception
    except:
        return '<p>Gap analysis page is not accessible</p>'


if __name__=="__main__":
    from resource.qa_constants import *
    url = qa_constants('QAAR').tp_gap_analysis
    html = get_rows_from_gap_analysys(url)
    print html