import streamlit as st

def apply_custom_theme():
    """Injects custom CSS to style the dashboard with a premium dark-scientific theme."""
    st.markdown("""
        <style>
        /* Base background adjustment */
        .stApp {
            background-color: #0B0F19;
            color: #E2E8F0;
        }
        
        /* Hide default Streamlit top padding to use full space */
        .css-18e3th9 {
            padding-top: 2rem;
        }

        /* Card Container Styling */
        .metric-card {
            background-color: #111827;
            border: 1px solid #1E293B;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
            text-align: center;
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            height: 100%;
        }
        .metric-card:hover {
            transform: translateY(-2px);
            border-color: #00E5FF;
            box-shadow: 0 0 15px rgba(0, 229, 255, 0.15);
        }

        /* Section Headers */
        h1 {
            color: #F8FAFC;
            font-weight: 700;
            letter-spacing: -0.025em;
            margin-bottom: 0.5rem;
        }
        h2, h3 {
            color: #E2E8F0;
            font-weight: 600;
            letter-spacing: 0.025em;
            margin-top: 1.5rem;
        }
        
        /* Subtitle / Research Question */
        .research-q {
            color: #00E5FF;
            font-size: 1.2rem;
            font-weight: 500;
            font-style: italic;
            margin-bottom: 2rem;
            padding-left: 1rem;
            border-left: 4px solid #00E5FF;
        }
        
        /* Subtle Dividers */
        hr {
            border-color: #1E293B;
            margin-top: 2.5rem;
            margin-bottom: 2.5rem;
        }
        
        /* Sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #0F172A;
            border-right: 1px solid #1E293B;
        }
        
        /* Plotly background override */
        .js-plotly-plot .plotly .bg {
            fill: transparent !important;
        }
        </style>
    """, unsafe_allow_html=True)

def create_kpi_card(title: str, value: str, subtext: str = None, color: str = "#00E5FF"):
    """Generates HTML for a custom KPI card."""
    subtext_html = f'<div style="color: #64748B; font-size: 0.85rem; margin-top: 0.5rem;">{subtext}</div>' if subtext else ''
    
    html = f"""
    <div class="metric-card">
        <div style="color: #94A3B8; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; font-weight: 600;">{title}</div>
        <div style="color: {color}; font-size: 2.5rem; font-weight: 700; line-height: 1.2; text-shadow: 0 0 10px {color}40;">{value}</div>
        {subtext_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
