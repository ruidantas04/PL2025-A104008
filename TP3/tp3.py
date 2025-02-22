import re


def markdown_to_html(md_text):
    # Cabeçalhos
    md_text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', md_text, flags=re.MULTILINE)
    md_text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', md_text, flags=re.MULTILINE)

    # Bold
    md_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', md_text)

    # Itálico
    md_text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', md_text)

    # Lista numerada
    md_text = re.sub(r'(?m)^\d+\. (.+)$', r'<li>\1</li>', md_text)
    md_text = re.sub(r'(?:<li>.+?</li>\n?)+', lambda m: f'<ol>\n{m.group(0)}\n</ol>', md_text, flags=re.DOTALL)

    # Links
    md_text = re.sub(r' \[(.*?)\]\((.*?)\)', r' <a href="\2">\1</a>', md_text)

    # Imagens
    md_text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1"/>', md_text)



    return md_text


# Exemplo de uso
md_example = "# Exemplo"
md_example1 = "Este é um **exemplo** ..."
md_example2 =  "Este é um *exemplo* ..."
md_example3 = ("""1. Primeiro item
2. Segundo item
3. Terceiro item""")
md_example4 = "Como pode ser consultado em [página da UC](http://www.uc.pt)"
md_example5 = "Como se vê na imagem seguinte: ![imagem dum coelho](http://www.coellho.com) ..."


html_output = markdown_to_html(md_example)
html_output1 = markdown_to_html(md_example1)
html_output2 = markdown_to_html(md_example2)
html_output3 = markdown_to_html(md_example3)
html_output4 = markdown_to_html(md_example4)
html_output5 = markdown_to_html(md_example5)

print(html_output)
print(html_output1)
print(html_output2)
print(html_output3)
print(html_output4)
print(html_output5)
