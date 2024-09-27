from transformers import pipeline

summarizer = pipeline("summarization", model="Falconsai/text_summarization")
