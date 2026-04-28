# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack_repo.builtin.build_systems.cmake import CMakePackage


class Dyad(CMakePackage):
    """DYAD: DYnamic and Asynchronous Data Streamliner."""

    # TODO: Replace with the actual URL for DYAD's source repository
    homepage = "https://github.com/flux-framework/dyad"
    git = "https://github.com/flux-framework/dyad.git"
    url = "https://github.com/flux-framework/dyad/archive/refs/tags/v0.1.0.tar.gz"

    version("main", branch="main")
    version("0.2.0rc0", commit="8c24e75a7b7994a6ecc7ade73ef555358ec55ad1")
    version("0.1.1", sha256="FIXME")  # Replace with actual sha256
    version("0.1.0", sha256="FIXME")  # Replace with actual sha256

    # ── Data transport variant (mutually exclusive) ──────────────────────
    variant(
        "transport_plugin",
        default="ucx",
        description="Data transport plugin for DYAD's Data Plane",
        values=("ucx", "ucx_rma", "margo"),
        multi=False,
    )

    # ── Profiler variant (mutually exclusive) ────────────────────────────
    variant(
        "profiler",
        default="none",
        description="Profiler to use for DYAD",
        values=("perfflow_aspect", "caliper", "dftracer", "none"),
        multi=False,
    )

    # ── Logger variant (mutually exclusive) ──────────────────────────────
    variant(
        "logger",
        default="none",
        description="Logger to use for DYAD",
        values=("flux", "cpp_logger", "none"),
        multi=False,
    )

    # ── Logger level variant ─────────────────────────────────────────────
    variant(
        "logger_level",
        default="none",
        description="Logging level to use for DYAD",
        values=("debug", "info", "warn", "error", "none"),
        multi=False,
    )

    # ── Required dependencies ────────────────────────────────────────────
    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("cmake@3.12:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("flux-core")
    depends_on("jansson@2.10:")

    # ── Optional dependencies (data transport) ───────────────────────────
    depends_on("ucx@1.6:", when="transport_plugin=ucx")
    depends_on("ucx@1.6:", when="transport_plugin=ucx_rma")
    depends_on("mochi-margo", when="transport_plugin=margo")
    depends_on("json-c", when="transport_plugin=margo")

    # ── Optional dependencies (profiler) ─────────────────────────────────
    depends_on("perfflowaspect", when="profiler=perfflow_aspect")
    # depends_on("caliper", when="profiler=caliper")  # Uncomment if available
    depends_on("dftracer", when="profiler=dftracer")

    # ── Optional dependencies (logger) ───────────────────────────────────
    depends_on("cpp-logger", when="logger=cpp_logger")

    def cmake_args(self):
        args = []

        # Always force LIBDIR_AS_LIB off
        args.append(self.define("DYAD_LIBDIR_AS_LIB", False))

        # Never build tests through Spack
        args.append(self.define("DYAD_ENABLE_TESTS", False))

        # Data transport plugin
        args.append(
            self.define("DYAD_ENABLE_UCX_DATA", "transport_plugin=ucx" in self.spec)
        )
        args.append(
            self.define(
                "DYAD_ENABLE_UCX_DATA_RMA", "transport_plugin=ucx_rma" in self.spec
            )
        )
        args.append(
            self.define("DYAD_ENABLE_MARGO_DATA", "transport_plugin=margo" in self.spec)
        )

        # Profiler
        profiler_map = {
            "perfflow_aspect": "PERFFLOW_ASPECT",
            "caliper": "CALIPER",
            "dftracer": "DFTRACER",
            "none": "NONE",
        }
        args.append(
            self.define(
                "DYAD_PROFILER",
                profiler_map[self.spec.variants["profiler"].value],
            )
        )

        # Logger
        logger_map = {
            "flux": "FLUX",
            "cpp_logger": "CPP_LOGGER",
            "none": "NONE",
        }
        args.append(
            self.define(
                "DYAD_LOGGER",
                logger_map[self.spec.variants["logger"].value],
            )
        )

        # Logger level
        logger_level_map = {
            "debug": "DEBUG",
            "info": "INFO",
            "warn": "WARN",
            "error": "ERROR",
            "none": "NONE",
        }
        args.append(
            self.define(
                "DYAD_LOGGER_LEVEL",
                logger_level_map[self.spec.variants["logger_level"].value],
            )
        )

        return args
