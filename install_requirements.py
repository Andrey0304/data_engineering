import subprocess
import os
import sys


def install_reqs(path_to_dir: str,
                 path_to_reqs='requirements.txt'):
    """Installs the required packages to the given directory"""
    
    if not os.path.exists(path_to_reqs):
        response = subprocess.run(
                        f'pip freeze > {path_to_reqs}',
                        stderr=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        shell=True
                    )
        if response.returncode != 0:
            logging.critical(f'\n{response.stderr}')
            os.remove(path_to_reqs)
            sys.exit()
    if not os.path.exists(path_to_dir):
        os.mkdir(path_to_dir)
    
    response = subprocess.run(
                f"pip install -r {path_to_reqs} -t {path_to_dir}",
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                shell=True
        )
    if response.returncode != 0:
        logging.critical(f'\n{response.stderr}')
    else:
        print('All dependencies were installed successfully.')


if __name__ == '__main__':
    import yaml
    import logging
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join('config', 'config.yaml')
    config = yaml.safe_load(open(config_path))

    PathToDir = config['required_packages_dir']
    PathToReqs = config['required_packages_file']
    logging.basicConfig(**config['logger'])

    install_reqs(PathToDir, PathToReqs)
