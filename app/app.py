from fastapi import FastAPI
from transformers import BartTokenizer, BartForConditionalGeneration
from model import summarizer

app = FastAPI()


@app.post("/summarize/")
async def summarize_text(text: str):
    summary = summarizer(text, max_length=1000, min_length=30, do_sample=False)
    return {"summary": summary}