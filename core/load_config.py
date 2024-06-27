import yaml

def load_configuration():
    with open('core/config.yaml', 'r') as file:
        config = yaml.safe_load(file)

    print(f"Environment: {config['environment']}")
    print(f"Base URL: {config['base_url']}")
