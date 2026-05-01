# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage


class A4xBenchmark(CMakePackage):
    """A benchmark for evaluating the effects of data management tools and workflow/resource management
    systems on the performance of scientific computing workflows.
    """

    homepage = "https://github.com/Analytics4MD/a4x-benchmark"
    git = "https://github.com/Analytics4MD/a4x-benchmark.git"

    maintainers("ilumsden")

    license("Apache-2.0 WITH LLVM-exception", checked_by="ilumsden")

    version("main", branch="main")
    version("0.1.0b2", tag="v0.1.0b2", preferred=True)
    version("0.1.0b1", tag="v0.1.0b1")

    variant("shared", default=True, description="Build shared libraries")
    variant("tests", default=False, description="Build and enable unit tests")

    # Language requirements
    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # Python is required at build time for discovering install paths and at runtime
    # for running the various utility, setup, and teardown commands.
    depends_on("python@3:", type=("build", "run"))

    # Dependencies for the C++ code
    depends_on("mpi")
    depends_on("nlohmann-json")
    depends_on("fmt")
    depends_on("adiak")
    # TODO make optional when A4X-Core perf shim is done
    depends_on("caliper")
    depends_on("a4x-core")

    # Dependencies for the Python code
    depends_on("py-a4x-orchestration@0.1.0b5:0.1.0", type="run")
    depends_on("py-a4x-pegasus-wms@0.1.0b0:0.1.0 ~api_only", type="run")

    # Dependencies for testing
    depends_on("py-pytest", type="test", when="+tests")

    def cmake_args(self):
        args = []

        python_prefix = self.spec["python"].prefix

        args.append(self.define("Python_ROOT_DIR", python_prefix))
        args.append(self.define("Python3_ROOT_DIR", python_prefix))
        args.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))
        args.append(self.define_from_variant("ENABLE_UNIT_TESTS", "tests"))

        args.append(self.define("ENABLE_CODE_COVERAGE", False))

        return args

    @run_after("build")
    def check(self):
        if self.run_tests:
            with working_dir(self.build_directory):
                ctest("--output-on-failure")
            with working_dir(self.stage.source_path):
                pytest = which("pytest")
                pytest("tests/unit/python")
