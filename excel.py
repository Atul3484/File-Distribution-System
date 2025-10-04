import streamlit as st
import pandas as pd
import os
import time

# --- Modern UI CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        background: #f5f7fa;
    }
    .company-header {
        display: flex;
        align-items: center;
        gap: 32px;
        margin-bottom: 18px;
        padding: 24px 0 12px 0;
        animation: fadeInDown 1s;
    }
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px);}
        to { opacity: 1; transform: translateY(0);}
    }
    .company-logo {
        width: 110px;
        border-radius: 18px;
        border: 3px solid #b30000;
        box-shadow: 0 4px 16px rgba(179,0,0,0.12);
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(179,0,0,0.2);}
        70% { box-shadow: 0 0 0 10px rgba(179,0,0,0);}
        100% { box-shadow: 0 0 0 0 rgba(179,0,0,0);}
    }
    .company-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #b30000;
        letter-spacing: 1.5px;
        margin-bottom: 0;
        line-height: 1.1;
        text-shadow: 1px 1px 0 #fff;
    }
    .company-subtitle {
        font-size: 1.3rem;
        color: #e74c3c;
        font-weight: 700;
        margin-top: 0;
        letter-spacing: 0.5px;
        text-shadow: 1px 1px 0 #fff;
    }
    .stButton>button, .stDownloadButton>button {
        background: linear-gradient(90deg, #b30000 0%, #e74c3c 100%);
        color: #fff;
        border-radius: 10px;
        border: none;
        font-weight: 700;
        font-size: 1.08rem;
        box-shadow: 0 2px 8px rgba(179,0,0,0.10);
        transition: box-shadow 0.2s, transform 0.2s, background 0.3s;
        padding: 10px 24px;
        cursor: pointer;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        box-shadow: 0 6px 24px rgba(179,0,0,0.18);
        transform: translateY(-2px) scale(1.03);
        background: linear-gradient(90deg, #e74c3c 0%, #b30000 100%);
    }
    .stProgress > div > div {
        background: linear-gradient(90deg, #b30000 0%, #e74c3c 100%);
        transition: width 0.5s;
    }
    .stSidebar {
        background: #fff;
        border-right: 2px solid #b30000;
        animation: fadeInLeft 1s;
    }
    @keyframes fadeInLeft {
        from { opacity: 0; transform: translateX(-30px);}
        to { opacity: 1; transform: translateX(0);}
    }
    .custom-upload-box {
        border: 3px solid #b30000 !important;
        border-radius: 14px;
        background: #f8f8f8;
        margin-bottom: 18px;
        padding: 18px 12px 12px 12px;
        animation: fadeInUp 1s;
    }
    .custom-preview-box {
        border: 3px solid #b30000 !important;
        border-radius: 14px;
        background: #fff;
        margin-bottom: 18px;
        padding: 12px 8px 8px 8px;
        animation: fadeInUp 1s;
    }
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px);}
        to { opacity: 1; transform: translateY(0);}
    }
    .preview-title, .upload-title {
        font-size: 1.18rem;
        color: #b30000;
        font-weight: 700;
        margin-bottom: 6px;
        margin-top: 10px;
        font-family: 'Inter', sans-serif;
        letter-spacing: 0.5px;
    }
    .footer {
        text-align:center;
        color:#b30000;
        font-size:1.05rem;
        margin-top:32px;
        padding-bottom: 16px;
        letter-spacing: 0.5px;
        opacity: 0.8;
    }
    .loading-logo {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 16px;
        margin-bottom: 10px;
        animation: fadeIn 1s;
    }
    .loading-logo img {
        width: 54px;
        border-radius: 12px;
        border: 3px solid #b30000;
        animation: spin 1.2s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg);}
        100% { transform: rotate(360deg);}
    }
    .download-area {
        background: #fff6f6;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(179,0,0,0.04);
        padding: 18px 12px 12px 12px;
        margin-bottom: 18px;
        border: none;
        animation: fadeInUp 1s;
    }
    .stMarkdown h4 {
        margin-top: 0;
    }
    </style>
