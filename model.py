from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_id = "mistralai/Mistral-7B-Instruct-v0.2"
tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=model_id, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    pretrained_model_name_or_path=model_id,
    torch_dtype=torch.bfloat16, # loads model in 16bit
    device_map="auto", # checks if cpu or gpu is avaiable to load model on
    trust_remote_code=True
)