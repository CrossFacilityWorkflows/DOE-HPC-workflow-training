from balsam.api import BatchJob, Site
import sys

if len(sys.argv) < 2:
    raise TypeError(f"{sys.argv[0]} requires: account at command line")

site_name = "nersc_tutorial"
site = Site.objects.get(site_name)

BatchJob.objects.create(
    site_id=site.id,
    num_nodes=2,
    wall_time_min=10,
    job_mode="mpi",
    project=str(sys.argv[1]),
    queue="regular",
)
