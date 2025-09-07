# main.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Import your custom modules
from src.parser import parse_latex_resume
from src.ai_utils import analyze_jd, tailor_resume_section
from src.builder import reconstruct_latex
from src.compiler import compile_latex_to_pdf

def main():
    # 1. SETUP
    print("🚀 Starting the Chameleon AI Resume Tailor...")
    load_dotenv() # Loads the .env file with your API key
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found. Please create a .env file and add it.")
    genai.configure(api_key=GOOGLE_API_KEY)

    # Initialize the Gemini Model
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    
    # Define file paths
    base_resume_path = 'resume_template/main.tex'
    jd_path = 'job_description.txt'
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    # 2. READ INPUTS
    print(f"🧐 Reading base resume from '{base_resume_path}'...")
    base_resume_data = parse_latex_resume(base_resume_path)

    print(f"📝 Reading job description from '{jd_path}'...")
    with open(jd_path, 'r') as f:
        job_description = f.read()

    # 3. RUN AI PIPELINE
    print("🧠 Analyzing Job Description...")
    jd_analysis = analyze_jd(job_description, model)

    if not jd_analysis:
        print("❌ Could not analyze job description. Exiting.")
        return

    print("✨ Tailoring resume sections...")
    tailored_data = base_resume_data.copy()
    tailored_data['profile'] = tailor_resume_section('profile', base_resume_data['profile'], jd_analysis, model)
    tailored_data['experience'] = tailor_resume_section('experience', base_resume_data['experience'], jd_analysis, model)
    tailored_data['projects'] = tailor_resume_section('projects', base_resume_data['projects'], jd_analysis, model)

    # 4. BUILD AND COMPILE
    print("🏗️ Reconstructing tailored LaTeX file...")
    final_tex_string = reconstruct_latex(tailored_data)

    print("📄 Compiling the final PDF...")
    final_pdf_path = compile_latex_to_pdf(final_tex_string, output_dir, jd_analysis)
    
    if final_pdf_path:
        print(f"\n🎉 Success! Your tailored resume is ready: {final_pdf_path}")
    else:
        print("\n❌ Failed to generate PDF.")


if __name__ == "__main__":
    main()
    
# At the end of your main() function in main.py

if final_pdf_path:
    print(f"\n🎉 Success! Your tailored resume is ready: {final_pdf_path}")
    # THIS IS THE CRUCIAL LINE FOR THE GITHUB ACTION
    print(f"::set-output name=pdf_path::{final_pdf_path}")
else:
    print("\n❌ Failed to generate PDF.")