""", unsafe_allow_html=True)

# --- Favicon ---
st.set_page_config(
    page_title="Discount Splitter",
    layout="wide",
    page_icon="https://play-lh.googleusercontent.com/FW1IjXPRNOdl87MG_a3yjf8uhwjX_4lsjEV22vaSq7Wo_6_A7l9pa8C6EMcn_vX3aXpKLMIYgImWZJWSdBnO5A=w240-h480-rw"
)

# --- Header with logo and name ---
st.markdown(
    """
    <div class="company-header">
        <img src="https://play-lh.googleusercontent.com/FW1IjXPRNOdl87MG_a3yjf8uhwjX_4lsjEV22vaSq7Wo_6_A7l9pa8C6EMcn_vX3aXpKLMIYgImWZJWSdBnO5A=w240-h480-rw" class="company-logo" alt="Company Logo" style="border-radius:50%;border:3px solid #fff;">
        <div>
            <div class="company-title">Generali Central Insurance</div>
            <div class="company-subtitle">Discount Excel Splitter Tool</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --- Sidebar for instructions ---
with st.sidebar:
    st.image("https://play-lh.googleusercontent.com/FW1IjXPRNOdl87MG_a3yjf8uhwjX_4lsjEV22vaSq7Wo_6_A7l9pa8C6EMcn_vX3aXpKLMIYgImWZJWSdBnO5A=w240-h480-rw", width=80)
    st.header("Instructions")
    st.markdown("""
    <span style='color:#b30000'>
    1. Upload your Excel or CSV file (skip first 2 rows for Excel).<br>
    2. Click <b>Generate Discount Files</b>.<br>
    3. Download your split files from below.
    </span>
    """, unsafe_allow_html=True)

st.markdown(
    "<h4 style='color: #b30000;'>Split discount Excels into <b>Private</b> and <b>Commercial</b> categories based on Age and Fuel Type.</h4>",
    unsafe_allow_html=True
)

