import yaml
import os
qaar = 'QAAR'
qat = 'QAT'
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
            self.gap_analysis = 'http://172.18.19.196:5253/tpEmrGapAnalysis.html'

        elif env == qaar:
            self.link = 'http://jenkins.shn.io/job/tp-automation-batch/'
            self.img = 'http://jenkins.shn.io/buildStatus/icon?job=tp-automation-batch/'
            self.gap_analysis = 'http://172.18.67.93:5253/tpEmrGapAnalysis.html'

        elif env == govqa:
            self.link = 'http://jenkins.shn.io/job/tp-automation-batch/'
            self.img = 'http://jenkins.shn.io/buildStatus/icon?job=tp-automation-batch/'
            self.gap_analysis = 'http://172.18.211.102:5253/tpEmrGapAnalysis.html'

        self.constants = {
                'link': self.link,
                'img': self.img,
                'gap_analysis': self.gap_analysis,
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
