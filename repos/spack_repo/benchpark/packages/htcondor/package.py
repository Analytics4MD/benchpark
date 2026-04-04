import hashlib
import os

from spack.package import *


class Htcondor(Package):
    """HTCondor is a high-throughput computing software framework for
    coarse-grained distributed parallelization of computationally intensive
    tasks.

    This package installs from HTCondor's pre-built Linux binary tarballs
    (the same artifacts fetched by get.htcondor.org).  Source builds are
    not yet implemented.
    """

    homepage = "https://htcondor.org"
    git = "https://github.com/htcondor/htcondor.git"

    url = "https://htcss-downloads.chtc.wisc.edu/tarball/current/25.7.2/release/condor-25.7.2-src.tar.gz"

    license("Apache-2.0")

    # -------------------------------------------------------------------------
    # Versions
    #
    # To handle binary installs correctly, we fetch the source tarball using
    # the "version()" directive, and we fetch the binary tarball using the
    # "resource()" directive.
    # -------------------------------------------------------------------------

    # HTCondor versions are split between LTS and feature releases.
    # Versions formatted as "X.0.Y" are LTS releases. For example,
    # 25.0.8 is the latest LTS release at the time of writing.
    # Other versions are feature releases.
    version(
        "25.7.2",
        sha256="7abf70d2e097285ae2376c1d04203242434192ab4e23b177007dd7c3a19c0ff6",
        preferred=True,
    )
    version(
        "25.6.1",
        sha256="0722ce9b24919bfaeb6042d0480832e910ee015e3258bdfb38c72214f19822e3",
    )
    version(
        "25.0.8",
        sha256="b116bbb73855a39f2922a144088e89d964e4e611924fa709f77653b4a9f14599",
    )

    # -------------------------------------------------------------------------
    # Variants
    # -------------------------------------------------------------------------

    # TODO: add a +binary / ~binary variant once source builds are supported.
    # When added, ~binary would cause HTCondor to be built from source with CMake.
    # This will also require HTCondor's full dependency set to be included in this
    # package. Currently, only binary installs are implemented.

    variant(
        "personal",
        default=False,
        description=(
            "Create a single-user, personal install. "
            "This involves running 'make-personal-from-tarball' after install. "
            "This variant should be enabled for personal Condor pools or for submitting "
            "to resource managers like Slurm or Flux."
        ),
    )

    # -------------------------------------------------------------------------
    # Per-platform binary tarball SHA256 checksums
    #
    # Keys are "<version>/<arch_family>/<htcondor_os_label>" where:
    #   arch_family       — spec.architecture.target.family.name (x86_64 | aarch64 | ppc64le)
    #   htcondor_os_label — a HTCondor-native operating system name
    #
    # Source: official sha256sum.txt published alongside each release at
    #   https://htcss-downloads.chtc.wisc.edu/tarball/current/<ver>/release/
    # -------------------------------------------------------------------------

    _binary_sha256 = {
        "25.7.2": {
            "x86_64": {
                "AlmaLinux8": "c980c168dbd2e8a1b77e9a8ebccfe85e74ccf7dcc4777d711eeb2ed625a9d9cd",
                "AlmaLinux9": "7990652bf1693c618b0223bf60fc5ddadb5496e40872d55016ab648a527dd1ae",
                "AlmaLinux10": "7f36bd1a7b26a236dfb7c2c5f1b765492345785c920f62fadb1e4cc02ecb4ca0",
                "AmazonLinux2023": "dedc0068bc702c06e8065cc22d8d4a623971ef1236f36d6a405c477d8be60fa6",
                "Debian12": "8519a0ecf11b65abdc036e324e1465353bc85d64a5c71ccdea8ee37694ce27f2",
                "Debian13": "e8010052e152dcba15493c30d3dc17c2d65478226c7f294a9a6d00d04b899a91",
                "Ubuntu22": "672d1ab42dc7c600dabcfc7a931e21ed2878f96f7c8d5fe25a2b3cb2f05421d3",
                "Ubuntu24": "4165cef52dd4622e062a53481b2b92389e814e70878c407537de9165cd4a710f",
                "openSUSE15": "4ca404025fc022322383e1f3beb33ec417014d5d452672c659d2744939a33ff6",
                "openSUSE16": "e0a27dbd00d9f9ce5d249095cc0a7c865116578f4f6c48659861a4ba873d1e0f",
                "SLES15SP5": "098562114523a100f0cac9fae798c28a2505b59e6546be381cdd6de1a600de3c",
            },
            "aarch64": {
                "AlmaLinux8": "86913ea20d41eca4544160a1ba9a99c676411033c52283e158a2a91e495ebc98",
                "AlmaLinux9": "c7fda1dcff667a9aea5d92e63115ad9469a16eaf982ebb3e5269eafeed36c3ec",
                "AlmaLinux10": "1a17f0e5d9975f87a29e0b72f211bfe2c1245173696928d86919f33f71af0842",
                "Ubuntu24": "4c513a2eb68a4d9ce5946be00b6f7f7614d0ec51645d9a5315b1af18f4370255",
            },
            "ppc64le": {
                "AlmaLinux8": "f3fd6eaed63c24da8c887dbaaad06a071c1e5bbb222be403af320df432f5437b",
            },
        },
        "25.6.1": {
            "x86_64": {
                "AlmaLinux8": "c2f1e5f823ca297a4ba71e9782d2f46268ed8e8fe000ab6b8a612f8cd1baea1e",
                "AlmaLinux9": "3f9bab5500be475720c9b778be7a4a402d0e3bbce879468f8a494fbfa80418ac",
                "AlmaLinux10": "d454cd6d419aa8b4e043689c3df0319f94044834d3de45150f520f6ab0d5cb33",
                "AmazonLinux2023": "b176a5d9d77866c77ea5bda507f713a60a96f3729617d9cf6f32d62617b1db4d",
                "Debian12": "9d5d63be59a96c0229b99e739d83300a6194a0a21cb6263381e4bc3c60040e23",
                "Debian13": "e61203414bf580cc1bbf6a90f79182711e15bd070a7538552125419623c9f0f9",
                "Ubuntu22": "cb461d7d5a1f1ebc6e360137659d3dbc87e88a59af83cb7a38060f84c7d4f631",
                "Ubuntu24": "76ef2ba5d05f5bb15c031390f6f622f8083be3404fcf8ba49c4bd3e2fa58b02e",
                "openSUSE15": "c55238b92429a36d38ae5e7c21a8e121ed963193526234d7e7fd1590bdce59a2",
                "openSUSE16": "ef3cd0d017fa78f76d4b2741c57cdbafca491c99af5a96d41f0e3cb41568a5be",
                "SLES15SP5": "af46538d9ec00fa4e105201a0258abbd96d154869219b69818139743d3103375",
            },
            "aarch64": {
                "AlmaLinux8": "b7071ecc5572afa2705c7aec84c0aa06a024b419ce8ef35adce83284ca0323b2",
                "AlmaLinux9": "734198d6d7f524f930b137f269236b7c6e413c11437d58d880d58c2ad43691b4",
                "AlmaLinux10": "f6b99009f6ffdf986562fd409a35850b9f9dd28a7c76281c6d3faeba3c01a62d",
                "Ubuntu24": "9be0d469881e46abb75f3d61623dca82a136a4d6b880de791a1732cffea56763",
            },
            "ppc64le": {
                "AlmaLinux8": "dccb596839cee486f8ab65b0872ca9322028db901ff47d2d6fcf84b0b8cf228e",
            },
        },
        "25.0.8": {
            "x86_64": {
                "AlmaLinux8": "c2f1e5f823ca297a4ba71e9782d2f46268ed8e8fe000ab6b8a612f8cd1baea1e",
                "AlmaLinux9": "3f9bab5500be475720c9b778be7a4a402d0e3bbce879468f8a494fbfa80418ac",
                "AlmaLinux10": "d454cd6d419aa8b4e043689c3df0319f94044834d3de45150f520f6ab0d5cb33",
                "AmazonLinux2023": "b176a5d9d77866c77ea5bda507f713a60a96f3729617d9cf6f32d62617b1db4d",
                "Debian12": "9d5d63be59a96c0229b99e739d83300a6194a0a21cb6263381e4bc3c60040e23",
                "Debian13": "e61203414bf580cc1bbf6a90f79182711e15bd070a7538552125419623c9f0f9",
                "Ubuntu22": "cb461d7d5a1f1ebc6e360137659d3dbc87e88a59af83cb7a38060f84c7d4f631",
                "Ubuntu24": "76ef2ba5d05f5bb15c031390f6f622f8083be3404fcf8ba49c4bd3e2fa58b02e",
                "openSUSE15": "c55238b92429a36d38ae5e7c21a8e121ed963193526234d7e7fd1590bdce59a2",
                "openSUSE16": "ef3cd0d017fa78f76d4b2741c57cdbafca491c99af5a96d41f0e3cb41568a5be",
                "SLES15SP5": "af46538d9ec00fa4e105201a0258abbd96d154869219b69818139743d3103375",
            },
            "aarch64": {
                "AlmaLinux8": "b7071ecc5572afa2705c7aec84c0aa06a024b419ce8ef35adce83284ca0323b2",
                "AlmaLinux9": "734198d6d7f524f930b137f269236b7c6e413c11437d58d880d58c2ad43691b4",
                "AlmaLinux10": "f6b99009f6ffdf986562fd409a35850b9f9dd28a7c76281c6d3faeba3c01a62d",
                "Ubuntu24": "9be0d469881e46abb75f3d61623dca82a136a4d6b880de791a1732cffea56763",
            },
            "ppc64le": {
                "AlmaLinux8": "dccb596839cee486f8ab65b0872ca9322028db901ff47d2d6fcf84b0b8cf228e",
            },
        },
    }

    # A mapping of HTCondor OS names to corresponding Spack OS names
    _reverse_os_map = {
        "AlmaLinux8": ["almalinux8", "rhel8", "rocky8", "centos8"],
        "AlmaLinux9": ["almalinux9", "rhel9", "rocky9", "centos9"],
        "AlmaLinux10": ["almalinux10", "rhel10", "rocky10", "centos10"],
        "AmazonLinux2023": ["amzn2023"],
        "Debian12": ["debian12"],
        "Debian13": ["debian13"],
        "Ubuntu22": ["ubuntu22.04"],
        "Ubuntu24": ["ubuntu24.04"],
        "openSUSE15": ["opensuse-leap15", "opensuse15"],
        "openSUSE16": ["opensuse-leap16", "opensuse16"],
        "SLES15SP5": ["sles15"],
    }

    # Directory under "spack-src" where the contents of the binary tarball
    # should be extracted
    _binary_tarball_extract_dest = "binary_tarball_extract"

    # This nested for loop executes the "resource()" directives that tell
    # Spack to fetch the correct binary tarball for the version of HTCondor,
    # requested architecture, and requested operating system.
    #
    # This is effectively a workaround for the fact that the "version()" directive
    # does not have a "when=..." argument.
    #
    # TODO if/when Spack adds support for "when=..." arguments in "version()"
    #      directives, this entire loop can be reworked to define versions per
    #      OS and architecture combo.
    for _ver, _ver_dict in _binary_sha256.items():
        # Get the "series" associated with the version.
        #
        # If the minor version number is 0, the version is an LTS release.
        # In this case, the series is simply "<major>.0".
        #
        # If the minor version number is not 0, the version is a feature release.
        # In this case, the series is "<major>.X".
        _ver_series = _ver.split(".")[:2]
        if _ver_series[1] != "0":
            _ver_series[1] = "x"
        _ver_series = ".".join(_ver_series)
        for _arch, _arch_dict in _ver_dict.items():
            for _os_label, _sha in _arch_dict.items():
                # Create the tarball name and URL based on:
                #   * The version
                #   * The version series
                #   * The architecture (e.g., x86_64, aarch64)
                #   * The HTCondor OS name (e.g., Ubuntu22, AlmaLinux8)
                _tarball_name = f"condor-{_ver}-{_arch}_{_os_label}-stripped.tar.gz"
                _tarball_url = (
                    f"https://htcss-downloads.chtc.wisc.edu"
                    f"/tarball/{_ver_series}/{_ver}/release/{_tarball_name}"
                )
                # Use _reverse_os_map to convert the HTCondor OS name to a list of
                # corresponding Spack OS names
                _spack_oses = _reverse_os_map.get(_os_label, [_os_label.lower()])
                for _spack_os in _spack_oses:
                    resource(
                        name=f"bin-{_arch}-{_os_label}",
                        url=_tarball_url,
                        sha256=_sha,
                        when=f"@{_ver} target={_arch}: os={_spack_os}",
                        destination=_binary_tarball_extract_dest,
                    )

    def url_for_version(self, version):
        """Return the platform-specific binary tarball URL for `version`."""
        ver = str(version)
        # Convert the first two components of the version into the
        # version series. If the version is an LTS, the series will be
        # "<major>.0". If the version is a feature release, the series
        # will be "<major>.x"
        ver_series = ver.split(".")[:2]
        if ver_series[1] != "0":
            ver_series[1] = "x"
        ver_series = ".".join(ver_series)
        # Generate the full URL for the source tarball
        name = f"condor-{ver}-src.tar"
        return (
            f"https://htcss-downloads.chtc.wisc.edu"
            f"/tarball/{ver_series}/{ver}/release/{name}"
        )

    def install(self, spec, prefix):
        # TODO add a conditional switch when the "binary" variant is added
        self._install_binary(spec, prefix)

    def _install_binary(self, spec, prefix):
        """Verify and install the binary tarball that Spack has already fetched."""

        import glob

        # Get the path to the directory where the binary tarball was extracted
        binary_tarball_dir = join_path(
            self.stage.source_path, self._binary_tarball_extract_dest
        )

        # Find the top-level condor directory (name varies by OS/version)
        subdirs = glob.glob(join_path(binary_tarball_dir, "condor-*"))
        if not subdirs:
            raise InstallError(
                f"Could not find extracted HTCondor directory in {binary_tarball_dir}"
            )

        # Step inside the top-level directory and install its contents (i.e., the contents
        # of the binary tarball)
        install_tree(subdirs[0], prefix)

        # If running with +personal, run the "make-personal-from-tarball" script
        # to configure HTCondor as a single-user, personal install
        if "+personal" in spec:
            tty.msg("Running make-personal-from-tarball...")
            make_personal = Executable(
                join_path(prefix, "bin", "make-personal-from-tarball")
            )
            make_personal()
        else:
            # Write a minimal CONDOR_CONFIG that points everything back into the
            # Spack prefix so condor_* tools work without daemon setup.
            # Users who want a full pool can overlay their own config on top.
            condor_config = join_path(prefix, "etc", "condor_config")
            if not os.path.exists(condor_config):
                mkdirp(join_path(prefix, "etc"))
                with open(condor_config, "w") as f:
                    f.write(
                        f"# Minimal HTCondor config generated by Spack.\n"
                        f"# Override by setting CONDOR_CONFIG in your environment.\n"
                        f"RELEASE_DIR = {prefix}\n"
                        f"LOCAL_DIR   = {prefix}/var\n"
                        f"LIBEXEC     = {prefix}/libexec/condor\n"
                        f"include : $(RELEASE_DIR)/etc/condor_config.local.stub\n"
                    )

    def setup_run_environment(self, env):
        # Set the CONDOR_CONFIG environment variable to point to the config
        # in the install prefix only if not already set
        condor_config = join_path(self.prefix, "etc", "condor_config")
        if os.path.exists(condor_config):
            if "CONDOR_CONFIG" not in os.environ:
                env.set("CONDOR_CONFIG", condor_config)

        # Update PATH to make the HTCondor command line tools (e.g., condor_submit,
        # condor_q) available
        env.prepend_path("PATH", join_path(self.prefix, "bin"))

        # Update MANPATH to make HTCondor's manpages available
        env.prepend_path("MANPATH", join_path(self.prefix, "man"))

        # Search for the HTCondor Python bindings and, if found, add
        # their directory to PYTHONPATH.
        #
        # HTCondor installs these into either:
        #   * <prefix>/lib/python3/dist-packages (for Debian-based OSes)
        #   * <prefix>/lib/python3.X/site-packages (other OSes)
        lib_dir = join_path(self.prefix, "lib")
        if os.path.isdir(lib_dir):
            for entry in os.listdir(lib_dir):
                candidate = os.path.join(lib_dir, entry)
                if entry.startswith("python") and os.path.isdir(candidate):
                    for sub in ("site-packages", "dist-packages"):
                        sp = os.path.join(candidate, sub)
                        if os.path.isdir(sp):
                            env.prepend_path("PYTHONPATH", sp)
