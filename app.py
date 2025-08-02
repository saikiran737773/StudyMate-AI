import streamlit as st
import pdfplumber
from qna import get_answer
from roadmap import generate_roadmap
from ats import analyze_resume

st.set_page_config(
    page_title="StudyMate - AI Study Companion",
    page_icon="📚",
    layout="wide"
)

# Custom CSS for modern look
st.markdown("""
<style>
/* Main sidebar background container */
section[data-testid="stSidebar"] {
    background-color: #000408 !important; /* slightly lighter than the dark section */
    padding: 2rem 1rem;
    box-shadow: 2px 0 8px rgba(0,0,0,0.05);
}

/* Hide default radio buttons */
.stRadio > div > label > div:first-child {
    display: none;
}

/* Style the radio text to look like modern menu */
.stRadio > div > label {
    font-weight: 600;
    color: #2d3748;
    padding: 10px 15px;
    border-radius: 12px;
    transition: background 0.3s ease;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* Hover effect for menu items */
.stRadio > div > label:hover {
    background-color: #e2e8f0;
    cursor: pointer;
}

/* Selected item */
.stRadio > div > label[data-selected="true"] {
    background-color: #d1d9e6 !important;
    color: #1a202c !important;
}

/* Sidebar title */
section[data-testid="stSidebar"] .css-1v0mbdj {
    font-size: 1.4rem;
    font-weight: bold;
    color: #2b2f38;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Title and Description
st.title("📚 StudyMate")
st.subheader("Your Personalized AI Study Companion")
st.markdown("Get smart answers from your notes, build a custom learning roadmap, and optimize your resume with AI!")

# Sidebar Navigation
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio(
    "Choose a Feature",
    ("📄 PDF Q&A", "🧭 Roadmap Generator", "📝 ATS Resume Checker")
)

# --- Feature 1: PDF Q&A ---
if page == "📄 PDF Q&A":
    st.header("📄 Ask Questions from Your Study Material")
    st.markdown("Upload your notes or textbooks in PDF format and ask questions directly. StudyMate will answer using the content of the file.")

    uploaded_pdf = st.file_uploader("Upload a PDF", type="pdf")
    user_question = st.text_input("❓ Enter your question about the document")

    if uploaded_pdf and user_question:
        st.info("🔍 Extracting text from PDF...")
        with pdfplumber.open(uploaded_pdf) as pdf:
            context = ""
            for page in pdf.pages:
                context += page.extract_text() or ""

        if context.strip():
            st.info("🤖 Generating Answer...")
            try:
                answer = get_answer(user_question, context)
                st.success(f"✅ Answer: {answer}")
            except Exception as e:
                st.error(f"⚠️ Error while processing: {e}")
        else:
            st.warning("The uploaded PDF has no readable text.")
    else:
        st.warning("Please upload a PDF and enter a question.")

# --- Feature 2: Roadmap Generator ---
elif page == "🧭 Roadmap Generator":
    st.title("📍 Personalized Career Roadmap Generator")

    st.markdown("Get a step-by-step learning plan tailored to **you**.")

    name = st.text_input("🧑‍🎓 Your Name", placeholder="e.g. Akhil")
    skills = st.text_area("🛠️ Your Current Skills", placeholder="e.g. Python, HTML, SQL")
    goal = st.text_input("🎯 Your Career Goal", placeholder="e.g. Become a Full Stack Developer")

    if st.button("Generate Roadmap"):
        if not name or not skills or not goal:
            st.warning("Please fill in all fields: Name, Skills, and Goal.")
        else:
            with st.spinner("Generating your personalized roadmap..."):
                roadmap = generate_roadmap(name, skills, goal)
            st.success("✅ Roadmap Generated!")
            st.markdown(f"### 📘 Roadmap for **{name}**")
            st.write(roadmap)

# --- Feature 3: ATS Resume Checker ---
elif page == "📝 ATS Resume Checker":
    st.title("🤖 ATS Resume Bot")

    st.markdown("Upload your resume PDF and get instant feedback from an AI-powered ATS bot.")

    uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])
    job_description = st.text_area("💼 Optional: Paste a Job Description", height=200)

    if st.button("Analyze Resume"):
        if not uploaded_file:
            st.warning("Please upload a resume PDF.")
        else:
            with pdfplumber.open(uploaded_file) as pdf:
                resume_text = "\n".join(page.extract_text() or "" for page in pdf.pages)

            with st.spinner("Analyzing your resume..."):
                result = analyze_resume(resume_text, job_description)
            
            st.success("✅ Analysis Complete!")
            st.markdown("### 📊 ATS Feedback")
            st.write(result)
