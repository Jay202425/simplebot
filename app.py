import streamlit as st
from mistralai import Mistral

# Page configuration
st.set_page_config(
    page_title="Mistral AI Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
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
    st.title("⚙️ Settings")
    
    api_key_input = st.text_input(
        "Mistral API Key",
        value=st.session_state.api_key,
        type="password",
        help="Enter your Mistral AI API key"
    )
    
    if api_key_input:
        st.session_state.api_key = api_key_input
    
    model_choice = st.selectbox(
        "Select Model",
        ["mistral-small-latest", "mistral-medium-latest", "mistral-large-latest"],
        help="Choose the Mistral AI model"
    )
    
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Higher = more creative, Lower = more precise"
    )
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Main title
st.title("🤖 Mistral AI Bot")
st.markdown("---")

# Chat display
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate bot response
    try:
        client = Mistral(api_key=st.session_state.api_key)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
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
            message_placeholder.markdown(assistant_message)
        
        # Add assistant response to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_message
        })
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("Please check your API key and try again.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        Powered by <a href='https://mistral.ai'>Mistral AI</a>
    </div>
    """,
    unsafe_allow_html=True
)
