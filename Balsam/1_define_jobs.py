from balsam.api import Job
import numpy as np

n_gpus = 4
site_name = "ALCF_tutorial"

#initial_temps = np.arange(0.72,2.16,0.12)
lattices = np.arange(0.15,0.85,0.05)

jobs = [Job(app_id="Lammps",
            site_name=site_name,
            workdir=f"LJ/{n}",
            parameters={"NGPUS": n_gpus,"tinit":1.5, "lat_scale": lat_scale,"input_file_path":input_file_path},
            num_nodes=1,
            ranks_per_node=n_gpus,
            gpus_per_rank=1,
            threads_per_rank=8, #This sets OMP_NUM_THREADS
            launch_params={"cpu_bind":"depth"},
            tags={"parameter_test":"density"},
        )
        for n,lat_scale in enumerate(lattices)]

jobs = Job.objects.bulk_create(jobs)