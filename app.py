import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Page Config
st.set_page_config(
    page_title="📊 AI Impact Dashboard — BNSP Data Analyst",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS design
st.markdown("""
<style>
    /* ---------- Import Google Fonts ---------- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ---------- Global ---------- */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* ---------- Sidebar (Light Theme) ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f7ff 0%, #eef2ff 50%, #f8f7ff 100%);
        border-right: 1px solid rgba(99, 102, 241, 0.15);
    }
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #4338ca !important;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown label {
        color: #475569 !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(99, 102, 241, 0.15) !important;
    }

    /* ---------- Sidebar Multiselect Tags ---------- */
    section[data-testid="stSidebar"] span[data-baseweb="tag"] {
        background-color: #818cf8 !important;
        border: 1px solid #6366f1 !important;
        color: #ffffff !important;
        border-radius: 8px !important;
    }
    section[data-testid="stSidebar"] span[data-baseweb="tag"] span {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] span[data-baseweb="tag"] svg {
        fill: #e0e7ff !important;
    }
    section[data-testid="stSidebar"] span[data-baseweb="tag"]:hover {
        background-color: #6366f1 !important;
        border-color: #4f46e5 !important;
    }

    /* ---------- Sidebar Inputs / Dropdowns ---------- */
    section[data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-color: #c7d2fe !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="select"] > div:hover {
        border-color: #818cf8 !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="select"] > div:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 1px rgba(99, 102, 241, 0.25) !important;
    }
    section[data-testid="stSidebar"] [data-baseweb="icon"] svg {
        fill: #6366f1 !important;
    }

    /* ---------- KPI Cards ---------- */
    .kpi-container {
        display: flex;
        gap: 16px;
        flex-wrap: wrap;
        margin-bottom: 24px;
    }
    .kpi-card {
        flex: 1;
        min-width: 200px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.12) 0%, rgba(139, 92, 246, 0.08) 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        border-color: rgba(99, 102, 241, 0.5);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15);
    }
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
        margin-bottom: 4px;
    }
    .kpi-label {
        font-size: 0.85rem;
        font-weight: 500;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .kpi-delta-up {
        color: #34d399;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .kpi-delta-down {
        color: #f87171;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* ---------- Section Headers ---------- */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #e2e8f0;
        margin: 32px 0 8px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(99, 102, 241, 0.3);
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .section-subtitle {
        font-size: 0.9rem;
        color: #94a3b8;
        margin-bottom: 20px;
        line-height: 1.5;
    }

    /* ---------- Dashboard Title ---------- */
    .dashboard-title {
        text-align: center;
        padding: 20px 0 10px 0;
    }
    .dashboard-title h1 {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #818cf8, #c084fc, #f0abfc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }
    .dashboard-title p {
        color: #94a3b8;
        font-size: 0.95rem;
    }

    /* ---------- Info Box ---------- */
    .info-box {
        background: rgba(99, 102, 241, 0.08);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 12px;
        padding: 16px 20px;
        color: #cbd5e1;
        font-size: 0.9rem;
        margin-bottom: 16px;
    }

    /* ---------- Hide Streamlit Defaults ---------- */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* ---------- Tab Styling ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 600;
    }

    /* ---------- Plotly Chart Containers ---------- */
    .stPlotlyChart {
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)


# Data Loading
@st.cache_data
def load_data():
    """Load and preprocess the dataset."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'ai_student_impact_dataset (1) (1).csv')
    df = pd.read_csv(csv_path)

    # --- Data Cleaning (mirror analisis_ai_impact.py) ---
    valid_years = ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate']
    df = df[df['Year_of_Study'].isin(valid_years)]
    df['Pre_Semester_GPA'] = df['Pre_Semester_GPA'].clip(0, 4.0)
    df['Post_Semester_GPA'] = df['Post_Semester_GPA'].clip(0, 4.0)
    df['Tool_Diversity'] = df['Tool_Diversity'].clip(1, 5)
    df['Skill_Retention_Score'] = df['Skill_Retention_Score'].clip(0, 100)
    df['Weekly_GenAI_Hours'] = df['Weekly_GenAI_Hours'].clip(lower=0)
    df['Traditional_Study_Hours'] = df['Traditional_Study_Hours'].clip(lower=0)

    if df['Paid_Subscription'].dtype == 'object':
        df['Paid_Subscription'] = df['Paid_Subscription'].map({'True': True, 'False': False})

    # --- Derived Columns ---
    df['AI_Usage_Segment'] = pd.cut(
        df['Weekly_GenAI_Hours'],
        bins=[-0.01, 5, 15, df['Weekly_GenAI_Hours'].max() + 1],
        labels=['Light (0–5 jam)', 'Moderate (5–15 jam)', 'Heavy (>15 jam)']
    )
    df['GPA_Change'] = df['Post_Semester_GPA'] - df['Pre_Semester_GPA']

    return df


df_raw = load_data()

COLORS = {
    'primary': '#818cf8',
    'secondary': '#c084fc',
    'accent': '#f0abfc',
    'success': '#34d399',
    'warning': '#fbbf24',
    'danger': '#f87171',
    'bg': '#0e1117',
    'card_bg': '#1a1a2e',
    'text': '#e2e8f0',
    'muted': '#94a3b8',
    'grid': 'rgba(148, 163, 184, 0.08)',
}

PALETTE = ['#818cf8', '#c084fc', '#f0abfc', '#34d399', '#fbbf24', '#f87171',
           '#38bdf8', '#fb923c', '#a3e635', '#e879f9']

BURNOUT_COLORS = {'Low': '#34d399', 'Medium': '#fbbf24', 'High': '#f87171'}
POLICY_COLORS = {'Actively_Encouraged': '#34d399', 'Allowed_With_Citation': '#818cf8', 'Strict_Ban': '#f87171'}
SEGMENT_COLORS = {'Light (0–5 jam)': '#34d399', 'Moderate (5–15 jam)': '#fbbf24', 'Heavy (>15 jam)': '#f87171'}


def plotly_layout(title="", height=450, showlegend=True):
    return dict(
        title=dict(text=title, font=dict(size=16, color=COLORS['text'], family='Inter')),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', color=COLORS['text'], size=12),
        height=height,
        margin=dict(l=60, r=30, t=60, b=60),
        showlegend=showlegend,
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLORS['muted'], size=11),
        ),
        xaxis=dict(
            gridcolor=COLORS['grid'],
            zerolinecolor=COLORS['grid'],
        ),
        yaxis=dict(
            gridcolor=COLORS['grid'],
            zerolinecolor=COLORS['grid'],
        ),
    )


