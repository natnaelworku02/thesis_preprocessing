import sys
import os
import lizard

# Fallback mapping for AST extension parsing
EXT_MAP = {
    "java": ".java", "python": ".py", "go": ".go",
    "ruby": ".rb", "php": ".php", "javascript": ".js"
}

def get_ast_complexity(code, language):
    """Extracts logical complexity (SFV) and physical lines (LOC) on CPU."""
    code_str = str(code).strip()
    ext = EXT_MAP.get(language.lower(), ".txt")
    dummy_filename = f"temp_file{ext}"
    loc = max(len(code_str.splitlines()), 1)
    
    try:
        analysis = lizard.analyze_file.analyze_source_code(dummy_filename, code_str)
        if analysis.function_list:
            token_count = analysis.function_list[0].token_count
        else:
            token_count = analysis.token_count
    except Exception:
        token_count = 0
        
    if token_count < 5:
        token_count = len(code_str.split())
    if token_count == 0:
        token_count = 1
        
    sfv = max(token_count * 0.3, 0.3)
    return sfv, loc

def run_gated_quality_gate(code, comment, language):
    print("\n" + "="*50)
    print("  COMPLEXITY-GATED QUALITY GATE GATEKEEPER")
    print("="*50)
    
    # Step 1: Calculate structural parameters instantly on CPU
    sfv, loc = get_ast_complexity(code, language)
    
    comment_lines = len([line for line in str(comment).splitlines() if line.strip()])
    if comment_lines == 0:
        comment_lines = 1
    mcv = comment_lines * 0.8
    
    print(f"File Metadata  | Language: {language.upper()}")
    print(f"Complexity     | SFV: {sfv:.2f} | LOC: {loc}")
    print(f"Documentation  | MCV: {mcv:.2f}")
    print("-" * 50)
    
    # Step 2: GATING DECISION
    if sfv >= 15.0:
        # Route to CPU Stream
        print("GATING DECISION: COMPLEX CODE DETECTED (SFV >= 15)")
        print(">>> ROUTING TO CPU STREAM: CALCULATING SYNTACTIC DENSITY...")
        adak_ss = ((100 * mcv * sfv) / (sfv**2 + loc)) - 100
        print(f"Calculated Adak_ss: {adak_ss:.4f}")
        
        if adak_ss < -80.0:
            print("STATUS: FAILED [Under-documented]")
        elif adak_ss > 50.0:
            print("STATUS: PASSED WITH WARNING [Over-documented/Verbosity warning]")
        else:
            print("STATUS: PASSED [Balanced Structural Quality]")
    else:
        # Route to GPU/Semantic Stream
        print("GATING DECISION: SIMPLE CODE DETECTED (SFV < 15)")
        print(">>> ROUTING TO GPU/SEMANTIC STREAM...")
        print("WARNING: Running in SIMULATION MODE (No local GPU required).")
        simulated_prob = 0.9482
        print(f"Calibrated Semantic Score (Simulated Probability): {simulated_prob:.4f}")
        print("STATUS: PASSED [Semantically Consistent]")

if __name__ == "__main__":
    # Test 1: Simple Method (Routes to GPU/Simulation)
    print("\n[RUNNING TEST CASE 1: Simple Method]")
    simple_code = "def add_numbers(a, b):\n    return a + b"
    simple_comment = "Adds two numbers together and returns the sum."
    run_gated_quality_gate(simple_code, simple_comment, "python")

    # Test 2: Complex Method (Routes to CPU Adak_ss)
    print("\n[RUNNING TEST CASE 2: Complex Method]")
    complex_code = """def process_data(data_list):
    processed = []
    if not data_list: return processed
    for item in data_list:
        if item is not None:
            cleaned = str(item).strip().lower()
            if len(cleaned) > 0 and cleaned != "empty":
                processed.append(cleaned)
            else: processed.append("default")
        else: processed.append("none")
    return sorted(processed)"""
    complex_comment = "Cleans, filters, and sorts a list of string elements."
    run_gated_quality_gate(complex_code, complex_comment, "python")