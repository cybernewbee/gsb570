import streamlit as st
from src.pokeapi import get_pokemon_details
import pandas as pd
import matplotlib.pyplot as plt
from utils import centered_image_html
from utils import image_to_base64
st.set_page_config(
    page_title="Compare Pokémon",  # 👈 THIS name defines the URL
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("<a name='top'></a>", unsafe_allow_html=True)
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    header, h1 { display: none; }
    </style>
""", unsafe_allow_html=True)

# Render pixel-art title, centered
st.markdown(centered_image_html("assets/comparison_title.png", width=700), unsafe_allow_html=True)

home_icon_b64 = image_to_base64("assets/back_to_home.png")

st.markdown(f"""
    <style>
    .home-icon {{
        position: fixed;
        top: 80px;
        left: 50px;
        z-index: 9999;
    }}

    .home-icon img {{
        width: 150px;  /* adjust size here */
        height: auto;
        cursor: pointer;
    }}
    </style>

    <a href="/" target="_self" class="home-icon">
        <img src="data:image/png;base64,{home_icon_b64}" alt="Home">
    </a>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    pokemon_1 = st.text_input("Enter first Pokémon name:", key="poke1")
with col2:
    pokemon_2 = st.text_input("Enter second Pokémon name:", key="poke2")

if pokemon_1 and pokemon_2:
    with st.spinner("Fetching data..."):
        p1 = get_pokemon_details(pokemon_1)
        p2 = get_pokemon_details(pokemon_2)

    if "error" in p1:
        col1.error(p1["error"])
    if "error" in p2:
        col2.error(p2["error"])

    if "error" not in p1 and "error" not in p2:
        # === Display sprites ===
        col1.image(p1["sprites"].get("official_artwork"), caption=p1["name"])
        col2.image(p2["sprites"].get("official_artwork"), caption=p2["name"])

        # === Type Chart ===
        col1.subheader("Type")
        col1.write(", ".join(p1.get("types", [])))

        col2.subheader("Type")
        col2.write(", ".join(p2.get("types", [])))

        # === Abilities ===
        col1.subheader("Abilities")
        for a in p1.get("abilities", []):
            col1.write(f"• {a}")

        col2.subheader("Abilities")
        for a in p2.get("abilities", []):
            col2.write(f"• {a}")

        # === Stats ===
        col1.subheader("Base Stats")
        for stat, val in p1.get("stats", {}).items():
            col1.write(f"{stat.title()}: {val}")

        col2.subheader("Base Stats")
        for stat, val in p2.get("stats", {}).items():
            col2.write(f"{stat.title()}: {val}")

        # === Evolution Chain ===
        col1.subheader("Evolution Chain")
        for chain in p1.get("evolution_chain", []):
            col1.write(chain)

        col2.subheader("Evolution Chain")
        for chain in p2.get("evolution_chain", []):
            col2.write(chain)

        # === Games Appeared In ===
        col1.subheader("Games")
        col1.write(", ".join(p1.get("associated_games", [])))

        col2.subheader("Games")
        col2.write(", ".join(p2.get("associated_games", [])))

        # Cry
        col1.subheader("Cry")
        col1.audio(p1.get("cry_url"))

        col2.subheader("Cry")
        col2.audio(p2.get("cry_url"))



        import numpy as np

        def plot_radar_chart(p1_data, p2_data, labels):
            angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
            angles += angles[:1]  # Complete the loop

            p1_values = [p1_data.get(stat, 0) for stat in labels]
            p2_values = [p2_data.get(stat, 0) for stat in labels]

            p1_values += p1_values[:1]
            p2_values += p2_values[:1]

    
            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            ax.plot(angles, p1_values, label=p1["name"], color="blue")
            ax.fill(angles, p1_values, alpha=0.25, color="blue")

            ax.plot(angles, p2_values, label=p2["name"], color="green")
            ax.fill(angles, p2_values, alpha=0.25, color="green")

            ax.set_title("Radar Chart - Base Stats")
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels([s.title() for s in labels])
            ax.set_yticklabels([])
            ax.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1))
            st.pyplot(fig)

        st.subheader("🕸️ Radar Chart Comparison")
        stat_order = ["hp", "attack", "defense", "special-attack", "special-defense", "speed"]
        plot_radar_chart(p1.get("stats", {}), p2.get("stats", {}), stat_order)

# At the bottom of your comparison or walkthrough page:

# Inject floating buttons via HTML/CSS
st.markdown("""
    <style>
    .scroll-top-btn {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background-color: white;
        color: black;
        padding: 10px 20px;
        border-radius: 10px;
        font-weight: bold;
        border: 1px solid #ccc;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        cursor: pointer;
        z-index: 9999;
    }
    </style>

    <a href="#top" class="scroll-top-btn">⬆️ Top</a>
""", unsafe_allow_html=True)

# Add the scroll anchor at the top of your page
st.markdown("<a name='top'></a>", unsafe_allow_html=True)






