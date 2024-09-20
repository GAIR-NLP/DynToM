from huggingface_hub import snapshot_download

HF_TOKEN = "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"
snapshot_download(repo_id="deepseek-ai/DeepSeek-V2-Lite-Chat",local_dir = "/home/share/models/DeepSeek-V2-Lite-Chat",token=HF_TOKEN)