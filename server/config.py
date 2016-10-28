import yaml


class _Config(dict):

    def update_from_file(self, config_file_path):
        try:
            config = yaml.safe_load(open(config_file_path))
        except Exception as e:
            print 'problem loading config file: {ex}'.format(ex=e)
            raise e
        self.update(config)


config = _Config()
config.update_from_file('config.yml')
