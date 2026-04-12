import streamlit as st
import requests
import threading

API_URL = st.secrets.get("API_URL", "http://127.0.0.1:8000")

def wake_backend():
    try:
        requests.get(f"{API_URL}/", timeout=10)
    except:
        pass

threading.Thread(target=wake_backend, daemon=True).start()

st.set_page_config(
    page_title="CRO AI Insight System",
    page_icon="📈",
    layout="centered",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
    .block-container { padding-top: 2rem; }
    .insight-card {
        background: #141414;
        border-left: 3px solid #00e5a0;
        border-radius: 4px;
        padding: 14px 18px;
        margin-bottom: 10px;
        color: #e8e8e8;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .meta-badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-family: 'IBM Plex Mono', monospace;
        font-weight: 600;
        text-transform: uppercase;
        margin-right: 6px;
    }
    .badge-green  { background: #00e5a01a; color: #00e5a0; border: 1px solid #00e5a044; }
    .badge-yellow { background: #ffd60a1a; color: #ffd60a; border: 1px solid #ffd60a44; }
    .badge-red    { background: #ff4d4f1a; color: #ff4d4f; border: 1px solid #ff4d4f44; }
    .badge-blue   { background: #4da6ff1a; color: #4da6ff; border: 1px solid #4da6ff44; }
</style>
""", unsafe_allow_html=True)

# ── session state init ────────────────────────────────────────────────────────
if "query_text" not in st.session_state:
    st.session_state["query_text"] = ""
if "results" not in st.session_state:
    st.session_state["results"] = None

# ── header ────────────────────────────────────────────────────────────────────
st.title("📈 CRO AI Insight System")
st.caption("BFSI · Forms · Landing Pages · Paid Ads — powered by RAG + GPT-4o-mini")

# ── sample query buttons ──────────────────────────────────────────────────────
SAMPLE_QUERIES = [
    "Why are users dropping off on our insurance quote form?",
    "How can we improve our loan application landing page for paid traffic?",
    "What changes will improve mobile form completions for a credit card page?",
    "Our BFSI landing page has high bounce rate from Google Ads — what should we fix?",
    "How do we reduce drop-off at the KYC document upload step?",
]

st.markdown("**Try a sample query:**")
cols = st.columns(2)
for i, sample in enumerate(SAMPLE_QUERIES):
    if cols[i % 2].button(sample, key=f"sample_{i}", use_container_width=True):
        st.session_state["query_text"] = sample
        st.session_state["results"] = None
        st.rerun()

# ── text area ─────────────────────────────────────────────────────────────────
query = st.text_area(
    "Or describe your CRO problem:",
    value=st.session_state["query_text"],
    height=110,
    placeholder="e.g. Users are abandoning our insurance form at the income field…",
)

# ── analyse button ────────────────────────────────────────────────────────────
if st.button("🔍 Analyse", type="primary", use_container_width=True):
    clean = query.strip()
    if not clean:
        st.warning("Please enter a query or select a sample.")
    else:
        st.session_state["query_text"] = clean
        with st.spinner("Waking up server + retrieving insights… (may take 30s if idle)"):
            try:
                resp = requests.post(
                    f"{API_URL}/analyze",
                    json={"query": clean},
                    timeout=60,
                )
                resp.raise_for_status()
                st.session_state["results"] = resp.json()
            except requests.exceptions.ConnectionError:
                st.error("❌ Server is starting up, please click Analyse again in 30 seconds.")
                st.stop()
            except requests.exceptions.Timeout:
                st.error("❌ Request timed out. Please try again.")
                st.stop()
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.stop()

# ── results ───────────────────────────────────────────────────────────────────
if st.session_state["results"]:
    data     = st.session_state["results"]
    focus    = data.get("focus_area", "general")
    conf     = data.get("confidence", "medium")
    insights = data.get("insights", [])

    conf_class = {"high": "badge-green", "medium": "badge-yellow", "low": "badge-red"}.get(conf, "badge-yellow")

    st.markdown(
        f'<span class="meta-badge badge-blue">{focus.replace("_", " ")}</span>'
        f'<span class="meta-badge {conf_class}">confidence: {conf}</span>',
        unsafe_allow_html=True,
    )
    st.markdown("### Insights")
    for i, insight in enumerate(insights, 1):
        st.markdown(
            f'<div class="insight-card"><strong>{i}.</strong> {insight}</div>',
            unsafe_allow_html=True,
        )

    if conf == "low":
        st.info("Low confidence — try rephrasing or adding more context.")

    if st.button("🔄 Clear Results"):
        st.session_state["results"] = None
        st.session_state["query_text"] = ""
        st.rerun()

st.divider()
st.caption("Knowledge base: BFSI research · Baymard · CXL · Nielsen Norman · VWO · Hotjar · Unbounce · McKinsey · Forrester")
