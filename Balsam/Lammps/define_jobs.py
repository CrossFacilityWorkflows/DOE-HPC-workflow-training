from balsam.api import Job
import numpy as np

n_gpus = 4

velocities = np.arange(0.72,2.16,0.12)

jobs = [Job(app_id="Lammps",
            site_name="polaris-jointdemos",
            workdir=f"LJ/{n}",
            parameters={"NGPUS": n_gpus},
            data={"velocity":v},
            num_nodes=1,
            ranks_per_node=n_gpus,
            gpus_per_rank=1,
            threads_per_rank=1, #This sets OMP_NUM_THREADS
            launch_params={"cpu_bind":"depth"},
        )
        for n,v in enumerate(velocities)]

jobs = Job.objects.bulk_create(jobs)