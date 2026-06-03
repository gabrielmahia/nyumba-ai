import streamlit as st
import urllib.request, json

st.set_page_config(page_title="Nyumba AI — Msaada wa Nyumba", page_icon="🏠", layout="centered")
st.markdown("""<style>
.stApp{background:#0a0c14;color:#e8eaf6}
.n-card{background:#0d1030;border:1px solid #283593;border-radius:10px;padding:14px 18px;margin:8px 0}
.warn{background:#1a1000;border:1px solid #f57f17;border-radius:8px;padding:10px 14px;margin:8px 0}
.stButton>button{background:#283593;color:#fff;border:none;border-radius:8px;padding:10px 24px;font-weight:700;width:100%}
</style>""", unsafe_allow_html=True)

API_KEY = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY","")
SYSTEM = """Wewe ni mshauri wa nyumba na ardhi Kenya. Jibu kwa Kiswahili rahisi.
Toa habari kuhusu: bei za kukodi na kununua, haki za mpangaji, uthibitisho wa hati, mikopo ya nyumba.
Onyesha ishara za ulaghai wa ardhi. Kama hali ni ya kisheria, peleka kwa wakili."""

def ask(q):
    if not API_KEY: return "❌ API key not configured."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    body = {"contents":[{"role":"user","parts":[{"text":q}]}],
            "systemInstruction":{"parts":[{"text":SYSTEM}]},
            "generationConfig":{"temperature":0.25,"maxOutputTokens":700}}
    try:
        req = urllib.request.Request(url,data=json.dumps(body).encode(),headers={"Content-Type":"application/json"},method="POST")
        with urllib.request.urlopen(req,timeout=30) as r:
            return json.loads(r.read())["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e: return f"❌ {e}"

st.markdown("# 🏠 Nyumba AI")
st.markdown("**Msaada wa Nyumba na Ardhi Kenya**")
tab1,tab2,tab3,tab4 = st.tabs(["🏘️ Bei za Nyumba","⚖️ Haki za Mpangaji","🚨 Ulaghai wa Ardhi","💰 Mikopo ya Nyumba"])

with tab1:
    area = st.text_input("Eneo:", placeholder="Mfano: Westlands Nairobi, Rongai, Thika Town...")
    bedrooms = st.selectbox("Vyumba:", ["Bedsitter","1 Chumba","2 Vyumba","3 Vyumba","4+ Vyumba"])
    tenure = st.radio("Nia:", ["Kukodi","Kununua"], horizontal=True)
    if st.button("💰 Angalia Bei", key="p_btn") and area:
        with st.spinner("..."): result = ask(f"Bei za {tenure.lower()} nyumba ya {bedrooms} katika {area} Kenya. Toa bei ya makadirio, mambo yanayoathiri bei, na ushauri wa majadiliano.")
        st.markdown(f'<div class="n-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab2:
    q_tenant = st.selectbox("Swali lako:", [
        "Mmiliki wangu anataka kunifukuza — haki zangu ni nini?",
        "Mmiliki hakurejesha amana yangu — nifanye nini?",
        "Mwenyeji anazuia maji/umeme — hii ni halali?",
        "Mkataba wangu wa kukodi umeisha — lazima niondoke?",
        "Ninaweza kupinga kodi mpya ya mmiliki wangu?",
    ])
    if st.button("⚖️ Niambie", key="t_btn"):
        with st.spinner("..."): result = ask(q_tenant + " Eleza haki zangu chini ya sheria za Kenya (Rent Restriction Act, Landlord and Tenant Act).")
        st.markdown(f'<div class="n-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="warn"><b>⚠️ Kenya inapoteza KES 10B+ kwa mwaka kwa ulaghai wa ardhi.</b> Fahamu ishara za hatari.</div>', unsafe_allow_html=True)
    fraud_q = st.selectbox("Hali unayoshuku:", [
        "Muuzaji ana hati lakini hakuna taarifa nyingine",
        "Bei ni ya chini sana — kwa nini?",
        "Muuzaji anasema hati iko court — ninaweza kununua?",
        "Ninaweza kuangalia kama hati ni halisi vipi?",
        "Ardhi ina wamiliki wawili wanaodai umiliki",
        "Jinsi ya kuthibitisha hati kabla ya kununua",
    ])
    if st.button("🚨 Chunguza", key="f_btn"):
        with st.spinner("..."): result = ask(f"Ulaghai wa ardhi: {fraud_q}. Toa hatua za kujikinga na jinsi ya kuthibitisha umiliki wa ardhi Kenya.")
        st.markdown(f'<div class="n-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

with tab4:
    salary = st.number_input("Mshahara wa mwezi (KES):", value=50000, step=5000)
    if st.button("💰 Nionyeshe Chaguo", key="loan_btn"):
        with st.spinner("..."): result = ask(f"Mtu ana mshahara wa KES {salary:,}/mwezi Kenya. Mikopo ya nyumba inayopatikana: KMRC, benki (KCB, Equity, Stanbic), SACCO, Boma Yangu. Toa: Kiasi cha mkopo, Kiwango cha riba, Muda, Masharti.")
        st.markdown(f'<div class="n-card">{result.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

st.markdown("---")
st.caption("🏠 Nyumba AI v1.0 | Si ushauri wa kisheria | Ardhi: lands.go.ke | CC BY-NC-ND 4.0")
