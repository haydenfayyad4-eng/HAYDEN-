import streamlit as st
import requests

# --- LETAK API KEY KAU KAT SINI ---
API_KEY = "LETAK_KEY_KAU_KAT_SINI"

st.set_page_config(page_title="Hayden AI", page_icon="🤖")
st.title("🤖 Hayden AI - Cikgu Adam")
st.write("Hai Muhammad Adam! Aku Hayden. Nak belajar apa hari ni?")

with st.sidebar:
    mode = st.selectbox("Nak belajar apa?", ["Borak Biasa", "Belajar Bahasa Inggeris", "Belajar Coding"])
    if st.button("Padam Borak"):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

soalan = st.chat_input("Tanya Hayden...")

if soalan:
    st.session_state.messages.append({"role": "user", "content": soalan})
    with st.chat_message("user"):
        st.write(soalan)

    try:
        teks_borak = ""
        for m in st.session_state.messages:
            teks_borak += f"{m['role']}: {m['content']}\n"

        if mode == "Belajar Bahasa Inggeris":
            arahan = "Kau Cikgu English yang best. Ajar Muhammad Adam Bahasa Inggeris cara santai, kelakar, guna Bahasa Melayu campur English. Kalau dia salah grammar, betulkan dan bagi contoh. Bagi latihan sikit-sikit."
        elif mode == "Belajar Coding":
            arahan = "Kau Cikgu Coding yang power. Ajar Muhammad Adam coding dari basic sampai pandai, guna Python. Terangkan step by step, guna Bahasa Melayu rojak yang senang faham. Bagi contoh code yang pendek, lepas tu bagi latihan kecil."
        else:
            arahan = "Kau Hayden, kawan baik Muhammad Adam. Cakap Bahasa Melayu rojak santai, kelakar macam kawan."

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
        data = {"contents": [{"parts": [{"text": f"{arahan}\nPerbualan:\n{teks_borak}\nJawab soalan terakhir."}]}]}
        res = requests.post(url, json=data, timeout=30)
        jawapan = res.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        jawapan = f"Alaa error: {e}. Check API Key kau betul ke tak."

    st.session_state.messages.append({"role": "assistant", "content": jawapan})
    with st.chat_message("assistant"):
        st.write(jawapan)
