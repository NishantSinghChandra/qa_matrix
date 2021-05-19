import requests
from resource.qa_constants import *
myenv = qa_constants('QAAR')

class dataserviceApi():
    def __init__(self):
        self.env = myenv.env
        self.dataserviceUrl = myenv.get_dataservice_url()


    def request_to_ds(self, endpoint, method='GET', data=None):
        header = {}


