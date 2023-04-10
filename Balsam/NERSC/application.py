from balsam.api import ApplicationDefinition

class Lammps(ApplicationDefinition):

    site = "perlmutter-jointdemos"

    #environment_variables = {"OMP_PROC_BIND":"spread", "OMP_PLACES":"cores"}

    def preprocess(self):
        import shutil
        import fileinput
        try:
            shutil.copy("/global/homes/c/csimpson/perlmutter-jointdemos/lj_lammps_template.in","lj.in")
            self.job.state = "PREPROCESSED"
        except:
            self.job.state="FAILED"
            self.job.state_data = {"error": "Preprocess failed to create input file"}
            
    def shell_preamble(self):
        return f'''source /global/homes/c/csimpson/perlmutter-jointdemos/nersc_lammps_envs.sh'''

    command_template = 'lmp -in lj.in -k on g {{NGPUS}} -sf kk -pk kokkos newton on neigh half -var tinit {{tinit}}'

    def postprocess(self):
        dat = self.job.data
        energy_file = os.path.abspath("energy.dat")
        try:
            with open(energy_file,"r") as f:
                for line in f:
                    pass
                line_entries = line.split()
                if line_entries[0] == "1000":
                    self.job.data = {**dat,"final_ke":line_entries[1],
                                    "final_pe":line_entries[2],
                                    "final_temp":line_entries[3]}
                    self.job.state="POSTPROCESSED"
                else:
                    self.job.state="FAILED"
                    self.job.state_data = {"reason": "Final step not reached"}
        except:
            self.job.state="FAILED"
            self.job.state_data = {"reason": "Energy file not written"}

Lammps.sync()

