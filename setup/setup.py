def identify_operating_system():
    # identify the operating system
    import platform
    operating_system = platform.system()
    print(f'Operating system: {operating_system}')
    return operating_system


def idnetify_shell(platform:str):
    # identify the shell environment:
    # e.g. bash and zsh - for Linux and Mac
    # or cmd and powershell - for Windows
    import os
    if (platform == 'Linux') | (platform == 'Darwin'):
        shell = os.environ["SHELL"]
    elif platform == 'Windows':
        shell = os.environ["COMSPEC"]
    print(f'Shell: {shell}')
    return shell


def identify_python_executable():
    # identify the filename of the Python interperater running this script.
    import sys
    executable = sys.executable
    print(f'The python executable file is: {executable}')
    if (executable.endswith('python')) | (executable.endswith('python.exe')):
        executable = 'python'
    elif (executable.endswith('python3')) | (executable.endswith('python3.exe')):
        exectuable = 'python3'
    else:
        raise ValueError(f"executable is {executable} and it doesn't end with neither 'python', 'python.exe', 'python3', nor 'python3.exe'. "
              "To support this executable, update this script"
              )
    return executable

def validate_python_version():
    # check that python version is the recommended one, i.e.: 3.7.x-3.10.x
    import sys
    if (sys.version_info >= (3, 7)) | (sys.version_info < (3, 11)):
        print(
            f'Python version {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} is installed. '
            '(the recommended version for this repository is 3.7.x-3.10.x)'
            )
    else:
        sys.exit(
            f'The Python version installed is: {sys.version_info.major}.{sys.version_info.minor}, and is not supported. '
            'Please install the recommended version of Python and try again. '
            'See: https://www.python.org/downloads/'
            )


def is_git_installed():
    # check that Git is installed
    import subprocess
    try:
        output = subprocess.run(['git', '--version'], check=True, stdout=subprocess.PIPE)
        output = output.stdout.decode('ascii').replace('\n','')
        print(f'Git is installed (version: {output})')
    except subprocess.CalledProcessError:
        raise ValueError(
            'Git is not installed. Please install Git and rerun this script.'
            'To install, see: https://git-scm.com/downloads'
            )


def is_pip_installed():
    # check if pip is installed
    try:
        import pip
        print(f'pip is installed (version: {pip.__version__})')
    except ImportError:
        raise ImportError('pip is not installed. Please install pip and run this script again')

def is_ensurepip_installed():
    # check if ensurepip is installed
    try:
        import ensurepip
        print(f'ensurepip is installed (version: {ensurepip.version()})')
    except ImportError:
        raise ImportError('ensurepip is not installed. Please install ensurepip and run this script again')


def create_venv(venv_path:str, platform:str, shell:str, executable:str):
    # create a virtual environment
    import os
    import subprocess
    import sys
    if os.path.exists(venv_path):
        print(
            f'{venv_path} - Virtual environment folder already exists. '
            'Skipping venv creation. '
            'If you want to recreate the venv, delete the folder and run this script again.'
            )
        return
    print(f'{venv_path} - Creating virtual environment...')
    subprocess.run(f'{executable} -m venv {venv_path}', shell=True)
    print(f'{venv_path} - Virtual environment created')


def install_packages(venv_path:str, requirements_path:str, platform:str, shell:str, executable:str):
    # install packages from requirements.txt
    import os
    import subprocess
    import sys
    print(f'{venv_path} - Installing packages...')
    if (platform == 'Linux') | (platform == 'Darwin'):
        subprocess.run(f'{venv_path}/bin/pip install -r {requirements_path}', shell=True)
    elif platform == 'Windows':
        subprocess.run(fr'{venv_path}\Scripts\pip install -r {requirements_path}', shell=True)
    print(f'{venv_path} - Packages installed')


def install_ipykernel(venv_path:str, venv_name:str, platform:str, shell:str, executable:str):
    # install ipykernel
    import os
    import subprocess
    import sys
    print(f'{venv_path} - Installing ipykernel...')
    if (platform == 'Linux') | (platform == 'Darwin'):
        subprocess.run(f'{venv_path}/bin/python -m ipykernel install --user --name={venv_name} --display-name={venv_name}', shell=True)
    elif platform == 'Windows':
        subprocess.run(fr'{venv_path}\Scripts\python -m ipykernel install --user --name={venv_name} --display-name={venv_name}', shell=True)
    print(f'{venv_path} - ipykernel installed')


def main():

    platform = identify_operating_system()
    shell = idnetify_shell(platform)
    validate_python_version()
    executable = identify_python_executable()
    is_git_installed()
    is_pip_installed()
    is_ensurepip_installed()
    venv_names = ['pytorch_cpu', 'tensorflow_cpu']
    if platform == 'Windows':
        venv_paths = [r'.\venv\\'+n for n in venv_names]
    elif (platform == 'Linux') | (platform == 'Darwin'):
        venv_paths = ['./venv/'+n for n in venv_names]
    requirements_paths = ['./setup/requirements_' + e + '.txt' for e in venv_names]
    for venv_path, requirements_path, venv_name in zip(venv_paths, requirements_paths, venv_names):
        create_venv(venv_path, platform, shell, executable)
        install_packages(venv_path, requirements_path, platform, shell, executable)
        install_ipykernel(venv_path, venv_name, platform, shell, executable)

if __name__ == '__main__':
    main()
