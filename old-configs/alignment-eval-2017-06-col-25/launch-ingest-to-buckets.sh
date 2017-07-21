if [[ $1 == "" ]]; then
    1>&2 echo "Usage: $0 <num-workers> <arbitrary-identifier>"
    exit 1
fi

if [[ $2 == "" ]]; then
    1>&2 echo "Usage: $0 <num-workers> <arbitrary-identifier>"
    exit 1
fi
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd /groups/flyem/proj/cluster/miniconda/envs/flyem/DVIDServicesServer/SparkLaunch/janelia_sge

source sparkenv.sh

./sparklaunch_janelia $1 \
    Ingest3DVolume \
    ingest-to-buckets-$2 \
    ${SCRIPT_DIR}/ingest-to-buckets.json \
    /groups/flyem/proj/cluster/miniconda/envs/flyem/DVIDSparkServices/workflows/launchworkflow.py \
    /groups/flyem/proj/cluster/miniconda/envs/flyem/bin/python \
##
