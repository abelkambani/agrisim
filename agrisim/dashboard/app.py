import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Ensure the package is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from agrisim.agent.irrigation_policy import ThresholdPolicy, AdaptivePolicy, NoIrrigationPolicy
from agrisim.analytics.experiment_runner import run_monte_carlo
from agrisim.analytics.statistical_summaries import summarize_monte_carlo, generate_comparative_summary
from agrisim.dashboard.theme import apply_custom_theme, create_kpi_card
from agrisim.dashboard.scenarios import get_scenario_config

# --- Page Setup & Theme ---
st.set_page_config(page_title="Agrisim Research", layout="wide", initial_sidebar_state="expanded")
apply_custom_theme()

# --- Header Section ---
st.markdown("<h1>Agrisim: Stochastic Agro-Ecological Modeler</h1>", unsafe_allow_html=True)
st.markdown('<div class="research-q">Research Question: How do stochastic rainfall patterns affect crop yield under adaptive irrigation policies?</div>', unsafe_allow_html=True)

# --- Sidebar Controls ---
st.sidebar.markdown("## Experiment Configuration")
scenario_choice = st.sidebar.radio(
    "Select Climate Scenario",
    ["🌵 Drought Scenario", "🌧️ Normal Climate", "🌾 Optimized Farming", "🔥 Extreme Heat Stress"]
)

st.sidebar.markdown("### Simulation Engine")
n_simulations = st.sidebar.slider("Monte Carlo Runs", 1, 50, 10, help="Number of independent runs per policy.")

st.sidebar.markdown("### Policy Parameters")
threshold = st.sidebar.slider("Irrigation Threshold (mm)", 10.0, 80.0, 40.0)
amount = st.sidebar.slider("Irrigation Amount (mm)", 5.0, 50.0, 20.0)

# --- Execution ---
# We run this immediately to populate the dashboard without a button for a seamless app feel
with st.spinner(f"Running Monte Carlo sweeps for {scenario_choice}..."):
    config = get_scenario_config(scenario_choice)
    config.irrigation_threshold = threshold
    config.irrigation_amount = amount
    
    policies = {
        "No Irrigation": NoIrrigationPolicy,
        "Threshold": ThresholdPolicy,
        "Adaptive": AdaptivePolicy
    }
    
    policy_raw_data = {}
    policy_summaries = {}
    
    for name, policy_class in policies.items():
        runs = run_monte_carlo(config, policy_class, n_simulations=n_simulations)
        policy_raw_data[name] = pd.concat(runs)
        policy_summaries[name] = summarize_monte_carlo(runs)
        
    comp_df = generate_comparative_summary(policy_summaries)

# --- KPI Section (Focusing on the Adaptive Policy as our primary result) ---
st.markdown("### Impact Analysis (Adaptive Policy)")
adaptive_summary = comp_df[comp_df['Policy'] == 'Adaptive'].iloc[0]
baseline_summary = comp_df[comp_df['Policy'] == 'No Irrigation'].iloc[0]

yield_delta = f"{((adaptive_summary['Mean Yield (kg/ha)'] / baseline_summary['Mean Yield (kg/ha)']) - 1) * 100:.1f}% vs baseline" if baseline_summary['Mean Yield (kg/ha)'] > 0 else "N/A"

col1, col2, col3, col4 = st.columns(4)
with col1:
    create_kpi_card("Mean Yield", f"{adaptive_summary['Mean Yield (kg/ha)']:,.0f} kg", yield_delta, color="#00E5FF")
with col2:
    create_kpi_card("Water Usage", f"{adaptive_summary['Mean Water Used (mm)']:,.0f} mm", "Mean applied water", color="#3B82F6")
with col3:
    # Let's pull average drought days from the raw data or summaries
    adaptive_df = policy_summaries['Adaptive']
    mean_drought = adaptive_df['drought_days'].mean()
    create_kpi_card("Drought Stress", f"{mean_drought:.0f} days", "Avg days in extreme drought", color="#F59E0B")
