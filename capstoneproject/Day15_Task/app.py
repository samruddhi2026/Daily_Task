import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from Day12_Task.main import generate_response
from Day11_Task.retriever import retrieve

st.set_page_config(page_title="Urban Edge Stylist", page_icon="👗", layout="wide")

page_style = """
<style>
body {
    background: linear-gradient(135deg, #f7f1ee 0%, #fbfbff 40%, #ede4f7 100%);
}
main .block-container {
    padding: 2rem 2rem 2rem 2rem;
    background-color: rgba(255, 255, 255, 0.95);
    border-radius: 36px;
    box-shadow: 0 35px 80px rgba(125, 91, 214, 0.12);
}
section[data-testid="stSidebar"] > div:first-child {
    background: linear-gradient(180deg, #fff9f4 0%, #f3ecff 100%);
    border-radius: 30px;
    padding: 1.5rem;
    border: 1px solid rgba(145, 103, 236, 0.16);
}
.stButton>button {
    background: linear-gradient(135deg, #8f64ff 0%, #5a2d9e 100%);
    color: white;
    border: none;
    border-radius: 22px;
    padding: 1rem 1.6rem;
    font-size: 1rem;
    font-weight: 700;
    box-shadow: 0 18px 30px rgba(90, 45, 158, 0.18);
}
.stButton>button:hover {
    background: linear-gradient(135deg, #7b49db 0%, #4c1f95 100%);
}
.stTextInput>div>div>input {
    border: 2px solid rgba(186, 136, 255, 0.35);
    border-radius: 24px;
    padding: 1rem 1.4rem;
    background: #fff8ff;
    color: #2a1651;
}
.css-1o9u4ze {
    padding: 1rem 1rem 1.5rem 1rem;
}
h1, h2, h3, h4 {
    color: #2f1453;
}
.page-banner {
    background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(245,230,255,0.95));
    border-radius: 30px;
    padding: 1.7rem 2rem;
    margin-bottom: 1.6rem;
    border: 1px solid rgba(156, 112, 255, 0.15);
}
.page-banner h1 {
    margin-bottom: 0.25rem;
}
.page-banner p {
    margin: 0;
    color: #5a3f8d;
}
.outfit-card {
    background: linear-gradient(180deg, #ffffff 0%, #fcf6ff 100%);
    border-radius: 28px;
    padding: 1.4rem;
    margin-bottom: 1rem;
    border: 1px solid rgba(142, 80, 231, 0.18);
    box-shadow: 0 24px 40px rgba(143, 84, 242, 0.08);
}
.outfit-card h3 {
    margin-bottom: 0.5rem;
}
.outfit-card p {
    margin: 0.25rem 0;
    color: #5b4479;
}
.outfit-badge {
    display: inline-block;
    background: #fdf1ff;
    color: #6e49b5;
    border-radius: 999px;
    padding: 0.4rem 0.95rem;
    font-size: 0.9rem;
    font-weight: 700;
    margin-top: 0.7rem;
    letter-spacing: 0.02em;
}
.mantra {
    background: rgba(255,255,255,0.9);
    border-radius: 24px;
    padding: 1.2rem 1.4rem;
    border: 1px dashed rgba(145, 103, 236, 0.24);
    margin-bottom: 1.5rem;
}
.mantra p {
    margin: 0;
    color: #4f3172;
}
.display-window {
    background: linear-gradient(180deg, #fff8f9 0%, #f5effd 100%);
    border: 1px solid rgba(137, 98, 221, 0.18);
    border-radius: 32px;
    padding: 1.5rem;
}
.display-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #3d1f63;
    margin-bottom: 0.8rem;
}
</style>
"""

st.markdown(page_style, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 👚 Stylist’s Closet")
    st.write("Discover your outfit mood inside a wardrobe-style interface.")
    st.markdown("---")
    st.markdown("### Try these looks")
    st.write("- minimalist outfit")
    st.write("- edgy streetwear")
    st.write("- summer outfit")
    st.write("- black outfit ideas")
    st.markdown("---")
    st.markdown("### Styling tools")
    st.write("- Semantic wardrobe search")
    st.write("- FAISS vector retrieval")
    st.write("- Style metadata matching")
    st.markdown("---")
    st.markdown("### Display rack")
    st.write("Use the clothing rack to preview curated fashion recommendations.")
    st.caption("Built using AI • RAG • FAISS")

st.markdown(
    """
    <div class='page-banner'>
        <h1>👗 Urban Edge Stylist</h1>
        <p>Your interactive wardrobe assistant that blends fashion mood, semantic search, and a mannequin-style display.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

query = st.text_input("Enter your style (e.g., minimalist outfit)")

st.markdown(
    """
    <div class='mantra'>
        <p>"From the wardrobe to the runway — choose a style vibe and let the mannequin rack suggest your next outfit."</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.button("✨ Get Recommendation"):
    if query:
        results = retrieve(query)
        st.markdown("<div class='display-window'><div class='display-title'>✨ Outfit Display Window</div></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        for i, item in enumerate(results, 1):
            target_col = col1 if i % 2 else col2
            target_col.markdown(
                f"""
                <div class='outfit-card'>
                    <h3>{i}. {item['text'].title()}</h3>
                    <p><strong>Style:</strong> {item.get('style_vibe', 'unknown').title()}</p>
                    <p><strong>Category:</strong> {item.get('category', 'fashion')}</p>
                    <span class='outfit-badge'>Mannequin Style</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.warning("Please enter a query to open your wardrobe.")

if query:
    st.info("Pick a fashion mood and click Get Recommendation to fill your display rack.")

