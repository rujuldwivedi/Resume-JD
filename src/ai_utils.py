# src/ai_utils.py
import google.generativeai as genai
import json

def analyze_jd(jd_text, model):
    """Uses Gemini to analyze the JD and extract key info as JSON."""
    print("\n[3/7] 🧠 Analyzing the Job Description with Gemini Pro...")
    prompt = f"""
    You are a highly intelligent recruitment analyst. Analyze the following Job Description (JD).
    Your task is to extract the key information and structure it as a JSON object.
    Identify the following:
    1.  `role_title`: The official job title.
    2.  `company_name`: The name of the company.
    3.  `key_responsibilities`: A list of the main duties and tasks mentioned.
    4.  `hard_skills`: A list of specific technical skills, programming languages, frameworks, and tools required (e.g., Python, AWS, Kubernetes, Scikit-learn).
    5.  `soft_skills`: A list of non-technical skills mentioned (e.g., communication, leadership, teamwork, agile).
    6.  `keywords`: A list of other important keywords and concepts that an ATS might look for (e.g., 'scalability', 'data pipelines', 'microservices', 'CI/CD').

    Here is the Job Description:
    ---
    {jd_text}
    ---

    Please provide the output ONLY in a valid JSON format.
    """
    try:
        response = model.generate_content(prompt)
        clean_response = response.text.replace("```json", "").replace("```", "").strip()
        print("   ✅ Job Description analyzed.")
        return json.loads(clean_response)
    except Exception as e:
        print(f"❗️ Error analyzing JD: {e}")
        print("   Model Output:", response.text)
        return None
    pass # Placeholder for your function

def tailor_resume_section(section_name, original_content, jd_analysis_data, model):
    """Uses Gemini to rewrite a specific section of the resume."""
    print(f"   - Tailoring section: '{section_name}'...")
    # Convert dicts to strings for the prompt
    original_content_str = json.dumps(original_content, indent=2)
    jd_analysis_str = json.dumps(jd_analysis_data, indent=2)

    prompt = f"""
    You are an expert resume writer and career coach specializing in software engineering roles. Your task is to rewrite a section of a resume to be perfectly tailored for a specific job description, maximizing its ATS score and impact on recruiters.

    **Instructions:**
    1.  **Incorporate Keywords:** Naturally weave in relevant keywords, technologies, and concepts from the Job Description Analysis into the original resume content.
    2.  **Align with Responsibilities:** Rephrase bullet points to show how the candidate's experience directly addresses the key responsibilities of the new role.
    3.  **Quantify Impact:** Keep existing metrics and numbers. If a bullet point lacks a metric, frame it in terms of impact (e.g., "streamlined process," "enhanced system reliability").
    4.  **Mirror Language:** Adopt the professional tone and terminology used in the job description (e.g., use "architected," "deployed," "containerized" if they appear in the JD).
    5.  **Factual Integrity:** **CRITICAL**: Do NOT invent new skills, experiences, or metrics. You can only rephrase and reframe the information provided in the original content.
    6.  **Maintain Structure:** The output format MUST be identical to the input format of the original section. If you are given a string, return a JSON object with a single key "content" containing the string. If given a list of objects, return a JSON object with a single key "content" containing the rewritten list of objects.

    **Job Description Analysis:**
    ```json
    {jd_analysis_str}
    ```

    **Original Resume Section (`{section_name}`):**
    ```json
    {original_content_str}
    ```

    **Your Task:**
    Rewrite the `{section_name}` section based on all the instructions above. Provide ONLY the rewritten content inside a valid JSON object with a single key "content".
    For example: {{"content": "Rewritten profile string here."}} or {{"content": [{{rewritten_experience_object_1}}, {{...}}]}}
    """
    try:
        response = model.generate_content(prompt)
        clean_response = response.text.replace("```json", "").replace("```", "").strip()
        tailored_content = json.loads(clean_response)
        return tailored_content['content']
    except Exception as e:
        print(f"❗️ Error tailoring '{section_name}'. Returning original content. Error: {e}")
        print("   Model Output:", response.text)
        return original_content # Fallback
    pass # Placeholder for your function