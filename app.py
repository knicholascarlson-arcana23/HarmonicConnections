import streamlit as st
import pandas as pd
from fractions import Fraction
import math
import colorsys
from pyvis.network import Network
import streamlit.components.v1 as components

# --- 1. ACOUSTIC MATH LOGIC (Unchanged) ---
def reduce_to_octave(numerator, denominator):
    """Reduces fraction to a ratio between 1.0 and 2.0."""
    frac = Fraction(numerator, denominator)
    while frac >= 2:
        frac = Fraction(frac.numerator, frac.denominator * 2)
    while frac < 1:
        frac = Fraction(frac.numerator * 2, frac.denominator)
    return frac

def get_prime_signature(num, den):
    """Extracts the odd prime 'DNA' of a ratio to group it by color."""
    def extract_odd_primes(n):
        factors = set()
        while n % 2 == 0:
            n //= 2  
        d = 3
        while d * d <= n:
            while n % d == 0:
                factors.add(d)
                n //= d
            d += 2
        if n > 1:
            factors.add(n)
        return tuple(sorted(factors))
    return (extract_odd_primes(num), extract_odd_primes(den))

def parse_iterations(raw_input):
    """Parses input like '3:2, 5:1' to generate all prime iterations."""
    factors = {}
    for item in raw_input.split(","):
        item = item.strip()
        if ":" in item:
            prime, count = item.split(":")
            factors[int(prime)] = int(count)
        else:
            factors[int(item)] = 1 
            
    identities = [1]
    for p, count in factors.items():
        new_ids = []
        for i in range(count + 1):
            for val in identities:
                new_ids.append(val * (p**i))
        identities = new_ids
    return sorted(list(set(identities)))

def calculate_diamond(identities):
    """Generates the matrix of Otonality and Utonality."""
    diamond_data = []
    unique_ratios = set()
    
    for otonality in identities:
        for utonality in identities:
            ratio = reduce_to_octave(otonality, utonality)
            cents = 1200 * math.log2(float(ratio))
            
            if ratio not in unique_ratios:
                signature = get_prime_signature(ratio.numerator, ratio.denominator)
                diamond_data.append({
                    "Otonality": otonality,
                    "Utonality": utonality,
                    "Ratio": f"{ratio.numerator}/{ratio.denominator}",
                    "Cents": round(cents, 2),
                    "signature": signature
                })
                unique_ratios.add(ratio)
                
    return sorted(diamond_data, key=lambda x: x["Cents"])

def generate_network_html(diamond_data):
    """Generates the pyvis network and saves it to a temporary HTML file."""
    net = Network(height="600px", width="100%", bgcolor="#1a1a1a", font_color="white")
    
    unique_sigs = list(set([d["signature"] for d in diamond_data if d["Ratio"] != "1/1"]))
    color_palette = {}
    
    for i, sig in enumerate(unique_sigs):
        hue = i / max(1, len(unique_sigs))
        rgb = colorsys.hls_to_rgb(hue, 0.65, 0.85)
        hex_color = '#%02x%02x%02x' % (int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
        color_palette[sig] = hex_color

    net.add_node("1/1", label="1/1\n(0c)", title="Root Fundamental", color="#FFFFFF", size=35)
    
    for data in diamond_data:
        ratio = data['Ratio']
        if ratio != "1/1":
            sig = data['signature']
            label = f"{ratio}\n({data['Cents']}c)"
            
            num_primes = ",".join(map(str, sig[0])) if sig[0] else "None"
            den_primes = ",".join(map(str, sig[1])) if sig[1] else "None"
            hover_text = f"Otonal Primes: {num_primes}\nUtonal Primes: {den_primes}"
            
            node_color = color_palette[sig]
            
            net.add_node(ratio, label=label, title=hover_text, color=node_color, size=25)
            net.add_edge("1/1", ratio, color="#555555")

    net.repulsion(node_distance=180, spring_length=220)
    
    # Save to a file that Streamlit can read
    net.write_html("lattice.html")

# --- 2. STREAMLIT WEB APP INTERFACE ---

# Page config
st.set_page_config(page_title="Acoustic Lattice Builder", layout="wide")

st.title("Color-Coded Acoustic Lattice")
st.markdown("### The Geometry of Just Intonation")
st.write("Format: `[Prime]:[Steps]`. Example: `3:2, 5:1` (goes 2 steps of 3, 1 step of 5)")

# Input Area
col1, col2 = st.columns([3, 1])
with col1:
    raw_input = st.text_input("Prime Iterations:", value="3:2, 5:1, 7:1")
with col2:
    st.write("") # Spacing
    st.write("")
    generate_pressed = st.button("Generate Lattice", type="primary", use_container_width=True)

# App Execution
if generate_pressed or raw_input:
    try:
        identities = parse_iterations(raw_input)
    except ValueError:
        st.error("Input Error: Please use the format like 3:2, 5:1")
        st.stop()

    # Calculate Math
    diamond_data = calculate_diamond(identities)
    
    # Create Layout (Left side table, Right side Interactive Graph)
    table_col, graph_col = st.columns([1, 2])
    
    with table_col:
        st.subheader("Data Table")
        # Drop the internal signature tuple before showing to the user
        display_df = pd.DataFrame(diamond_data).drop(columns=['signature'])
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
    with graph_col:
        st.subheader("Interactive Geometry")
        generate_network_html(diamond_data)
        
        # Read the generated HTML and embed it into the Streamlit app
        HtmlFile = open("lattice.html", 'r', encoding='utf-8')
        source_code = HtmlFile.read() 
        components.html(source_code, height=620)