# src/builder.py
def reconstruct_latex(tailored_data, template_info):
    """Rebuilds the .tex file string from the tailored Python dictionary."""
    print("\n[5/7] 🏗️ Reconstructing the tailored LaTeX file...")

    # --- Reconstruct Skills Table ---
    skills_table = "\\begin{tabular}{ @{} >{\\bfseries}l @{\\hspace{4ex}} l }\n"
    for category, skills_list in tailored_data['skills'].items():
        skills_str = ", ".join(skills_list)
        skills_table += f"{category} & {skills_str} \\\\\n"
    skills_table += "\\end{tabular}"

    # --- Reconstruct Experience Section ---
    exp_section = ""
    for item in tailored_data['experience']:
        bullets = "\n".join([f"    \\item {point}" for point in item['description_points']])
        exp_section += f"""
\\textbf{{{item['title']}}} {item['details']}
\\vspace{{-6pt}}
\\begin{{itemize}}
    \\itemsep -6pt
{bullets}
\\end{{itemize}}
"""

    # --- Reconstruct Projects Section ---
    proj_section = ""
    for item in tailored_data['projects']:
        bullets = "\n".join([f"    \\item {point}" for point in item['description_points']])
        proj_section += f"""
\\textbf{{{item['title']}}} {item['details']}
\\vspace{{-6pt}}
\\begin{{itemize}}
    \\itemsep -6pt
{bullets}
\\end{{itemize}}
"""

    # --- Assemble the Final .tex File ---
    # We use the original template and inject our tailored sections
    final_tex = f"""
\\documentclass{{resume}}
\\usepackage[left=0.4in,top=0.4in,right=0.4in,bottom=0.4in]{{geometry}}
\\newcommand{{\\tab}}[1]{{\\hspace{{.2667\\textwidth}}\\rlap{{#1}}}}
\\newcommand{{\\itab}}[1]{{\\hspace{{0em}}\\rlap{{#1}}}}
\\name{{Rujul Dwivedi}}
\\address{{Phone: \\href{{tel:+919695133900}}{{+91 96951 33900}} • Email: \\href{{mailto:rujuldwivedi@icloud.com}}{{rujuldwivedi@icloud.com}}}}
\\address{{Portfolio: \\href{{https://rujuldwivedi.in}}{{rujuldwivedi.in}} • LinkedIn: \\href{{https://linkedin.com/in/rujuldwivedi}}{{linkedin.com/in/rujuldwivedi}} • GitHub: \\href{{https://github.com/rujuldwivedi}}{{github.com/rujuldwivedi}}}}
\\address{{\\textbf{{Bengaluru, India}}}}
\\begin{{document}}
\\vspace{{-6pt}}
% --- PROFILE ---
\\begin{{rSection}}{{Profile}}
{tailored_data['profile']}
\\end{{rSection}}
\\vspace{{-6pt}}
% --- EDUCATION ---
\\begin{{rSection}}{{Education}}
{{\\bf B.Tech in Mathematics \& Computer Science}}, \\textit{{Indian Institute of Technology Goa}} \\hfill {{Grad. July 2025}} \\\\
\\underline{{Coursework}}: System Design, Operating Systems, Networks, DBMS, Data Structures \& Algorithms
\\end{{rSection}}
\\vspace{{-6pt}}
% --- TECHNICAL SKILLS ---
\\begin{{rSection}}{{Technical Skills}}
{skills_table}
\\end{{rSection}}
\\vspace{{-6pt}}
% --- EXPERIENCE ---
\\begin{{rSection}}{{Experience}}
{exp_section}
\\end{{rSection}}
\\vspace{{-6pt}}
% --- PROJECTS ---
\\begin{{rSection}}{{Projects}}
{proj_section}
\\end{{rSection}}
\\vspace{{-6pt}}
% --- ACHIEVEMENTS ---
\\begin{{rSection}}{{Achievements}}
\\begin{{itemize}}
\\itemsep -6pt
\\item \\textbf{{Winner}}, Goa Police Hackathon - led team in building data-driven public safety solutions.
\\item \\textbf{{Finalist}}, Inter IIT Tech Meet - represented IIT Goa in industry-level ML challenges.
\\end{{itemize}}
\\end{{rSection}}
\\end{{document}}
"""
    final_tex_filename = "Rujul_Dwivedi_Resume_Tailored.tex"
    with open(final_tex_filename, "w") as f:
        f.write(final_tex)
    print(f"   ✅ Tailored LaTeX file '{final_tex_filename}' created.")
    return final_tex_filename
    # This function will now be cleaner. It will take tailored_data
    # and maybe some basic info from the original template and return
    # the final LaTeX string.
    pass # Placeholder for your function