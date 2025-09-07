# src/parser.py
from pylatexenc.latexwalker import LatexWalker, LatexEnvironmentNode, LatexMacroNode, LatexCharsNode

def parse_latex_resume(file_path):
    """
    Parses the specific structure of your main.tex file.
    This is tailored to the rSection, itemize, and tabular environments.
    """
    print("\n[2/7] 🧐 Parsing your base LaTeX resume into a structured format...")
    with open(file_path, 'r') as f:
        content = f.read()

    lw = LatexWalker(content)
    # get_latex_nodes() returns a tuple, the first element is the root LatexNodesList
    nodelist, _, _ = lw.get_latex_nodes()

    resume_data = {"profile": "", "experience": [], "projects": [], "skills": {}}

    # Helper to get clean text from a nodelist
    def get_text(nodelist):
        return nodelist.latex_verbatim().strip()

    # Iterate directly over the root nodelist
    for node in nodelist:
        if node.isNodeType(LatexEnvironmentNode) and node.envname == 'rSection':
            section_title = get_text(node.nodeargs[0].nodelist)
            section_content_nodes = node.nodelist

            if section_title == 'Profile':
                # Assuming profile content is the first child node that is text or similar
                profile_content = ""
                for content_node in section_content_nodes:
                    if content_node.isNodeType(LatexCharsNode) or content_node.isNodeType(LatexMacroNode):
                        profile_content += get_text(LatexWalker(content_node.latex_verbatim()).get_latex_nodes()[0]) + " "
                resume_data['profile'] = profile_content.strip()


            elif section_title == 'Technical Skills':
                # Simplified parser for this specific 3x2 table
                # The table content is typically within a LatexEnvironmentNode (tabular)
                for sub_node in section_content_nodes:
                    if sub_node.isNodeType(LatexEnvironmentNode) and sub_node.envname == 'tabular':
                        # The rows are within the nodelist of the tabular environment
                        for row in sub_node.nodelist:
                             if row.isNodeType(LatexCharsNode) and '&' in row.chars:
                                parts = row.chars.split('&')
                                if len(parts) == 2:
                                    category = parts[0].strip().replace('\\textbf{', '').replace('}', '') # Clean category name
                                    skills = parts[1].replace('\\\\', '').strip()
                                    resume_data['skills'][category] = [s.strip() for s in skills.split(',')] # Split skills by comma


            elif section_title in ['Experience', 'Projects']:
                items = []
                current_item = {}
                # Iterate through nodes to group titles, details, and bullet points
                for sub_node in section_content_nodes:
                    if sub_node.isNodeType(LatexMacroNode) and sub_node.macroname == 'textbf':
                        # New item starts here. If previous item exists, save it.
                        if current_item:
                            items.append(current_item)
                        current_item = {'title': get_text(sub_node.nodeargs[0].nodelist), 'details': '', 'description_points': []}

                    elif sub_node.isNodeType(LatexCharsNode) and current_item and 'title' in current_item and not current_item.get('details'):
                        # This might capture text between \textbf and \vspace or \begin{itemize}
                        # Need to refine how 'details' is captured based on your specific .tex structure
                         current_item['details'] = sub_node.chars.strip()


                    elif sub_node.isNodeType(LatexEnvironmentNode) and sub_node.envname == 'itemize' and current_item:
                        bullets = []
                        for item_node in sub_node.nodelist:
                            if item_node.isNodeType(LatexMacroNode) and item_node.macroname == 'item':
                                bullet_text = get_text(item_node.nodeargs[0].nodelist) if item_node.nodeargs else ""
                                # Clean up formatting commands for the LLM
                                bullet_text = bullet_text.replace('\\textbf{', '').replace('}', '').replace('\\textit{', '').replace('}', '')
                                bullets.append(bullet_text.strip())
                        current_item['description_points'] = bullets

                # Append the last item
                if current_item:
                    items.append(current_item)

                if section_title == 'Experience':
                    resume_data['experience'] = items
                else: # Projects
                    resume_data['projects'] = items

    print("   ✅ Resume parsed successfully.")
    return resume_data