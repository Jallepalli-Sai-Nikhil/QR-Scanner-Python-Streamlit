import streamlit as st
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import tempfile
import os
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

st.title("📷 QR Code Scanner using Streamlit & OpenCV")

# File uploader for scanning QR codes from images
uploaded_file = st.file_uploader("Upload an image containing a QR Code", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name

    # Read the image
    image = cv2.imread(temp_path)
    qr_codes = decode(image)

    # Process detected QR codes
    if qr_codes:
        for qr in qr_codes:
            qr_data = qr.data.decode('utf-8')
            qr_rect = qr.rect

            # Draw rectangle around QR code
            cv2.rectangle(image, (qr_rect.left, qr_rect.top), 
                          (qr_rect.left + qr_rect.width, qr_rect.top + qr_rect.height), 
                          (0, 255, 0), 3)

            # Put QR data as text on the image
            cv2.putText(image, qr_data, (qr_rect.left, qr_rect.top - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        st.image(image, channels="BGR", caption="Processed QR Code Image")
        st.success(f"🔍 QR Code Data: {qr_data}")
    else:
        st.warning("No QR code detected in the uploaded image.")

    # Remove the temporary file
    os.remove(temp_path)

# Live Camera QR Code Scanner
st.subheader("📹 Live QR Code Scanner (Works on Mobile & Desktop)")

class QRCodeProcessor(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        qr_codes = decode(img)
        
        for qr in qr_codes:
            qr_data = qr.data.decode('utf-8')
            qr_rect = qr.rect
            
            # Draw rectangle around QR code
            cv2.rectangle(img, (qr_rect.left, qr_rect.top),
                          (qr_rect.left + qr_rect.width, qr_rect.top + qr_rect.height),
                          (0, 255, 0), 3)

            # Display QR data
            cv2.putText(img, qr_data, (qr_rect.left, qr_rect.top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
            
            st.success(f"🔍 QR Code Data: {qr_data}")
        
        return img

webrtc_streamer(key="qr-scanner", video_processor_factory=QRCodeProcessor)
