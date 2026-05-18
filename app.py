import streamlit as st
from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Microfiber Image Analysis", layout="wide")

st.title("Microscope + Image Analysis Digital Model")
st.write("AI-Based Microfiber Detection from Wastewater Images")

uploaded_file = st.file_uploader(
    "Upload Microscope Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    # Open image
    image = Image.open(uploaded_file)

    # Convert to grayscale
    gray_image = image.convert("L")

    # Apply threshold
    threshold_value = 120

    binary_image = gray_image.point(
        lambda p: 255 if p > threshold_value else 0
    )

    # Convert to numpy array
    binary_array = np.array(binary_image)

    # Simple fiber estimation
    white_pixels = np.sum(binary_array == 255)

    fiber_count = white_pixels // 500

    avg_length = round(fiber_count * 0.12, 2)

    # AI Logic (UPDATED)
    if fiber_count < 1000:
        contamination = "LOW"
        decision = "Normal Filtration"
    else:
        contamination = "HIGH"
        decision = "Advanced Filtration"

    # Layout
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Original Microscope Image")
        st.image(image, use_container_width=True)

    with col2:
        st.subheader("Grayscale Image")
        st.image(gray_image, use_container_width=True)

    with col3:
        st.subheader("Threshold Detection")
        st.image(binary_image, use_container_width=True)

    # Results
    st.subheader("Microfiber Analysis Result")

    result_data = {
        "Parameter": [
            "Estimated Fiber Count",
            "Average Fiber Length",
            "Contamination Level",
            "AI Filtration Decision"
        ],
        "Output": [
            fiber_count,
            f"{avg_length} mm",
            contamination,
            decision
        ]
    }

    df = pd.DataFrame(result_data)
    st.table(df)

    # Graph
    st.subheader("Fiber Analysis Graph")

    graph_data = pd.DataFrame({
        "Category": ["Detected Fibers"],
        "Value": [fiber_count]
    })

    fig, ax = plt.subplots()

    ax.bar(
        graph_data["Category"],
        graph_data["Value"]
    )

    ax.set_ylabel("Fiber Count")

    st.pyplot(fig)

    # AI Output
    st.subheader("AI Decision Output")

    if contamination == "LOW":
        st.success(f"Recommended Action: {decision}")
    else:
        st.error(f"Recommended Action: {decision}")

else:
    st.info("Please upload a microscope image to begin analysis.")