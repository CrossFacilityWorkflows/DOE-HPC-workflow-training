#!/usr/bin/python3
#
#-  run-workflow.py ~~
#

import os
from fireworks import LaunchPad
from fireworks.core.rocket_launcher import rapidfire

# Set up and reset the LaunchPad using MongoDB URI string.
launchpad = LaunchPad(host = os.getenv("MONGODB_URI"), uri_mode = True)

# Launch workflow locally
print("Looking for workflows ...")
rapidfire(launchpad)
print("Done.")

