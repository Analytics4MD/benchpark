from benchpark.error import BenchparkError
from benchpark.directives import variant
from benchpark.experiment import Experiment, SingleNode
from benchpark.scaling import Scaling
from benchpark.expr.builtin.caliper import Caliper


def _round(n, base):
    return base * round(n / base)


class A4xBenchmark(Experiment, SingleNode, Scaling, Caliper):
    variant(
        "version",
        default="main",
        description="version of A4X-Benchmark",
    )

    variant(
        "workload",
        default="md_ensemble_size_scaling",
        values=(
            "md_ensemble_size_scaling",
            "md_molecular_model_size_scaling",
            "md_frame_gen_frequency_scaling",
        ),
        description="workload to run",
    )

    variant(
        "two_node",
        default=False,
        description="Two node execution mode. Only supported with certain workloads",
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
        default=None,
        description="root directory into which the benchmark will write/read files for file-based DTL",
    )

    def _print_scaling_ignored_message(self):
        print(
            "NOTICE: the workload '{}' does not support custom scaling. Ignoring scaling parameters.".format(
                self.spec["workload"]
            )
        )

    def _add_dtl_configuration(self, data_size):
        self.add_experiment_variable("dtlType", self.spec.variants["dtl"][0])
        if self.spec.variants["dtl"][0] == "mpi":
            self.add_experiment_variable("dtlArgs", f"{_round(data_size, 1024)}")
        elif self.spec.variants["dtl"][0] == "filesystem":
            self.add_experiment_variable(
                "dtlArgs", f"{self.spec.variants['rootDir'][0]}"
            )

    def _compute_md_ensemble_size(self):
        if self.spec.satisfies("+single_node"):
            self._print_scaling_ignored_message()
            raise NotImplementedError(
                "Single node MD ensemble size scaling not yet implemented"
            )
        elif self.spec.satisfies("+two_node"):
            self._print_scaling_ignored_message()
            raise NotImplementedError(
                "Two node MD ensemble size scaling not yet implemented"
            )
            pass
        else:
            self.add_experiment_variable("ppn", "{sys_gpus_per_node}")
            num_nodes = {"n_nodes": 2}
            scaled_num_nodes = self.scale_experiment_variables(
                {tuple(num_nodes.keys()): list(num_nodes.values())},
                self.spec.variants["scaling-factor"][0],
                self.spec.variants["scaling-iterations"][0],
            )
            for pk, pv in scaled_num_nodes.items():
                self.add_experiment_variable(pk, pv)
            self.add_experiment_variable("ensembleSize", "{ppn} * {n_nodes} / 2")

    def _compute_md_molecular_model_size(self):
        pass

    def _compute_md_frame_gen_freq(self):
        pass

    def compute_applications_section(self):
        # TODO replace with conflicts statements above
        if self.spec.satisfies("dtl=mpi") and self.spec.variants["rootDir"] is not None:
            raise BenchparkError("'rootDir' variant conflicts with 'dtl=mpi'")
        if (
            self.spec.satisfies("dtl=filesystem")
            and self.spec.variants["rootDir"] is None
        ):
            raise BenchparkError("'rootDir' must be provided when 'dtl=filesystem'")
        if (
            self.spec.satisfies("+single_node")
            and self.spec.variants["workload"] != "md_ensemble_size_scaling"
        ):
            raise BenchparkError(
                "'+single_node' conflicts with all workloads except 'md_ensemble_size_scaling'"
            )
        if (
            self.spec.satisfies("+two_node")
            and self.spec.variants["workload"] != "md_ensemble_size_scaling"
        ):
            raise BenchparkError(
                "'+two_node' conflicts with all workloads except 'md_ensemble_size_scaling'"
            )

        if self.spec.satisfies("workload=md_ensemble_size_scaling"):
            self._compute_md_ensemble_size()
        elif self.spec.satisfies("workload=md_molecular_model_size_scaling"):
            self._compute_md_molecular_model_size()
        elif self.spec.satisfies("workload=md_frame_gen_frequency_scaling"):
            self._compute_md_frame_gen_freq()

    def compute_spack_section(self):
        app_version = self.spec.variants["version"][0]
        dtl_name = self.spec.variants["dtl"][0]

        system_specs = {}
        system_specs["compiler"] = "default-compiler"
        system_specs["mpi"] = "default-mpi"

        self.add_spack_spec(system_specs["mpi"])
        self.add_spack_spec(
            self.name,
            [
                f"a4x-benchmark@{app_version} core_plugins={dtl_name}",
                system_specs["compiler"],
            ],
        )
