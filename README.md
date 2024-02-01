# Reinstall pyenv virtualenv

A very specific script to reinstall pyenv virtual envs.

Can be used for pyenv virtual envs created with the version number in the virtual env name:

    pyenv virtualenv 3.9.17 my_project_name__3.9.17

Use at your own risk! This script does not install python dependencies after a virtual env
has been re-created.

## Usage

Dry run is enabled by default, apply changes with `--run`.

See `./reinstall.py --help` for available options

Reinstall a specific python version and virtual envs:

    ./reinstall.py -v 3.13.1

Apply changes:
    
    ./reinstall.py -v 3.13.1 --run