
import json
import re
import html
import requests
import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Reviewly | AI Review Intelligence",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen2.5:3b"

SAMPLE_REVIEWS = """Food was amazing and biryani quantity was good.
Delivery was very late and food became cold.
Paneer starter was tasty but too spicy.
Packaging was neat and no leakage.
Prices are high compared to quantity.
Customer support was not helpful.
Ambience is good for family.
Service was slow during weekend.
Desserts were excellent.
Overall food taste is good but delivery needs improvement."""

THINKING_OPTIONS = {
    "Quick": {
        "num_predict": 650,
        "description": "Fast and concise analysis",
    },
    "Balanced": {
        "num_predict": 1200,
        "description": "A balanced business report",
    },
    "Deep": {
        "num_predict": 2200,
        "description": "More detailed business insights",
    },
}

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "reviews" not in st.session_state:
    st.session_state.reviews = ""

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "thinking_strength" not in st.session_state:
    st.session_state.thinking_strength = "Balanced"

if "output_language" not in st.session_state:
    st.session_state.output_language = "English"


# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------
st.markdown(
    """
<style>
:root {
    color-scheme: dark;
}

.stApp {
    background:
        radial-gradient(
            ellipse at 50% -15%,
            rgba(124, 92, 255, 0.14),
            transparent 45%
        ),
        #101116;
    color: #f2f2f5;
}

[data-testid="stSidebar"],
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
}

.block-container {
    max-width: 1040px;
    padding-top: 1.2rem;
    padding-bottom: 5rem;
}

#MainMenu, footer {
    visibility: hidden;
}

.brand {
    display: flex;
    align-items: center;
    gap: 11px;
    font-weight: 800;
    font-size: 21px;
    letter-spacing: -0.7px;
    color: #f9f9fc;
}

.brand-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 12px;
    background: linear-gradient(135deg, #8b5cf6, #6366f1);
    color: white;
    font-size: 20px;
    box-shadow: 0 5px 22px rgba(139,92,246,.25);
}

.brand-sub {
    color: #a1a1b3;
    font-size: 12px;
    font-weight: 450;
    letter-spacing: 0;
    margin-top: -2px;
}

.status {
    text-align: right;
    color: #aaaab7;
    font-size: 12px;
    padding-top: 10px;
}

.status-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    background: #34d399;
    border-radius: 50%;
    margin-right: 6px;
    box-shadow: 0 0 10px rgba(52,211,153,.5);
}

.hero {
    text-align: center;
    padding: 55px 12px 31px;
}

.hero-orb {
    width: 65px;
    height: 65px;
    margin: 0 auto 20px;
    background: linear-gradient(145deg, #a78bfa, #6366f1);
    border-radius: 22px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 31px;
    color: #fff;
    box-shadow:
        0 12px 40px rgba(124,92,255,.24),
        inset 0 1px 2px rgba(255,255,255,.4);
}

.hero-title {
    font-size: clamp(29px, 5vw, 44px);
    font-weight: 800;
    letter-spacing: -1.8px;
    line-height: 1.2;
    color: #fafafa;
}

.hero-title span {
    background: linear-gradient(100deg, #c4b5fd, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-description {
    max-width: 570px;
    color: #a8a8b7;
    font-size: 15px;
    line-height: 1.8;
    margin: 15px auto 0;
}

.feature-line {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 9px;
    margin-top: 23px;
}

.feature-pill {
    padding: 6px 12px;
    font-size: 12px;
    color: #c4c1d8;
    border: 1px solid #34333f;
    border-radius: 999px;
    background: rgba(255,255,255,.025);
}

.section-label {
    font-size: 14px;
    color: #d9d8e3;
    font-weight: 700;
    margin-bottom: 9px;
}

.stTextArea textarea {
    background: #1c1c25 !important;
    border: 1px solid #343442 !important;
    border-radius: 17px !important;
    color: #f5f5f7 !important;
    padding: 18px !important;
    line-height: 1.65 !important;
    font-size: 14px !important;
    min-height: 210px !important;
    resize: vertical !important;
}

.stTextArea textarea:focus {
    border-color: #8b5cf6 !important;
    box-shadow: 0 0 0 1px rgba(139,92,246,.25) !important;
}

.stTextArea textarea::placeholder {
    color: #77778a !important;
}

div[data-testid="stSelectbox"] > div > div {
    background: #1c1c25 !important;
    border-color: #393947 !important;
    border-radius: 12px !important;
}

div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(125deg, #8b5cf6, #6d5dfc);
    border: none;
    border-radius: 12px;
    color: white;
    font-weight: 700;
    min-height: 43px;
    box-shadow: 0 5px 18px rgba(124,92,255,.18);
}

div[data-testid="stButton"] button[kind="primary"]:hover {
    background: #9d76ff;
    color: white;
}

div[data-testid="stButton"] button[kind="secondary"] {
    background: #24242e;
    color: #dedee8;
    border: 1px solid #393947;
    border-radius: 12px;
    min-height: 43px;
}

div[data-testid="stButton"] button {
    transition: all .2s ease;
}

div[data-testid="stButton"] button:hover {
    transform: translateY(-1px);
}

.input-hint {
    color: #858598;
    font-size: 12px;
    padding-top: 3px;
}

.result-heading {
    font-size: 25px;
    font-weight: 800;
    letter-spacing: -.8px;
    margin-top: 30px;
    margin-bottom: 8px;
}

.result-subheading {
    font-size: 13px;
    color: #9696a8;
    margin-bottom: 18px;
}

.metric-card {
    background: #1c1d26;
    border: 1px solid #333340;
    padding: 20px;
    border-radius: 18px;
    height: 100%;
    min-height: 125px;
}

.metric-label {
    color: #a6a5b5;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 11px;
}

.metric-value {
    color: #fafafa;
    font-size: 25px;
    font-weight: 800;
    overflow-wrap: anywhere;
}

.metric-description {
    color: #9090a1;
    font-size: 12px;
    margin-top: 9px;
}

.content-card {
    background: #1c1d26;
    border: 1px solid #333340;
    padding: 21px;
    border-radius: 18px;
    margin-top: 15px;
    color: #d5d5e0;
    line-height: 1.7;
    overflow-wrap: anywhere;
}

.content-title {
    color: #f5f5f7;
    font-size: 16px;
    font-weight: 750;
    margin-bottom: 13px;
}

.insight-item {
    padding: 11px 13px;
    background: #252530;
    border: 1px solid #373743;
    border-radius: 11px;
    margin-bottom: 9px;
    font-size: 13px;
    line-height: 1.6;
    color: #e0dfeb;
}

.insight-item.positive {
    border-left: 3px solid #34d399;
}

.insight-item.negative {
    border-left: 3px solid #fb7185;
}

.insight-item.warning {
    border-left: 3px solid #fbbf24;
}

.insight-item.suggestion {
    border-left: 3px solid #a78bfa;
}

.tag {
    display: inline-block;
    background: #302b48;
    color: #c4b5fd;
    border: 1px solid #4d416e;
    border-radius: 999px;
    padding: 4px 11px;
    margin: 3px 5px 3px 0;
    font-size: 12px;
}

.rating-track {
    height: 8px;
    background: #343440;
    border-radius: 999px;
    overflow: hidden;
    margin-top: 12px;
}

.rating-fill {
    height: 100%;
    background: linear-gradient(90deg, #8b5cf6, #c4b5fd);
    border-radius: 999px;
}

.footer-note {
    text-align: center;
    color: #77778b;
    font-size: 12px;
    margin-top: 45px;
    padding-bottom: 10px;
}

@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: .65rem;
    }

    .hero {
        padding: 33px 5px 24px;
    }

    .hero-title {
        letter-spacing: -1px;
    }

    .hero-description {
        font-size: 13px;
    }

    .hero-orb {
        width: 54px;
        height: 54px;
    }

    .metric-card {
        padding: 14px;
        min-height: 105px;
    }

    .metric-value {
        font-size: 19px;
    }

    .content-card {
        padding: 15px;
    }

    .feature-pill {
        font-size: 11px;
    }

    .status {
        font-size: 11px;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# --------------------------------------------------
# BACKEND HELPERS
# --------------------------------------------------
def safe(value):
    return html.escape(str(value))


def ollama_status():
    try:
        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=4,
        )
        response.raise_for_status()

        models = [
            item.get("name", "")
            for item in response.json().get("models", [])
        ]

        model_available = (
            MODEL in models
            or any(
                name.split(":")[0] == MODEL.split(":")[0]
                and name.endswith(":3b")
                for name in models
            )
        )

        return True, model_available

    except requests.RequestException:
        return False, False


def extract_json(text):
    text = text.strip()

    # Remove Markdown code fences if the model includes them.
    text = re.sub(
        r"^```(?:json)?\\s*|\\s*```$",
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()

    try:
        result = json.loads(text)

    except json.JSONDecodeError:
        decoder = json.JSONDecoder()
        start = text.find("{")

        if start == -1:
            raise ValueError(
                "The model did not return a JSON object."
            )

        try:
            result, _ = decoder.raw_decode(text[start:])

        except json.JSONDecodeError as exc:
            raise ValueError(
                "The model returned incomplete or invalid JSON. "
                "Try Balanced or Deep analysis."
            ) from exc

    if not isinstance(result, dict):
        raise ValueError("Expected a JSON report object.")

    return result


def analyse_reviews(reviews, language, strength):
    setting = THINKING_OPTIONS[strength]

    depth_instructions = {
        "Quick": (
            "Produce a brief report. Use short summaries "
            "and concise bullet points."
        ),
        "Balanced": (
            "Produce a practical business report. "
            "Identify important patterns and actionable improvements."
        ),
        "Deep": (
            "Produce a more detailed analysis. Examine recurring "
            "complaints, customer expectations, strengths, "
            "operational issues, and prioritized recommendations. "
            "Do not invent evidence or statistics."
        ),
    }

    system_prompt = """
You are an expert restaurant customer-experience analyst.

Your task is to analyze customer reviews and create
a structured, evidence-based business report.

Rules:
- Return one valid JSON object only.
- No Markdown, comments, or explanation outside JSON.
- Do not invent customer feedback.
- Use only the reviews provided.
- Do not treat an estimated rating as a real platform rating.
- Acknowledge mixed feedback where appropriate.
- Keep JSON keys in English.
- Write the JSON string values in the requested language.
- All requested fields must be present.
- Keep numeric estimated_rating_out_of_5 between 0 and 5.
"""

    user_prompt = f"""
Analyze the following restaurant reviews.

ANALYSIS STRENGTH:
{strength}

DEPTH INSTRUCTIONS:
{depth_instructions[strength]}

OUTPUT LANGUAGE:
{language}

CUSTOMER REVIEWS:
<reviews>
{reviews}
</reviews>

Return ONLY a valid JSON object using this exact structure:

{{
    "overall_sentiment": "Positive",
    "estimated_rating_out_of_5": 4.0,
    "one_line_verdict": "Short overall verdict",
    "summary": "Summary of customer feedback",
    "top_positives": [
        "Positive finding 1",
        "Positive finding 2",
        "Positive finding 3"
    ],
    "top_negatives": [
        "Negative finding 1",
        "Negative finding 2",
        "Negative finding 3"
    ],
    "customer_pain_points": [
        "Pain point 1",
        "Pain point 2",
        "Pain point 3"
    ],
    "business_suggestions": [
        "Actionable recommendation 1",
        "Actionable recommendation 2",
        "Actionable recommendation 3"
    ],
    "best_for": [
        "Suitable customer group 1",
        "Suitable customer group 2"
    ],
    "keywords": [
        "keyword 1",
        "keyword 2",
        "keyword 3"
    ]
}}

overall_sentiment must be one of:
Positive, Neutral, Negative, Mixed.

Estimated rating is your interpretation of the provided feedback,
not an actual customer star rating.

If evidence for a finding is unavailable, use an empty list
instead of inventing information.
"""

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        "stream": False,
        "format": "json",
        "options": {
            # Low fixed temperature helps produce valid JSON.
            # Thinking strength adjusts depth and token budget instead.
            "temperature": 0.2,
            "num_predict": setting["num_predict"],
            "num_ctx": 8192,
        },
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300,
    )

    response.raise_for_status()

    data = response.json()
    content = data.get("message", {}).get("content", "")

    if not content:
        raise ValueError(
            "Ollama returned an empty response."
        )

    return extract_json(content)


def render_items(items, css_class):
    if not isinstance(items, list):
        return ""

    return "".join(
        f'<div class="insight-item {css_class}">'
        f'{safe(item)}</div>'
        for item in items
    )


def render_tags(items):
    if not isinstance(items, list):
        return ""

    return "".join(
        f'<span class="tag">{safe(item)}</span>'
        for item in items
    )


def render_card(title, content):
    st.markdown(
        f"""
        <div class="content-card">
            <div class="content-title">{safe(title)}</div>
            {content}
        </div>
        """,
        unsafe_allow_html=True,
    )


def reset_all():
    st.session_state.analysis_result = None
    st.session_state.reviews = ""


# --------------------------------------------------
# TOP NAVIGATION
# --------------------------------------------------
nav_left, nav_right = st.columns([3, 2])

with nav_left:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">✦</div>
            <div>
                Reviewly
                <div class="brand-sub">AI Review Intelligence</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

running, model_ready = ollama_status()

with nav_right:
    if running and model_ready:
        status_html = (
            '<span class="status-dot"></span>'
            'Qwen2.5:3b · Local AI'
        )
    elif running:
        status_html = "● Model not downloaded"
    else:
        status_html = "● Ollama offline"

    st.markdown(
        f'<div class="status">{status_html}</div>',
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# HERO SECTION
# --------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="hero-orb">✦</div>
        <div class="hero-title">
            Turn reviews into <span>real insights.</span>
        </div>
        <div class="hero-description">
            Understand what customers love, what frustrates them,
            and how to make your restaurant better.
            Powered by AI running privately on your machine.
        </div>
        <div class="feature-line">
            <span class="feature-pill">✧ Sentiment intelligence</span>
            <span class="feature-pill">◈ Customer insights</span>
            <span class="feature-pill">✦ Actionable recommendations</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# OLLAMA CONNECTION WARNINGS
# --------------------------------------------------
if not running:
    st.error(
        "Ollama is not running. Start Ollama before analyzing reviews."
    )

    st.code(
        "ollama serve",
        language="bash",
    )

elif not model_ready:
    st.warning(
        f"The model {MODEL} is not installed."
    )

    st.code(
        f"ollama pull {MODEL}",
        language="bash",
    )


# --------------------------------------------------
# REVIEW INPUT
# --------------------------------------------------
st.markdown(
    '<div class="section-label">✍️ Customer reviews</div>',
    unsafe_allow_html=True,
)

st.text_area(
    "Customer reviews",
    key="reviews",
    height=240,
    placeholder=(
        "Paste your restaurant reviews here...\n\n"
        "Example:\n"
        "The food was delicious and the staff were friendly.\n"
        "Delivery was late and the packaging was damaged.\n"
        "Great atmosphere but the prices felt too high."
    ),
    label_visibility="collapsed",
)

reviews_text = st.session_state.reviews

review_count = len(
    [
        line
        for line in reviews_text.splitlines()
        if line.strip()
    ]
)

st.markdown(
    f"""
    <div class="input-hint">
        {review_count} non-empty lines detected ·
        Tip: Paste one review per line for better analysis.
    </div>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# INPUT TOOLBAR
# --------------------------------------------------
# This provides a ChatGPT-inspired toolbar directly
# under the review text box, without a sidebar.

tool_left, tool_middle, tool_right = st.columns(
    [1.3, 1.2, 1.5],
    vertical_alignment="bottom",
)

with tool_left:
    thinking_strength = st.selectbox(
        "✦ Thinking strength",
        options=list(THINKING_OPTIONS.keys()),
        key="thinking_strength",
        help=(
            "Quick creates concise insights. "
            "Balanced provides practical analysis. "
            "Deep requests a more detailed report. "
            "Qwen2.5:3b does not support native thinking-effort control."
        ),
    )

with tool_middle:
    output_language = st.selectbox(
        "🌐 Language",
        options=["English", "Telugu", "Tenglish"],
        key="output_language",
    )

with tool_right:
    analyse_clicked = st.button(
        "✦ Analyze reviews",
        type="primary",
        use_container_width=True,
        disabled=not (running and model_ready),
    )

st.caption(
    f"✧ {THINKING_OPTIONS[thinking_strength]['description']}"
    " · Powered by Qwen2.5:3b"
)

action_left, action_right, action_space = st.columns(
    [1, 1, 2.5]
)

with action_left:
    st.button(
        "Try example",
        use_container_width=True,
        on_click=lambda: st.session_state.update(
            reviews=SAMPLE_REVIEWS,
            analysis_result=None,
        ),
    )

with action_right:
    st.button(
        "Clear all",
        use_container_width=True,
        on_click=reset_all,
    )


# --------------------------------------------------
# RUN ANALYSIS
# --------------------------------------------------
if analyse_clicked:
    if not reviews_text.strip():
        st.warning("Please enter customer reviews first.")

    else:
        with st.spinner(
            f"Analyzing with Qwen2.5:3b · {thinking_strength}..."
        ):
            try:
                result = analyse_reviews(
                    reviews_text,
                    output_language,
                    thinking_strength,
                )

                st.session_state.analysis_result = result
                st.session_state.analysis_meta = {
                    "strength": thinking_strength,
                    "language": output_language,
                    "review_count": review_count,
                }

            except requests.exceptions.HTTPError as exc:
                st.error(
                    f"Ollama returned an HTTP error: {exc}"
                )

            except requests.exceptions.Timeout:
                st.error(
                    "The request timed out. Try Quick analysis "
                    "or use fewer reviews."
                )

            except requests.exceptions.RequestException as exc:
                st.error(
                    f"Could not connect to Ollama: {exc}"
                )

            except ValueError as exc:
                st.error(str(exc))


# --------------------------------------------------
# ANALYSIS DASHBOARD
# --------------------------------------------------
if st.session_state.analysis_result is not None:

    result = st.session_state.analysis_result

    st.divider()

    st.markdown(
        '<div class="result-heading">✦ Your review intelligence</div>',
        unsafe_allow_html=True,
    )

    meta = st.session_state.get("analysis_meta", {})

    st.markdown(
        f"""
        <div class="result-subheading">
            Generated locally with {safe(MODEL)}
            · {safe(meta.get("strength", "Balanced"))} analysis
            · {safe(meta.get("language", "English"))}
        </div>
        """,
        unsafe_allow_html=True,
    )

    sentiment = str(
        result.get("overall_sentiment", "N/A")
    )

    verdict = str(
        result.get("one_line_verdict", "No verdict available")
    )

    try:
        rating = float(
            result.get("estimated_rating_out_of_5", 0)
        )
        rating = max(0, min(5, rating))

    except (TypeError, ValueError):
        rating = 0.0

    sentiment_colors = {
        "positive": "#34d399",
        "negative": "#fb7185",
        "neutral": "#fbbf24",
        "mixed": "#c4b5fd",
    }

    sentiment_color = sentiment_colors.get(
        sentiment.lower(), "#c4b5fd"
    )

    # ----------------------------------------------
    # METRICS
    # ----------------------------------------------
    metric_a, metric_b, metric_c = st.columns(3)

    with metric_a:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Overall sentiment</div>
                <div class="metric-value"
                     style="color:{sentiment_color}">
                    {safe(sentiment)}
                </div>
                <div class="metric-description">
                    AI-detected customer sentiment
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with metric_b:
        rating_width = rating / 5 * 100

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Estimated rating</div>
                <div class="metric-value">
                    {rating:.1f}
                    <span style="font-size:14px;color:#999">
                        / 5
                    </span>
                </div>
                <div class="rating-track">
                    <div class="rating-fill"
                         style="width:{rating_width}%"></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with metric_c:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Reviews analyzed</div>
                <div class="metric-value">
                    {meta.get("review_count", review_count)}
                </div>
                <div class="metric-description">
                    Non-empty input lines
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ----------------------------------------------
    # VERDICT
    # ----------------------------------------------
    render_card(
        "✦ AI verdict",
        f"""
        <div style="font-size:17px;font-weight:650;color:#e5dcff">
            {safe(verdict)}
        </div>
        """,
    )

    # ----------------------------------------------
    # SUMMARY
    # ----------------------------------------------
    render_card(
        "◈ Executive summary",
        f"""
        <div>
            {safe(result.get("summary", "No summary available."))}
        </div>
        """,
    )

    # ----------------------------------------------
    # POSITIVES AND NEGATIVES
    # ----------------------------------------------
    positive_col, negative_col = st.columns(2)

    with positive_col:
        render_card(
            "✓ What customers love",
            render_items(
                result.get("top_positives", []),
                "positive",
            ) or "<p>No clear positives identified.</p>",
        )

    with negative_col:
        render_card(
            "✕ What needs improvement",
            render_items(
                result.get("top_negatives", []),
                "negative",
            ) or "<p>No clear negatives identified.</p>",
        )

    # ----------------------------------------------
    # PAIN POINTS
    # ----------------------------------------------
    render_card(
        "⚑ Customer pain points",
        render_items(
            result.get("customer_pain_points", []),
            "warning",
        ) or "<p>No recurring pain points identified.</p>",
    )

    # ----------------------------------------------
    # RECOMMENDATIONS
    # ----------------------------------------------
    render_card(
        "✧ Recommended actions",
        render_items(
            result.get("business_suggestions", []),
            "suggestion",
        ) or "<p>No recommendations available.</p>",
    )

    # ----------------------------------------------
    # CUSTOMER FIT + KEYWORDS
    # ----------------------------------------------
    fit_col, keyword_col = st.columns(2)

    with fit_col:
        render_card(
            "♧ Best suited for",
            render_tags(
                result.get("best_for", [])
            ) or "<p>Not enough information.</p>",
        )

    with keyword_col:
        render_card(
            "⌗ Key themes",
            render_tags(
                result.get("keywords", [])
            ) or "<p>No themes identified.</p>",
        )

    st.write("")

    # ----------------------------------------------
    # EXPORT
    # ----------------------------------------------
    st.download_button(
        label="↓ Export full report as JSON",
        data=json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
        ),
        file_name="reviewly_analysis.json",
        mime="application/json",
        use_container_width=True,
    )

    st.caption(
        "The sentiment and rating are AI estimates based only "
        "on the supplied reviews, not verified platform metrics."
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.markdown(
    """
    <div class="footer-note">
        ✦ Reviewly · Powered by Ollama & Qwen2.5
        <br>
        Local-first AI · Your review data stays on your machine
    </div>
    """,
    unsafe_allow_html=True,
)

