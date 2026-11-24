import streamlit as st
import requests
import xml.etree.ElementTree as ET

# --- PASTE API KEY KAU KAT SINI ---
API_KEY = "LETAK_KEY_KAU_KAT_SINI"

st.set_page_config(page_title="Hayden AI", page_icon="🤖")
st.title("🤖 Hayden AI - Cikgu Adam")
st.write("Hai Adam! Semua ada kat sini, pilih tab kat bawah.")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["💬 Borak", "📚 Wikipedia", "📰 Berita", "📖 Kamus", "📕 Novel", "🕌 Islam"])

# ============ 1. BORAK ============
with tab1:
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
            teks = ""
            for m in st.session_state.messages:
                teks += f"{m['role']}: {m['content']}\n"
            if mode == "Belajar Bahasa Inggeris":
                arahan = "Kau Cikgu English best. Ajar Muhammad Adam English santai, kelakar, campur Melayu + English. Betulkan grammar, bagi contoh dan latihan sikit."
            elif mode == "Belajar Coding":
                arahan = "Kau Cikgu Coding power. Ajar Muhammad Adam coding Python dari basic sampai pandai. Terangkan step by step Bahasa Melayu rojak senang faham. Bagi contoh code pendek dan latihan kecil."
            else:
                arahan = "Kau Hayden, kawan baik Muhammad Adam. Cakap Melayu rojak santai, kelakar macam kawan."
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
            data = {"contents": [{"parts": [{"text": f"{arahan}\nPerbualan:\n{teks}\nJawab soalan terakhir."}]}]}
            res = requests.post(url, json=data, timeout=30)
            jawapan = res.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            jawapan = f"Alaa error: {e}. Check API Key kat atas code tu."
        st.session_state.messages.append({"role": "assistant", "content": jawapan})
        with st.chat_message("assistant"):
            st.write(jawapan)

# ============ 2. WIKIPEDIA ============
with tab2:
    st.header("📚 Wikipedia Melayu")
    cari = st.text_input("Taip apa nak cari, contoh: Hang Tuah", key="wiki")
    if st.button("Cari Wikipedia"):
        try:
            r = requests.get(f"https://ms.wikipedia.org/api/rest_v1/page/summary/{cari}", timeout=10).json()
            st.subheader(r.get("title", cari))
            st.write(r.get("extract", "Tak jumpa la. Cuba eja lain."))
            if r.get("thumbnail"):
                st.image(r["thumbnail"]["source"])
        except:
            st.write("Tak jumpa. Cuba taip lain.")

# ============ 3. BERITA ============
with tab3:
    st.header("📰 Berita Melayu Terkini")
    sumber = st.selectbox("Pilih Berita", ["Berita Harian", "
