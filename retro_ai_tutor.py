import gradio as gr
import random
import requests
import json

# Global state for user progress
user_stats = {
    "xp": 0,
    "level": 1,
    "questions_solved": 0,
    "lessons_completed": 0
}

# NVIDIA API Configuration
NVIDIA_API_KEY = "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"
NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

def call_nvidia_api(prompt, system_prompt="You are GRIND GLITCH, a helpful AI tutor with a retro gaming and space exploration personality. Use terms like 'PROCESSING', 'ANALYSIS COMPLETE', and add gaming elements to your responses. Remember: you're here to help because users deserve the best education in the universe."):
    """Call NVIDIA API with the given prompt"""
    try:
        headers = {
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "meta/llama-4-maverick-17b-128e-instruct",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "stream": False
        }

        response = requests.post(NVIDIA_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()

        result = response.json()
        return result['choices'][0]['message']['content']

    except requests.exceptions.RequestException as e:
        return f"⚠️ NETWORK ERROR: Connection to AI Oracle failed. Please check your connection and try again.\n\nError details: {str(e)}"
    except KeyError as e:
        return f"⚠️ API ERROR: Unexpected response format from AI Oracle.\n\nError details: {str(e)}"
    except Exception as e:
        return f"⚠️ SYSTEM ERROR: An unexpected error occurred.\n\nError details: {str(e)}"

def calculate_level(xp):
    return min(10, (xp // 100) + 1)

def add_xp(points):
    user_stats["xp"] += points
    user_stats["level"] = calculate_level(user_stats["xp"])
    return user_stats

# Enhanced CSS for spaceship interior aesthetic with floating UFOs
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&display=swap');

/* Global spaceship interior styling */
.gradio-container {
    background: 
        radial-gradient(circle at 20% 30%, rgba(0, 100, 255, 0.1), transparent 40%),
        radial-gradient(circle at 80% 70%, rgba(0, 255, 150, 0.1), transparent 40%),
        linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 25%, #16213e 50%, #0f1419 75%, #000000 100%) !important;
    color: #00ff88 !important;
    font-family: 'Orbitron', monospace !important;
    min-height: 100vh !important;
    overflow-x: hidden !important;
    position: relative !important;
}

/* Floating UFOs in background */
.gradio-container .ufo-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 2;
    overflow: hidden;
}

.gradio-container .ufo {
    position: absolute;
    width: 30px;
    height: 15px;
    background: linear-gradient(to bottom, #00ff00, #00cc00);
    border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
    box-shadow: 
        0 0 10px #00ff00,
        0 -3px 0 #00ff00,
        0 3px 0 rgba(0, 255, 0, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.3);
    animation: float-ufo 8s ease-in-out infinite;
}

.gradio-container .ufo::before {
    content: '';
    position: absolute;
    top: -8px;
    left: 50%;
    transform: translateX(-50%);
    width: 12px;
    height: 8px;
    background: linear-gradient(to bottom, #00ff00, #00aa00);
    border-radius: 50%;
    box-shadow: 0 0 5px #00ff00;
}

.gradio-container .ufo::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 50%;
    transform: translateX(-50%);
    width: 40px;
    height: 3px;
    background: radial-gradient(ellipse, rgba(0, 255, 0, 0.3), transparent);
    border-radius: 50%;
    animation: beam-pulse 2s ease-in-out infinite;
}

.gradio-container .ufo-1 {
    top: 15%;
    left: 10%;
    animation: float-ufo-1 12s ease-in-out infinite;
    animation-delay: 0s;
}

.gradio-container .ufo-2 {
    top: 25%;
    right: 15%;
    animation: float-ufo-2 15s ease-in-out infinite;
    animation-delay: -2s;
    transform: scale(0.8);
}

.gradio-container .ufo-3 {
    top: 45%;
    left: 5%;
    animation: float-ufo-3 18s ease-in-out infinite;
    animation-delay: -5s;
    transform: scale(1.2);
}

.gradio-container .ufo-4 {
    top: 60%;
    right: 8%;
    animation: float-ufo-4 10s ease-in-out infinite;
    animation-delay: -3s;
    transform: scale(0.6);
}

.gradio-container .ufo-5 {
    top: 80%;
    left: 20%;
    animation: float-ufo-5 14s ease-in-out infinite;
    animation-delay: -7s;
    transform: scale(0.9);
}

@keyframes float-ufo-1 {
    0%, 100% { transform: translate(0, 0) rotate(0deg); }
    25% { transform: translate(30px, -20px) rotate(5deg); }
    50% { transform: translate(-20px, 15px) rotate(-3deg); }
    75% { transform: translate(15px, -10px) rotate(2deg); }
}

@keyframes float-ufo-2 {
    0%, 100% { transform: scale(0.8) translate(0, 0) rotate(0deg); }
    33% { transform: scale(0.8) translate(-40px, 25px) rotate(-8deg); }
    66% { transform: scale(0.8) translate(25px, -15px) rotate(6deg); }
}

@keyframes float-ufo-3 {
    0%, 100% { transform: scale(1.2) translate(0, 0) rotate(0deg); }
    20% { transform: scale(1.2) translate(50px, 30px) rotate(10deg); }
    40% { transform: scale(1.2) translate(-30px, -20px) rotate(-5deg); }
    60% { transform: scale(1.2) translate(40px, 10px) rotate(7deg); }
    80% { transform: scale(1.2) translate(-20px, 25px) rotate(-3deg); }
}

@keyframes float-ufo-4 {
    0%, 100% { transform: scale(0.6) translate(0, 0) rotate(0deg); }
    50% { transform: scale(0.6) translate(-60px, -30px) rotate(-12deg); }
}

@keyframes float-ufo-5 {
    0%, 100% { transform: scale(0.9) translate(0, 0) rotate(0deg); }
    25% { transform: scale(0.9) translate(-35px, -25px) rotate(-6deg); }
    50% { transform: scale(0.9) translate(45px, 20px) rotate(4deg); }
    75% { transform: scale(0.9) translate(-25px, 35px) rotate(-2deg); }
}

@keyframes beam-pulse {
    0%, 100% { opacity: 0.3; transform: translateX(-50%) scaleY(1); }
    50% { opacity: 0.6; transform: translateX(-50%) scaleY(1.2); }
}

/* Spaceship hull plating texture */
.gradio-container::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        repeating-linear-gradient(
            0deg,
            transparent,
            transparent 2px,
            rgba(0, 255, 136, 0.02) 2px,
            rgba(0, 255, 136, 0.02) 4px
        ),
        repeating-linear-gradient(
            90deg,
            transparent,
            transparent 2px,
            rgba(0, 200, 255, 0.02) 2px,
            rgba(0, 200, 255, 0.02) 4px
        );
    pointer-events: none;
    z-index: 1;
}

/* Floating control panels and HUD elements */
.gradio-container::after {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(2px 2px at 5% 15%, #00ff88, transparent),
        radial-gradient(1px 1px at 95% 25%, #0088ff, transparent),
        radial-gradient(3px 3px at 15% 85%, #00ff88, transparent),
        radial-gradient(2px 2px at 85% 90%, #0088ff, transparent),
        radial-gradient(1px 1px at 45% 5%, #ff8800, transparent),
        radial-gradient(2px 2px at 75% 15%, #00ff88, transparent);
    background-size: 
        300px 100vh,
        250px 100vh,
        350px 100vh,
        280px 100vh,
        200px 100vh,
        320px 100vh;
    animation: 
        hud-drift-1 20s linear infinite,
        hud-drift-2 15s linear infinite;
    pointer-events: none;
    z-index: 1;
    opacity: 0.8;
}

@keyframes hud-drift-1 {
    0% { transform: translateY(-100vh) translateX(10px); }
    100% { transform: translateY(100vh) translateX(-30px); }
}

@keyframes hud-drift-2 {
    0% { transform: translateY(-100vh) translateX(-15px); }
    100% { transform: translateY(100vh) translateX(25px); }
}

/* Main container as spaceship bridge */
#component-0 {
    background: transparent !important;
    border: none !important;
    min-height: 100vh !important;
    position: relative !important;
}

/* Title styling - Main ship computer display */
.gradio-container h1 {
    color: #00ff88 !important;
    text-align: center !important;
    font-size: 3.8rem !important;
    font-weight: 900 !important;
    text-shadow: 
        0 0 20px #00ff88, 
        0 0 40px #00ff88,
        0 0 60px #00ff88,
        0 2px 0 #003322 !important;
    margin: 1rem 0 !important;
    font-family: 'Orbitron', monospace !important;
    letter-spacing: 0.3em !important;
    animation: main-display-glow 3s ease-in-out infinite alternate !important;
    z-index: 10 !important;
    position: relative !important;
    background: 
        linear-gradient(135deg, rgba(0, 255, 136, 0.1), transparent),
        linear-gradient(45deg, transparent, rgba(0, 255, 136, 0.05), transparent) !important;
    padding: 20px 40px !important;
    border: 2px solid rgba(0, 255, 136, 0.3) !important;
    border-radius: 15px !important;
    backdrop-filter: blur(5px) !important;
}

.gradio-container h2 {
    color: #00ccff !important;
    text-align: center !important;
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    text-shadow: 0 0 15px #00ccff, 0 0 30px #00ccff !important;
    margin: 1rem 0 !important;
    font-family: 'Rajdhani', sans-serif !important;
    letter-spacing: 0.15em !important;
    z-index: 10 !important;
    position: relative !important;
}

.gradio-container h3 {
    color: #ffaa00 !important;
    text-align: center !important;
    font-size: 1.6rem !important;
    font-weight: 600 !important;
    text-shadow: 0 0 10px #ffaa00 !important;
    margin: 0.5rem 0 !important;
    font-family: 'Rajdhani', sans-serif !important;
    z-index: 10 !important;
    position: relative !important;
}

@keyframes main-display-glow {
    from { 
        text-shadow: 
            0 0 20px #00ff88, 
            0 0 40px #00ff88, 
            0 0 60px #00ff88,
            0 2px 0 #003322;
        border-color: rgba(0, 255, 136, 0.3);
    }
    to { 
        text-shadow: 
            0 0 30px #00ff88, 
            0 0 60px #00ff88, 
            0 0 90px #00ff88,
            0 2px 0 #003322;
        border-color: rgba(0, 255, 136, 0.6);
    }
}

/* SPACESHIP CONTROL BUTTON STYLING */
.gradio-container button {
    /* Base spaceship control panel styling */
    background: 
        linear-gradient(145deg, 
            rgba(0, 255, 136, 0.2) 0%, 
            rgba(0, 200, 120, 0.3) 25%,
            rgba(0, 150, 100, 0.4) 50%,
            rgba(0, 120, 80, 0.3) 75%,
            rgba(0, 100, 60, 0.2) 100%
        ),
        linear-gradient(45deg, 
            transparent 30%, 
            rgba(255, 255, 255, 0.1) 50%, 
            transparent 70%
        ) !important;
    
    color: #00ff88 !important;
    border: 3px solid transparent !important;
    border-image: 
        linear-gradient(45deg, 
            #00ff88 0%, 
            #00ccff 25%, 
            #00ff88 50%, 
            #0088ff 75%, 
            #00ff88 100%
        ) 1 !important;
    
    border-radius: 0 !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    padding: 18px 35px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.15em !important;
    
    /* Spaceship control panel effects */
    box-shadow: 
        /* Main glow */
        0 0 20px rgba(0, 255, 136, 0.4),
        /* Inner highlight */
        inset 0 2px 0 rgba(255, 255, 255, 0.2),
        /* Inner shadow */
        inset 0 -2px 0 rgba(0, 0, 0, 0.3),
        /* Left edge highlight */
        inset 2px 0 0 rgba(0, 255, 136, 0.2),
        /* Right edge shadow */
        inset -2px 0 0 rgba(0, 0, 0, 0.2),
        /* Outer depth */
        0 4px 8px rgba(0, 0, 0, 0.3) !important;
    
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    z-index: 10 !important;
    margin: 0.8rem !important;
    min-width: 280px !important;
    
    /* Hexagonal clipping for futuristic look */
    clip-path: polygon(
        10px 0%, 
        calc(100% - 10px) 0%, 
        100% 25%, 
        100% 75%, 
        calc(100% - 10px) 100%, 
        10px 100%, 
        0% 75%, 
        0% 25%
    ) !important;
    
    /* Control panel texture */
    background-attachment: fixed !important;
    backdrop-filter: blur(2px) !important;
}

/* LED status indicators on buttons */
.gradio-container button::before {
    content: '';
    position: absolute;
    top: 8px;
    right: 12px;
    width: 8px;
    height: 8px;
    background: #00ff88;
    border-radius: 50%;
    box-shadow: 
        0 0 8px #00ff88,
        inset 0 0 4px rgba(255, 255, 255, 0.6);
    animation: led-pulse 2s ease-in-out infinite;
    z-index: 1;
}

@keyframes led-pulse {
    0%, 100% { 
        opacity: 1; 
        box-shadow: 
            0 0 8px #00ff88,
            inset 0 0 4px rgba(255, 255, 255, 0.6);
    }
    50% { 
        opacity: 0.4; 
        box-shadow: 
            0 0 4px #00ff88,
            inset 0 0 2px rgba(255, 255, 255, 0.3);
    }
}

/* Control panel lines on buttons */
.gradio-container button::after {
    content: '';
    position: absolute;
    bottom: 6px;
    left: 15px;
    right: 15px;
    height: 2px;
    background: linear-gradient(90deg, 
        transparent 0%, 
        #00ff88 20%, 
        #00ccff 50%, 
        #00ff88 80%, 
        transparent 100%
    );
    opacity: 0.6;
    animation: scanner-line 3s linear infinite;
}

@keyframes scanner-line {
    0% { transform: translateX(-100%); opacity: 0; }
    50% { opacity: 0.8; }
    100% { transform: translateX(100%); opacity: 0; }
}

/* Hover state - Control activation */
.gradio-container button:hover {
    background: 
        linear-gradient(145deg, 
            rgba(0, 255, 136, 0.4) 0%, 
            rgba(0, 240, 140, 0.5) 25%,
            rgba(0, 220, 120, 0.6) 50%,
            rgba(0, 200, 100, 0.5) 75%,
            rgba(0, 180, 80, 0.4) 100%
        ),
        linear-gradient(45deg, 
            transparent 20%, 
            rgba(255, 255, 255, 0.2) 50%, 
            transparent 80%
        ) !important;
    
    box-shadow: 
        /* Enhanced main glow */
        0 0 35px rgba(0, 255, 136, 0.7),
        0 0 60px rgba(0, 255, 136, 0.4),
        /* Inner highlight */
        inset 0 3px 0 rgba(255, 255, 255, 0.3),
        /* Inner shadow */
        inset 0 -3px 0 rgba(0, 0, 0, 0.4),
        /* Edge effects */
        inset 3px 0 0 rgba(0, 255, 136, 0.3),
        inset -3px 0 0 rgba(0, 0, 0, 0.3),
        /* Enhanced depth */
        0 6px 12px rgba(0, 0, 0, 0.4) !important;
    
    transform: translateY(-2px) scale(1.02) !important;
    color: #ffffff !important;
    
    border-image: 
        linear-gradient(45deg, 
            #00ff88 0%, 
            #ffffff 25%, 
            #00ff88 50%, 
            #00ccff 75%, 
            #00ff88 100%
        ) 1 !important;
}

/* Active state - Control engaged */
.gradio-container button:active {
    transform: translateY(1px) scale(0.98) !important;
    box-shadow: 
        0 0 15px rgba(0, 255, 136, 0.8),
        inset 0 4px 8px rgba(0, 0, 0, 0.4),
        inset 0 0 20px rgba(0, 255, 136, 0.2) !important;
    
    background: 
        linear-gradient(145deg, 
            rgba(0, 200, 100, 0.6), 
            rgba(0, 255, 136, 0.4)
        ) !important;
}

/* Special start button - Main power control */
.start-button {
    font-size: 2.5rem !important;
    padding: 30px 80px !important;
    margin: 2rem auto !important;
    display: block !important;
    min-width: 400px !important;
    
    background: 
        radial-gradient(ellipse at center, 
            rgba(0, 255, 136, 0.3) 0%, 
            rgba(0, 200, 100, 0.4) 30%,
            rgba(0, 150, 80, 0.5) 60%,
            rgba(0, 100, 60, 0.3) 100%
        ),
        linear-gradient(45deg, 
            transparent 40%, 
            rgba(255, 255, 255, 0.15) 50%, 
            transparent 60%
        ) !important;
    
    box-shadow: 
        0 0 40px rgba(0, 255, 136, 0.6),
        0 0 80px rgba(0, 255, 136, 0.3),
        inset 0 0 30px rgba(0, 255, 136, 0.2) !important;
    
    animation: main-power-pulse 4s ease-in-out infinite !important;
}

@keyframes main-power-pulse {
    0%, 100% { 
        box-shadow: 
            0 0 40px rgba(0, 255, 136, 0.6),
            0 0 80px rgba(0, 255, 136, 0.3),
            inset 0 0 30px rgba(0, 255, 136, 0.2);
    }
    50% { 
        box-shadow: 
            0 0 60px rgba(0, 255, 136, 0.8),
            0 0 120px rgba(0, 255, 136, 0.5),
            inset 0 0 50px rgba(0, 255, 136, 0.4);
    }
}

/* Stats display - Ship status panel */
.stats-container {
    background: 
        linear-gradient(135deg, 
            rgba(0, 255, 136, 0.1) 0%, 
            rgba(0, 200, 120, 0.15) 50%, 
            rgba(0, 150, 100, 0.1) 100%
        ) !important;
    border: 2px solid #00ff88 !important;
    border-radius: 15px !important;
    padding: 20px !important;
    margin: 1rem auto !important;
    max-width: 450px !important;
    box-shadow: 
        0 0 30px rgba(0, 255, 136, 0.3),
        inset 0 0 20px rgba(0, 255, 136, 0.1) !important;
    text-align: center !important;
    z-index: 10 !important;
    position: relative !important;
    backdrop-filter: blur(3px) !important;
    
    clip-path: polygon(
        15px 0%, 
        calc(100% - 15px) 0%, 
        100% 15px, 
        100% calc(100% - 15px), 
        calc(100% - 15px) 100%, 
        15px 100%, 
        0% calc(100% - 15px), 
        0% 15px
    ) !important;
}

.stats-text {
    color: #00ff88 !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 1.2rem !important;
    margin: 8px 0 !important;
    text-shadow: 0 0 5px #00ff88 !important;
}

/* Text areas and inputs - Control interfaces */
.gradio-container textarea, .gradio-container input {
    background: 
        linear-gradient(135deg, 
            rgba(0, 50, 30, 0.8) 0%, 
            rgba(0, 40, 25, 0.9) 100%
        ) !important;
    border: 2px solid #00ff88 !important;
    border-radius: 8px !important;
    color: #00ff88 !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 1.1rem !important;
    padding: 15px !important;
    box-shadow: 
        inset 0 0 15px rgba(0, 255, 136, 0.2),
        0 0 10px rgba(0, 255, 136, 0.3) !important;
    backdrop-filter: blur(2px) !important;
}

.gradio-container textarea:focus, .gradio-container input:focus {
    border-color: #00ccff !important;
    box-shadow: 
        0 0 25px rgba(0, 204, 255, 0.5),
        inset 0 0 20px rgba(0, 204, 255, 0.2) !important;
    outline: none !important;
    color: #00ccff !important;
}

/* Output styling - Data displays */
.output-text {
    background: 
        linear-gradient(135deg, 
            rgba(0, 40, 25, 0.9) 0%, 
            rgba(0, 30, 20, 0.95) 100%
        ) !important;
    border: 2px solid #00ff88 !important;
    border-radius: 12px !important;
    color: #00ff88 !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 1.1rem !important;
    padding: 25px !important;
    margin: 1rem auto !important;
    box-shadow: 
        0 0 25px rgba(0, 255, 136, 0.3),
        inset 0 0 15px rgba(0, 255, 136, 0.1) !important;
    line-height: 1.7 !important;
    z-index: 10 !important;
    position: relative !important;
    backdrop-filter: blur(3px) !important;
}

/* Center content in spaceship bridge layout */
.gradio-container .contain {
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
    min-height: 100vh !important;
    text-align: center !important;
    z-index: 10 !important;
    position: relative !important;
    padding: 30px !important;
    margin: 0 auto !important;
    max-width: 1400px !important;
}

.gradio-container > div {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    width: 100% !important;
    min-height: 100vh !important;
}

.gradio-container .wrap {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    width: 100% !important;
    min-height: 100vh !important;
    padding: 2rem !important;
}

/* Control panel grid layout */
.button-grid {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)) !important;
    gap: 25px !important;
    max-width: 900px !important;
    margin: 2rem auto !important;
    padding: 25px !important;
}

/* Hide gradio branding */
.footer {
    display: none !important;
}

.gradio-container .version {
    display: none !important;
}

/* Achievement notifications - Ship alerts */
.achievement {
    background: 
        linear-gradient(145deg, 
            rgba(255, 170, 0, 0.9) 0%, 
            rgba(255, 136, 0, 0.95) 100%
        ) !important;
    color: #000 !important;
    border: 3px solid #ffaa00 !important;
    border-radius: 12px !important;
    padding: 18px !important;
    margin: 12px !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: bold !important;
    text-align: center !important;
    animation: achievement-alert 0.6s ease-out !important;
    box-shadow: 
        0 0 25px #ffaa00,
        inset 0 0 15px rgba(255, 255, 255, 0.2) !important;
    backdrop-filter: blur(2px) !important;
}

@keyframes achievement-alert {
    0% { 
        transform: scale(0.7) translateY(30px) rotate(-5deg); 
        opacity: 0; 
    }
    50% { 
        transform: scale(1.05) translateY(-5px) rotate(1deg); 
    }
    100% { 
        transform: scale(1) translateY(0) rotate(0deg); 
        opacity: 1; 
    }
}

/* Spaceship ambient lighting effects */
.gradio-container {
    animation: ambient-lighting 8s ease-in-out infinite !important;
}

@keyframes ambient-lighting {
    0%, 100% { 
        background: 
            radial-gradient(circle at 20% 30%, rgba(0, 100, 255, 0.1), transparent 40%),
            radial-gradient(circle at 80% 70%, rgba(0, 255, 150, 0.1), transparent 40%),
            linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 25%, #16213e 50%, #0f1419 75%, #000000 100%);
    }
    25% { 
        background: 
            radial-gradient(circle at 30% 20%, rgba(0, 150, 255, 0.12), transparent 40%),
            radial-gradient(circle at 70% 80%, rgba(0, 255, 100, 0.12), transparent 40%),
            linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 25%, #16213e 50%, #0f1419 75%, #000000 100%);
    }
    50% { 
        background: 
            radial-gradient(circle at 80% 30%, rgba(0, 200, 255, 0.08), transparent 40%),
            radial-gradient(circle at 20% 70%, rgba(0, 255, 200, 0.08), transparent 40%),
            linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 25%, #16213e 50%, #0f1419 75%, #000000 100%);
    }
    75% { 
        background: 
            radial-gradient(circle at 70% 20%, rgba(0, 120, 255, 0.1), transparent 40%),
            radial-gradient(circle at 30% 80%, rgba(0, 255, 120, 0.1), transparent 40%),
            linear-gradient(135deg, #0a0a1a 0%, #1a1a2e 25%, #16213e 50%, #0f1419 75%, #000000 100%);
    }
}
"""

# Add UFO HTML injection function
def inject_ufos():
    return """
    <div class="ufo-container">
        <div class="ufo ufo-1"></div>
        <div class="ufo ufo-2"></div>
        <div class="ufo ufo-3"></div>
        <div class="ufo ufo-4"></div>
        <div class="ufo ufo-5"></div>
    </div>
    """

# Functions for different features remain the same
def start_tutor():
    return {
        page_1: gr.update(visible=False),
        page_2: gr.update(visible=True)
    }

def go_back():
    return {
        page_1: gr.update(visible=True),
        page_2: gr.update(visible=False),
        ask_oracle_page: gr.update(visible=False),
        training_page: gr.update(visible=False),
        lesson_page: gr.update(visible=False),
        challenge_page: gr.update(visible=False)
    }

def show_ask_oracle():
    return {
        page_2: gr.update(visible=False),
        ask_oracle_page: gr.update(visible=True)
    }

def show_training():
    return {
        page_2: gr.update(visible=False),
        training_page: gr.update(visible=True)
    }

def show_lesson_builder():
    return {
        page_2: gr.update(visible=False),
        lesson_page: gr.update(visible=True)
    }

def show_challenge_creator():
    return {
        page_2: gr.update(visible=False),
        challenge_page: gr.update(visible=True)
    }

def ask_ai_tutor(question):
    if not question.strip():
        return "⚠️ ERROR: Please enter a question to receive wisdom from the AI Oracle!"

    add_xp(10)
    user_stats["questions_solved"] += 1

    system_prompt = """You are the AI Oracle, a wise and powerful tutor with a retro gaming personality. 
    
    IMPORTANT GUIDELINES:
    - Start responses with gaming-style headers like "🔮 PROCESSING QUERY...", "⚡ ANALYSIS COMPLETE", "🚀 KNOWLEDGE SCAN INITIATED"
    - Use retro gaming terminology and style
    - Be educational and helpful while maintaining the gaming theme
    - End with XP and level information
    - Keep responses concise but informative
    - Use bullet points and clear structure when explaining concepts
    - Add motivational gaming elements"""

    prompt = f"A student asks: '{question}'\n\nProvide a helpful educational response in your retro gaming AI Oracle style. The student just gained +10 XP and is now Level {user_stats['level']} with {user_stats['xp']} total XP."

    ai_response = call_nvidia_api(prompt, system_prompt)

    if "XP" not in ai_response and "Level" not in ai_response:
        ai_response += f"\n\n🎮 **+10 XP GAINED!** | Level: {user_stats['level']} | Total XP: {user_stats['xp']}"

    return ai_response

def generate_practice():
    add_xp(15)

    system_prompt = """You are GRIND GLITCH Training Mode AI that generates practice questions and exercises. 
    Use retro space-gaming style with headers like "🎯 TRAINING PODS ACTIVATED", "⚔️ COSMIC DRILL SEQUENCE", "🔥 STELLAR CHALLENGE PROTOCOL".
    Generate 3-4 practice questions on random educational topics (math, science, language, etc.).
    Keep the cosmic gaming theme and remember: we're here to help because users deserve the best education.
    End with XP information."""

    prompt = f"Generate a training session with practice questions. The student just gained +15 XP and is now Level {user_stats['level']} with {user_stats['xp']} total XP."

    ai_response = call_nvidia_api(prompt, system_prompt)

    if "XP" not in ai_response:
        ai_response += f"\n\n🎮 **+15 XP GAINED!** | Level: {user_stats['level']} | Total XP: {user_stats['xp']}"

    return ai_response

def create_lesson(topic):
    if not topic.strip():
        return "⚠️ ERROR: Please specify a topic for lesson generation!"

    add_xp(25)
    user_stats["lessons_completed"] += 1

    system_prompt = """You are GRIND GLITCH Knowledge Forge AI, a cosmic lesson builder with retro space-gaming personality.
    Use headers like "🏗️ STELLAR KNOWLEDGE FORGE ACTIVATED", "📚 GALACTIC LESSON CONSTRUCTION INITIATED".
    Create a comprehensive lesson outline for the given topic including:
    - Introduction/Overview
    - Key concepts and definitions
    - Examples and applications
    - Practice exercises
    - Summary and next steps
    Maintain the cosmic gaming theme and remember: we're here to help because you deserve the universe's best education."""

    prompt = f"Create a comprehensive lesson on the topic: '{topic}'. The student just gained +25 XP, completed {user_stats['lessons_completed']} lessons, and is now Level {user_stats['level']} with {user_stats['xp']} total XP."

    ai_response = call_nvidia_api(prompt, system_prompt)

    if "XP" not in ai_response:
        ai_response += f"\n\n🎮 **LESSON BUILDER ACHIEVEMENT!** +25 XP | Level: {user_stats['level']} | Lessons Created: {user_stats['lessons_completed']} | Total XP: {user_stats['xp']}"

    return ai_response

def create_questions(subject):
    if not subject.strip():
        return "⚠️ ERROR: Please specify a subject for question generation!"

    add_xp(20)

    system_prompt = """You are GRIND GLITCH Challenge Creator AI with retro space-gaming personality.
    Use headers like "🎲 COSMIC CHALLENGE CREATOR ONLINE", "🎯 STELLAR QUESTION BANK GENERATED".
    Create a variety of questions for the given subject across different difficulty levels:
    - Easy (multiple choice, basic concepts)
    - Medium (short answer, applications)  
    - Hard (essay, analysis, problem-solving)
    - Expert (research, creative applications)
    Maintain the cosmic gaming theme and remember: we're here to help because you deserve the best education in the galaxy."""

    prompt = f"Generate practice questions for the subject: '{subject}'. Create questions across different difficulty levels. The student just gained +20 XP and is now Level {user_stats['level']} with {user_stats['xp']} total XP."

    ai_response = call_nvidia_api(prompt, system_prompt)

    if "XP" not in ai_response:
        ai_response += f"\n\n🎮 **QUESTION MASTER BADGE!** +20 XP | Level: {user_stats['level']} | Total XP: {user_stats['xp']}"

    return ai_response

def get_stats():
    return f"** SHIP STATUS** \n\n** COMMANDER LEVEL:** {user_stats['level']} \n** TOTAL XP:** {user_stats['xp']} \n** MISSIONS COMPLETED:** {user_stats['questions_solved']} \n** KNOWLEDGE MODULES:** {user_stats['lessons_completed']} \n\n** NEXT RANK:** {(user_stats['level'] * 100) - user_stats['xp']} XP to promotion"

# Create the Gradio interface
with gr.Blocks(css=custom_css, title="GRIND GLITCH - INTERSTELLAR LEARNING COMMAND") as demo:

    # Add UFO HTML elements
    gr.HTML(inject_ufos())

    # Page 1: Landing Page
    with gr.Column(visible=True) as page_1:
        gr.Markdown("# GRIND GLITCH")
        gr.Markdown("### INTERSTELLAR LEARNING PROTOCOL ACTIVATED")
        gr.Markdown("*Cosmic support for stellar minds - because you deserve the universe's best education*")
        gr.Markdown("*From distant galaxies, we're here to help you achieve greatness*")
        gr.Markdown("*Powered by NVIDIA Llama AI Core*")

        start_btn = gr.Button("ACTIVATE GRIND GLITCH", elem_classes=["start-button"], variant="primary")

    # Page 2: Main Menu
    with gr.Column(visible=False) as page_2:
        gr.Markdown("## GRIND GLITCH COMMAND CENTER")
        gr.Markdown("### Navigate your learning journey across the cosmos!")
        gr.Markdown("*We're here to help you reach the stars - you deserve stellar education*")

        # Stats display
        stats_display = gr.Markdown(get_stats(), elem_classes=["stats-container"])

        with gr.Row():
            with gr.Column():
                oracle_btn = gr.Button("COSMIC ORACLE\n*Stellar answers from across the galaxy*", variant="primary")
                training_btn = gr.Button("STELLAR TRAINING\n*Because you deserve the best preparation*", variant="primary")
            with gr.Column():
                lesson_btn = gr.Button("KNOWLEDGE FORGE\n*Universe-class custom lessons*", variant="primary")
                challenge_btn = gr.Button(" COSMIC CHALLENGES\n*Galactic-level practice questions*", variant="primary")

        back_btn = gr.Button("MAIN CONSOLE", variant="secondary")

    # Ask Oracle Page
    with gr.Column(visible=False) as ask_oracle_page:
        gr.Markdown("## 🔮 GRIND GLITCH ORACLE CHAMBER")
        gr.Markdown("### Accessing cosmic knowledge database...")
        gr.Markdown("*We're here to help - ask anything, you deserve stellar answers*")

        question_input = gr.Textbox(
            label="Query Input:",
            placeholder="Enter your question for the Oracle...",
            lines=3
        )
        ask_btn = gr.Button("TRANSMIT QUERY", variant="primary")
        oracle_output = gr.Markdown("", elem_classes=["output-text"])

        back_oracle_btn = gr.Button("RETURN TO COMMAND CENTER", variant="secondary")

    # Training Mode Page
    with gr.Column(visible=False) as training_page:
        gr.Markdown("## 🎯 GRIND GLITCH TRAINING BAY")
        gr.Markdown("### Stellar practice sessions - because you deserve the best preparation!")

        generate_btn = gr.Button("INITIATE COSMIC TRAINING", variant="primary")
        training_output = gr.Markdown("", elem_classes=["output-text"])

        back_training_btn = gr.Button("RETURN TO COMMAND CENTER", variant="secondary")

    # Lesson Builder Page
    with gr.Column(visible=False) as lesson_page:
        gr.Markdown("## 🏗️ GRIND GLITCH KNOWLEDGE FORGE")
        gr.Markdown("### Crafting galactic wisdom - you deserve universe-class education!")

        topic_input = gr.Textbox(
            label="Learning Module Topic:",
            placeholder="Enter the subject for cosmic knowledge synthesis...",
            lines=2
        )
        lesson_btn = gr.Button("FORGE STELLAR LESSON", variant="primary")
        lesson_output = gr.Markdown("", elem_classes=["output-text"])

        back_lesson_btn = gr.Button("RETURN TO COMMAND CENTER", variant="secondary")

    # Challenge Creator Page
    with gr.Column(visible=False) as challenge_page:
        gr.Markdown("## 🎲 GRIND GLITCH MISSION CREATOR")
        gr.Markdown("### Generating cosmic challenges - because you deserve the best practice!")

        subject_input = gr.Textbox(
            label="Challenge Parameters:",
            placeholder="Enter subject area for stellar challenge generation...",
            lines=2
        )
        create_btn = gr.Button("DEPLOY COSMIC CHALLENGES", variant="primary")
        challenge_output = gr.Markdown("", elem_classes=["output-text"])

        back_challenge_btn = gr.Button("RETURN TO COMMAND CENTER", variant="secondary")

    # Event handlers
    start_btn.click(start_tutor, outputs=[page_1, page_2])

    back_btn.click(go_back, outputs=[page_1, page_2, ask_oracle_page, training_page, lesson_page, challenge_page])
    back_oracle_btn.click(go_back, outputs=[page_1, page_2, ask_oracle_page, training_page, lesson_page, challenge_page])
    back_training_btn.click(go_back, outputs=[page_1, page_2, ask_oracle_page, training_page, lesson_page, challenge_page])
    back_lesson_btn.click(go_back, outputs=[page_1, page_2, ask_oracle_page, training_page, lesson_page, challenge_page])
    back_challenge_btn.click(go_back, outputs=[page_1, page_2, ask_oracle_page, training_page, lesson_page, challenge_page])

    oracle_btn.click(show_ask_oracle, outputs=[page_2, ask_oracle_page])
    training_btn.click(show_training, outputs=[page_2, training_page])
    lesson_btn.click(show_lesson_builder, outputs=[page_2, lesson_page])
    challenge_btn.click(show_challenge_creator, outputs=[page_2, challenge_page])

    ask_btn.click(ask_ai_tutor, inputs=[question_input], outputs=[oracle_output])
    generate_btn.click(generate_practice, outputs=[training_output])
    lesson_btn.click(create_lesson, inputs=[topic_input], outputs=[lesson_output])
    create_btn.click(create_questions, inputs=[subject_input], outputs=[challenge_output])

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False,
        show_error=True,
        quiet=False
    )