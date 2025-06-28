import importlib

def load_config(env_name):
    print(f" ++++++Loading configuration for environment: {env_name}")

    module_name = f'env_config.{env_name}'
    print(f" ++++++Module name: {module_name}")

    try:
        return importlib.import_module(module_name)
    except ImportError:
        raise ValueError(f"Invalid environment: {env_name}")


if __name__ == '__main__':
    load_config('default')
