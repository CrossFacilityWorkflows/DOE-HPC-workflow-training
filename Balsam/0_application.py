from balsam.api import ApplicationDefinition

site_name = "ALCF_tutorial"
demo_path = "/home/csimpson/polaris/DOE-HPC-workflow-training/Balsam"
application_env = demo_path+"/ALCF/lammps_envs.sh"
input_file_path = demo_path+"/lj_lammps_template.in"

class Lammps(ApplicationDefinition):

    site = site_name
            
    def shell_preamble(self):
        return f'source {application_env}'


    command_template = 'lmp -in {{input_file_path}} -k on g {{NGPUS}} -var tinit {{tinit}} -var lat_scale {{lat_scale}} -sf kk -pk kokkos neigh half neigh/qeq full newton on'
    
        
    def postprocess(self):
        print("starting postprocess")
        try:
            with open("energy.dat","r") as f:
                for line in f:
                    pass
                line_entries = line.split()
                if line_entries[0] == "1000":
                    self.job.data = {"tfinal":float(line_entries[3]), "efinal":float(line_entries[1])+float(line_entries[2]), "Pfinal":float(line_entries[4])}
                    self.job.state = "POSTPROCESSED"
                else:
                    self.job.state = "FAILED"
                    self.job.state_data = {"reason": "Final step not reached"}
        except Exception as e:
            self.job.state = "FAILED"
            self.job.state_data = {"reason": str(e)}        

Lammps.sync()