import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageDraw
from io import BytesIO

st.set_page_config(page_title="Kreiserkennung", layout="wide")
st.title("🔍 Kreise im Bild erkennen (1–100 mm)")

uploaded_file = st.sidebar.file_uploader("📁 Bild hochladen", type=["png", "jpg", "jpeg", "tif", "tiff"])
if not uploaded_file:
    st.warning("Bitte zuerst ein Bild hochladen.")
    st.stop()

# Bild vorbereiten
img = Image.open(uploaded_file).convert("RGB")
img_array = np.array(img)
gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)

# DPI oder Maßstab eingeben
dpi = st.sidebar.number_input("📏 Bildauflösung (DPI)", min_value=10, max_value=1200, value=300)
mm_to_pixel = lambda mm: int((mm / 25.4) * dpi)

min_mm = st.sidebar.slider("🔽 Minimaler Durchmesser (mm)", 1, 100, 5)
max_mm = st.sidebar.slider("🔼 Maximaler Durchmesser (mm)", min_mm, 100, 50)

min_radius = mm_to_pixel(min_mm) // 2
max_radius = mm_to_pixel(max_mm) // 2

# Kreise erkennen
circles = cv2.HoughCircles(
    gray,
    cv2.HOUGH_GRADIENT,
    dp=1.2,
    minDist=10,
    param1=50,
    param2=30,
    minRadius=min_radius,
    maxRadius=max_radius
)

# Kreise zeichnen
draw_img = img.copy()
draw = ImageDraw.Draw(draw_img)

if circles is not None:
    circles = np.uint16(np.around(circles))
    for x, y, r in circles[0, :]:
        draw.ellipse([(x - r, y - r), (x + r, y + r)], outline="red", width=2)
    st.image(draw_img, caption="🟠 Erkannte Kreise", use_container_width=True)

    # Download-Button
    buffer = BytesIO()
    draw_img.save(buffer, format="PNG")
    st.download_button(
        label="📥 Bild mit Kreisen herunterladen",
        data=buffer.getvalue(),
        file_name="kreise_erkannt.png",
        mime="image/png"
    )
else:
    st.info("Keine Kreise im angegebenen Größenbereich erkannt.")
