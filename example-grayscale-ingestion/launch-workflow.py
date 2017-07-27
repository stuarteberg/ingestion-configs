#!/usr/bin/env python

from __future__ import print_function
import os
from os.path import dirname, basename, splitext, abspath
import sys
import shutil
import subprocess
import argparse
import json
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
    parser.add_argument('--max-hours', type=int, default=24, help='The maximum runtime length before LSF auto-kills the job')
    parser.add_argument('workflow_type')
    parser.add_argument('config_file')
    args = parser.parse_args()

    num_workers = args.num_workers
    driver_slots = args.driver_slots
    max_hours = args.max_hours
    workflow_type = args.workflow_type

    config_name = splitext(basename(args.config_file))[0]
    timestamp = '{:%Y%m%d.%H%M%S}'.format(datetime.now())
    job_name = config_name + '-' + timestamp

    # Make a subdirectory for this job
    mkdir_p(job_name)

    # Copy the config file to the new directory
    shutil.copy(args.config_file, job_name)
    config_file_copy = abspath(os.path.join(job_name, basename(args.config_file)))

    bjob_log_dir = job_name + "/bjob-logs"
    mkdir_p(bjob_log_dir)

    config_data = json.load(open(config_file_copy, 'r'))
    try:
        task_log_dir = config_data["options"]["log-collector-directory"]
    except KeyError:
        pass
    else:
        mkdir_p(job_name + "/" + task_log_dir)

    # We copy the worker-dvid initialization script and toml,
    # but only if they exist in this HARD-CODED location.
    if os.path.exists('worker-dvid-files'):
        job_worker_dvid_files = job_name + '/worker-dvid-files'
        mkdir_p(job_worker_dvid_files)
        mkdir_p(job_worker_dvid_files + '/worker-dvid-logs')
        mkdir_p(job_worker_dvid_files + '/worker-dvid-tomls')
        shutil.copy('worker-dvid-files/launch-worker-dvid.sh', job_worker_dvid_files)
        shutil.copy('worker-dvid-files/worker-dvid-config.toml', job_worker_dvid_files)

    vars = {}
    vars.update(locals())
    vars.update(globals())

    cmd = '{LSF_SUBMIT_SCRIPT} \
             --driver-slots={driver_slots} \
             --job-log-dir={bjob_log_dir} \
             --max-hours={max_hours} \
             {num_workers} \
             {workflow_type} \
             {config_file_copy}'.format(**vars)
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
