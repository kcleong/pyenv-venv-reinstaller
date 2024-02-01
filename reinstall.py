#!/usr/bin/python3
import argparse
import os
import subprocess


class ReinstallVirtualEnv:
    def __init__(self, dry_run=True):
        self.pyenv_versions_path = os.path.expanduser("~/.pyenv/versions")
        self.dry_run = dry_run

    @property
    def directories(self):
        """Get a list of directories containing "__" """
        directories = [d for d in os.listdir(self.pyenv_versions_path) if "__" in d]
        directories.sort()
        return directories

    @property
    def versions(self):
        for directory in self.directories:
            yield directory.split("__")[1]

    def repair_all(self):
        for version in self.versions:
            self.repair(version)

    def repair(self, python_version):
        target_virtual_envs = []
        for directory in self.directories:
            version_number = directory.split("__")[1]
            if version_number == python_version:
                target_virtual_envs.append(directory)

        if not target_virtual_envs:
            print(
                f"Could not find '{python_version}' in {self.pyenv_versions_path}, aborting.."
            )
            exit(1)

        self._print(f"Targeting {python_version}, with the following virtual envs:")
        for virtual_env in target_virtual_envs:
            print(f"  {virtual_env}")

        self._print("Uninstalling pyenv virtualenvs:")
        for virtual_env in target_virtual_envs:
            self._run(f"pyenv uninstall -f {virtual_env}")

        self._print("Uninstalling pyenv version")
        self._run(f"pyenv uninstall -f {python_version}")

        self._print("Installing pyenv version")
        self._run(f"pyenv install {python_version}")

        self._print("Installing pyenv virtualenvs:")
        for virtual_env in target_virtual_envs:
            self._run(f"pyenv virtualenv {python_version} {virtual_env}")

    def _run(self, command, dry_run=False):
        if self.dry_run:
            print(f"Dry running: {command}")
        else:
            print(command)
            subprocess.run(command, shell=True)

    @staticmethod
    def _print(text):
        print("\n")
        print("-" * 80)
        print(text)
        print("-" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Script to reinstall pyenv versions and virtualenvs"
    )
    parser.add_argument(
        "-r",
        "--run",
        action="store_true",
        help="Apply changes (no dry run)",
    )
    parser.add_argument("-v", "--version", type=str, help="Pyenv virtualenv version")

    args = parser.parse_args()

    if args.run:
        dry_run = False
    else:
        print("** Dry-run is enabled, changes are not applied **")
        dry_run = True

    reinstaller = ReinstallVirtualEnv(dry_run)

    if args.version:
        reinstaller.repair(args.version)
    else:
        reinstaller.repair_all()


if __name__ == "__main__":
    main()
