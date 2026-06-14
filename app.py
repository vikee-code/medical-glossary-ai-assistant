import streamlit as st
from modules.gemini_client import get_gemini_response

st.set_page_config(
    page_title="Medical Terminology Assistant",
    page_icon="🩺",
    layout="centered"  
)

st.title("🩺 Medical Terminology Assistant")

st.markdown("""
### Selamat Datang

Asisten AI ini dirancang khusus untuk membantu Anda:
- **Menerjemahkan Istilah Medis**: Mengubah bahasa kedokteran yang rumit menjadi penjelasan yang mudah dipahami orang awam.
- **Menjelaskan Hasil Lab/Diagnosis**: Membantu memahami arti dari kata-kata asing di lembar diagnosis atau hasil laboratorium Anda.
- **Kamus Kesehatan Portabel**: Menjawab pertanyaan seputar singkatan atau prosedur medis.

⚠️ **PENTING**: *Alat ini hanya berfungsi sebagai media edukasi dan pendukung informasi. Alat ini tidak menggantikan diagnosis, saran, atau perawatan dari dokter profesional.*
""")

st.divider()


if "started" not in st.session_state:
    st.session_state["started"] = False


api_key = st.text_input(
    "Masukkan Gemini API Key Anda untuk Memulai",
    type="password",
    placeholder="AIzaSy..."
)

if api_key:
    st.success("API Key berhasil dimuat!")


if st.button("Mulai Asisten", disabled=not bool(api_key)):
    st.session_state["started"] = True

st.divider()

if st.session_state["started"]:

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": """
Halo! Saya adalah **Asisten Istilah Medis** Anda. 👋

Tugas saya adalah menjelaskan bahasa atau istilah kedokteran yang rumit menjadi kalimat yang santai dan mudah dipahami oleh orang awam.

**Apa yang ingin Anda tanyakan hari ini?**
*Contoh: "Apa itu kardiomegali?" atau "Apa arti istilah 'suspek' pada hasil rontgen?"*
"""
            }
        ]

    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Tanyakan istilah medis di sini...")

    if prompt:
        # Tampilkan langsung pesan dari user ke layar
        with st.chat_message("user"):
            st.markdown(prompt)
        
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Sedang merangkum penjelasan..."):
                try:
                    # Persona LLM
                    system_instruction = (
                        "Anda adalah seorang dokter ramah yang ahli menjelaskan istilah medis rumit "
                        "menjadi analogi atau bahasa yang sangat sederhana, mudah dipahami orang awam, "
                        "dan menenangkan tanpa mengurangi esensi akurasi medisnya. Gunakan bahasa Indonesia."
                    )
                    
                    full_prompt = f"{system_instruction}\n\nPertanyaan User: {prompt}"
                    
                    # Panggil function dari gemini_client.py 
                    response = get_gemini_response(api_key, full_prompt)
                    
                except Exception as e:
                    response = f"Gagal mendapatkan respon dari AI. Error: {str(e)}"
                
                # Tampilkan respons asisten ke layar
                st.markdown(response)
        
        # Simpan respons asisten ke dalam riwayat session_state
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        st.rerun()
