import os
import glob

html_files = glob.glob('templates/*.html')
js_files = glob.glob('static/js/*.js')

for f in html_files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace('🤖 IA Assistente', 'IA Goole')
    content = content.replace('EV Assistente', 'Goole')
    content = content.replace('🤖', '<img src="/static/goole.png" style="width:100%;height:100%;object-fit:cover;border-radius:50%;background:white;"/>')
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

for f in js_files:
    if 'ia.js' in f:
        continue # handled separately below
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.replace('🤖 IA Assistente', 'IA Goole')
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

with open('static/js/ia.js', 'r', encoding='utf-8') as file:
    content = file.read()

content = content.replace('🤖 IA Assistente', 'IA Goole')
content = content.replace('ChargeGrid Assistant, seu assistente inteligente de recarga de VEs', 'Goole, o assistente inteligente da GoodWe')
content = content.replace("avatar.textContent = isAI ? '🤖' : '👤';", "if (isAI) {\n    avatar.innerHTML = '<img src=\"/static/goole.png\" style=\"width:100%;height:100%;object-fit:cover;border-radius:50%;background:white;\"/>';\n  } else {\n    avatar.textContent = '👤';\n  }")
content = content.replace('<div class="chat-avatar">🤖</div>', '<div class="chat-avatar"><img src="/static/goole.png" style="width:100%;height:100%;object-fit:cover;border-radius:50%;background:white;"/></div>')
with open('static/js/ia.js', 'w', encoding='utf-8') as file:
    file.write(content)
