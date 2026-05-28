import re

with open('/Users/shreyasalimath/Desktop/multi-agent-rag/dashboard/app.py', 'r') as f:
    content = f.read()

old_style = '''html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif !important;
    background-color: #10141a !important;
    color: #d0dce8 !important;
    font-size: 15px !important;
}'''

new_style = '''html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif !important;
    background-color: #10141a !important;
    color: #d0dce8 !important;
    font-size: 20px !important;
}

p, li, div, span, label {
    font-size: 18px !important;
    line-height: 1.8 !important;
}

.stMarkdown p {
    font-size: 18px !important;
    line-height: 1.8 !important;
}

h1 { font-size: 2.6rem !important; margin-bottom: 0.5rem !important; }
h2 { font-size: 2rem !important; }
h3 { font-size: 1.6rem !important; }

.stButton > button {
    font-size: 18px !important;
    padding: 14px 28px !important;
    border-radius: 8px !important;
}

[data-testid="stTextArea"] textarea {
    font-size: 18px !important;
    line-height: 1.7 !important;
    padding: 16px !important;
}

[data-testid="stMetricValue"] {
    font-size: 2.8rem !important;
}

[data-testid="stMetricLabel"] {
    font-size: 16px !important;
}

.stTabs [data-baseweb="tab"] {
    font-size: 16px !important;
    padding: 12px 28px !important;
}

caption, .stCaption {
    font-size: 15px !important;
}'''

content = content.replace(old_style, new_style)

with open('/Users/shreyasalimath/Desktop/multi-agent-rag/dashboard/app.py', 'w') as f:
    f.write(content)

print("Done!")
