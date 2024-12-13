from benchpark.error import BenchparkError
from benchpark.directives import variant
from benchpark.experiment import Experiment
from benchpark.expr.builtin.caliper import Caliper


class A4xBenchmark(Experiment, Caliper):
    variant(
        "version",
        default="main",
        description="version of A4X-Benchmark",
    )

    # TODO: if desired, tweak to include generic workloads here
    variant(
        "workload",
        default="one_to_one",
        description="workload to run",
    )

    variant(
        "hicomb_stride_scaling",
        default=False,
        description="Configure and run the stride scaling experiment from https://doi.org/10.1109/IPDPSW63119.2024.00111"
    )

    variant(
        "hicomb_ensemble_size_scaling",
        default=False,
        description="Configure and run the ensemble size scaling experiment from https://doi.org/10.1109/IPDPSW63119.2024.00111"
    )

    variant(
        "hicomb_data_size_scaling",
        default=False,
        description="Configure and run the data size scaling experiment from https://doi.org/10.1109/IPDPSW63119.2024.00111"
    )

    variant(
        "dtl",
        default="mpi",
        values=(
            "mpi",
            "filesystem",
        ),
        description="data transport layer to use",
    )

    variant(
        "rootDir",
        default="$(pwd)",
        description="root directory into which the benchmark will write/read files",
    )
    
    def _compute_hicomb_stride(self):
        pass
    
    def _compute_hicomb_ensemble_size(self):
        pass

    def _compute_hicomb_data_size(self):
        pass

    def compute_applications_section(self):
        # TODO: Replace with conflicts clause
        scaling_modes = {
            "hicomb_stride": self.spec.satisfies("+hicomb_stride_scaling"),
            "hicomb_ensemble_size": self.spec.satisfies("+hicomb_ensemble_size_scaling"),
            "hicomb_data_size": self.spec.satisfies("+hicomb_data_size_scaling"),
        }
        
        scaling_mode_enabled = [key for key, value in scaling_modes.items() if value]
        if len(scaling_mode_enabled) != 1:
            print(scaling_mode_enabled)
            raise BenchparkError(
                f"Only one type of scaling per experiment is allowed for application package {self.name}"
            )
            
        if self.spec.satisfies("+hicomb_stride_scaling"):
            self._compute_hicomb_stride()
        elif self.spec.satisfies("+hicomb_ensemble_size_scaling"):
            self._compute_hicomb_ensemble_size()
        elif self.spec.satisfies("+hicomb_data_size_scaling"):
            self._compute_hicomb_data_size()

    def compute_spack_section(self):
        app_version = self.spec.variants["version"][0]
        dtl_name = self.spec.variants["dtl"][0]

        system_specs = {}
        system_specs["compiler"] = "default-compiler"
        system_specs["mpi"] = "default-mpi"
        
        self.add_spack_spec(system_specs["mpi"])
        self.add_spack_spec(
            self.name,
            [f"a4x-benchmark@{app_version} core_plugins={dtl_name}", system_specs["compiler"]],
        )
