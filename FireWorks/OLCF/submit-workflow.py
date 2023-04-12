#!/usr/bin/env python3
#
#-  submit-workflow.py ~~
#
#-  Run this workflow on a Summit login node from the demo directory like this:
#       $ source setup-summit.bash
#       $ python3 submit-workflow.py
#

import os

from fireworks import Firework, LaunchPad, ScriptTask, Workflow
from fireworks.core.rocket_launcher import rapidfire

# Set up and reset the LaunchPad using MongoDB URI string.
launchpad = LaunchPad(host = os.getenv("MONGODB_URI"), uri_mode = True)
launchpad.reset("", require_password=False)

# Specify the demo directory via environment variable explicitly. Even though
# this program is running on a login node from the demo directory, the 
# individual Python scripts will execute elsewhere.
demo_dir = os.getenv("DEMO_DIR")

# Create the individual FireWorks and Workflow. The `jsrun` will run on a
# batch node, and the Python scripts will execute on compute nodes.
fw1 = Firework(ScriptTask.from_str("jsrun -n 1 -a 1 -c 1 python3 " +
        os.path.join(demo_dir, "step_1_diabetes_preprocessing.py")),
            name = "step-1")
fw2 = Firework(ScriptTask.from_str("jsrun -n 10 -a 1 -c 1 python3 " +
        os.path.join(demo_dir, "step_2_diabetes_correlation.py")),
            name = "Step-2")
fw3 = Firework(ScriptTask.from_str("jsrun -n 1 -a 1 -c 1 python3 " +
        os.path.join(demo_dir, "step_3_diabetes_postprocessing.py")),
            name = "Step-3")
wf = Workflow([fw1, fw2, fw3], {fw1: fw2, fw2: fw3}, name = "FireWorks demo")

# Store workflow
launchpad.add_wf(wf)
print("Workflow submitted.")

#-  vim:set syntax=python:
