# Compile Contracts
compile:
	. .env/bin/activate && cd vvet && brownie compile

test:
	. .env/bin/activate && cd vvet && python3 -m pytest -vv -s
# Install compiler tools
install:
	npm install -g ganache-cli
	python3 -m venv .env
	. .env/bin/activate && pip3 install wheel
	. .env/bin/activate && pip3 install -r requirements.txt