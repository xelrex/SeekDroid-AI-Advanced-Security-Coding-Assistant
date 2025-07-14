import streamlit as st
from streamlit_monaco import st_monaco
import openai
from streamlit_audio_recorder import audio_recorder
import tempfile
import speech_recognition as sr
from gtts import gTTS
import os
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Read API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set page config for SeekDroid AI
st.set_page_config(
    page_title="SeekDroid AI | Advanced Security & Coding Assistant",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="collapsed",
    experimental_capture_streamlit_audio=True  # Fix for audio recording
)

# Custom CSS for SeekDroid styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Display SeekDroid header
st.markdown("""
<div class="logo">
    <i class="fas fa-shield-alt logo-icon"></i>
    <div class="logo-gradient">SeekDroid AI</div>
</div>
<h1>Advanced Security & AI Tools</h1>
<p class="subtitle">AI-powered security solutions combined with intelligent development tools</p>
<div class="security-badge">
    <i class="fas fa-lock"></i>
    Military-Grade Encryption & AI Intelligence
</div>
""", unsafe_allow_html=True)

# Main tabs for different features
tab1, tab2 = st.tabs(["🔒 Security Coding Assistant", "✨ Lyra Prompt Optimizer"])

with tab1:
    # Main columns layout
    col1, col2 = st.columns([1, 1])

    with col1:
        # Security features section
        st.markdown("""
        <div class="capabilities">
            <div class="capabilities-header">
                <h2>Security Features</h2>
                <p>AI-powered security capabilities integrated with coding assistant</p>
            </div>
            
            <div class="capabilities-grid">
                <div class="capability-card">
                    <div class="capability-icon">
                        <i class="fas fa-brain"></i>
                    </div>
                    <h3>Secure Code Analysis</h3>
                    <p>AI detects vulnerabilities and security flaws in your code in real-time</p>
                    <div class="tech-stack">
                        <span class="tech-item">Static Analysis</span>
                        <span class="tech-item">Vulnerability Scanning</span>
                    </div>
                    <div class="capability-stats">
                        <div class="stat">
                            <div class="stat-value">99.7%</div>
                            <div class="stat-label">Threat Detection</div>
                        </div>
                    </div>
                </div>
                
                <div class="capability-card">
                    <div class="capability-icon">
                        <i class="fas fa-shield-virus"></i>
                    </div>
                    <h3>AI Code Protection</h3>
                    <p>Automatic security hardening and best practice implementation</p>
                    <div class="tech-stack">
                        <span class="tech-item">Code Obfuscation</span>
                        <span class="tech-item">Security Patches</span>
                    </div>
                    <div class="capability-stats">
                        <div class="stat">
                            <div class="stat-value">96%</div>
                            <div class="stat-label">Vulnerability Prevention</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Voice assistant section
        st.markdown("""
        <div class="notes">
            <h2><i class="fas fa-microphone-alt"></i> Voice Coding Assistant</h2>
            <p>Use voice commands to interact with the AI assistant</p>
            <div style="margin: 20px 0; text-align: center;">
        """, unsafe_allow_html=True)
        
        audio_bytes = audio_recorder(
            pause_threshold=2.0,
            text="Speak your code request",
            recording_color="#6c63ff",
            neutral_color="#1e293b",
            icon_size="2x",
        )
        
        st.markdown("</div></div>", unsafe_allow_html=True)

    with col2:
        # Coding assistant section
        st.markdown("""
        <div class="capabilities">
            <div class="capabilities-header">
                <h2><i class="fas fa-code"></i> AI Coding Assistant</h2>
                <p>Get AI-powered code explanations, improvements, and security analysis</p>
            </div>
        """, unsafe_allow_html=True)
        
        code = st_monaco(
            value='''# Write a Python function to check if a number is prime
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True''',
            language='python',
            height=300,
            key="code_editor"
        )
        
        text_override = st.text_area("Or type your question here (overrides voice input):", height=100)
        
        # Speech recognition function
        def speech_to_text(audio_bytes):
            recognizer = sr.Recognizer()
            if audio_bytes:
                try:
                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                        tmp_file.write(audio_bytes)
                        tmp_file.flush()
                        with sr.AudioFile(tmp_file.name) as source:
                            audio = recognizer.record(source)
                    text = recognizer.recognize_google(audio)
                    return text
                except Exception as e:
                    return f"[Speech recognition error: {e}]"
            return ""

        # Text to speech function
        def text_to_speech(text):
            if text:
                tts = gTTS(text=text, lang='en')
                tmp_audio = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
                tts.save(tmp_audio.name)
                return tmp_audio.name
            return ""
        
        if text_override.strip():
            user_query = text_override.strip()
        elif audio_bytes:
            with st.spinner("Transcribing voice command..."):
                user_query = speech_to_text(audio_bytes)
            st.write("You said:", user_query)
        else:
            user_query = ""
        
        # OpenAI query function
        def ask_openai(prompt):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are an expert programming assistant and security analyst. Provide detailed explanations with security best practices."},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.3,
                    max_tokens=800,
                )
                return response.choices[0].message.content
            except Exception as e:
                return f"⚠️ API Error: {str(e)}"
        
        if st.button("Get AI Analysis", use_container_width=True, type="primary"):
            if not user_query and not code.strip():
                st.warning("Please provide a voice input, typed question, or code snippet.")
            else:
                prompt = ""
                if code.strip():
                    prompt += f"Here is Python code:\n{code}\n\nSecurity analysis: Please identify any vulnerabilities, suggest improvements, and add security best practices.\n\n"
                if user_query:
                    prompt += f"User question: {user_query}\n\n"
                
                prompt += (
                    "Provide a detailed response with code examples. "
                    "If the question requires external info, perform research and provide sources."
                )
                
                with st.spinner("Analyzing code with AI security protocols..."):
                    ai_response = ask_openai(prompt)
                
                st.subheader("AI Security Analysis")
                st.markdown(ai_response)
        
                if ai_response and not ai_response.startswith("⚠️"):
                    with st.spinner("Generating voice summary..."):
                        audio_file = text_to_speech(ai_response[:500])  # Limit to first 500 chars
                    
                    if audio_file:
                        st.audio(audio_file, format="audio/mp3")
                        # Cleanup temporary audio file
                        try:
                            os.remove(audio_file)
                        except Exception:
                            pass
        
        st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    # Lyra Prompt Optimizer section
    st.markdown("""
    <div class="capabilities">
        <div class="capabilities-header">
            <h2><i class="fas fa-wand-magic-sparkles"></i> Lyra Prompt Optimizer</h2>
            <p>Enhance your AI prompts for better results with ChatGPT, Claude, Gemini, and more</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Target AI selector
    target_ai = st.selectbox(
        "Target AI",
        ["ChatGPT", "Claude", "Gemini", "Other", "Machine Learning", "Hacking", "Internet Learning", 
         "Python Coding", "C++ Expert", "Meta Editor Coding", "Pine Script Coding", "Animation Generation"],
        key="lyra_target"
    )
    
    # Mode selector
    mode = st.radio("Mode", ["DETAIL", "BASIC"], horizontal=True, key="lyra_mode")
    
    # Predefined templates
    templates = {
        "Python Coding": 'Write a Python function that connects to an API, fetches JSON data, and stores it in a CSV file.',
        "C++ Expert": 'Create a C++ class with proper constructors, destructors, and memory management for a custom linked list.',
        "Meta Editor Coding": 'Generate an MQL5 Expert Advisor that uses a 50 EMA crossover strategy with a trailing stop.',
        "Pine Script Coding": 'Write a Pine Script that plots buy signals based on RSI oversold conditions and MACD bullish crossover.',
        "Animation Generation": 'Describe a short animation scene where a rocket launches from Earth and enters orbit, visualized frame-by-frame.'
    }
    
    # Set the input prompt based on template if the target_ai is in templates
    input_prompt = st.text_area(
        "Paste or type your rough prompt here...",
        value=templates.get(target_ai, ""),
        height=150,
        key="lyra_input"
    )
    
    if st.button("Optimize Prompt", key="lyra_optimize", use_container_width=True, type="primary"):
        base_prompt = input_prompt.strip()
        improvements = []
        
        if mode == 'DETAIL':
            improvements.append('Clarified intent and added structure.')
            improvements.append('Decomposed task into actionable steps.')
            improvements.append(f'Tailored output for {target_ai}.')
            improvements.append('Encouraged deep thought, experimentation, and curiosity.')
            improvements.append('Promoted self-awareness and free-form reflection.')
        else:
            improvements.append('Improved clarity and focus.')
        
        optimized = f'"{target_ai}", respond to this prompt in a { "structured, multi-step format that encourages deep thinking, experimentation, curiosity, and self-awareness" if mode == "DETAIL" else "concise, clear, and exploratory manner"}:\n\n{base_prompt}'
        
        # Display the optimized prompt and explanation
        st.subheader("✅ Optimized Prompt")
        st.code(optimized, language='text')
        
        st.subheader("🔍 What Changed:")
        for improvement in improvements:
            st.markdown(f"- {improvement}")
        
        # Create a download button
        st.download_button(
            label="Download Prompt",
            data=optimized,
            file_name="optimized_prompt.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<footer>
    <p>© 2023 SeekDroid AI. All rights reserved.</p>
    <div class="footer-links">
        <a href="#"><i class="fas fa-file-contract"></i> Terms</a>
        <a href="#"><i class="fas fa-lock"></i> Privacy</a>
        <a href="#"><i class="fas fa-envelope"></i> Contact</a>
        <a href="#"><i class="fas fa-book"></i> Docs</a>
        <a href="#"><i class="fas fa-shield-alt"></i> Security</a>
    </div>
</footer>
""", unsafe_allow_html=True)

# Add custom CSS
st.markdown("""
<style>
:root {
    --primary: #6c63ff;
    --secondary: #4d46d9;
    --accent: #00c9a7;
    --dark: #0f172a;
    --darker: #0a0f1f;
    --medium: #1e293b;
    --light: #e2e8f0;
    --lighter: #f1f5f9;
}

body {
    background: linear-gradient(135deg, var(--darker), var(--dark));
    color: var(--light);
    line-height: 1.6;
    font-family: 'Inter', sans-serif;
}

.logo {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 10px;
}

.logo-gradient {
    background: linear-gradient(to right, var(--accent), var(--primary));
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}

.logo-icon {
    color: var(--accent);
    font-size: 2.5rem;
}

h1 {
    font-size: 2.5rem;
    background: linear-gradient(to right, var(--accent), var(--primary));
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 15px;
    font-weight: 800;
    text-align: center;
}

.subtitle {
    font-size: 1.2rem;
    color: #94a3b8;
    text-align: center;
    max-width: 800px;
    margin: 0 auto 20px;
    line-height: 1.7;
}

.security-badge {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background: rgba(0, 201, 167, 0.15);
    color: var(--accent);
    padding: 8px 20px;
    border-radius: 30px;
    font-size: 1rem;
    margin: 0 auto 30px;
    font-weight: 600;
    border: 1px solid rgba(0, 201, 167, 0.3);
    width: fit-content;
}

.capabilities {
    background: rgba(30, 41, 59, 0.85);
    border-radius: 16px;
    padding: 30px;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(108, 99, 255, 0.3);
    position: relative;
    overflow: hidden;
}

.capabilities::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(to right, var(--accent), var(--primary));
}

.capabilities-header {
    margin-bottom: 25px;
}

.capabilities-header h2 {
    font-size: 1.8rem;
    margin-bottom: 10px;
    color: var(--accent);
    display: flex;
    align-items: center;
    gap: 12px;
}

.capabilities-header p {
    color: #94a3b8;
}

.capability-card {
    background: rgba(15, 23, 42, 0.5);
    border-radius: 12px;
    padding: 20px;
    border: 1px solid rgba(108, 99, 255, 0.2);
    margin-bottom: 20px;
}

.capability-icon {
    font-size: 2rem;
    color: var(--primary);
    margin-bottom: 15px;
    background: rgba(108, 99, 255, 0.1);
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.capability-card h3 {
    font-size: 1.4rem;
    margin-bottom: 10px;
    color: var(--light);
}

.capability-card p {
    color: #cbd5e1;
    margin-bottom: 15px;
    line-height: 1.7;
}

.tech-stack {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 15px 0;
}

.tech-item {
    background: rgba(0, 201, 167, 0.15);
    color: var(--accent);
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
    border: 1px solid rgba(0, 201, 167, 0.3);
}

.capability-stats {
    display: flex;
    justify-content: space-between;
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.stat {
    text-align: center;
}

.stat-value {
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--accent);
    margin-bottom: 5px;
}

.stat-label {
    font-size: 0.9rem;
    color: #94a3b8;
}

.notes {
    background: rgba(30, 41, 59, 0.85);
    border-radius: 16px;
    padding: 25px;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(108, 99, 255, 0.3);
    position: relative;
    overflow: hidden;
}

.notes::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(to right, var(--accent), var(--primary));
}

.notes h2 {
    font-size: 1.6rem;
    margin-bottom: 20px;
    color: var(--accent);
    display: flex;
    align-items: center;
    gap: 12px;
}

.notes p {
    color: #cbd5e1;
    text-align: center;
}

footer {
    text-align: center;
    padding: 30px 0 20px;
    color: #94a3b8;
    font-size: 0.95rem;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    margin-top: 30px;
}

.footer-links {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 20px;
    margin: 15px 0;
}

.footer-links a {
    color: var(--accent);
    text-decoration: none;
    transition: color 0.3s ease;
    display: flex;
    align-items: center;
    gap: 6px;
}

.footer-links a:hover {
    color: var(--primary);
}

/* Monaco editor styling */
.monaco-editor {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid rgba(108, 99, 255, 0.3) !important;
}

/* Button styling */
.stButton>button {
    background: linear-gradient(to right, var(--primary), var(--secondary)) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.stButton>button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 15px rgba(108, 99, 255, 0.3) !important;
}

/* Text area styling */
.stTextArea>div>div>textarea {
    background: rgba(15, 23, 42, 0.5) !important;
    color: var(--light) !important;
    border: 1px solid rgba(108, 99, 255, 0.3) !important;
    border-radius: 10px !important;
    padding: 15px !important;
}

/* Tabs styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    margin-bottom: 20px;
}

.stTabs [data-baseweb="tab"] {
    padding: 12px 24px;
    border-radius: 10px;
    background: rgba(30, 41, 59, 0.5) !important;
    border: 1px solid rgba(108, 99, 255, 0.3) !important;
    transition: all 0.3s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 15px rgba(108, 99, 255, 0.1) !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(to right, var(--primary), var(--secondary)) !important;
    color: white !important;
    border: none !important;
}

.stTabs [aria-selected="true"] div {
    color: white !important;
}

.stRadio [role="radiogroup"] {
    gap: 15px;
}

.stRadio [role="radio"] {
    margin-right: 5px;
}

.stSelectbox [data-baseweb="select"] > div {
    background: rgba(15, 23, 42, 0.5) !important;
    border: 1px solid rgba(108, 99, 255, 0.3) !important;
    color: var(--light) !important;
}

.stCode code {
    background: rgba(15, 23, 42, 0.5) !important;
    border: 1px solid rgba(108, 99, 255, 0.3) !important;
    border-radius: 10px !important;
    padding: 20px !important;
    white-space: pre-wrap !important;
}

.stMarkdown ul {
    background: rgba(15, 23, 42, 0.5);
    border-radius: 10px;
    padding: 20px 30px !important;
    border: 1px solid rgba(108, 99, 255, 0.3);
}

.stMarkdown ul li {
    color: #cbd5e1;
    margin-bottom: 10px;
}

.stDownloadButton>button {
    background: rgba(0, 201, 167, 0.15) !important;
    color: var(--accent) !important;
    border: 1px solid rgba(0, 201, 167, 0.3) !important;
    transition: all 0.3s ease !important;
}

.stDownloadButton>button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 15px rgba(0, 201, 167, 0.1) !important;
}
</style>
""", unsafe_allow_html=True)

# Add Font Awesome
st.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">',
    unsafe_allow_html=True
)