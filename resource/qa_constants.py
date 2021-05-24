import yaml
import os
from bs4 import BeautifulSoup as BS
import requests
qaar = 'QAAR'
qat = 'QAT'
qas = 'QAS'
govqa = 'GovQA'
envs = ['QAAR', 'QAT', 'GovQA', 'QAS']
service_to_monitor_list = ['KAFKA:FALCON','KAFKA:ULTRON', 'KAFKA_ZOOKEEPER:FALCON', 'SI-SERV:DEFAULT', 'MERLIN:DEFAULT'
                           'KAFKA_ZOOKEEPER:ULTRON', 'NETACUITY-SERVER:PROXYAPI','TP-DATASERVICE:FALCON-INT',
                           'WATCHTOWER-SERVER:DEFAULT', 'DASHBOARD:QAT']
cur_path = os.path.dirname(os.path.realpath(__file__))

class qa_constants:
    def __init__(self, env):
        with open(os.path.join(cur_path, "properties.yml"), 'r') as stream:
            self.env_properties = yaml.load(stream)#Loader=yaml.FullLoader

        self.regression_job_link = self.env_properties['Environment'][env]['regression_job_link']
        self.regression_job_img = self.env_properties['Environment'][env]['regression_job_img']
        self.ekg_page = self.env_properties['Environment'][env]['ekg_page']
        self.artifacts = self._load_monitor_json()
        ip = self.get_gapanalysis_ip()
        self.tp_gap_analysis = 'http://{}:5253/tpEmrGapAnalysis.html'.format(ip)
        self.dp_gap_analysis = 'http://{}:5253/dpEmrGapAnalysis.html'.format(ip)
        self.eureka_link = self.get_eureka_link()
        self.constants = {
                'regression_job_link': self.regression_job_link,
                'regression_job_img': self.regression_job_img,
                'tp_gap_analysis': self.tp_gap_analysis,
                'dp_gap_analysis': self.dp_gap_analysis,
                'eureka_link': self.eureka_link,
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

    def _load_monitor_json(self):
        tmp = {"hosts": {}}
        try:
            b = BS(requests.get(self.ekg_page).content, features="lxml")
        except requests.exceptions.ConnectionError:
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
        return tmp

    def get_gapanalysis_ip(self):
        if len(self.artifacts)==0:
            return False
        for key, value in self.artifacts['hosts'].iteritems():
            if key.__contains__('gapanalysis'):
                return value.keys()[0]

    def get_eureka_link(self):
        if len(self.artifacts)==0:
            return False
        for key, value in self.artifacts['hosts'].iteritems():
            if key.__contains__('eureka'):
                ip = value.keys()[0]
                return "http://{}:8080/eureka/".format(ip)
global myenv
myenv = qa_constants


if __name__ == "__main__":
    qat = qa_constants('QAT')
    print qat.set_gapanalysis_links()
