from cloudinit import log as logging
from cloudinit import net as cloudnet
from cloudinit import sources
from cloudinit import util
from cloudinit import url_helper
import json

LOG = logging.getLogger(__name__)

BASE_URL_V1 = 'http://169.254.169.254/'

BUILTIN_DS_CONFIG = {
    'metadata_url': BASE_URL_V1 + 'v1.json',
    'userdata_url': BASE_URL_V1 + 'user-data/user-data',
}

MD_RETRIES = 60
MD_TIMEOUT = 2
MD_WAIT_RETRY = 2

def read_metadata(url, timeout=2, sec_between=2, retries=30):
    response = url_helper.readurl(url, timeout=timeout,
                                  sec_between=sec_between, retries=retries)
    if not response.ok():
        raise RuntimeError("unable to read metadata at %s" % url)
    return json.loads(response.contents.decode())


def read_userdata(url, timeout=2, sec_between=2, retries=30):
    response = url_helper.readurl(url, timeout=timeout,
                                  sec_between=sec_between, retries=retries)
    if not response.ok():
        raise RuntimeError("unable to read metadata at %s" % url)
    return response.contents.decode()

class DataSourceVultr(sources.DataSource):

    dsname = 'Vultr'

    def __init__(self, sys_cfg, distro, paths):
        sources.DataSource.__init__(self, sys_cfg, distro, paths)
        self.distro = distro
        self.metadata = dict()
        self.ds_cfg = util.mergemanydict([
            util.get_cfg_by_path(sys_cfg, ["datasource", "Vultr"], {}),
            BUILTIN_DS_CONFIG])
        self.metadata_address = self.ds_cfg['metadata_url']
        self.userdata_address = self.ds_cfg['userdata_url']
        self.retries = self.ds_cfg.get('retries', MD_RETRIES)
        self.timeout = self.ds_cfg.get('timeout', MD_TIMEOUT)
        self.wait_retry = self.ds_cfg.get('wait_retry', MD_WAIT_RETRY)
        self._network_config = None
        self.dsmode = sources.DSMODE_NETWORK

    def get_data(self):

        md = read_metadata(
            self.metadata_address, timeout=self.timeout,
            sec_between=self.wait_retry, retries=self.retries)
        ud = read_userdata(
            self.userdata_address, timeout=self.timeout,
            sec_between=self.wait_retry, retries=self.retries)

        self.userdata_raw = ud
        self.metadata_full = md

        """hostname is name provided by user at launch.  The API enforces
        it is a valid hostname, but it is not guaranteed to be resolvable
        in dns or fully qualified."""
        self.metadata['instance-id'] = md['instanceid']
        self.metadata['local-hostname'] = md['hostname']
        self.metadata['public-keys'] = md.get('public-keys', None)
        self.vendordata_raw = md.get("vendor_data", None)

        return True

    @property
    def network_config(self):
        """Configure the networking. This needs to be done each boot, since
           the IP information may have changed due to snapshot and/or
           migration.
        """

        return None


# Used to match classes to dependencies
datasources = [
    (DataSourceVultr, (sources.DEP_FILESYSTEM, sources.DEP_NETWORK)),
]


# Return a list of data sources that match this set of dependencies
def get_datasource_list(depends):
    return sources.list_from_depends(depends, datasources)

# vi: ts=4 expandtab
