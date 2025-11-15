import re
import base64
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Crop Model Accuracy", layout="wide")

ROOT = Path(".")
HTML = ROOT / "1.html"

html = HTML.read_text(encoding="utf-8")

# Map wrong names → correct files YOU actually have
file_map = {
    "random_forest.png": "random forest.png",
    "naive_bayes.png": "Naive.png",
    "decision_tree.png": "decission.png",
    "correlation_matrix.png": "CORELATION.png",
    "xgboost.png": "XGBOOST.png",
    # these are already correct:
    "svm.png": "svm.png",
    "knn.png": "knn.png",
    "logistic.png": "logistic.png",
    "icon.png": "icon.png"
}

# Inline ANY src/href/data-src that matches these image names
pattern = re.compile(r'(?P<attr>src|href|data-src)=(?P<q>["\'])(?P<path>[^"\']+\.(?:png|jpg|jpeg|gif|svg))(?P=q)',
                     re.IGNORECASE)

def to_data_uri(filename):
    suf = filename.suffix.lower()
    mime = "image/png"
    if suf in (".jpg", ".jpeg"): mime = "image/jpeg"
    if suf == ".svg": mime = "image/svg+xml"

    b64 = base64.b64encode(filename.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"

def replace_img(m):
    attr = m.group("attr")
    original = m.group("path")

    # If wrong name → map to the REAL name
    real_name = file_map.get(original, original)

    p = ROOT / real_name
    if not p.exists():
        # leave unchanged but warn
        st.warning(f"Image not found: {real_name}")
        return m.group(0)

    data_uri = to_data_uri(p)
    return f'{attr}="{data_uri}"'

html = pattern.sub(replace_img, html)

# Render
st.components.v1.html(html, height=2000, scrolling=True)
