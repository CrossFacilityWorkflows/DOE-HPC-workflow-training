from balsam.api import Job
import numpy as np

n_gpus = 4

input_temps = np.arange(0.72,2.16,0.12)
#velocities = [1.44]

jobs = [Job(app_id="Lammps",
            site_name="perlmutter-jointdemos",
            workdir=f"LJ/{n}",
            parameters={"NGPUS": n_gpus,"tinit": tinit},
            num_nodes=1,
            ranks_per_node=n_gpus,
            gpus_per_rank=1,
            threads_per_core=2,
            threads_per_rank=32, #This sets OMP_NUM_THREADS
            launch_params={"gpu-bind":"none"},
            tags={"parameter_test":"velocity"}
        )
        for n,tinit in enumerate(input_temps)]

jobs = Job.objects.bulk_create(jobs)


