# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.python import PythonPackage


class PyA4xPegasusWms(PythonPackage):
    """Pegasus WMS plugin for the A4X Orchestrator."""

    homepage = "https://pegasus.isi.edu"
    pypi = "a4x-pegasus-wms/a4x_pegasus_wms-0.1.0b0.tar.gz"
    git = "https://github.com/pegasus-isi/a4x-pegasus-wms.git"

    license("Apache-2.0")

    version("main", branch="main", git=git)
    version(
        "0.1.0b0",
        sha256="57b65117331be9f369a41015752f20a30604cf223b3a2f38ff0c9c4a7975146a",
        preferred=True,
    )
    version(
        "0.1.0a1",
        sha256="2a85553c9300bd44fd643aa8ed915f3b911b698cdd17a0935eb8c76bcbb352bf",
    )

    variant(
        "api_only",
        default=False,
        description=(
            "Depend on the lightweight pegasus-wms.api PyPI package instead "
            "of the full Pegasus WMS binary package.  By default, this package "
            "depends on the full Pegasus WMS installation, which includes the "
            "planner, command-line tools, and all runtime components needed to "
            "plan and submit workflows.  Enable +api_only if you only need the "
            "Python API bindings and do not need to plan or run workflows from "
            "this environment."
        ),
    )

    # ---------------------------------------------------------------------------
    # Python version requirement
    # ---------------------------------------------------------------------------

    depends_on("python@3.8:", type=("build", "run"))

    # ---------------------------------------------------------------------------
    # Build dependencies
    # ---------------------------------------------------------------------------

    depends_on("py-setuptools@44:", type="build")
    depends_on("py-wheel", type="build")

    # ---------------------------------------------------------------------------
    # Runtime dependencies
    # ---------------------------------------------------------------------------

    depends_on("py-a4x-orchestration@0.1.0b5:0.1", type=("build", "run"))

    depends_on("pegasus-wms@5:", when="~api_only", type=("build", "run"))
    depends_on("py-pegasus-wms-api@5:", when="+api_only", type=("build", "run"))
