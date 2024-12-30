from spack import *


class A4xBenchmark(CachedCMakePackage):
    homepage = "https://analytics4md.org/"
    git = "git@github.com:Analytics4MD/a4x-benchmark.git"

    version("main", branch="main")
    version("0.1.0", tag="v0.1.0")

    version("many_to_one", branch="many_to_one")
    version("expanded_perf", branch="expanded_perf")

    core_plugins_values = ("mpi", "filesystem", "dyad")
    variant(
        "core_plugins", default="mpi,filesystem", values=core_plugins_values, multi=True
    )
    variant("caliper", default=False)

    depends_on("a4x-core", type="link")
    depends_on("a4x-orchestration", type="link")

    # Overrides for other A4X packages for specific benchmark versions
    depends_on("a4x-core@main", when="@main", type="link")
    depends_on("a4x-orchestration@main", when="@main", type="link")

    depends_on("mpi", type=("build", "link"))
    depends_on("nlohmann-json", type="link")
    depends_on("fmt", type="link")
    depends_on("caliper", type=("link", "run"))
    depends_on("adiak", type="link")
    depends_on("caliper", when="+caliper", type="link")
    depends_on("adiak", when="+caliper", type="link")
    depends_on("a4x-core +caliper", when="+caliper")

    for cpv in core_plugins_values:
        depends_on(
            "a4x-core plugins={}".format(cpv), when="core_plugins={}".format(cpv)
        )

    def initconfig_package_entries(self):
        entries = super(A4xBenchmark, self).initconfig_package_entries()

        return entries
