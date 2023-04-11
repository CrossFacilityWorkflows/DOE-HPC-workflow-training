from balsam.api import BatchJob, Site

site_name = "summit_tutorial"
site = Site.objects.get(site_name)

BatchJob.objects.create(
    site_id=site.id,
    num_nodes=2,
    wall_time_min=10,
    job_mode="mpi",
    project="WALSforAll",
    queue="R476170",
)