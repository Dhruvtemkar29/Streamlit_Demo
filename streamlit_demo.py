import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------------------------------------------
# Page Config
# ---------------------------------------------------
st.set_page_config(
    page_title="📊 Smart CSV Dashboard",
    page_icon="📈",
    layout="wide"
)

# ---------------------------------------------------
# Custom CSS
# ---------------------------------------------------
st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#0f172a,#1e293b,#111827);
}

.block-container{
    padding-top:2rem;
}

.big-title{
    font-size:45px;
    color:white;
    font-weight:bold;
}

.subtitle{
    color:#d1d5db;
    font-size:18px;
}

.metric-card{
    background:#1f2937;
    padding:18px;
    border-radius:15px;
    text-align:center;
    box-shadow:0 8px 20px rgba(0,0,0,.3);
}

.metric-title{
    color:#9ca3af;
    font-size:16px;
}

.metric-value{
    color:#38bdf8;
    font-size:32px;
    font-weight:bold;
}

div[data-testid="stSidebar"]{
    background:#111827;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Header
# ---------------------------------------------------
st.markdown("""
<div class='big-title'>
📊 Smart Data Visualizer
</div>

<div class='subtitle'>
Upload a CSV • Explore Data • Create Interactive Charts
</div>

<br>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# Upload
# ---------------------------------------------------
uploaded_file = st.file_uploader(
    "📂 Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=np.number).columns.tolist()

    # ---------------------------------------------------
    # KPI Cards
    # ---------------------------------------------------

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class='metric-card'>
        <div class='metric-title'>Rows</div>
        <div class='metric-value'>{df.shape[0]}</div>
        </div>
        """,unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class='metric-card'>
        <div class='metric-title'>Columns</div>
        <div class='metric-value'>{df.shape[1]}</div>
        </div>
        """,unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class='metric-card'>
        <div class='metric-title'>Missing</div>
        <div class='metric-value'>{df.isna().sum().sum()}</div>
        </div>
        """,unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class='metric-card'>
        <div class='metric-title'>Numeric</div>
        <div class='metric-value'>{len(numeric_cols)}</div>
        </div>
        """,unsafe_allow_html=True)

    st.write("")

    # ---------------------------------------------------
    # Sidebar
    # ---------------------------------------------------

    st.sidebar.title("🎛 Dashboard")

    page = st.sidebar.radio(
        "Navigate",
        [
            "Dataset",
            "Visualization",
            "Statistics"
        ]
    )

    # ---------------------------------------------------
    # Dataset
    # ---------------------------------------------------

    if page=="Dataset":

        st.subheader("📄 Dataset Preview")

        st.dataframe(df,use_container_width=True,height=500)

    # ---------------------------------------------------
    # Visualization
    # ---------------------------------------------------

    elif page=="Visualization":

        chart = st.selectbox(
    "Select Visualization",
    [
        "Histogram",
        "Scatter",
        "Line",
        "Bar",
        "Pie",
        "Box Plot",
        "Violin Plot",
        "Area Chart",
        "Bubble Chart",
        "Density Contour",
        "Sunburst Chart",
        "Treemap",
        "3D Scatter",
        "Correlation Heatmap"
    ]
)

        if chart=="Histogram":

            col = st.selectbox("Column",numeric_cols)

            fig = px.histogram(
                df,
                x=col,
                template="plotly_dark",
                color_discrete_sequence=["cyan"]
            )

            st.plotly_chart(fig,use_container_width=True)

        elif chart=="Scatter":

            x = st.selectbox("X",numeric_cols)

            y = st.selectbox("Y",numeric_cols,index=min(1,len(numeric_cols)-1))

            color = st.selectbox(
                "Color",
                [None]+categorical_cols
            )

            fig = px.scatter(
                df,
                x=x,
                y=y,
                color=color,
                template="plotly_dark"
            )

            st.plotly_chart(fig,use_container_width=True)

        elif chart=="Line":

            x = st.selectbox("X Axis",df.columns)

            y = st.selectbox("Y Axis",numeric_cols)

            fig = px.line(
                df,
                x=x,
                y=y,
                template="plotly_dark"
            )

            st.plotly_chart(fig,use_container_width=True)

        elif chart=="Bar":

            x = st.selectbox("Category",df.columns)

            y = st.selectbox("Value",numeric_cols)

            fig = px.bar(
                df,
                x=x,
                y=y,
                color=x,
                template="plotly_dark"
            )

            st.plotly_chart(fig,use_container_width=True)

        elif chart=="Pie":

            if len(categorical_cols)>0:

                cat = st.selectbox(
                    "Category",
                    categorical_cols
                )

                pie = df[cat].value_counts().reset_index()

                pie.columns=["Category","Count"]

                fig = px.pie(
                    pie,
                    names="Category",
                    values="Count",
                    hole=0.45,
                    template="plotly_dark"
                )

                st.plotly_chart(fig,use_container_width=True)
                
        elif chart == "Box Plot":

                y = st.selectbox("Column", numeric_cols)

                fig = px.box(
                    df,
                    y=y,
                    color_discrete_sequence=["cyan"],
                    template="plotly_dark"
                )

                st.plotly_chart(fig, use_container_width=True)
                
        elif chart == "Violin Plot":

                y = st.selectbox("Column", numeric_cols)

                fig = px.violin(
                    df,
                    y=y,
                    box=True,
                    points="all",
                    template="plotly_dark"
                )

                st.plotly_chart(fig, use_container_width=True)
                
        elif chart == "Area Chart":

                x = st.selectbox("X Axis", df.columns)

                y = st.selectbox("Y Axis", numeric_cols)

                fig = px.area(
                    df,
                    x=x,
                    y=y,
                    template="plotly_dark"
                )

                st.plotly_chart(fig, use_container_width=True)
                
        elif chart == "Bubble Chart":

                x = st.selectbox("X", numeric_cols)

                y = st.selectbox("Y", numeric_cols, index=min(1, len(numeric_cols)-1))

                size = st.selectbox("Bubble Size", numeric_cols)

                fig = px.scatter(
                    df,
                    x=x,
                    y=y,
                    size=size,
                    color=size,
                    template="plotly_dark"
                )

                st.plotly_chart(fig, use_container_width=True)
                
        elif chart == "Density Contour":

                x = st.selectbox("X", numeric_cols)

                y = st.selectbox("Y", numeric_cols, index=min(1, len(numeric_cols)-1))

                fig = px.density_contour(
                    df,
                    x=x,
                    y=y,
                    template="plotly_dark"
                )

                st.plotly_chart(fig, use_container_width=True)
                
        elif chart == "Treemap":

                if categorical_cols:

                    cat = st.selectbox("Category", categorical_cols)

                    value = st.selectbox("Value", numeric_cols)

                    fig = px.treemap(
                        df,
                        path=[cat],
                        values=value,
                        template="plotly_dark"
                    )

                    st.plotly_chart(fig, use_container_width=True)
                    
        elif chart == "Sunburst Chart":

                if categorical_cols:

                    cat = st.selectbox("Category", categorical_cols)

                    value = st.selectbox("Value", numeric_cols)

                    fig = px.sunburst(
                        df,
                        path=[cat],
                        values=value,
                        template="plotly_dark"
                    )

                    st.plotly_chart(fig, use_container_width=True)

                else:
                    st.warning("No categorical columns found.")
                    
        elif chart == "3D Scatter":

                if len(numeric_cols) >= 3:

                    x = st.selectbox("X", numeric_cols)

                    y = st.selectbox("Y", numeric_cols, index=1)

                    z = st.selectbox("Z", numeric_cols, index=2)

                    fig = px.scatter_3d(
                        df,
                        x=x,
                        y=y,
                        z=z,
                        color=z,
                        template="plotly_dark"
                    )

                    st.plotly_chart(fig, use_container_width=True)

                else:
                    st.warning("Need at least 3 numeric columns.")
                    
        elif chart == "Correlation Heatmap":

                corr = df[numeric_cols].corr()

                if corr.empty:
                    st.warning("No numeric columns available.")
                else:
                    fig = px.imshow(
                        corr,
                        text_auto=True,
                        color_continuous_scale="RdBu",
                        template="plotly_dark"
                    )

                    st.plotly_chart(fig, use_container_width=True)

        else:
                st.warning("No categorical columns found.")

    # ---------------------------------------------------
    # Statistics
    # ---------------------------------------------------

    else:

        left,right = st.columns([2,1])

        with left:

            st.subheader("📈 Statistical Summary")

            st.dataframe(df.describe())

        with right:

            st.subheader("⚠ Missing Values")

            missing = df.isna().sum()

            st.dataframe(missing)

        if len(numeric_cols)>1:

            st.subheader("🔥 Correlation Matrix")

            corr = df[numeric_cols].corr()

            fig = px.imshow(
                corr,
                text_auto=True,
                color_continuous_scale="RdBu",
                aspect="auto"
            )

            st.plotly_chart(fig,use_container_width=True)

        st.download_button(
            "📥 Download CSV",
            df.to_csv(index=False).encode(),
            "dataset.csv",
            "text/csv"
        )

else:

    st.info("👈 Upload a CSV file to get started.")

