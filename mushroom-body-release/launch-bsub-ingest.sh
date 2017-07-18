if [[ $1 == "" ]]; then
    1>&2 echo "Usage: $0 <num-workers> <arbitrary-identifier>"
    exit 1
fi

if [[ $2 == "" ]]; then
    1>&2 echo "Usage: $0 <num-workers> <arbitrary-identifier>"
    exit 1
fi
THIS_SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

JANELIA_LSF_DIR=/groups/flyem/proj/cluster/miniconda/envs/flyem/DVIDServicesServer/SparkLaunch/janelia_lsf
LSF_SUBMIT_SCRIPT=${JANELIA_LSF_DIR}/sparklaunch_janelia_lsf

${LSF_SUBMIT_SCRIPT} $1 \
    --driver-slots=16 \
    --job-log-dir=${THIS_SCRIPT_DIR}/bjob-logs \
    Ingest3DVolume \
    ingest-to-buckets-$2 \
    ${THIS_SCRIPT_DIR}/ingest-to-buckets.json \
    /groups/flyem/proj/cluster/miniconda/envs/flyem/DVIDSparkServices/workflows/launchworkflow.py \
    /groups/flyem/proj/cluster/miniconda/envs/flyem/bin/python \
##
