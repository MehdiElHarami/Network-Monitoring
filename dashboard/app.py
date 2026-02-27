import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="NetWatch Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    /* Main background & font */
    .main .block-container { padding-top: 1.5rem; }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%);
        border: 1px solid #3a3a5c;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 14px rgba(0,0,0,.25);
    }
    div[data-testid="stMetric"] label {
        color: #a0a0b8 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #e0e0ff !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
    }

    /* Section headers */
    .section-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #c0c0e0;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid #3a3a5c;
    }

    /* Alert cards */
    .alert-card {
        background: linear-gradient(135deg, #3b1a1a 0%, #4a2020 100%);
        border-left: 4px solid #ff4b4b;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 8px;
        color: #ffcccc;
    }
    .alert-card .alert-ip { font-weight: 700; color: #ff6b6b; font-size: 1rem; }
    .alert-card .alert-count { color: #ff9999; }

    /* Success card */
    .success-card {
        background: linear-gradient(135deg, #1a3b2a 0%, #204a30 100%);
        border-left: 4px solid #4bff6b;
        border-radius: 8px;
        padding: 12px 16px;
        color: #ccffdd;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #12121f 0%, #1a1a2e 100%);
    }

    /* Hide default Streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


st_autorefresh(interval=2_000, key="live_refresh")

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/network-protection.png", width=64)
    st.markdown("## 🛡️ NetWatch")
    st.caption("Real-time Network Monitoring")
    st.divider()
    st.markdown("🟢 **Live** — refreshing every 2s")
    refresh_btn = st.button("🔄 Refresh Now", use_container_width=True)
    st.divider()
    st.markdown(f"**Last updated:**  \n`{datetime.now().strftime('%H:%M:%S')}`")


def api_get(endpoint: str):
    try:
        r = requests.get(f"{API_URL}{endpoint}", timeout=5)
        if r.status_code == 200:
            return r.json()
    except requests.ConnectionError:
        pass
    return None


def format_bytes(b: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if b < 1024:
            return f"{b:.1f} {unit}"
        b /= 1024
    return f"{b:.1f} TB"


st.markdown("# 🛡️ NetWatch Dashboard")
st.caption("Real-time network traffic monitoring & anomaly detection")

summary = api_get("/stats/summary")

if summary:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📦 Total Packets", f"{summary['total_packets']:,}")
    c2.metric("📡 Unique Sources", summary["unique_sources"])
    c3.metric("🎯 Unique Destinations", summary["unique_destinations"])
    c4.metric("💾 Total Traffic", format_bytes(summary["total_bytes"]))
else:
    st.warning("⚠️ Could not connect to backend at `http://127.0.0.1:8000`")
    st.stop()

st.markdown("")

col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown('<div class="section-header">📈 Traffic Over Time (last 30 min)</div>', unsafe_allow_html=True)

    traffic_data = api_get("/stats/traffic-over-time")
    if traffic_data:
        df_traffic = pd.DataFrame(traffic_data)
        df_traffic["timestamp"] = pd.to_datetime(df_traffic["timestamp"])
        df_traffic = df_traffic.set_index("timestamp").resample("30s").agg(
            packet_count=("packet_size", "count"),
            total_bytes=("packet_size", "sum"),
        ).reset_index()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_traffic["timestamp"],
            y=df_traffic["packet_count"],
            mode="lines+markers",
            name="Packets",
            line=dict(color="#636EFA", width=2.5),
            marker=dict(size=4),
            fill="tozeroy",
            fillcolor="rgba(99,110,250,0.1)",
        ))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=10, b=20),
            height=320,
            xaxis=dict(showgrid=False),
            yaxis=dict(title="Packets / 30s", gridcolor="#2a2a3e"),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No traffic data in the last 30 minutes.")

with col_right:
    st.markdown('<div class="section-header">🧬 Protocol Distribution</div>', unsafe_allow_html=True)

    proto_data = api_get("/stats/protocol-distribution")
    if proto_data:
        df_proto = pd.DataFrame(proto_data)
        colors = {"TCP": "#636EFA", "UDP": "#EF553B", "OTHER": "#FFA15A"}
        fig_proto = px.pie(
            df_proto,
            values="count",
            names="protocol",
            color="protocol",
            color_discrete_map=colors,
            hole=0.45,
        )
        fig_proto.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=10, b=20),
            height=320,
            showlegend=True,
            legend=dict(orientation="h", y=-0.1),
        )
        fig_proto.update_traces(textinfo="percent+label", textfont_size=12)
        st.plotly_chart(fig_proto, use_container_width=True)
    else:
        st.info("No protocol data yet.")

col_talkers, col_alerts = st.columns([3, 2])

with col_talkers:
    st.markdown('<div class="section-header">🔥 Top Talkers</div>', unsafe_allow_html=True)

    talkers_data = api_get("/stats/top-talkers")
    if talkers_data:
        df_talkers = pd.DataFrame(talkers_data)
        fig_talkers = px.bar(
            df_talkers,
            x="src_ip",
            y="count",
            color="count",
            color_continuous_scale=["#2d2d6b", "#636EFA", "#b0b0ff"],
            text="count",
        )
        fig_talkers.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=10, b=20),
            height=300,
            xaxis=dict(title="Source IP", showgrid=False),
            yaxis=dict(title="Packet Count", gridcolor="#2a2a3e"),
            coloraxis_showscale=False,
            showlegend=False,
        )
        fig_talkers.update_traces(textposition="outside", textfont_size=12)
        st.plotly_chart(fig_talkers, use_container_width=True)
    else:
        st.info("No traffic data yet.")

with col_alerts:
    st.markdown('<div class="section-header">🚨 Active Alerts</div>', unsafe_allow_html=True)

    alerts_data = api_get("/alerts")
    if alerts_data is not None:
        if alerts_data:
            for alert in alerts_data:
                st.markdown(f"""
                <div class="alert-card">
                    <span class="alert-ip">⚠ {alert['src_ip']}</span><br>
                    <span class="alert-count">{alert['packet_count']} packets</span> —
                    {alert['alert']}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="success-card">✅ No active alerts — network looks healthy.</div>', unsafe_allow_html=True)
    else:
        st.error("Could not retrieve alerts.")

st.markdown('<div class="section-header">📋 Recent Packets</div>', unsafe_allow_html=True)

recent_data = api_get("/packets/recent?limit=30")
if recent_data:
    df_recent = pd.DataFrame(recent_data)
    df_recent["timestamp"] = pd.to_datetime(df_recent["timestamp"]).dt.strftime("%H:%M:%S")
    df_recent.columns = ["Time", "Source IP", "Destination IP", "Protocol", "Size (bytes)"]

    st.dataframe(
        df_recent,
        use_container_width=True,
        height=350,
        column_config={
            "Protocol": st.column_config.TextColumn(width="small"),
            "Size (bytes)": st.column_config.NumberColumn(format="%d"),
        },
    )
else:
    st.info("No packets captured yet.")
