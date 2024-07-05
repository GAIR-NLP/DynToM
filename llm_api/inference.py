from llm_api.model_chat import *

model_name_2_class = {
    "Meta-Llama-3-8B-Instruct": Llama38BInstruct,
    "Meta-Llama-3-70B-Instruct": Llama370BInstruct,
    "Mistral-7B-Instruct-v0.3": Mistra7BInstructV03,
    # "Mixtral-8x7B-Instruct-v0.1":Mistra87BInstructV01,
    "Qwen2-7B-Instruct":QWen27BInstruct,
    "Qwen2-72B-Instruct":QWen272BInstruct,
    "DeepSeek-V2-Lite-Chat":DeepSeekV2LiteChat
}


def run_inference(model_name):
    """run inference to get answers for the questions

    Args:
        model_name (_type_): _description_
    """
    chat_model = model_name_2_class[model_name]()
    response = chat_model.chat(
        "answer the question, and response in format '{question id}.{option id}, {question id}.{option id},...',such as '1.A, 2.B, 3.C,...'"
    )
    # for 
    print(response[0]["generated_text"][-1]["content"])


if __name__ == "__main__":
    run_inference("DeepSeek-V2-Lite-Chat")
