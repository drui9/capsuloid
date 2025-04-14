env := .venv
deps := -r requirements.txt
streamer := stream/main.py

run: $(env)
	@$</bin/flask run --debug --port 8000

install: $(env)
	$</bin/pip install --upgrade $(deps) & npm i .

$(env):
	python -m venv $@

clean:
	rm -rf __pycache__ **/__pycache__ **/**/__pycache__ Logs

