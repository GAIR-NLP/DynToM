from huggingface_hub import snapshot_download

HF_TOKEN = "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"
snapshot_download(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",local_dir = "/data/xiaoyang/models/mistralai/Mixtral-8x7B-Instruct-v0.1",token=HF_TOKEN)