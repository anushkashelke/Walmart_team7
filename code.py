pip install pyzbar pillow
!apt install libzbar0
!pip install -q streamlit
pip install pytesseract pillow
!sudo apt-get install tesseract-ocr
!sudo apt-get install libtesseract-dev
!sudo apt-get install tesseract-ocr-eng

%%writefile app.py

import streamlit as st
import pandas as pd
from PIL import Image
from pyzbar.pyzbar import decode
import numpy as np
import cv2
import pytesseract


def retrieve_numeric_text_from_image(img,barcode):


    gray_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    result=""
    # Apply image preprocessing (optional but can improve OCR accuracy)
    processed_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    processed_image = cv2.threshold(processed_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Perform OCR on the processed image using pytesseract
    extracted_text = pytesseract.image_to_string(processed_image)

    # Filter the extracted text to keep only numbers
    extracted_numbers = "".join(filter(str.isdigit, extracted_text))

    if(barcode==extracted_numbers):
      st.write(f"Extracted Barcode: {extracted_numbers}")
      result="yes"
    else:
      st.write(f" ")
      result="no"
    return result

# Function to decode the barcode and check if it exists in the 'barcode' column
def check_barcode_existence(uploaded_image, df):
    if uploaded_image is not None:
        # Open the image and decode the barcode
        img = Image.open(uploaded_image)
        decoded_objects = decode(img)

        if decoded_objects:
            barcode_data = decoded_objects[0].data.decode('utf-8')
            st.write(f"Decoded Barcode: {barcode_data}")
            df['barcode'] = df['barcode'].astype(str).str.replace(',', '')

            # Check if the barcode_data exists in the 'barcode' column of the DataFrame
            if barcode_data in df['barcode'].values:
                st.write("Barcode exists in the dataset.")
            else:
                st.write("Barcode not found in the dataset.")
        else:
            st.write("No barcode found in the uploaded image.")

# Main Streamlit app code
def main():

    st.title("BARCODE DETECTOR")

    # Read the dataset (e.g., an XLSX file) into a DataFrame
    # Replace 'path/to/your/dataset.xlsx' with the actual file path of your dataset
    dataset_file_path = '/content/barcode_data (1) (2).xlsx'
    df = pd.read_excel(dataset_file_path)

    # File uploader widget
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    # Check if a file is uploaded
    if uploaded_file is not None:
        # Display the image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        image = Image.open(uploaded_file)
        img_array = np.array(image)
        decoded_objects = decode(image)
        barcode = decoded_objects[0].data.decode('utf-8')
        # Convert the image bytes to a NumPy array
        ans=retrieve_numeric_text_from_image(img_array,barcode)
        # Call the check_barcode_existence function with the uploaded image and DataFrame as arguments
        check_barcode_existence(uploaded_file, df)

        if(ans=="yes"):
          st.write(f"The barcode generated from above image matches with the barcode value below the barcode")

if __name__ == "__main__":
    main()


!npm install localtunnel
!streamlit run app.py &>/content/logs.txt & curl ipv4.icanhazip.com
!npx localtunnel --port 8501
