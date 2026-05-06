import argparse
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
load_dotenv()
from cad3dify import generate_step_from_2d_cad_image

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_type", type=str, default="gpt")
    return parser.parse_args()

args = parse_args()
st.title("2D чертёж → 3D CAD")

if "generated" not in st.session_state:
    st.session_state.generated = False
if "last_file" not in st.session_state:
    st.session_state.last_file = None

uploaded_file = st.sidebar.file_uploader("Выберите файл изображения", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    ext = os.path.splitext(uploaded_file.name)[1]
    st.image(image, caption="Загруженное изображение", use_column_width=True)
    st.write("Размер изображения: ", image.size)

    # Запускаем генерацию только если файл новый
    if st.session_state.last_file != uploaded_file.name:
        st.session_state.generated = False
        st.session_state.last_file = uploaded_file.name

    if not st.session_state.generated:
        with open(f"temp{ext}", "wb") as f:
            f.write(uploaded_file.getbuffer())

        with st.spinner("Обработка изображения..."):
            generate_step_from_2d_cad_image(
                f"temp{ext}", "output.step", model_type=args.model_type
            )
        st.session_state.generated = True

    st.success("Генерация 3D CAD данных завершена.")

    if os.path.exists("output.step"):
        with open("output.step", "rb") as f:
            st.download_button(
                label="⬇️ Скачать output.step",
                data=f,
                file_name="output.step",
                mime="application/octet-stream",
            )
else:
    st.session_state.generated = False
    st.session_state.last_file = None
    st.write("Изображение не загружено.")