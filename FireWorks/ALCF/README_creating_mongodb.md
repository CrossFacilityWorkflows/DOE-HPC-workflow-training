# Creating a MongoDB on Polaris

Adapted from notes kindly provided by Alvaro Vazquez: https://gist.github.com/alvarovm/80e635ca67d48b2437c639927a430411

First, log on to Polaris

```
mkdir mongodb
cd mongodb
```

## Download MongoDB files we need

First get mongodb server for suse 15

```
wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-suse15-6.0.5.tgz
tar -xvf mongodb-linux-x86_64-suse15-6.0.5.tgz
```

Next get MongoDB shell

```
wget https://downloads.mongodb.com/compass/mongosh-1.8.0-linux-x64.tgz
tar -xvf mongosh-1.8.0-linux-x64.tgz
```

## Configure Mongo Server

We can use this sample config file. Note that you'll need
to modify the paths for your username and installation
location. Note you'll also need to create the `testdb`
directory.

You'll also need to choose a login node number,
a port number of the form 275{xx} and contains two extra digits,
and you'll need to enter the internal IP of the login node. You
can find the IP of your chosen login node by sshing to it and
running the `hostname -I` command. For example:

```
(base) stephey@polaris-login-01:~/mongodb> hostname -I
10.201.0.58 10.140.56.123 172.22.56.104 172.23.56.104 140.221.112.11 
```

Make sure you choose the IP address that starts with `10.{}`.


```
stephey@polaris-login-{}:~/mongodb> cat mj.mongod.conf 
storage:
  dbPath: /home/stephey/testdb
  journal:
    enabled: true
#  engine:
#  wiredTiger:

# where to write logging data.
systemLog:
  destination: file
  logAppend: true
  path: /home/stephey/testdb/mongod.log

# network interfaces
net:
  port: 275{xx}
  bindIp: 10.{}
#  bindIpAll: true

# how the process runs
processManagement:
  #fork: true
  timeZoneInfo: /usr/share/zoneinfo
```

You can copy this file and fill in the information we described
above.

## Start your Mongo Server

The rest of the tutorial only works if the Mongo Server
remains alive! We'll use `screen` to achieve this.

First start a screen session

```
screen -S mongodb_fireworks
```

Now use our configuration file to start up a MongoDB server

```
mongodb-linux-x86_64-suse15-6.0.5/bin/mongod -f mj.mongod.conf
```

Now we can detach from this server using `Cntl+a d`, or we can open a new Polaris
terminal.

## Now let's connect to running server using the Mongo Shell

Note you'll need to modify this command depending on the login node IP and port number you chose.

```
stephey@polaris-login-01:~/mongodb> mongosh-1.8.0-linux-x64/bin/mongosh --host 10.201.0.58 --port 27560
```

Using the Mongo Shell, we can create a database called `DATABASE_NAME` for user `DATABASE_USER`
with password `DATABASE_PASSWORD`. Note you should set a real password.

```
test> db = db.getSiblingDB('DATABASE_NAME')
DATABASE_NAME
DATABASE_NAME> db.createUser( { user: "DATABASE_USER", pwd: "DATABASE_PASSWORD", roles: [ "readWrite", "dbAdmin" ]} )
{ ok: 1 }
DATABASE_NAME> exit 
```

As a preview, this is the information you'll be prompted to enter when you configure FireWorks.
Make sure you note this information somewhere safe.

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

