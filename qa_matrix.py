# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Flask, render_template, redirect
from collections import OrderedDict
import socket
import socks
import json
from resource.qa_constants import *
import logging
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from lib.general import *
app = Flask(__name__)
app.logger.setLevel(logging.INFO)


scheduler = BackgroundScheduler()

status = dict()
qat_constants = qa_constants(qat)
qaar_constants = qa_constants(qaar)
govqa_constants = qa_constants(govqa)
qas_constants = qa_constants(qas)

def _getConstants(env):
    if env == qat:
        constants = qat_constants
    elif env == qaar:
        constants = qaar_constants
    elif env == govqa:
        constants = govqa_constants
    elif env == qas:
        constants = qas_constants
    return constants

@app.route('/get_status')
def getStatus():
    print('into scheduled job')
    for env in envs:
        status[env] = dict()
        constants = _getConstants(env)
        status[env]['status_tp'] = get_regression_status(constants.regression_job_link)
        status[env]['status_dp'] = get_regression_status(constants.dp_regression_job_link)
        status[env]['tp_rows'] = get_rows_from_gap_analysys(constants.tp_gap_analysis)
        status[env]['dp_rows'] = get_rows_from_gap_analysys(constants.dp_gap_analysis)
        # get_rows_from_eureka(qa_constants(env).eureka_link, service_to_monitor_list)
    return redirect('/')


# getStatus()
# scheduler.add_job(func=getStatus, trigger='interval', seconds=900)
# scheduler.start()
# atexit.register(lambda: scheduler.shutdown())


@app.route('/')
def index():
    return render_template("menu.html")


@app.route('/<env>')
def get_status(env):

    if env in envs:
        constants = _getConstants(env)
        env_var = vars(constants)
    else:
        return redirect('/')
    app.logger.info('fetch tp reg status')
    status_tp = get_regression_status(constants.regression_job_link) #status[env]['status_tp']
    app.logger.info('Done fetching tp reg status')

    app.logger.info('fetch dp reg status')
    status_dp = get_regression_status(constants.dp_regression_job_link) #status[env]['status_dp']
    app.logger.info('Done fetching dp reg status')

    app.logger.info('fetch tp pipeline stauts')
    tp_rows = get_rows_from_gap_analysys(constants.tp_gap_analysis) #status[env]['tp_rows']
    app.logger.info('Done fetching tp pipeline stauts')

    app.logger.info('fetch dp pipeline stauts')
    dp_rows = get_rows_from_gap_analysys(constants.dp_gap_analysis) #status[env]['dp_rows']
    app.logger.info('Done fetching dp pipeline stauts')
    # eureka_rows = get_rows_from_eureka(env_var.eureka_link, service_to_monitor_list)
    eureka_rows = None
    return render_template("status.html", result_tp=status_tp, result_dp=status_dp, constants=env_var, tp_analysis_table=tp_rows, dp_analysis_table=dp_rows, eureka_rows=eureka_rows)



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
    app.run(debug=True, threaded=True)
