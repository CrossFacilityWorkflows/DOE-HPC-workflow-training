# Parsl Tutorial at ALCF

To open the tutorial notebook on Polaris, you will need to create an ssh tunnel.  From a shell on your computer, follow these instructions, but replace the port number `9900` with an integer of your choice between 9000 and 65535 (it needs to be unique from other users):

```
ssh -L 9900:localhost:9900 csimpson@polaris.alcf.anl.gov
module load conda
conda activate /grand/projects/WALSforAll/conda_environments/parsl
jupyter notebook --no-browser --port 9900
```
The shell will generate a path that looks like `http://localhost:9900/?token=xxxxx`.  Copy and paste it in a local browser.  Navigate to your copy of the workshop repository on the file system and open the notebook `0_molecular-design-with-parsl.ipynb`.
