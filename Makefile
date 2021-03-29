# Compile Contracts
compile:
	. .env/bin/activate && cd vvet &&  brownie compile

# Install compiler tools
install:
	python3 -m venv .env
	. .env/bin/activate && pip3 install wheel
	. .env/bin/activate && pip3 install -r requirements.txt