#!/usr/bin/python3

import numpy as np
import pandas as pd
from sklearn.datasets import load_diabetes

#load public diabetes dataset
x_diabetes, y_diabetes = load_diabetes(return_X_y=True)

#dataset info on the docs page: https://scikit-learn.org/stable/datasets/toy_dataset.html#diabetes-dataset
#https://www4.stat.ncsu.edu/~boos/var.select/diabetes.html

#Note: Each of these 10 feature variables have been mean centered and scaled by the standard deviation
#times the square root of n_samples (i.e. the sum of squares of each column totals 1).

# Number of Instances:

#     442
# Number of Attributes:

#     First 10 columns are numeric predictive values
# Target:

#     Column 11 is a quantitative measure of disease progression one year after baseline
# Attribute Information:

#         age age in years

#         sex

#         bmi body mass index

#         bp average blood pressure

#         s1 tc, total serum cholesterol

#         s2 ldl, low-density lipoproteins

#         s3 hdl, high-density lipoproteins

#         s4 tch, total cholesterol / HDL

#         s5 ltg, possibly log of serum triglycerides level

#         s6 glu, blood sugar level

# take a look at the data, but remember it has been mean centered and scaled
print(pd.DataFrame(x_diabetes).describe())

# save attributes
np.save('x_diabetes', x_diabetes)
print("wrote x_diabetes file")

# save disease progression measure
np.save('y_diabetes', y_diabetes)
print("wrote y_diabetes file")

