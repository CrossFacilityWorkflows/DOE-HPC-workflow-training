# Installing and configuring FireWorks at NERSC

## Building your custom FireWorks environment

We'll use a custom conda environment to install FireWorks. We're
also installing packages that we'll use in our demo.

```
module load python
conda create -n fireworks python=3.9 -y
conda activate fireworks
conda install -c conda-forge fireworks pytest numpy scikit-learn pandas
MPICC="cc -shared" pip install --force-reinstall --no-cache-dir --no-binary=mpi4py mpi4py
```

Note that I had difficulty getting all packages to resolve with Python 3.10,
so we're using Python 3.9 in this example.

## Configuring your MongoDB

If you are an exising NERSC user and requested a MongoDB
in the registration form for this workshop, please follow the instructions
in the `mongodb_existing_nersc_users.pdf` PDF in this folder.

If you are using a NERSC test account, please follow the instructions in the
`nersc_training_and_mongodb.pdf` PDF in this folder. Note
that a MongoDB has been created for every test account in this
training.

## Configuring FireWorks

Once you have your MongoDB credentials and your FireWorks enviroment
created, you can configure your FireWorks LaunchPad. Note you will 
need to enter the hostname of your database, the port number of
your database, the name of your database, and your admin password.
The other values are optional- press enter to accept the defaults.

```
lpad init

Please supply the following configuration values
(press Enter if you want to accept the defaults)

Enter host parameter. (default: localhost). Example: 'localhost' or 'mongodb+srv://CLUSTERNAME.mongodb.net': mongodb07.nersc.gov
Enter port parameter. (default: 27017). : 
Enter name parameter. (default: fireworks). Database under which to store the fireworks collections: my_db
Enter username parameter. (default: None). Username for MongoDB authentication: my_db_admin
Enter password parameter. (default: None). Password for MongoDB authentication: my_password
Enter ssl_ca_file parameter. (default: None). Path to any client certificate to be used for Mongodb connection: 
Enter authsource parameter. (default: None). Database used for authentication, if not connection db. e.g., for MongoDB Atlas this is sometimes 'admin'.: 

Configuration written to my_launchpad.yaml!
```

This should create a `my_launchpad.yaml` in the current directory.

To test your LaunchPad, you can run

```
lpad -h
```

to see the full help menu or `lpad reset` to reset your database.

```
(fireworks)stephey@perlmutter:login03:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC> lpad reset
Are you sure? This will RESET 0 workflows and all data. (Y/N)y
2023-04-09 14:39:55,678 INFO Performing db tune-up
2023-04-09 14:39:55,737 INFO LaunchPad was RESET.
(fireworks)stephey@perlmutter:login03:/pscratch/sd/s/stephey/DOE-HPC-workflow-training/FireWorks/NERSC> 
```

If this did not produce an error you should be ready to use FireWorks.
