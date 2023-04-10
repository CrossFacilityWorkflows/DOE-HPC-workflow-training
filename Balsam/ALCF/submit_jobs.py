from balsam.api import BatchJob,Site

site_name = "polaris-jointdemos"
site = Site.objects.get(site_name)

BatchJob.objects.create(
    site_id=site.id,
    num_nodes=2,
    wall_time_min=10,
    job_mode="mpi",
    project="datascience",
    queue="debug",
)