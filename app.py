import streamlit as st
import zxcvbn
import re
import math
import random

# Page Configuration
st.set_page_config(
    page_title="SHIELD | Password Strength Analyser",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Memorable word list for passphrase generator
MEMORABLE_WORDS = [
    "apple", "banana", "cherry", "dragon", "eagle", "forest", "galaxy", "harbor", "island", "jungle",
    "knight", "lemon", "mountain", "nebula", "ocean", "planet", "quartz", "river", "shadow", "tiger",
    "valley", "wizard", "xenon", "yellow", "zenith", "alpha", "bravo", "castle", "delta", "echo",
    "falcon", "glacier", "horizon", "indigo", "joker", "koala", "lunar", "meteor", "nomad", "oasis",
    "phoenix", "radar", "safari", "tundra", "uranium", "vortex", "whisper", "matrix", "beacon", "canyon",
    "dune", "emerald", "frost", "geyser", "helix", "iron", "jade", "crater", "lagoon", "magma",
    "nova", "opal", "pulse", "reef", "solar", "timber", "ultra", "velvet", "wave", "alloy",
    "breeze", "cobalt", "dust", "ember", "flare", "gravity", "halo", "ion", "jasper", "kinetic",
    "lava", "mirage", "neon", "orbit", "plasma", "rust", "sonic", "titan", "vector", "warp",
    "anchor", "blaze", "comet", "drift", "flame", "glow", "hawk", "ice", "jolt", "laser",
    "mist", "nexus", "onyx", "prism", "ridge", "spark", "tide", "volt", "wind", "zenith"
]

# Custom CSS Injection for Premium Glassmorphic Design and UI Overrides
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

/* Main App Styles */
html, body, [class*="css"], .stApp {
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #0b0f19;
    color: #f1f5f9;
}

/* Glassmorphic Column Containers */
[data-testid="column"] {
    background: rgba(17, 24, 39, 0.45) !important;
    border-radius: 20px !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    padding: 30px !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.4) !important;
    margin-bottom: 24px !important;
    transition: all 0.3s ease;
}

[data-testid="column"]:hover {
    border-color: rgba(255, 255, 255, 0.12) !important;
    box-shadow: 0 15px 35px 0 rgba(0, 0, 0, 0.5) !important;
}

/* Reset nested columns so they don't look like outer cards */
[data-testid="column"] [data-testid="column"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    backdrop-filter: none !important;
    box-shadow: none !important;
    margin-bottom: 0 !important;
}

/* Custom Headers styling */
.app-header {
    text-align: center;
    padding: 30px 0 10px 0;
}
.app-title {
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #38bdf8, #818cf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
    letter-spacing: -1px;
}
.app-subtitle {
    font-size: 1.15rem;
    color: #94a3b8;
    font-weight: 300;
    margin-bottom: 30px;
}

/* Custom interactive strength meter */
.meter-container {
    margin: 24px 0;
}
.meter-label {
    display: flex;
    justify-content: space-between;
    font-weight: 600;
    font-size: 1rem;
    margin-bottom: 10px;
}
.meter-bg {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 9999px;
    height: 14px;
    width: 100%;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.08);
}
.meter-fill {
    height: 100%;
    border-radius: 9999px;
    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1), background-color 0.6s ease;
}

/* Checklist items styling */
.check-item {
    display: flex;
    align-items: center;
    margin-bottom: 14px;
    font-size: 0.98rem;
}
.check-icon {
    margin-right: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    font-size: 0.8rem;
    font-weight: bold;
    transition: all 0.3s ease;
}
.check-pass {
    background: rgba(16, 185, 129, 0.15);
    color: #10b981;
    border: 1px solid rgba(16, 185, 129, 0.3);
}
.check-fail {
    background: rgba(244, 63, 94, 0.1);
    color: #f43f5e;
    border: 1px solid rgba(244, 63, 94, 0.2);
    opacity: 0.75;
}
.check-text-pass {
    color: #f8fafc;
}
.check-text-fail {
    color: #94a3b8;
    opacity: 0.8;
}

