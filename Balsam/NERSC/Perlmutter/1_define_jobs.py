from balsam.api import Job
import numpy as np
import os

# There are 4 GPUS on a Perlmutter node
n_gpus = 4

site_name = "perlmutter_tutorial"
demo_path = os.getcwd()
input_file_path = os.path.join(demo_path,"lj_lammps_template.in")

lat_scales = np.arange(0.15,0.85,0.05)

jobs = [Job(app_id="Lammps",
            site_name=site_name,
            workdir=f"LJ/{n}",
            parameters={"NGPUS": n_gpus,"tinit":1.5, 
                        "lat_scale": lat_scale,
                        "input_file_path":input_file_path},
            num_nodes=1,
            ranks_per_node=n_gpus,
            gpus_per_rank=1,
            threads_per_core=2,
            threads_per_rank=32,
            launch_params={"gpu-bind":"none"},
            tags={"parameter_test":"density"},
        )
        for n,lat_scale in enumerate(lat_scales)]

jobs = Job.objects.bulk_create(jobs)
