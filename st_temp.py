import streamlit as st
import time

# ------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------
st.set_page_config(
    page_title="Document Processor - Circular Workflow",
    layout="wide"
)

# ------------------------------------------------------
# ✅ CSS (FIXED Sticky Title + Stepper + Logs)
# ------------------------------------------------------
st.markdown("""
<style>

main > div {
    overflow: visible !important;  /* ✅ REQUIRED for sticky to work */
}

/* Reduce padding for more usable screen space */
.block-container {
    padding-top: 0.5rem;
    padding-bottom: 1rem;
}

/* -------------------------------------------------- */
/* ✅ FROZEN HEADER: TITLE + STEPPER */
/* -------------------------------------------------- */
.frozen-header {
    position: sticky;
    top: 0;
    z-index: 9999;
    background: white;
    padding: 8px 20px 12px 20px;
    border-bottom: 1px solid #ddd;
    box-shadow: 0px 2px 6px rgba(0,0,0,0.05);
}

.frozen-header h1 {
    margin: 0;
    font-size: 1.45rem;
}

/* -------------------------------------------------- */
/* ✅ Circular Stepper */
/* -------------------------------------------------- */
.stepper {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 6px;
}

.step-circle {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: #e3e3e3;
    border: 3px solid #ccc;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    transition: all 0.3s ease;
}

.step-circle.active {
    background: #e8f0ff;
    border-color: #3f82ff;
    animation: pulse 1.4s infinite;
}

.step-circle.completed {
    background: #d9ffe0;
    border-color: #19a63b;
    transform: translateY(-4px);
}

.step-label {
    text-align: center;
    font-size: 0.80rem;
    margin-top: 4px;
}

.stepper-line {
    flex-grow: 1;
    height: 4px;
    background: #dcdcdc;
    margin: 0 -2px;
}

.stepper-line.completed {
    background: #19a63b;
}

/* Pulse animation for active circle */
@keyframes pulse {
    0%   { box-shadow: 0 0 0 0 rgba(63,130,255, .5); }
    70%  { box-shadow: 0 0 15px 10px rgba(63,130,255, 0); }
    100% { box-shadow: 0 0 0 0 rgba(63,130,255, 0); }
}

/* -------------------------------------------------- */
/* ✅ STICKY LOG PANEL */
/* -------------------------------------------------- */
.log-box {
    position: sticky;
    top: 145px;   /* Below frozen header */
    height: 260px;
    background: #000;
    color: #00ff6a;
    padding: 10px;
    overflow-y: auto;
    border: 1px solid #333;
    border-radius: 8px;
    font-family: Consolas, monospace;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------
if "step" not in st.session_state: st.session_state.step = 1
if "logs" not in st.session_state: st.session_state.logs = []
if "pdf_bytes" not in st.session_state: st.session_state.pdf_bytes = None
if "extracted_data" not in st.session_state: st.session_state.extracted_data = None


# ------------------------------------------------------
# UTILITIES
# ------------------------------------------------------
def log(msg):
    st.session_state.logs.append(msg)

def render_logs():
    st.markdown(
        "<div class='log-box'>" +
        "<br>".join(st.session_state.logs) +
        "</div>", unsafe_allow_html=True
    )

def render_stepper():
    steps = ["Upload", "Extract", "Preview", "API", "Done"]

    html = "<div class='stepper'>"

    for i, step_name in enumerate(steps, start=1):

        css = "step-circle"
        if st.session_state.step == i:
            css += " active"
        elif st.session_state.step > i:
            css += " completed"

        html += f"""
        <div style='text-align:center;'>
            <div class='{css}'>{i}</div>
            <div class='step-label'>{step_name}</div>
        </div>
        """

        # connecting line
        if i != len(steps):
            line_class = "stepper-line"
            if st.session_state.step > i:
                line_class += " completed"
            html += f"<div class='{line_class}'></div>"

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)


def extract_pdf_data(pdf_bytes):
    time.sleep(1.2)
    return {
        "customer_id":"88921",
        "request_type":"update_address",
        "new_address":{
            "street":"871 Creekside",
            "city":"Charlotte",
            "state":"NC",
            "zip":"28202"
        }
    }

def call_api(data):
    time.sleep(1)
    return {"status": "success", "received": data}


# ------------------------------------------------------
# ✅ FROZEN HEADER (TITLE + STEPPER)
# ------------------------------------------------------
st.markdown("<div class='frozen-header'>", unsafe_allow_html=True)

st.title("📄 Document Processor — Circular Workflow 🚀")
render_stepper()

st.markdown("</div>", unsafe_allow_html=True)


# ------------------------------------------------------
# MAIN LAYOUT
# ------------------------------------------------------
col_left, col_right = st.columns([1.6, 1])

# LEFT SIDE — Pipeline
with col_left:

    st.markdown("### Step 1 — Upload PDF")
    uploaded = st.file_uploader("Upload PDF", type=["pdf"])
    if uploaded:
        st.session_state.pdf_bytes = uploaded.read()
        log("✅ PDF uploaded.")
        if st.session_state.step == 1:
            st.session_state.step = 2
            st.rerun()

    if st.session_state.step >= 2:
        st.markdown("---")
        st.markdown("### Step 2 — Extract PDF Data")
        if st.button("Extract PDF Data"):
            log("⚙️ Extracting PDF ...")
            with st.spinner("Reading PDF..."):
                data = extract_pdf_data(st.session_state.pdf_bytes)
            st.session_state.extracted_data = data
            log("✅ Extraction complete.")
            st.session_state.step = 3
            st.rerun()

    if st.session_state.step >= 3:
        st.markdown("---")
        st.markdown("### Step 3 — Preview Extracted JSON")
        st.json(st.session_state.extracted_data)

    if st.session_state.step >= 3:
        st.markdown("---")
        st.markdown("### Step 4 — Call API")
        if st.button("Send To API"):
            log("📡 Calling API ...")
            with st.spinner("Submitting request..."):
                api_result = call_api(st.session_state.extracted_data)
            st.session_state.api_result = api_result
            log("✅ API call successful.")
            st.session_state.step = 4
            st.rerun()

    if st.session_state.step >= 4:
        st.markdown("---")
        st.markdown("### ✅ Step 5 — Done")
        st.success("🎉 Workflow Completed Successfully!")
        st.json(st.session_state.api_result)
        st.session_state.step = 5


# RIGHT SIDE — Logs (Sticky)
with col_right:
    st.markdown("### 📟 Live Logs")
    render_logs()