/* Crack Time Grid cards */
.crack-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    margin-top: 15px;
}
.crack-card {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 14px;
    padding: 16px;
    text-align: center;
    transition: all 0.3s ease;
}
.crack-card:hover {
    background: rgba(255, 255, 255, 0.04);
    border-color: rgba(255, 255, 255, 0.1);
}
.crack-title {
    font-size: 0.8rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
    font-weight: 600;
}
.crack-time {
    font-size: 1.15rem;
    color: #f8fafc;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}

/* Informational metrics */
.metric-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 20px;
    background: rgba(255, 255, 255, 0.02);
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.05);
    margin-top: 15px;
}
.metric-value {
    font-size: 1.4rem;
    font-weight: 700;
    color: #38bdf8;
    font-family: 'JetBrains Mono', monospace;
}

/* Streamlit component style overrides to fix text contrast issues */
div[data-testid="stTextInput"] div[data-baseweb="input"] {
    background-color: #0f172a !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 10px !important;
}
div[data-testid="stTextInput"] input {
    background-color: #0f172a !important;
    color: #ffffff !important;
    font-family: 'JetBrains Mono', monospace !important;
}
div[data-testid="stTextInput"] input::placeholder {
    color: #64748b !important;
}

/* Custom styled inputs for Selectbox dropdowns */
div[data-baseweb="select"] {
    background-color: #0f172a !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 10px !important;
}
div[data-baseweb="select"] > div {
    background-color: transparent !important;
    color: #ffffff !important;
}

/* General widget labels and radio/checkbox text color fixes */
label,
.stWidgetLabel,
[data-testid="stWidgetLabel"] p,
.stCheckbox p,
.stRadio p,
.stCheckbox span,
.stRadio span,
p {
    color: #e2e8f0 !important;
}

/* General button styling */
.stButton>button {
    background: linear-gradient(135deg, #6366f1, #4f46e5) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    width: 100% !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #4f46e5, #4338ca) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 16px rgba(79, 70, 229, 0.4) !important;
}

/* Custom styled small buttons in history logs */
div[data-testid="column"] div[data-testid="column"] button {
    padding: 4px 8px !important;
    font-size: 0.82rem !important;
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: none !important;
    color: #e2e8f0 !important;
    border-radius: 6px !important;
    margin-top: 2px !important;
}
div[data-testid="column"] div[data-testid="column"] button:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
    color: #ffffff !important;
    transform: none !important;
}

/* Feedback blocks */
.warning-box {
    background: rgba(239, 68, 68, 0.08);
    border-left: 4px solid #ef4444;
    padding: 16px;
    border-radius: 0 14px 14px 0;
    margin-top: 15px;
}
.warning-title {
    font-weight: 700;
    color: #fca5a5;
    margin-bottom: 4px;
    font-size: 0.95rem;
}
.warning-desc {
    color: #f1f5f9;
    font-size: 0.92rem;
}

.suggestion-box {
    background: rgba(245, 158, 11, 0.08);
    border-left: 4px solid #f59e0b;
    padding: 16px;
    border-radius: 0 14px 14px 0;
    margin-top: 15px;
}
.suggestion-title {
    font-weight: 700;
    color: #fde047;
    margin-bottom: 4px;
    font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)

# App Title & Header
st.markdown("""
<div class="app-header">
    <div class="app-title">🛡️ SHIELD</div>
    <div class="app-subtitle">A modern, secure password strength analyzer & smart generator</div>
</div>
""", unsafe_allow_html=True)

# Helper functions
def calculate_entropy(password):
    if not password:
        return 0, "Empty", "#64748b"
    
    pool = 0
    has_lower = False
    has_upper = False
    has_digit = False
    has_special = False
    
    for char in password:
        if char.islower():
            has_lower = True
        elif char.isupper():
            has_upper = True
        elif char.isdigit():
            has_digit = True
        else:
            has_special = True
            
    if has_lower: pool += 26
    if has_upper: pool += 26
    if has_digit: pool += 10
    if has_special: pool += 32
    
    entropy = len(password) * math.log2(pool) if pool > 0 else 0
    
    if entropy < 28:
        strength = "Very Weak"
        color = "#f43f5e"
    elif entropy < 36:
        strength = "Weak"
        color = "#fb923c"
    elif entropy < 60:
        strength = "Moderate"
        color = "#facc15"
    elif entropy < 128:
        strength = "Strong"
        color = "#4ade80"
    else:
        strength = "Very Strong"
        color = "#10b981"
        
    return round(entropy, 1), strength, color

