from spack.package import *
from spack_repo.builtin.build_systems.python import PythonPackage


class PyA4xOrchestration(PythonPackage):
    """Abstracts the process of configuring workflows for various workflow
    management systems (WMS)."""

    homepage = "https://github.com/Analytics4MD/a4x-orchestration"

    pypi = "a4x-orchestration/a4x_orchestration-0.1.0b5.tar.gz"
    git = "https://github.com/Analytics4MD/a4x-orchestration.git"

    maintainers("ilumsden")

    license("Apache-2.0 WITH LLVM-exception", checked_by="ilumsden")

    version("main", branch="main", git=git)
    version(
        "0.1.0b5",
        sha256="a71ad079dd7041cf7979995beba2e3d4d62186d5fc1b60d3783dbadc07da1a43",
        preferred=True,
    )

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools@64:", type="build")

    depends_on("py-ruamel-yaml@0.18:0.18", type=("build", "run"))
    depends_on("py-networkx", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-pydantic@2:", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))

    depends_on("py-importlib-metadata", type=("build", "run"), when="^python@:3.9")
    depends_on("py-eval-type-backport", type=("build", "run"), when="^python@:3.9")
