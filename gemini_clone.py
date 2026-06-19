import streamlit as st
import google.generativeai as genai

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="Gemini Empire Elite", page_icon="✨", layout="wide")

# Custom CSS for premium layout
st.markdown("""
<style>
    .reportview-container { background: #131314; }
    .stChatInputContainer { padding-bottom: 20px; }
    .location-footer { position: fixed; bottom: 0; left: 0; width: 100%; text-align: center; color: #80868b; font-size: 12px; padding: 10px; background-color: #131314; z-index: 100; }
</style>
""", unsafe_allow_html=True)

# 2. AUTOMATIC API KEY COUPLING (Directly from your secrets.toml)
# Aapki file mein key jis naam se bhi ho, yeh system khud hi use connect kar lega
api_key = ""
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    elif "api_key" in st.secrets:
        api_key = st.secrets["api_key"]
    elif "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    pass

# API ko configure karna bina kisi warning message ke
if api_key:
    genai.configure(api_key=api_key)

# Initialize Session States for Active Chat and History Titles
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "recent_chats" not in st.session_state:
    st.session_state.recent_chats = []

# 3. SIDEBAR (Left Menu - Real-time Chat Tracker Only)
with st.sidebar:
    st.subheader("✨ Gemini Empire")
    st.write("---")
    
    # New Chat Button
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.chat_history = []
    
    st.write("---")
    st.subheader("🕒 Recent Chat History")
    
    # User jo bhi sawal poochega, uska title automatic yahan list hota jayega
    if st.session_state.recent_chats:
        for title in reversed(st.session_state.recent_chats):
            st.caption(f"💬 {title}")
    else:
        st.info("No recent chats yet. Start typing below!")

    st.write("---")
    with st.expander("⚙️ Settings"):
        st.selectbox("🎨 Theme", ["Dark Mode", "Light Mode"])

# 4. MAIN HEADER & TOP BAR
col_title, col_upgrade = st.columns([8, 2])
with col_title:
    st.title("Gemini ⚡")
with col_upgrade:
    st.button("✨ Upgrade to Advanced", type="primary", use_container_width=True)

str_line = "---"
st.write(str_line)

# 5. MODEL SELECTOR DROPDOWN
model_mapping = {
    "Gemini 2.5 Flash (Latest & Fast)": "gemini-2.5-flash",
    "Gemini 1.5 Pro (Thinking Level)": "gemini-1.5-pro"
}
selected_ui_model = st.selectbox("🤖 Select Model Level:", list(model_mapping.keys()))
actual_model_id = model_mapping[selected_ui_model]
st.info(f"Active Model: {selected_ui_model}")

# 6. DISPLAY ACTIVE CHAT MESSAGES
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])

# 7. CHAT INPUT BAR
st.write(str_line)
input_col, mic_col = st.columns([9, 1])

with input_col:
    user_query = st.chat_input("📌 Ask Gemini...")
with mic_col:
    st.button("🎙️", help="Voice Typing")

# 8. CORE AI PROCESSING
if user_query:
    # Key check validation block
    if not api_key:
        st.error("❌ Error: API Key aapki secrets.toml file mein nahi mili. Meharbani karke file check karein ya key confirm karein.")
    else:
        # Append to left sidebar summary title
        short_title = user_query[:25] + "..." if len(user_query) > 25 else user_query
        if short_title not in st.session_state.recent_chats:
            st.session_state.recent_chats.append(short_title)
            
        # Display user message
        with st.chat_message("user"):
            st.write(user_query)
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        
        # Generate response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            try:
                model_instance = genai.GenerativeModel(model_name=actual_model_id)
                response = model_instance.generate_content(user_query)
                ai_resp = response.text
                
                response_placeholder.write(ai_resp)
                st.session_state.chat_history.append({"role": "assistant", "content": ai_resp})
                
                # App ko immediate refresh karna taake side history sync ho jaye
                st.rerun()
                
            except Exception as e:
                response_placeholder.error(f"API Error (400/Invalid): {str(e)}")

# 9. FOOTER
st.markdown(
    '<div class="location-footer">📍 Lahore, Pakistan • From your IP address • <span style="color:#4285F4; cursor:pointer;">Update location</span></div>', 
    unsafe_allow_html=True
)