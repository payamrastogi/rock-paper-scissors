import yaml
class Config:
    def __init__(self):
        with open('config.yaml', 'r') as file:
            self.config = yaml.safe_load(file)

    def get_host(self):
        return self.config['host']

    def get_port(self):
        return self.config['port']

if __name__ == "__main__":
    config = Config()
    print(config.get_host())
    print(config.get_port())