# --- Upload box with circle logo border and styled title ---
st.markdown("<div class='custom-upload-box'>", unsafe_allow_html=True)
st.markdown("<div class='upload-title'>⬆️ Upload Excel or CSV File</div>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["xlsx", "csv"])
st.markdown("</div>", unsafe_allow_html=True)

if uploaded_file:
    # --- Branded loading animation ---
    with st.spinner(
        """
        <div class='loading-logo'>
            <img src='https://play-lh.googleusercontent.com/FW1IjXPRNOdl87MG_a3yjf8uhwjX_4lsjEV22vaSq7Wo_6_A7l9pa8C6EMcn_vX3aXpKLMIYgImWZJWSdBnO5A=w240-h480-rw'>
            <span style='color:#b30000;font-weight:700;font-size:1.2rem;'>Loading file...</span>
        </div>
        """):
        time.sleep(1)  # Simulate loading for effect
        # --- Support both Excel and CSV ---
        if uploaded_file.name.lower().endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, skiprows=2)
    st.success("✅ File uploaded and loaded successfully!")

    # --- Data Preview with red border ONLY around actual table ---
    st.markdown("<div class='custom-preview-box' style='border:none;'>", unsafe_allow_html=True)
    st.markdown("<div class='preview-title'>🔍 Data Preview</div>", unsafe_allow_html=True)
    st.dataframe(df.head(), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    private_dir = "private_discount_excels"
    commercial_dir = "commercial_discount_excels"
    os.makedirs(private_dir, exist_ok=True)
    os.makedirs(commercial_dir, exist_ok=True)

    private_columns = ['CITY_ID', 'STATE ID', 'SMS_Model', 'DISCOUNT_P']
    commercial_columns = ['CITY_ID', 'STATE ID', 'SMS_Model', 'DISCOUNT_C']
    rename_map_private = {
        'CITY_ID': 'CITY_ID',
        'STATE ID': 'STATE_ID',
        'SMS_Model': 'MODEL_CODE',
        'DISCOUNT_P': 'DISCOUNT'
    }
    rename_map_commercial = {
        'CITY_ID': 'CITY_ID',
        'STATE ID': 'STATE_ID',
        'SMS_Model': 'MODEL_CODE',
        'DISCOUNT_C': 'DISCOUNT'
    }

    if st.button("🚀 Generate Discount Files"):
        # --- Modern animated progress bar and interactive status ---
        progress = st.progress(0, text="Splitting files...")
        status_placeholder = st.empty()
        files_private, files_commercial = [], []
        try:
            groups = list(df.groupby(['Age', 'FUEL_TYPE']))
            total_groups = len(groups)
            for i, ((age, fuel), group_df) in enumerate(groups):
                age_str = str(age).replace(" ", "_")
                fuel_str = str(fuel).replace(" ", "_")

                private_df = group_df[private_columns].rename(columns=rename_map_private)
                private_df['DISCOUNT_L'] = ''
                private_filename = f"Age{age_str}_{fuel_str}_private.xlsx"
                private_path = os.path.join(private_dir, private_filename)
                private_df.to_excel(private_path, index=False)
                files_private.append(private_path)

                commercial_df = group_df[commercial_columns].rename(columns=rename_map_commercial)
                commercial_df['DISCOUNT_L'] = ''
                commercial_filename = f"Age{age_str}_{fuel_str}_commercial.xlsx"
                commercial_path = os.path.join(commercial_dir, commercial_filename)
                commercial_df.to_excel(commercial_path, index=False)
                files_commercial.append(commercial_path)

                # --- Solid animated progress bar with effects ---
                progress.progress((i + 1) / total_groups)
                status_placeholder.markdown(
                    f"""
                    <div style='width:100%;margin:16px 0;'>
                        <div style='height:18px;background:linear-gradient(90deg,#b30000 0%,#e74c3c 100%);border-radius:9px;box-shadow:0 2px 8px rgba(179,0,0,0.10);position:relative;overflow:hidden;'>
                            <div style='width:{int(((i+1)/total_groups)*100)}%;height:100%;background:rgba(255,255,255,0.18);border-radius:9px;transition:width 0.4s;'></div>
                        </div>
                        <div style='text-align:center;margin-top:6px;color:#b30000;font-weight:700;font-size:1.08rem;letter-spacing:0.5px;'>
                            <span style='font-size:1.2rem;'>⏳</span>
                            <span>Progress: {i+1} of {total_groups}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True
                )
                time.sleep(0.3)  # Simulate animation

            # Success animation and message
            status_placeholder.markdown(
                """
                <div style='display:flex;align-items:center;gap:12px;'>
                    <span style='font-size:1.7rem;'>✅</span>
                    <span style='color:#27ae60;font-size:1.18rem;font-weight:700;'>
                        All files exported successfully!
                    </span>
                </div>
                """, unsafe_allow_html=True
            )
            st.markdown(f"<span style='color:#b30000'>📁 Files saved in <b>{private_dir}</b> and <b>{commercial_dir}</b> folders.</span>", unsafe_allow_html=True)

            # --- Download buttons with enhanced UI ---
            st.markdown("<div class='download-area'>", unsafe_allow_html=True)
            st.subheader("⬇️ Download Your Files")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<b style='color:#b30000'>Private Discount Files</b>", unsafe_allow_html=True)
                for file in files_private:
                    with open(file, "rb") as f:
                        st.download_button(
                            label=f"Download {os.path.basename(file)}",
                            data=f.read(),
                            file_name=os.path.basename(file),
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
            with col2:
                st.markdown("<b style='color:#b30000'>Commercial Discount Files</b>", unsafe_allow_html=True)
                for file in files_commercial:
                    with open(file, "rb") as f:
                        st.download_button(
                            label=f"Download {os.path.basename(file)}",
                            data=f.read(),
                            file_name=os.path.basename(file),
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
            st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Error: {e}")
else:
    st.info("📂 Please upload an Excel or CSV file to begin.")

# --- Custom Footer ---
st.markdown("""
    <div class='footer'>
        &copy; 2025 Generali Central Insurance &mdash; Discount Excel Splitter Tool
    </div>
""", unsafe_allow_html=True)

