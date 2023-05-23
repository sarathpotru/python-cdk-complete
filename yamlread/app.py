import yaml

# Load YAML file
with open('file.yaml') as file:
    config = yaml.safe_load(file)

# Access values as variables
value1 = config['key1']['subkey1']
value2 = config['key1']['subkey2']
print(value1)