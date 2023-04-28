# Installing FireWorks at ALCF- Polaris

## Creating a FireWorks conda environment

In the steps that follow we'll create a FireWorks conda environment
that contains all the dependencies needed to run the demo in this
tutorial. 

```
module load PrgEnv-gnu conda
conda create -n fireworks python=3.9 -y
conda activate fireworks
conda install -c conda-forge fireworks pytest numpy scikit-learn pandas -y
MPICC="cc -shared" pip install --force-reinstall --no-cache-dir --no-binary=mpi4py mpi4py
```

## Initializing our FireWorks launchpad

Now that we've installed and activated FireWorks, the next step is to initialize
our launchpad (the part of FireWorks that interfaces with our MongoDB). 

Note here you'll need to remember the information that you used to set up your
Mongo Server. If you type `lpad init` you should be prompted to enter this information.

```
(fireworks) stephey@polaris-login-01:~/fireworks> lpad init
Please supply the following configuration values
(press Enter if you want to accept the defaults)

Enter host parameter. (default: localhost). Example: 'localhost' or 'mongodb+srv://CLUSTERNAME.mongodb.net': 10.201.0.58
Enter port parameter. (default: 27017). : 27560
Enter name parameter. (default: fireworks). Database under which to store the fireworks collections: DATABASE_NAME
Enter username parameter. (default: None). Username for MongoDB authentication: DATABASE_USER
Enter password parameter. (default: None). Password for MongoDB authentication: DATABASE_PASSWORD
Enter ssl_ca_file parameter. (default: None). Path to any client certificate to be used for Mongodb connection:
Enter authsource parameter. (default: None). Database used for authentication, if not connection db. e.g., for MongoDB Atlas this is sometimes 'admin'.:

Configuration written to my_launchpad.yaml!
```

## Checking to see if our lpad is configured correctly

One way to check to see if your launchpad is working is to try the `lpad reset` command.
If you see something like this, your MongoDB and FireWorks setup are working correctly.

```
(fireworks) stephey@polaris-login-01:~/fireworks> lpad reset
Are you sure? This will RESET 0 workflows and all data. (Y/N)y
2023-04-06 05:33:02,693 INFO Performing db tune-up
2023-04-06 05:33:02,897 INFO LaunchPad was RESET.
(fireworks) stephey@polaris-login-01:~/fireworks>
```

FireWorks is now ready to help you run workflows.
