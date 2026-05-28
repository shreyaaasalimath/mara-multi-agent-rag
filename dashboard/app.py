import streamlit as st
import sys, os
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from orchestrator import Orchestrator

st.set_page_config(page_title="MARA", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; background: #ffffff !important; color: #111 !important; }
body { zoom: 1.4; }
.stApp { background: #ffffff !important; }
#MainMenu, footer, header, [data-testid="stToolbar"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { background: #f9f9f9 !important; border-right: 1px solid #e5e5e5 !important; }
section[data-testid="stSidebar"] .block-container { padding: 1rem !important; }
section[data-testid="stSidebar"] * { font-size: 14px !important; color: #222 !important; }
.stTextArea textarea { font-size: 16px !important; padding: 14px !important; border: 1.5px solid #e0e0e0 !important; border-radius: 12px !important; background: #fafafa !important; color: #111 !important; resize: none !important; }
.stTextArea textarea:focus { border-color: #2563eb !important; background: #fff !important; box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important; }
.stButton > button { font-size: 15px !important; font-weight: 600 !important; padding: 10px 20px !important; border-radius: 10px !important; border: 1px solid #e0e0e0 !important; background: #f5f5f5 !important; color: #333 !important; width: 100% !important; }
.stButton > button:hover { background: #ebebeb !important; }
button[kind="primary"] { background: #2563eb !important; color: #fff !important; border: none !important; }
button[kind="primary"]:hover { background: #1d4ed8 !important; }
hr { border-color: #e5e5e5 !important; }
.stSpinner > div { border-top-color: #2563eb !important; }
div[data-testid="column"] { padding: 0 6px !important; }
</style>
""", unsafe_allow_html=True)

AGENT_COLORS = {
    "finance":  {"hex": "#16a34a", "light": "#f0fdf4", "border": "#bbf7d0"},
    "research": {"hex": "#2563eb", "light": "#eff6ff", "border": "#bfdbfe"},
    "legal":    {"hex": "#d97706", "light": "#fffbeb", "border": "#fde68a"},
}

def render_agent_card(r):
    c = AGENT_COLORS.get(r["domain"], {"hex": "#2563eb", "light": "#eff6ff", "border": "#bfdbfe"})
    conf = r.get("confidence", 50)
    conf_color = "#16a34a" if conf >= 75 else "#d97706" if conf >= 50 else "#dc2626"
    st.markdown(
        "<div style='background:" + c["light"] + ";border:1px solid " + c["border"] + ";"
        + "border-top:3px solid " + c["hex"] + ";border-radius:10px;padding:14px;margin-bottom:8px'>"
        + "<div style='font-weight:700;color:" + c["hex"] + ";font-size:13px;margin-bottom:6px'>"
        + r["domain"].upper() + " AGENT "
        + "<span style='color:" + conf_color + "'>" + str(conf) + "% conf</span></div>"
        + "<div style='font-size:14px;color:#222;line-height:1.75'>" + r["answer"] + "</div>"
        + "</div>",
        unsafe_allow_html=True
    )
    if r.get("sources"):
        st.caption("Sources: " + " · ".join(r["sources"]))

@st.cache_resource
def load_orchestrator():
    return Orchestrator()

with st.spinner("Loading..."):
    orch = load_orchestrator()

if "conversations" not in st.session_state:
    chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.conversations = {chat_id: {"title": "New Chat", "messages": []}}
    st.session_state.current_chat_id = chat_id

if "pending_query" not in st.session_state:
    st.session_state.pending_query = ""

if "auto_send" not in st.session_state:
    st.session_state.auto_send = False

def new_chat():
    chat_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.conversations[chat_id] = {"title": "New Chat", "messages": []}
    st.session_state.current_chat_id = chat_id
    st.session_state.pending_query = ""
    st.session_state.auto_send = False
    st.session_state.query_box = ""
    orch.clear_conversation()

stats = orch.get_session_stats()

# SIDEBAR
with st.sidebar:
    if st.button("New Chat", type="primary", use_container_width=True):
        new_chat()
        st.rerun()

    st.divider()
    st.markdown("**Recent Chats**")
    for cid, chat in sorted(st.session_state.conversations.items(), key=lambda x: x[0], reverse=True):
        is_current = cid == st.session_state.current_chat_id
        n = len(chat["messages"])
        label = (">> " if is_current else "") + chat["title"] + (" (" + str(n) + ")" if n > 0 else "")
        if st.button(label, key="chat_" + cid, use_container_width=True):
            st.session_state.current_chat_id = cid
            st.rerun()

    st.divider()
    st.markdown("**Agents**")
    for name, c in AGENT_COLORS.items():
        s = orch.agents[name].get_stats()
        active = stats and stats.get("agent_usage", {}).get(name, 0) > 0
        dot = "ON" if active else "OFF"
        st.markdown(
            "<div style='padding:8px 10px;margin-bottom:6px;border-radius:8px;"
            + "background:" + c["light"] + ";border-left:3px solid " + c["hex"] + "'>"
            + "<b style='color:" + c["hex"] + "'>" + name.upper() + "</b> "
            + "<span style='color:#888;font-size:12px'>" + str(s["total_queries"]) + " queries</span>"
            + "</div>",
            unsafe_allow_html=True
        )

    st.divider()
    st.markdown("**Knowledge Bases**")
    kb = {
        "finance":  ["apple_earnings.txt", "market_overview.txt", "nvidia_analysis.txt"],
        "research": ["transformer_paper.txt", "rag_paper.txt", "llm_scaling.txt"],
        "legal":    ["employment_contract.txt", "gdpr_summary.txt", "contract_law.txt"],
    }
    for domain, files in kb.items():
        c = AGENT_COLORS[domain]
        st.markdown("<b style='color:" + c["hex"] + ";font-size:13px'>" + domain.upper() + "</b>", unsafe_allow_html=True)
        for f in files:
            st.markdown("<span style='color:#888;font-size:12px;padding-left:8px'>· " + f + "</span>", unsafe_allow_html=True)

    if stats:
        st.divider()
        st.markdown("**Stats**")
        st.markdown(
            "<div style='font-size:13px;color:#555;line-height:2.2'>"
            + str(stats.get("total_queries", 0)) + " queries · "
            + str(stats.get("avg_latency", 0)) + "s avg<br>"
            + str(stats.get("total_tokens", 0)) + " tokens · "
            + str(stats.get("avg_confidence", 0)) + "% conf"
            + "</div>",
            unsafe_allow_html=True
        )

# MAIN
st.markdown("<div style='max-width:860px;margin:0 auto;padding:28px 24px 20px 24px'>", unsafe_allow_html=True)

current_chat = st.session_state.conversations[st.session_state.current_chat_id]
messages = current_chat["messages"]

if not messages:
    st.markdown(
        "<div style='text-align:center;padding:50px 0 32px'>"
        "<div style='font-size:3rem;margin-bottom:12px'>🤖</div>"
        "<h2 style='font-size:1.8rem;font-weight:700;color:#111;margin-bottom:8px'>How can I help you?</h2>"
        "<p style='color:#666;font-size:16px'>Ask anything across Finance, Research, and Legal.</p>"
        "</div>",
        unsafe_allow_html=True
    )
    examples = [
        ("💰", "What was Apple's revenue and gross margin?"),
        ("🔬", "How does the Transformer architecture work?"),
        ("⚖️",  "What are GDPR Tier 2 penalties?"),
        ("🤖", "How does RAG work and how is NVIDIA benefiting?"),
        ("📝", "What IP rights do employment contracts assign?"),
        ("📊", "Compare LLM scaling laws with Apple AI strategy"),
    ]
    col1, col2 = st.columns(2)
    for i, (icon, ex) in enumerate(examples):
        col = col1 if i % 2 == 0 else col2
        with col:
            if st.button(icon + " " + ex, key="ex_" + str(i), use_container_width=True):
                st.session_state.pending_query = ex
                st.session_state.auto_send = True
                st.rerun()

for turn in messages:
    res = turn["result"]

    st.markdown(
        "<div style='display:flex;justify-content:flex-end;margin:16px 0 8px'>"
        "<div style='background:#2563eb;color:#fff;border-radius:18px 18px 4px 18px;"
        "padding:14px 20px;max-width:75%;font-size:15px;line-height:1.65'>"
        + turn["query"]
        + "</div></div>",
        unsafe_allow_html=True
    )

    badges = " ".join([
        "<span style='background:" + AGENT_COLORS[a]["light"] + ";color:" + AGENT_COLORS[a]["hex"] + ";"
        + "border:1px solid " + AGENT_COLORS[a]["border"] + ";padding:2px 10px;"
        + "border-radius:20px;font-size:12px;font-weight:600'>" + a.upper() + "</span>"
        for a in res["agents_called"]
    ])
    st.markdown(
        "<div style='font-size:12px;color:#aaa;margin-bottom:10px;text-align:center'>"
        + "Routed to " + badges + " · " + str(res["total_latency_sec"]) + "s · " + str(res["total_tokens"]) + " tokens"
        + "</div>",
        unsafe_allow_html=True
    )

    agent_responses = res["agent_responses"]
    if len(agent_responses) > 1:
        cols = st.columns(len(agent_responses))
        for col, r in zip(cols, agent_responses):
            with col:
                render_agent_card(r)
    else:
        render_agent_card(agent_responses[0])

    oc = res.get("overall_confidence", 50)
    oc_color = "#16a34a" if oc >= 75 else "#d97706" if oc >= 50 else "#dc2626"
    st.markdown(
        "<div style='display:flex;justify-content:flex-start;margin:8px 0 28px'>"
        "<div style='background:#f8f9fa;border:1px solid #e5e5e5;"
        "border-radius:4px 18px 18px 18px;"
        "padding:18px 22px;max-width:85%;font-size:15px;line-height:1.85;color:#111'>"
        "<div style='font-size:12px;font-weight:700;color:#2563eb;margin-bottom:10px'>"
        "MARA &nbsp;·&nbsp; <span style='color:" + oc_color + "'>" + str(oc) + "% confidence</span></div>"
        + res["final_answer"]
        + "</div></div>",
        unsafe_allow_html=True
    )

st.divider()

input_col, btn_col = st.columns([6, 1])
with input_col:
    query = st.text_area(
        "",
        value=st.session_state.pending_query,
        placeholder="Ask anything...",
        height=80,
        label_visibility="collapsed",
        key="query_box"
    )
with btn_col:
    st.markdown("<div style='padding-top:6px'>", unsafe_allow_html=True)
    send = st.button("Send", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    "<p style='text-align:center;color:#bbb;font-size:12px;margin-top:8px'>MARA · Finance · Research · Legal</p>",
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)

auto_send = st.session_state.auto_send
if auto_send:
    st.session_state.auto_send = False

if (send or auto_send) and query.strip():
    st.session_state.pending_query = ""
    with st.spinner("Thinking..."):
        result = orch.run(query.strip())
    cid = st.session_state.current_chat_id
    st.session_state.conversations[cid]["messages"].append({
        "query": query.strip(),
        "result": result
    })
    if len(st.session_state.conversations[cid]["messages"]) == 1:
        title = query.strip()[:40] + ("..." if len(query.strip()) > 40 else "")
        st.session_state.conversations[cid]["title"] = title
    st.rerun()