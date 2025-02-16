from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load gemini model
model=genai.GenerativeModel('gemini-2.0-flash')

def get_gemini_response(input_prompt,image):
    response=model.generate_content([input_prompt,image[0]])
    return response.text

def input_image_details(uploaded_file): ##Check if a file has been uploaded
    if uploaded_file is not None:
        #Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file Uploaded")
    

##Streamlit app
st.set_page_config(page_title="Gemini Health App")

st.header("Gemini Health")
uploaded_file = st.file_uploader("Choose an image...",type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image", use_container_width=True)

submit=st.button("Tell me about Calories")

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
                and calculate the total calories, also provide the details of
                every food items with calories intake
                in below format

                1. Item 1 - Number of calories, Healthy or Unhealthy
                2. Item 2 - Number of calories, Healthy or Unhealthy
                ------
                ------
            Finally you can also mention the overall food is healthy or not and also
            mention the
            precentage split of the ratio of carbohydrates,fats,fibres,sugar,protien and
            thing required in human diet

        You can also answer to the questions regarding the person physique goal he/she has to acheive and recommend
        some diet information regarding theri goal.
"""
if submit:

##if submit is clicked
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data)
    st.subheader("The Response is")
    st.write(response)