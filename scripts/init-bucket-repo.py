import os
import sys
import time
import argparse
import subprocess
import DVIDSparkServices

DVID_CONSOLE = '/groups/flyem/proj/cluster/miniconda/envs/flyem/diced/diced/dvid-console/dist-lite.html'
BUCKET_NAME = 'flyem-alignment-quick-eval'
LOG_DIR = '/groups/flyem/data/scratchspace/ingestion-configs/scripts/logs'

GOOGLE_APPLICATION_CREDENTIALS='/groups/flyem/home/bergs/.cloud-keys/dvid-em-28a78d822e11.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_APPLICATION_CREDENTIALS

TOML_TEXT = """
[server]
httpAddress = ":8000"
rpcAddress = ":8001"
webClient = "{DVID_CONSOLE}"
instance_id_gen = "sequential"
instance_id_start = 100  # new ids start at least from this.

note = \"""
{{"source": "gs://{BUCKET_NAME}"}}
\"""

[logging]
logfile = "{LOG_DIR}/{BUCKET_NAME}.log"
max_log_size = 500 # MB
max_log_age = 30   # days
[store]
    [store.mutable]
        engine = "gbucket"
        bucket= "{BUCKET_NAME}"
""".format(**globals())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('new_repo_name')
    parser.add_argument('new_repo_description')
    args = parser.parse_args()

    toml_path = '{BUCKET_NAME}.toml'.format(**globals())
    with open(toml_path, 'w') as f_toml:
        f_toml.write(TOML_TEXT)
    
    print "Wrote {}".format(toml_path)
    
    cmd = 'dvid -verbose serve {toml_path}'.format(toml_path=toml_path)
    print cmd
    subprocess.Popen(cmd, shell=True)
    
    # Wait 3 seconds for DVID to start up...
    time.sleep(3.0)

    cmd = 'dvid repos new "{}" "{}"'.format(args.new_repo_name, args.new_repo_description)
    response = subprocess.check_output(cmd, shell=True).strip()
    print response
    repo_uuid = response.split()[-1]    

if __name__ == "__main__":
    sys.exit( main() )
