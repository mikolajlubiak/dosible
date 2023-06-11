import os.path
import subprocess

# import docker
# client = docker.from_env()
# container = client.containers.run("ubuntu:latest", detach=True)
# print(container.exec_run("echo hello world"))

f = open("demo.dsbl", "r")
lines = f.readlines()
names = []

packageManagers = {
    "/etc/redhat-release": ["yum", "install"],
    "/etc/arch-release": ["pacman", "--sync"],
    "/etc/gentoo-release": ["emerge", "--ask"],
    "/etc/SuSE-release": ["zypper", "install"],
    "/etc/debian_version": ["apt-get", "install"],
    "/etc/alpine-release": ["apk", "add"],
}
packageManager = ""
for path, package_manager in packageManagers.items():
    if os.path.isfile(path):
        packageManager = package_manager

for line in lines:
    words = line.split()
    if words[0][0] == '#':
        pass
    elif words[0][-1] == ':':
        names.append(words[0][:-1])
    elif words[0] == "RUN":
        command = words[1:]
        subprocess.run(command)
    elif words[0] == "INSTALL":
        packages = words[1:]
        subprocess.run(["sudo"] + packageManager + packages)
    elif words[0] == "CLONE":
        args = words[1:]
        subprocess.run(["git", "clone"] + args)
