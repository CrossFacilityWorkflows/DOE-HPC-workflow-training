#!/usr/bin/python3
#
#-  run-workflow.py ~~
#
#-  Do not run this script manually, because it will fail when run on a login
#   node. Instead, this script will be run by the LSF batch script:
#       $ bsub batch-runner.lsf
#

import os
from fireworks import LaunchPad
from fireworks.core.rocket_launcher import rapidfire

# Set up and reset the LaunchPad using MongoDB URI string.
launchpad = LaunchPad(host = os.getenv("MONGODB_URI"), uri_mode = True)

# Launch workflow "locally" -- this will run on a Summit batch node.
print("Looking for workflows ...")
rapidfire(launchpad)
print("Done.")
