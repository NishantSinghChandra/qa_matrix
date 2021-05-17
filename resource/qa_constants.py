qaar = 'QAAR'
qat = 'QAT'
govqa = 'GovQA'
envs = ['QAAR', 'QAT', 'GovQA']


class qa_constants:
    def __init__(self, env):
        self.env = env
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
            self.gap_analysis = 'http://172.18.67.93:5253/tpEmrGapAnalysis.html'

        self.constants = {
            'link': self.link,
            'img': self.img,
            'gap_analysis': self.gap_analysis,
            'env': self.env
        }


myenv = qa_constants


if __name__ == "__main__":
    qat = qa_constants('QAT')
    print qat.link
