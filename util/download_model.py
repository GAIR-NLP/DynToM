from huggingface_hub import snapshot_download

HF_TOKEN = "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"
snapshot_download(repo_id="01-ai/Yi-1.5-9B-Chat-16K",local_dir = "/data/xiaoyang/models/01-ai/01-ai/Yi-1.5-9B-Chat-16K",token=HF_TOKEN)