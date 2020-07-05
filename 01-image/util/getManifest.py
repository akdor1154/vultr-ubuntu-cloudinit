#!/usr/bin/env python3

import json
import sys

manifest = json.load(sys.stdin)
lastRun = manifest['last_run_uuid']
vultrBuild = next(
    b
    for b in manifest['builds']
    if b.get('packer_run_uuid') == lastRun
)
sys.stdout.write(vultrBuild['artifact_id']+'\n')