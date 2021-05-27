# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Flask, render_template, redirect
from collections import OrderedDict
import socket
import socks
import json
from resource.qa_constants import *
from lib.general import *
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("menu.html")


@app.route('/<env>')
def status(env):
    status = OrderedDict()
    if env in envs:
        env_var = qa_constants(env)
        constants = env_var.constants
    else:
        return redirect('/')
    status = get_regression_status(env_var.regression_job_link)
    # status['Dataservice'] = get_dataservice_status(env_var)
    tp_rows = get_rows_from_gap_analysys(env_var.tp_gap_analysis)
    dp_rows = get_rows_from_gap_analysys(env_var.dp_gap_analysis)
    eureka_rows = get_rows_from_eureka(env_var.eureka_link, service_to_monitor_list)
    return render_template("status.html", result=status, constants=constants, tp_analysis_table=tp_rows, dp_analysis_table=dp_rows, eureka_rows=eureka_rows)


def get_dataservice_status(env_var):
    try:
        ds_url = env_var.get_dataservice_url()
        endpoint = '/csp/sanctioned'
        return _request_to_data_service(ds_url, endpoint)
    except:
        return 'Down'



def _request_to_data_service(ds_url, endpoint, request_data=None,
                             request_type='get', headers=None, automation_purpose=False):
    # converts the dict to json string
    if isinstance(request_data, dict) or isinstance(request_data, list):
        request_data = json.dumps(request_data)

    if headers is None:
        headers = {'Content-type': 'application/json'}

    endpoint = ds_url + '/v1' + endpoint
    request_method = getattr(requests, request_type)

    response = request_method(
        endpoint,
        timeout=100,
        data=request_data,
        headers=headers)
    status = 'OK' if response.status_code == 200 else 'Down'
    return status

if __name__ == "__main__":
    socks.set_default_proxy(socks.SOCKS5, "localhost", int(9997))
    socket.socket = socks.socksocket
    app.run(debug=True)
