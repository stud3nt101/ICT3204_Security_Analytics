ifeq ($(OS),Windows_NT)
	CC=python
else
	CC=python3
endif

PFLAGS=-3.9-64
SOURCES = $(shell find src/ -type f -name '*.py')

.PHONY: run check install

run:
	flask run

install:
	@echo "\nInstalling pip requirements"
	pip3 install --quiet --no-cache-dir -r requirements.txt
	
	@echo "\nInstalling tshark and argus-server"
	sudo apt install tshark
	sudo apt install argus-server

check:
	@echo "\nTesting tshark"
	tshark -r test/test.pcapng -T fields -E header=y -E separator=, -E occurrence=a -E quote=s -e frame.time -e _ws.col.Protocol -e _ws.col.Length -e tcp.flags -e ip.src -e tcp.srcport -e udp.srcport -e ip.dst -e tcp.dstport -e udp.dstport -e _ws.col.Info > test/test-success.csv
	rm test/test-success.csv

	@echo "\nTesting argus-server"
	argus -F utils/argus.conf -r test/test.pcapng -w temp.biargus | ra -r temp.biargus -n -F utils/ra.conf -Z b > test/test-success.binetflow
	rm test/test-success.binetflow