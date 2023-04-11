from balsam.api import Job
import numpy as np
import os

site_name = "cori_tutorial"
demo_path = os.getcwd()
input_file_path = os.path.join(demo_path,"lj_lammps_template.in")

lattice_density = np.arange(0.15,0.85,0.05)

jobs = [Job(app_id="Lammps",
            site_name=site_name,
            workdir=f"LJ/{n}",
            parameters={"tinit":1.5, "lat_scale": lat_scale,"input_file_path":input_file_path},
            num_nodes=1,
            ranks_per_node=32,
            threads_per_core=1,
            launch_params={"cpu_bind":"depth"},
            tags={"parameter_test":"density"},
        )
        for n,lat_scale in enumerate(lattice_density)]

jobs = Job.objects.bulk_create(jobs)
