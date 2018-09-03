import trafaret as T

from trafaret_config import commandline

class Options():

    def __init__(self, config):
        self.config = config
        self.print_config_vars = False
        self.print_config = False
        self.check_config = False

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

def get_config():
    options = Options('config/dev.yaml')
    config = commandline.config_from_options(options, TRAFARET)

    return config