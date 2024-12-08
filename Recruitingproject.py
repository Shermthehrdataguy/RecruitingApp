import streamlit as st
import pandas as pd
import PyPDF2

# Custom CSS for Styling
st.markdown("""
    <style>
        /* Customize the title and background */
        .main {
            background-color: #f5f5f5;
        }
        h1 {
            color: #2c3e50;
            font-family: 'Arial Black', sans-serif;
            font-size: 2.5rem;
        }
        .sidebar .sidebar-content {
            background-color: #2c3e50;
            color: white;
        }
        .stButton button {
            background-color: #2ecc71;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 1rem;
            font-weight: bold;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #27ae60;
        }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.title("🚀 Recruiter Candidate Sorting Tool")
st.markdown(
    """
    **Empower your hiring process** with an AI-powered tool that helps recruiters:
    - Upload and parse resumes instantly.
    - Apply advanced filters and scoring.
    - Identify top candidates in seconds!
    """
)

# File Upload Section
st.markdown("## 📂 Upload Candidate Resumes")
uploaded_files = st.file_uploader(
    "Upload resumes (PDF or CSV format)",
    type=["pdf", "csv"],
    accept_multiple_files=True,
    help="Drag and drop files here or click to upload.",
)

# Process Uploaded Files
candidate_data = []

def parse_pdf(file):
    """Extract text from a PDF file."""
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

if uploaded_files:
    for file in uploaded_files:
        if file.type == "application/pdf":
            resume_text = parse_pdf(file)
            candidate_data.append({"Name": file.name, "Resume": resume_text})
        elif file.type == "text/csv":
            csv_data = pd.read_csv(file)
            candidate_data.extend(csv_data.to_dict(orient="records"))
    st.success(f"Successfully processed {len(uploaded_files)} file(s)!")

# Sidebar Filters
st.sidebar.title("🎯 Candidate Filters")
min_experience = st.sidebar.slider("Minimum Years of Experience", 0, 20, 2)
desired_skills = st.sidebar.text_input("Enter desired skills (comma-separated)").lower().split(',')

# Candidate Results Section
if candidate_data:
    st.markdown("## 🏆 Ranked Candidates")
    st.write("### Candidates filtered and ranked based on your criteria:")

    def rank_candidates(candidates, skills):
        """Rank candidates based on skill match."""
        for candidate in candidates:
            resume_text = candidate["Resume"].lower()
            candidate["Score"] = sum(skill.strip() in resume_text for skill in skills if skill)
        return sorted(candidates, key=lambda x: x["Score"], reverse=True)

    ranked_candidates = rank_candidates(candidate_data, desired_skills)

    for idx, candidate in enumerate(ranked_candidates, start=1):
        st.markdown(
            f"""
            **{idx}. Name:** {candidate['Name']}  
            **Relevance Score:** {candidate['Score']}  
            **Resume Preview:** {candidate['Resume'][:300]}...
            """
        )

# Call-to-Action
st.markdown("---")
st.markdown(
    """
    ### 💼 Ready to Revolutionize Hiring? Call Sherman Lee and
    Take the guesswork out of recruitment with our **AI-driven tool**.  
    👉 [Request a Demo](#) or [Contact Us](#) today to see it in action.
    """
)
