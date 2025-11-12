"""
Premium HR Analytics Suite - Main Application
"""
import streamlit as st
from dashboard import render_dashboard
from admin_panel import admin_panel
from ml_model import ml_dashboard
from utils import load_custom_css

# Page configuration
st.set_page_config(
    page_title="HR Analytics Suite",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load premium CSS with dark mode support
def get_theme_css(dark_mode):
    """Get CSS with dark/light theme applied"""
    base_css = load_custom_css()
    
    if dark_mode:
        # Apply dark mode data attribute for CSS variable system
        dark_mode_css = """
        /* Apply dark mode class */
        html, body {
            background: var(--bg-dark) !important;
        }
        
        [data-testid="stAppViewContainer"],
        section[data-testid="stMain"],
        .main {
            background: var(--bg-dark) !important;
        }
        
        /* Force dark mode variables */
        :root {
            --bg-primary: #0d1117 !important;
            --bg-secondary: #161b22 !important;
            --text-primary: #ffffff !important;
            --text-secondary: #d1d5db !important;
            --text-muted: #9ca3af !important;
            --card-bg: #161b22 !important;
            --card-border: #30363d !important;
            --input-bg: #161b22 !important;
            --input-text: #ffffff !important;
            --input-border: #30363d !important;
            --chart-text: #ffffff !important;
            --chart-grid: #30363d !important;
        }
        """
        return base_css + dark_mode_css
    else:
        return base_css

# Initialize dark mode in session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Load CSS with theme
css = get_theme_css(st.session_state.dark_mode)
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Initialize session state
if 'admin_authenticated' not in st.session_state:
    st.session_state.admin_authenticated = False

if 'show_login' not in st.session_state:
    st.session_state.show_login = False

if 'unlock_text' not in st.session_state:
    st.session_state.unlock_text = ""

if 'login_username' not in st.session_state:
    st.session_state.login_username = ""

if 'login_password' not in st.session_state:
    st.session_state.login_password = ""

if 'key_detector' not in st.session_state:
    st.session_state.key_detector = ""

# Admin credentials
ADMIN_USERNAME = "simar@gmail.com"
ADMIN_PASSWORD = "12345678"

def show_unlock_screen():
    """Display premium unlock screen"""
    st.markdown("""
    <div class="unlock-container">
        <div class="unlock-card">
            <h2 style="text-align: center; color: #1e293b; margin-bottom: 1rem; font-size: 2rem;">
                🔐 Admin Access
            </h2>
            <p style="text-align: center; color: #64748b; margin-bottom: 2rem;">
                Type "open" to access the admin panel
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hidden input that captures typing
    unlock_input = st.text_input(
        "",
        value=st.session_state.get('unlock_text', ''),
        key="unlock_input_hidden",
        label_visibility="collapsed",
        placeholder="Type 'open' here..."
    )
    
    # Check if "open" is typed
    if unlock_input:
        input_lower = unlock_input.lower().strip()
        st.session_state.unlock_text = input_lower
        
        if "open" in input_lower:
            st.session_state.show_login = True
            st.session_state.unlock_text = ""
            st.rerun()

def show_login_form():
    """Display premium login form with autofill"""
    st.markdown("""
    <div class="unlock-container">
        <div class="unlock-card" style="animation: fadeInUp 0.6s ease-out;">
            <h2 style="text-align: center; color: #1e293b; margin-bottom: 2rem; font-size: 2rem;">
                🔐 Admin Login
            </h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Autofill button outside form
    if st.button("🔑 Autofill Credentials", use_container_width=True, key="autofill_btn"):
        st.session_state.login_username = ADMIN_USERNAME
        st.session_state.login_password = ADMIN_PASSWORD
        st.rerun()
    
    with st.form("login_form", clear_on_submit=False):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            username = st.text_input(
                "Username",
                value=st.session_state.get('login_username', ''),
                key="login_username",
                placeholder="Enter your email"
            )
        
        with col2:
            password = st.text_input(
                "Password",
                type="password",
                value=st.session_state.get('login_password', ''),
                key="login_password",
                placeholder="Enter your password"
            )
        
        login_clicked = st.form_submit_button("Login", type="primary", use_container_width=True)
        
        if login_clicked:
            final_username = username if username else st.session_state.get('login_username', '')
            final_password = password if password else st.session_state.get('login_password', '')
            
            if final_username == ADMIN_USERNAME and final_password == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.session_state.show_login = False
                st.session_state.unlock_text = ""
                # Clear login credentials by deleting keys (will be recreated empty on next rerun)
                if 'login_username' in st.session_state:
                    del st.session_state.login_username
                if 'login_password' in st.session_state:
                    del st.session_state.login_password
                st.success("✅ Login successful! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")
    
    if st.button("← Back to Dashboard", use_container_width=True):
        st.session_state.show_login = False
        st.session_state.unlock_text = ""
        # Clear login credentials by deleting keys
        if 'login_username' in st.session_state:
            del st.session_state.login_username
        if 'login_password' in st.session_state:
            del st.session_state.login_password
        st.rerun()

def detect_unlock():
    """Detect if user types 'open' anywhere on the page"""
    # Hidden input for JavaScript to update
    hidden_key_detector = st.text_input(
        "",
        value=st.session_state.get('key_detector', ''),
        key="key_detector_hidden",
        label_visibility="collapsed"
    )
    
    # Check if "open" was detected
    if hidden_key_detector and hidden_key_detector.lower().strip() == 'open':
        st.session_state.show_login = True
        st.session_state.unlock_text = ""
        st.session_state.key_detector = ""
        st.rerun()
    
    # Check if "open" was detected via JavaScript or sidebar input
    with st.sidebar:
        st.markdown("---")
        st.markdown('<h3 class="admin-access-heading" style="margin-bottom: 0.5rem;">🔓 Admin Access</h3>', unsafe_allow_html=True)
        
        unlock_input = st.text_input(
            "Type 'open' to login",
            value=st.session_state.get('unlock_text', ''),
            key="unlock_input",
            placeholder="Type 'open'...",
            help="Type the word 'open' to access the admin login"
        )
        
        if unlock_input:
            input_lower = unlock_input.lower().strip()
            st.session_state.unlock_text = input_lower
            
            if "open" in input_lower:
                st.session_state.show_login = True
                st.session_state.unlock_text = ""
                st.rerun()
    
    # Add JavaScript to detect "open" typed anywhere and update hidden input
    st.markdown("""
    <script>
    (function() {
        if (window.openDetectorInitialized) return;
        window.openDetectorInitialized = true;
        
        let typedSequence = '';
        let lastKeyTime = Date.now();
        const RESET_TIME = 3000; // Reset after 3 seconds of no typing
        const TARGET = 'open';
        
        function findHiddenInput() {
            // Find input with key_detector_hidden - look for inputs with label_visibility="collapsed"
            const allInputs = document.querySelectorAll('input[type="text"], input[type="password"]');
            for (let input of allInputs) {
                const container = input.closest('[data-testid]');
                const label = container?.querySelector('label');
                // If label is hidden or doesn't exist, it might be our hidden input
                if (!label || label.style.display === 'none' || label.offsetHeight === 0) {
                    // Check if it's really hidden (not just a regular input)
                    const parent = input.closest('div');
                    if (parent && (parent.style.display === 'none' || parent.offsetHeight === 0)) {
                        return input;
                    }
                }
            }
            return null;
        }
        
        function updateHiddenInput() {
            const hiddenInput = findHiddenInput();
            if (hiddenInput) {
                hiddenInput.value = 'open';
                hiddenInput.focus();
                hiddenInput.blur();
                // Trigger change event
                const event = new Event('input', { bubbles: true, cancelable: true });
                hiddenInput.dispatchEvent(event);
                const changeEvent = new Event('change', { bubbles: true, cancelable: true });
                hiddenInput.dispatchEvent(changeEvent);
            }
        }
        
        function handleKeyPress(e) {
            // Don't capture if user is typing in a visible input/textarea
            const tag = e.target.tagName;
            if (tag === 'INPUT' || tag === 'TEXTAREA') {
                const input = e.target;
                // Only ignore if it's a visible input
                if (input.offsetParent !== null && input.style.display !== 'none') {
                    return;
                }
            }
            
            const now = Date.now();
            
            // Reset if too much time has passed
            if (now - lastKeyTime > RESET_TIME) {
                typedSequence = '';
            }
            
            lastKeyTime = now;
            
            // Only track letter keys
            if (e.key.length === 1 && /[a-zA-Z]/.test(e.key)) {
                typedSequence += e.key.toLowerCase();
                
                // Keep only last 4 characters
                if (typedSequence.length > TARGET.length) {
                    typedSequence = typedSequence.slice(-TARGET.length);
                }
                
                // Check if "open" is typed
                if (typedSequence === TARGET) {
                    typedSequence = ''; // Reset
                    updateHiddenInput();
                    // Force a small delay then trigger rerun
                    setTimeout(() => {
                        window.location.reload();
                    }, 100);
                }
            }
        }
        
        // Wait for page to load and initialize
        function init() {
            setTimeout(() => {
                document.addEventListener('keydown', handleKeyPress, true);
            }, 1000);
        }
        
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
        } else {
            init();
        }
    })();
    </script>
    """, unsafe_allow_html=True)

def main():
    # Ensure session state is initialized
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    if 'show_login' not in st.session_state:
        st.session_state.show_login = False
    if 'unlock_text' not in st.session_state:
        st.session_state.unlock_text = ""
    if 'login_username' not in st.session_state:
        st.session_state.login_username = ""
    if 'login_password' not in st.session_state:
        st.session_state.login_password = ""
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    
    # Apply theme CSS dynamically (re-apply in case it changed)
    theme_css = get_theme_css(st.session_state.dark_mode)
    st.markdown(f"<style>{theme_css}</style>", unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("🏢 HR Analytics Suite")
    
    # Dark/Light Mode Toggle
    col_toggle1, col_toggle2 = st.sidebar.columns([1, 1])
    with col_toggle1:
        if st.button("🌙 Dark", use_container_width=True, key="dark_btn"):
            st.session_state.dark_mode = True
            st.rerun()
    with col_toggle2:
        if st.button("☀️ Light", use_container_width=True, key="light_btn"):
            st.session_state.dark_mode = False
            st.rerun()
    
    if st.session_state.dark_mode:
        st.sidebar.success("🌙 Dark Mode Active")
    else:
        st.sidebar.info("☀️ Light Mode Active")
    
    st.sidebar.markdown("---")
    
    # Check if login should be shown
    if st.session_state.get('show_login', False):
        show_login_form()
        return
    
    # Detect unlock command (sidebar input + global keyboard)
    detect_unlock()
    
    # App mode selection
    app_mode = st.sidebar.selectbox(
        "Choose the App Mode",
        ["Dashboard", "Admin Panel", "ML Predictor", "About"],
        key="app_mode"
    )
    
    # Show logout button if authenticated
    if st.session_state.get('admin_authenticated', False):
        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            st.session_state.admin_authenticated = False
            st.session_state.show_login = False
            st.rerun()
        st.sidebar.markdown("""
        <div class="admin-mode">
            ✅ Admin Mode Active
        </div>
        """, unsafe_allow_html=True)
    
    # Route to appropriate page
    if app_mode == "Dashboard":
        render_dashboard()
    elif app_mode == "Admin Panel":
        admin_panel()
    elif app_mode == "ML Predictor":
        ml_dashboard()

if __name__ == "__main__":
    main()
