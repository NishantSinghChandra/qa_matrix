import yaml
import os
from bs4 import BeautifulSoup as BS
import requests
qaar = 'QAAR'
qat = 'QAT'
qas = 'QAS'
govqa = 'GovQA'
envs = ['QAAR', 'QAT', 'GovQA', 'QAS']
service_to_monitor_list = ['KAFKA', 'SI-SERV', 'MERLIN', 'NETACUITY-SERVER', 'TP-DATASERVICE', 'WATCHTOWER-SERVER',
                           'DASHBOARD']
cur_path = os.path.dirname(os.path.realpath(__file__))

class qa_constants:
    def __init__(self, env):
        with open(os.path.join(cur_path, "properties.yml"), 'r') as stream:
            env_properties = yaml.load(stream)#Loader=yaml.FullLoader

        self.regression_job_link = env_properties['Environment'][env]['regression_job_link']
        self.regression_job_img = env_properties['Environment'][env]['regression_job_img']
        self.ekg_page = env_properties['Environment'][env]['ekg_page']
        # self.artifacts = self._load_monitor_json()
        links = self.get_links()
        self.tp_gap_analysis = 'http://{}:5253/tpEmrGapAnalysis.html'.format(links.get('gapanalysis'))
        self.dp_gap_analysis = 'http://{}:5253/dpEmrGapAnalysis.html'.format(links.get('gapanalysis'))
        self.eureka_link = links.get('eureka')
        self.create_link = links.get('crate')
        self.swagger_link = links.get('swagger')
        self.tp_data_service_ip = links.get('tp_data_service_ip')

        self.constants = {
                'regression_job_link': self.regression_job_link,
                'regression_job_img': self.regression_job_img,
                'tp_gap_analysis': self.tp_gap_analysis,
                'dp_gap_analysis': self.dp_gap_analysis,
                'eureka_link': self.eureka_link,
                'swagger_link': links.get('swagger'),
                'crate_link': links.get('crate'),
                'env': env
                }

    def get_dataservice_url(self):
        for ip in self.tp_data_service_ip:
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

    def get_links(self):
        artifacts = self._load_monitor_json()
        if len(artifacts) ==0:
            return False
        links = dict()
        for key, value in artifacts['hosts'].iteritems():
            if key.__contains__('tpcratereadclient') and 'crate' not in links:
                ip = value.keys()[0]
                links['crate'] = "http://{}:4200/#!/console".format(ip)

            elif key.__contains__('elasticsearchclient') and 'elasticsearch' not in links:
                ip = value.keys()[0]
                links['elasticsearch'] = "http://{}:9200/_plugin/head/".format(ip)

            elif key.__contains__('tpdatasrvcint') and 'swagger' not in links:
                ip = value.keys()[0]
                links['swagger'] = "http://{}:8094/swagger-ui.html".format(ip)
            elif key.__contains__('eureka') and 'eureka' not in links:
                ip = value.keys()[0]
                links['eureka'] = "http://{}:8080/eureka/".format(ip)
            elif key.__contains__('gapanalysis') and 'gapanalysis' not in links:
                ip = value.keys()[0]
                links['gapanalysis'] = ip
            elif key.__contains__('tp-dataservice') and 'tp-dataservice' not in links:
                links['tp-dataservice'] = value.keys()
        return links

global myenv
myenv = qa_constants


if __name__ == "__main__":
    qat = qa_constants('QAT')
    print qat.set_gapanalysis_links()
