from balsam.api import ApplicationDefinition

class Lammps(ApplicationDefinition):

    site = "polaris-jointdemos"

    environment_variables = {"OMP_PROC_BIND":"spread", "OMP_PLACES":"cores"}

    def preprocess(self):
        import shutil
        import fileinput
        try:
            velocity = self.job.data["velocity"]
            shutil.copy("/home/csimpson/polaris/polaris-jointdemos/lj_lammps_template.in","lj.in")
            with fileinput.FileInput("lj.in", inplace = True, backup ='.template') as f:
                for line in f:
                    if "velocity" in line:
                        print(f"velocity	all create {velocity} 87287 loop geom", end ='\n')
                    else:
                        print(line, end ='')

            self.job.state = "PREPROCESSED"
        except:
            self.job.state="FAILED"
            self.job.state_data = {"error": "Preprocess failed to create input file"}
            
    def shell_preamble(self):
        return f'''source /home/csimpson/polaris/polaris-jointdemos/lammps_envs.sh'''

    command_template = '/lus/eagle/projects/datascience/csimpson/lammps/my-lammps/lammps-3Nov2022/src/lmp_polaris_nvhpc_kokkos -in lj.in -k on g {{NGPUS}} -sf kk -pk kokkos neigh half neigh/qeq full newton on'

Lammps.sync()

