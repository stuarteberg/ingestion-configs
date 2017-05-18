if [[ $1 == "" ]]; then
    1>&2 echo "Usage: $0 <num-workers> <test-index>"
    exit 1
fi

if [[ $2 == "" ]]; then
    1>&2 echo "Usage: $0 <num-workers> <test-index>"
    exit 1
fi

cd /groups/flyem/proj/cluster/miniconda/envs/flyem/DVIDServicesServer/SparkLaunch/janelia_sge

source sparkenv.sh

./sparklaunch_janelia $1 \
    Ingest3DVolume \
    sec26-ingest-to-buckets-$2 \
    /groups/flyem/data/scratchspace/ingestion-configs/section-26-downsampled/ingest-mini-sec26-to-buckets.json \
    /groups/flyem/proj/cluster/miniconda/envs/flyem/DVIDSparkServices/workflows/launchworkflow.py \
    /groups/flyem/proj/cluster/miniconda/envs/flyem/bin/python \
##
