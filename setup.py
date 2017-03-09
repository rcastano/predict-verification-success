import os.path
import subprocess
import sys

def _script_path():
    return os.path.dirname(os.path.realpath(__file__))

# TODO(rcastano): replace git methods with an actual git API in python
# git remote get-url origin
def check_git_remote(dir, expected_url):
    output = subprocess.check_output(
        'git remote get-url origin'.split(),
        cwd=dir)
    return url in output
    
def check_git_commit(dir, expected_commit):
    output = subprocess.check_output(
        'git rev-parse HEAD'.split(),
        cwd=dir)
    return commit in output

external_dirs = 'external'
def check_repo_status(expected_dir, expected_url, expected_commit):
    expected_dir = get_external_dir_path(expected_dir)
    check_git_remote(expected_dir, expected_url)

    check_git_commit(expected_dir, expected_commit)

def get_external_dir_path(dir):
    return os.path.join(_script_path(), '/../', external_dirs, dir)


def setup_repo(dir, url, commit):
    dir = get_external_dir_path(dir)
    command = 'git clone'.split()
    command.append(url)
    command.append(dir)
    if os.path.exists(dir):
        raise Exception('Directory for repository already exists.')
    try:
        subprocess.check_call(
            command,
            cwd=dir)
    except Exception as e:
        print >> sys.stderr, 'Failed to clone repository'
        raise e

    command = 'git checkout'.split()
    command.append(commit)
    try:
        subprocess.check_call(
            command,
            cwd=dir)
    except Exception as e:
        print >> sys.stderr, 'Failed to checkout specified commit'
        raise e

def main(args):
    expected_svcomp_dir = 'sv-benchmarks'
    expected_svcomp_url = 'https://github.com/sosy-lab/sv-benchmarks/'
    expected_svcomp_commit = 'c5b6508fb8580ee6e82db94dae4c52db90a98f8b'

    expected_cpachecker_dir = 'cpachecker'
    expected_cpachecker_url = 'https://github.com/sosy-lab/cpachecker/'
    expected_cpachecker_commit = 'addf52135c4f7e83cb5431f828a968f1b85a81f6'
    if args.setup_repos:
        setup_repo(
            dir = expected_svcomp_dir,
            url = expected_svcomp_url,
            commit = expected_svcomp_commit)

        setup_repo(
            dir = expected_cpachecker_dir,
            url = expected_cpachecker_url,
            commit = expected_cpachecker_commit)
    check_repo_status(
        expected_dir=expected_cpachecker_dir,
        expected_url=expected_cpachecker_url,
        expected_commit=expected_cpachecker_commit)
    check_repo_status(
        expected_dir=expected_svcomp_dir,
        expected_url=expected_svcomp_url,
        expected_commit=expected_svcomp_commit)

    