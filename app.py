import streamlit as st
from mistralai import Mistral
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Mistral AI Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with beautiful colors and styling
st.markdown("""
    <style>
    :root {
        --primary-color: #6366F1;
        --secondary-color: #EC4899;
        --accent-color: #F59E0B;
        --success-color: #10B981;
        --warning-color: #EF4444;
    }
    
    * {
        margin: 0;
        padding: 0;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .chat-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
    .stChatMessage {
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        animation: slideIn 0.3s ease-in-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
    }
    
    .assistant-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(245, 87, 108, 0.3);
    }
    
    .title-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
    }
    
    .title-container h1 {
        font-size: 3rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    }
    
    .title-container p {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    .sidebar-container {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(245, 87, 108, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(245, 87, 108, 0.5);
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #667eea;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #667eea;
        padding: 0.75rem;
    }
    
    .stSlider > div > div {
        border-radius: 10px;
    }
    
    .footer-text {
        text-align: center;
        color: white;
        padding: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-top: 2rem;
        font-size: 0.95rem;
    }
    
    .header-emoji {
        font-size: 2.5rem;
        margin-right: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key" not in st.session_state:
    st.session_state.api_key = "Mgkw2azh24EGH2iBA2AqDK5okbClIUVV"

# Sidebar configuration
with st.sidebar:
    st.markdown("""
        <div class="sidebar-container">
            <h2 style="color: white; margin-bottom: 1.5rem; text-align: center;">
                <span style="font-size: 2rem;">🤖</span><br/>
                AI Settings
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px; margin-bottom: 1rem; color: white; text-align: center;">
            <p style="margin: 0;">⚙️ <strong>Configure your AI Robot</strong></p>
        </div>
    """, unsafe_allow_html=True)
    
    api_key_input = st.text_input(
        "🔑 API Key",
        value=st.session_state.api_key,
        type="password",
        help="Enter your Mistral AI API key"
    )
    
    if api_key_input:
        st.session_state.api_key = api_key_input
    
    st.markdown("---")
    
    model_choice = st.selectbox(
        "🧠 AI Model",
        ["mistral-small-latest", "mistral-medium-latest", "mistral-large-latest"],
        help="Choose the Mistral AI model"
    )
    
    st.markdown("---")
    
    temperature = st.slider(
        "🌡️ Creativity Level",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher = more creative, Lower = more precise"
    )
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    st.markdown("---")
    st.markdown("""
        <div style="background: rgba(255, 255, 255, 0.1); padding: 1rem; border-radius: 10px; color: white; text-align: center;">
            <p style="margin: 0; font-size: 0.9rem;">💡 <strong>Tip:</strong> Adjust creativity for different responses!</p>
        </div>
    """, unsafe_allow_html=True)

# Main title with gradient background and robot theme
st.markdown("""
    <div class="title-container">
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <span style="font-size: 4rem; animation: bounce 2s infinite;">🤖</span>
        </div>
        <h1>Mistral AI Bot</h1>
        <p style="font-size: 1.2rem;">Your Intelligent AI Robot Assistant</p>
        <div style="margin-top: 1rem; display: flex; justify-content: center; gap: 1rem;">
            <span style="font-size: 2rem;">⚙️</span>
            <span style="font-size: 2rem;">🧠</span>
            <span style="font-size: 2rem;">💡</span>
        </div>
    </div>
    <style>
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }
    </style>
""", unsafe_allow_html=True)

# Chat display with better styling
chat_container = st.container()

with chat_container:
    if st.session_state.messages:
        st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.95); border-radius: 15px; padding: 2rem; margin-bottom: 2rem; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);">
        """, unsafe_allow_html=True)
        
        for idx, message in enumerate(st.session_state.messages):
            if message["role"] == "user":
                st.markdown(f"""
                    <div style="display: flex; justify-content: flex-end; margin-bottom: 1rem;">
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; padding: 1rem 1.5rem; max-width: 70%; box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);">
                            <strong>👤 You:</strong><br/>{message["content"]}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start; margin-bottom: 1rem;">
                        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; border-radius: 15px; padding: 1rem 1.5rem; max-width: 70%; box-shadow: 0 5px 15px rgba(245, 87, 108, 0.3);">
                            <strong>🤖 Bot:</strong><br/>{message["content"]}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="text-align: center; padding: 3rem; color: white;">
                <div style="font-size: 5rem; margin-bottom: 1rem; animation: pulse 2s infinite;">🤖</div>
                <h2 style="font-size: 2rem; margin-bottom: 1rem;">Welcome to Mistral Bot!</h2>
                <p style="font-size: 1.1rem; opacity: 0.9;">Start a conversation with your AI robot assistant</p>
                <p style="margin-top: 2rem; opacity: 0.7;">Ask me anything - I'm here to help! 💭</p>
                <div style="margin-top: 2rem; font-size: 1.5rem;">
                    <span style="margin: 0 0.5rem;">⚙️</span>
                    <span style="margin: 0 0.5rem;">🧠</span>
                    <span style="margin: 0 0.5rem;">💡</span>
                </div>
            </div>
            <style>
                @keyframes pulse {
                    0%, 100% { opacity: 1; transform: scale(1); }
                    50% { opacity: 0.8; transform: scale(1.05); }
                }
            </style>
        """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("💬 Ask me anything...", key="chat_input"):
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    
    # Display user message
    with st.chat_message("user", avatar="🧑"):
        st.markdown(prompt)
    
    # Generate bot response
    try:
        client = Mistral(api_key=st.session_state.api_key)
        
        with st.chat_message("assistant", avatar="🤖"):
            message_placeholder = st.empty()
            status_placeholder = st.empty()
            
            with status_placeholder.container():
                st.markdown("⏳ *Thinking...*")
            
            # Call the API
            response = client.chat.complete(
                model=model_choice,
                messages=[
                    {"role": msg["role"], "content": msg["content"]}
                    for msg in st.session_state.messages
                ],
                temperature=temperature
            )
            
            assistant_message = response.choices[0].message.content
            status_placeholder.empty()
            message_placeholder.markdown(assistant_message)
        
        # Add assistant response to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_message
        })
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("ℹ️ Please check your API key and try again.")

# Footer with gradient background and robot theme
st.markdown("---")
st.markdown("""
    <div class="footer-text">
        <div style="font-size: 3rem; margin-bottom: 1rem;">
            <span style="animation: rotate 3s linear infinite;">⚙️</span>
            <span style="margin: 0 1rem;">🤖</span>
            <span style="animation: rotate 3s linear infinite;">⚙️</span>
        </div>
        <h3>✨ Powered by Mistral AI Robot ✨</h3>
        <p>Advanced AI Language Model for Intelligent Conversations</p>
        <p style="margin-top: 1rem; font-size: 0.95rem;">
            Your intelligent robot assistant powered by cutting-edge AI technology
        </p>
        <p style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
            🔗 <a href='https://mistral.ai' style='color: white; text-decoration: none;'>Learn more about Mistral AI</a>
        </p>
        <p style="margin-top: 1rem; opacity: 0.7;">Made with ❤️ and 🤖</p>
    </div>
    <style>
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
""", unsafe_allow_html=True)