# Sidebar Streamlit
with st.sidebar:
    st.markdown("## 🎛️ Filter Dashboard")
    st.markdown("---")

    # Major Category
    all_majors = sorted(df_raw['Major_Category'].unique())
    selected_majors = st.multiselect(
        "🎓 Bidang Studi (Major)",
        options=all_majors,
        default=all_majors,
        help="Pilih satu atau lebih bidang studi"
    )

    st.markdown("")

    # Year of Study
    year_order = ['Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate']
    all_years = [y for y in year_order if y in df_raw['Year_of_Study'].unique()]
    selected_years = st.multiselect(
        "📚 Jenjang (Year of Study)",
        options=all_years,
        default=all_years,
        help="Pilih satu atau lebih jenjang"
    )

    st.markdown("")

    # Institutional Policy
    all_policies = sorted(df_raw['Institutional_Policy'].unique())
    selected_policies = st.multiselect(
        "🏛️ Kebijakan Institusi",
        options=all_policies,
        default=all_policies,
        help="Pilih satu atau lebih kebijakan"
    )

    st.markdown("---")

    # Data Summary
    df = df_raw[
        (df_raw['Major_Category'].isin(selected_majors)) &
        (df_raw['Year_of_Study'].isin(selected_years)) &
        (df_raw['Institutional_Policy'].isin(selected_policies))
    ].copy()

    st.markdown(f"""
    <div class="info-box">
        📊 <strong>Data Terfilter</strong><br/>
        <span style="font-size:1.3rem;font-weight:700;color:#818cf8;">{len(df):,}</span>
        dari {len(df_raw):,} mahasiswa
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;color:#64748b;font-size:0.75rem;">
        BNSP Data Analyst Certification<br/>
        Dashboard BI — Modul 6<br/>
        © 2024
    </div>
    """, unsafe_allow_html=True)
