dummy_config = False

try:
    import receipt_service.config as conf
except ImportError:
    dummy_config = True


def get_conf(name):
    if dummy_config:
        return None
    else:
        return getattr(conf, name)
