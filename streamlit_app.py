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
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    .block-container {
        padding-top: 2.5rem;
        max-width: 760px;
    }
    .app-header {
        margin-bottom: 2rem;
    }
    .app-title {
        font-size: 1.6rem;
        font-weight: 600;
        color: #0f0f0f;
        letter-spacing: -0.5px;
        margin: 0 0 4px 0;
    }
    .app-subtitle {
        font-size: 0.85rem;
        color: #888;
        font-family: 'DM Mono', monospace;
        margin: 0;
    }
    .section-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #aaa;
        margin-bottom: 10px;
    }
    .sample-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        margin-bottom: 1.5rem;
    }
    .sample-btn {
        background: #f7f7f7;
        border: 1px solid #e8e8e8;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 0.82rem;
        color: #333;
        cursor: pointer;
        text-align: left;
        line-height: 1.4;
        transition: all 0.15s ease;
        font-family: 'DM Sans', sans-serif;
        width: 100%;
    }
    .sample-btn:hover {
        background: #f0f0f0;
        border-color: #d0d0d0;
    }
    .results-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 1.8rem 0 1rem 0;
    }
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-family: 'DM Mono', monospace;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .badge-focus  { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }
    .badge-high   { background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; }
    .badge-medium { background: #fffbeb; color: #92400e; border: 1px solid #fde68a; }
    .badge-low    { background: #fef2f2; color: #991b1b; border: 1px solid #fecaca; }
    .insight-card {
        background: #fff;
        border: 1px solid #e8e8e8;
        border-radius: 10px;
        padding: 16px 18px;
        margin-bottom: 10px;
    }
    .insight-number {
        font-size: 0.72rem;
        font-family: 'DM Mono', monospace;
        color: #aaa;
        font-weight: 500;
        margin-bottom: 6px;
    }
    .insight-action {
        font-size: 0.95rem;
        font-weight: 600;
        color: #0f0f0f;
        line-height: 1.5;
        margin-bottom: 10px;
    }
    .insight-meta {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }
    .insight-evidence {
        font-size: 0.8rem;
        color: #666;
        line-height: 1.4;
        display: flex;
        gap: 6px;
    }
    .insight-impact {
        font-size: 0.8rem;
        color: #059669;
        line-height: 1.4;
        display: flex;
        gap: 6px;
        font-weight: 500;
    }
    .meta-icon {
        flex-shrink: 0;
        opacity: 0.7;
    }
    .divider {
        border: none;
        border-top: 1px solid #f0f0f0;
        margin: 2rem 0 1rem 0;
    }
    .footer-text {
        font-size: 0.75rem;
        color: #bbb;
        font-family: 'DM Mono', monospace;
    }
    div[data-testid="stTextArea"] textarea {
        border-radius: 8px !important;
        border-color: #e0e0e0 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.92rem !important;
    }
    div[data-testid="stTextArea"] textarea:focus {
        border-color: #aaa !important;
        box-shadow: none !important;
    }
    div[data-testid="stButton"] > button[kind="primary"] {
        background: #0f0f0f !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        padding: 0.55rem 1rem !important;
    }
    div[data-testid="stButton"] > button[kind="primary"]:hover {
        background: #333 !important;
    }
    div[data-testid="stButton"] > button[kind="secondary"] {
        border-radius: 8px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.82rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ── session state ─────────────────────────────────────────────────────────────
if "query_text" not in st.session_state:
    st.session_state["query_text"] = ""
if "results" not in st.session_state:
    st.session_state["results"] = None
if "pending_sample" not in st.session_state:
    st.session_state["pending_sample"] = None

# ── apply pending sample before rendering text area ───────────────────────────
# This is the fix: we apply the sample BEFORE the text area renders,
# not after — so st.rerun() is not needed and there is no flicker or lag
if st.session_state["pending_sample"]:
    st.session_state["query_text"] = st.session_state["pending_sample"]
    st.session_state["pending_sample"] = None
    st.session_state["results"] = None

# ── header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <p class="app-title">CRO Insight System</p>
  <p class="app-subtitle">BFSI · Forms · Landing Pages · Paid Ads</p>
</div>
""", unsafe_allow_html=True)

# ── sample queries ────────────────────────────────────────────────────────────
SAMPLE_QUERIES = [
    "Why are users dropping off on our insurance quote form?",
    "How do we improve our loan landing page for paid traffic?",
    "What improves mobile form completions for a credit card page?",
    "High bounce rate on our BFSI page from Google Ads — what to fix?",
    "How to reduce drop-off at the KYC document upload step?",
    "What CTA copy works best for a mutual fund SIP page?",
]

st.markdown('<p class="section-label">Quick prompts</p>', unsafe_allow_html=True)
cols = st.columns(2)
for i, sample in enumerate(SAMPLE_QUERIES):
    if cols[i % 2].button(sample, key=f"s_{i}", use_container_width=True):
        st.session_state["pending_sample"] = sample
        st.rerun()

st.markdown("<div style='margin-top:1.2rem'></div>", unsafe_allow_html=True)

# ── text area — value driven by session state ─────────────────────────────────
query = st.text_area(
    "Describe your CRO problem",
    value=st.session_state["query_text"],
    height=100,
    placeholder="e.g. Users abandon our insurance form at the income field…",
)

# sync manual typing back to session state
st.session_state["query_text"] = query

# ── analyse button ────────────────────────────────────────────────────────────
col1, col2 = st.columns([4, 1])
with col1:
    analyse = st.button("Analyse", type="primary", use_container_width=True)
with col2:
    if st.button("Clear", use_container_width=True):
        st.session_state["query_text"] = ""
        st.session_state["results"] = None
        st.rerun()

if analyse:
    clean = query.strip()
    if not clean:
        st.warning("Please enter a problem or pick a quick prompt above.")
    else:
        st.session_state["query_text"] = clean
        with st.spinner("Retrieving insights…"):
            try:
                resp = requests.post(
                    f"{API_URL}/analyze",
                    json={"query": clean},
                    timeout=60,
                )
                resp.raise_for_status()
                st.session_state["results"] = resp.json()
            except requests.exceptions.ConnectionError:
                st.error("Cannot reach backend. If self-hosting run: uvicorn main:app --reload")
                st.stop()
            except requests.exceptions.Timeout:
                st.error("Request timed out — server may be waking up. Try again in 15 seconds.")
                st.stop()
            except Exception as e:
                st.error(f"Error: {e}")
                st.stop()

# ── results ───────────────────────────────────────────────────────────────────
if st.session_state["results"]:
    data     = st.session_state["results"]
    focus    = data.get("focus_area", "general")
    conf     = data.get("confidence", "medium")
    insights = data.get("insights", [])

    conf_class = {"high": "badge-high", "medium": "badge-medium", "low": "badge-low"}.get(conf, "badge-medium")

    st.markdown(f"""
<div class="results-header">
  <span class="badge badge-focus">{focus.replace("_", " ")}</span>
  <span class="badge {conf_class}">{conf} confidence</span>
</div>
""", unsafe_allow_html=True)

    for i, insight in enumerate(insights, 1):
        if isinstance(insight, dict):
            action   = insight.get("action", "")
            evidence = insight.get("evidence", "")
            impact   = insight.get("impact", "")
            st.markdown(f"""
<div class="insight-card">
  <div class="insight-number">0{i}</div>
  <div class="insight-action">{action}</div>
  <div class="insight-meta">
    <div class="insight-evidence"><span class="meta-icon">📊</span><span>{evidence}</span></div>
    <div class="insight-impact"><span class="meta-icon">🎯</span><span>{impact}</span></div>
  </div>
</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
<div class="insight-card">
  <div class="insight-number">0{i}</div>
  <div class="insight-action">{insight}</div>
</div>""", unsafe_allow_html=True)

    if conf == "low":
        st.info("Low confidence — try adding more context or rephrasing the problem.")

st.markdown('<hr class="divider"/>', unsafe_allow_html=True)
st.markdown('<p class="footer-text">Baymard · CXL · Nielsen Norman · VWO · Hotjar · Unbounce · McKinsey · Forrester · IRDAI</p>', unsafe_allow_html=True)
