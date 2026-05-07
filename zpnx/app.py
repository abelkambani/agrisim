"""
🇿🇼 ZimNova Pulse Nexus (ZPNX)
Heritage-Based AI Decision System for Lithium Beneficiation,
Predictive Financing, and Community Industrialisation.
"""
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from engine import (predict_output, run_monte_carlo, calculate_entropy,
                    predict_yield, compute_credit_score, generate_decision)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE CONFIG & CUSTOM CSS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(page_title="ZPNX — ZimNova Pulse Nexus",
                   page_icon="🇿🇼", layout="wide",
                   initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
:root{--bg:#0E1117;--gold:#D4AF37;--surface:#161B22;--border:#21262D;
      --text:#E6EDF3;--muted:#8B949E;--green:#2EA043;--red:#DA3633;--amber:#D29922;}
html,body,[data-testid="stAppViewContainer"]{background:var(--bg);color:var(--text);
    font-family:'Inter',sans-serif;}
[data-testid="stSidebar"]{display:none;}
.block-container{padding:1rem 2rem 2rem 2rem;max-width:100%;}
h1,h2,h3{font-family:'Inter',sans-serif;font-weight:600;letter-spacing:-0.02em;}
/* Gold accent for critical signals */
.gold{color:var(--gold);font-weight:600;}
.tag{display:inline-block;padding:2px 10px;border-radius:12px;font-size:.75rem;
     font-weight:600;letter-spacing:.04em;}
.tag-high{background:#2EA04322;color:var(--green);}
.tag-med{background:#D2992222;color:var(--amber);}
.tag-low{background:#DA363322;color:var(--red);}
.tag-approved{background:#2EA04333;color:var(--green);font-size:.85rem;}
.tag-conditional{background:#D2992233;color:var(--amber);font-size:.85rem;}
.tag-rejected{background:#DA363333;color:var(--red);font-size:.85rem;}
/* Decision card */
.dec-card{background:var(--surface);border-left:3px solid var(--gold);
          padding:14px 18px;margin:8px 0;border-radius:0 6px 6px 0;}
/* Flow bar */
.flow{display:flex;align-items:center;gap:6px;flex-wrap:wrap;
      font-size:.8rem;color:var(--muted);margin:10px 0;}
.flow span{background:var(--surface);padding:4px 12px;border-radius:4px;
           color:var(--text);font-weight:500;}
.flow .arrow{background:none;color:var(--gold);font-weight:700;font-size:1rem;}
/* Section divider */
.divider{border-top:1px solid var(--border);margin:20px 0 14px 0;}
/* Stat */
.stat-label{color:var(--muted);font-size:.75rem;text-transform:uppercase;
            letter-spacing:.06em;margin-bottom:2px;}
.stat-value{font-size:1.5rem;font-weight:700;letter-spacing:-0.02em;}
/* Remove streamlit defaults */
[data-testid="stHeader"]{background:transparent;}
footer{display:none;}
div[data-testid="stDecoration"]{display:none;}
</style>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HEADER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("## 🇿🇼 ZimNova Pulse Nexus")
st.caption("Heritage-Based AI Decision System · INPUT → MODEL → SIMULATION → CONFIDENCE → DECISION")

# System flow bar
st.markdown("""
<div class="flow">
<span>INPUT</span><span class="arrow">→</span>
<span>MODEL</span><span class="arrow">→</span>
<span>SIMULATION</span><span class="arrow">→</span>
<span>CONFIDENCE</span><span class="arrow">→</span>
<span class="gold">DECISION</span>
</div>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# MODULE TABS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tab_li, tab_ag = st.tabs(["⛏️  Lithium Intelligence — Bikita Model",
                           "🌾  Agricultural Credit Engine"])

# ╔══════════════════════════════════════════════════════════════════╗
# ║  TAB 1 — LITHIUM INTELLIGENCE                                  ║
# ╚══════════════════════════════════════════════════════════════════╝
with tab_li:
    left, right = st.columns([1, 2], gap="large")

    # ── LEFT: CONTROL PANEL ──────────────────────────────────────
    with left:
        st.markdown("#### Control Panel")

        # Demo mode
        demo = st.button("⚡ Run Full Simulation", use_container_width=True)
        if demo:
            st.session_state["li_grade"] = 3.2
            st.session_state["li_vol"] = 12000.0
            st.session_state["li_price"] = 42000.0

        ore_grade = st.slider("Ore Grade (%)", 1.0, 5.0,
                              st.session_state.get("li_grade", 2.5),
                              0.1, key="ore_grade_sl",
                              help="Spodumene Li₂O concentration")
        extraction_vol = st.number_input(
            "Extraction Volume (tonnes)", 1000, 50000,
            int(st.session_state.get("li_vol", 8000)), 500,
            key="ext_vol_in")
        market_price = st.number_input(
            "Market Price ($/tonne)", 5000, 100000,
            int(st.session_state.get("li_price", 35000)), 1000,
            key="mkt_price_in")

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Cause trace
        with st.expander("🔍 Cause → Effect Trace"):
            eff = 0.60 + (ore_grade - 1.0) * (0.30 / 4.0)
            st.markdown(f"""
- **Ore Grade {ore_grade}%** → Efficiency factor **{eff:.3f}**
- Extraction {extraction_vol:,}t × {ore_grade}% × {eff:.3f} = predicted output
- Uncertainty CV: **{0.25 - (ore_grade-1.0)*(0.10/4.0):.0%}** (lower grade = more noise)
""")

    # ── RIGHT: MODEL OUTPUT ──────────────────────────────────────
    with right:
        # 1. PREDICT
        pred = predict_output(ore_grade, extraction_vol)
        predicted = pred["predicted_tonnes"]

        # 2. SIMULATE
        mc = run_monte_carlo(predicted, ore_grade)
        p10 = float(np.percentile(mc, 10))
        p50 = float(np.percentile(mc, 50))
        p90 = float(np.percentile(mc, 90))

        # 3. CONFIDENCE
        conf = calculate_entropy(mc)

        # Headline metrics
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f'<div class="stat-label">Output Range</div>'
                        f'<div class="stat-value">{p10:,.0f}–{p90:,.0f} t</div>',
                        unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="stat-label">P50 (Median)</div>'
                        f'<div class="stat-value">{p50:,.0f} t</div>',
                        unsafe_allow_html=True)
        with c3:
            tag_cls = {"HIGH":"tag-high","MEDIUM":"tag-med","LOW":"tag-low"}[conf["classification"]]
            st.markdown(f'<div class="stat-label">Confidence</div>'
                        f'<div class="stat-value">{conf["score"]:.2f} '
                        f'<span class="tag {tag_cls}">{conf["classification"]}</span></div>',
                        unsafe_allow_html=True)
        with c4:
            rev = p50 * market_price
            st.markdown(f'<div class="stat-label">Est. Revenue (P50)</div>'
                        f'<div class="stat-value gold">${rev:,.0f}</div>',
                        unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Monte Carlo histogram
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=mc, nbinsx=60, marker_color="#D4AF37", opacity=0.85,
            name="Simulated Output"))
        for pval, lbl, clr in [(p10,"P10","#DA3633"),(p50,"P50","#E6EDF3"),(p90,"P90","#2EA043")]:
            fig.add_vline(x=pval, line_dash="dash", line_color=clr, line_width=1.5,
                          annotation_text=f"{lbl}: {pval:,.0f}t",
                          annotation_font_color=clr, annotation_font_size=11)
        fig.update_layout(
            template="plotly_dark", paper_bgcolor="#0E1117", plot_bgcolor="#0E1117",
            title="Monte Carlo Distribution (10,000 iterations)",
            xaxis_title="Output (tonnes)", yaxis_title="Frequency",
            height=340, margin=dict(l=40,r=20,t=50,b=40),
            showlegend=False, font=dict(family="Inter"))
        st.plotly_chart(fig, use_container_width=True)

        # Risk profile expander
        with st.expander("📊 Risk Profile Details"):
            rc1, rc2, rc3 = st.columns(3)
            rc1.metric("P10 (Downside)", f"{p10:,.0f} t")
            rc2.metric("P50 (Base)", f"{p50:,.0f} t")
            rc3.metric("P90 (Upside)", f"{p90:,.0f} t")
            spread = (p90 - p10) / predicted if predicted > 0 else 0
            st.markdown(f"**Spread ratio:** {spread:.2%} — "
                        f"{'Tight ✓' if spread < 0.5 else 'Wide ⚠️'}")
            st.markdown(f"**Shannon Entropy:** {conf['raw_entropy']:.4f} bits")

    # ── BOTTOM: DECISION ENGINE ──────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("#### 🧠 Decision Engine")

    recs, token_ok, spread_val = generate_decision(mc, conf, predicted, market_price)
    for icon, text in recs:
        st.markdown(f'<div class="dec-card">{icon} &nbsp; {text}</div>',
                    unsafe_allow_html=True)

    # Tokenisation flow
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("##### 🪙 Tokenisation Pipeline")
    tok_color = "var(--green)" if token_ok else "var(--red)"
    tok_label = "ELIGIBLE" if token_ok else "NOT ELIGIBLE"
    st.markdown(f"""
<div class="flow">
<span>Deposit</span><span class="arrow">→</span>
<span>Prediction ({predicted:,.0f}t)</span><span class="arrow">→</span>
<span>Risk (spread {spread_val:.1%})</span><span class="arrow">→</span>
<span>Confidence ({conf['score']:.2f})</span><span class="arrow">→</span>
<span style="color:{tok_color};border:1px solid {tok_color}">{tok_label}</span>
</div>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════╗
# ║  TAB 2 — AGRICULTURAL CREDIT ENGINE                            ║
# ╚══════════════════════════════════════════════════════════════════╝
with tab_ag:
    left2, right2 = st.columns([1, 2], gap="large")

    with left2:
        st.markdown("#### Control Panel — Agriculture")

        demo2 = st.button("⚡ Run Credit Simulation", use_container_width=True)
        if demo2:
            st.session_state["ag_rain"] = 72.0
            st.session_state["ag_soil"] = 65.0
            st.session_state["ag_hist"] = 58.0

        rainfall = st.slider("Rainfall Index", 0.0, 100.0,
                              st.session_state.get("ag_rain", 55.0), 1.0,
                              help="Seasonal rainfall adequacy (0=drought, 100=optimal)")
        soil_q = st.slider("Soil Quality Index", 0.0, 100.0,
                            st.session_state.get("ag_soil", 50.0), 1.0)
        hist_yield = st.slider("Historical Yield Index", 0.0, 100.0,
                                st.session_state.get("ag_hist", 45.0), 1.0)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        with st.expander("🔍 Cause → Effect Trace"):
            st.markdown(f"""
- Rainfall ({rainfall:.0f}) × **0.40** = {rainfall*0.40:.1f}
- Soil ({soil_q:.0f}) × **0.35** = {soil_q*0.35:.1f}
- Historical ({hist_yield:.0f}) × **0.25** = {hist_yield*0.25:.1f}
- **Predicted Yield Index** = {rainfall*0.40+soil_q*0.35+hist_yield*0.25:.1f}
""")

    with right2:
        # Borrow lithium confidence for cross-module decision
        if "ore_grade_sl" not in st.session_state:
            # Standalone ag: run a quick entropy from synthetic data
            ag_conf_score = 0.65
            ag_conf_class = "MEDIUM"
        else:
            ag_conf_score = conf["score"]
            ag_conf_class = conf["classification"]

        py = predict_yield(rainfall, soil_q, hist_yield)

        # Risk factor derived from inverse of input quality
        avg_input = (rainfall + soil_q + hist_yield) / 3
        risk_factor = max(1.0, 3.0 - (avg_input / 50.0))

        credit = compute_credit_score(py, ag_conf_score, risk_factor)

        # Display
        ac1, ac2, ac3 = st.columns(3)
        with ac1:
            st.markdown(f'<div class="stat-label">Predicted Yield Index</div>'
                        f'<div class="stat-value">{py:.1f}</div>',
                        unsafe_allow_html=True)
        with ac2:
            st.markdown(f'<div class="stat-label">Risk Factor</div>'
                        f'<div class="stat-value">{risk_factor:.2f}</div>',
                        unsafe_allow_html=True)
        with ac3:
            dec_cls = {"APPROVED":"tag-approved","CONDITIONAL":"tag-conditional",
                       "REJECTED":"tag-rejected"}[credit["decision"]]
            st.markdown(f'<div class="stat-label">Credit Score</div>'
                        f'<div class="stat-value">{credit["score"]:.0f} '
                        f'<span class="tag {dec_cls}">{credit["decision"]}</span></div>',
                        unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # Credit sensitivity chart
        rain_range = np.linspace(10, 100, 50)
        scores = []
        for r in rain_range:
            y = predict_yield(r, soil_q, hist_yield)
            avg = (r + soil_q + hist_yield) / 3
            rf = max(1.0, 3.0 - (avg / 50.0))
            scores.append(compute_credit_score(y, ag_conf_score, rf)["score"])

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=rain_range, y=scores, mode="lines",
            line=dict(color="#D4AF37", width=2.5), name="Credit Score"))
        fig2.add_hline(y=65, line_dash="dash", line_color="#2EA043",
                       annotation_text="Approved threshold",
                       annotation_font_color="#2EA043")
        fig2.add_hline(y=40, line_dash="dash", line_color="#D29922",
                       annotation_text="Conditional threshold",
                       annotation_font_color="#D29922")
        fig2.add_vline(x=rainfall, line_dash="dot", line_color="#E6EDF3",
                       annotation_text="Current",
                       annotation_font_color="#E6EDF3")
        fig2.update_layout(
            template="plotly_dark", paper_bgcolor="#0E1117", plot_bgcolor="#0E1117",
            title="Credit Score Sensitivity to Rainfall",
            xaxis_title="Rainfall Index", yaxis_title="Credit Score",
            height=320, margin=dict(l=40,r=20,t=50,b=40),
            showlegend=False, font=dict(family="Inter"))
        st.plotly_chart(fig2, use_container_width=True)

    # ── BOTTOM: AG DECISION ENGINE ───────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("#### 🧠 Agricultural Decision Engine")

    ag_recs = []
    if credit["decision"] == "APPROVED":
        ag_recs.append(("✅", f"Credit score {credit['score']:.0f}/100 — "
                        "Approve financing. Low risk of default based on "
                        "predicted yield and data confidence."))
    elif credit["decision"] == "CONDITIONAL":
        ag_recs.append(("⚠️", f"Credit score {credit['score']:.0f}/100 — "
                        "Conditional approval. Require collateral or "
                        "partial disbursement with milestone review."))
    else:
        ag_recs.append(("🛑", f"Credit score {credit['score']:.0f}/100 — "
                        "Reject financing application. Yield prediction "
                        "and/or data confidence too low."))

    if ag_conf_class == "LOW":
        ag_recs.append(("📉", "Data confidence LOW — Recommend delaying "
                        "credit decision until sensor/rainfall data improves."))
    if risk_factor > 2.0:
        ag_recs.append(("🌧️", f"Risk factor {risk_factor:.2f} is elevated — "
                        "Agricultural inputs are weak. Advise irrigation "
                        "investment before next cycle."))

    for icon, text in ag_recs:
        st.markdown(f'<div class="dec-card">{icon} &nbsp; {text}</div>',
                    unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FOOTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.caption("ZPNX v1.0 · ZimNova Pulse Nexus · 21dev-first Decision Architecture · "
           "Built for Zimbabwe's mineral-industrial sovereignty")
