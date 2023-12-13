python3 LLMRepair validate \
    --dataset 395subset \
    --output-dir training-data/395-dataset/bugs-data \
    --use-supported \
    --envs-dir ~/Desktop/bgp_envs_local \
    --include-projects black \
    --timeout 30 \
    --overwrite \
    --partitions 8
