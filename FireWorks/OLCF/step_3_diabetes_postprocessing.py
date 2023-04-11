#!/usr/bin/python3

"""
diabetes postprocessing
"""

import os
import numpy as np
import pandas as pd

# Save project directory. Note the use of ${PROJWORK} -- this prevents problems
# that arise because ${HOME} is not available on Summit's compute nodes.
demo_dir = os.getenv("DEMO_DIR")

all_coeffs = np.load(os.path.join(demo_dir, "all_coeffs.npy"))

np.set_printoptions(precision=3)
print(all_coeffs)

#put results into dict with attribute as key

results = dict()
results["age"] = [all_coeffs[0]]
results["sex"] = [all_coeffs[1]]
results["body_mass_index"] = [all_coeffs[2]]
results["blood_pressure"] = [all_coeffs[3]]
results["total_cholesterol"] = [all_coeffs[4]]
results["ldl_cholesterol"] = [all_coeffs[5]]
results["hdl_cholesterol"] = [all_coeffs[6]]
results["total/hdl_cholesterol"] = [all_coeffs[7]]
results["log_of_serum_triglycerides"] = [all_coeffs[8]]
results["blood_sugar_level"] = [all_coeffs[9]]

df = pd.DataFrame.from_dict(results)

# print to terminal

print("pearson correlation coefficients for each attribute")
print(df.transpose().head(10))
