# app.py

# Imports
import streamlit as st
import io
from PIL import Image
from pdf2image import convert_from_bytes
import os
from transformers import DonutProcessor, VisionEncoderDecoderModel
import torch
import base64
import pandas as pd
import json

# Load the processor and model
processor = DonutProcessor.from_pretrained("onlas/donut_1440x1920_5e-6_mlength_768_base_v1")
model = VisionEncoderDecoderModel.from_pretrained("onlas/donut_1440x1920_5e-6_mlength_768_base_v1")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def demo_process(input_content, file_type):
    # Check if the uploaded file is a PDF
    if file_type == "application/pdf":
        # Convert only the first page of the PDF to an image
        images = convert_from_bytes(input_content, first_page=1, last_page=1)
        if not images:
            return {"error": "Failed to convert PDF to image."}, None
        input_img = images[0]
    else:
        input_img = Image.open(io.BytesIO(input_content))

    # Convert uploaded image to the format expected by the processor
    pixel_values = processor(input_img, return_tensors="pt").pixel_values

    task_prompt = "<s_cord-v2>"
    decoder_input_ids = processor.tokenizer(task_prompt, add_special_tokens=False, return_tensors="pt")["input_ids"]

    outputs = model.generate(pixel_values.to(device),
                             decoder_input_ids=decoder_input_ids.to(device),
                             max_length=model.decoder.config.max_position_embeddings,
                             early_stopping=True,
                             pad_token_id=processor.tokenizer.pad_token_id,
                             eos_token_id=processor.tokenizer.eos_token_id,
                             use_cache=True,
                             num_beams=1,
                             bad_words_ids=[[processor.tokenizer.unk_token_id]],
                             return_dict_in_generate=True,
                             output_scores=True)

    sequence = processor.batch_decode(outputs.sequences)[0]

    # Check if the sequence is empty or None
    if not sequence:
        return {"error": "Model returned an empty or None sequence."}, None

    # Try to convert the sequence to JSON format
    try:
        json_output = processor.token2json(sequence)
    except Exception as e:
        return {"error": f"Failed to convert to JSON: {str(e)}"}, None

    return json_output, input_img


def format_output(json_output):
    """Format the JSON output to be displayed in a more readable format."""
    formatted_output = ""
    for key, value in json_output.items():
        formatted_output += f"{key.replace('_', ' ').capitalize()}: {value}\n"
    return formatted_output


# Streamlit UI
st.title("Donut Model Inference")

uploaded_file = st.file_uploader("Choose an image or PDF file", type=["jpg", "png", "pdf"])

if uploaded_file:
    # Read file content
    file_content = uploaded_file.getvalue()
    
    # Process the content and get the model's output
    with st.spinner('Processing...'):
        output, display_img = demo_process(file_content, uploaded_file.type)

    # If there's an image to display, display it
    if display_img:
        st.image(display_img, caption="Uploaded Image", use_column_width=True)

    # Include the filename in the output
    output['file_name'] = uploaded_file.name

    # Display the formatted output
    st.text(format_output(output))

    # Download buttons
    st.write("**Download Results**")

    # JSON download button
    if st.button('Download JSON'):
        b64 = base64.b64encode(json.dumps(output).encode()).decode()
        st.markdown(f'<a href="data:file/json;base64,{b64}" download="{uploaded_file.name}.json">Click here to download as JSON</a>', unsafe_allow_html=True)

    # Excel download button
    if st.button('Download Excel'):
        df = pd.DataFrame([output])
        towrite = io.BytesIO()
        downloaded_file = df.to_excel(towrite, index=False, header=True)  # Removed 'encoding'
        towrite.seek(0)
        b64 = base64.b64encode(towrite.read()).decode()
        st.markdown(f'<a href="data:file/excel;base64,{b64}" download="{uploaded_file.name}.xlsx">Click here to download as Excel</a>', unsafe_allow_html=True)
