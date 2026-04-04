from spack.package import *
from spack_repo.builtin.build_systems.python import PythonPackage


class PyPegasusWmsApi(PythonPackage):
    """Pegasus Workflow Management System Python API"""

    homepage = "https://pegasus.isi.edu"

    # Default to PyPI for standard releases
    pypi = "pegasus-wms.api/pegasus_wms_api-5.1.2.tar.gz"

    # Fallback to GitHub for development versions
    git = "https://github.com/pegasus-isi/pegasus.git"

    license("Apache-2.0")

    version("master", branch="master", git=git)

    version(
        "5.1.2",
        sha256="b6c4acd664bca6abdcbf05b2f82279c3357292a6d8e4d4cb2c2783772c81ec2b",
        preferred=True,
    )
    version(
        "5.1.1",
        sha256="7303a4a5e294951da79441b6dab9fee4688563d60136c8a0132140b946b647c0",
    )
    version(
        "5.0.9",
        sha256="3075378b3a1e041a88a5b204311a68b1e8d720d6db700cce5c603bb9019e2f1e",
    )

    depends_on("python@3.6:", when="@5.1:", type=("build", "run"))
    depends_on("python@3.5:", when="@:5.0.9", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pegasus-wms-common", type=("build", "run"))

    def url_for_version(self, version):
        """Handle the shift to PEP 625 filename normalization in v5.1.0 and later."""
        if version < Version("5.1"):
            # Legacy naming convention: pegasus-wms.api-5.0.9.tar.gz
            return f"https://pypi.io/packages/source/p/pegasus-wms.api/pegasus-wms.api-{version}.tar.gz"

        # For >= 5.1, let Spack use the 'pypi' attribute to generate the URL
        return super().url_for_version(version)

    @property
    def build_directory(self):
        """Get the directory from which any build commands (e.g., when getting code from GitHub) need to be run in.

        When fetching from GitHub (e.g., the master branch), the Python package
        is located in a subdirectory of the Pegasus monorepo. When fetching
        from PyPI, the tarball is just the Python package itself, so the
        setup.py is at the root.
        """
        if self.spec.satisfies("@master"):
            return "packages/pegasus-api"
        return "."
