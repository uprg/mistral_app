from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import torch
import asyncio
from request_model import RequestBody

from model import model, tokenizer

app = FastAPI()

def non_stream_data(text):
    input_texts = tokenizer(text=text, return_tensors="pt") # return_tensor='pt' means return tensor in torch format

    with torch.no_grad():
        output = model.generate(**input_texts, max_new_tokens=2000)
        return tokenizer.decode(token_ids=output[0], skip_special_tokens=True)

async def stream_data(text):
    input_texts = tokenizer(text=text, return_tensors="pt") # return_tensor='pt' means return tensor in torch format

    with torch.no_grad():
        output = model.generate(**input_texts, max_new_tokens=2000)
        output_text = tokenizer.decode(token_ids=output[0], skip_special_tokens=True)

    start = 0
    end = 20
    step = 20

    while True:
        output_subset = output_text[start:end]

        start = end
        end = end + step

        if len(output_subset) == 0:
            break

        yield output_subset
        await asyncio.sleep(0.1)




@app.post("/generate")
async def generate_endpoint(request_body: RequestBody):
    requestbody = request_body.model_dump()
    question = requestbody["question"]
    streaming = requestbody["streaming"]

    if streaming == True:
        return StreamingResponse(content=stream_data(text=question))
    else:
        return non_stream_data(text=question)
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="app:app", host="localhost", port=5000, reload=True)