with col4:
    # Efficiency Score = Yield / Water
    efficiency = adaptive_summary['Mean Yield (kg/ha)'] / adaptive_summary['Mean Water Used (mm)'] if adaptive_summary['Mean Water Used (mm)'] > 0 else 0
    create_kpi_card("Efficiency Score", f"{efficiency:.1f}", "Yield (kg) per mm water", color="#10B981")

st.markdown("<hr>", unsafe_allow_html=True)

# --- Narrative Flow Visualizations ---

# 1. Plotly Timeline for Climate & Moisture
st.markdown("### 1. Environmental Driver: Climate & Soil Response")
st.markdown("Showing a single trajectory from the Adaptive policy to illustrate hidden Markov states driving soil depletion.")

# Get Run 0 from Adaptive
run_0 = policy_raw_data['Adaptive'][policy_raw_data['Adaptive']['run_id'] == 0]

fig1 = go.Figure()
# Add Moisture
fig1.add_trace(go.Scatter(x=run_0['timestep'], y=run_0['soil_moisture'], mode='lines', name='Soil Moisture (mm)', line=dict(color='#00E5FF', width=2)))
# Add Rainfall as bars on secondary axis
fig1.add_trace(go.Bar(x=run_0['timestep'], y=run_0['rainfall'], name='Rainfall (mm)', marker_color='rgba(59, 130, 246, 0.5)', yaxis='y2'))

# Layout for dual axis and dark theme
fig1.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#E2E8F0'),
    xaxis=dict(title='Timestep (Days)', showgrid=True, gridcolor='#1E293B'),
    yaxis=dict(title='Moisture (mm)', showgrid=True, gridcolor='#1E293B'),
    yaxis2=dict(title='Rainfall (mm)', overlaying='y', side='right', showgrid=False),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=0, r=0, t=30, b=0),
    hovermode="x unified"
)
st.plotly_chart(fig1, use_container_width=True)


col_left, col_right = st.columns([1, 1])

# 2. Plotly Phase Plot
with col_left:
    st.markdown("### 2. Biological Attractor: Crop vs. Pests")
    st.markdown("Lotka-Volterra dynamics across all Monte Carlo runs. The attractor shifts based on climate stress.")
    
    fig2 = go.Figure()
    colors = {"No Irrigation": "#EF4444", "Threshold": "#F59E0B", "Adaptive": "#10B981"}
    
    for name, df in policy_raw_data.items():
        # Plot run 0 for clarity
        df_sub = df[df['run_id'] == 0]
        fig2.add_trace(go.Scatter(
            x=df_sub['crop_biomass'], 
            y=df_sub['pest_population'], 
            mode='lines', 
            name=name,
            line=dict(color=colors[name], width=2)
        ))
        
    fig2.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0'),
        xaxis=dict(title='Crop Biomass (kg/ha)', showgrid=True, gridcolor='#1E293B'),
        yaxis=dict(title='Pest Population', showgrid=True, gridcolor='#1E293B'),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig2, use_container_width=True)

# 3. Yield Distribution
with col_right:
    st.markdown("### 3. Intervention Outcome: Yield Distributions")
    st.markdown("Yield variance caused by stochastic weather, mitigated by the chosen policy.")
    
    # Combine summaries for plotly boxplot
    all_summaries = []
    for name, df in policy_summaries.items():
        df['Policy'] = name
        all_summaries.append(df)
    combined_summary = pd.concat(all_summaries)
    
    fig3 = px.box(
        combined_summary, x="Policy", y="final_yield", color="Policy",
        color_discrete_map={"No Irrigation": "#EF4444", "Threshold": "#F59E0B", "Adaptive": "#10B981"}
    )
    
    fig3.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E2E8F0'),
        xaxis=dict(title='', showgrid=False),
        yaxis=dict(title='Final Yield (kg/ha)', showgrid=True, gridcolor='#1E293B'),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)

# --- Data & Export Section ---
st.markdown("### Statistical Data & Export")
st.dataframe(
    comp_df.round(2),
    use_container_width=True
)

csv = comp_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Research Summary (CSV)",
    data=csv,
    file_name='policy_comparison.csv',
    mime='text/csv',
)
