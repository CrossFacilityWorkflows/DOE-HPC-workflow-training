from balsam.api import ApplicationDefinition
import os

site_name = "cori_tutorial"
demo_path = os.getcwd() 
application_env = os.path.join(demo_path,"lammps_envs.sh")

class Lammps(ApplicationDefinition):

    site = site_name
            
    def shell_preamble(self):
        return f'source {application_env}'

    command_template = 'lmp -in {{input_file_path}} -var tinit {{tinit}} -var lat_scale {{lat_scale}}'
    
        
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
