#To build an update
# use git to identify changed and new source files
# store them in a tree similar to that of the original
# send the 

# to update the app
# look for the apps path in the system_path
# replace the source files that have changed
# migrate the database
# restart the server

# must have a command line argument for the previous version

# each update build is assigned to a major release 
# each update builds up on the last released update
# major build changes cannot be updated
# changes to the requirements of the applications must prevent any update from #
# being performed, instead suggesting a new major release


import sys
import os 
import shutil
from distutils.dir_util import copy_tree
import time
import git 
from build_logger import create_logger
import json
import re
from util import repo_checks, run_tests
import subprocess
import datetime


MINOR = None
if len(sys.argv) == 2:
    MINOR = sys.argv[1] == '-m' 

#CONSTANTS
START = time.time()
BASE_DIR = os.path.dirname(os.getcwd())
REPO = git.Repo(BASE_DIR)
BUILD_COUNTER = None

logger = create_logger('update')

with open(os.path.join(BASE_DIR, 'build_counter.json'), 'r') as bc:
    BUILD_COUNTER  = json.load(bc)

if len(BUILD_COUNTER['major_releases']) == 0:
    raise Exception("No previous major release found. Build the application using the -M argument and then updates can be made to the release")

UPDATE_FROM = BUILD_COUNTER['major_releases'][-1]


# GLOBAL FUNCTIONS
def get_sha_from_version(counter, version):
    for build in counter['builds']:
        if build['version'] == version:
            return build['hash']


def get_specific_commit(repo, sha):
    for commit in repo.iter_commits():
        if commit.hexsha == sha:
            return commit

    return None

def search_differences(diffs, regex):
    results = []
    for diff in diffs:
        if re.search(regex, diff.b_path):
            results.append(diff.b_path)

    return results 

def increment_version(minor, build_counter):
    if minor:
        return "{}.{}.{}".format(
            build_counter['major'], 
            build_counter['minor'] + 1,
            0
        )

    else:
        return "{}.{}.{}".format(
            build_counter['major'],
            build_counter['minor'],
            build_counter['patch'] + 1
        )

        

def build_update():
    #check the current changes have been committed
    #repo_checks(REPO, logger)

    #run unit_tests
    os.chdir(BASE_DIR)
    #run_tests(logger)

    #collect static files
    result = subprocess.run(['python', 'manage.py', 'collectstatic', '--noinput'])
    if result.returncode != 0:
        logger.info("Failed to collect static files")
        raise Exception("The static files collection process failed")

    # get diffs between current version and supplied argument version
    commit = get_specific_commit(REPO, UPDATE_FROM['hash'])
    diffs = REPO.head.commit.diff(UPDATE_FROM['hash'])
    
    if len(list(diffs)) == 0:
        raise Exception('There are no changes between the last build and the current app')

    # analyse differences to make changes on differences
    
    # seach for changes to the requirements.txt
    requirements = search_differences(diffs, r'^requirements.txt$')
    if len(requirements) > 0:
        logger.critical("The applications dependancies have changed. Exiting")
        raise Exception("The dependencies for the application have changed."
        " Build a new release instead of an update to this version of the"
        " software")

    update_dir = os.path.join(BASE_DIR, 'dist', 'update', 'files')
    if not os.path.exists(update_dir):
        os.makedirs(update_dir)

    fail_counter = 0
    delete_list = open(os.path.join(
        os.path.dirname(update_dir), 'del_list.txt'), 'w')

    for d in [ i for i in diffs if 'build' not in i.b_path]:
        if d.change_type == "D":
            delete_list.write(d.b_path + '\n')
        else:
            pathname = d.b_path.replace("/", "\\")
            dest_dir = os.path.join(update_dir, os.path.dirname(pathname))
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            try:
                shutil.copy(os.path.join(BASE_DIR, pathname), dest_dir)
            except Exception as e:
                fail_counter += 1
                print(e)
                print(d.change_type)

    delete_list.close()


    if fail_counter > 0:
        logger.warning("{} files failed to copy".format(fail_counter))
        raise Exception('Some files failed to copy')

    # analyse fixtures, if changes exist, install the fixture (NB) except for 
    # chart of accounts accounts as this will reset account balances.


    #build update executable
    os.chdir(os.path.join(BASE_DIR, 'build'))
    results = subprocess.run(['pyinstaller', 'update.py', '--onefile'])
    if results.returncode != 0:
        raise Exception('Failed to build installer')

    shutil.copy(os.path.join('dist', 'update.exe'), 
        os.path.join(BASE_DIR, 'dist', 'update'))


    metadata = {
        'date': f'{datetime.date.today()}',
        'hash': REPO.head.commit.hexsha,
        'version': increment_version(MINOR, BUILD_COUNTER)
    }

    # TODO update build counter with major release updates

    with open('meta.json', 'w') as f:
        json.dump(metadata, f)
        
    shutil.copy('meta.json', os.path.join(BASE_DIR, 'dist', 'update'))
    os.remove('meta.json')
    os.chdir(BASE_DIR)


    print('Build completed succesfully in {:.2f} seconds.'.format(time.time() - START))


if __name__ == "__main__":
    build_update()

