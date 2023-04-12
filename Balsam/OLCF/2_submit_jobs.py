from balsam.api import BatchJob, Site

# The user should first check that their project and queue are in the site's settings.yml file
# The user then has to input project and queue in the BatchJob below

site_name = "summit_tutorial"
site = Site.objects.get(site_name)

BatchJob.objects.create(
    site_id=site.id,
    num_nodes=2,
    wall_time_min=10,
    job_mode="mpi",
    project="",
    queue="",
)