import subprocess
import os


def download_package(package_name):
    proc = subprocess.Popen(f'apt-get install -y {package_name}', shell=True, stdin=None,
                            stdout=open(os.devnull, "wb"),
                            stderr=subprocess.STDOUT, executable="/bin/bash")
    proc.wait()


