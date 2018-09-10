import argparse
import pathlib
import trafaret as T

from trafaret_config import commandline

BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = BASE_DIR / 'config' / 'dev.yaml'

TRAFARET = T.Dict({
    T.Key('mysql'):
        T.Dict({
            'database': T.String(),
            'user': T.String(),
            'password': T.String(),
            'host': T.String(),
            'port': T.Int(),
            'minsize': T.Int(),
            'maxsize': T.Int(),
        }),
    T.Key('host'): T.IP,
    T.Key('port'): T.Int(),
})

def get_config(argv=None):

    ap = argparse.ArgumentParser()
    commandline.standard_argparse_options(
        ap,
        default_config=DEFAULT_CONFIG_PATH
    )

    options, unknown = ap.parse_known_args(argv)

    if argv:
        options.config = "{}/config/{}.yaml".format(BASE_DIR, options.config)

    config = commandline.config_from_options(options, TRAFARET)

    return config