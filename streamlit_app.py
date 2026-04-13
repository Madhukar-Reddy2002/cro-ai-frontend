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
    page_title="CRO AI — Insight Engine",
    page_icon="⚡",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: #0a0a0f;
    color: #e8e8f0;
}
.block-container {
    padding-top: 2rem;
    max-width: 780px;
}

/* ── header ── */
.hero {
    padding: 2.5rem 0 2rem 0;
    position: relative;
}
.hero-eyebrow {
    font-family: 'Inter', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #a78bfa;
    margin-bottom: 12px;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -1px;
    margin: 0 0 12px 0;
    background: linear-gradient(135deg, #ffffff 0%, #a78bfa 50%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 0.95rem;
    color: #6b7280;
    line-height: 1.6;
    margin: 0;
}

/* ── pills ── */
.pill-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 1.8rem;
}
.pill {
    background: rgba(167,139,250,0.08);
    border: 1px solid rgba(167,139,250,0.2);
    border-radius: 100px;
    padding: 5px 14px;
    font-size: 0.75rem;
    color: #a78bfa;
    font-weight: 500;
    letter-spacing: 0.03em;
}

/* ── sample buttons ── */
.section-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #4b5563;
    margin-bottom: 10px;
}

div[data-testid="stButton"] > button {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #9ca3af !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.8rem !important;
    font-weight: 400 !important;
    text-align: left !important;
    padding: 10px 14px !important;
    transition: all 0.2s ease !important;
    line-height: 1.4 !important;
}
div[data-testid="stButton"] > button:hover {
    background: rgba(167,139,250,0.08) !important;
    border-color: rgba(167,139,250,0.3) !important;
    color: #e8e8f0 !important;
    transform: translateY(-1px) !important;
}

/* ── primary button ── */
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg, #7c3aed, #2563eb) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #fff !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    padding: 0.65rem 1.2rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 0 20px rgba(124,58,237,0.3) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    box-shadow: 0 0 32px rgba(124,58,237,0.5) !important;
    transform: translateY(-1px) !important;
}

/* ── textarea ── */
div[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e8e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.92rem !important;
    line-height: 1.6 !important;
    padding: 14px !important;
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(167,139,250,0.4) !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.1) !important;
}
div[data-testid="stTextArea"] label {
    color: #6b7280 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
}

/* ── problem summary banner ── */
.problem-banner {
    background: linear-gradient(135deg, rgba(124,58,237,0.12), rgba(37,99,235,0.12));
    border: 1px solid rgba(167,139,250,0.2);
    border-radius: 12px;
    padding: 14px 18px;
    margin: 1.8rem 0 1.2rem 0;
    font-size: 0.88rem;
    color: #c4b5fd;
    line-height: 1.5;
}
.problem-banner strong {
    color: #a78bfa;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    display: block;
    margin-bottom: 5px;
}

