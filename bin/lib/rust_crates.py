import json
import urllib


def get_builder_user_agent_id():
    return "Compiler Explorer Library Builder (github.com/compiler-explorer/infra)"


def get_manual_user_agent_id():
    return "Compiler Explorer (github.com/compiler-explorer/infra)"


class RustCrate:
    def __init__(self, libid, libversion, agent):
        self.libid = libid
        self.version = libversion
        self.cratesio = "https://crates.io"
        self.agent = agent
        self.crateinfo = self.LoadCrateInfo()

    def LoadCrateInfo(self):
        url = f"{self.cratesio}/api/v1/crates/{self.libid}/{self.version}"
        req = urllib.request.Request(url)
        req.add_header("User-Agent", self.agent)
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())
        return data

    def GetDownloadUrl(self):
        download_path = self.crateinfo["version"]["dl_path"]
        download_url = f"{self.cratesio}{download_path}"

        return download_url


class TopRustCrates:
    def __init__(self):
        self.cratesio = "https://crates.io"
        self.agent = get_manual_user_agent_id()

    def list(self, limit=100):
        url = f"{self.cratesio}/api/v1/crates?page=1&per_page={limit}&sort=downloads"
        req = urllib.request.Request(url)
        req.add_header("User-Agent", self.agent)
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())

        crates = []

        for crate in data["crates"]:
            crates.append(dict(libid=crate["id"], libversion=crate["max_stable_version"]))

        return crates


class RustCudaCrates:
    def __init__(self):
        self.cratesio = "https://crates.io"
        self.agent = get_manual_user_agent_id()
        # Define the Rust-CUDA crates we need
        self.cuda_crates = [ "cuda-builder", "cuda-std"]
    
    def list(self):
        """Return the list of Rust-CUDA crates we need to download."""
        crates = []
        for crate in self.cuda_crates:
            crates.append(dict(libid=crate, libversion=self.get_latest_version(crate)))
        return crates
        
    def get_latest_version(self, libid):
        """Get the latest version of a crate from crates.io."""
        url = f"{self.cratesio}/api/v1/crates/{libid}"
        req = urllib.request.Request(url)
        req.add_header("User-Agent", self.agent)
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())
        return data["crate"]["max_version"]