from spack.package import *
from spack_repo.builtin.build_systems.python import PythonPackage


class PyA4xOrchestration(PythonPackage):
    """Abstracts the process of configuring workflows for various workflow
    management systems (WMS)."""

    homepage = "https://github.com/Analytics4MD/a4x-orchestration"

    pypi = "a4x-orchestration/a4x_orchestration-0.1.0b5.tar.gz"
    # git = "https://github.com/Analytics4MD/a4x-orchestration.git"
    git = "git@github.com:Analytics4MD/a4x-orchestration.git"

    maintainers("ilumsden")

    license("Apache-2.0 WITH LLVM-exception", checked_by="ilumsden")

    version("main", branch="main", git=git)
    version(
        "0.1.0b6",
        sha256="2564b6c512777d911a76d97848a4b642e01112a1b6b02aaa06836d1fe5483f8c",
        preferred=True,
    )

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools@64:", type="build", when="@:0.1.0b5")
    depends_on("py-hatchling@1.26:", type="build", when="@0.1.0b6:")
    depends_on("py-hatch-vcs@0.4.0:", type="build", when="@0.1.0b6:")

    depends_on("py-ruamel-yaml@0.18:0.18", type=("build", "run"))
    depends_on("py-networkx", type=("build", "run"))
    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-pydantic@2:", type=("build", "run"))
    depends_on("py-typing-extensions", type=("build", "run"))

    depends_on("py-importlib-metadata", type=("build", "run"), when="^python@:3.9")
    depends_on("py-eval-type-backport", type=("build", "run"), when="^python@:3.9")
