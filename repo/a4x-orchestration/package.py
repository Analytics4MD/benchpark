from spack import *


class A4xOrchestration(CachedCMakePackage):
    homepage = "https://analytics4md.org"
    git = "git@github.com:Analytics4MD/a4x-orchestration.git"

    maintainers("ilumsden")

    version("main", branch="main")
    version("0.1.0", tag="v0.1.0")

    version("explicit_sync_hooks", branch="explicit_sync_hooks")

    depends_on("mpi", type=("build", "link"))
    depends_on("nlohmann-json", type="link")
