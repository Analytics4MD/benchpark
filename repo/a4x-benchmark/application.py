from ramble.appkit import *

from itertools import product


class A4xBenchmark(ExecutableApplication):
    name = "a4x-benchmark"

    workflows = [
        "one_to_one",
        "one_to_one_md",
        "one_to_many",
    ]

    workflow_vars = {
        "one_to_one": (
            "a4x-benchmark OneToOne {num_nodes} {ppn} {numIters} {producerIterTime} {consumerIterTime} {dataSize}",
            [
                (
                    "numIters",
                    "number of iterations for the producer and consumer to run",
                    None,
                ),
                (
                    "producerIterTime",
                    "time (in microseconds) that the producer spends in 'computation' per iteration",
                    None,
                ),
                (
                    "consumerIterTime",
                    "time (in microseconds) that the consumer spends in 'computation' per iteration",
                    None,
                ),
                (
                    "dataSize",
                    "amount of data (in bytes) passed between a producer and a consumer per iteration",
                    None,
                ),
            ],
        ),
        "one_to_one_md": (
            "a4x-benchmark OneToOneMD {ensembleSize} {ppn} {numTimesteps} {timestepDuration} {analysisIterTime} {numAtoms} {stride}",
            [
                (
                    "ensembleSize",
                    "number of producer-consumer pairs to run in parallel as an ensemble workflow",
                    None,
                ),
                (
                    "numTimesteps",
                    "number of emulated MD timesteps to run per producer",
                    None,
                ),
                (
                    "timestepDuration",
                    "time (in microseconds) for a single MD timestep",
                    None,
                ),
                (
                    "analysisIterTime",
                    "time (in microseconds) that analysis (i.e., consumer) takes per iteration",
                    None,
                ),
                ("numAtoms", "number of atoms in the molecular system"),
                (
                    "stride",
                    "number of MD timesteps to run before creating a frame. Must evenly divide numTimesteps",
                    None,
                ),
            ],
        ),
        "one_to_many": (
            "a4x-benchmark OneToMany {num_nodes} {ppn} {numProducers} {numConsumersPerProducer} {taskmap} {numIters} {producerIterTime} {consumerIterTime} {dataSize}",
            [
                ("numProducers", "number of producers in the workflow", None),
                (
                    "numConsumersPerProducer",
                    "number of consumers in the workflow for each producer",
                    None,
                ),
                (
                    "taskmap",
                    "method for mapping workflow tasks to nodes",
                    ["block", "cyclic"],
                ),
                (
                    "numIters",
                    "number of iterations for the producer and consumer to run",
                    None,
                ),
                (
                    "producerIterTime",
                    "time (in microseconds) that the producer spends in 'computation' per iteration",
                    None,
                ),
                (
                    "consumerIterTime",
                    "time (in microseconds) that the consumer spends in 'computation' per iteration",
                    None,
                ),
                (
                    "dataSize",
                    "amount of data (in bytes) passed between a producer and a consumer per iteration",
                    None,
                ),
            ],
        ),
    }

    dtl_plugin_vars = {
        "mpi": [
            (
                "maxDataSize",
                "maximum amount of data that can be transfered at once per producer/consumer",
            ),
        ],
        "filesystem": [
            (
                "rootDir",
                "root directory into which the benchmark will write/read files",
            ),
        ],
    }

    cli_tuples = product(workflow_vars.keys(), dtl_plugin_vars.keys())

    workflow_workloads = {}
    dtl_workloads = {}

    for wflow, dtl in cli_tuples:
        workload_name = "{}_{}".format(wflow, dtl)
        workload_exec_name = "{}_run".format(workload_name)
        workload_exec = "{} {} {}".format(
            workflow_vars[wflow][0], dtl, " ".join([v[0] for v in dtl_plugin_vars[dtl]])
        )
        executable(workload_exec_name, workload_exec, use_mpi=True)
        workload(workload_name, executables=["workload_exec_name"])
