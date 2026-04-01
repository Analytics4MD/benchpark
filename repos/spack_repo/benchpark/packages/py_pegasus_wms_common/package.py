from spack.package import *
from spack_repo.builtin.build_systems.python import PythonPackage


class PyPegasusWmsCommon(PythonPackage):
    """Pegasus Workflow Management System Python Common"""

    homepage = "https://pegasus.isi.edu"

    # Default to PyPI for standard releases (handles >= 5.1 PEP 625 naming)
    pypi = "pegasus-wms.common/pegasus_wms_common-5.1.2.tar.gz"

    # Fallback to GitHub for development versions
    git = "https://github.com/pegasus-isi/pegasus.git"

    license("Apache-2.0")

    # -------------------------------------------------------------------------
    # Versions
    # -------------------------------------------------------------------------
    version("master", branch="master", git=git)

    version(
        "5.1.2",
        sha256="0007256f4d1baa983c23e2967a7634cea1d51620bd37d2d8e521ed038c78ab50",
    )
    version("5.1.1", sha256="FIXME")
    version("5.0.9", sha256="FIXME")

    # -------------------------------------------------------------------------
    # Dependencies
    # -------------------------------------------------------------------------
    depends_on("python@3.5:", when="@:5.0.9", type=("build", "run"))
    depends_on("python@3.6:", when="@5.1:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pyyaml@5.3.1:", type=("build", "run"))
    depends_on("py-dataclasses", when="@5.1: ^python@3.6", type=("build", "run"))

    # -------------------------------------------------------------------------
    # Fetch Logic
    # -------------------------------------------------------------------------
    def url_for_version(self, version):
        """Handle the shift to PEP 625 filename normalization in v5.1.0."""
        if version < Version("5.1"):
            # Legacy naming convention: pegasus-wms.common-5.0.9.tar.gz
            return f"https://pypi.io/packages/source/p/pegasus-wms.common/pegasus-wms.common-{version}.tar.gz"

        # For >= 5.1, let Spack use the 'pypi' attribute to generate the URL
        return super().url_for_version(version)

    # -------------------------------------------------------------------------
    # Build System
    # -------------------------------------------------------------------------
    @property
    def build_directory(self):
        """Handle the difference between the PyPI tarball and GitHub monorepo."""
        if self.spec.satisfies("@master"):
            return "packages/pegasus-common"
        return "."
