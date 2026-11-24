import streamlit as st
import requests

st.set_page_config(page_title="HAYDEN AI", page_icon="🤖")
st.title("🤖 HAYDEN AI")
st.write("Hai Muhammad Adam! Aku Hayden. Semua dalam Bahasa Melayu sekarang!")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Borak", "📚 Wikipedia Melayu", "📰 Berita Melayu", "📖 Kamus Melayu", "❓ Soalan"])

with tab1:
    q = st.text_input("Tanya Hayden dalam Melayu:")
    if q:
        st.success(f"Hayden faham! Kau tanya pasal '{q}' kan? Cuba tengok kat tab Wikipedia Melayu tu, mesti ada jawapan dia.")

with tab2:
    wiki_q = st.text_input("Cari di Wikipedia Bahasa Melayu:", key="wiki")
    bahasa = st.selectbox("Pilih Bahasa Wikipedia:", ["ms - Melayu", "en - English"])
    kode = "ms" if "ms" in bahasa else "en"
    if st.button("Cari Wikipedia"):
        try:
            url = f"https://{kode}.wikipedia.org/api/rest_v1/page/summary/{wiki_q}"
            r = requests.get(url).json()
            st.subheader(r.get("title",""))
            st.write(r.get("extract","Tak jumpa la. Cuba eja lain."))
            if "thumbnail" in r:
                st.image(r["thumbnail"]["source"])
        except:
            st.error("Tak jumpa. Cuba perkataan lain.")

with tab3:
    st.subheader("Berita Terkini Bahasa Melayu")
    if st.button("Load Berita Melayu"):
        try:
            url = "https://api.rss2json.com/v1/api.json?rss_url=https://www.bharian.com.my/rss"
            data = requests.get(url).json()
            for item in data.get("items",[])[:5]:
                st.write(f"**{item['title']}**")
                st.write(item.get("description","")[:250])
                st.write("---")
        except:
            st.error("Berita tak dapat load. Cuba lagi nanti.")

with tab4:
    st.subheader("Kamus Melayu - English")
    st.write("Tulis perkataan Melayu, Hayden bagi maksud English. Atau sebaliknya.")
    word = st.text_input("Cari perkataan:", key="kamus")
    arah = st.radio("Arah Kamus:", ["Melayu -> English", "English -> Melayu"])
    if st.button("Cari Kamus"):
        try:
            src = "ms" if "Melayu ->" in arah else "en"
            tgt = "en" if src=="ms" else "ms"
            url = f"https://api.mymemory.translated.net/get?q={word}&langpair={src}|{tgt}"
            data = requests.get(url).json()
            maksud = data["responseData"]["translatedText"]
            st.success(f"{word} = {maksud}")
            st.write("Kamus ni guna translator Melayu-English.")
        except:
            st.error("Perkataan tak jumpa. Cuba lain.")

with tab5:
    st.write("Kuiz Bahasa Melayu!")
    jawapan = st.radio("Apakah maksud 'gembira'?", ["Sedih", "Happy / Seronok", "Marah"])
    if st.button("Semak Jawapan"):
        if jawapan == "Happy / Seronok":
            st.balloons()
            st.success("BETUL! Pandai Adam! Gembira maksud dia seronok!")
        else:
            st.error("Salah, cuba lagi! Gembira tu maksud dia seronok.")
