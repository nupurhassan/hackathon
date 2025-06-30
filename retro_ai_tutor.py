import gradio as gr
import random
import requests
import json
import numpy as np
from time import perf_counter

# Global state for user progress
user_stats = {
    "xp": 0,
    "level": 1,
    "questions_solved": 0,
    "lessons_completed": 0,
    "benchmarks_run": 0
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
        return f"NETWORK ERROR: Connection to AI Oracle failed. Please check your connection and try again.\n\nError details: {str(e)}"
    except KeyError as e:
        return f"API ERROR: Unexpected response format from AI Oracle.\n\nError details: {str(e)}"
    except Exception as e:
        return f"SYSTEM ERROR: An unexpected error occurred.\n\nError details: {str(e)}"

def calculate_level(xp):
    return min(10, (xp // 100) + 1)

def add_xp(points):
    user_stats["xp"] += points
    user_stats["level"] = calculate_level(user_stats["xp"])
    return user_stats

def spaceship_engine_status():
    """Monitor real-time GPU acceleration and engine status"""
    add_xp(25)

    try:
        import cupy as cp
        import numpy as np
        from time import perf_counter

        results = []
        results.append("SPACESHIP ENGINE STATUS MONITOR")
        results.append("=" * 55)
        results.append("")

        # GPU Detection and Basic Info
        try:
            gpu_info = cp.cuda.runtime.getDeviceProperties(0)
            memory_info = cp.cuda.runtime.memGetInfo()

            results.append("WARP DRIVE CORE STATUS")
            results.append(f"    Engine Model: {gpu_info['name'].decode()}")
            results.append(f"    Processing Cores: {gpu_info['multiProcessorCount']}")
            results.append(f"    Max Clock Speed: {gpu_info['clockRate'] // 1000} MHz")
            results.append("")

            # Memory Status
            free_mem = memory_info[0] // (1024**3)
            total_mem = memory_info[1] // (1024**3)
            used_mem = total_mem - free_mem
            usage_percent = (used_mem / total_mem) * 100

            results.append("STELLAR MEMORY BANKS")
            results.append(f"    Total Capacity: {total_mem} GB")
            results.append(f"    Available: {free_mem} GB")
            results.append(f"    In Use: {used_mem} GB ({usage_percent:.1f}%)")

            # Memory status indicator
            if usage_percent < 30:
                mem_status = "OPTIMAL - Ready for Deep Space Missions"
            elif usage_percent < 70:
                mem_status = "MODERATE - System Running Efficiently"
            else:
                mem_status = "HIGH - Consider Memory Optimization"

            results.append(f"    Status: {mem_status}")
            results.append("")

        except Exception as e:
            results.append("WARP DRIVE OFFLINE")
            results.append("   CPU-only navigation mode active")
            results.append("")

        # Acceleration Test
        results.append("LIVE ACCELERATION TEST")
        try:
            # Quick performance test
            size = 1024
            A_cpu = np.random.rand(size, size).astype(np.float32)
            B_cpu = np.random.rand(size, size).astype(np.float32)

            # CPU test
            start_time = perf_counter()
            C_cpu = np.matmul(A_cpu, B_cpu)
            cpu_time = perf_counter() - start_time

            # GPU test
            A_gpu = cp.array(A_cpu)
            B_gpu = cp.array(B_cpu)

            start_time = perf_counter()
            C_gpu = cp.matmul(A_gpu, B_gpu)
            cp.cuda.Device().synchronize()
            gpu_time = perf_counter() - start_time

            speedup = cpu_time / gpu_time

            results.append(f"    CPU Engine: {cpu_time:.4f}s")
            results.append(f"    GPU Engine: {gpu_time:.4f}s")
            results.append(f"    Warp Factor: {speedup:.1f}x acceleration")

            # Engine performance status
            if speedup >= 20:
                engine_status = "HYPERDRIVE - Maximum Efficiency"
            elif speedup >= 10:
                engine_status = "WARP DRIVE - Excellent Performance"
            elif speedup >= 5:
                engine_status = "IMPULSE - Good Acceleration"
            else:
                engine_status = "THRUSTER - Basic Propulsion"

            results.append(f"    Engine Class: {engine_status}")
            results.append("")

            # Cleanup
            del A_cpu, B_cpu, C_cpu, A_gpu, B_gpu, C_gpu

        except Exception as e:
            results.append("    Acceleration test failed - Running on backup thrusters")
            results.append("")

        # Engine Recommendations
        results.append("STELLAR ENGINEERING REPORT")
        try:
            if usage_percent > 80:
                results.append("    High memory usage detected")
                results.append("    Recommend closing background processes")
            elif speedup >= 15:
                results.append("    Warp drives operating at peak efficiency")
                results.append("    Ready for advanced computational missions")
            elif speedup >= 8:
                results.append("    Good engine performance detected")
                results.append("    Consider upgrading for maximum acceleration")
            else:
                results.append("    Suboptimal acceleration detected")
                results.append("    Recommend warp drive diagnostics")
        except:
            results.append("    GPU acceleration unavailable")
            results.append("    Install CUDA drivers for warp drive activation")

        results.append("")
        results.append("=" * 55)
        results.append(f"ENGINE MONITOR ACHIEVEMENT! +25 XP")
        results.append(f"Current Rank: Level {user_stats['level']} | Total XP: {user_stats['xp']}")
        results.append("=" * 55)

        return "\n".join(results)

    except ImportError:
        return f"WARP DRIVE MODULES OFFLINE\n\nEngine monitoring requires stellar libraries:\n- CuPy for GPU acceleration\n- NumPy for backup thrusters\n\nInstall required modules to activate spaceship engines."
    except Exception as e:
        return f"ENGINE DIAGNOSTIC ERROR\n\nUnexpected engine malfunction: {str(e)}\n\nRecommend immediate engineering inspection."

def gpu_benchmark():
    """Run comprehensive GPU benchmarks and return cosmic-style results"""
    add_xp(50)
    user_stats["benchmarks_run"] += 1

    try:
        import cupy as cp
        import pandas as pd
        import numpy as np
        from time import perf_counter

        results = []
        results.append("STELLAR PERFORMANCE ANALYSIS INITIATED")
        results.append("=" * 60)
        results.append("")

        # GPU Detection
        try:
            gpu_info = cp.cuda.runtime.getDeviceProperties(0)
            results.append(f"STARSHIP PROCESSOR DETECTED: {gpu_info['name'].decode()}")
            results.append(f"ENERGY CORES: {gpu_info['multiProcessorCount']}")
            results.append(f"MEMORY BANKS: {gpu_info['totalGlobalMem'] // (1024**3)} GB")
            results.append("")
        except:
            results.append("STARSHIP PROCESSOR STATUS: OFFLINE")
            results.append("")

        # CuPy Matrix Operations Benchmark
        results.append("MATRIX COMPUTATION ENGINE TEST")
        size = 2048

        # CPU Baseline
        A_cpu = np.random.rand(size, size).astype(np.float32)
        B_cpu = np.random.rand(size, size).astype(np.float32)

        start_time = perf_counter()
        C_cpu = np.matmul(A_cpu, B_cpu)
        cpu_time = perf_counter() - start_time

        # GPU Acceleration
        A_gpu = cp.array(A_cpu)
        B_gpu = cp.array(B_cpu)
        cp.matmul(A_gpu, B_gpu)  # Warmup

        start_time = perf_counter()
        C_gpu = cp.matmul(A_gpu, B_gpu)
        cp.cuda.Device().synchronize()
        gpu_time = perf_counter() - start_time

        speedup = cpu_time / gpu_time
        results.append(f"    CPU PROCESSING TIME: {cpu_time:.4f} seconds")
        results.append(f"    GPU ACCELERATION TIME: {gpu_time:.4f} seconds")
        results.append(f"    WARP SPEED BOOST: {speedup:.2f}x FASTER")
        results.append("")

        # Memory Bandwidth Test
        results.append("STELLAR MEMORY BANDWIDTH ANALYSIS")
        data_size = 100_000_000
        test_data = cp.random.rand(data_size, dtype=cp.float32)

        start_time = perf_counter()
        result = cp.sum(test_data)
        cp.cuda.Device().synchronize()
        bandwidth_time = perf_counter() - start_time

        bandwidth_gb = (data_size * 4) / (bandwidth_time * 1e9)  # GB/s
        results.append(f"    MEMORY BANDWIDTH: {bandwidth_gb:.2f} GB/s")
        results.append("")

        # cuDF Data Processing Benchmark
        results.append("STELLAR DATA PROCESSING ENGINE TEST")
        try:
            # Enable cudf.pandas acceleration
            import cudf.pandas
            cudf.pandas.install()

            n = 1_000_000
            data = {
                'stellar_id': np.random.randint(0, 1000, n),
                'energy_level': np.random.randn(n),
                'cosmic_flux': np.random.randn(n)
            }

            df = pd.DataFrame(data)

            start_time = perf_counter()
            result = df.groupby('stellar_id').agg({
                'energy_level': ['sum', 'mean'],
                'cosmic_flux': ['min', 'max']
            })
            data_time = perf_counter() - start_time

            results.append(f"    DATA ANALYSIS TIME: {data_time:.4f} seconds")
            results.append(f"    RECORDS PROCESSED: {n:,} stellar objects")
            results.append("")

        except ImportError:
            results.append("    RAPIDS cuDF engine offline - Standard processing active")
            results.append("")

        # Performance Classification
        results.append("STARSHIP PERFORMANCE CLASSIFICATION")
        if speedup >= 50:
            classification = "HYPERDRIVE CLASS - FEDERATION FLAGSHIP"
        elif speedup >= 20:
            classification = "WARP DRIVE CLASS - DEEP SPACE EXPLORER"
        elif speedup >= 10:
            classification = "IMPULSE CLASS - SYSTEM PATROL VESSEL"
        elif speedup >= 5:
            classification = "THRUSTER CLASS - ORBITAL TRANSPORT"
        else:
            classification = "MAINTENANCE CLASS - DOCK FOR UPGRADES"

        results.append(f"    {classification}")
        results.append("")

        # System Recommendations
        results.append("STELLAR ENGINEERING RECOMMENDATIONS")
        if speedup >= 30:
            results.append("    WARP CORES OPERATING AT PEAK EFFICIENCY")
            results.append("    READY FOR ADVANCED DEEP LEARNING MISSIONS")
        elif speedup >= 15:
            results.append("    EXCELLENT ACCELERATION DETECTED")
            results.append("    OPTIMAL FOR SCIENTIFIC COMPUTING OPERATIONS")
        elif speedup >= 8:
            results.append("    GOOD PERFORMANCE - MINOR OPTIMIZATIONS POSSIBLE")
            results.append("    CONSIDER MEMORY OPTIMIZATION PROTOCOLS")
        else:
            results.append("    SUBOPTIMAL PERFORMANCE DETECTED")
            results.append("    RECOMMEND WARP CORE DIAGNOSTICS")

        results.append("")
        results.append("=" * 60)
        results.append(f"BENCHMARK MASTER ACHIEVEMENT UNLOCKED! +50 XP")
        results.append(f"CURRENT RANK: Level {user_stats['level']} | Total XP: {user_stats['xp']}")
        results.append(f"BENCHMARKS COMPLETED: {user_stats['benchmarks_run']}")
        results.append("=" * 60)

        # Cleanup
        del A_cpu, B_cpu, C_cpu, A_gpu, B_gpu, C_gpu, test_data
        if 'df' in locals():
            del df

        return "\n".join(results)

    except ImportError as e:
        return f"STELLAR ACCELERATION MODULES OFFLINE\n\nMissing stellar libraries: {str(e)}\n\nPlease install: cupy, cudf, rapids for full performance analysis."
    except Exception as e:
        return f"SYSTEM DIAGNOSTIC ERROR\n\nUnexpected stellar anomaly detected: {str(e)}\n\nRecommend system recalibration and retry."

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

/* Title styling - Main ship computer display */
.gradio-container h1 {
    color: #00ff88 !important;
    text-align: center !important;
    font-size: 4.5rem !important;
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
    font-size: 2.8rem !important;
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
    font-size: 2.0rem !important;
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
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    padding: 22px 40px !important;
    text-transform: uppercase !important;
    letter-spacing: 0.15em !important;
    
    box-shadow: 
        0 0 20px rgba(0, 255, 136, 0.4),
        inset 0 2px 0 rgba(255, 255, 255, 0.2),
        inset 0 -2px 0 rgba(0, 0, 0, 0.3),
        inset 2px 0 0 rgba(0, 255, 136, 0.2),
        inset -2px 0 0 rgba(0, 0, 0, 0.2),
        0 4px 8px rgba(0, 0, 0, 0.3) !important;
    
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    position: relative !important;
    z-index: 10 !important;
    margin: 0.8rem !important;
    min-width: 320px !important;
    
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
    
    background-attachment: fixed !important;
    backdrop-filter: blur(2px) !important;
}

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
        0 0 35px rgba(0, 255, 136, 0.7),
        0 0 60px rgba(0, 255, 136, 0.4),
        inset 0 3px 0 rgba(255, 255, 255, 0.3),
        inset 0 -3px 0 rgba(0, 0, 0, 0.4),
        inset 3px 0 0 rgba(0, 255, 136, 0.3),
        inset -3px 0 0 rgba(0, 0, 0, 0.3),
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
    font-size: 1.4rem !important;
    margin: 8px 0 !important;
    text-shadow: 0 0 5px #00ff88 !important;
}

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
    font-size: 1.3rem !important;
    padding: 18px !important;
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
    font-size: 1.3rem !important;
    padding: 28px !important;
    margin: 1rem auto !important;
    box-shadow: 
        0 0 25px rgba(0, 255, 136, 0.3),
        inset 0 0 15px rgba(0, 255, 136, 0.1) !important;
    line-height: 1.8 !important;
    z-index: 10 !important;
    position: relative !important;
    backdrop-filter: blur(3px) !important;
}

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

.button-grid {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)) !important;
    gap: 25px !important;
    max-width: 900px !important;
    margin: 2rem auto !important;
    padding: 25px !important;
}