def get_checklist_html(password):
    checks = [
        ("At least 8 characters", len(password) >= 8),
        ("Contains uppercase letter (A-Z)", bool(re.search(r"[A-Z]", password))),
        ("Contains lowercase letter (a-z)", bool(re.search(r"[a-z]", password))),
        ("Contains number (0-9)", bool(re.search(r"\d", password))),
        ("Contains special character (e.g. !@#$)", bool(re.search(r"[^A-Za-z0-9]", password))),
    ]
    
    html = ""
    for label, passed in checks:
        icon_class = "check-pass" if passed else "check-fail"
        icon_symbol = "✓" if passed else "✗"
        text_class = "check-text-pass" if passed else "check-text-fail"
        
        html += (
            f'<div class="check-item">'
            f'<span class="check-icon {icon_class}">{icon_symbol}</span>'
            f'<span class="{text_class}">{label}</span>'
            f'</div>'
        )
    return html

def get_strength_meter_html(score, password):
    if not password:
        return (
            '<div class="meter-container">'
            '<div class="meter-label">'
            '<span>Strength: <span style="color: #64748b;">No Password</span></span>'
            '<span>0%</span>'
            '</div>'
            '<div class="meter-bg">'
            '<div class="meter-fill" style="width: 0%; background: #475569;"></div>'
            '</div>'
            '</div>'
        )
        
    color_map = {
        0: ("linear-gradient(90deg, #f43f5e, #fda4af)", "20%", "Too Weak", "#f43f5e"),
        1: ("linear-gradient(90deg, #fb923c, #ffedd5)", "40%", "Weak", "#fb923c"),
        2: ("linear-gradient(90deg, #facc15, #fef9c3)", "60%", "Moderate", "#facc15"),
        3: ("linear-gradient(90deg, #4ade80, #d1fae5)", "80%", "Strong", "#4ade80"),
        4: ("linear-gradient(90deg, #10b981, #a7f3d0)", "100%", "Excellent", "#10b981")
    }
    
    gradient, width, strength_label, text_color = color_map.get(score, ("#475569", "0%", "None", "#64748b"))
    
    return (
        f'<div class="meter-container">'
        f'<div class="meter-label">'
        f'<span>Strength: <span style="color: {text_color}; font-weight: 800;">{strength_label}</span></span>'
        f'<span>{width}</span>'
        f'</div>'
        f'<div class="meter-bg">'
        f'<div class="meter-fill" style="width: {width}; background: {gradient};"></div>'
        f'</div>'
        f'</div>'
    )

def get_crack_times_html(crack_times):
    scenarios = [
        ("Online Throttled", crack_times.get("online_throttling_100_per_hour", "instant"), "🔒 rate-limited login"),
        ("Online Unthrottled", crack_times.get("online_no_throttling_10_per_second", "instant"), "🌐 API endpoint"),
        ("Offline Slow Hash", crack_times.get("offline_slow_hashing_1e4_per_second", "instant"), "💾 bcrypt/scrypt leak"),
        ("Offline Fast Hash", crack_times.get("offline_fast_hashing_1e10_per_second", "instant"), "🚀 GPU brute-force"),
    ]
    
    html = '<div class="crack-grid">'
    for title, time_val, description in scenarios:
        time_color = "#38bdf8"
        if "instant" in time_val or "second" in time_val or "minute" in time_val:
            time_color = "#f43f5e"
        elif "hour" in time_val or "day" in time_val:
            time_color = "#fb923c"
        elif "month" in time_val or "year" in time_val:
            time_color = "#facc15"
        else:
            time_color = "#4ade80"
            
        html += (
            f'<div class="crack-card">'
            f'<div class="crack-title">{title}</div>'
            f'<div class="crack-time" style="color: {time_color};">{time_val}</div>'
            f'<div style="font-size: 0.72rem; color: #64748b; margin-top: 4px;">{description}</div>'
            f'</div>'
        )
    html += '</div>'
    return html

def get_feedback_html(feedback):
    warning = feedback.get("warning", "")
    suggestions = feedback.get("suggestions", [])
    
    html = ""
    if warning:
        html += (
            f'<div class="warning-box">'
            f'<div class="warning-title">⚠️ Warning</div>'
            f'<div class="warning-desc">{warning}</div>'
            f'</div>'
        )
    if suggestions:
        suggestions_list = "".join([f"<li style='margin-bottom: 5px;'>{s}</li>" for s in suggestions])
        html += (
            f'<div class="suggestion-box">'
            f'<div class="suggestion-title">💡 Suggestions</div>'
            f'<ul style="margin: 0; padding-left: 15px; color: #cbd5e1; font-size: 0.9rem;">'
            f'{suggestions_list}'
            f'</ul>'
            f'</div>'
        )
    return html

