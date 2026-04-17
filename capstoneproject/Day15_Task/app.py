import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from Day12_Task.main import generate_response, hf_generate_image
import json

st.set_page_config(page_title="Urban Edge Stylist", page_icon="👗", layout="wide")

page_style = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;700&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Outfit', sans-serif;
    background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
}

main .block-container {
    padding: 3rem 4rem;
    background-color: rgba(255, 255, 255, 0.98);
    border-radius: 40px;
    box-shadow: 0 40px 100px rgba(0, 0, 0, 0.05);
    margin-top: 20px;
}

section[data-testid="stSidebar"] > div:first-child {
    background: #ffffff;
    border-radius: 0;
    padding: 2rem;
    border-right: 1px solid #eee;
}

.stButton>button {
    background: #111;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.8rem 2rem;
    font-size: 1rem;
    font-weight: 700;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    background: #333;
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.stTextInput>div>div>input {
    border: 1px solid #e0e0e0;
    border-radius: 14px;
    padding: 0.9rem 1.2rem;
    font-size: 1.1rem;
}

.page-banner {
    background: #000;
    border-radius: 20px;
    padding: 3rem 2.5rem;
    margin-bottom: 2.5rem;
    color: white;
    text-align: center;
}

.page-banner h1 {
    font-size: 3.5rem;
    font-weight: 700;
    letter-spacing: -0.05em;
    margin-bottom: 0.5rem;
    color: white;
}

.page-banner p {
    font-size: 1.1rem;
    opacity: 0.8;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.outfit-card {
    background: #ffffff;
    border-radius: 24px;
    padding: 2rem;
    border: 1px solid #f0f0f0;
    transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
}

.outfit-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 30px 60px rgba(0,0,0,0.08);
}

.outfit-badge {
    background: #000;
    color: #fff;
    border-radius: 4px;
    padding: 0.3rem 0.8rem;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

.mantra {
    border-left: 4px solid #111;
    padding: 1rem 1.5rem;
    background: #f9f9f9;
    margin-bottom: 2rem;
    font-style: italic;
    color: #444;
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
    st.write("- Mannequin Catalog Mode")
    st.markdown("---")
    st.caption("Built using AI • RAG • Pollinations")

st.markdown(
    """
    <div class='page-banner'>
        <h1>👗 Urban Edge Stylist</h1>
        <p>Your interactive wardrobe assistant: Single Outfit Curation & Studio Mannequin Display.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("style_vibe_form", clear_on_submit=False):
    query = st.text_input("Enter your style vibe (e.g., minimalist office wear)")
    
    st.markdown(
        """
        <div class='mantra'>
            <p>"From the wardrobe to the runway — Choose a vibe, and let the AI mannequin render your style."</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    submit = st.form_submit_button("Get Recommendation")

if submit:
    if query:
        # Initialize session state for outfit if not present
        outfit_data = None
        img_placeholder_html = ""

        with st.status("Creative Stylist at work...", expanded=True) as status:
            st.write("Analyzing your wardrobe...")
            raw_response = generate_response(query)
            
            try:
                data = json.loads(raw_response)
                outfit_data = data.get("outfit")
                image_prompt = data.get("image_prompt")
            except:
                st.write(raw_response) # Fallback

            if outfit_data:
                st.write("Curating your perfect look...")
                st.write(f"Rendering: {outfit_data['style']}...")
                img_data, _ = hf_generate_image(image_prompt)
                
                st.write("Capturing final studio shot...")
                status.update(label="Studio Mannequin Ready!", state="complete", expanded=False)
                
                if img_data:
                    img_placeholder_html = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; border-radius:30px; box-shadow: 0 15px 35px rgba(0,0,0,0.15);">'
            else:
                status.update(label=" Stylist encountered a glitch", state="error")

        # RENDER OUTSIDE STATUS CONTAINER (Fixes "Showing Code" Bug)
        if outfit_data:
            st.markdown(f"## {outfit_data['style']}")
            
            # Professional Catalog Layout: Image Left, Details Right
            col_img, col_txt = st.columns([1, 1])
            
            with col_img:
                if img_placeholder_html:
                    st.markdown(img_placeholder_html, unsafe_allow_html=True)
                else:
                    st.warning("Studio camera was slightly out of focus. Please try again!")
            
            with col_txt:
                items_html = "<ul>"
                
                # Intelligent One-Piece Detection
                top = outfit_data.get("topwear", "").lower()
                bottom = outfit_data.get("bottomwear", "").lower()
                is_one_piece = bottom == "none" and any(x in top for x in ["gown", "sari", "dress", "jumpsuit", "lehenga", "suit", "set"])

                for cat in ["topwear", "bottomwear", "layer", "footwear", "accessories"]:
                    val = outfit_data.get(cat)
                    if val and val.lower() != "none":
                        # Dynamic Labeling
                        label = cat.title()
                        if is_one_piece and cat == "topwear":
                            label = "Outfit"
                        
                        items_html += f"<li><strong style='color:#6a4da8;'>{label}:</strong> {val}</li>"
                items_html += "</ul>"

                st.markdown(
                    f"""
                    <div class='outfit-card' style='height: 100%;'>
                        <p style='font-style: italic; color: #5a3f8d; margin-bottom: 20px;'>A high-fidelity studio curation based on your mood: "{query}".</p>
                        <hr style='border: 0; border-top: 1px solid rgba(0,0,0,0.05); margin-bottom: 15px;'>
                        {items_html}
                        <br>
                        <span class='outfit-badge'> Studio Mannequin Edition</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        elif query:
            st.warning("Could not structure the recommendation. Try a different vibe!")
    else:
        st.warning("Please enter a query to open your wardrobe.")

if query:
    st.info("Pick a fashion mood and click Get Recommendation to fill your display rack.")

