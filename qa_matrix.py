from flask import Flask, render_template, redirect
from resource.qa_constants import *
app = Flask(__name__)


@app.route('/hello/<user>')
def hello_world(user):
	return render_template('hello_world.html', name=user)


@app.route('/')
def index():
	return render_template("menu.html")


@app.route('/<env>')
def status(env):
	if env in envs:
		constants = qa_constants(env).constants
	else:
		return redirect('/')
	status = {'state': 'green', 'health': 'ok', 'pipeline': 'running'}

	return render_template("status.html", result=status, constants=constants)


if __name__ == "__main__":
	app.run(debug=True)
