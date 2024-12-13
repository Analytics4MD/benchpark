from ramble.appkit import *

_dtl_exe = {
    "mpi": r"mpi {maxDataSize}",
    "filesystem": r"filesystem {rootDir}",
}
_dtl_vars = [
    {
        "name": "maxDataSize",
        "default": 1024,
        "description": "maximum amount of data that can be transfered at once per producer/consumer",
        "dtl": ["mpi"],
    },
    {
        "name": "rootDir",
        "default": "$(pwd)",
        "description": "root directory into which the benchmark will write/read files",
        "dtl": ["filesystem"],
    },
]
_workflow_exe = {
    "one_to_one": r"a4x-benchmark OneToOne {num_nodes} {ppn} {numIters} {producerIterTime} {consumerIterTime} {dataSize}",
    "one_to_one_md": r"a4x-benchmark OneToOneMD {ensembleSize} {ppn} {numTimesteps} {timestepDuration} {analysisIterTime} {numAtoms} {stride}",
    "one_to_many": r"a4x-benchmark OneToMany {num_nodes} {ppn} {numProducers} {numConsumersPerProducer} {taskmap} {numIters} {producerIterTime} {consumerIterTime} {dataSize}",
}
_workflow_vars = [
    {
        "name": "numNodes",
        "default": 1,
        "description": "number of nodes for the run",
        "workflow": ["one_to_one"],
    },
    {
        "name": "ppn",
        "default": 2,
        "description": "number of processes per node",
        "workflow": ["one_to_one"],
    },
    {
        "name": "numIters",
        "default": 1,
        "description": "number of iterations for the producer and consumer to run",
        "workflow": ["one_to_one", "one_to_many"],
    },
    {
        "name": "producerIterTime",
        "default": 1000,
        "description": "time (in microseconds) that the producer spends in 'computation' per iteration",
        "workflow": ["one_to_one", "one_to_many"],
    },
    {
        "name": "consumerIterTime",
        "default": 1000,
        "description": "time (in microseconds) that the consumer spends in 'computation' per iteration",
        "workflow": ["one_to_one", "one_to_many"],
    },
    {
        "name": "dataSize",
        "default": 1024,
        "description": "amount of data (in bytes) passed between a producer and a consumer per iteration",
        "workflow": ["one_to_one", "one_to_many"],
    },
    {
        "name": "ensembleSize",
        "default": 1,
        "description": "number of producer-consumer pairs to run in parallel as an ensemble workflow",
        "workflow": ["one_to_one_md"],
    },
    {
        "name": "numTimeSteps",
        "default": 112640,
        "description": "number of emulated md timesteps to run per producer",
        "workflow": ["one_to_one_md"],
    },
    {
        "name": "timeStepDuration",
        "default": 0.93,
        "description": "time (in microseconds) for a single md timestep",
        "workflow": ["one_to_one_md"],
    },
    {
        "name": "analysisIterTime",
        "default": 818.4,
        "description": "time (in microseconds) that analysis (i.e., consumer) takes per iteration",
        "workflow": ["one_to_one_md"],
    },
    {
        "name": "numAtoms",
        "default": 23558,
        "description": "number of atoms in the molecular system",
        "workflow": ["one_to_one_md"],
    },
    {
        "name": "stride",
        "default": 880,
        "description": "number of md timesteps to run before creating a frame. must evenly divide numtimesteps",
        "workflow": ["one_to_one_md"],
    },
    {
        "name": "numProducers",
        "default": 1,
        "description": "number of producers in the workflow",
        "workflow": ["one_to_many"],
    },
    {
        "name": "numConsumersPerProducer",
        "default": 2,
        "description": "number of consumers in the workflow for each producer",
        "workflow": ["one_to_many"],
    },
    {
        "name": "taskmap",
        "default": "block",
        "description": "method for mapping workflow tasks to nodes",
        "values": ["block", "cyclic"],
        "workflow": ["one_to_many"],
    },
]


class a4xbenchmark(executableapplication):
    name = "a4x-benchmark"
    
    _a4x_workload_by_workflow = {}
    _a4x_workload_by_dtl = {}

    for workflow_name, workflow_cmd_line in _workflow_exe.items():
        for dtl_name, dtl_cmd_line in _dtl_exe.items():
            workload_name = "{}_{}".format(workflow_name, dtl_name)
            workflow_name_exe = workflow_name + "_exe"
            exectuable(
                workflow_name_exe,
                "{} {}".format(workflow_cmd_line, dtl_cmd_line),
                use_mpi=True,
            )
            workload(
                workload_name,
                executables=[workflow_name_exe],
            )
            if workflow_name not in _a4x_workload_by_workflow:
                _a4x_workload_by_workflow[workflow_name] = [workload_name]
            else:
                _a4x_workload_by_dtl[workflow_name].append(workload_name)
            if dtl_name not in _a4x_workload_by_dtl:
                _a4x_workload_by_dtl[dtl_name] = [workload_name]
            else:
                _a4x_workload_by_dtl[dtl_name].append(workload_name)
    
    for dtl_var in _dtl_vars:
        dtl_types = dtl_var["dtl"]
        var_args = dtl_var.copy()
        del var_args["dtl"]
        workloads = []
        for dtl_type in dtl_types:
            workloads.extend(_a4x_workload_by_dtl[dtl_type])
        workload_variable(**var_args, workloads=workloads)
    
    for wflow_var in _workflow_vars:
        wflow_types = wflow_var["workflow"]
        var_args = wflow_var.copy()
        del var_args["dtl"]
        workloads = []
        for wflow_type in wflow_types:
            workloads.extend(_a4x_workload_by_workflow[wflow_type])
        workload_variable(**var_args, workloads=workloads)
