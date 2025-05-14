import streamlit as st
from src.answer_pipeline import answer_query
from utils import centered_image_html
from utils import image_to_base64
st.set_page_config(
    page_title="Walkthrough Assistant",  # 👈 THIS name defines the URL
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("<a name='top'></a>", unsafe_allow_html=True)
# Hide header/title spacing
#Optional: Remove default Streamlit title/header spacing
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    header, h1 { display: none; }
    </style>
""", unsafe_allow_html=True)

# Render pixel-art title, centered
st.markdown(centered_image_html("assets/walkthrough_title.png", width=700), unsafe_allow_html=True)

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
        width: 150px;
        height: auto;
        cursor: pointer;
    }}
    </style>

    <a href="/" target="_self" class="home-icon">
        <img src="data:image/png;base64,{home_icon_b64}" alt="Home">
    </a>
""", unsafe_allow_html=True)


user_input = st.text_input("Ask a question (e.g., 'Where do I catch Ralts in Emerald?')")

if user_input:
    with st.spinner("Thinking..."):
        result = answer_query(user_input)

    # Handle error
    if "error" in result:
        st.error(result["error"])
    else:
        query_fields = result.get("query_fields", {})
        walkthroughs = result.get("walkthrough_results", [])
        pokemon_info = result.get("pokemon_info", {})

        # Query summary
        st.subheader("🧠 Extracted Query Fields")
        st.json(query_fields)

        # Walkthrough links
        st.subheader("📚 Walkthroughs")
        if walkthroughs:
            for item in walkthroughs:
                st.markdown(f"**[{item['title']}]({item['link']})**\n\n{item['snippet']}")
        else:
            st.info("No walkthroughs found.")
        # 📖 Walkthrough Guide (Generated)
        if result.get("walkthrough_article"):
            st.subheader("📝 Walkthrough Guide (Generated)")
            st.markdown(result["walkthrough_article"])


        # Pokémon info
        if "error" in pokemon_info:
            st.warning(pokemon_info["error"])
        else:
            st.subheader(f"🔍 Pokémon Info: {pokemon_info['name']}")
            
            cols = st.columns(4)
            sprites = pokemon_info.get("sprites", {})
            for i, label in enumerate(["front_default", "back_default", "front_shiny", "back_shiny"]):
                if sprites.get(label):
                    cols[i].image(sprites[label], caption=label.replace("_", " ").title())

            if sprites.get("official_artwork"):
                st.image(sprites["official_artwork"], caption="Official Artwork", use_container_width=True)
            st.markdown("**Type(s):** " + ", ".join(pokemon_info.get("types", [])))
            st.subheader("📈 Base Stats")
            cols = st.columns(3)
            for i, (stat, value) in enumerate(pokemon_info.get("stats", {}).items()):
                cols[i % 3].metric(label=stat.title(), value=value)
            st.markdown("**Abilities:** " + ", ".join(pokemon_info.get("abilities", [])))
            st.markdown("**Location Encounters:** " + ", ".join(pokemon_info.get("location_encounters", [])))
            st.markdown("**Games Appeared In:** " + ", ".join(pokemon_info.get("associated_games", [])))
            st.markdown("**Evolution Chain:**")
            for path in pokemon_info.get("evolution_chain", []):
                st.write(path)
            import streamlit.components.v1 as components

            if "cry_url" in pokemon_info:
                st.subheader("🔊 Cry")
                components.html(
                    f"""
                    <audio controls style="height:25px;">
                    <source src="{pokemon_info['cry_url']}" type="audio/ogg">
                    Your browser does not support the audio element.
                    </audio>
                    """,
                    height=40,
                    )
# At the bottom of your comparison or walkthrough page:

# Scroll-to-top floating button
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

