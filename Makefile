source-venv:
	source ./venv/bin/activate

run-dev-game:
	python ./main.py

run-dev-web:
	rm -rf ./build
	python -m pygbag .

build-prod-binary:
	pyinstaller ./Duellum.spec
