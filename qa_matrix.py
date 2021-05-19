# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask import Flask, render_template, redirect
import socket
import socks
from resource.qa_constants import *
from lib.general import *
app = Flask(__name__)


@app.route('/')
def index():
	return render_template("menu.html")


@app.route('/<env>')
def status(env):
	if env in envs:
		constants = qa_constants(env).constants
	else:
		return redirect('/')
	status = {'state': 'dummy', 'health': 'dummy', 'pipeline': 'dummy'}
	print constants['gap_analysis']
	rows = get_rows_from_gap_analysys(constants['gap_analysis'])
	return render_template("status.html", result=status, constants=constants, gap_analysis_table=rows)

if __name__ == "__main__":
	socks.set_default_proxy(socks.SOCKS5, "localhost", int(9997))
	socket.socket = socks.socksocket
	app.run(debug=True)
