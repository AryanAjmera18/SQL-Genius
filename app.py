import streamlit as st
from pathlib import Path
from sqlalchemy import create_engine
import sqlite3

# LangChain imports (latest structure)
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain.agents.agent_types import AgentType
from langchain_groq import ChatGroq

# --- Streamlit UI Setup ---
st.set_page_config(page_title="💬 Chat with SQL DB using LangChain", layout="wide")
st.markdown("<h1 style='text-align: center;'>🦜💬 LangChain SQL Chat Assistant</h1>", unsafe_allow_html=True)

# Constants
LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"
radio_opt = ["Use SQLite (student.db)", "Connect to your MySQL Database"]

# --- Sidebar Inputs ---
with st.sidebar:
    st.header("🔧 Configuration")
    selected_opt = st.radio("Select a database", radio_opt)

    if radio_opt.index(selected_opt) == 1:
        db_uri = MYSQL
        mysql_host = st.text_input("MySQL Host")
        mysql_user = st.text_input("MySQL Username")
        mysql_password = st.text_input("MySQL Password", type="password")
        mysql_db = st.text_input("MySQL Database Name")
    else:
        db_uri = LOCALDB

    api_key = st.text_input("🔐 GROQ API Key", type="password")

    if not api_key:
        st.warning("Please provide your GROQ API key to continue.")
        st.stop()

# --- Initialize LLM ---
llm = ChatGroq(groq_api_key=api_key, model_name="Llama3-8b-8192", streaming=True)

# --- DB Configuration ---
@st.cache_resource(ttl="2h")
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri == LOCALDB:
        dbfilepath = (Path(__file__).parent / "student.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri == MYSQL:
        if not all([mysql_host, mysql_user, mysql_password, mysql_db]):
            st.error("⚠️ Please provide all MySQL connection details.")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))

db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db) if db_uri == MYSQL else configure_db(db_uri)

# --- Agent Setup ---
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)

# --- Chat Session ---
if "messages" not in st.session_state or st.sidebar.button("🔄 Clear Chat History"):
    st.session_state["messages"] = [{"role": "assistant", "content": "👋 Hello! Ask me anything about your database."}]

# --- Display Chat Messages ---
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- User Input Handling ---
user_query = st.chat_input("💬 Ask your database something...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container())
        try:
            response = agent.run(user_query, callbacks=[st_cb])
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Try to format response as a table if it's a SQL SELECT result
            if response.strip().startswith("[(") and response.strip().endswith(")]"):
                try:
                    import ast, pandas as pd
                    data = ast.literal_eval(response)
                    df = pd.DataFrame(data)
                    st.dataframe(df, use_container_width=True)
                except:
                    st.markdown(response)
            else:
                st.markdown(response)
        except Exception as e:
            st.error(f"❌ Error processing query: {e}")
