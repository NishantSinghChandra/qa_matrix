import yaml
import os
from bs4 import BeautifulSoup as BS
import requests
qaar = 'QAAR'
qat = 'QAT'
qas = 'QAS'
govqa = 'GovQA'
envs = ['QAAR', 'QAT', 'GovQA', 'QAS']
cur_path = os.path.dirname(os.path.realpath(__file__))

class qa_constants:
    def __init__(self, env):
        with open(os.path.join(cur_path, "properties.yml"), 'r') as stream:
            self.env_properties = yaml.load(stream)#Loader=yaml.FullLoader

        if env == qat:
            self.link = 'http://jenkins.shn.io/job/tp-automation-batch-py3/'
            self.img = 'http://jenkins.shn.io/buildStatus/icon?job=tp-automation-batch-py3'
            self.tp_gap_analysis = 'http://172.18.19.196:5253/tpEmrGapAnalysis.html'
            self.dp_gap_analysis = 'http://172.18.19.196:5253/dpEmrGapAnalysis.html'
            self.ekg = 'http://ekg-qat.shared.int.shn.io/v1/html'

        elif env == qaar:
            self.link = 'http://jenkins.shn.io/job/tp-automation-batch/'
            self.img = 'http://jenkins.shn.io/buildStatus/icon?job=tp-automation-batch/'
            self.tp_gap_analysis = 'http://172.18.67.93:5253/tpEmrGapAnalysis.html'
            self.dp_gap_analysis = 'http://172.18.67.93:5253/dpEmrGapAnalysis.html'
            self.ekg = 'http://ekg-qaautoregression.shared.int.shn.io/v1/html'

        elif env == govqa:
            self.link = ''
            self.img = ''
            self.tp_gap_analysis = 'http://172.18.211.102:5253/tpEmrGapAnalysis.html'
            self.dp_gap_analysis = 'http://172.18.211.102:5253/dpEmrGapAnalysis.html'
            self.ekg = 'http://ekg-govqa.shared.int.shn.io/v1/html'

        elif env == qas:
            self.link = ''
            self.img = ''
            self.tp_gap_analysis = 'http://172.18.115.124:5253/tpEmrGapAnalysis.html'
            self.dp_gap_analysis = 'http://172.18.115.124:5253/dpEmrGapAnalysis.html'
            self.ekg = 'http://ekg-awsqastable.shared.int.shn.io/v1/html'

        self.artifacts = self.load_monitor_json()
        self.constants = {
                'link': self.link,
                'img': self.img,
                'tp_gap_analysis': self.tp_gap_analysis,
                'dp_gap_analysis': self.dp_gap_analysis,
                'env': env
                }
    def get_dataservice_url(self):
        try:
            tp_data_service_ip = list(self.artifacts['hosts']['tp-dataservice'].keys())
        except:
            return False
        for ip in tp_data_service_ip:
            tp_data_service_url = "http://" + ip + ":8094/swagger-ui.html"
            try:

                if requests.get(tp_data_service_url).status_code == 200:
                    return "http://" + ip + ":8094/tp-pipeline"
            except requests.exceptions.ConnectionError:
                continue

    def load_monitor_json(self):
        tmp = {"hosts": {}}
        # from BeautifulSoup import BeautifulSoup as BS
        # from urllib.request import urlopen
        try:
            b = BS(requests.get(self.ekg).content, features="lxml")
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
            if str(row[0].text) in ['None', 'default', 'ekg']:
                env_info[component][str(row[2].text)] = str(row[1].text)
            else:
                env_info[component][str(row[2].text)] = str(row[0].text)
        tmp["hosts"] = env_info
        # self._load_census_json()
        return tmp


global myenv
myenv = qa_constants


if __name__ == "__main__":
    qat = qa_constants('QAT')
    print qat.link
