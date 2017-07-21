#!/usr/bin/env python

from __future__ import print_function
import os
import sys
import subprocess
import argparse
from datetime import datetime

FLYEM_ENV = '/groups/flyem/proj/cluster/miniconda/envs/flyem'
PYTHON_EXE = FLYEM_ENV + '/bin/python'
DSS_LAUNCH_WORKFLOW = FLYEM_ENV + '/DVIDSparkServices/workflows/launchworkflow.py'
JANELIA_LSF_DIR = FLYEM_ENV + '/DVIDServicesServer/SparkLaunch/janelia_lsf'
LSF_SUBMIT_SCRIPT = JANELIA_LSF_DIR + '/sparklaunch_janelia_lsf'
THIS_SCRIPT_DIR = os.path.split(__file__)[0]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--num-workers', '-n', type=int, default=1, help='How many worker nodes to use in the cluster (not inclduing the master)')
    parser.add_argument('--driver-slots', type=int, default=16, help='How many slots to use for the driver process.')
    parser.add_argument('--iteration-id', '-i', help='An arbitrary string that will be added to the bjob name. Default: a timestamp.')
    parser.add_argument('workflow_type')
    parser.add_argument('config_file')
    args = parser.parse_args()

    num_workers = args.num_workers
    driver_slots = args.driver_slots
    workflow_type = args.workflow_type
    job_name = os.path.splitext(os.path.basename(args.config_file))[0]
    config_file = os.path.abspath(args.config_file)
    iteration_id = args.iteration_id
    if not iteration_id:
        iteration_id = '{:%Y%m%d.%H%M%S}'.format(datetime.now())

    vars = {}
    vars.update(locals())
    vars.update(globals())

    mkdir_p("{}/bjob-logs".format(THIS_SCRIPT_DIR))

    cmd = '{LSF_SUBMIT_SCRIPT} \
             --driver-slots={driver_slots} \
             --job-log-dir={THIS_SCRIPT_DIR}/bjob-logs \
             {num_workers} \
             {workflow_type} \
             {job_name}-{iteration_id} \
             {config_file} \
             {DSS_LAUNCH_WORKFLOW} \
             {PYTHON_EXE}'.format(**vars)
    cmd = ' '.join(cmd.split())

    try:
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError as ex:
        print('\n\nError: Command:\n\n' + cmd + '\n\nExited with bad code: {}'.format(ex.returncode), file=sys.stderr)
        return ex.returncode

    return 0


def mkdir_p(path):
    """
    Like the bash command: mkdir -p
    
    ...why the heck isn't this built-in to the Python std library?
    """
    import os, errno
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


if __name__ == "__main__":
    sys.exit( main() )
