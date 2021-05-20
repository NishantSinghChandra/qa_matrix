import yaml
import os
qaar = 'QAAR'
qat = 'QAT'
qas = 'QAS'
govqa = 'GovQA'
envs = ['QAAR', 'QAT', 'GovQA', 'QAS']
cur_path = os.path.dirname(os.path.realpath(__file__))

class qa_constants:
    def __init__(self, env):
        self.deployedenv = 'development'
        self.socksproxy_port = 9997
        with open(os.path.join(cur_path, "properties.yml"), 'r') as stream:
            self.env_properties = yaml.load(stream, Loader=yaml.FullLoader)

        if env == qat:
            self.link = 'http://jenkins.shn.io/job/tp-automation-batch-py3/'
            self.img = 'http://jenkins.shn.io/buildStatus/icon?job=tp-automation-batch-py3'
            self.tp_gap_analysis = 'http://172.18.19.196:5253/tpEmrGapAnalysis.html'
            self.dp_gap_analysis = 'http://172.18.19.196:5253/dpEmrGapAnalysis.html'

        elif env == qaar:
            self.link = 'http://jenkins.shn.io/job/tp-automation-batch/'
            self.img = 'http://jenkins.shn.io/buildStatus/icon?job=tp-automation-batch/'
            self.tp_gap_analysis = 'http://172.18.67.93:5253/tpEmrGapAnalysis.html'
            self.dp_gap_analysis = 'http://172.18.67.93:5253/dpEmrGapAnalysis.html'

        elif env == govqa:
            self.link = ''
            self.img = ''
            self.tp_gap_analysis = 'http://172.18.211.102:5253/tpEmrGapAnalysis.html'
            self.dp_gap_analysis = 'http://172.18.211.102:5253/dpEmrGapAnalysis.html'

        elif env == qas:
            self.link = ''
            self.img = ''
            self.tp_gap_analysis = 'http://172.18.115.124:5253/tpEmrGapAnalysis.html'
            self.dp_gap_analysis = 'http://172.18.115.124:5253/dpEmrGapAnalysis.html'

        self.constants = {
                'link': self.link,
                'img': self.img,
                'tp_gap_analysis': self.tp_gap_analysis,
                'dp_gap_analysis': self.dp_gap_analysis,
                'env': env
                }
    def get_dataservice_url(self):
        tp_data_service_url = "http://" + '172.18.20.137' + ":8094/swagger-ui.html"
        return tp_data_service_url

global myenv
myenv = qa_constants


if __name__ == "__main__":
    qat = qa_constants('QAT')
    print qat.link
