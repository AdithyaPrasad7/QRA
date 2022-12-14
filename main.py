import qrcode
import streamlit as st
import os
import numpy as np
import time
from PIL import Image
import cv2
import PIL.Image as Image
from io import BytesIO

qr=qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

def toggle_widget():
    if st.session_state.widget_disabled:
        st.session_state.widget_disabled = False
    else:
        st.session_state.widget_disabled = True  

if 'widget_disabled' not in st.session_state:
    st.session_state.widget_disabled = True

def dynamic_cam(img_file_buffer):
    detector=cv2.QRCodeDetector()
    imqg=Image.open(file_name)
    img=np.asarray(imqg)
    data,bbox,_=detector.detectAndDecode(img)
    if data:
        return data
    else:
        return "Error scan again!"

def qr_code_generator(s,colour1,colour2):
    
    qr.add_data(s)
    qr.make(fit=True)

    img=qr.make_image(fill_color=colour1, back_color=colour2)
    path=os.getcwd()
    current_time=time.strftime("%H-%M-%S")
    file_name='qr_image_'+current_time+'_.png'
    save_img=os.path.join(path,file_name)
    img.save(save_img)
    return save_img

def decode_qr_code(image):
    image_bytes=np.asarray(bytearray(image.read()),dtype=np.uint8)
    open_image=cv2.imdecode(image_bytes,1)
    decoder=cv2.QRCodeDetector() 
    data,vertices_array,binary_qrcode=decoder.detectAndDecode(open_image)
    if vertices_array is not None:
        return data
    else:
        return "There was some error"

st.set_page_config(layout='wide')
st.markdown("<h1 style='text-align: center; color: red;'>Welcome to QR code Generator</h1>", unsafe_allow_html=True)

page1,page2,page3=st.tabs(["Generate QR Code","Decode QR Code","Scan"])

with page1:
    with st.form(key="encode"):
        data=st.text_area('Enter the data:-')
        st.text(data)

        t1,t2=st.columns(2)

        with t1:
            colour1=st.color_picker('Pick A Painting  Colour',key="fill_colour",value='#000000')
            st.write('Preferred colour:-Black  #000000')
            st.write('Ensure Painting Colour to be Dark Colour compared to Background  Colour')

        with t2:
            colour2=st.color_picker('Pick A Background Colour',key="back_colour",value='#FFFFFF')
            st.write('Preferred colour:-White  #FFFFFF')
            st.write('Ensure Background Colour to be Light Colour compared to Painting  Colour')
        
        submit=st.form_submit_button("Generate  QR Code")

    if submit:
        img_path=qr_code_generator(data,colour1,colour2)
        img=Image.open(img_path)

        with open(img_path,"rb") as file:
            dwn=st.download_button(
                label="Download Image",
                data=file,
                file_name=img_path,
                mime="image/png"
            )

        st.image(img)
        

with page2:
     with st.form(key="decode"):
        img=st.file_uploader("Upload QR Code",type=['jpeg','jpg','png'])
        #st.image(path)
        submit=st.form_submit_button("Decode the Image")
        
        if submit:
            text=decode_qr_code(img)
            p1,p2=st.columns(2)

            with p1:
                st.image(img)

            with p2:
                st.info("Decoded Text from Image is:-")
                st.text(text)

with page3:
    st.button('Scan',on_click=toggle_widget)
    img_file_buffer=st.camera_input("Scan the QR Code",disabled=st.session_state.widget_disabled,key =7)

    current_time=time.strftime("%H-%M-%S")
    file_name='qr_code_'+current_time+'_.png'

    if img_file_buffer is not None:
        bytes_data=img_file_buffer.getvalue()
        stream=BytesIO(bytes_data)
        image=Image.open(stream).convert("RGBA")
        stream.close()
        im1=image.save(file_name)

        s=dynamic_cam(file_name)
        t3,t4=st.columns(2)

        with t3:
            st.image(file_name)
        with t4:
            if s is not None:
                st.info(s)