.footer {
    display: none !important;
}

/* Alien celebration animation */
@keyframes alien-flyby {
    0% { 
        transform: translateX(-200px) translateY(20px) rotate(-10deg) scale(0.8);
        opacity: 0;
    }
    20% {
        opacity: 1;
        transform: translateX(-50px) translateY(0px) rotate(0deg) scale(1);
    }
    50% {
        transform: translateX(50px) translateY(-10px) rotate(5deg) scale(1.1);
    }
    80% {
        transform: translateX(150px) translateY(0px) rotate(0deg) scale(1);
    }
    100% { 
        transform: translateX(300px) translateY(20px) rotate(10deg) scale(0.8);
        opacity: 0;
    }
}

@keyframes celebration-text {
    0% { 
        transform: translateY(50px) scale(0);
        opacity: 0;
    }
    20% {
        transform: translateY(0px) scale(1.2);
        opacity: 1;
    }
    80% {
        transform: translateY(-10px) scale(1);
        opacity: 1;
    }
    100% {
        transform: translateY(-50px) scale(0.8);
        opacity: 0;
    }
}

.alien-celebration {
    position: fixed;
    top: 20%;
    left: 0;
    width: 100%;
    height: 200px;
    pointer-events: none;
    z-index: 1000;
    display: none;
}