def generate_random_password(length, use_upper, use_lower, use_nums, use_syms, exclude_ambig):
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nums = "0123456789"
    syms = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    if exclude_ambig:
        lower = "abcdefghijkmnopqrstuvwxyz"
        upper = "ABCDEFGHJKLMNOPQRSTUVWXYZ"
        nums = "23456789"
        
    char_pool = ""
    required_chars = []
    
    if use_lower:
        char_pool += lower
        required_chars.append(random.choice(lower))
    if use_upper:
        char_pool += upper
        required_chars.append(random.choice(upper))
    if use_nums:
        char_pool += nums
        required_chars.append(random.choice(nums))
    if use_syms:
        char_pool += syms
        required_chars.append(random.choice(syms))
        
    if not char_pool:
        return "Please select at least one character option!"
        
    rem_len = length - len(required_chars)
    if rem_len > 0:
        required_chars.extend(random.choices(char_pool, k=rem_len))
        
    random.shuffle(required_chars)
    return "".join(required_chars)

def generate_passphrase(num_words, separator, capitalize, append_num_sym):
    words = random.sample(MEMORABLE_WORDS, min(num_words, len(MEMORABLE_WORDS)))
    if capitalize:
        words = [w.capitalize() for w in words]
    else:
        words = [w.lower() for w in words]
        
    passphrase = separator.join(words)
    
    if append_num_sym:
        digit = random.choice("0123456789")
        symbol = random.choice("!@#$%^&*")
        passphrase += separator + digit + symbol
        
    return passphrase

# Initialize session states
if "password_input" not in st.session_state:
    st.session_state.password_input = ""
if "generated_password" not in st.session_state:
    st.session_state.generated_password = ""
if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []
if "generator_history" not in st.session_state:
    st.session_state.generator_history = []

# Callback to apply generated password to the analyzer
def apply_generated_password():
    st.session_state.password_input = st.session_state.generated_password
    st.session_state.password_input_widget = st.session_state.generated_password

# Columns layout
col_analyser, col_generator = st.columns([1.2, 1])

