import json


def update_config(config_parameter: str, value: str):
    """Function that updates config value
    @param config_parameter: config parameter to update
    @param value: new value of config parameter
    """

    with open('config.json', 'r') as config_file:
        cfg = json.load(config_file)
    cfg[config_parameter] = value
    with open('config.json', 'w') as config_file:
        json.dump(cfg, config_file)


def get_config_parameter_value(config_parameter: str):
    """Function that returns config value
    @param config_parameter: config parameter to get
    @return: config value
    """

    with open('config.json', 'r') as config_file:
        cfg = json.load(config_file)
    return cfg[config_parameter]
