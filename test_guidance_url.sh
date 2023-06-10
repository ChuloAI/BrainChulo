#!/bin/bash

curl -X POST http://0.0.0.0:9000 \
-H "content-type: application/json" \
-d "{\"prompt_template\": \"hi, sir A{{gen 'name' max_tokens=2 temperature=1}}\", \"output_vars\": [], \"guidance_kwargs\":{}, \"input_vars\": {}}"