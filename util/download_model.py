
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

from huggingface_hub import snapshot_download

HF_TOKEN = "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"

repo="meta-llama/Meta-Llama-3.1-70B-Instruct"
snapshot_download(repo_id=repo,local_dir = f"/data/yxiao2/models/{repo}",token=HF_TOKEN,endpoint="https://hf-mirror.com",max_workers=128,resume_download=True)