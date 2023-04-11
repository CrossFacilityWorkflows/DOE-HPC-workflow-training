# FireWorks at OLCF

This tutorial demonstrates the [FireWorks](https://materialsproject.github.io/fireworks/) workflow management system on the [Summit](https://www.top500.org/system/179397/) supercomputer at [OLCF](https://www.olcf.ornl.gov/). Specifically, this tutorial shows how to use the Python API provided by FireWorks in order to run a simple machine learning workflow on Summit.

You will need to work out of a directory to which Summit's compute nodes can read and write (for example, within `$PROJWORK` but not `$HOME`). For more information, see [this page](https://docs.olcf.ornl.gov/data/index.html#data-storage-and-transfers). Here, we use `$DEMO_DIR` as a convention.

## Building your custom FireWorks environment

We'll use a custom Conda environment to install Fireworks. We're also installing packages that we'll use in our demo. 
```bash
$ export DEMO_DIR="${PROJWORK}/stf019/fireworks-demo" # Note: change project ID
$ module load gcc
$ module load python
$ conda create -p ${DEMO_DIR}/conda-stuff
$ source activate ${DEMO_DIR}/conda-stuff
$ conda install -c conda-forge fireworks numpy pandas pytest scikit-learn
$ MPICC="mpicc -shared" pip install --no-cache-dir --no-binary=mpi4py mpi4py
```

## Configuring your MongoDB

FireWorks uses [MongoDB](https://www.mongodb.com/) for persistent storage. You will need to [request access to Slate](https://docs.olcf.ornl.gov/services_and_applications/slate/getting_started.html) and follow [these directions](https://docs.olcf.ornl.gov/services_and_applications/slate/use_cases/mongodb_service.html) in order to launch an instance of MongoDB on Slate. You should follow the directions for connecting to the Marble cluster, not Onyx, and you must follow far enough to expose MongoDB outside of the cluster. You will end up with a MongoDB that has a username `admin` and a password `password`, as well as a port number -- the NodePort that is automatically assigned. In the documentation example, this means you would run the following on your personal machine:
```bash
$ oc get service mongo
NAME    TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)           AGE
mongo   NodePort   172.25.233.185   <none>        27017:32093/TCP   13s
```
The important number in the above example is 32093. You will need it as the port number to construct a MongoDB URI:
```
mongodb://admin:password@apps.marble.ccs.ornl.gov:32093/test?authSource=admin
```

## Configuring FireWorks

No additional steps are necessary for configuration, except to export the MongoDB URI constructed in the previous section as an environment variable in your shell:
```bash
$ export MONGODB_URI="mongodb://admin:password@apps.marble.ccs.ornl.gov:32093/test?authSource=admin"
```

That variable will then be used by the Python programs to connect to the MongoDB database.
