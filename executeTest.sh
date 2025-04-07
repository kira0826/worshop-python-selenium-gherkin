#!/bin/bash
source /home/zai/Documents/semester7/automatizacion/venv/bin/activate
cd /home/zai/Documents/semester7/automatizacion/worshop-python-selenium-gherkin
behave >> /home/zai/Documents/semester7/automatizacion/worshop-python-selenium-gherkin/output.txt 2>&1 
deactivate
