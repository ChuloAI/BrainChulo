#!/bin/bash
trap 'kill $(jobs -p)' EXIT

cd /home/karajan/labzone/gd_tests/langchain_guidance/frontend && npm run serve
conda activa txtgdc2
cd /home/karajan/labzone/gd_tests/langchain_guidance && python gdc_server.py&