# Column 1: Analyser
with col_analyser:
    st.markdown('<h2 style="color:#38bdf8; font-weight:700; margin-top:0; font-size:1.8rem; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:10px; margin-bottom:20px;">🛡️ Analyser</h2>', unsafe_allow_html=True)
    
    # Checkbox to toggle visibility
    show_password = st.checkbox("Show password characters", value=False)
    
    # Password Input
    pwd_input = st.text_input(
        "Enter Password",
        value=st.session_state.password_input,
        type="default" if show_password else "password",
        placeholder="Type or paste a password here...",
        key="password_input_widget"
    )
    
    # Sync password input widget with session state
    st.session_state.password_input = pwd_input
    
    # Perform Strength Checks
    if st.session_state.password_input:
        res = zxcvbn.zxcvbn(st.session_state.password_input)
        score = res.get("score", 0)
        feedback = res.get("feedback", {})
        crack_times = res.get("crack_times_display", {})
        
        # Entropy & Strength Label
        entropy_val, ent_strength, ent_color = calculate_entropy(st.session_state.password_input)
        
        # Keep analysis history updated (intelligent updates without character duplication)
        hist = st.session_state.analysis_history
        if not hist or hist[0]["password"] != st.session_state.password_input:
            if hist and st.session_state.password_input.startswith(hist[0]["password"]):
                hist[0] = {
                    "password": st.session_state.password_input,
                    "strength": ent_strength,
                    "entropy": entropy_val,
                    "color": ent_color
                }
            else:
                st.session_state.analysis_history.insert(0, {
                    "password": st.session_state.password_input,
                    "strength": ent_strength,
                    "entropy": entropy_val,
                    "color": ent_color
                })
                st.session_state.analysis_history = st.session_state.analysis_history[:5]
        
        # Display custom strength meter HTML
        st.markdown(get_strength_meter_html(score, st.session_state.password_input), unsafe_allow_html=True)
        
        # Metrics layout
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.markdown(f"""
            <div class="metric-container">
                <span style="font-weight: 600; color: #94a3b8;">Entropy Score</span>
                <span class="metric-value" style="color: {ent_color};">{entropy_val} <span style="font-size:0.75rem; color:#94a3b8; font-weight:300;">bits</span></span>
            </div>
            """, unsafe_allow_html=True)
            
            # Displays warning/suggestions if any
            feedback_html = get_feedback_html(feedback)
            if feedback_html:
                st.markdown(feedback_html, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="suggestion-box" style="background: rgba(16,185,129,0.05); border-left-color: #10b981;">
                    <div class="suggestion-title" style="color: #4ade80;">✨ Security Alert</div>
                    <div style="font-size:0.9rem; color:#f1f5f9;">No obvious vulnerabilities found! Outstanding password patterns.</div>
                </div>
                """, unsafe_allow_html=True)
                
        with metric_col2:
            st.markdown('<div style="font-weight: 600; color: #94a3b8; margin-bottom:12px;">Requirements Checklist</div>', unsafe_allow_html=True)
            st.markdown(get_checklist_html(st.session_state.password_input), unsafe_allow_html=True)
            
        # Crack time estimates
        st.markdown('<h3 style="color:#f8fafc; font-weight:600; font-size:1.15rem; margin-top:25px; margin-bottom:10px;">Time to Crack Estimates</h3>', unsafe_allow_html=True)
        st.markdown(get_crack_times_html(crack_times), unsafe_allow_html=True)
    else:
        # Default placeholder views when password is empty
        st.markdown(get_strength_meter_html(0, ""), unsafe_allow_html=True)
        
        col_empty1, col_empty2 = st.columns(2)
        with col_empty1:
            st.markdown(f"""
            <div class="metric-container">
                <span style="font-weight: 600; color: #94a3b8;">Entropy Score</span>
                <span class="metric-value" style="color: #64748b;">0.0 <span style="font-size:0.75rem; color:#64748b; font-weight:300;">bits</span></span>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div style="padding: 16px; border-radius: 12px; border: 1px dashed rgba(255,255,255,0.06); text-align:center; color:#64748b; margin-top:15px; font-size:0.9rem;">
                Enter a password to run real-time vulnerability checks.
            </div>
            """, unsafe_allow_html=True)
        with col_empty2:
            st.markdown('<div style="font-weight: 600; color: #94a3b8; margin-bottom:12px;">Requirements Checklist</div>', unsafe_allow_html=True)
            st.markdown(get_checklist_html(""), unsafe_allow_html=True)
            
        st.markdown('<h3 style="color:#64748b; font-weight:600; font-size:1.15rem; margin-top:25px; margin-bottom:10px;">Time to Crack Estimates</h3>', unsafe_allow_html=True)
        default_crack = {
            "online_throttling_100_per_hour": "N/A",
            "online_no_throttling_10_per_second": "N/A",
            "offline_slow_hashing_1e4_per_second": "N/A",
            "offline_fast_hashing_1e10_per_second": "N/A"
        }
        st.markdown(get_crack_times_html(default_crack), unsafe_allow_html=True)

# Column 2: Generator
with col_generator:
    st.markdown('<h2 style="color:#818cf8; font-weight:700; margin-top:0; font-size:1.8rem; border-bottom:1px solid rgba(255,255,255,0.08); padding-bottom:10px; margin-bottom:20px;">🔑 Generator</h2>', unsafe_allow_html=True)
    
    # Select Mode
    gen_mode = st.radio("Style", ["Random Characters", "Memorable Passphrase"], horizontal=True)
    
    if gen_mode == "Random Characters":
        gen_len = st.slider("Password Length", min_value=8, max_value=64, value=16)
        
        c_1, c_2 = st.columns(2)
        with c_1:
            g_lower = st.checkbox("Lowercase (a-z)", value=True)
            g_upper = st.checkbox("Uppercase (A-Z)", value=True)
        with c_2:
            g_nums = st.checkbox("Numbers (0-9)", value=True)
            g_syms = st.checkbox("Symbols (!@#$)", value=True)
            
        g_ambig = st.checkbox("Exclude Ambiguous (e.g. l, 1, O, 0)", value=False)
        
        if st.button("Generate Password"):
            pwd = generate_random_password(
                gen_len, g_upper, g_lower, g_nums, g_syms, g_ambig
            )
            st.session_state.generated_password = pwd
            # Add to generator history
            st.session_state.generator_history.insert(0, pwd)
            st.session_state.generator_history = st.session_state.generator_history[:5]
            
    else:
        gen_words = st.slider("Number of Words", min_value=3, max_value=8, value=4)
        gen_sep = st.selectbox("Word Separator", ["-", "_", ".", "Space", "None"], index=0)
        
        sep_map = {"-": "-", "_": "_", ".": ".", "Space": " ", "None": ""}
        separator_char = sep_map[gen_sep]
        
        g_cap = st.checkbox("Capitalize Words", value=True)
        g_num_sym = st.checkbox("Append Number & Symbol", value=True)
        
        if st.button("Generate Passphrase"):
            pwd = generate_passphrase(
                gen_words, separator_char, g_cap, g_num_sym
            )
            st.session_state.generated_password = pwd
            # Add to generator history
            st.session_state.generator_history.insert(0, pwd)
            st.session_state.generator_history = st.session_state.generator_history[:5]
            
    # Display generated output in a normal, clean input field with no code styling
    if st.session_state.generated_password:
        st.markdown('<div style="font-weight:600; color:#94a3b8; margin-top:20px; margin-bottom:8px;">Generated Result:</div>', unsafe_allow_html=True)
        st.text_input(
            "Generated Password Output Box",
            value=st.session_state.generated_password,
            label_visibility="collapsed"
        )
        st.markdown('<p style="font-size:0.8rem; color:#64748b; margin-top:5px; margin-bottom:15px;">💡 Highlight the password in the box above and press Ctrl+C to copy.</p>', unsafe_allow_html=True)
        
        # Button to test in analyser
        st.button("⚡ Test in Analyser", on_click=apply_generated_password)

# Separator & Session History Logs Expander at the bottom of the page
st.markdown('<hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.08); margin: 30px 0 20px 0;">', unsafe_allow_html=True)

with st.expander("📊 Session History Logs (Click to expand)", expanded=False):
    hist_col1, hist_col2 = st.columns(2)
    
    with hist_col1:
        st.markdown('<h4 style="color:#38bdf8; font-weight:600; margin-top:0;">Analyzed Passwords</h4>', unsafe_allow_html=True)
        if st.session_state.analysis_history:
            for i, entry in enumerate(st.session_state.analysis_history):
                masked_pwd = entry["password"]
                if len(masked_pwd) > 5:
                    display_pwd = f"{masked_pwd[:2]}••••{masked_pwd[-2:]}"
                else:
                    display_pwd = "•••••"
                    
                col_h1, col_h2 = st.columns([3, 1])
                with col_h1:
                    st.markdown(f'<div style="font-family:\'JetBrains Mono\', monospace; font-size:0.95rem; margin-top: 6px;"><code>{display_pwd}</code> <span style="color:{entry["color"]}; font-weight:bold;">({entry["strength"]})</span></div>', unsafe_allow_html=True)
                with col_h2:
                    if st.button("Load 🔍", key=f"load_ana_{i}"):
                        st.session_state.password_input = entry["password"]
                        st.session_state.password_input_widget = entry["password"]
                        st.rerun()
        else:
            st.markdown('<div style="color:#64748b; font-size:0.9rem; font-style:italic;">No analyzed passwords in this session.</div>', unsafe_allow_html=True)
            
    with hist_col2:
        st.markdown('<h4 style="color:#818cf8; font-weight:600; margin-top:0;">Generated Passwords</h4>', unsafe_allow_html=True)
        if st.session_state.generator_history:
            for i, pwd in enumerate(st.session_state.generator_history):
                if len(pwd) > 5:
                    display_pwd = f"{pwd[:2]}••••{pwd[-2:]}"
                else:
                    display_pwd = "•••••"
                    
                col_h1, col_h2 = st.columns([3, 1])
                with col_h1:
                    st.markdown(f'<div style="font-family:\'JetBrains Mono\', monospace; font-size:0.95rem; margin-top: 6px;"><code>{display_pwd}</code></div>', unsafe_allow_html=True)
                with col_h2:
                    if st.button("Load 🔍", key=f"load_gen_{i}"):
                        st.session_state.password_input = pwd
                        st.session_state.password_input_widget = pwd
                        st.rerun()
        else:
            st.markdown('<div style="color:#64748b; font-size:0.9rem; font-style:italic;">No generated passwords in this session.</div>', unsafe_allow_html=True)
