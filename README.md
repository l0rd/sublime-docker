SublimeDocker
=============

A Sublime Text package that include some build systems that use [Docker Language Stacks](http://blog.docker.com/2014/09/docker-hub-official-repos-announcing-language-stacks/). It currently builds python (2.7, 3.4, or with the Tensorflow library), ruby, perl, c/c++ (gcc), clojure, go (golang), java, R, Dockerfile and Fig configuration files.

# Prerequisite

Requires Docker. You can get it here https://get.docker.com/.

Your user [should belong to the Docker group](https://docs.docker.com/installation/ubuntulinux/#giving-non-root-access) to run docker without using `sudo`.

# Installation

Install using [SublimeText PackageControl](http://wbond.net/sublime_packages/package_control). Otherwise you can also Download/Clone the package and put it in your Packages-directory.

# Usage

After installing, you will find new options in `Tools > Build system` of your Sublime menu:

- C++ in Docker Container
- Clojure in Docker Container
- Dockerfile
- Fig
- Go in Docker Container
- Java in Docker Container
- Perl in Docker Container
- Python in Docker Container
- Ruby in Docker Container
- R in Docker Container

### Build and run using Docker containers 

![Build System Menu](images/BuildSystems_SubMenu.png "Build System Menu")

Remember, you can always launch the selected build with `Control+B` (Linux/Windows) or `Command+B` (OS X).

### Select different versions

You can select specific interpreter/compiler variants with  `Control+Shift+P` (Linux/Windows) or `Command+Shift+P` (OS X)
and typing build to reduce the selection to the available build variants for the selected build system as shown below for various language build systems.
![Build Variants](images/GO_Menu_BuildSelection_Variants.png "Build Variants")
![Build Variants](images/Java_Menu_BuildSelection_Variants.png "Build Variants")

### Dockerfile: build images and run containers with a dockerfile
![Build Variants](images/Dockerfile_Menu_BuildSelection_Variants.png "Build Variants")

### Fig: Run multiple containers using fig.yml file  
![Build Variants](images/Fig_Menu_BuildSelection_Variants.png "Build Variants")