.alien-ship {
    position: absolute;
    width: 80px;
    height: 40px;
    background: linear-gradient(to bottom, #00ff00, #00cc00);
    border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
    box-shadow: 
        0 0 20px #00ff00,
        0 -6px 0 #00ff00,
        0 6px 0 rgba(0, 255, 0, 0.3),
        inset 0 2px 0 rgba(255, 255, 255, 0.3);
    animation: alien-flyby 3s ease-in-out;
}

.alien-ship::before {
    content: '';
    position: absolute;
    top: -15px;
    left: 50%;
    transform: translateX(-50%);
    width: 25px;
    height: 15px;
    background: linear-gradient(to bottom, #00ff00, #00aa00);
    border-radius: 50%;
    box-shadow: 0 0 10px #00ff00;
}

.alien-ship::after {
    content: '';
    position: absolute;
    bottom: -8px;
    left: 50%;
    transform: translateX(-50%);
    width: 100px;
    height: 6px;
    background: radial-gradient(ellipse, rgba(0, 255, 0, 0.6), transparent);
    border-radius: 50%;
    animation: beam-pulse 0.5s ease-in-out infinite;
}

.celebration-message {
    position: absolute;
    top: 60px;
    left: 50%;
    transform: translateX(-50%);
    color: #00ff00;
    font-family: 'Orbitron', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    text-shadow: 0 0 15px #00ff00;
    animation: celebration-text 3s ease-in-out;
    white-space: nowrap;
}

.show-celebration {
    display: block !important;
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

# Course roadmap data structure
COURSE_ROADMAP = {
    "chapters": [
        {
            "id": 1,
            "title": "Introduction to Machine Learning",
            "youtube_url": "https://youtu.be/f1OXmHzg-G8?feature=shared",
            "textbook_chapter": "Chapter 1",
            "topics": [
                "What is Machine Learning?",
                "Types of Learning (Supervised, Unsupervised, Reinforcement)",
                "Learning Problems and Applications",
                "Basic Notation and Terminology"
            ],
            "prerequisites": [],
            "estimated_time": "2-3 hours"
        },
        {
            "id": 2,
            "title": "The PAC Learning Framework",
            "youtube_url": "https://youtu.be/Olqi2aMGdFg?feature=shared",
            "textbook_chapter": "Chapter 2",
            "topics": [
                "Probably Approximately Correct (PAC) Learning",
                "Sample Complexity",
                "Computational Complexity",
                "Realizable and Agnostic Cases"
            ],
            "prerequisites": ["Introduction to Machine Learning"],
            "estimated_time": "4-5 hours"
        },
        {
            "id": 3,
            "title": "Rademacher Complexity and VC Dimension",
            "youtube_url": "https://youtu.be/tVxzEWiSQ-E?feature=shared",
            "textbook_chapter": "Chapter 3",
            "topics": [
                "Rademacher Complexity",
                "Vapnik-Chervonenkis (VC) Dimension",
                "Growth Function and Shattering",
                "Generalization Bounds"
            ],
            "prerequisites": ["The PAC Learning Framework"],
            "estimated_time": "5-6 hours"
        },
        {
            "id": 4,
            "title": "Model Selection",
            "youtube_url": "https://youtu.be/4E-FdkzQCII?feature=shared",
            "textbook_chapter": "Chapter 4",
            "topics": [
                "Cross-Validation",
                "Bias-Variance Tradeoff",
                "Structural Risk Minimization",
                "Stability and Generalization"
            ],
            "prerequisites": ["Rademacher Complexity and VC Dimension"],
            "estimated_time": "4-5 hours"
        },
        {
            "id": 5,
            "title": "Support Vector Machines",
            "youtube_url": "https://youtu.be/MsnKd864RsE?feature=shared",
            "textbook_chapter": "Chapter 5",
            "topics": [
                "Linear Separators",
                "Margin and Support Vectors",
                "Dual Formulation",
                "Soft Margin SVM"
            ],
            "prerequisites": ["Model Selection"],
            "estimated_time": "6-7 hours"
        },
        {
            "id": 6,
            "title": "Kernel Methods",
            "youtube_url": "https://youtu.be/h2lV0LNY3QE?feature=shared",
            "textbook_chapter": "Chapter 6",
            "topics": [
                "Kernel Functions",
                "Reproducing Kernel Hilbert Spaces",
                "Kernel Perceptron",
                "Gaussian and Polynomial Kernels"
            ],
            "prerequisites": ["Support Vector Machines"],
            "estimated_time": "5-6 hours"
        },
        {
            "id": 7,
            "title": "Boosting",
            "youtube_url": "https://youtu.be/6dGAiP4KHt4?feature=shared",
            "textbook_chapter": "Chapter 7",
            "topics": [
                "AdaBoost Algorithm",
                "Weak Learning",
                "Boosting Theory",
                "Generalization Bounds for Boosting"
            ],
            "prerequisites": ["Kernel Methods"],
            "estimated_time": "5-6 hours"
        },
        {
            "id": 8,
            "title": "On-Line Learning",
            "youtube_url": "https://youtu.be/km1zuclkmYE?feature=shared",
            "textbook_chapter": "Chapter 8",
            "topics": [
                "Online Learning Model",
                "Perceptron Algorithm",
                "Winnow Algorithm",
                "Regret Bounds"
            ],
            "prerequisites": ["Boosting"],
            "estimated_time": "4-5 hours"
        },
        {
            "id": 9,
            "title": "Multi-Class Classification",
            "youtube_url": "https://youtu.be/PylsjhpKrIc?feature=shared",
            "textbook_chapter": "Chapter 9",
            "topics": [
                "One-vs-All Strategy",
                "All-Pairs Strategy",
                "Error-Correcting Output Codes",
                "Multi-Class SVMs"
            ],
            "prerequisites": ["On-Line Learning"],
            "estimated_time": "4-5 hours"
        },
        {
            "id": 10,
            "title": "Ranking",
            "youtube_url": "https://youtu.be/P0jvO2t12tU?feature=shared",
            "textbook_chapter": "Chapter 10",
            "topics": [
                "Ranking Problems",
                "RankBoost Algorithm",
                "Bipartite Ranking",
                "AUC Optimization"
            ],
            "prerequisites": ["Multi-Class Classification"],
            "estimated_time": "4-5 hours"
        },
        {
            "id": 11,
            "title": "Regression",
            "youtube_url": "https://youtu.be/lLoHsno0hk8?feature=shared",
            "textbook_chapter": "Chapter 11",
            "topics": [
                "Linear Regression",
                "Ridge Regression",
                "Lasso Regression",
                "Kernel Ridge Regression"
            ],
            "prerequisites": ["Ranking"],
            "estimated_time": "5-6 hours"
        },
        {
            "id": 12,
            "title": "Maximum Entropy Models",
            "youtube_url": "https://youtu.be/2gTrsLVnp9c?feature=shared",
            "textbook_chapter": "Chapter 12",
            "topics": [
                "Maximum Entropy Principle",
                "Exponential Families",
                "Logistic Regression",
                "Feature Selection"
            ],
            "prerequisites": ["Regression"],
            "estimated_time": "5-6 hours"
        },
        {
            "id": 13,
            "title": "Conditional Maximum Entropy Models",
            "youtube_url": "https://youtu.be/2gTrsLVnp9c?feature=shared",
            "textbook_chapter": "Chapter 13",
            "topics": [
                "Conditional Models",
                "Conditional Random Fields",
                "Parameter Estimation",
                "Inference Algorithms"
            ],
            "prerequisites": ["Maximum Entropy Models"],
            "estimated_time": "5-6 hours"
        },
        {
            "id": 14,
            "title": "Algorithmic Stability",
            "youtube_url": "https://youtu.be/vPmR8kYYB_g?feature=shared",
            "textbook_chapter": "Chapter 14",
            "topics": [
                "Uniform Stability",
                "Hypothesis Stability",
                "Stability and Generalization",
                "Regularization and Stability"
            ],
            "prerequisites": ["Conditional Maximum Entropy Models"],
            "estimated_time": "4-5 hours"
        },
        {
            "id": 15,
            "title": "Dimensionality Reduction",
            "youtube_url": "https://youtu.be/3lPtXlRQd44?feature=shared",
            "textbook_chapter": "Chapter 15",
            "topics": [
                "Principal Component Analysis (PCA)",
                "Linear Discriminant Analysis (LDA)",
                "Johnson-Lindenstrauss Lemma",
                "Random Projections"
            ],
            "prerequisites": ["Algorithmic Stability"],
            "estimated_time": "5-6 hours"
        },
        {
            "id": 16,
            "title": "Learning Automata and Languages",
            "youtube_url": "https://youtu.be/lzscfkFsWQM?feature=shared",
            "textbook_chapter": "Chapter 16",
            "topics": [
                "Finite Automata",
                "Regular Languages",
                "Context-Free Grammars",
                "Learning Algorithms for Languages"
            ],
            "prerequisites": ["Dimensionality Reduction"],
            "estimated_time": "6-7 hours"
        },
        {
            "id": 17,
            "title": "Reinforcement Learning",
            "youtube_url": "https://youtu.be/FhgL3nFSQbQ?feature=shared",
            "textbook_chapter": "Chapter 17",
            "topics": [
                "Markov Decision Processes",
                "Value Functions",
                "Policy Gradient Methods",
                "Q-Learning Algorithm"
            ],
            "prerequisites": ["Learning Automata and Languages"],
            "estimated_time": "6-8 hours"
        }
    ]
}

# User progress tracking
user_progress = {
    "completed_chapters": [],
    "current_chapter": 1,
    "chapter_scores": {},
    "total_course_progress": 0
}

# Sample questions for each chapter (these would be expanded with actual textbook problems)
CHAPTER_QUESTIONS = {
    1: [
        {
            "question": "What are the three main types of machine learning paradigms?",
            "type": "multiple_choice",
            "options": ["Supervised, Unsupervised, Reinforcement", "Classification, Regression, Clustering", "Linear, Nonlinear, Deep", "Batch, Online, Semi-supervised"],
            "correct": 0,
            "explanation": "The three main paradigms are Supervised Learning (learning from labeled data), Unsupervised Learning (finding patterns in unlabeled data), and Reinforcement Learning (learning through interaction with an environment)."
        },
        {
            "question": "Define what makes a learning problem 'supervised'.",
            "type": "short_answer",
            "sample_answer": "Supervised learning involves learning from labeled training data, where each example has an input and a corresponding desired output. The goal is to learn a function that maps inputs to outputs.",
            "keywords": ["labeled", "training data", "input", "output", "function", "mapping"]
        }
    ],
    2: [
        {
            "question": "In PAC learning, what does 'probably approximately correct' mean?",
            "type": "short_answer",
            "sample_answer": "PAC means that with high probability (probably), the learned hypothesis will have low error (approximately correct). Specifically, with probability at least (1-δ), the error is at most ε.",
            "keywords": ["probability", "error", "hypothesis", "delta", "epsilon", "approximately"]
        },
        {
            "question": "What is sample complexity in the context of PAC learning?",
            "type": "multiple_choice",
            "options": ["The number of features in the data", "The minimum number of samples needed to achieve PAC learning", "The computational time required", "The size of the hypothesis space"],
            "correct": 1,
            "explanation": "Sample complexity refers to the minimum number of training examples required to ensure that a learning algorithm produces a hypothesis that is PAC-learnable."
        }
    ]
    # Additional questions would be added for each chapter
}

def get_chapter_info(chapter_id):
    """Get detailed information about a specific chapter"""
    chapter = COURSE_ROADMAP["chapters"][chapter_id - 1]
    return chapter

def check_prerequisites(chapter_id):
    """Check if user has completed prerequisites for a chapter"""
    chapter = get_chapter_info(chapter_id)
    if not chapter["prerequisites"]:
        return True

    for prereq in chapter["prerequisites"]:
        prereq_id = next((c["id"] for c in COURSE_ROADMAP["chapters"] if c["title"] == prereq), None)
        if prereq_id not in user_progress["completed_chapters"]:
            return False
    return True

def calculate_course_progress():
    """Calculate overall course progress"""
    total_chapters = len(COURSE_ROADMAP["chapters"])
    completed = len(user_progress["completed_chapters"])
    return (completed / total_chapters) * 100

def generate_roadmap_display():
    """Generate a visual roadmap of the course with enhanced formatting"""
    roadmap = ["FOUNDATIONS OF MACHINE LEARNING - COURSE ROADMAP"]
    roadmap.append("=" * 70)
    roadmap.append("")

    total_progress = calculate_course_progress()
    roadmap.append(f"MISSION STATUS: {total_progress:.1f}% Complete")
    roadmap.append(f"CHAPTERS COMPLETED: {len(user_progress['completed_chapters'])}/{len(COURSE_ROADMAP['chapters'])}")
    roadmap.append(f"CURRENT CHAPTER: {user_progress['current_chapter']}")
    roadmap.append("")
    roadmap.append("CHAPTER NAVIGATION MAP:")
    roadmap.append("-" * 40)
    roadmap.append("")

    for i, chapter in enumerate(COURSE_ROADMAP["chapters"], 1):
        # Determine status
        if i in user_progress["completed_chapters"]:
            status = "[✓ COMPLETED]"
            status_color = ""
        elif i == user_progress["current_chapter"]:
            status = "[► CURRENT]"
            status_color = ""
        elif check_prerequisites(i):
            status = "[○ AVAILABLE]"
            status_color = ""
        else:
            status = "[🔒 LOCKED]"
            status_color = ""

        roadmap.append(f"{status} CHAPTER {i:2d}: {chapter['title']}")

        # Add key info
        roadmap.append(f"     ⏱️  Duration: {chapter['estimated_time']}")
        roadmap.append(f"     📺 Video: Available")
        roadmap.append(f"     📖 Textbook: {chapter['textbook_chapter']}")

        # Show prerequisites if any
        if chapter["prerequisites"]:
            prereq_text = ", ".join(chapter["prerequisites"])
            if len(prereq_text) > 50:
                prereq_text = prereq_text[:47] + "..."
            roadmap.append(f"     📋 Prerequisites: {prereq_text}")

        # Show some key topics
        key_topics = chapter["topics"][:2]  # Show first 2 topics
        for topic in key_topics:
            roadmap.append(f"     • {topic}")
        if len(chapter["topics"]) > 2:
            roadmap.append(f"     • ... and {len(chapter['topics']) - 2} more topics")

        roadmap.append("")

    roadmap.append("=" * 70)
    roadmap.append("COMMAND PROTOCOLS:")
    roadmap.append("• START CHAPTER X - Begin specific chapter (replace X with 1-17)")
    roadmap.append("• ASSESSMENT - Take quiz for current chapter")
    roadmap.append("• Enter any topic - Generate custom lesson")
    roadmap.append("")
    roadmap.append("LEARNING RESOURCES:")
    roadmap.append("• Textbook & Solutions: github.com/nupurhassan/Foundations-of-Machine-Learning-secound-edition-Textbook-and-solution")
    roadmap.append("• Video Lectures: Linked in each chapter")
    roadmap.append("• Interactive Assessments: Available after each chapter")
    roadmap.append("")
    roadmap.append(f"CURRENT RANK: Level {user_stats['level']} | Total XP: {user_stats['xp']}")
    roadmap.append("=" * 70)

    return "\n".join(roadmap)

def start_chapter(chapter_num):
    """Start a specific chapter with content and assessment"""
    try:
        chapter_id = int(chapter_num)
        if chapter_id < 1 or chapter_id > len(COURSE_ROADMAP["chapters"]):
            return "ERROR: Invalid chapter number. Please enter a number between 1 and 17."

        if not check_prerequisites(chapter_id):
            chapter = get_chapter_info(chapter_id)
            return f"ERROR: Prerequisites not met for Chapter {chapter_id}. You need to complete: {', '.join(chapter['prerequisites'])}"

        chapter = get_chapter_info(chapter_id)
        user_progress["current_chapter"] = chapter_id

        content = []
        content.append(f"CHAPTER {chapter_id}: {chapter['title'].upper()}")
        content.append("=" * 60)
        content.append("")
        content.append("MISSION BRIEFING:")
        content.append(f"Estimated Time: {chapter['estimated_time']}")
        content.append(f"Textbook Reference: {chapter['textbook_chapter']}")
        content.append("")
        content.append("VIDEO LECTURE:")
        content.append(f"Watch: {chapter['youtube_url']}")
        content.append("")
        content.append("LEARNING OBJECTIVES:")
        for topic in chapter["topics"]:
            content.append(f"- {topic}")
        content.append("")
        content.append("TEXTBOOK MATERIALS:")
        content.append("- Read the corresponding chapter in the textbook")
        content.append("- Review the solution manual for practice problems")
        content.append("- Complete the end-of-chapter exercises")
        content.append("")
        content.append("ASSESSMENT CHECKPOINT:")
        content.append("After studying the materials, you'll answer questions to test your understanding.")
        content.append("")
        content.append("=" * 60)
        content.append("Ready to begin? Type 'ASSESSMENT' to start the chapter quiz!")

        return "\n".join(content)

    except ValueError:
        return "ERROR: Please enter a valid chapter number (1-17)."

def generate_chapter_assessment(chapter_id):
    """Generate assessment questions for a chapter"""
    if chapter_id not in CHAPTER_QUESTIONS:
        return "Assessment questions not available for this chapter yet."

    questions = CHAPTER_QUESTIONS[chapter_id]
    assessment = []
    assessment.append(f"CHAPTER {chapter_id} ASSESSMENT")
    assessment.append("=" * 40)
    assessment.append("")

    for i, q in enumerate(questions, 1):
        assessment.append(f"QUESTION {i}:")
        assessment.append(q["question"])
        assessment.append("")

        if q["type"] == "multiple_choice":
            for j, option in enumerate(q["options"]):
                assessment.append(f"{chr(65+j)}. {option}")
            assessment.append("")
        elif q["type"] == "short_answer":
            assessment.append("(Provide a brief explanation in your own words)")
            assessment.append("")

    assessment.append("=" * 40)
    assessment.append("Submit your answers to proceed to the next chapter!")

    return "\n".join(assessment)

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
        challenge_page: gr.update(visible=False),
        benchmark_page: gr.update(visible=False),
        engine_page: gr.update(visible=False)
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

def show_gpu_benchmark():
    return {
        page_2: gr.update(visible=False),
        benchmark_page: gr.update(visible=True)
    }

def show_spaceship_engine():
    return {
        page_2: gr.update(visible=False),
        engine_page: gr.update(visible=True)
    }

# Oracle session state
oracle_session = {
    "is_initialized": False,
    "current_topic": None,
    "lesson_step": 0,
    "awaiting_confirmation": False,
    "awaiting_answer": False,
    "practice_count": 0,
    "user_answers": []
}

def ask_ai_tutor(question):
    """Enhanced AI tutor with structured interactive lesson flow"""
    if not question.strip():
        return "ERROR: Please enter a question to receive wisdom from the AI Oracle!", ""

    # Initialize Oracle session if first interaction
    if not oracle_session["is_initialized"]:
        oracle_session["is_initialized"] = True
        welcome_message = """GRIND GLITCH ORACLE CHAMBER ACTIVATED
        
ANALYSIS COMPLETE - Interactive Learning Protocol Engaged

Welcome, Commander! I am your AI Tutor Oracle, designed to guide you through structured learning experiences.

LEARNING PROTOCOL INITIATED:
Which topic would you like to learn today?

IMPORTANT: Please specify ONE topic at a time for optimal learning efficiency.

Examples:
- "Machine Learning Basics"
- "Linear Regression"  
- "Support Vector Machines"
- "Python Functions"
- "Photosynthesis"
- "Algebra Equations"

Awaiting your topic selection..."""
        return welcome_message, ""

    # Topic confirmation flow
    if not oracle_session["awaiting_confirmation"] and oracle_session["current_topic"] is None:
        oracle_session["current_topic"] = question.strip()
        oracle_session["awaiting_confirmation"] = True
        return f"TOPIC CONFIRMATION REQUIRED:\n\nSo we'll be exploring '{oracle_session['current_topic']}', correct?\n\nPlease respond with 'YES' to confirm or provide a different topic.", ""

    # Handle topic confirmation
    if oracle_session["awaiting_confirmation"]:
        if question.upper() in ["YES", "Y", "CONFIRM", "CORRECT"]:
            oracle_session["awaiting_confirmation"] = False
            oracle_session["lesson_step"] = 1

            # Generate structured lesson using AI
            system_prompt = f"""You are an expert AI Tutor Bot following an interactive lesson flow for the topic: {oracle_session['current_topic']}

LESSON STEP 1 - CONCEPTUAL EXPLANATION:
- Provide a clear, concise definition of {oracle_session['current_topic']}
- Explain why it matters and real-world contexts where it's applied
- Use headers like "PROCESSING KNOWLEDGE MATRIX", "ANALYSIS COMPLETE"
- Keep the retro gaming space theme
- End with: "Do you have any questions or need clarification before we practice?"

Format your response with clear sections and gaming-style headers."""

            prompt = f"Provide step 1 conceptual explanation for topic: {oracle_session['current_topic']}"

            add_xp(10)
            user_stats["questions_solved"] += 1

            ai_response = call_nvidia_api(prompt, system_prompt)

            if "XP" not in ai_response:
                ai_response += f"\n\n+10 XP GAINED! | Level: {user_stats['level']} | Total XP: {user_stats['xp']}"

            return ai_response, ""
        else:
            # Reset and ask for new topic
            oracle_session["current_topic"] = question.strip()
            return f"TOPIC UPDATED:\n\nSo we'll be exploring '{oracle_session['current_topic']}', correct?\n\nPlease respond with 'YES' to confirm or provide a different topic.", ""

    # Handle lesson progression
    if oracle_session["lesson_step"] == 1:
        # Check for doubts after conceptual explanation
        if question.upper() in ["NO", "NO QUESTIONS", "CLEAR", "UNDERSTOOD", "PROCEED", "CONTINUE"]:
            oracle_session["lesson_step"] = 2

            system_prompt = f"""You are an expert AI Tutor Bot. 

LESSON STEP 2 - GUIDED EXAMPLE:
- Work through one step-by-step example problem for {oracle_session['current_topic']}
- Label and explain each step clearly
- Show your reasoning process
- Use gaming headers like "EXAMPLE SIMULATION ACTIVATED"
- End with the first practice question for the student to solve
- Format: "PRACTICE MISSION 1: [question]"

Make the example and practice question appropriate for {oracle_session['current_topic']}"""

            prompt = f"Provide guided example and first practice question for: {oracle_session['current_topic']}"
            ai_response = call_nvidia_api(prompt, system_prompt)
            oracle_session["awaiting_answer"] = True
            oracle_session["practice_count"] = 1

            return ai_response, ""
        else:
            # Handle clarification questions
            system_prompt = f"""You are an expert AI Tutor Bot. The student has a question about {oracle_session['current_topic']}.

Provide a clear, helpful clarification while maintaining the gaming theme. After answering, ask again: "Do you have any questions or need clarification before we practice?"

Student's question: {question}"""

            ai_response = call_nvidia_api(question, system_prompt)
            return ai_response, ""

    # Handle practice answers
    if oracle_session["awaiting_answer"] and oracle_session["practice_count"] <= 3:
        oracle_session["user_answers"].append(question)

        system_prompt = f"""You are an expert AI Tutor Bot evaluating a student's answer for {oracle_session['current_topic']}.

EVALUATION PROTOCOL:
- Analyze if the answer is correct or incorrect
- If correct: Congratulate and provide next practice question
- If incorrect: Pinpoint the error and provide corrective guidance
- Use gaming-style feedback
- This is practice question #{oracle_session['practice_count']}

Student's answer: {question}
Practice count: {oracle_session['practice_count']}/3

If this is practice 3 and still incorrect, provide the full solution."""

        prompt = f"Evaluate student answer for {oracle_session['current_topic']} practice #{oracle_session['practice_count']}: {question}"
        ai_response = call_nvidia_api(prompt, system_prompt)

        oracle_session["practice_count"] += 1

        if oracle_session["practice_count"] > 3:
            oracle_session["awaiting_answer"] = False
            oracle_session["lesson_step"] = 3
            ai_response += f"\n\nMISSION COMPLETE! You've finished the structured lesson on {oracle_session['current_topic']}.\n\nTo start a new topic, simply tell me what you'd like to learn next!"

            # Reset session for new topic
            oracle_session["current_topic"] = None
            oracle_session["lesson_step"] = 0
            oracle_session["practice_count"] = 0
            oracle_session["user_answers"] = []

        return ai_response, ""

    # Fallback for any other interactions
    system_prompt = """You are GRIND GLITCH Oracle AI. Provide helpful responses while maintaining the retro gaming space theme."""
    ai_response = call_nvidia_api(question, system_prompt)
    return ai_response, ""

def generate_practice():
    """Enhanced training with structured interactive lesson flow"""
    # Initialize Training session if first interaction
    if not training_session["is_initialized"]:
        training_session["is_initialized"] = True
        welcome_message = """STELLAR TRAINING BAY ACTIVATED
        
TRAINING PROTOCOL INITIATED

Welcome to the Stellar Training Bay, Commander! I am your specialized Training AI, designed to guide you through intensive practice sessions.

TRAINING PROTOCOL:
Which topic would you like to train on today?

MISSION PARAMETERS: Please specify ONE topic at a time for optimal training efficiency.

Training Examples:
- "Calculus Derivatives"
- "Physics Momentum" 
- "Chemistry Balancing Equations"
- "Programming Loops"
- "Statistics Probability"
- "Geometry Theorems"

Awaiting your training topic selection..."""
        return welcome_message

    add_xp(15)

    system_prompt = """You are GRIND GLITCH Training Mode AI that generates practice questions and exercises following the structured interactive lesson flow.
    
    TRAINING PROTOCOL:
    1. Topic Inquiry & Confirmation
    2. Conceptual Explanation 
    3. Guided Example
    4. Check for Doubts
    5. Progressive Practice Questions (3 levels)
    6. Evaluate and Feedback
    7. Final Wrap-Up
    
    Use retro space-gaming style with headers like "TRAINING PODS ACTIVATED", "COSMIC DRILL SEQUENCE", "STELLAR CHALLENGE PROTOCOL".
    Generate comprehensive training sessions with the gaming theme.
    Remember: we're here to help because users deserve the best education.
    End with XP information."""

    prompt = f"Generate a comprehensive training session. The student just gained +15 XP and is now Level {user_stats['level']} with {user_stats['xp']} total XP."

    ai_response = call_nvidia_api(prompt, system_prompt)

    if "XP" not in ai_response:
        ai_response += f"\n\n+15 XP GAINED! | Level: {user_stats['level']} | Total XP: {user_stats['xp']}"

    return ai_response

# Knowledge Forge session state
knowledge_forge_session = {
    "is_initialized": False,
    "current_mode": None,  # "roadmap", "chapter", "assessment", "custom"
    "current_chapter": None,
    "awaiting_input": False
}

def create_lesson(topic):
    """Enhanced lesson creation with roadmap integration and structured learning"""
    if not topic.strip():
        return "ERROR: Please specify a topic for lesson generation!", ""

    # Initialize Knowledge Forge if first interaction
    if not knowledge_forge_session["is_initialized"]:
        knowledge_forge_session["is_initialized"] = True
        welcome_message = """GRIND GLITCH KNOWLEDGE FORGE ACTIVATED

STELLAR KNOWLEDGE SYNTHESIS PROTOCOL INITIATED

Welcome to the Knowledge Forge, Commander! I am your Learning Architecture AI, capable of multiple learning modes:

AVAILABLE COMMAND PROTOCOLS:

1. ROADMAP MODE:
   - Type 'ROADMAP' to view the complete ML course structure
   - Track your progress through 17 comprehensive chapters
   - See prerequisites and unlock new content

2. CHAPTER MODE:
   - Type 'START CHAPTER X' (where X = 1-17) to begin specific chapters
   - Access video lectures, textbook references, and structured content
   - Each chapter includes learning objectives and materials

3. ASSESSMENT MODE:
   - Type 'ASSESSMENT' to take quizzes for your current chapter
   - Interactive questions with immediate feedback
   - Progress tracking and achievement unlocking

4. CUSTOM LESSON MODE:
   - Enter any topic for AI-generated custom lessons
   - Comprehensive lesson plans with examples and exercises
   - Personalized learning content creation

MISSION SELECTION:
Which learning protocol would you like to activate?

Examples:
- 'ROADMAP' - View course structure
- 'START CHAPTER 1' - Begin Introduction to ML
- 'ASSESSMENT' - Take current chapter quiz
- 'Neural Networks' - Create custom lesson

Awaiting your command, Commander..."""
        return welcome_message, ""

    # Check if it's a roadmap command
    if topic.upper().startswith("ROADMAP"):
        knowledge_forge_session["current_mode"] = "roadmap"
        return generate_roadmap_display(), ""

    # Check if it's a chapter start command
    if topic.upper().startswith("START CHAPTER"):
        try:
            chapter_num = topic.split()[-1]
            knowledge_forge_session["current_mode"] = "chapter"
            knowledge_forge_session["current_chapter"] = int(chapter_num)
            return start_chapter(chapter_num), ""
        except:
            return "ERROR: Please use format 'START CHAPTER X' where X is the chapter number (1-17).", ""

    # Check if it's an assessment command
    if topic.upper() == "ASSESSMENT":
        knowledge_forge_session["current_mode"] = "assessment"
        current_chapter = user_progress.get("current_chapter", 1)
        return generate_chapter_assessment(current_chapter), ""

    # Check if it's a chapter-specific query
    for chapter in COURSE_ROADMAP["chapters"]:
        if any(keyword.lower() in topic.lower() for keyword in chapter["title"].split()):
            knowledge_forge_session["current_mode"] = "chapter_info"
            chapter_info = f"CHAPTER {chapter['id']}: {chapter['title']}\n\n"
            chapter_info += f"YouTube Video: {chapter['youtube_url']}\n"
            chapter_info += f"Textbook: {chapter['textbook_chapter']}\n\n"
            chapter_info += "Key Topics:\n"
            for t in chapter["topics"]:
                chapter_info += f"- {t}\n"
            chapter_info += f"\nEstimated Time: {chapter['estimated_time']}\n"
            chapter_info += f"\nTo start this chapter, type: START CHAPTER {chapter['id']}"
            return chapter_info, ""

    # Regular lesson creation with AI - Custom Lesson Mode
    knowledge_forge_session["current_mode"] = "custom"
    add_xp(25)
    user_stats["lessons_completed"] += 1

    system_prompt = """You are GRIND GLITCH Knowledge Forge AI, a cosmic lesson architect with retro space-gaming personality.

LESSON CONSTRUCTION PROTOCOL:
Follow this exact interactive lesson flow for any topic:

1. **Topic Analysis & Overview**
   - Provide a clear, comprehensive definition of the topic
   - Explain why it matters and real-world applications
   - Set learning objectives for the session

2. **Conceptual Foundation**
   - Break down core concepts and principles
   - Use analogies and examples for clarity
   - Build knowledge systematically

3. **Guided Examples**
   - Work through detailed step-by-step examples
   - Show reasoning and problem-solving process
   - Multiple examples of increasing complexity

4. **Interactive Elements**
   - Pose questions to check understanding
   - Provide practice problems for hands-on learning
   - Include self-assessment opportunities

5. **Advanced Applications**
   - Show how concepts apply in complex scenarios
   - Connect to related topics and fields
   - Demonstrate practical implementations

6. **Summary & Next Steps**
   - Summarize key takeaways
   - Suggest follow-up topics or advanced study
   - Provide resources for continued learning

Use headers like "STELLAR KNOWLEDGE FORGE ACTIVATED", "CONCEPTUAL MATRIX LOADING", "LEARNING PROTOCOLS ENGAGED".
Maintain the cosmic gaming theme while delivering comprehensive educational content.
Remember: we're here to help because you deserve the universe's best education."""

    prompt = f"Create a comprehensive, structured lesson on the topic: '{topic}'. Follow the interactive lesson flow protocol. The student just gained +25 XP, completed {user_stats['lessons_completed']} lessons, and is now Level {user_stats['level']} with {user_stats['xp']} total XP."

    ai_response = call_nvidia_api(prompt, system_prompt)

    if "XP" not in ai_response:
        ai_response += f"\n\nLESSON BUILDER ACHIEVEMENT! +25 XP | Level: {user_stats['level']} | Lessons Created: {user_stats['lessons_completed']} | Total XP: {user_stats['xp']}"

    return ai_response, ""

def create_questions(subject):
    """Enhanced challenge creator with ML textbook exam generation"""
    if not subject.strip():
        return "ERROR: Please specify a subject for question generation!", ""

    # Initialize Challenge session if first interaction
    if not challenge_session["is_initialized"]:
        challenge_session["is_initialized"] = True
        welcome_message = """COSMIC CHALLENGE CREATOR ACTIVATED

EXAM GENERATION PROTOCOL INITIATED

Welcome, Commander! I am your AI Exam Generator Bot for "Foundations of Machine Learning, 2nd edition" by Mehryar Mohri, Afshin Rostamizadeh, and Ameet Talwalkar (MIT Press, 2018).

MISSION BRIEFING:
I will guide you through creating a custom exam with precise specifications.

STEP 1 - CONTENT SELECTION:
Which chapter(s) or section(s) would you like to include questions from?

Available Chapters:
1. Introduction to Machine Learning
2. PAC Learning Framework  
3. Rademacher Complexity and VC Dimension
4. Model Selection
5. Support Vector Machines
6. Kernel Methods
7. Boosting
8. On-Line Learning
9. Multi-Class Classification
10. Ranking
11. Regression
12. Maximum Entropy Models
13. Conditional Maximum Entropy Models
14. Algorithmic Stability
15. Dimensionality Reduction
16. Learning Automata and Languages
17. Reinforcement Learning

Please specify your chapter selection (e.g., "Chapter 3: Rademacher Complexity and VC-Dimension" or "Chapters 1-5")..."""
        return welcome_message, ""

    # Handle the step-by-step exam generation process
    if challenge_session["current_step"] == 0:
        # Step 1: Content Selection
        challenge_session["chapters_selected"] = subject
        challenge_session["current_step"] = 1
        return f"CONTENT CONFIRMED: {subject}\n\nSTEP 2 - QUESTION COUNT:\nHow many questions should the exam have?\n\nPlease enter a number (e.g., 10):", ""

    elif challenge_session["current_step"] == 1:
        # Step 2: Question Count
        try:
            challenge_session["question_count"] = int(subject)
            challenge_session["current_step"] = 2
            return f"QUESTION COUNT SET: {challenge_session['question_count']} questions\n\nSTEP 3 - QUESTION TYPES:\nWhat types of questions? Choose any combination of:\n- MCQ (Multiple Choice)\n- Short Answer\n- Long Answer\n\nPlease enter your selection (e.g., 'MCQ, Short Answer'):", ""
        except ValueError:
            return "ERROR: Please enter a valid number for question count.", ""

    elif challenge_session["current_step"] == 2:
        # Step 3: Question Types
        challenge_session["question_types"] = subject
        challenge_session["current_step"] = 3
        total_q = challenge_session["question_count"]
        return f"QUESTION TYPES SET: {subject}\n\nSTEP 4 - DIFFICULTY DISTRIBUTION:\nHow would you like the difficulty distributed?\nSpecify counts for easy, medium, and hard (total must equal {total_q}).\n\nExample format: 'easy: 3, medium: 4, hard: 3'\n\nPlease enter your distribution:", ""

    elif challenge_session["current_step"] == 3:
        # Step 4: Difficulty Distribution
        challenge_session["difficulty_distribution"] = subject
        challenge_session["current_step"] = 4

        # Generate the exam using AI
        system_prompt = f"""You are an AI Exam Generator Bot for "Foundations of Machine Learning, 2nd edition".

EXAM SPECIFICATIONS:
- Chapters: {challenge_session['chapters_selected']}
- Question Count: {challenge_session['question_count']}
- Question Types: {challenge_session['question_types']}
- Difficulty Distribution: {challenge_session['difficulty_distribution']}

GENERATION PROTOCOL:
1. Create questions based on specific concepts from the chosen chapters
2. For MCQ: Create stem + 4 options (1 correct, 3 distractors)
3. For Short Answer: Precise questions requiring few sentences or formulas
4. For Long Answer: Discussion/derivation questions needing paragraphs/proofs
5. Label each question with difficulty level
6. After all questions, provide complete answer key with explanations

Use gaming headers like "EXAM MATRIX GENERATING", "QUESTION FORGE ACTIVATED"
Format professionally but maintain the cosmic theme."""

        prompt = f"Generate a complete exam based on the specifications: Chapters: {challenge_session['chapters_selected']}, Count: {challenge_session['question_count']}, Types: {challenge_session['question_types']}, Difficulty: {challenge_session['difficulty_distribution']}"

        add_xp(20)
        ai_response = call_nvidia_api(prompt, system_prompt)

        challenge_session["generated_exam"] = ai_response

        ai_response += f"\n\nSTEP 5 - REVIEW & CUSTOMIZATION:\nWould you like to adjust any question or change the distribution?\nType 'ADJUST' to make changes or 'COMPLETE' to finish."

        if "XP" not in ai_response:
            ai_response += f"\n\nQUESTION MASTER BADGE! +20 XP | Level: {user_stats['level']} | Total XP: {user_stats['xp']}"

        return ai_response, ""

    elif challenge_session["current_step"] == 4:
        # Step 5: Review & Customization
        if subject.upper() == "COMPLETE":
            # Reset session for new exam
            challenge_session["is_initialized"] = False
            challenge_session["current_step"] = 0
            return "EXAM GENERATION COMPLETE!\n\nMission accomplished, Commander! Your custom exam has been generated.\n\nTo create another exam, simply enter a new subject or chapter selection.", ""
        elif subject.upper() == "ADJUST":
            return "ADJUSTMENT MODE ACTIVATED:\nPlease specify what you'd like to change:\n- 'CHANGE DIFFICULTY' - Modify difficulty distribution\n- 'CHANGE TYPES' - Modify question types\n- 'CHANGE COUNT' - Modify question count\n- 'REGENERATE' - Generate completely new questions", ""
        else:
            # Handle specific adjustments
            system_prompt = f"""You are an AI Exam Generator Bot handling exam adjustments.

Original Exam: {challenge_session['generated_exam']}
User Request: {subject}

Modify the exam according to the user's request while maintaining the cosmic gaming theme."""

            ai_response = call_nvidia_api(subject, system_prompt)
            return ai_response + "\n\nType 'COMPLETE' when satisfied or specify additional changes.", ""

    # Fallback - shouldn't reach here
    return "ERROR: Unknown state in challenge generation.", ""

def get_stats():
    return f"SHIP STATUS REPORT \n\nCOMMANDER LEVEL: {user_stats['level']} \nTOTAL XP: {user_stats['xp']} \nMISSIONS COMPLETED: {user_stats['questions_solved']} \nKNOWLEDGE MODULES: {user_stats['lessons_completed']} \nBENCHMARKS RUN: {user_stats['benchmarks_run']}\n\nNEXT RANK: {(user_stats['level'] * 100) - user_stats['xp']} XP to promotion"

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
        gr.Markdown("*Powered by NVIDIA Llama AI Core & GPU Acceleration*")

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
                engine_btn = gr.Button("SPACESHIP ENGINE\n*Monitor warp drive acceleration*", variant="primary")
            with gr.Column():
                lesson_btn = gr.Button("KNOWLEDGE FORGE\n*Universe-class custom lessons*", variant="primary")
                challenge_btn = gr.Button("COSMIC CHALLENGES\n*Galactic-level practice questions*", variant="primary")
                benchmark_btn = gr.Button("STELLAR BENCHMARK\n*Test your starship's processing power*", variant="primary")

        back_btn = gr.Button("MAIN CONSOLE", variant="secondary")

    # Ask Oracle Page
    with gr.Column(visible=False) as ask_oracle_page:
        gr.Markdown("## GRIND GLITCH ORACLE CHAMBER")
        gr.Markdown("### Accessing cosmic knowledge database...")
        gr.Markdown("*Interactive AI Tutor - Structured Learning Protocol*")
        gr.Markdown("**PROTOCOL:** Specify ONE topic at a time for optimal learning")

        oracle_output = gr.Markdown("", elem_classes=["output-text"])

        question_input = gr.Textbox(
            label="Query Input:",
            placeholder="Enter your topic or answer here...",
            lines=3
        )
        ask_btn = gr.Button("TRANSMIT QUERY", variant="primary")

        back_oracle_btn = gr.Button("RETURN TO COMMAND CENTER", variant="secondary")

    # Training Mode Page
    with gr.Column(visible=False) as training_page:
        gr.Markdown("## GRIND GLITCH TRAINING BAY")
        gr.Markdown("### Stellar practice sessions - because you deserve the best preparation!")
        gr.Markdown("**INTERACTIVE TRAINING PROTOCOL:** Structured lesson flow with progressive difficulty")
        gr.Markdown("*Specify ONE topic at a time for optimal training efficiency*")

        training_output = gr.Markdown("", elem_classes=["output-text"])

        training_input = gr.Textbox(
            label="Training Parameters:",
            placeholder="Enter specific training topic or answer here...",
            lines=2
        )
        generate_btn = gr.Button("INITIATE COSMIC TRAINING", variant="primary")

        back_training_btn = gr.Button("RETURN TO COMMAND CENTER", variant="secondary")

    # Lesson Builder Page
    with gr.Column(visible=False) as lesson_page:
        gr.Markdown("## GRIND GLITCH KNOWLEDGE FORGE")
        gr.Markdown("### Crafting galactic wisdom - you deserve universe-class education!")
        gr.Markdown("**MULTI-MODE LEARNING SYSTEM:**")
        gr.Markdown("🗺️ **ROADMAP** - Complete ML course structure with progress tracking")
        gr.Markdown("📚 **START CHAPTER X** - Begin specific chapters (1-17) with videos & materials")
        gr.Markdown("🎯 **ASSESSMENT** - Take interactive quizzes for current chapter")
        gr.Markdown("🔬 **CUSTOM LESSONS** - AI-generated lessons on any topic")
        gr.Markdown("*Four distinct learning modes in one unified interface*")

        lesson_output = gr.Markdown("", elem_classes=["output-text"])

        topic_input = gr.Textbox(
            label="Learning Module Command:",
            placeholder="Try: 'ROADMAP', 'START CHAPTER 1', 'ASSESSMENT', or any custom topic...",
            lines=2
        )
        lesson_create_btn = gr.Button("FORGE STELLAR LESSON", variant="primary")

        back_lesson_btn = gr.Button("RETURN TO COMMAND CENTER", variant="secondary")

    # Challenge Creator Page
    with gr.Column(visible=False) as challenge_page:
        gr.Markdown("## GRIND GLITCH MISSION CREATOR")
        gr.Markdown("### Generating cosmic challenges - because you deserve the best practice!")
        gr.Markdown("**AI EXAM GENERATOR:** For 'Foundations of Machine Learning, 2nd Edition'")
        gr.Markdown("*Step-by-step exam creation with custom specifications*")

        challenge_output = gr.Markdown("", elem_classes=["output-text"])

        subject_input = gr.Textbox(
            label="Challenge Parameters:",
            placeholder="Follow the guided process for exam generation...",
            lines=2
        )
        create_btn = gr.Button("DEPLOY COSMIC CHALLENGES", variant="primary")

        back_challenge_btn = gr.Button("RETURN TO COMMAND CENTER", variant="secondary")

    # GPU Benchmark Page
    with gr.Column(visible=False) as benchmark_page:
        gr.Markdown("## GRIND GLITCH STELLAR BENCHMARK")
        gr.Markdown("### Stellar performance analysis - test your starship's processing power!")
        gr.Markdown("*Analyzing warp cores and acceleration drives...*")

        benchmark_output = gr.Markdown("", elem_classes=["output-text"])

        benchmark_input = gr.Textbox(
            label="Benchmark Parameters:",
            placeholder="Optional: Enter specific benchmark settings or comments...",
            lines=2
        )
        run_benchmark_btn = gr.Button("INITIATE STELLAR ANALYSIS", variant="primary")

        back_benchmark_btn = gr.Button("RETURN TO COMMAND CENTER", variant="secondary")

    # Spaceship Engine Page
    with gr.Column(visible=False) as engine_page:
        gr.Markdown("## GRIND GLITCH ENGINE BAY")
        gr.Markdown("### Real-time warp drive monitoring and acceleration status")
        gr.Markdown("*Live diagnostics of your starship's computational engines...*")

        engine_output = gr.Markdown("", elem_classes=["output-text"])

        engine_input = gr.Textbox(
            label="Engine Parameters:",
            placeholder="Optional: Enter specific diagnostic parameters...",
            lines=2
        )
        monitor_engine_btn = gr.Button("SCAN ENGINE STATUS", variant="primary")

        back_engine_btn = gr.Button("RETURN TO COMMAND CENTER", variant="secondary")

    # Event handlers
    start_btn.click(start_tutor, outputs=[page_1, page_2])

    back_btn.click(go_back, outputs=[page_1, page_2, ask_oracle_page, training_page, lesson_page, challenge_page, benchmark_page, engine_page])
    back_oracle_btn.click(go_back, outputs=[page_1, page_2, ask_oracle_page, training_page, lesson_page, challenge_page, benchmark_page, engine_page])
    back_training_btn.click(go_back, outputs=[page_1, page_2, ask_oracle_page, training_page, lesson_page, challenge_page, benchmark_page, engine_page])
    back_lesson_btn.click(go_back, outputs=[page_1, page_2, ask_oracle_page, training_page, lesson_page, challenge_page, benchmark_page, engine_page])
    back_challenge_btn.click(go_back, outputs=[page_1, page_2, ask_oracle_page, training_page, lesson_page, challenge_page, benchmark_page, engine_page])
    back_benchmark_btn.click(go_back, outputs=[page_1, page_2, ask_oracle_page, training_page, lesson_page, challenge_page, benchmark_page, engine_page])
    back_engine_btn.click(go_back, outputs=[page_1, page_2, ask_oracle_page, training_page, lesson_page, challenge_page, benchmark_page, engine_page])

    oracle_btn.click(show_ask_oracle, outputs=[page_2, ask_oracle_page])
    training_btn.click(show_training, outputs=[page_2, training_page])
    lesson_btn.click(show_lesson_builder, outputs=[page_2, lesson_page])
    challenge_btn.click(show_challenge_creator, outputs=[page_2, challenge_page])
    benchmark_btn.click(show_gpu_benchmark, outputs=[page_2, benchmark_page])
    engine_btn.click(show_spaceship_engine, outputs=[page_2, engine_page])

    ask_btn.click(ask_ai_tutor, inputs=[question_input], outputs=[oracle_output, question_input])
    generate_btn.click(lambda x: (generate_practice(), ""), inputs=[training_input], outputs=[training_output, training_input])
    lesson_create_btn.click(create_lesson, inputs=[topic_input], outputs=[lesson_output, topic_input])
    create_btn.click(create_questions, inputs=[subject_input], outputs=[challenge_output, subject_input])
    run_benchmark_btn.click(lambda x: (gpu_benchmark(), ""), inputs=[benchmark_input], outputs=[benchmark_output, benchmark_input])
    monitor_engine_btn.click(lambda x: (spaceship_engine_status(), ""), inputs=[engine_input], outputs=[engine_output, engine_input])

if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False,
        show_error=True,
        quiet=False
    )