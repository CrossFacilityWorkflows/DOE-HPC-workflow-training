# Parsl at OLCF

To open the tutorial notebook on Summit, you will need to create an ssh tunnel.  From a shell on your computer, follow these instructions, but replace the port number `9900` with an integer of your choice between 9000 and 65535 (it needs to be unique from other users):

```
ssh -L 9900:localhost:9900 tskluzac@summit.olcf.ornl.gov
module load python
source activate /gpfs/alpine/world-shared/stf001/tutorial10
jupyter notebook --no-browser --port 9900
```
The shell will generate a URL that looks like `http://localhost:9900/?token=xxxxx`.  Copy and paste it in a local browser.  Navigate to your copy of the workshop repository on the file system and open the notebook `mol-design-demo.ipynb`.
