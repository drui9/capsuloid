env := .venv
deps := -r requirements.txt
streamer := stream/main.py

all:
	@make -j 2 tailwind run

run: $(env)
	@$</bin/flask run --debug --port 8000

tailwind:
	npm run build

test: $(env)
	@$</bin/python -m unittest

install: $(env)
	$</bin/pip install --upgrade $(deps) & npm install .

$(env):
	python -m venv $@

clean:
	rm -rf __pycache__ **/__pycache__ **/**/__pycache__ Logs

