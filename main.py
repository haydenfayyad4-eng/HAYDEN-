import streamlit as st
import requests

st.set_page_config(page_title="Hayden AI", page_icon="🤖")
st.title("🤖 Hayden AI - Adam punya kawan")
st.write("Hai Muhammad Adam! Aku Hayden. Borak la apa-apa pun, aku ingat semua.")

# Sidebar untuk API Key
with st.sidebar:
    st.header("Setting")
    api_key = st.text_input("Masukkan Gemini API Key kau", type="password", help="Ambil free kat Google AI Studio")
    st.write("Dah ada key? Paste kat atas tu.")
    if st.button("Padam Borak"):
        st.session_state.messages = []
        st.rerun()

# Simpan borak lama
if "messages" not in st.session_state:
    st.session_state.messages = []

# Papar borak lama
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# Kotak taip soalan
soalan = st.chat_input("Tanya Hayden apa-apa...")

if soalan:
    st.session_state.messages.append({"role": "user", "content": soalan})
    with st.chat_message("user"):
        st.write(soalan)

    if not api_key:
        jawapan = "Eh Adam, kau belum letak API Key lagi la kat sidebar kiri tu. Letak dulu, baru aku boleh jawab power macam ChatGPT."
    else:
        try:
            # Hantar semua borak lama supaya dia ingat
            teks_borak = ""
            for m in st.session_state.messages:
                teks_borak += f"{m['role']}: {m['content']}\n"

            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
            data = {
                "contents": [{"parts": [{"text": f"Kau nama Hayden, kawan baik Muhammad Adam. Cakap Bahasa Melayu rojak yang santai, kelakar, macam kawan. Jangan formal sangat. Ini perbualan setakat ni:\n{teks_borak}\nJawab soalan terakhir ni."}]}]
            }
            res = requests.post(url, json=data, timeout=30)
            jawapan = res.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            jawapan = f"Alaa error sikit: {e}. Cuba check API Key kau betul ke tak."

    st.session_state.messages.append({"role": "assistant", "content": jawapan})
    with st.chat_message("assistant"):
        st.write(jawapan)