/* ── badges ── */
.badge-row {
    display: flex;
    gap: 8px;
    align-items: center;
    margin-bottom: 1.2rem;
    flex-wrap: wrap;
}
.badge {
    display: inline-flex;
    align-items: center;
    padding: 4px 12px;
    border-radius: 100px;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.badge-focus  { background: rgba(56,189,248,0.1);  color: #38bdf8; border: 1px solid rgba(56,189,248,0.25); }
.badge-high   { background: rgba(52,211,153,0.1);  color: #34d399; border: 1px solid rgba(52,211,153,0.25); }
.badge-medium { background: rgba(251,191,36,0.1);  color: #fbbf24; border: 1px solid rgba(251,191,36,0.25); }
.badge-low    { background: rgba(248,113,113,0.1); color: #f87171; border: 1px solid rgba(248,113,113,0.25); }

/* ── insight cards ── */
.insight-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 22px 24px;
    margin-bottom: 14px;
    position: relative;
    transition: border-color 0.2s ease;
}
.insight-card:hover {
    border-color: rgba(167,139,250,0.3);
}
.insight-index {
    font-family: 'Syne', sans-serif;
    font-size: 0.68rem;
    font-weight: 700;
    color: #4b5563;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-bottom: 10px;
}
.insight-action {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #f3f4f6;
    line-height: 1.45;
    margin-bottom: 14px;
}
.insight-hypothesis {
    background: rgba(167,139,250,0.06);
    border-left: 2px solid #7c3aed;
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    font-size: 0.82rem;
    color: #c4b5fd;
    line-height: 1.55;
    margin-bottom: 14px;
    font-style: italic;
}
.insight-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 16px;
}
.insight-meta-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 10px 12px;
}
.meta-label {
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #4b5563;
    margin-bottom: 5px;
    display: flex;
    align-items: center;
    gap: 5px;
}
.meta-value {
    font-size: 0.82rem;
    color: #d1d5db;
    line-height: 1.4;
}
.meta-value-impact {
    font-size: 0.82rem;
    color: #34d399;
    line-height: 1.4;
    font-weight: 500;
}

/* ── PIE score ── */
.pie-container {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 14px 16px;
}
.pie-title {
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #4b5563;
    margin-bottom: 12px;
}
.pie-scores {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1.2fr;
    gap: 8px;
    align-items: end;
}
.pie-item {
    text-align: center;
}
.pie-label {
    font-size: 0.62rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 5px;
}
.pie-bar-wrap {
    height: 48px;
    background: rgba(255,255,255,0.04);
    border-radius: 4px;
    display: flex;
    align-items: flex-end;
    overflow: hidden;
    margin-bottom: 5px;
}
.pie-bar {
    width: 100%;
    border-radius: 4px 4px 0 0;
    transition: height 0.3s ease;
}
.pie-bar-p { background: linear-gradient(180deg, #a78bfa, #7c3aed); }
.pie-bar-i { background: linear-gradient(180deg, #38bdf8, #0284c7); }
.pie-bar-e { background: linear-gradient(180deg, #34d399, #059669); }
.pie-bar-t { background: linear-gradient(180deg, #fbbf24, #d97706); }
.pie-num {
    font-family: 'Syne', sans-serif;
    font-size: 0.9rem;
    font-weight: 700;
    color: #f3f4f6;
}
.pie-total-num {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 800;
    color: #fbbf24;
}

/* ── divider ── */
hr {
    border: none !important;
    border-top: 1px solid rgba(255,255,255,0.05) !important;
    margin: 2.5rem 0 1rem 0 !important;
}
.footer {
    font-size: 0.72rem;
    color: #374151;
    letter-spacing: 0.04em;
    padding-bottom: 2rem;
}

/* ── spinner ── */
div[data-testid="stSpinner"] {
    color: #a78bfa !important;
}
</style>
""", unsafe_allow_html=True)

# ── session state ─────────────────────────────────────────────────────────────
if "query_text"    not in st.session_state: st.session_state["query_text"]    = ""
if "results"       not in st.session_state: st.session_state["results"]       = None
if "pending_sample" not in st.session_state: st.session_state["pending_sample"] = None

if st.session_state["pending_sample"]:
    st.session_state["query_text"]    = st.session_state["pending_sample"]
    st.session_state["pending_sample"] = None
    st.session_state["results"]       = None

# ── hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <p class="hero-eyebrow">⚡ CRO Insight Engine</p>
  <h1 class="hero-title">Turn drop-offs into conversions</h1>
  <p class="hero-sub">Paste your CRO problem. Get 3 research-backed insights with hypothesis, evidence, impact, and PIE scores — in seconds.</p>
</div>
<div class="pill-row">
  <span class="pill">BFSI</span>
  <span class="pill">Forms</span>
  <span class="pill">Landing Pages</span>
  <span class="pill">Paid Ads</span>
  <span class="pill">Mobile UX</span>
  <span class="pill">Trust & Social Proof</span>
</div>
""", unsafe_allow_html=True)

# ── sample queries ────────────────────────────────────────────────────────────
SAMPLE_QUERIES = [
    "Why are users dropping off on our insurance quote form?",
    "How to improve loan landing page for paid traffic?",
    "Mobile form completions are low on our credit card page",
    "High bounce rate on BFSI page from Google Ads",
    "Drop-off at KYC document upload step",
    "What CTA copy works best for a mutual fund SIP page?",
]

st.markdown('<p class="section-label">Quick prompts</p>', unsafe_allow_html=True)
cols = st.columns(2)
for i, sample in enumerate(SAMPLE_QUERIES):
    if cols[i % 2].button(sample, key=f"s_{i}", use_container_width=True):
        st.session_state["pending_sample"] = sample
        st.rerun()

st.markdown("<div style='margin-top:1.4rem'></div>", unsafe_allow_html=True)

# ── input ─────────────────────────────────────────────────────────────────────
query = st.text_area(
    "Your CRO problem",
    value=st.session_state["query_text"],
    height=110,
    placeholder="e.g. Users abandon our insurance form at the income field. We see 60% drop-off on mobile…",
)
st.session_state["query_text"] = query

col1, col2 = st.columns([5, 1])
with col1:
    analyse = st.button("⚡ Analyse Problem", type="primary", use_container_width=True)
with col2:
    if st.button("Clear", use_container_width=True):
        st.session_state["query_text"] = ""
        st.session_state["results"]    = None
        st.rerun()

# ── analyse ───────────────────────────────────────────────────────────────────
if analyse:
    clean = query.strip()
    if not clean:
        st.warning("Please enter a problem or pick a quick prompt above.")
    else:
        st.session_state["query_text"] = clean
        with st.spinner("Analysing problem and retrieving insights…"):
            try:
                resp = requests.post(
                    f"{API_URL}/analyze",
                    json={"query": clean},
                    timeout=60,
                )
                resp.raise_for_status()
                st.session_state["results"] = resp.json()
            except requests.exceptions.ConnectionError:
                st.error("Cannot reach backend. Run: uvicorn main:app --reload")
                st.stop()
            except requests.exceptions.Timeout:
                st.error("Request timed out — server may be waking up. Try again in 15 seconds.")
                st.stop()
            except Exception as e:
                st.error(f"Error: {e}")
                st.stop()

# ── results ───────────────────────────────────────────────────────────────────
if st.session_state["results"]:
    data            = st.session_state["results"]
    focus           = data.get("focus_area", "general")
    conf            = data.get("confidence", "medium")
    insights        = data.get("insights", [])
    problem_summary = data.get("problem_summary", "")

    if problem_summary:
        st.markdown(f"""
<div class="problem-banner">
  <strong>Problem Analysis</strong>
  {problem_summary}
</div>""", unsafe_allow_html=True)

    conf_class = {"high": "badge-high", "medium": "badge-medium", "low": "badge-low"}.get(conf, "badge-medium")
    st.markdown(f"""
<div class="badge-row">
  <span class="badge badge-focus">{focus.replace("_", " ")}</span>
  <span class="badge {conf_class}">{conf} confidence</span>
  <span class="badge" style="background:rgba(255,255,255,0.04);color:#6b7280;border:1px solid rgba(255,255,255,0.08)">{len(insights)} insights</span>
</div>""", unsafe_allow_html=True)

    for i, insight in enumerate(insights, 1):
        if not isinstance(insight, dict):
            continue

        action     = insight.get("action", "")
        hypothesis = insight.get("hypothesis", "")
        evidence   = insight.get("evidence", "")
        impact     = insight.get("impact", "")
        pie        = insight.get("pie", {})

        p     = pie.get("potential",  0)
        imp   = pie.get("importance", 0)
        e     = pie.get("ease",       0)
        total = pie.get("total",      0)

        p_h   = int((p   / 10) * 48)
        imp_h = int((imp / 10) * 48)
        e_h   = int((e   / 10) * 48)
        t_h   = int((total / 10) * 48)

        st.markdown(f"""
<div class="insight-card">
  <div class="insight-index">Insight {i} of {len(insights)}</div>
  <div class="insight-action">{action}</div>
  <div class="insight-hypothesis">{hypothesis}</div>

  <div class="insight-grid">
    <div class="insight-meta-box">
      <div class="meta-label">📊 Evidence</div>
      <div class="meta-value">{evidence}</div>
    </div>
    <div class="insight-meta-box">
      <div class="meta-label">🎯 Impact</div>
      <div class="meta-value-impact">{impact}</div>
    </div>
  </div>

  <div class="pie-container">
    <div class="pie-title">PIE Score</div>
    <div class="pie-scores">
      <div class="pie-item">
        <div class="pie-label">Potential</div>
        <div class="pie-bar-wrap"><div class="pie-bar pie-bar-p" style="height:{p_h}px"></div></div>
        <div class="pie-num">{p}</div>
      </div>
      <div class="pie-item">
        <div class="pie-label">Importance</div>
        <div class="pie-bar-wrap"><div class="pie-bar pie-bar-i" style="height:{imp_h}px"></div></div>
        <div class="pie-num">{imp}</div>
      </div>
      <div class="pie-item">
        <div class="pie-label">Ease</div>
        <div class="pie-bar-wrap"><div class="pie-bar pie-bar-e" style="height:{e_h}px"></div></div>
        <div class="pie-num">{e}</div>
      </div>
      <div class="pie-item">
        <div class="pie-label">Total</div>
        <div class="pie-bar-wrap"><div class="pie-bar pie-bar-t" style="height:{t_h}px"></div></div>
        <div class="pie-total-num">{total}</div>
      </div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

    if conf == "low":
        st.info("Low confidence — try adding more detail to your problem statement.")

st.markdown("<hr/>", unsafe_allow_html=True)
st.markdown('<p class="footer">Powered by RAG + GPT-4o-mini · Knowledge: Baymard · CXL · Nielsen Norman · VWO · Hotjar · Unbounce · McKinsey · Forrester · IRDAI</p>', unsafe_allow_html=True)
