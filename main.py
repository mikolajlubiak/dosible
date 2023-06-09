import os.path
import subprocess
import docker

client = docker.from_env()
container = client.containers.run("ubuntu:latest", detach=True)
print(container.exec_run("echo hello world"))

f = open("demo.dsbl", "r")
lines = f.readlines()
names = []

packageManagers = {
    "/etc/redhat-release": ["yum"],
    "/etc/arch-release": ["pacman", "-S"],
    "/etc/gentoo-release": ["emerge"],
    "/etc/SuSE-release": ["zypp"],
    "/etc/debian_version": ["apt-get", "install"],
    "/etc/alpine-release": ["apk"],
}
packageManager = ""
for path, package_manager in packageManagers.items():
    if os.path.isfile(path):
        packageManager = package_manager
        
for line in lines:
    if line.startswith("#"):
        pass
    elif ":" in line:
        name = ""
        for char in line:
            if char == ":":
                break
            name += char
        names.append(name)
    elif line.startswith("RUN"):
        command = line.lstrip("RUN").split()
        subprocess.run(command) 
    elif line.startswith("INSTALL"):
        packages = line.lstrip("INSTALL").split()
        subprocess.run(packageManager, packages) 
        
print(names)
print(packageManager)