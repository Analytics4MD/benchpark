# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage


class A4xCore(CMakePackage):
    """TBA"""

    homepage = "https://github.com/Analytics4MD/a4x-core"
    git = "https://github.com/Analytics4MD/a4x-core.git"

    maintainers("ilumsden")

    license("Apache-2.0 WITH LLVM-exception", checked_by="ilumsden")

    version("main", branch="main")
    version("0.1.0", tag="v0.1.0")

    variant(
        "dtl",
        values=auto_or_any_combination_of("mpi", "filesystem", "dyad").with_default(
            ("mpi", "filesystem")
        ),
        description="The DTL plugins to build with A4X-Core",  # TODO add description
    )
    variant(
        "caliper",
        default=False,
        description="Enable Caliper support for performance monitoring",
    )
    variant(
        "dftracer",
        default=False,
        description="Enable DFTracer support for performance monitoring",
    )
    variant(
        "log-level",
        default="none",
        values=("none", "trace", "debug", "info", "warn", "error", "critical"),
        description="Compiled logging level support for A4X",
    )
    variant("tests", default=False, description="Build and enable unit tests")

    # Language requirements
    depends_on("cxx", type="build")

    # Dependencies that are always required
    depends_on("mpi")
    depends_on("nlohmann-json")
    depends_on("fmt")
    depends_on("spdlog")

    # Optional dependencies for DTL plugins
    depends_on("dyad", when="dtl=dyad")

    # Optional dependencies for performance monitoring
    depends_on("caliper", when="+caliper")
    depends_on("adiak", when="+caliper")
    depends_on("py-pydftracer", when="+dftracer")

    # TODO change into a for loop over combinations/permutations
    conflicts(
        "+caliper",
        when="+dftracer",
        msg="A4X-Core cannot be built with multiple profilers simultaneously",
    )

    def cmake_args(self):
        args = []

        # DTL plugins
        args.append(self.define("WITH_MPI_DTL", "dtl=mpi" in self.spec))
        args.append(self.define("WITH_FS_DTL", "dtl=filesystem" in self.spec))
        args.append(self.define("WITH_DYAD_DTL", "dtl=dyad" in self.spec))

        # Serialization
        # TODO consider if this should be removed
        args.append(self.define("WITH_NLOHMANN_SERIALIZATION", "ON"))

        # Profiler
        if "+caliper" in self.spec:
            args.append(self.define("A4X_PROFILER", "CALIPER"))
        elif "+dftracer" in self.spec:
            args.append(self.define("A4X_PROFILER", "DFTRACER"))
        else:
            args.append(self.define("A4X_PROFILER", "NONE"))

        # Log level (CMake expects uppercase)
        args.append(
            self.define("A4X_LOG_LEVEL", self.spec.variants["log-level"].value.upper())
        )

        # Unit tests
        if "+tests" in self.spec:
            args.append(self.define_from_variant("ENABLE_UNIT_TESTS", "tests"))

            # Code coverage is not exposed as a Spack variant because it forces a
            # Debug build and is typically not useful in a package-manager context.
            args.append(self.define("ENABLE_CODE_COVERAGE", False))

        return args

    # ---------------------------------------------------------------------------
    # Optional: run CTest after build when +tests is active
    # ---------------------------------------------------------------------------

    @run_after("build")
    def check(self):
        if self.run_tests:
            with working_dir(self.build_directory):
                ctest("--output-on-failure")
