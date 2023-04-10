import matplotlib.pyplot as plt
from balsam.api import Site,Job

site_name = "ALCF_tutorial"
site = Site.objects.get(site_name)

finished_jobs = Job.objects.filter(state="JOB_FINISHED",site_id=site.id,tags={"parameter_test":"density"})

if finished_jobs.count() > 0:
    efinal = []
    tfinal = []
    density = []
    Pfinal = []
    tinit = []
    for j in finished_jobs:

        efinal.append(j.data['efinal'])
        tfinal.append(j.data['tfinal'])
        Pfinal.append(j.data['Pfinal'])
        density.append(j.get_parameters()['lat_scale'])
        tinit.append(j.get_parameters()['tinit'])

    plt.plot(density,tfinal,'o',label="Temperature")
    plt.plot(density,Pfinal,'s',label="Pressure")
    plt.ylim(0,2.1)
    plt.xlim(0,1)
    plt.ylabel("Temperature, Pressure")
    plt.xlabel("Density")
    plt.legend(loc=0)
    plt.savefig("lammps_phases.png")
