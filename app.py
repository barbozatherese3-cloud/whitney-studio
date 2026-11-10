import json
import os
import re
import sys
import warnings
from urllib.parse import quote_plus
import streamlit as st
from groq import Groq

warnings.filterwarnings("ignore")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

st.set_page_config(
    page_title="WHITNEY — Direction Artistique & Stylisme",
    page_icon="—",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Urbanist:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&display=swap');

    /* Fond vert continu intégral */
    .stApp {
        background-color: #8A641E !important;
        background-image: radial-gradient(circle at 10% 20%, #9B7122 0%, #7A581A 90%) !important;
        color: #EDEDD1 !important;
        font-family: 'Urbanist', sans-serif !important;
        letter-spacing: 0.2px;
    }

    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Navigation supérieure */
    .top-curation-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 0.5px solid rgba(237, 237, 209, 0.35);
        padding-bottom: 0.8rem;
        margin-bottom: 3rem;
        font-family: 'Urbanist', sans-serif;
        font-size: 0.76rem;
        font-weight: 500;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #EDEDD1;
        opacity: 0.85;
    }

    /* Titres monumentaux en Cormorant Garamond */
    .manifesto-line-1 {
        font-family: 'Cormorant Garamond', serif;
        font-size: clamp(4.8rem, 12vw, 11rem);
        font-weight: 300;
        line-height: 0.85;
        text-transform: uppercase;
        letter-spacing: -2px;
        color: #EDEDD1;
        display: block;
        text-align: left;
    }

    .manifesto-line-2 {
        font-family: 'Cormorant Garamond', serif;
        font-size: clamp(4.8rem, 12vw, 11rem);
        font-weight: 400;
        line-height: 0.85;
        text-transform: uppercase;
        letter-spacing: -2px;
        color: #7F2230;
        text-shadow: 2px 2px 0px rgba(237, 237, 209, 0.15);
        display: block;
        text-align: right;
        margin-top: 0.5rem;
        margin-bottom: 3.5rem;
    }

    .manifesto-statement-giant {
        font-family: 'Cormorant Garamond', serif;
        font-size: clamp(2.4rem, 5.5vw, 5.2rem);
        font-weight: 400;
        line-height: 1.08;
        text-transform: uppercase;
        color: #EDEDD1;
        letter-spacing: -0.5px;
        border-top: 0.5px solid rgba(237, 237, 209, 0.35);
        border-bottom: 0.5px solid rgba(237, 237, 209, 0.35);
        padding: 3rem 0;
        margin: 3rem 0 4rem 0;
    }

    .manifesto-statement-giant span.accent-red {
        color: #7F2230;
    }

    /* Grille en 3 colonnes de l'accueil */
    .triptych-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        border-top: 0.5px solid rgba(237, 237, 209, 0.35);
        border-bottom: 0.5px solid rgba(237, 237, 209, 0.35);
        margin-bottom: 4rem;
    }

    .triptych-col {
        padding: 2.2rem 2rem 2.8rem 2rem;
        border-right: 0.5px solid rgba(237, 237, 209, 0.35);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .triptych-col:last-child {
        border-right: none;
    }

    .triptych-num {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.4rem;
        color: #EDEDD1;
        opacity: 0.7;
        margin-bottom: 1.2rem;
    }

    .triptych-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.1rem;
        font-weight: 500;
        line-height: 1.05;
        text-transform: uppercase;
        letter-spacing: -0.5px;
        color: #EDEDD1;
        margin-bottom: 1.5rem;
    }

    .triptych-body {
        font-family: 'Urbanist', sans-serif;
        font-size: 0.9rem;
        font-weight: 300;
        line-height: 1.7;
        color: #EDEDD1;
        opacity: 0.9;
        margin-bottom: 2rem;
    }

    .triptych-link {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.15rem;
        font-style: italic;
        color: #EDEDD1;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        opacity: 0.85;
    }

    /* Succession verticale & LOOK monumental */
    .look-sheet-vertical {
        border-top: 1.5px solid rgba(237, 237, 209, 0.45);
        padding-top: 3.5rem;
        margin-bottom: 7rem;
    }

    .look-giant-display {
        margin-bottom: 3rem;
        border-bottom: 0.5px solid rgba(237, 237, 209, 0.35);
        padding-bottom: 2rem;
    }

    .look-massive-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: clamp(5.5rem, 14vw, 12.5rem);
        font-weight: 300;
        line-height: 0.82;
        letter-spacing: -3px;
        color: #EDEDD1;
        text-transform: uppercase;
        display: block;
    }

    .look-massive-sub {
        font-family: 'Cormorant Garamond', serif;
        font-size: clamp(2rem, 4.5vw, 4rem);
        font-weight: 400;
        font-style: italic;
        color: #7F2230;
        text-shadow: 2px 2px 0px rgba(237, 237, 209, 0.15);
        letter-spacing: -0.5px;
        margin-top: 0.5rem;
        text-align: right;
    }

    .vertical-section-block {
        border-bottom: 0.5px solid rgba(237, 237, 209, 0.25);
        padding-bottom: 2.5rem;
        margin-bottom: 2.5rem;
    }

    .section-label-fine {
        font-family: 'Urbanist', sans-serif;
        font-size: 0.74rem;
        font-weight: 600;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: #EDEDD1;
        opacity: 0.7;
        margin-bottom: 1.4rem;
    }

    .swatches-ribbon {
        display: flex;
        gap: 16px;
        flex-wrap: wrap;
    }

    .swatch-box-ribbon {
        border-radius: 2px;
        padding: 12px 18px;
        min-width: 160px;
        min-height: 64px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        border: 0.5px solid rgba(255, 255, 255, 0.18);
    }

    .swatch-name-txt {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.3rem;
        font-weight: 500;
        line-height: 1;
    }

    .swatch-hex-txt {
        font-family: 'Urbanist', sans-serif;
        font-size: 0.68rem;
        font-weight: 400;
        letter-spacing: 1px;
        opacity: 0.85;
    }

    .da-essay-body {
        font-family: 'Urbanist', sans-serif;
        font-size: 1.08rem;
        font-weight: 300;
        line-height: 1.85;
        color: #EDEDD1;
        max-width: 950px;
        text-align: justify;
    }

    .urbanist-item-line {
        font-family: 'Urbanist', sans-serif;
        font-size: 0.94rem;
        font-weight: 300;
        line-height: 1.7;
        margin-bottom: 10px;
        color: #EDEDD1;
        opacity: 0.95;
    }

    .shopping-grid-vinted {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
        gap: 20px;
        margin-top: 1rem;
    }

    .shopping-item-card {
        border: 0.5px solid rgba(237, 237, 209, 0.35);
        padding: 16px 20px;
        background: rgba(237, 237, 209, 0.05);
    }

    .item-title-vinted {
        font-family: 'Urbanist', sans-serif;
        font-size: 0.88rem;
        font-weight: 600;
        letter-spacing: 1px;
        color: #EDEDD1;
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    .item-neu-sub {
        font-family: 'Urbanist', sans-serif;
        font-size: 0.78rem;
        opacity: 0.75;
        margin-bottom: 8px;
    }

    .vinted-text-link {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.15rem;
        font-style: italic;
        color: #EDEDD1 !important;
        text-decoration: underline !important;
        text-underline-offset: 3px;
        display: inline-block;
        opacity: 0.85;
        transition: opacity 0.2s ease;
    }

    .vinted-text-link:hover {
        opacity: 1;
        color: #7F2230 !important;
    }

    .cartel-prompt-block {
        border: 0.5px solid rgba(237, 237, 209, 0.35);
        padding: 2rem 2.2rem;
        margin-top: 2rem;
        background: rgba(0, 0, 0, 0.1);
    }

    .cartel-title {
        font-family: 'Urbanist', sans-serif;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: #EDEDD1;
        opacity: 0.7;
        margin-bottom: 0.8rem;
    }

    .cartel-body-text {
        font-family: 'Urbanist', sans-serif;
        font-size: 0.92rem;
        font-style: italic;
        font-weight: 300;
        line-height: 1.7;
        color: #EDEDD1;
        opacity: 0.85;
    }

    /* Boutons en Cormorant Garamond */
    div.stButton > button {
        background-color: transparent !important;
        color: #EDEDD1 !important;
        border: 0.5px solid #EDEDD1 !important;
        font-family: 'Cormorant Garamond', serif !important;
        font-weight: 500 !important;
        font-size: 1.45rem !important;
        text-transform: none !important;
        letter-spacing: 0.5px !important;
        padding: 0.75rem 2.5rem !important;
        border-radius: 0px !important;
        width: 100% !important;
        transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
        cursor: pointer !important;
    }

    div.stButton > button:hover {
        background-color: #7F2230 !important;
        border-color: #7F2230 !important;
        color: #FFFFFF !important;
        transform: translateY(-2px) !important;
    }

    /* Inputs en fond Cream */
    .stTextArea textarea, .stNumberInput input {
        background-color: #EDEDD1 !important;
        color: #2D2621 !important;
        border: 0.5px solid rgba(237, 237, 209, 0.8) !important;
        border-radius: 0px !important;
        font-family: 'Urbanist', sans-serif !important;
        font-size: 0.95rem !important;
    }

    .stTextArea textarea:focus, .stNumberInput input:focus {
        border-color: #7F2230 !important;
    }

    .stNumberInput button {
        background-color: #EDEDD1 !important;
        color: #2D2621 !important;
        border: none !important;
    }

    label {
        color: #EDEDD1 !important;
        font-family: 'Urbanist', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.78rem !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
        opacity: 0.85;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

CLE_GROQ = os.environ.get("GROQ_API_KEY")
if not CLE_GROQ:
    st.error("GROQ_API_KEY absente du fichier .env")
    st.stop()

client_groq = Groq(api_key=CLE_GROQ)
STATUTS_VINTED = [1, 6, 2]


def lien_vinted(mots_cles: str) -> str:
    statuts = "&".join(f"status_ids[]={s}" for s in STATUTS_VINTED)
    return f"https://www.vinted.fr/vetements?search_text={quote_plus(mots_cles)}&{statuts}"


def detecter_modele():
    try:
        tous = [m.id for m in client_groq.models.list().data]
        exclus = ["guard", "whisper", "vision", "embed", "safeguard", "tts", "orpheus"]
        valides = [m for m in tous if not any(x in m.lower() for x in exclus)]
        ordre = [
            "openai/gpt-oss-20b",
            "llama-3.3-70b-versatile",
            "llama3-70b-8192",
            "llama3-8b-8192",
            "gemma2-9b-it",
        ]
        for p in ordre:
            if p in valides:
                return p
        if valides:
            return valides[0]
    except Exception:
        pass
    return "openai/gpt-oss-20b"


PROMPT_SILHOUETTE_INDIVIDUELLE = """
Tu es WHITNEY, directrice artistique et styliste personnelle de renom, réputée pour sa rigueur chirurgicale, son œil Quiet Luxury et son expertise du layering Pinterest haut de gamme.
Tu ne rédiges jamais de conseils vagues ou génériques. Tu déconstruis la silhouette avec une précision d'orfèvre.
Tu réponds STRICTEMENT sous la forme d'un objet JSON valide, sans aucune phrase de bavardage.

RÈGLES D'OR DE WHITNEY :
1. ANALYSE DA TECHNIQUE & INCARNÉE ("intention_da") :
   - Rédige un véritable paragraphe éditorial (5 à 7 phrases) qui justifie l'architecture globale, le dialogue des textures (ex: rusticité d'une maille tressée contre netteté d'un pantalon tailleur peigné) et l'équilibre des volumes par rapport à la météo et au contexte exigeant.
2. COMPOSITION HEAD-TO-TOE EXHAUSTIVE ("composition_look") :
   - Fournis 5 à 6 puces ultra-précises décrivant chaque strate de la silhouette :
     * Première couche / base (matière, col, couleur)
     * Layering intermédiaire (pièce préexistante ou cardigan)
     * Veste ou manteau de protection (coupe, longueur, boutonnage)
     * Bas obligatoire (taille, coupe, tombé exact sur le soulier)
     * Souliers obligatoires (matière, finition du cuir, modèle exact)
     * Accessoires précis (cuir, métal doré brossé ou argenté, placement du sac)
3. CONSIGNES DE PORTÉ MILLIMÉTRÉES ("consignes_porte") :
   - 4 instructions gestuelles concrètes : de combien de centimètres faire dépasser le col/poignet, type de rentré (french tuck asymétrique, ceinturé), tombé de l'ourlet sur le cou-de-pied, attitude manteau ouvert ou croisé.
4. PROMPT CROQUIS HAUTE DÉFINITION ("prompt_croquis") :
   - Rédige un prompt d'image professionnel et immersif en anglais de 100 à 130 mots pour Midjourney/Flux : pose décontractée chic en pied, fond atelier papier texturé, éclairage éditorial doux, détails exacts de tissage, superposition visible strate par strate, souliers et finitions.
5. SOURCING VINTED RÉALISTE ("pieces_shopping") :
   - Mots-clés de recherche Vinted ciblés pour tomber directement sur les bonnes pièces, avec équivalent neuf chez Arket, Cos, Uniqlo ou Mango.

FORMAT JSON STRICT ATTENDU :
{
  "nom_look": "Nom évocateur du look",
  "intention_da": "Paragraphe de vision DA complet et chirurgical...",
  "palette": [
    {"nom": "Teinte 1", "hex": "#HEX", "text_color": "#FFFFFF"},
    {"nom": "Teinte 2", "hex": "#HEX", "text_color": "#2D2621"},
    {"nom": "Teinte 3", "hex": "#HEX", "text_color": "#FFFFFF"}
  ],
  "composition_look": [
    "Première couche : ...",
    "Layering : ...",
    "Extérieur : ...",
    "Bas : ...",
    "Souliers : ...",
    "Accessoires : ..."
  ],
  "consignes_porte": [
    "Consigne 1...",
    "Consigne 2...",
    "Consigne 3...",
    "Consigne 4..."
  ],
  "pieces_shopping": [
    {
      "nom": "Nom précis de la pièce",
      "mots_cles_vinted": "mots clés de recherche précis",
      "prix_vinted_estime": 12,
      "alternative_neuve": "Marque + modèle"
    }
  ],
  "prompt_croquis": "Haute couture fashion illustration sketch, runway watercolor on textured cream paper background. Full length female model..."
}
"""


def extraire_json_clean(texte: str):
    if not texte:
        return None
    texte = texte.strip()
    texte = re.sub(r"^```[a-zA-Z]*", "", texte)
    texte = re.sub(r"```$", "", texte)
    texte = texte.strip()
    try:
        return json.loads(texte)
    except Exception:
        pass
    match = re.search(r"(\{.*\})", texte, re.DOTALL)
    if match:
        blob = match.group(1).strip()
        try:
            return json.loads(blob)
        except Exception:
            for s in ["}", "]}", "]}}", '"}]}}']:
                try:
                    return json.loads(blob + s)
                except Exception:
                    continue
    return None


def generer_silhouettes(demande: str, budget: int):
    modele = detecter_modele()
    try:
        rep1 = client_groq.chat.completions.create(
            model=modele,
            messages=[
                {"role": "system", "content": PROMPT_SILHOUETTE_INDIVIDUELLE},
                {"role": "user", "content": f"Brief cliente : {demande}\nBudget total d'achat : {budget} €.\nGénère la silhouette LOOK 1 (orientation structurée, tailoring)."},
            ],
            temperature=0.6,
            max_tokens=2500,
        )
        l1 = extraire_json_clean(rep1.choices[0].message.content)

        rep2 = client_groq.chat.completions.create(
            model=modele,
            messages=[
                {"role": "system", "content": PROMPT_SILHOUETTE_INDIVIDUELLE},
                {"role": "user", "content": f"Brief cliente : {demande}\nBudget total d'achat : {budget} €.\nGénère la silhouette LOOK 2 (orientation fluide, layering souple et contrasté, différente de la première)."},
            ],
            temperature=0.65,
            max_tokens=2500,
        )
        l2 = extraire_json_clean(rep2.choices[0].message.content)

        propositions = []
        if l1:
            propositions.append(l1)
        if l2:
            propositions.append(l2)

        if propositions:
            return {"propositions": propositions}, None
        return None, "Structure reçue illisible. Relancez l'élaboration."
    except Exception as e:
        return None, str(e)


# ----------------- SESSION STATE -----------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "resultats" not in st.session_state:
    st.session_state.resultats = None
if "budget_choisi" not in st.session_state:
    st.session_state.budget_choisi = 60


# ================= PAGE 1 : ACCUEIL =================
if st.session_state.page == "home":
    st.markdown(
        """
        <div class="top-curation-nav">
            <span>WHITNEY STUDIO / DIRECTION ARTISTIQUE</span>
            <span>COLLECTION PERMANENTE — 2026</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <span class="manifesto-line-1">WHITNEY</span>
        <span class="manifesto-line-2">STUDIO.</span>
        <div class="manifesto-statement-giant">
            DIRECTION ARTISTIQUE & STYLISME PERSONNEL.<br>
            <span class="accent-red">ANATOMIE DU VESTIAIRE,</span><br>
            SUPERPOSITIONS RECHERCHÉES<br>
            & SOURCING SECONDE MAIN POINTU.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="triptych-grid">
            <div class="triptych-col">
                <div>
                    <div class="triptych-num">01/</div>
                    <div class="triptych-title">Architecture<br>du vestiaire</div>
                    <div class="triptych-body">
                        Déconstruction méthodique des proportions, tombé des matières nobles et superpositions précises pensées de la tête aux pieds.
                    </div>
                </div>
                <div class="triptych-link">→ Head-to-toe Layering</div>
            </div>
            <div class="triptych-col">
                <div>
                    <div class="triptych-num">02/</div>
                    <div class="triptych-title">Direction<br>chromatique</div>
                    <div class="triptych-body">
                        Composition d'harmonies feutrées limitées à trois nuances signatures adaptées à votre carnation et vos pièces déjà possédées.
                    </div>
                </div>
                <div class="triptych-link">→ Curated Harmonies</div>
            </div>
            <div class="triptych-col">
                <div>
                    <div class="triptych-num">03/</div>
                    <div class="triptych-title">Sourcing<br>seconde main</div>
                    <div class="triptych-body">
                        Curation chirurgicale sur Vinted ciblant exclusivement le très bon état et l'état neuf dans le respect strict de votre budget.
                    </div>
                </div>
                <div class="triptych-link">→ Archive Finder</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_btn_wrap, _ = st.columns([1, 1])
    with col_btn_wrap:
        if st.button("Entrer dans le studio de Whitney —"):
            st.session_state.page = "form"
            st.rerun()


# ================= PAGE 2 : BRIEFING =================
elif st.session_state.page == "form":
    st.markdown(
        """
        <div class="top-curation-nav">
            <span>WHITNEY STUDIO / CONSULTATION EN LIGNE</span>
            <span>ÉTAPE 02 — FORMULATION DU BRIEF</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div style='font-family: Cormorant Garamond, serif; font-size: 3.4rem; font-weight: 400; color: #EDEDD1; margin-bottom: 0.8rem; line-height: 1.05;'>"
        "Sur quel vestiaire travaillons-nous aujourd'hui ?"
        "</div>",
        unsafe_allow_html=True,
    )

    demande_val = st.text_area(
        label="VOTRE BRIEF (OCCASION, MÉTÉO, SILHOUETTE, PIÈCES DÉJÀ EN VOTRE POSSESSION) :",
        value="Bureau au quotidien, environnement exigeant (clients, réunions), élégant mais décontracté. Météo : 6 °C, pluie fine, Paris. Pièce déjà possédée : pull rose à maille tressée. Taille 36, 1m68. Layering avec chemise ou col roulé fin qui dépasse sous pull ou blazer, grand manteau par-dessus.",
        height=140,
    )

    budget_val = st.number_input(
        "BUDGET D'ACHAT MAXIMUM ALLOUÉ (€) :", min_value=15, max_value=400, value=st.session_state.budget_choisi, step=5
    )

    col1, col2 = st.columns([1, 2])
    with col1:
        if st.button("← Retour au studio"):
            st.session_state.page = "home"
            st.rerun()
    with col2:
        if st.button("Élaborer les 2 silhouettes —"):
            if not demande_val.strip():
                st.warning("Veuillez préciser votre demande.")
            else:
                with st.spinner("Whitney étudie le brief et compose vos deux silhouettes..."):
                    res, err = generer_silhouettes(demande_val, budget_val)
                if not res or not res.get("propositions"):
                    st.error(f"Erreur : {err}")
                else:
                    st.session_state.resultats = res.get("propositions")
                    st.session_state.budget_choisi = budget_val
                    st.session_state.page = "results"
                    st.rerun()


# ================= PAGE 3 : RÉSULTATS (LOOK IMPOSANT & VERTICALITÉ) =================
elif st.session_state.page == "results":
    st.markdown(
        """
        <div class="top-curation-nav">
            <span>WHITNEY STUDIO / ARCHIVE D'EXPOSITION</span>
            <span>2 PROPOSITIONS ÉDITORIALES</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_btn, _ = st.columns([1, 4])
    with col_btn:
        if st.button("← Nouveau brief"):
            st.session_state.page = "form"
            st.rerun()

    st.write("")

    propositions = st.session_state.resultats or []
    for idx, look in enumerate(propositions, start=1):
        st.markdown(f'<div class="look-sheet-vertical">', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="look-giant-display">
                <span class="look-massive-title">LOOK 0{idx}</span>
                <div class="look-massive-sub">— {look.get('nom_look', '').upper()}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="vertical-section-block">', unsafe_allow_html=True)
        st.markdown('<div class="section-label-fine">01 / Palette chromatique</div>', unsafe_allow_html=True)
        swatches_html = '<div class="swatches-ribbon">'
        for c in look.get("palette", []):
            nom_c = c.get("nom", "Teinte") if isinstance(c, dict) else str(c)
            hex_c = c.get("hex", "#2B2D2F") if isinstance(c, dict) else "#2B2D2F"
            txt_c = c.get("text_color", "#FFFFFF") if isinstance(c, dict) else "#FFFFFF"
            swatches_html += (
                f'<div class="swatch-box-ribbon" style="background-color: {hex_c}; color: {txt_c};">'
                f'<span class="swatch-name-txt">{nom_c}</span>'
                f'<span class="swatch-hex-txt">{hex_c.lower()}</span>'
                f'</div>'
            )
        swatches_html += '</div>'
        st.markdown(swatches_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="vertical-section-block">', unsafe_allow_html=True)
        st.markdown('<div class="section-label-fine">02 / Le Regard de Whitney</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="da-essay-body">{look.get("intention_da", "")}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="vertical-section-block">', unsafe_allow_html=True)
        col_comp, col_porte = st.columns(2, gap="large")

        with col_comp:
            st.markdown('<div class="section-label-fine">03 / Ce qui compose le look</div>', unsafe_allow_html=True)
            for piece in look.get("composition_look", []):
                st.markdown(f'<div class="urbanist-item-line">— {piece}</div>', unsafe_allow_html=True)

        with col_porte:
            st.markdown('<div class="section-label-fine">04 / Comment le porter & gestuelle</div>', unsafe_allow_html=True)
            for tip in look.get("consignes_porte", []):
                st.markdown(f'<div class="urbanist-item-line" style="font-style: italic; opacity: 0.9;">{tip}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="vertical-section-block">', unsafe_allow_html=True)
        st.markdown('<div class="section-label-fine">05 / Curation Shopping Seconde Main</div>', unsafe_allow_html=True)

        shopping_cards_html = '<div class="shopping-grid-vinted">'
        total_look = 0.0
        pieces_list = look.get("pieces_shopping") or look.get("pieces", [])
        for p in pieces_list:
            prix = float(p.get("prix_vinted_estime") or 0)
            total_look += prix
            url_v = lien_vinted(p.get("mots_cles_vinted", p.get("nom", "")))
            shopping_cards_html += (
                f'<div class="shopping-item-card">'
                f'<div class="item-title-vinted">{p.get("nom", "").upper()} (~{prix:.0f} €)</div>'
                f'<div class="item-neu-sub">Neuf : {p.get("alternative_neuve", "-")}</div>'
                f'<a href="{url_v}" target="_blank" class="vinted-text-link">Chiner sur Vinted ↗</a>'
                f'</div>'
            )
        shopping_cards_html += '</div>'
        st.markdown(shopping_cards_html, unsafe_allow_html=True)

        verdict = "Dans le budget alloué" if total_look <= st.session_state.budget_choisi else "Au-dessus du budget"
        st.markdown(
            f'<div style="font-family: \'Urbanist\', sans-serif; font-size: 0.8rem; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; margin-top: 1.4rem; opacity: 0.85;">'
            f'Total estimé : ~{total_look:.0f} € / {st.session_state.budget_choisi} € ({verdict})</div>',
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

        prompt_texte = look.get("prompt_croquis", "")
        st.markdown(
            f"""
            <div class="cartel-prompt-block">
                <div class="cartel-title">06 / Cartel — Prompt d'illustration de mode haute définition</div>
                <div class="cartel-body-text">{prompt_texte}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('</div>', unsafe_allow_html=True)
        