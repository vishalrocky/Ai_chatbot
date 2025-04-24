import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import warnings
warnings.filterwarnings('ignore')
load_dotenv()

# Sidebar Model Selection
st.sidebar.title("🧠 Model Selector")
selected_model = st.sidebar.selectbox(
    "Choose a model:",
    ["llama3-70b-8192",  "deepseek-r1-distill-llama-70b"],
    index=1
)

# Load selected model
LLM = ChatGroq(model=selected_model)

# Title and header
st.title("🌟 RockyBot 🪄")
st.header("Content Creation Assistant ✍️")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        SystemMessage(content="""
You are an AI assistant designed to help users create high-quality content for various purposes, such as blog posts, social media, articles, and more. Your name is ROCKY. Any non-content-related question should be ignored.
""")
    ]

# Chat input
query = st.chat_input("Type your message here...")

# 💅 Updated CSS for cleaner borders and chat layout
st.markdown("""
    <style>
        .chat-container {
            display: flex;
            flex-direction: column;
        }
        .chat-message {
            max-width: 70%;
            padding: 5px 10px;
            border-radius: 12px;
            margin: 8px;
        }
        .user-message {
            align-self: flex-end;
            background: linear-gradient(135deg, #E3FDF5, #FFE6FA);
            color: #333;
            border: 1px solid #A6DCEF;  /* Reduced border */
            text-align: right;
        }
        .ai-message {
            align-self: flex-start;
            background: linear-gradient(135deg, #FFF6E0, #D0F2FF);
            color: #000;
            border: 1px solid #FFC26F;  /* Reduced border */
        }
    </style>
""", unsafe_allow_html=True)


# Process the input
if query:
    try:
        human_message = HumanMessage(content=query)
        st.session_state.chat_history.append(human_message)

        with st.spinner("Rocky is thinking... 🧠✨"):
            response = LLM.invoke(st.session_state.chat_history)
            result = response.content

        if result:
            ai_message = AIMessage(content=result)
            st.session_state.chat_history.append(ai_message)

        # Display all chat messages
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        for message in st.session_state.chat_history:
            if isinstance(message, HumanMessage):
                st.markdown(f"<div class='chat-message user-message'>👤 You: {message.content}</div>", unsafe_allow_html=True)
            elif isinstance(message, AIMessage):
                st.markdown(f"<div class='chat-message ai-message'>🤖 ROCKY AI: {message.content}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Limit message history
        st.session_state.chat_history = st.session_state.chat_history[-100:]

    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.markdown("<div class='chat-message ai-message'>ROCKY: Oops! Something went wrong. Try again 💬</div>", unsafe_allow_html=True)

# Clear button
if st.button("Clear Chat"):
    st.session_state.chat_history = [
        SystemMessage(content="""You are an AI assistant designed to help users create high-quality content for various purposes, such as blog posts, social media, articles, and more. Your name is ROCKY. Any non-content-related question should be ignored.
""")
    ]
    st.rerun()
