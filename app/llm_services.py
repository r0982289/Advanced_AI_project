from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import streamlit as st

@st.cache_resource
def load_translation_model():
    model_name = "t5-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    return tokenizer, model

def translate_text(text, target_language):
    tokenizer, model = load_translation_model()
    prompt = f"Translate English to {target_language}: {text}"
    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs.input_ids, max_length=512)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
