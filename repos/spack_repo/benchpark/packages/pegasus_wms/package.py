import hashlib
import os

from spack.package import *


class PegasusWms(Package):
    """Pegasus WMS (Workflow Management System) encompasses a set of
    technologies that help workflow-based applications execute in a
    number of different environments including desktops, campus clusters,
    grids, and clouds.

    Pegasus bridges the scientific domain and the execution environment
    by automatically mapping high-level workflow descriptions onto
    distributed resources.  It automatically locates the necessary input
    data and computational resources required by a workflow, and plans
    out all of the required data transfer and job submission operations
    required to execute the workflow.

    This package installs from Pegasus's pre-built Linux binary tarballs.
    Source builds are not yet implemented.
    """

    homepage = "https://pegasus.isi.edu"
    git = "https://github.com/pegasus-isi/pegasus.git"

    # The url field is only provided as a fallback and as a way for commands
    # like `spack versions` to work. For most work, this URL will be ignored
    # in favor of the dynamic URLs built by "url_for_version"
    url = "https://download.pegasus.isi.edu/pegasus/5.1.2/pegasus-binary-5.1.2-x86_64_rhel_9.tar.gz"

    license("Apache-2.0")

    # -------------------------------------------------------------------------
    # Versions
    #
    # The tarballs for each version of Pegasus are architecture- and OS-specific.
    # As a result, the `version()` entries below do not have SHAs. The SHA
    # validation is performed manually in the `install()` function.
    #
    # Install with `spack install --no-checksum pegasus` to suppress the
    # warning, or set `checksum: false` for this package in your spack.yaml.
    # -------------------------------------------------------------------------

    version("5.1.2", preferred=True)
    version("5.1.1")
    version("5.0.9")

    # -------------------------------------------------------------------------
    # Variants
    # -------------------------------------------------------------------------

    variant(
        "worker",
        default=False,
        description=(
            "Pre-stage the Pegasus worker tarball into the install prefix. "
            "The worker package is a lightweight runtime tarball that Pegasus "
            "stages to remote compute nodes that lack a local Pegasus install. "
            "By default, Pegasus downloads the worker package from the internet "
            "at runtime.  Enable this variant to pre-download the worker tarball. "
            "The tarball is placed at <prefix>/share/pegasus/worker/ and can be "
            "referenced in the Pegasus transformation catalog."
        ),
    )
    variant(
        "mysql",
        default=True,
        description="Install necessary dependencies for using MySQL as the runtime database.",
    )
    variant(
        "postgre",
        default=False,
        description="Install necessary dependencies for using PostgreSQL as the runtime database.",
    )

    # -------------------------------------------------------------------------
    # Dependencies
    # -------------------------------------------------------------------------

    depends_on("java@17:", type="run")
    depends_on("python@3.6:", type="run")
    depends_on("py-pyyaml", type="run")
    depends_on("py-gitpython", type="run")

    depends_on("py-mysqlclient", when="+mysql", type="run")
    depends_on("py-psycopg2", when="+postgre", type="run")

    # -------------------------------------------------------------------------
    # Per-platform tarball SHA256 checksums
    #
    # Keys are "<arch>/<pegasus_os_label>" where:
    #   arch             — spec.architecture.target.family.name (x86_64 | aarch64)
    #   pegasus_os_label — resolved by _pegasus_os_label(spec) below
    #
    # _binary_sha256 holds checksums for the binary (pegasus-binary-*) tarballs.
    # _worker_sha256 holds checksums for the worker (pegasus-worker-*) tarballs.
    #
    # Source: official sha256 published alongside each release at
    # https://download.pegasus.isi.edu/pegasus/<ver>/sha256sums.txt
    # -------------------------------------------------------------------------

    _binary_sha256 = {
        "5.1.2": {
            # aarch64
            "aarch64/alpine_3": "df885aca9ee0ae9209b7e6a92d96f51acb0fbe039d29bc287b550109ea11c894",
            "aarch64/deb_11": "fa290a86dc47d14dae04a579669eacbae670b91e9f9049035f95aa99c1e1408c",
            "aarch64/deb_12": "360d35437435592d2c6652de1c61ce63ea0196c2d699dc20ccee5c69157941ac",
            "aarch64/deb_13": "393d589e4d0e4624606145725e2923008bad99cccaf4a9bc61d41c1808dc91e3",
            "aarch64/rhel_10": "d4c4753308ae50c9be7585768d7b50e437d66a16d712fb95fa2582c9b0a28828",
            "aarch64/rhel_8": "7e04768b7e89e5bc26364df6e276ac65ccea3bbfb9ff73a4b07e468624cfd3a5",
            "aarch64/rhel_9": "af0203394a10f5b21758ef5662c1079eeef5d83cd9bf48faa3828568cd991ab7",
            "aarch64/ubuntu_22": "07b3ee3012dfdc5026810adf15c9614592d2b490e2db727c8e879940babf7e36",
            "aarch64/ubuntu_24": "4ec57c7dee9010245bef2873338ef270a78f326a0d0cd50eaaf32d5aa652a1a5",
            "aarch64/ubuntu_26": "19fc4b3a0fc62c667ccc19085f8523fa3ae1946bed39b5a79bcae5dd0fc987c4",
            # x86_64
            "x86_64/alpine_3": "84a9191c46c17dafcd2ada223f4499d18593c6b4c38c4cd551a2d969cca29934",
            "x86_64/deb_11": "dea736f379d13a63beda46e346c94f30b148cf5e64275a483466641b0073065c",
            "x86_64/deb_12": "1069d14cb20d2d15cdaa6d1c04a92b741ebfccb3c686f0a3d5f6e728850884f1",
            "x86_64/deb_13": "2dc4620fba07ef9df71a6bc9c3f06016af789e572e89d29306e1bd7990cb6ce2",
            "x86_64/rhel_10": "edc36b929b2653aba894170bad1a08e10ace64cfd57c725b0039ad50cc55e8dc",
            "x86_64/rhel_8": "da3d1c5dcbce0b200dc527c006be25cb0e6712d9bd86d5f1c409925c006a7348",
            "x86_64/rhel_9": "59b93954f0f344d126a3716f6e35e272052ec16e0cf3364ae09dd5a4e52760f4",
            "x86_64/suse_15": "cd399652ace217f2784cdff2ac1f325f6cfd29d0afc7d9d5051f98c05e0771d8",
            "x86_64/ubuntu_22": "8a22c5502896a2b16dea66f9c7ebe0e0d6f70626e5c4b3444697effdda23e8f2",
            "x86_64/ubuntu_24": "98cc8bd573a0002a9166141a29af47f6f232f873afaf7e8277d29578dd6e5e45",
            "x86_64/ubuntu_26": "6fceb5bd45782f163973f07c93ecadb56fc641112efbeb580e4a8e0bfcb12cbd",
        },
        "5.1.1": {
            # aarch64
            "aarch64/alpine_3": "074c32d4bc9dc87bb08ef9beba618c49da15a2fe8f19b83042cb73ce432a3354",
            "aarch64/deb_11": "f3216aeb7a68d9395459ae1d7ab4d608caea5673c2d81b16daaabb803c7fbc4a",
            "aarch64/deb_12": "93acadfe3343736722b7f9dbb255eddc2cdd78b3273717d87f7797315bbb569a",
            "aarch64/rhel_10": "53327b5cefef0d5a0abca2b02c6d32729757b81166acdcec610ea521aeded5c0",
            "aarch64/rhel_8": "1ea99fb5ad67623bb64dfc57facfa390f546023b27ff0a94b0d4ebf8278d7799",
            "aarch64/rhel_9": "4842a1dac4d1909d74960d61e99ca5e185c03399b05af012ec632ab24d42cc27",
            "aarch64/ubuntu_22": "ef9ffb97949c2b30d5d215731f47bbe93d86bb47e492948ee625ce80d9e7e4d9",
            "aarch64/ubuntu_24": "48d03001144126fad3428443286acfb4a44c574264104f38cf19ce1d3733dc10",
            # x86_64
            "x86_64/alpine_3": "47c0d17d49ecf2a76584846fb2bf368eb232fb0678ab788729708a24fc332d6c",
            "x86_64/deb_11": "dbc627186fcbcc9a51d0f039c2346e5a93c3882a8d1db1676a759ddbaaaca17c",
            "x86_64/deb_12": "dbe743e2ddbf494f9d7d38ae1ff8b115fa684dc509af29497c1961bac90f1c97",
            "x86_64/rhel_10": "5fec4895a402ccf5af48b2a0a0c51b8107963905b0f66a5737e91b615655aee3",
            "x86_64/rhel_8": "11d3f086f1ed601b94f1fefb52146392c17e4b926f08265d3d19370d57c0947c",
            "x86_64/rhel_9": "e5410f10c39b9d826a9f0d4c33422f9b0b790d93d427e676faf16c4e823b03f1",
            "x86_64/suse_15": "509ac45c668629da3fc3e32f11642776053c0800bd7860c57e8d8e70c174e946",
            "x86_64/ubuntu_22": "486e430a98b69b8e1e032eb6ae2ea98495e3d2a2e6dcf0c4b1c07e131cec374c",
            "x86_64/ubuntu_24": "5ed85a61446ca8e26438a49268a736dce96bb2ed57328b46224706aa92b80cbe",
        },
        "5.0.9": {
            # aarch64
            "aarch64/alpine_3": "71e00f7b171c895956898cf829f3078600e34758419e3c0b245d63bfa5fdf135",
            "aarch64/deb_10": "7ede41442b87167557f7afbb53ae542f4d19aab5e332ded44d2096fdfb199753",
            "aarch64/deb_11": "a7a8fb9965e57e52308878bfd06c9aa8e91141c75334ef2af9eca083065d7b1b",
            "aarch64/deb_12": "54bdd43b3983f40865e4d74bd48e2be2a73af383b314a75cb53737bf472e4e32",
            "aarch64/rhel_8": "aa3677214f278b22582fe46d7854f6c2a6c5b8ab4e30c17f7111719045c6bb74",
            "aarch64/rhel_9": "e8c31a9b488f6085bcae2bd73fa625d21689f8901a70b65fdd73bc93f3ffd1d4",
            "aarch64/ubuntu_20": "4431d73485d6af5860f7862edf9d603128acfcf6fa572c0d554798a4c2b83ddf",
            "aarch64/ubuntu_22": "07898b60b5d59c61a7914db9db3c5b0f17986d9921c21670b1b8deb206158b84",
            # x86_64
            "x86_64/alpine_3": "8ddafd66aee886cdd4f80b02731a38fc368d3253d26088bbcdb5f7cbd988f4ae",
            "x86_64/deb_10": "4dc15b49c83df57abec6de834675f9ec407112259c42abc9d5d6aeac8d967cf7",
            "x86_64/deb_11": "ce2a772d9331450110d4bea02d31e25959265dfd1c12da53eeedab1c4f91a9e3",
            "x86_64/deb_12": "a695c2c762039ed4bf7306e596d5badd714f646cde3cd87a418e9f0ddaf54391",
            "x86_64/rhel_7": "498dfa18041281bea25d4aa99fcc28e8454ee15e9247efd03f30b730f3569fd0",
            "x86_64/rhel_8": "f95beb791fa464f8fefe841ff14eaf5a826084faad00dbce0977755bebfff139",
            "x86_64/rhel_9": "2bc55441dda081396b3cafcdb53def68eb071d34882e478c6483a8c8e0601fd0",
            "x86_64/suse_15": "4fb5bdfe4946e8f0187a52a6d438bc3d20811f70aeecb87514919c72f2b0f391",
            "x86_64/ubuntu_18": "9ee1f10bb7e9ef1b308a7f221b70891977ee6a4e023943124f6c4ca4d50932ff",
            "x86_64/ubuntu_20": "c6995f22e01e532eea9c46e53e9e497d65fff021bbda6d3ec64a990c33f6e100",
            "x86_64/ubuntu_22": "36934d32940338c01f72336e46c9f57c5dbb557e7844eb7679c1077b47701f09",
        },
    }

    _worker_sha256 = {
        "5.1.2": {
            # aarch64
            "aarch64/alpine_3": "63e2974dc588e626bf7fa778fd00bf725ff674774720298761ff3456307439fa",
            "aarch64/deb_11": "c841a5ef9330a7b585149f4f83c178b07e890872a8543e6fcce57cf71b1b633e",
            "aarch64/deb_12": "5e19c1493e741ba9b7564144af1b43809328470f62eaf399f8dcbbc87a135ab8",
            "aarch64/deb_13": "f3d5c2f5a77a328dbb286d7edafa2c7ced41d4e0a9b3d3c3c53b570df02c2bc3",
            "aarch64/rhel_10": "bcfd51cd764a3618a4d4d60f118697e29e4c7eb44b8106f679c5b3c61204cf3b",
            "aarch64/rhel_8": "c0b648d7a0a27aa5fa66e514ee6b5a10dda750c92009912dc5ec0d42bbb609e8",
            "aarch64/rhel_9": "13c29c4549b8e610399260bf1d2af8e1ae19354b85cffb58ebba02e2a9555c27",
            "aarch64/ubuntu_22": "095e3e4772895b41a6a3904163ed6e5c0a0e9ab566dcba790a39e75585dada67",
            "aarch64/ubuntu_24": "ef39da4f2763c9fecb5baa3b3b5dc2c994028812278a202485df3dbf670a3d44",
            "aarch64/ubuntu_26": "7173c61cfd6b735bbea524e57d82d199d09d135ed3b0ee6f273d7003e899131f",
            # x86_64
            "x86_64/alpine_3": "648172fc76fc774e64d65a82e26bffbe115f481d3db05fdbab38b232e2886bbe",
            "x86_64/deb_11": "1dc20fa935e31fdd0521f925935db76f225c3353214ed77bd6577689d0f265a6",
            "x86_64/deb_12": "22a577e365e59407bbd8153892e368ca190584b4df715d67100c5d6398e2a0c4",
            "x86_64/deb_13": "46509b53e270eb13fa8aacb1c709bf801d1aff81081b5a60fd63907b0c319c64",
            "x86_64/rhel_10": "108bc637b5b237e415110e3a7b589b0fd95d4233be8cab87424d2deedd7b5866",
            "x86_64/rhel_8": "77ea9ba1a349d00d695c29a43951bf918584be047c0582b66ae7cdd95a1cb5c4",
            "x86_64/rhel_9": "a9cadca0323bbf1bc607b6e5d6c18219e557a0ea93df84e64d1067cf218abe41",
            "x86_64/suse_15": "d87e586ad565c5c7978755b4a0b0f74fabfe79719baa319bbd91bf7ae7e34427",
            "x86_64/ubuntu_22": "399997cd29f41b3076feb24237ca8754e331c3f4103c986a8d2a9096bffb3f3a",
            "x86_64/ubuntu_24": "32807a3ff3bc4cf2789bc32218e160069280a08a8948af3aa278d699f6cbb581",
            "x86_64/ubuntu_26": "13110b5a87f67bc664bbc627d0e3c97bda09d2a6ed46e27c9567ed0084d2f7fa",
        },
        "5.1.1": {
            # aarch64
            "aarch64/alpine_3": "1605b098b09cfac51e28a0e35f5abfeb9b338949c4a688fde77c832e0ec93511",
            "aarch64/deb_11": "4730b33ff311724edae12bb6431c40982e359572f27ccf1ab11a9c548d8a7508",
            "aarch64/deb_12": "e240637dd0a4b71427ef068caa37b1239dbfeb3fda95caef10c997696533ca97",
            "aarch64/rhel_10": "4755b784ad82827964f3220f274b8eacffb218266bea5b52a4c46c4227df1c39",
            "aarch64/rhel_8": "ec2e0be1c8d18cbe093bfea72f6f69aec48ba3098d12974d0b6529cbb3e0f650",
            "aarch64/rhel_9": "d793552b0e0d863381507d0b7bc2c317eb4dd7c2270caa00acdece5307a27f68",
            "aarch64/ubuntu_22": "73bd3063abd04c8c58bf45c2af3aa83a83f15a31b9bc8896c81a6a39f2cc9e1c",
            "aarch64/ubuntu_24": "5fadb7761439f925d4dba57a72143707cdc1c6aac248b3e5ffa04bd20fa95741",
            # x86_64
            "x86_64/alpine_3": "089f93adba2b350883c201231eca76315395502e1eb7c95df886ab5e5676932b",
            "x86_64/deb_11": "06c287a964681e8ecbffedd28666673d64e7fdb322d456537f847af3ca8b0e8e",
            "x86_64/deb_12": "55b6f8f521300d42036fc5b5df7dc9bbb89a45aa117b8df3a3277d692b72ed26",
            "x86_64/rhel_10": "bdb25980d288e55c49cd55be798eee21fee084042a3981415a62efc1c25c3e7a",
            "x86_64/rhel_8": "d88dabba87e33f7796d5967048b4c8f96510aa8d036cd39770fd3c04b0d60960",
            "x86_64/rhel_9": "130d96fed13b1a1895c3c37b4d2ed7d6b027eed93abb44d85de5ce715498019f",
            "x86_64/suse_15": "10dfab1cbef62bfa610f7562c4a27260ac985cf78284b2987d1feb17d49cad2f",
            "x86_64/ubuntu_22": "b93bc9b95e564966e436f02e0cc544daaa2a66cc8c0afc4f7be707142c91e2cd",
            "x86_64/ubuntu_24": "6879264417779a7ab33919a4b41fc8f884fe490e8f29941f6da14a50f70781cd",
        },
        "5.0.9": {
            # aarch64
            "aarch64/alpine_3": "b797e95335990504cf4220a40b066e7f0df1c42c36f4d313ff001fdfed4c2f48",
            "aarch64/deb_10": "944452f7c150483f7c58a07bc8c14ec333059e63d68ee095780d0b91a3b03218",
            "aarch64/deb_11": "74cc43bcb11d175692e989d0abe5541d386cdecd2e2e205a166c86c16f4f420b",
            "aarch64/deb_12": "65f219ff8ea99ee6c2cc999226960fbc06557cf6a80def0c8cd22885e572a4cd",
            "aarch64/rhel_8": "24da38314bbcc0c99141be6814b6093d997372b9c22c07ccddcfbd883dfdfb44",
            "aarch64/rhel_9": "cc3b31d2de52e6daea393f33d9a70cfe0452c1effe2ca8646b3664d5123f9adb",
            "aarch64/ubuntu_20": "27a8963154f9074dad1249c13d2267d32970ed85fceaca8a02ba10f1d1fd13d2",
            "aarch64/ubuntu_22": "afcb504c99a76fdaac9427ae4c791c49bf0e2db58f3fa408677f4508b5347033",
            # x86_64
            "x86_64/alpine_3": "1f75c534027d3c8ea7152943a63d9dee86df1351fe4545981d3b9c398544168a",
            "x86_64/deb_10": "79fec30cda5cbb8c2ec29013211718945f2438135d5d6caf425c42c2b96b6828",
            "x86_64/deb_11": "d65db4ac49cab8e3a336d51a321c05d7ea9a5e3f24b78f0015ece0ac637f125c",
            "x86_64/deb_12": "c453fff0da80f75ea31a95e5326fe001a6f70710552454ff56bd4b13d0f785a2",
            "x86_64/rhel_7": "e8fe1c9c77c4a2c1e7fc5289fd95e92396b86ec394e44e30741e8f69d2d28e11",
            "x86_64/rhel_8": "5a75382fd40caac42ff7be782ab6f8b7a95e8d9b384e4d9c997c6de21980b53b",
            "x86_64/rhel_9": "fc65bfbf3d8ed0c5398dd26791546c345f0dcd31c1fd87f53355112a7ef7c601",
            "x86_64/suse_15": "b975aab8656b6744ca62ea941dbb87dc8c2005dd8dc211907cc5a86a5fa2c27e",
            "x86_64/ubuntu_18": "0e7e074f7858318589418e66471bc89a64fd24d9594e0e74f7e9acc10ccc5286",
            "x86_64/ubuntu_20": "1d03e4fbf47df24ee47c230e6914b39cde8faa3ec743c8977d25f47409f423ab",
            "x86_64/ubuntu_22": "bdd93db96ab6a85934ea536182d5e7fdddd62b39a022419e414b2456682bbff0",
        },
    }

    # -------------------------------------------------------------------------
    # OS / architecture detection helpers
    # -------------------------------------------------------------------------

    @staticmethod
    def _pegasus_arch(spec):
        """Return the Pegasus architecture string from the concretized spec."""
        family = spec.architecture.target.family.name
        if family in ("x86_64", "aarch64"):
            return family
        raise InstallError(
            f"Unsupported architecture for Pegasus binary install: {family!s}.\n"
            f"Pegasus binary tarballs are only available for x86_64 and aarch64.\n"
            f"Source builds are not yet implemented in this package."
        )

    @staticmethod
    def _pegasus_os_label(spec):
        """Map `spec.architecture.os` to the Pegasus platform string used in
        tarball filenames (e.g. `rhel_9`, `ubuntu_24`, `deb_12`).
        """
        spack_os = spec.architecture.os

        # Each tuple is (prefix, label_fn) where label_fn accepts the version
        # suffix that follows the prefix in the spack_os string.
        os_map = [
            # RHEL family -- Pegasus uses "rhel" for all RHEL-compatible distros
            ("almalinux", lambda v: f"rhel_{v.split('.')[0]}"),
            ("rhel", lambda v: f"rhel_{v.split('.')[0]}"),
            ("centos", lambda v: f"rhel_{v.split('.')[0]}"),
            ("rocky", lambda v: f"rhel_{v.split('.')[0]}"),
            ("ol", lambda v: f"rhel_{v.split('.')[0]}"),
            # Debian family
            ("ubuntu", lambda v: f"ubuntu_{v.split('.')[0]}"),
            ("debian", lambda v: f"deb_{v.split('.')[0]}"),
            # SUSE
            ("opensuse-leap", lambda v: f"suse_{v.split('.')[0]}"),
            ("sles", lambda v: f"suse_{v.split('.')[0]}"),
            # Alpine
            ("alpine", lambda v: f"alpine_{v.split('.')[0]}"),
        ]

        # Checks if the OS name from Spack matches a prefix in the mapping
        # above. If so, get the version suffix and pass it to the corresponding
        # lambda in the mapping. The result of the mapping gets returned.
        for prefix, label_fn in os_map:
            if spack_os.startswith(prefix):
                version_suffix = spack_os[len(prefix) :]
                return label_fn(version_suffix)

        raise InstallError(
            f"No Pegasus binary tarball mapping for Spack OS {spack_os!s}.\n"
            f"Add an entry to _pegasus_os_label() or check\n"
            f"  https://download.pegasus.isi.edu/pegasus/<version>/"
        )

    # -------------------------------------------------------------------------
    # URL / fetch helpers
    # -------------------------------------------------------------------------

    def _platform_key(self):
        """Return the '<arch>/<os_label>' key for the current spec."""
        arch = self._pegasus_arch(self.spec)
        os_label = self._pegasus_os_label(self.spec)
        return f"{arch}/{os_label}"

    def _tarball_basename(self, kind, version=None):
        """Return the filename for a Pegasus tarball.

        Args:
            kind: Either "binary" or "worker".
            version: A provided version string or None. If None, get the version from `self.spec`.
        """
        if kind not in ("binary", "worker"):
            tty.die(
                f"INTERNAL PACKAGE ERROR: 'kind' must be either 'binary' or 'worker'. Got {kind}"
            )
        if version is None:
            ver = str(self.spec.version)
        else:
            ver = version
        arch = self._pegasus_arch(self.spec)
        os_label = self._pegasus_os_label(self.spec)
        return f"pegasus-{kind}-{ver}-{arch}_{os_label}.tar.gz"

    def url_for_version(self, version):
        """Return the platform-specific binary tarball URL for `version`."""
        ver = str(version)
        name = self._tarball_basename("binary", version=ver)
        return f"https://download.pegasus.isi.edu/pegasus/{ver}/{name}"

    def _worker_tarball_url(self):
        """Return the URL for the worker tarball matching the current spec."""
        ver = str(self.spec.version)
        name = self._tarball_basename("worker")
        return f"https://download.pegasus.isi.edu/pegasus/{ver}/{name}"

    def _get_sha256(self, kind):
        """Look up a SHA256 from one of the checksum dicts for the current spec.

        Args:
            kind: Either "binary" or "worker"
        """
        if kind not in ("binary", "worker"):
            tty.die(
                f"INTERNAL PACKAGE ERROR: 'kind' must be either 'binary' or 'worker'. Got {kind}"
            )
        ver = str(self.spec.version)
        key = self._platform_key()
        sha_dict = self._binary_sha256 if kind == "binary" else self._worker_sha256
        try:
            return sha_dict[ver][key]
        except KeyError:
            raise InstallError(
                f"No {kind} SHA256 entry for version={ver}, platform={key}.\n"
                f"Check the SHA256 dicts in the package and add the hash.\n"
                f"Download the tarball from:\n"
                f"  https://download.pegasus.isi.edu/pegasus/{ver}/\n"
                f"and run: sha256sum <tarball>"
            )

    def _verify_sha256(self, filepath, expected):
        """Verify the SHA256 checksum of a file against an expected value."""
        tty.msg(f"Verifying SHA256 of {os.path.basename(filepath)}...")
        hasher = hashlib.sha256()
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                hasher.update(chunk)
        actual = hasher.hexdigest()
        if actual != expected:
            raise InstallError(
                f"SHA256 mismatch for {os.path.basename(filepath)}:\n"
                f"  expected: {expected}\n"
                f"  actual:   {actual}"
            )

    # -------------------------------------------------------------------------
    # Install
    # -------------------------------------------------------------------------

    def install(self, spec, prefix):
        self._install_binary(spec, prefix)

    def _install_binary(self, spec, prefix):
        """Verify and install the binary tarball that Spack has already fetched.

        If +worker is enabled, also fetch the worker tarball and place it
        (as a tarball, not extracted) into <prefix>/share/pegasus/worker/.
        """

        # Verify the binary tarball that Spack has already fetched
        expected = self._get_sha256("binary")
        self._verify_sha256(self.stage.archive_file, expected)

        # Copy the binary tarball's contents into the install prefix
        install_tree(self.stage.source_path, prefix)

        # If +worker is provided, call `_install_worker` to install the worker tarball
        if "+worker" in spec:
            self._install_worker(prefix)

    def _install_worker(self, prefix):
        """Fetch the worker tarball and place it into the install prefix."""
        from spack.fetch_strategy import URLFetchStrategy
        from spack.stage import Stage

        # Get the URL, SHA, and tarball name for the worker
        worker_url = self._worker_tarball_url()
        worker_sha = self._get_sha256("worker")
        worker_basename = self._tarball_basename("worker")

        tty.msg(f"Fetching Pegasus worker package from {worker_url}")

        # Prepare a Stage object for fetching and verifying the worker tarball
        fetcher = URLFetchStrategy(url=worker_url, sha256=worker_sha)
        worker_stage = Stage(
            fetcher,
            name=f"pegasus-worker-{self.spec.version}-stage",
            path=join_path(self.stage.path, "spack-worker-stage"),
            keep=False,
            lock=False,
        )

        try:
            # Fetch the worker tarball and verify its SHA
            # Note that we do NOT extract the worker tarball
            worker_stage.create()
            worker_stage.fetch()
            worker_stage.check()

            # Place the worker tarball (as-is, not extracted) into the prefix.
            worker_dir = join_path(prefix, "share", "pegasus", "worker")
            mkdirp(worker_dir)
            install(worker_stage.archive_file, join_path(worker_dir, worker_basename))

            tty.msg(
                f"Worker tarball installed to:\n"
                f"  {join_path(worker_dir, worker_basename)}"
            )
        finally:
            worker_stage.destroy()

    # -------------------------------------------------------------------------
    # Environment
    # -------------------------------------------------------------------------

    def setup_run_environment(self, env):
        # Update PATH to make the Pegasus command line tools (e.g.,
        # pegasus-plan, pegasus-run, pegasus-status) available
        env.prepend_path("PATH", join_path(self.prefix, "bin"))

        # If +worker was enabled, set PEGASUS_WORKER_PACKAGE_DIR to point to the
        # directory where the worker tarball can be found. This is a convenience
        # environment variable for users.
        if "+worker" in self.spec:
            worker_dir = join_path(self.prefix, "share", "pegasus", "worker")
            if os.path.isdir(worker_dir):
                env.set("PEGASUS_WORKER_PACKAGE_DIR", worker_dir)

        # Invoke `pegasus-config` (in the <preifx>/bin directory) to try to identify
        # the correct PYTHONPATH and CLASSPATH.
        #
        # The `set_pythonpath` and `set_classpath` variables are used to track the
        # success of this process. If not successful, a fallback is invoked below
        pegasus_config_path = join_path(self.prefix, "bin", "pegasus-config")
        set_pythonpath = False
        set_classpath = False
        if os.path.isfile(pegasus_config_path):
            pegasus_config = Executable(pegasus_config_path)

            # Try to identify and set PYTHONPATH using `pegasus-config`
            try:
                python_path = pegasus_config("--python", output=str).strip()
                if python_path and os.path.isdir(python_path):
                    env.prepend_path("PYTHONPATH", python_path)
                    set_pythonpath = True
            except (ProcessError, OSError):
                pass

            # Try to identify and set CLASSPATH using `pegasus-config`
            try:
                classpath = pegasus_config("--classpath", output=str).strip()
                if classpath:
                    env.prepend_path("CLASSPATH", classpath)
                    set_classpath = True
            except (ProcessError, OSError):
                pass

        # Fallback: manually search for Python and Java paths
        if not set_pythonpath:
            lib64_python = join_path(self.prefix, "lib64", "pegasus", "python")
            if os.path.isdir(lib64_python):
                env.prepend_path("PYTHONPATH", lib64_python)

            lib_python = join_path(self.prefix, "lib", "pegasus", "python")
            if os.path.isdir(lib_python):
                env.prepend_path("PYTHONPATH", lib_python)

        if not set_classpath:
            java_dir = join_path(self.prefix, "share", "pegasus", "java")
            if os.path.isdir(java_dir):
                env.prepend_path("CLASSPATH", java_dir)

        # Update MANPATH if man pages are present
        man_dir = join_path(self.prefix, "share", "man")
        if os.path.isdir(man_dir):
            env.prepend_path("MANPATH", man_dir)
