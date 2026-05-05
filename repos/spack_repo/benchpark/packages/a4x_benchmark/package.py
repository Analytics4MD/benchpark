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
    # git = "https://github.com/Analytics4MD/a4x-benchmark.git"
    git = "git@github.com:Analytics4MD/a4x-benchmark.git"

    maintainers("ilumsden")

    license("Apache-2.0 WITH LLVM-exception", checked_by="ilumsden")

    version("main", branch="main")
    version("benchmark_tuo_fixes", branch="benchmark_tuo_fixes")
    version("0.1.0b2", tag="v0.1.0b2", preferred=True)
    version("0.1.0b1", tag="v0.1.0b1")

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

        args.append(self.define("ENABLE_CODE_COVERAGE", False))

        return args
    
    def _get_python_site_packages_dir(self):
        python = self.spec["python"]
        result = python.command(
            "-c",
            "import sysconfig; "
            "p = sysconfig.get_path('purelib', vars={'userbase': '', 'base': ''}); "
            "p = p.lstrip('/'); "
            "p = p[4:] if p.startswith('lib/') else p; "
            "print(p, end='')",
            output=str,
        )
        return join_path(self.prefix.lib, result)

    def setup_run_environment(self, env):
        env.prepend_path("PYTHONPATH", self._get_python_site_packages_dir())

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("PYTHONPATH", self._get_python_site_packages_dir())
        