if len(df) == 0:
    st.warning("⚠️ Tidak ada data yang sesuai filter. Silakan ubah pilihan filter di sidebar.")
    st.stop()


# Header
st.markdown("""
<div class="dashboard-title">
    <h1>🎓 AI Impact on Students Dashboard</h1>
    <p>Analisis Dampak Penggunaan AI Generatif terhadap Performa Akademik & Kesejahteraan Mahasiswa</p>
</div>
""", unsafe_allow_html=True)


# KPI 
avg_gpa = df['Post_Semester_GPA'].mean()
avg_retention = df['Skill_Retention_Score'].mean()
high_burnout_pct = (df['Burnout_Risk_Level'] == 'High').sum() / len(df) * 100
avg_ai_hours = df['Weekly_GenAI_Hours'].mean()
gpa_delta = df['GPA_Change'].mean()

kpi_delta_class = "kpi-delta-up" if gpa_delta >= 0 else "kpi-delta-down"
kpi_delta_arrow = "▲" if gpa_delta >= 0 else "▼"

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-value">{avg_gpa:.2f}</div>
        <div class="kpi-label">Rata-rata GPA</div>
        <div class="{kpi_delta_class}">{kpi_delta_arrow} {abs(gpa_delta):.3f} vs Pre-GPA</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{avg_retention:.1f}</div>
        <div class="kpi-label">Rata-rata Skill Retention</div>
        <div class="kpi-delta-up">Skor /100</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{high_burnout_pct:.1f}%</div>
        <div class="kpi-label">High Burnout Risk</div>
        <div class="{'kpi-delta-down' if high_burnout_pct > 30 else 'kpi-delta-up'}">
            {'⚠️ Perlu perhatian' if high_burnout_pct > 30 else '✅ Terkendali'}
        </div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{avg_ai_hours:.1f}h</div>
        <div class="kpi-label">Rata-rata AI Hours/Week</div>
        <div class="kpi-delta-up">Jam per minggu</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">{len(df):,}</div>
        <div class="kpi-label">Total Mahasiswa</div>
        <div class="kpi-delta-up">Data terfilter</div>
    </div>
