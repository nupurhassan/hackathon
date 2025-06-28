import gradio as gr
import random

# Global state for user progress
user_stats = {
    "xp": 0,
    "level": 1,
    "questions_solved": 0,
    "lessons_completed": 0
}

def calculate_level(xp):
    return min(10, (xp // 100) + 1)

def add_xp(points):
    user_stats["xp"] += points
    user_stats["level"] = calculate_level(user_stats["xp"])
    return user_stats

# Custom CSS for retro AI tutor aesthetic with floating UFOs
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap');

/* Global styling */
.gradio-container {
    background: #000 !important;
    color: #00ff00 !important;
    font-family: 'Orbitron', monospace !important;
    min-height: 100vh !important;
    overflow-x: hidden !important;
}

/* Hide gradio header and footer */
.gradio-container .main > .wrap {
    background: #000 !important;
}

/* Main container styling */
#component-0 {
    background: #000 !important;
    border: none !important;
    min-height: 100vh !important;
    position: relative !important;
}

/* Floating UFOs */
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

/* Additional falling stars layers */
.gradio-container::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(2px 2px at 5% 30%, #00ff00, transparent),
        radial-gradient(3px 3px at 95% 10%, #00ff00, transparent),
        radial-gradient(2px 2px at 20% 60%, #00ff00, transparent),
        radial-gradient(4px 4px at 80% 40%, #00ff00, transparent),
        radial-gradient(2px 2px at 45% 80%, #00ff00, transparent),
        radial-gradient(3px 3px at 65% 20%, #00ff00, transparent),
        radial-gradient(2px 2px at 35% 45%, #00ff00, transparent),
        radial-gradient(3px 3px at 75% 70%, #00ff00, transparent),
        radial-gradient(2px 2px at 55% 15%, #00ff00, transparent),
        radial-gradient(4px 4px at 25% 85%, #00ff00, transparent);
    background-size: 
        180px 100vh,
        260px 100vh,
        200px 100vh,
        140px 100vh,
        220px 100vh,
        170px 100vh,
        250px 100vh,
        190px 100vh,
        230px 100vh,
        160px 100vh;
    animation: 
        falling-stars-4 15s linear infinite,
        falling-stars-5 9s linear infinite,
        falling-stars-6 11s linear infinite;
    pointer-events: none;
    z-index: 1;
    opacity: 0.6;
}

@keyframes falling-stars-4 {
    0% { transform: translateY(-100vh) translateX(-20px); }
    100% { transform: translateY(100vh) translateX(30px); }
}

@keyframes falling-stars-5 {
    0% { transform: translateY(-100vh) translateX(15px); }
    100% { transform: translateY(100vh) translateX(-25px); }
}

@keyframes falling-stars-6 {
    0% { transform: translateY(-100vh) translateX(10px); }
    100% { transform: translateY(100vh) translateX(20px); }
}

/* Falling stars container */
.gradio-container::after {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(3px 3px at 10% 10%, #00ff00, transparent),
        radial-gradient(2px 2px at 90% 20%, #00ff00, transparent),
        radial-gradient(4px 4px at 30% 5%, #00ff00, transparent),
        radial-gradient(2px 2px at 70% 15%, #00ff00, transparent),
        radial-gradient(3px 3px at 50% 8%, #00ff00, transparent),
        radial-gradient(2px 2px at 15% 25%, #00ff00, transparent),
        radial-gradient(3px 3px at 85% 35%, #00ff00, transparent),
        radial-gradient(2px 2px at 40% 30%, #00ff00, transparent),
        radial-gradient(4px 4px at 60% 12%, #00ff00, transparent),
        radial-gradient(2px 2px at 25% 40%, #00ff00, transparent);
    background-size: 
        200px 100vh,
        150px 100vh,
        300px 100vh,
        180px 100vh,
        250px 100vh,
        220px 100vh,
        190px 100vh,
        280px 100vh,
        160px 100vh,
        240px 100vh;
    animation: 
        falling-stars-1 8s linear infinite,
        falling-stars-2 12s linear infinite,
        falling-stars-3 10s linear infinite;
    pointer-events: none;
    z-index: 1;
    opacity: 0.8;
}

@keyframes falling-stars-1 {
    0% { transform: translateY(-100vh) translateX(0px); }
    100% { transform: translateY(100vh) translateX(50px); }
}

@keyframes falling-stars-2 {
    0% { transform: translateY(-100vh) translateX(20px); }
    100% { transform: translateY(100vh) translateX(-30px); }
}

@keyframes falling-stars-3 {
    0% { transform: translateY(-100vh) translateX(-10px); }
    100% { transform: translateY(100vh) translateX(40px); }
}

@keyframes float {
    0%, 100% { transform: translateY(0px) translateX(0px); }
    25% { transform: translateY(-15px) translateX(30px); }
    50% { transform: translateY(5px) translateX(-20px); }
    75% { transform: translateY(-10px) translateX(15px); }
}

/* Scan lines effect */
.gradio-container {
    background-image: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0, 255, 0, 0.03) 2px,
        rgba(0, 255, 0, 0.03) 4px
    );
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    min-height: 100vh !important;
}

/* Title styling */
.gradio-container h1 {
    color: #00ff00 !important;
    text-align: center !important;
    font-size: 3.5rem !important;
    font-weight: 900 !important;
    text-shadow: 0 0 20px #00ff00, 0 0 40px #00ff00 !important;
    margin: 1rem 0 !important;
    font-family: 'Orbitron', monospace !important;
    letter-spacing: 0.2em !important;
    animation: glow 2s ease-in-out infinite alternate !important;
    z-index: 10 !important;
    position: relative !important;
}

.gradio-container h2 {
    color: #00ff00 !important;
    text-align: center !important;
    font-size: 2.5rem !important;
    font-weight: 700 !important;
    text-shadow: 0 0 15px #00ff00 !important;
    margin: 1rem 0 !important;
    font-family: 'Orbitron', monospace !important;
    letter-spacing: 0.15em !important;
    z-index: 10 !important;
    position: relative !important;
}

.gradio-container h3 {
    color: #00ccff !important;
    text-align: center !important;
    font-size: 1.8rem !important;
    font-weight: 600 !important;
    text-shadow: 0 0 10px #00ccff !important;
    margin: 0.5rem 0 !important;
    font-family: 'Orbitron', monospace !important;
    z-index: 10 !important;
    position: relative !important;
}

@keyframes glow {
    from { text-shadow: 0 0 20px #00ff00, 0 0 30px #00ff00, 0 0 40px #00ff00; }
    to { text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00, 0 0 30px #00ff00; }
}

/* Button styling */
.gradio-container button {
    background: linear-gradient(145deg, #00ff00, #00cc00) !important;
    color: #000 !important;
    border: 3px solid #00ff00 !important;
    border-radius: 0 !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    padding: 15px 40px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.2em !important;
    box-shadow: 
        0 0 15px #00ff00,
        inset 0 0 15px rgba(255,255,255,0.2) !important;
    transition: all 0.3s ease !important;
    position: relative !important;
    z-index: 10 !important;
    margin: 0.8rem !important;
    min-width: 250px !important;
    image-rendering: pixelated !important;
}

.gradio-container button:hover {
    background: linear-gradient(145deg, #00ff00, #00ff00) !important;
    box-shadow: 
        0 0 25px #00ff00,
        0 0 40px #00ff00,
        inset 0 0 25px rgba(255,255,255,0.3) !important;
    transform: scale(1.05) translateY(-3px) !important;
    text-shadow: 0 0 10px #000 !important;
}

.gradio-container button:active {
    transform: scale(0.98) !important;
    box-shadow: 
        0 0 10px #00ff00,
        inset 0 0 10px rgba(0,0,0,0.2) !important;
}

/* Special button variants */
.start-button {
    font-size: 2.2rem !important;
    padding: 25px 70px !important;
    margin: 2rem auto !important;
    display: block !important;
}

/* Stats display */
.stats-container {
    background: rgba(0, 255, 0, 0.1) !important;
    border: 2px solid #00ff00 !important;
    border-radius: 10px !important;
    padding: 15px !important;
    margin: 1rem auto !important;
    max-width: 400px !important;
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.3) !important;
    text-align: center !important;
    z-index: 10 !important;
    position: relative !important;
}

.stats-text {
    color: #00ff00 !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 1.1rem !important;
    margin: 5px 0 !important;
}

/* Text areas and inputs */
.gradio-container textarea, .gradio-container input {
    background: rgba(0, 50, 0, 0.8) !important;
    border: 2px solid #00ff00 !important;
    border-radius: 5px !important;
    color: #00ff00 !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 1rem !important;
    padding: 10px !important;
    box-shadow: inset 0 0 10px rgba(0, 255, 0, 0.2) !important;
}

.gradio-container textarea:focus, .gradio-container input:focus {
    border-color: #00ff00 !important;
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.5) !important;
    outline: none !important;
}

/* Output styling */
.gradio-container .output-text {
    background: rgba(0, 40, 0, 0.9) !important;
    border: 2px solid #00ff00 !important;
    border-radius: 8px !important;
    color: #00ff00 !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 1.1rem !important;
    padding: 20px !important;
    margin: 1rem auto !important;
    box-shadow: 0 0 20px rgba(0, 255, 0, 0.3) !important;
    line-height: 1.6 !important;
    z-index: 10 !important;
    position: relative !important;
}

/* Center content */
.gradio-container .contain {
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
    min-height: 100vh !important;
    text-align: center !important;
    z-index: 10 !important;
    position: relative !important;
    padding: 20px !important;
    margin: 0 auto !important;
    max-width: 1200px !important;
}

/* Better centering for all content */
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

/* Grid layout for buttons */
.button-grid {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)) !important;
    gap: 20px !important;
    max-width: 800px !important;
    margin: 2rem auto !important;
    padding: 20px !important;
}

/* Hide gradio branding */
.footer {
    display: none !important;
}

.gradio-container .version {
    display: none !important;
}

/* Achievement notifications */
.achievement {
    background: linear-gradient(145deg, #ffaa00, #ff8800) !important;
    color: #000 !important;
    border: 3px solid #ffaa00 !important;
    border-radius: 10px !important;
    padding: 15px !important;
    margin: 10px !important;
    font-family: 'Orbitron', monospace !important;
    font-weight: bold !important;
    text-align: center !important;
    animation: achievement-pop 0.5s ease-out !important;
    box-shadow: 0 0 20px #ffaa00 !important;
}

@keyframes achievement-pop {
    0% { transform: scale(0.8) translateY(20px); opacity: 0; }
    100% { transform: scale(1) translateY(0); opacity: 1; }
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

# Functions for different features
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
        return "ERROR: Please enter a question to receive wisdom from the AI Oracle!"

    # Add XP for asking questions
    add_xp(10)
    user_stats["questions_solved"] += 1

    responses = [
        f"PROCESSING QUERY... \n\n**AI ORACLE RESPONSE:** \n\nYour question '{question}' is an excellent inquiry! Let me break this down for you:\n\n**ANALYSIS:** This topic requires understanding of fundamental concepts.\n\n**SOLUTION APPROACH:** \n1. Start with the basics\n2. Build upon core principles\n3. Apply logical reasoning\n\n**NEXT STEPS:** Practice similar problems to reinforce learning!\n\n**+10 XP GAINED!** | Level: {user_stats['level']} | Total XP: {user_stats['xp']}",

        f"KNOWLEDGE SCAN COMPLETE... \n\n**TUTOR ANALYSIS:** \n\nFor '{question}', here's your personalized learning path:\n\n**CONCEPT BREAKDOWN:** \n• Key principle identification\n• Step-by-step methodology\n• Real-world applications\n\n**MASTERY TIP:** Connect this to previous knowledge for better retention!\n\n**ACHIEVEMENT UNLOCKED:** Curious Learner! \n**+10 XP** | Level: {user_stats['level']} | Total XP: {user_stats['xp']}",

        f"QUANTUM LEARNING ACTIVATED... \n\n**DEEP DIVE ANALYSIS:** \n\nYour question '{question}' demonstrates critical thinking! \n\n**SOLUTION MATRIX:** \n→ Foundation concepts ✓\n→ Advanced applications ✓\n→ Problem-solving strategies ✓\n\n**PRO TIP:** Try explaining this concept to someone else - it's the ultimate test!\n\n**PROGRESS UPDATE:** +10 XP | Level: {user_stats['level']} | Questions Solved: {user_stats['questions_solved']}"
    ]

    return random.choice(responses)

def generate_practice():
    add_xp(15)

    practice_sets = [
        f"TRAINING MODE ACTIVATED! \n\n**DRILL SEQUENCE #{random.randint(1000, 9999)}:** \n\n**Practice Question 1:** \nSolve for x: 2x + 5 = 15 \n\n**Practice Question 2:** \nWhat is the derivative of x²? \n\n**Practice Question 3:** \nExplain the water cycle in 3 steps \n\n**BONUS CHALLENGE:** Create your own similar problem! \n\n**+15 XP GAINED!** | Level: {user_stats['level']} | Total XP: {user_stats['xp']}",

        f"CHALLENGE PROTOCOL INITIALIZED! \n\n**SKILL BUILDER ROUND #{random.randint(100, 999)}:** \n\n**Brain Teaser 1:** \nIf 5 machines make 5 widgets in 5 minutes, how long for 100 machines to make 100 widgets? \n\n**Brain Teaser 2:** \nWhat comes next in the sequence: 2, 6, 12, 20, 30, ? \n\n**Brain Teaser 3:** \nA book costs $10 plus half its price. What's the total cost? \n\n**MASTERY METER:** Rising! Keep training, warrior! \n\n**+15 XP** | Level: {user_stats['level']}"
    ]

    return random.choice(practice_sets)

def create_lesson(topic):
    if not topic.strip():
        return "ERROR: Please specify a topic for lesson generation!"

    add_xp(25)
    user_stats["lessons_completed"] += 1

    return f"KNOWLEDGE FORGE ACTIVATED! \n\n**GENERATING LESSON: '{topic.upper()}'** \n\n**LESSON STRUCTURE:** \n\n**INTRODUCTION** \nFoundational concepts and importance \n\n**CORE CONCEPTS** \n• Key definitions and principles \n• Visual aids and examples \n• Interactive demonstrations \n\n**PRACTICAL APPLICATIONS** \n• Real-world scenarios \n• Hands-on exercises \n• Problem-solving techniques \n\n**ASSESSMENT** \n• Quick comprehension check \n• Practice problems \n• Extended challenges \n\n**RESOURCES** \n• Additional reading materials \n• Video tutorials \n• Interactive simulations \n\n**LESSON BUILDER ACHIEVEMENT UNLOCKED!** \n**+25 XP** | Level: {user_stats['level']} | Lessons Created: {user_stats['lessons_completed']} | Total XP: {user_stats['xp']}"

def create_questions(subject):
    if not subject.strip():
        return "ERROR: Please specify a subject for question generation!"

    add_xp(20)

    question_types = [
        f"CHALLENGE CREATOR ONLINE! \n\n**QUESTION BANK: '{subject.upper()}'** \n\n**EASY LEVEL:** \n• Multiple choice fundamentals \n• True/false basics \n• Fill-in-the-blank concepts \n\n**MEDIUM LEVEL:** \n• Short answer applications \n• Problem-solving scenarios \n• Concept connections \n\n**HARD LEVEL:** \n• Essay-style analysis \n• Multi-step calculations \n• Critical thinking challenges \n\n**BOSS LEVEL:** \n• Research projects \n• Creative applications \n• Cross-disciplinary synthesis \n\n**+20 XP** | Level: {user_stats['level']} | Total XP: {user_stats['xp']}",

        f"RANDOM QUESTION GENERATOR ACTIVATED! \n\n**SUBJECT: '{subject.upper()}'** \n\n**Sample Questions Generated:** \n\n? What are the key principles of {subject}? \n? How does {subject} apply to real-world situations? \n? Compare and contrast different aspects of {subject} \n? Analyze the impact of {subject} on society \n? Design an experiment to test {subject} concepts \n\n**DIFFICULTY MODES:** \nBeginner | Intermediate | Advanced | Expert \n\n**QUESTION MASTER BADGE EARNED!** \n**+20 XP** | Level: {user_stats['level']}"
    ]

    return random.choice(question_types)

def get_stats():
    return f"**PLAYER STATS** \n\n**LEVEL:** {user_stats['level']} \n**TOTAL XP:** {user_stats['xp']} \n**QUESTIONS SOLVED:** {user_stats['questions_solved']} \n**LESSONS COMPLETED:** {user_stats['lessons_completed']} \n\n**NEXT LEVEL:** {(user_stats['level'] * 100) - user_stats['xp']} XP remaining"

# Create the Gradio interface
with gr.Blocks(css=custom_css, title="RETRO AI TUTOR") as demo:

    # Add UFO HTML elements
    gr.HTML(inject_ufos())

    # Page 1: Landing Page
    with gr.Column(visible=True) as page_1:
        gr.Markdown("# RETRO AI TUTOR")
        gr.Markdown("### INITIALIZE LEARNING PROTOCOL")
        gr.Markdown("*Your personal AI learning companion with retro gaming vibes*")

        start_btn = gr.Button("ACTIVATE TUTOR", elem_classes=["start-button"], variant="primary")

    # Page 2: Main Menu
    with gr.Column(visible=False) as page_2:
        gr.Markdown("## LEARNING COMMAND CENTER")
        gr.Markdown("### Choose your learning adventure!")

        # Stats display
        stats_display = gr.Markdown(get_stats(), elem_classes=["stats-container"])

        with gr.Row():
            with gr.Column():
                oracle_btn = gr.Button("ASK THE ORACLE\n*Get AI-powered answers*", variant="primary")
                training_btn = gr.Button("TRAINING MODE\n*Practice questions & drills*", variant="primary")
            with gr.Column():
                lesson_btn = gr.Button("KNOWLEDGE FORGE\n*Generate custom lessons*", variant="primary")
                challenge_btn = gr.Button("CHALLENGE CREATOR\n*Build practice questions*", variant="primary")

        back_btn = gr.Button("RETURN TO START", variant="secondary")

    # Ask Oracle Page
    with gr.Column(visible=False) as ask_oracle_page:
        gr.Markdown("## AI ORACLE CHAMBER")
        gr.Markdown("### Ask any question and receive wisdom!")

        question_input = gr.Textbox(
            label="Your Question:",
            placeholder="Enter your question here...",
            lines=3
        )
        ask_btn = gr.Button("CONSULT ORACLE", variant="primary")
        oracle_output = gr.Markdown("", elem_classes=["output-text"])

        back_oracle_btn = gr.Button("BACK TO MENU", variant="secondary")

    # Training Mode Page
    with gr.Column(visible=False) as training_page:
        gr.Markdown("## TRAINING CHAMBER")
        gr.Markdown("### Sharpen your skills with practice questions!")

        generate_btn = gr.Button("GENERATE PRACTICE SET", variant="primary")
        training_output = gr.Markdown("", elem_classes=["output-text"])

        back_training_btn = gr.Button("BACK TO MENU", variant="secondary")

    # Lesson Builder Page
    with gr.Column(visible=False) as lesson_page:
        gr.Markdown("## KNOWLEDGE FORGE")
        gr.Markdown("### Create comprehensive lessons on any topic!")

        topic_input = gr.Textbox(
            label="Lesson Topic:",
            placeholder="Enter the topic you want to learn about...",
            lines=2
        )
        lesson_btn = gr.Button("FORGE LESSON", variant="primary")
        lesson_output = gr.Markdown("", elem_classes=["output-text"])

        back_lesson_btn = gr.Button("BACK TO MENU", variant="secondary")

    # Challenge Creator Page
    with gr.Column(visible=False) as challenge_page:
        gr.Markdown("## CHALLENGE CREATOR")
        gr.Markdown("### Generate practice questions for any subject!")

        subject_input = gr.Textbox(
            label="Subject:",
            placeholder="Enter the subject for question generation...",
            lines=2
        )
        create_btn = gr.Button("CREATE CHALLENGES", variant="primary")
        challenge_output = gr.Markdown("", elem_classes=["output-text"])

        back_challenge_btn = gr.Button("BACK TO MENU", variant="secondary")

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
        server_port=7861,  # Changed to 7861
        share=False,
        show_error=True,
        quiet=False
    )