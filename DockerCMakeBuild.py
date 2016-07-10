from . import dockerutils
import sublime, sublime_plugin
import os

# Build Project using CMake
# 1. rm -rf build
# 2. mkdir build
# 3. cd build
# 4. cmake ..
# 5. make

class DockerCmakeBuildCommand(sublime_plugin.WindowCommand):

    type = "RUN"
    docker_image = "ubuntu-devenv"
    docker_image_tag = "latest" # Value seems to be unused?
    docker_image_exe = "cmake"

    def run(self, type="RUN", docker_image="ubuntu-devenv", docker_image_tag="latest", docker_image_exe="cmake", file_regex='UNSET'):
        self.type = type
        self.docker_image = docker_image
        self.docker_image_tag = docker_image_tag
        self.docker_image_exe = docker_image_exe
        self.file_regex = file_regex
        self.file_name = dockerutils.getFileName()
        self.file_dir = dockerutils.getFileDir()


        if not dockerutils.isDockerInstalled():
            dockerutils.isNotInstalledMessage()
        elif not dockerutils.isDockerRunning():
            dockerutils.isNotRunningMessage()
        elif dockerutils.isUnsupportedFileType(self.file_name):
            sublime.status_message("Cannot " + type.lower() + " an unsupported file type")
        else:
            sublime.status_message("Start to execute CMake in Docker.")
            self.executeFile()


    def executeFile(self):
        if self.type == "RUN":
            opt_volume =  " -v \"" + self.file_dir+"/\":/src"
            opt_temporary = " -t"
            image = " " + self.docker_image + ":" + self.docker_image_tag
            docker_cmd = dockerutils.getCommand()
            build_cmd = self.generateBuildCmd()
            command = [docker_cmd + " run" + opt_volume + opt_temporary + ' ' + dockerutils.opt_cleanup + image + build_cmd]
            dockerutils.logDockerCommand(command)
        else:
            self.errorMessage("Unknown command: " + self.type)
            return

        dockerutils.getView().window().run_command("exec", { 'kill': True })
        dockerutils.getView().window().run_command("exec", {
            'shell': True,
            'cmd': command,
            'working_dir' : self.file_dir,
            'file_regex'  : self.file_regex
        })


    def generateBuildCmd(self):
        cpp_check_list = ["gcc", "g++", "cpp", "c++"]
        exec_cmd = ""
        if any(map(lambda x: x in self.docker_image or x in self.docker_image_exe, cpp_check_list)):
            exec_cmd = "./a.out;"
        build_cmd =  " " + self.docker_image_exe + " \"/src/" + self.file_name + "\"; "
        build_cmd = " bash -c 'cd /src; " + build_cmd + exec_cmd + "'"
        return build_cmd
