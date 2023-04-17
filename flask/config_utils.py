import yaml

class ConfigUtils:
    @staticmethod
    def load(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            dict_ = yaml.safe_load(f)
        return dict_

    def update(filename, key, new_value):
        with open(filename, 'r+', encoding='utf-8') as f:
            dict_ = yaml.safe_load(f)
            dict_[key] = new_value
            f.truncate(0)
            f.seek(0)
            yaml.safe_dump(dict_, f, indent=4, sort_keys=False)