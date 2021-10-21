# ICT3204 Security Analytics

<Introduction>
An analytic tool to help packet analyser deduce potential malicious packets running through the network

## Requirements
[![Ubuntu](https://img.shields.io/badge/Ubuntu-21.04-green)]
[![Python](https://img.shields.io/badge/Python-3.9.5-blue)]
[![Argus](https://img.shields.io/badge/argus--server-2%3A3.0.8.2--2ubuntu1-blue)]
[![Tshark](https://img.shields.io/badge/tshark-3.4.4--1ubuntu1-blue)]
[![make](https://img.shields.io/badge/make-4.3--4ubuntu1-blue)]

## Features
- 

## Installation

Ensure that you're in ```./app``` directory before executing any ```make``` commands
A makefile is written to automatically install all required dependencies. 
```bash
make install
```

Test if t-shark and argus are running. If an error appears during the check, ensure you have both package installed and try again.
```bash
make check
```

To access flask website
```bash
make run
```

## Usage



## Contributing
<Contributors>

## License
[MIT](https://choosealicense.com/licenses/mit/)