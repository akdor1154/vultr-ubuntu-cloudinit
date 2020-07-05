#!/usr/bin/env python3

import yaml
import json
import sys

yamlDoc = yaml.load(sys.stdin, Loader=yaml.SafeLoader)
json.dump(yamlDoc, sys.stdout)
