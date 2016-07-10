import sublime
import os, re, subprocess
import time, shutil
import os.path

opt_cleanup = '--rm'

# Used by logDockerCommand(command) below:
#SUBLIME_DOCKER_LOGFILE='/tmp/sublime-docker.log'
SUBLIME_DOCKER_LOGFILE=None

DOCKER_NOT_INSTALLED_LINUX_MSG='''Docker is not installed.

Install it to use SublimeDocker: open a Terminal and run
    'curl -sSL https://get.docker.com/ | sh'
'''

DOCKER_NOT_INSTALLED_OSX_MSG='''Docker is not installed.

Install it to use SublimeDocker. Visit the following URL for installation instructions:

    https://docs.docker.com/en/latest/installation/
'''

DOCKER_NOT_RUNNING_LINUX_MSG='''Docker engine is not running.

Start it to use SublimeDocker.
'''
DOCKER_NOT_RUNNING_OSX_MSG='''Docker engine is not running.

Start it to use SublimeDocker: open a Terminal and run 'docker-machine start $(docker-machine active)' or 'boot2docker up'
'''

def isDockerInstalled():
    platform = sublime.platform()
    if platform == 'linux':
        return isDockerInstalledOnLinux()
    if platform == 'osx':
        return isDockerInstalledOnOSX()

def isDockerRunning():
    platform = sublime.platform()
    if platform == 'linux':
        return isDockerRunningOnLinux()
    if platform == 'osx':
        return isDockerRunningOnOSX()

def isDockerRunningOnLinux():
    """ Check is Docker daemon is running:
          We assume that the path to the daemon which appears in full ps output
          is of the form */bin/docker
    """
    if len(os.popen("ps -aef | grep '/bin/docker ' | grep -v grep").read().strip()) > 0:
        return True
    if len(os.popen("ps -aef | grep '/bin/docker.io ' | grep -v grep").read().strip()) > 0:
        return True
    return False

def isDockerRunningOnOSX():
    return (
        (os.path.isfile('/usr/local/bin/boot2docker')
            and isBoot2DockerRunning()) or
        (os.path.isfile('/usr/local/bin/docker-machine')
            and isDockerMachineRunning()) or
        (os.path.isfile('/usr/local/bin/docker')
            and isDockerNativeRunning()))


def isBoot2DockerRunning():
    if len(os.popen("ps -aef | grep 'boot2docker' | grep -v grep").read().strip()) < 1:
        return False
    try:
        os.environ["DOCKER_HOST"]
        os.environ["DOCKER_CERT_PATH"]
        os.environ["DOCKER_TLS_VERIFY"]
    except KeyError:
        boot2docker_init_cmd = subprocess.check_output(["/usr/local/bin/boot2docker", "shellinit"], stderr=None).strip()
        env = dict(re.findall(r'(\S+)=(".*?"|\S+)', boot2docker_init_cmd.decode()))
        for key,value in env.items():
            os.environ[key]=value
    return True

def isDockerMachineRunning():
    machine_ls = os.popen("/usr/local/bin/docker-machine ls -q").read().strip()
    if len(machine_ls) < 1:
        return False
    try:
        os.environ["DOCKER_HOST"]
        os.environ["DOCKER_CERT_PATH"]
        os.environ["DOCKER_TLS_VERIFY"]
        os.environ["DOCKER_MACHINE_NAME"]
    except KeyError:
        setEnvVariables()
    return True

def isDockerNativeRunning():
    docker_ping = "curl --unix-socket /var/run/docker.sock http://localhost/_ping"
    status = os.popen(docker_ping).read().strip()
    if (status == "OK"):
        return True
    return False

def isDockerInstalledOnLinux():
    if shutil.which('docker') != None :
        return True
    return False

def isDockerInstalledOnOSX():

    if not os.path.isfile('/usr/local/bin/docker'):
        print("which(docker) returned None")
        return False
    if not os.path.isfile('/usr/local/bin/boot2docker') and not os.path.isfile('/usr/local/bin/docker-machine'):
        print("which(boot2docker and docker-machine) returned None")
        return False
    return True

def isNotRunningMessage():
    platform = sublime.platform()
    if platform == 'linux':
        isNotRunningMessageLinux()
    if platform == 'osx':
        isNotRunningMessageOSX()

def isNotInstalledMessage():
    platform = sublime.platform()
    if platform == 'linux':
        isNotInstalledMessageLinux()
    if platform == 'osx':
        isNotInstalledMessageOSX()

def isNotInstalledMessageLinux():
    sublime.error_message(DOCKER_NOT_INSTALLED_LINUX_MSG)

def isNotInstalledMessageOSX():
    sublime.error_message(DOCKER_NOT_INSTALLED_OSX_MSG)

def isNotRunningMessageLinux():
    sublime.error_message(DOCKER_NOT_RUNNING_LINUX_MSG)

def isNotRunningMessageOSX():
    sublime.error_message(DOCKER_NOT_RUNNING_OSX_MSG)

def isUnsupportedFileType(file_name):
    return False

def getFileFullPath():
    win = sublime.active_window()
    if win:
        view = win.active_view()
        if view and view.file_name():
            return view.file_name()
    return ""

def getFileDir():
    filefullpath = getFileFullPath()
    dirname = os.path.dirname(filefullpath)
    if os.path.exists(dirname):
        return dirname
    else:
        return ""

def getFileName():
    filefullpath = getFileFullPath()
    return os.path.basename(filefullpath)

def getView():
    win = sublime.active_window()
    return win.active_view()

def getCommand():
    platform = sublime.platform()
    if platform == 'linux':
        return "docker"
    if platform == 'osx':
        return "/usr/local/bin/docker"

def logDockerCommand(command):
    if SUBLIME_DOCKER_LOGFILE != None:
        with open(SUBLIME_DOCKER_LOGFILE, 'a+') as f:
            f.write(time.strftime("\n%d/%m/%Y %H:%M:%S ") + str(command))
            f.close()

def setEnvVariables():
    env_out = run_machine_env()
    vars = dict(re.findall(r'(\S+)=(".*?"|\S+)', env_out))
    for key,value in vars.items():
        os.environ[key]=value.strip('"')

def run_machine_env():
    home_dir = os.path.expanduser('~')
    cmd = "/usr/local/bin/docker-machine -s " + home_dir + "/.docker/machine env default"
    return os.popen(cmd).read().strip()
