import streamlit as st
import requests

# === Configuration ===
GROQ_API_KEY = "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"  
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama3-70b-8192"  # Use the correct model name from Groq

# === Helper Functions ===
def create_prompt(description):
    return f"""
    A company wants to build: "{description}"
    
    Recommend the best tech stack for this product.

    Include:
    - Frontend framework
    - Backend language
    - Database
    - Hosting/cloud provider

    Answer in bullet points.
    """

def ask_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(GROQ_URL, headers=headers, json=data)
    result = response.json()
    return result["choices"][0]["message"]["content"]

# === Streamlit UI ===
st.set_page_config(page_title="Tech Stack Recommender", page_icon="🧠")
st.title("🧠 AI Tech Stack Recommender")
st.write("Describe your product and get a suggested technology stack.")

product_description = st.text_area("Product Description", height=150, placeholder="e.g., An eCommerce platform for handmade crafts")

if st.button("Get Recommendation"):
    if not product_description.strip():
        st.warning("Please enter a description first.")
    else:
        with st.spinner("Thinking..."):
            prompt = create_prompt(product_description)
            response = ask_groq(prompt)
            st.success("Here's the recommended stack:")
            st.code(response)
