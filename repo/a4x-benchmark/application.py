from ramble.appkit import *


class A4xBenchmark(ExecutableApplication):
    name = "a4x-benchmark"

    maintainers = ["ilumsden"]

    executable(
        "md_ensemble_size_scaling",
        "a4x-benchmark OneToOneMD {ensembleSize} {ppn} 112640 930 818400 23558 880 {dtlType} {dtlArgs}",
        use_mpi=True,
    )
    # Ensemble Size Scaling workload from https://doi.org/10.1109/IPDPSW63119.2024.00111
    workload(
        "md_ensemble_size_scaling",
        executables=["md_ensemble_size_scaling"],
    )

    executable(
        "md_molecular_model_size_and_frame_gen_freq_scaling",
        "a4x-benchmark OneToOneMD {ensembleSize} {ppn} {numTimesteps} {timestepDuration} {analysisIterTime} {numAtoms} {stride} {dtlType} {dtlArgs}",
        use_mpi=True,
    )
    # Molecular Model Size Scaling workload from https://doi.org/10.1109/IPDPSW63119.2024.00111
    workload(
        "md_molecular_model_size_scaling",
        executables=["md_molecular_model_size_and_frame_gen_freq_scaling"],
    )
    # Frame Generation Frequency Scaling workload from https://doi.org/10.1109/IPDPSW63119.2024.00111
    workload(
        "md_frame_gen_frequency_scaling",
        executables=["md_molecular_model_size_and_frame_gen_frequency_scaling"],
    )

    # These variables must be set for every workload
    workload_variable(
        name="dtlType",
        default="mpi",
        description="data transport layer (DTL) to use",
        workflow=[
            "md_ensemble_size_scaling",
            "md_molecular_model_size_scaling",
        ],
    )
    workload_variable(
        name="dtlArgs",
        default="1024",
        description="arguments to configure the DTL",
        workflow=[
            "md_ensemble_size_scaling",
            "md_molecular_model_size_scaling",
        ],
    )

    # These variables are workload-specific

    # For the md_..._scaling experiments, 'ensembleSize' and 'ppn' should be
    # set based on the number of GPUs per node.
    workload_variable(
        name="ensembleSize",
        default=1,
        description="number of producer-consumer pairs to run in parallel as an ensemble workflow",
        workflow=[
            "md_ensemble_size_scaling",
            "md_molecular_model_size_scaling",
            "md_frame_gen_frequency_scaling",
        ],
    )
    workload_variable(
        name="ppn",
        default=2,
        description="number of processes per node",
        workflow=[
            "md_ensemble_size_scaling",
            "md_molecular_model_size_scaling",
            "md_frame_gen_frequency_scaling",
        ],
    )
    workload_variable(
        name="numTimesteps",
        default=112640,
        description="number of emulated md timesteps to run per producer",
        workflow=[
            "md_molecular_model_size_scaling",
            "md_frame_gen_frequency_scaling",
        ],
    )
    workload_variable(
        name="timestepDuration",
        default=930,
        description="time (in microseconds) for a single md timestep",
        workflow=[
            "md_molecular_model_size_scaling",
            "md_frame_gen_frequency_scaling",
        ],
    )
    workload_variable(
        name="analysisIterTime",
        default=818400,
        description="time (in microseconds) that analysis (i.e., consumer) takes per iteration",
        workflow=[
            "md_molecular_model_size_scaling",
            "md_frame_gen_frequency_scaling",
        ],
    )
    workload_variable(
        name="numAtoms",
        default=23558,
        description="number of atoms in the molecular system",
        workflow=[
            "md_molecular_model_size_scaling",
            "md_frame_gen_frequency_scaling",
        ],
    )
    workload_variable(
        name="stride",
        default=880,
        description="number of md timesteps to run before creating a frame. must evenly divide numtimesteps",
        workflow=[
            "md_molecular_model_size_scaling",
            "md_frame_gen_frequency_scaling",
        ],
    )

    # Templates for different types of workflows in A4X Benchmark

    # executable(
    #     "one_to_one_md",
    #     "a4x-benchmark OneToOneMD {ensembleSize} {ppn} {numTimesteps} {timestepDuration} {analysisIterTime} {numAtoms} {stride} {dtlType} {dtlArgs}",
    # )
    # workload("one_to_one_md", executables=["one_to_one_md"])

    # exectuable(
    #     "one_to_one",
    #     "a4x-benchmark OneToOne {num_nodes} {ppn} {numIters} {producerIterTime} {consumerIterTime} {dataSize} {dtlType} {dtlArgs}",
    # )
    # workload("one_to_one", executables=["one_to_one"])

    # exectuable(
    #     "one_to_many",
    #     "a4x-benchmark OneToMany {num_nodes} {ppn} {numProducers} {numConsumersPerProducer} {taskmap} {numIters} {producerIterTime} {consumerIterTime} {dataSize} {dtlType} {dtlArgs}",
    # )
    # workload("one_to_many", executables=["one_to_many"])

    # workload_variable(
    #     name="numNodes",
    #     default=1,
    #     description="number of nodes for the run",
    #     workflow=["one_to_one"],
    # )
    # workload_variable(
    #     name="numIters",
    #     default=1,
    #     description="number of iterations for the producer and consumer to run",
    #     workflow=["one_to_one", "one_to_many"],
    # )
    # workload_variable(
    #     name="producerIterTime",
    #     default=1000,
    #     description="time (in microseconds) that the producer spends in 'computation' per iteration",
    #     workflow=["one_to_one", "one_to_many"],
    # )
    # workload_variable(
    #     name="consumerIterTime",
    #     default=1000,
    #     description="time (in microseconds) that the consumer spends in 'computation' per iteration",
    #     workflow=["one_to_one", "one_to_many"],
    # )
    # workload_variable(
    #     name="dataSize",
    #     default=1024,
    #     description="amount of data (in bytes) passed between a producer and a consumer per iteration",
    #     workflow=["one_to_one", "one_to_many"],
    # )
    # workload_variable(
    #     name="ensembleSize",
    #     default=1,
    #     description="number of producer-consumer pairs to run in parallel as an ensemble workflow",
    #     workflow=["one_to_one_md"],
    # )
    # workload_variable(
    #     name="numTimeSteps",
    #     default=112640,
    #     description="number of emulated md timesteps to run per producer",
    #     workflow=["one_to_one_md"],
    # )
    # workload_variable(
    #     name="timeStepDuration",
    #     default=930,
    #     description="time (in microseconds) for a single md timestep",
    #     workflow=["one_to_one_md"],
    # )
    # workload_variable(
    #     name="analysisIterTime",
    #     default=818400,
    #     description="time (in microseconds) that analysis (i.e., consumer) takes per iteration",
    #     workflow=["one_to_one_md"],
    # )
    # workload_variable(
    #     name="numAtoms",
    #     default=23558,
    #     description="number of atoms in the molecular system",
    #     workflow=["one_to_one_md"],
    # )
    # workload_variable(
    #     name="stride",
    #     default=880,
    #     description="number of md timesteps to run before creating a frame. must evenly divide numtimesteps",
    #     workflow=["one_to_one_md"],
    # )
    # workload_variable(
    #     name="numProducers",
    #     default=1,
    #     description="number of producers in the workflow",
    #     workflow=["one_to_many"],
    # )
    # workload_variable(
    #     name="numConsumersPerProducer",
    #     default=2,
    #     description="number of consumers in the workflow for each producer",
    #     workflow=["one_to_many"],
    # )
    # workload_variable(
    #     name="taskmap",
    #     default="block",
    #     description="method for mapping workflow tasks to nodes",
    #     values=["block", "cyclic"],
    #     workflow=["one_to_many"],
    # )