</div>
""", unsafe_allow_html=True)


# Main 
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Overview",
    "🤖 Dampak AI",
    "🧠 Kesehatan Mental",
    "📖 Retensi Pengetahuan",
    "⚠️ Profil Risiko"
])


# TAB 1: OVERVIEW
with tab1:
    st.markdown('<div class="section-header">📋 Overview — Distribusi Mahasiswa</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Distribusi mahasiswa berdasarkan bidang studi, jenjang pendidikan, dan kebijakan institusi.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # --- 1a. Distribusi per Bidang Studi ---
    with col1:
        major_counts = df['Major_Category'].value_counts().reset_index()
        major_counts.columns = ['Major', 'Count']
        fig_major = px.bar(
            major_counts, x='Major', y='Count',
            color='Major', color_discrete_sequence=PALETTE,
            text='Count'
        )
        fig_major.update_traces(
            texttemplate='%{text:,}', textposition='outside',
            marker_line_width=0,
        )
        fig_major.update_layout(**plotly_layout("Distribusi per Bidang Studi", showlegend=False))
        fig_major.update_xaxes(title_text="")
        fig_major.update_yaxes(title_text="Jumlah Mahasiswa")
        st.plotly_chart(fig_major, use_container_width=True)

    # --- 1b. Distribusi per Jenjang ---
    with col2:
        year_counts = df['Year_of_Study'].value_counts().reindex(
            [y for y in year_order if y in df['Year_of_Study'].unique()]
        ).reset_index()
        year_counts.columns = ['Year', 'Count']
        fig_year = px.bar(
            year_counts, x='Year', y='Count',
            color='Year', color_discrete_sequence=PALETTE[3:],
            text='Count'
        )
        fig_year.update_traces(
            texttemplate='%{text:,}', textposition='outside',
            marker_line_width=0,
        )
        fig_year.update_layout(**plotly_layout("Distribusi per Jenjang Pendidikan", showlegend=False))
        fig_year.update_xaxes(title_text="")
        fig_year.update_yaxes(title_text="Jumlah Mahasiswa")
        st.plotly_chart(fig_year, use_container_width=True)

    # --- 1c. Distribusi per Kebijakan Institusi (Donut) ---
    col3, col4 = st.columns(2)

    with col3:
        policy_counts = df['Institutional_Policy'].value_counts().reset_index()
        policy_counts.columns = ['Policy', 'Count']
        fig_policy = px.pie(
            policy_counts, values='Count', names='Policy',
            color='Policy',
            color_discrete_map=POLICY_COLORS,
            hole=0.45,
        )
        fig_policy.update_traces(
            textinfo='percent+label',
            textfont_size=12,
            marker=dict(line=dict(color='#0e1117', width=2)),
        )
        fig_policy.update_layout(**plotly_layout("Distribusi Kebijakan Institusi", height=400))
        st.plotly_chart(fig_policy, use_container_width=True)

    # --- 1d. GPA per Major (Grouped Bar) ---
    with col4:
        gpa_major = df.groupby('Major_Category').agg(
            Pre_GPA=('Pre_Semester_GPA', 'mean'),
            Post_GPA=('Post_Semester_GPA', 'mean')
        ).reset_index()

        fig_gpa_major = go.Figure()
        fig_gpa_major.add_trace(go.Bar(
            name='Pre-Semester GPA', x=gpa_major['Major_Category'], y=gpa_major['Pre_GPA'],
            marker_color='#818cf8', text=gpa_major['Pre_GPA'].round(2),
            textposition='outside', textfont_size=10,
        ))
        fig_gpa_major.add_trace(go.Bar(
            name='Post-Semester GPA', x=gpa_major['Major_Category'], y=gpa_major['Post_GPA'],
            marker_color='#c084fc', text=gpa_major['Post_GPA'].round(2),
            textposition='outside', textfont_size=10,
        ))
        fig_gpa_major.update_layout(
            **plotly_layout("Rata-rata GPA per Bidang Studi", height=400),
            barmode='group',
        )
        fig_gpa_major.update_xaxes(title_text="")
        fig_gpa_major.update_yaxes(title_text="GPA", range=[0, 4.3])
        st.plotly_chart(fig_gpa_major, use_container_width=True)


# TAB 2: DAMPAK AI
with tab2:
    st.markdown('<div class="section-header">🤖 Dampak AI — GPA vs Intensitas Penggunaan</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Perubahan GPA rata-rata berdasarkan segmentasi penggunaan AI: Light (0–5 jam), Moderate (5–15 jam), Heavy (>15 jam).</div>', unsafe_allow_html=True)

    # --- 2a. GPA Change by AI Segment ---
    col1, col2 = st.columns(2)

    with col1:
        seg_stats = df.groupby('AI_Usage_Segment', observed=True).agg(
            Avg_Pre_GPA=('Pre_Semester_GPA', 'mean'),
            Avg_Post_GPA=('Post_Semester_GPA', 'mean'),
            Avg_GPA_Change=('GPA_Change', 'mean'),
            Count=('Student_ID', 'count')
        ).reset_index()

        fig_seg = go.Figure()
        fig_seg.add_trace(go.Bar(
            name='Pre-Semester GPA',
            x=seg_stats['AI_Usage_Segment'].astype(str),
            y=seg_stats['Avg_Pre_GPA'],
            marker_color='#818cf8',
            text=seg_stats['Avg_Pre_GPA'].round(3),
            textposition='outside',
        ))
        fig_seg.add_trace(go.Bar(
            name='Post-Semester GPA',
            x=seg_stats['AI_Usage_Segment'].astype(str),
            y=seg_stats['Avg_Post_GPA'],
            marker_color='#c084fc',
            text=seg_stats['Avg_Post_GPA'].round(3),
            textposition='outside',
        ))
        fig_seg.update_layout(
            **plotly_layout("Perbandingan GPA: Pre vs Post per Segmen AI"),
            barmode='group',
        )
        fig_seg.update_yaxes(title_text="GPA", range=[0, 4.3])
        fig_seg.update_xaxes(title_text="Segmen Penggunaan AI")
        st.plotly_chart(fig_seg, use_container_width=True)

    with col2:
        # GPA Change waterfall
        fig_change = go.Figure()
        colors_seg = ['#34d399', '#fbbf24', '#f87171']
        for i, row in seg_stats.iterrows():
            fig_change.add_trace(go.Bar(
                x=[str(row['AI_Usage_Segment'])],
                y=[row['Avg_GPA_Change']],
                marker_color=colors_seg[i],
                text=[f"{row['Avg_GPA_Change']:+.3f}"],
                textposition='outside',
                name=str(row['AI_Usage_Segment']),
                showlegend=True,
            ))
        fig_change.update_layout(**plotly_layout("Rata-rata Perubahan GPA (Δ) per Segmen"))
        fig_change.update_yaxes(title_text="Δ GPA (Post − Pre)", zeroline=True, zerolinecolor='#94a3b8', zerolinewidth=1)
        fig_change.update_xaxes(title_text="Segmen Penggunaan AI")
        st.plotly_chart(fig_change, use_container_width=True)

    # --- 2b. Scatter: Weekly AI Hours vs Post GPA ---
    st.markdown("---")

    fig_scatter = px.scatter(
        df.sample(min(5000, len(df)), random_state=42),
        x='Weekly_GenAI_Hours', y='Post_Semester_GPA',
        color='AI_Usage_Segment',
        color_discrete_map=SEGMENT_COLORS,
        opacity=0.4,
        size_max=8,
        hover_data=['Major_Category', 'Year_of_Study', 'Pre_Semester_GPA'],
        labels={
            'Weekly_GenAI_Hours': 'Jam Penggunaan AI / Minggu',
            'Post_Semester_GPA': 'Post-Semester GPA',
            'AI_Usage_Segment': 'Segmen',
        }
    )

    # Add trendline per segment
    for seg, color in SEGMENT_COLORS.items():
        seg_data = df[df['AI_Usage_Segment'] == seg]
        if len(seg_data) > 10:
            z = np.polyfit(seg_data['Weekly_GenAI_Hours'], seg_data['Post_Semester_GPA'], 1)
            p = np.poly1d(z)
            x_line = np.linspace(seg_data['Weekly_GenAI_Hours'].min(), seg_data['Weekly_GenAI_Hours'].max(), 50)
            fig_scatter.add_trace(go.Scatter(
                x=x_line, y=p(x_line),
                mode='lines', line=dict(color=color, width=2, dash='dash'),
                name=f"Trend {seg}", showlegend=True,
            ))

    fig_scatter.update_layout(**plotly_layout("Jam Penggunaan AI vs Post-Semester GPA (sample 5000)", height=500))
    st.plotly_chart(fig_scatter, use_container_width=True)

    # --- Summary stats table ---
    st.markdown("#### 📊 Statistik per Segmen Penggunaan AI")
    seg_detail = df.groupby('AI_Usage_Segment', observed=True).agg(
        Jumlah=('Student_ID', 'count'),
        Avg_Pre_GPA=('Pre_Semester_GPA', 'mean'),
        Avg_Post_GPA=('Post_Semester_GPA', 'mean'),
        Avg_GPA_Change=('GPA_Change', 'mean'),
        Avg_AI_Dependency=('Perceived_AI_Dependency', 'mean'),
        Avg_Skill_Retention=('Skill_Retention_Score', 'mean'),
    ).round(3).reset_index()
    seg_detail.columns = ['Segmen', 'Jumlah', 'Pre-GPA', 'Post-GPA', 'Δ GPA', 'AI Dependency', 'Skill Retention']
    st.dataframe(seg_detail, use_container_width=True, hide_index=True)


# TAB 3: KESEHATAN MENTAL
with tab3:
    st.markdown('<div class="section-header">🧠 Kesehatan Mental — Burnout & Anxiety</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Distribusi Burnout Risk Level dan Anxiety Level berdasarkan kebijakan institusi.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # --- 3a. Burnout Risk Distribution by Policy ---
    with col1:
        burnout_policy = pd.crosstab(
            df['Institutional_Policy'], df['Burnout_Risk_Level']
        ).reindex(columns=['Low', 'Medium', 'High']).reset_index()

        fig_bp = go.Figure()
        for level, color in BURNOUT_COLORS.items():
            if level in burnout_policy.columns:
                fig_bp.add_trace(go.Bar(
                    name=level, x=burnout_policy['Institutional_Policy'],
                    y=burnout_policy[level],
                    marker_color=color,
                    text=burnout_policy[level],
                    textposition='inside',
                ))
        fig_bp.update_layout(
            **plotly_layout("Burnout Risk Level per Kebijakan Institusi"),
            barmode='stack',
        )
        fig_bp.update_xaxes(title_text="Kebijakan Institusi")
        fig_bp.update_yaxes(title_text="Jumlah Mahasiswa")
        st.plotly_chart(fig_bp, use_container_width=True)

    # --- 3b. Anxiety Level Distribution by Policy ---
    with col2:
        fig_anxiety = px.box(
            df, x='Institutional_Policy', y='Anxiety_Level_During_Exams',
            color='Institutional_Policy',
            color_discrete_map=POLICY_COLORS,
            labels={
                'Anxiety_Level_During_Exams': 'Anxiety Level (1–10)',
                'Institutional_Policy': 'Kebijakan Institusi'
            }
        )
        fig_anxiety.update_layout(**plotly_layout("Distribusi Anxiety Level per Kebijakan", showlegend=False))
        fig_anxiety.update_xaxes(title_text="")
        st.plotly_chart(fig_anxiety, use_container_width=True)

    # --- 3c. Burnout % by Policy (normalized) ---
    st.markdown("---")
    col3, col4 = st.columns(2)

    with col3:
        burnout_pct = pd.crosstab(
            df['Institutional_Policy'], df['Burnout_Risk_Level'], normalize='index'
        ).reindex(columns=['Low', 'Medium', 'High']).reset_index()

        fig_bp_pct = go.Figure()
        for level, color in BURNOUT_COLORS.items():
            if level in burnout_pct.columns:
                fig_bp_pct.add_trace(go.Bar(
                    name=level, x=burnout_pct['Institutional_Policy'],
                    y=burnout_pct[level] * 100,
                    marker_color=color,
                    text=(burnout_pct[level] * 100).round(1).astype(str) + '%',
                    textposition='inside',
                ))
        fig_bp_pct.update_layout(
            **plotly_layout("Proporsi Burnout Risk (%) per Kebijakan"),
            barmode='stack',
        )
        fig_bp_pct.update_yaxes(title_text="Persentase (%)", range=[0, 105])
        fig_bp_pct.update_xaxes(title_text="")
        st.plotly_chart(fig_bp_pct, use_container_width=True)

    with col4:
        # Anxiety by AI segment
        fig_anx_seg = px.violin(
            df, x='AI_Usage_Segment', y='Anxiety_Level_During_Exams',
            color='AI_Usage_Segment',
            color_discrete_map=SEGMENT_COLORS,
            box=True, points=False,
            category_orders={'AI_Usage_Segment': ['Light (0–5 jam)', 'Moderate (5–15 jam)', 'Heavy (>15 jam)']},
            labels={
                'Anxiety_Level_During_Exams': 'Anxiety Level',
                'AI_Usage_Segment': 'Segmen AI'
            }
        )
        fig_anx_seg.update_layout(**plotly_layout("Anxiety Level per Segmen Penggunaan AI", showlegend=False))
        fig_anx_seg.update_xaxes(title_text="")
        st.plotly_chart(fig_anx_seg, use_container_width=True)


# TAB 4: RETENSI PENGETAHUAN
with tab4:
    st.markdown('<div class="section-header">📖 Retensi Pengetahuan — Skill Retention vs AI Dependency</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Korelasi antara Skill Retention Score dengan Perceived AI Dependency.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # --- 4a. Scatter: Skill Retention vs AI Dependency ---
    with col1:
        sample_data = df.sample(min(5000, len(df)), random_state=42)
        fig_ret = px.scatter(
            sample_data,
            x='Perceived_AI_Dependency', y='Skill_Retention_Score',
            color='AI_Usage_Segment',
            color_discrete_map=SEGMENT_COLORS,
            opacity=0.35,
            labels={
                'Perceived_AI_Dependency': 'Perceived AI Dependency (1–10)',
                'Skill_Retention_Score': 'Skill Retention Score (0–100)',
            },
            hover_data=['Major_Category', 'Post_Semester_GPA'],
        )
        # Add overall trendline
        z = np.polyfit(df['Perceived_AI_Dependency'], df['Skill_Retention_Score'], 1)
        p = np.poly1d(z)
        corr_val = df['Perceived_AI_Dependency'].corr(df['Skill_Retention_Score'])
        x_line = np.linspace(df['Perceived_AI_Dependency'].min(), df['Perceived_AI_Dependency'].max(), 50)
        fig_ret.add_trace(go.Scatter(
            x=x_line, y=p(x_line),
            mode='lines', line=dict(color='#f87171', width=3, dash='dash'),
            name=f'Trend (r={corr_val:.3f})',
        ))
        fig_ret.update_layout(**plotly_layout("Skill Retention vs AI Dependency (sample 5000)", height=480))
        st.plotly_chart(fig_ret, use_container_width=True)

    # --- 4b. Average Retention by Dependency level ---
    with col2:
        dep_bins = pd.cut(df['Perceived_AI_Dependency'], bins=range(0, 11), labels=[str(i) for i in range(1, 11)])
        ret_by_dep = df.copy()
        ret_by_dep['Dep_Bin'] = dep_bins
        ret_avg = ret_by_dep.groupby('Dep_Bin', observed=True)['Skill_Retention_Score'].mean().reset_index()
        ret_avg.columns = ['AI Dependency Level', 'Avg Skill Retention']

        fig_ret_bar = px.bar(
            ret_avg, x='AI Dependency Level', y='Avg Skill Retention',
            color='Avg Skill Retention',
            color_continuous_scale=['#34d399', '#fbbf24', '#f87171'],
            text='Avg Skill Retention',
        )
        fig_ret_bar.update_traces(texttemplate='%{text:.1f}', textposition='outside')
        fig_ret_bar.update_layout(**plotly_layout("Rata-rata Skill Retention per Level Dependency", height=480, showlegend=False))
        fig_ret_bar.update_yaxes(title_text="Skill Retention Score", range=[0, 100])
        fig_ret_bar.update_xaxes(title_text="Perceived AI Dependency Level")
        fig_ret_bar.update_coloraxes(showscale=False)
        st.plotly_chart(fig_ret_bar, use_container_width=True)

    # --- 4c. Heatmap: Skill Retention by Major + Policy ---
    st.markdown("---")
    ret_heatmap = df.pivot_table(
        values='Skill_Retention_Score',
        index='Major_Category',
        columns='Institutional_Policy',
        aggfunc='mean'
    ).round(1)

    fig_hm = px.imshow(
        ret_heatmap,
        text_auto='.1f',
        color_continuous_scale='Viridis',
        labels=dict(x="Kebijakan Institusi", y="Bidang Studi", color="Skill Retention"),
        aspect='auto',
    )
    fig_hm.update_layout(**plotly_layout("Heatmap: Rata-rata Skill Retention per Major × Kebijakan", height=380, showlegend=False))
    st.plotly_chart(fig_hm, use_container_width=True)


# TAB 5: PROFIL RISIKO
with tab5:
    st.markdown('<div class="section-header">⚠️ Profil Risiko — Segmentasi AI Dependency × Burnout</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-subtitle">Segmentasi mahasiswa berdasarkan kombinasi tingkat ketergantungan AI dan risiko burnout untuk mengidentifikasi kelompok berisiko tinggi.</div>', unsafe_allow_html=True)

    # --- Create Risk Profile ---
    df_risk = df.copy()
    df_risk['Dependency_Level'] = pd.cut(
        df_risk['Perceived_AI_Dependency'],
        bins=[0, 3, 6, 10],
        labels=['Low (1-3)', 'Medium (4-6)', 'High (7-10)'],
        include_lowest=True,
    )

    col1, col2 = st.columns(2)

    # --- 5a. Heatmap: Risk Matrix ---
    with col1:
        risk_matrix = pd.crosstab(
            df_risk['Dependency_Level'],
            df_risk['Burnout_Risk_Level'],
        )
        risk_matrix = risk_matrix.reindex(
            index=['Low (1-3)', 'Medium (4-6)', 'High (7-10)'],
            columns=['Low', 'Medium', 'High'],
        ).fillna(0).astype(int)

        fig_rm = px.imshow(
            risk_matrix,
            text_auto=True,
            color_continuous_scale=['#1e293b', '#fbbf24', '#ef4444'],
            labels=dict(x="Burnout Risk", y="AI Dependency", color="Jumlah"),
            aspect='auto',
        )
        fig_rm.update_layout(**plotly_layout("Risk Matrix: AI Dependency × Burnout Risk", height=420, showlegend=False))
        st.plotly_chart(fig_rm, use_container_width=True)

    # --- 5b. Sunburst chart ---
    with col2:
        sunburst_data = df_risk.groupby(
            ['Dependency_Level', 'Burnout_Risk_Level'], observed=True
        ).size().reset_index(name='Count')

        fig_sun = px.sunburst(
            sunburst_data,
            path=['Dependency_Level', 'Burnout_Risk_Level'],
            values='Count',
            color='Count',
            color_continuous_scale=['#818cf8', '#c084fc', '#f87171'],
        )
        fig_sun.update_layout(**plotly_layout("Sunburst: Dependency → Burnout", height=420, showlegend=False))
        fig_sun.update_traces(textinfo='label+percent parent')
        st.plotly_chart(fig_sun, use_container_width=True)

    # --- 5c. High-Risk Profiling ---
    st.markdown("---")
    st.markdown("#### 🔴 Profil Mahasiswa Risiko Tinggi (High Dependency + High Burnout)")

    high_risk = df_risk[
        (df_risk['Dependency_Level'] == 'High (7-10)') &
        (df_risk['Burnout_Risk_Level'] == 'High')
    ]

    if len(high_risk) > 0:
        hr_pct = len(high_risk) / len(df) * 100

        col_a, col_b, col_c, col_d = st.columns(4)
        col_a.metric("Jumlah Mahasiswa", f"{len(high_risk):,}", f"{hr_pct:.1f}% dari total")
        col_b.metric("Avg Post-GPA", f"{high_risk['Post_Semester_GPA'].mean():.2f}")
        col_c.metric("Avg Skill Retention", f"{high_risk['Skill_Retention_Score'].mean():.1f}")
        col_d.metric("Avg Anxiety Level", f"{high_risk['Anxiety_Level_During_Exams'].mean():.1f}")

        col_e, col_f = st.columns(2)

        with col_e:
            hr_major = high_risk['Major_Category'].value_counts().reset_index()
            hr_major.columns = ['Major', 'Count']
            fig_hr_major = px.bar(
                hr_major, x='Major', y='Count',
                color='Major', color_discrete_sequence=PALETTE,
                text='Count',
            )
            fig_hr_major.update_traces(textposition='outside')
            fig_hr_major.update_layout(**plotly_layout("High-Risk: Distribusi per Bidang Studi", height=380, showlegend=False))
            fig_hr_major.update_xaxes(title_text="")
            fig_hr_major.update_yaxes(title_text="Jumlah")
            st.plotly_chart(fig_hr_major, use_container_width=True)

        with col_f:
            hr_year = high_risk['Year_of_Study'].value_counts().reindex(
                [y for y in year_order if y in high_risk['Year_of_Study'].unique()]
            ).reset_index()
            hr_year.columns = ['Year', 'Count']
            fig_hr_year = px.bar(
                hr_year, x='Year', y='Count',
                color='Year', color_discrete_sequence=PALETTE[3:],
                text='Count',
            )
            fig_hr_year.update_traces(textposition='outside')
            fig_hr_year.update_layout(**plotly_layout("High-Risk: Distribusi per Jenjang", height=380, showlegend=False))
            fig_hr_year.update_xaxes(title_text="")
            fig_hr_year.update_yaxes(title_text="Jumlah")
            st.plotly_chart(fig_hr_year, use_container_width=True)
    else:
        st.info("Tidak ada mahasiswa dalam kategori High Dependency + High Burnout dengan filter saat ini.")


# FOOTER
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#64748b; padding:20px 0; font-size:0.8rem;">
    <strong>Dashboard BI — Modul 6</strong> | Sertifikasi BNSP Data Analyst<br/>
    Dataset: AI Impact on Students — 50.000 Mahasiswa | 16 Variabel<br/>
    Built with Streamlit + Plotly | © 2024
</div>
""", unsafe_allow_html=True)
