from flask import Flask, render_template
app = Flask(__name__)


@app.route('/hello/<user>')
def hello_world(user):
	return render_template('hello_world.html', name=user)


@app.route('/')
def index():
	return render_template("menu.html")


@app.route('/qat')
def qat():
	env = 'QAT'
	status = {'state': 'green', 'health': 'ok', 'pipeline': 'running'}
	jenkin_vars = {
					'env': env,
					'link': 'http://jenkins.shn.io/job/tp-automation-batch-py3/',
					'img': 'http://jenkins.shn.io/buildStatus/icon?job=tp-automation-batch-py3'}
	return render_template("qat.html", env=env, result=status, jenkin_vars=jenkin_vars)


@app.route('/qaar')
def qaar():
	env = 'QAAR'
	status = {'state': 'amber', 'health': 'ok', 'pipeline': 'running'}
	jenkin_vars = {
		'env': env,
		'link': 'http://jenkins.shn.io/job/tp-automation-batch/',
		'img': 'http://jenkins.shn.io/buildStatus/icon?job=tp-automation-batch/'}
	return render_template("qat.html", env=env, result=status, jenkin_vars=jenkin_vars)


@app.route('/govqa')
def govqa():
	env='GovQA'
	status = {'state': 'red', 'health': 'bad', 'pipeline': 'stopped'}
	jenkin_vars = {
		'env': env,
		'link': 'http://jenkins.shn.io/job/tp-automation-batch-py3/',
		'img': 'http://jenkins.shn.io/buildStatus/icon?job=tp-automation-batch-py3'}
	return render_template("qat.html", env=env, result=status, jenkin_vars=jenkin_vars)


if __name__ == "__main__":
	app.run(debug=True)
