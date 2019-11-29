env:
	virtualenv env
	. env/bin/activate; pip install -r requirements.txt

install: env
	. env/bin/activate; pip install -r requirements.txt

lint:
	. env/bin/activate; isort --atomic *.py; pylint --exit-zero *.py
