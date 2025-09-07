# src/compiler.py
import subprocess
import os

def compile_latex_to_pdf(tex_string, output_dir, final_name_info):
    """Compiles the .tex file to a .pdf and renames it."""
    print("\n[6/7] 📄 Compiling the final PDF...")
    
    # Use a list of arguments for subprocess
    command = ["pdflatex", "-interaction=nonstopmode", tex_filename]
    
    # Run twice to ensure all references (if any) are correctly generated
    compilation_result = subprocess.run(command, capture_output=True, text=True)
    compilation_result = subprocess.run(command, capture_output=True, text=True)

    if compilation_result.returncode != 0:
        print("--- ❗️ LaTeX Compilation Failed ---")
        log_file = tex_filename.replace(".tex", ".log")
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                print(f"   Showing last 20 lines of '{log_file}':\n---")
                # Print the tail of the log file which usually contains the error
                log_lines = f.readlines()
                for line in log_lines[-20:]:
                    print(line, end='')
                print("---")
        return None

    # Construct the final filename
    role = jd_analysis.get('role_title', 'Role').replace(' ', '_').replace('/', '_')
    company = jd_analysis.get('company_name', 'Company').replace(' ', '_').replace('/', '_')
    base_name = os.path.splitext(tex_filename)[0]
    
    # Original PDF name from pdflatex
    original_pdf_name = f"{base_name}.pdf"
    final_pdf_name = f"Rujul_Dwivedi_Resume_{role}_{company}.pdf"
    
    try:
        os.rename(original_pdf_name, final_pdf_name)
        print(f"   ✅ PDF compiled and saved as: '{final_pdf_name}'")
        return final_pdf_name
    except OSError as e:
        print(f"❗️ Error renaming PDF: {e}")
        return None
    # It will take the LaTeX string, save it to a temp file in the
    # output directory, run pdflatex, and rename the final PDF.
    pass # Placeholder for your function