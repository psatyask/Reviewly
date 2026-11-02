# ✦ Reviewly — AI-Powered Google Reviews Sentiment Analysis

### Understand customer sentiment. Discover recurring patterns. Turn feedback into actionable insights.

Reviewly is a locally hosted, Generative AI-powered sentiment analysis application that transforms unstructured customer reviews into meaningful, structured business intelligence.

Built with **Python, Streamlit, Ollama, and Qwen2.5:3b**, the application helps restaurant owners, business managers, and analysts identify customer satisfaction patterns, recognize operational weaknesses, and discover opportunities to improve the customer experience.

Instead of manually reading hundreds of reviews and identifying trends, users can paste customer feedback into Reviewly and generate an AI-powered report containing sentiment classification, estimated ratings, recurring complaints, customer preferences, and actionable recommendations.

The application runs using a locally hosted Large Language Model (LLM), eliminating the need for paid cloud-based inference APIs.

---

## 1. Project Overview

### What is Reviewly?

Online customer reviews are an important source of business intelligence. Platforms such as Google Reviews, Zomato, and Swiggy allow customers to express opinions about food quality, service, delivery, pricing, cleanliness, and overall experience.

However, individual reviews are often unstructured, subjective, and difficult to analyze collectively.

Reviewly addresses this challenge using **Generative AI and Natural Language Processing (NLP)** to convert raw text feedback into organized insights.

The application analyzes customer reviews and generates:

- **Overall Sentiment:** Positive, Negative, Neutral, or Mixed.
- **Estimated Customer Rating:** AI-derived rating on a five-point scale.
- **Executive Summary:** Consolidated understanding of customer feedback.
- **Positive Feedback Patterns:** Frequently praised aspects of the business.
- **Negative Feedback Patterns:** Recurring customer complaints.
- **Customer Pain Points:** Operational problems affecting customer satisfaction.
- **Business Recommendations:** Practical suggestions for improvement.
- **Customer Suitability:** Potential customer groups based on feedback.
- **Key Themes:** Important topics appearing in customer reviews.

The generated analysis can also be exported as a structured JSON report.

### Primary objective

The goal of this project is not simply to classify reviews as positive or negative.

It is to **understand why customers feel a certain way, identify recurring patterns, and translate those patterns into business decisions.**

For example, a restaurant may receive positive feedback about taste while repeatedly receiving negative feedback about delivery speed.

A traditional sentiment classifier might identify both positive and negative reviews. Reviewly goes further by identifying the operational gap and recommending improvements.

---

## 2. Business Problem

### The challenge

Businesses receive customer feedback across multiple online platforms.

As the number of reviews increases, manually analyzing every review becomes time-consuming and inconsistent.

Common challenges include:

1. **Unstructured feedback:** Customer opinions are written in natural language rather than organized categories.
2. **Mixed sentiments:** A single review may contain both praise and criticism.
3. **Recurring problems:** Operational issues may appear across multiple reviews but remain unnoticed.
4. **Limited actionable insights:** Standard ratings do not necessarily explain what needs improvement.
5. **Manual analysis overhead:** Business teams must spend time reading, categorizing, and summarizing feedback.
6. **Decision-making gaps:** Management may know that satisfaction is declining without understanding the underlying reasons.

### Proposed solution

Reviewly uses a local Large Language Model to interpret customer feedback in context.

Instead of relying only on keyword matching, the system uses prompt-driven language understanding to identify important themes and produce a structured report.

**Example**

Customer feedback:

> "The biryani was delicious, but delivery took almost an hour and the food arrived cold."

A basic sentiment classifier may struggle with the combination of positive and negative opinions.

Reviewly can identify:

| Category               | Insight                                     |
| ---------------------- | ------------------------------------------- |
| Positive feedback      | Food taste                                  |
| Negative feedback      | Delayed delivery                            |
| Customer pain point    | Food arriving cold                          |
| Business opportunity   | Improve delivery coordination and packaging |
| Overall interpretation | Mixed sentiment                             |

This provides a more useful understanding of the customer experience.

---

## 3. Technology Stack

| Component            | Technology              | Purpose                                         |
| -------------------- | ----------------------- | ----------------------------------------------- |
| Programming Language | Python                  | Application logic and backend processing        |
| Frontend Framework   | Streamlit               | Interactive, responsive web application         |
| Large Language Model | Qwen2.5:3b              | Customer-review language understanding          |
| LLM Runtime          | Ollama                  | Local model hosting and inference               |
| API Communication    | Requests                | HTTP communication between Streamlit and Ollama |
| Data Exchange        | JSON                    | Structured LLM responses and report export      |
| Text Processing      | Python `re`             | Response cleanup and JSON extraction            |
| UI Styling           | HTML and CSS            | Custom interface and responsive design          |
| Application State    | Streamlit Session State | Preserving user input and analysis results      |

### Why Qwen2.5:3b?

Qwen2.5:3b is a relatively compact language model suitable for experimenting with local Generative AI applications.

Its advantages for this project include:

- Local inference without a paid external LLM API.
- Natural-language understanding of customer feedback.
- Ability to follow structured JSON output instructions.
- Multilingual text-generation capabilities.
- Relatively modest hardware requirements compared with larger language models.

Performance depends on the local hardware, model configuration, number of reviews, and requested report depth.

### Why Ollama?

Ollama simplifies running open-weight language models locally.

It provides a REST API through which the Streamlit application can send prompts and receive generated responses.

The local Ollama service is typically available at:

`http://localhost:11434`

The chat endpoint used in this project is:

`http://localhost:11434/api/chat`

No external hosted inference API is required for the configured workflow.

---

## 4. System Architecture

Reviewly follows a lightweight, local, inference-based architecture.

```text
                  ┌──────────────────────────────┐
                  │         End User             │
                  │ Restaurant Owner / Analyst   │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │       Streamlit UI           │
                  │                              │
                  │ • Customer Review Input      │
                  │ • Thinking Strength          │
                  │ • Output Language            │
                  │ • Analyze Button             │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │     Application Backend      │
                  │           Python             │
                  │                              │
                  │ • Input Validation           │
                  │ • Prompt Construction        │
                  │ • Inference Configuration    │
                  │ • API Request Handling       │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │       Ollama REST API        │
                  │  localhost:11434/api/chat    │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │       Qwen2.5:3b LLM         │
                  │                              │
                  │ • Language Understanding     │
                  │ • Sentiment Interpretation   │
                  │ • Theme Identification       │
                  │ • Insight Generation         │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │      Structured JSON         │
                  │                              │
                  │ • Sentiment                  │
                  │ • Estimated Rating           │
                  │ • Summary                    │
                  │ • Positives / Negatives      │
                  │ • Pain Points                │
                  │ • Recommendations            │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │    Validation & Parsing      │
                  │                              │
                  │ • JSON Extraction            │
                  │ • Basic Type Checks          │
                  │ • Error Handling             │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                  ┌──────────────────────────────┐
                  │       Results Dashboard      │
                  │                              │
                  │ • Visual Metric Cards        │
                  │ • Feedback Insights          │
                  │ • Business Suggestions       │
                  │ • JSON Export                │
                  └──────────────────────────────┘
```

### Architecture explanation

**Frontend layer — Streamlit**

The frontend collects review text, analysis preferences, and user actions. It also displays the generated report through a responsive dashboard.

**Application layer — Python**

The backend prepares prompts, configures inference settings, communicates with Ollama, and converts the model response into data the frontend can display.

**Inference layer — Ollama and Qwen2.5**

Ollama loads and serves Qwen2.5:3b. The model processes the reviews and generates a structured response based on the instructions supplied by the application.

**Output layer — JSON and dashboard**

The application parses the generated JSON and presents it in a readable business report.

The user can export the report for further processing.

---

## 5. End-to-End Workflow

The application operates through the following sequence.

### Step 1 — User provides customer reviews

Users paste customer reviews into the text area.

Example:

```text
The biryani was excellent and the portion size was generous.

The delivery was delayed and the food arrived cold.

Staff were friendly and the restaurant was clean.

Prices were slightly high compared to nearby restaurants.

Desserts were delicious and the ambience was family-friendly.
```

For the current interface, placing one review on each line is recommended.

The application counts non-empty lines as an approximate review count.

### Step 2 — User selects analysis strength

Users can choose between three analysis modes.

| Mode     | Behavior                                    | Best suited for              |
| -------- | ------------------------------------------- | ---------------------------- |
| Quick    | Short, concise analysis                     | Fast review summaries        |
| Balanced | Practical and reasonably detailed insights  | General business analysis    |
| Deep     | More extensive findings and recommendations | Detailed business evaluation |

These options change the prompt instructions and generated-token budget.

**Technical clarification:** Qwen2.5:3b does not provide a native reasoning-effort control equivalent to dedicated reasoning models. Therefore, the thinking-strength selector is an application-level analysis-depth setting, not an activation of hidden model reasoning.

### Step 3 — User selects output language

Supported output choices:

- English
- Telugu
- Tenglish (Telugu-English mixed communication)

The language instruction is passed to the model as part of the prompt.

Language accuracy depends on the model's multilingual capabilities.

### Step 4 — Prompt engineering

The Python backend constructs two messages:

**System prompt**

Defines the model's role as a restaurant customer-experience analyst and instructs it to produce valid structured JSON without inventing customer feedback.

**User prompt**

Contains the supplied customer reviews, requested language, analysis strength, output schema, and business-analysis instructions.

This architecture uses **prompt engineering rather than fine-tuning**.

The model's parameters are not updated, and no additional training is performed.

### Step 5 — Local LLM inference

The application sends a POST request to Ollama.

Simplified example:

```python
payload = {
    "model": "qwen2.5:3b",
    "messages": [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ],
    "stream": False,
    "format": "json",
    "options": {
        "temperature": 0.2,
        "num_predict": 1200,
        "num_ctx": 8192
    }
}
```

Ollama runs the model locally and returns a generated response.

`format="json"` requests JSON-formatted output, while the prompts specify the expected report structure.

### Step 6 — Response processing

The application extracts and parses the JSON generated by the model.

Processing includes:

- Removing possible Markdown code fences.
- Parsing the response using Python's JSON library.
- Attempting to recover a JSON object from surrounding text.
- Checking that the top-level result is a JSON object.
- Reporting an error if the response cannot be parsed.

The implementation performs basic JSON parsing and validation. Full schema validation of every field has not been implemented.

### Step 7 — Business intelligence report

After successful parsing, Streamlit displays the report.

The result includes sentiment metrics, an estimated rating, customer feedback categories, and business recommendations.

The report remains available through Streamlit session state during the active application session.

### Step 8 — Export report

Users can download the generated analysis as a JSON file.

This format can be used for additional analysis, data storage, or integration with other applications.

---

## 6. Key Features

### 6.1 Context-aware sentiment analysis

Reviewly interprets the overall tone of customer feedback.

Supported sentiment categories:

| Sentiment | Meaning                                           |
| --------- | ------------------------------------------------- |
| Positive  | Feedback is predominantly favorable               |
| Negative  | Feedback is predominantly unfavorable             |
| Neutral   | Feedback is mainly neutral or inconclusive        |
| Mixed     | Meaningful positive and negative feedback coexist |

Unlike a basic keyword-based classifier, the LLM can interpret sentiment within the context of a complete statement.

### 6.2 Estimated customer rating

The application requests an estimated score between 0 and 5.

This score is a model-generated interpretation of the supplied customer feedback.

It is **not** an actual Google Reviews rating or a statistically verified average of customer star ratings.

### 6.3 Positive and negative pattern identification

The application identifies customer experiences commonly associated with satisfaction or dissatisfaction.

Examples:

**Positive themes**

- Food quality and taste.
- Friendly staff.
- Restaurant ambience.
- Product variety.
- Packaging quality.

**Negative themes**

- Delivery delays.
- High pricing.
- Slow customer support.
- Inconsistent food quality.
- Poor service experience.

These are illustrative categories; actual outputs depend on the submitted reviews.

### 6.4 Customer pain-point discovery

The system attempts to distinguish ordinary negative feedback from actionable operational problems.

For instance:

> "The food tasted great, but it arrived cold after 50 minutes."

Potential pain point: delivery delays affecting food temperature and satisfaction.

### 6.5 Business recommendation generation

The model translates identified customer problems into practical improvement suggestions.

Examples include improving delivery coordination, reviewing pricing and portion sizes, providing staff training, or strengthening quality-control procedures.

Recommendations should be reviewed by the business before implementation.

### 6.6 Local-first processing

The configured application sends reviews to the Ollama server on the local machine.

This offers greater control over where inference takes place compared with sending prompts to a third-party hosted model API.

However, the current version does not include enterprise security controls such as authentication, access management, or encrypted persistent storage.

### 6.7 Responsive dashboard

The Streamlit interface includes:

- Minimal dark-theme design.
- No navigation sidebar.
- Integrated input and analysis controls.
- Rounded insight cards.
- Responsive column layouts.
- Custom CSS styling.
- JSON export functionality.

---

## 7. Project Structure

The core project can be organized as follows:

```text
google-review-analyser/
│
├── app.py
│   └── Streamlit UI, prompt engineering,
│       Ollama integration, result rendering
│
├── requirements.txt
│   └── Python dependencies
│
├── README.md
│   └── Project documentation
│
└── .gitignore
    └── Ignored local and generated files
```

### Main application components

| Function / Component | Responsibility                                  |
| -------------------- | ----------------------------------------------- |
| `ollama_status()`    | Checks connectivity and model availability      |
| `extract_json()`     | Parses structured model responses               |
| `analyse_reviews()`  | Builds prompts and calls the Ollama API         |
| `render_items()`     | Displays positive, negative, and other findings |
| `render_tags()`      | Displays keywords and customer categories       |
| `render_card()`      | Renders reusable result cards                   |
| `reset_all()`        | Clears review input and analysis state          |
| `st.session_state`   | Preserves interaction state during reruns       |

The current project uses a single-file application architecture for simplicity.

---

## 8. Installation and Setup

### Prerequisites

Ensure the following are available:

- Python 3.10 or newer.
- pip package manager.
- Ollama installed locally.
- Internet connection for initial downloads.
- Sufficient RAM and disk space to run Qwen2.5:3b.

A GPU can improve inference performance, but it is not mandatory for running a suitable local Ollama model.

### Step 1 — Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Replace the placeholder with your actual GitHub repository URL.

### Step 2 — Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

For macOS or Linux:

```bash
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

The main Python dependencies are:

```text
streamlit>=1.39.0
requests>=2.31.0
```

Python's built-in `json`, `re`, and `html` modules do not require separate installation.

### Step 4 — Install Ollama

Download Ollama from its official website:

[https://ollama.com/download](https://ollama.com/download)

Complete the installation for your operating system.

Verify installation:

```bash
ollama --version
```

### Step 5 — Download Qwen2.5:3b

```bash
ollama pull qwen2.5:3b
```

Verify downloaded models:

```bash
ollama list
```

The model should appear in the installed-model list.

### Step 6 — Start Ollama

Ensure the Ollama service is running.

If it is not already running, launch it with:

```bash
ollama serve
```

Some desktop installations automatically start Ollama in the background.

### Step 7 — Launch Reviewly

Open a terminal in the project directory.

```bash
streamlit run app.py
```

Streamlit will normally open the application at:

```text
http://localhost:8501
```

The application is now ready for local review analysis.

---

## 9. How to Use Reviewly

1. Open the Streamlit application in your browser.
2. Copy customer review text from Google Reviews or another supported review source, where you are permitted to use that content.
3. Paste the reviews into the input area.
4. Select Quick, Balanced, or Deep analysis.
5. Choose English, Telugu, or Tenglish.
6. Click **Analyze reviews**.
7. Review the generated insights and recommendations.
8. Select **Export full report as JSON** to save the analysis.

### Additional controls

**Try example:** Loads a sample collection of restaurant reviews for testing.

**Clear all:** Clears the current review text and generated analysis.

### Important input note

The current version accepts pasted review text. It does not automatically collect Google Reviews from Google Maps or connect to the Google Places API.

The current implementation also treats each non-empty line as an approximate review count. Multiline reviews may therefore need preprocessing for accurate counting.

---

## 10. Example Input and Output

### Sample input

```text
The food tasted amazing and the biryani was excellent.

Customer service was polite and helpful.

Delivery took too long and the food arrived cold.

The prices are expensive compared to the quantity.

The ambience is excellent for families.

Packaging was good and the desserts were delicious.
```

### Illustrative output

The following is an example of the expected JSON structure, not a measured result from a recorded model execution.

```json
{
  "overall_sentiment": "Mixed",
  "estimated_rating_out_of_5": 3.7,
  "one_line_verdict": "Great food and ambience, but delivery and pricing need improvement.",
  "summary": "Customers appreciate the taste, friendly service, and family-friendly ambience. However, delayed deliveries and perceived high pricing negatively affect the overall experience.",
  "top_positives": [
    "Excellent food taste",
    "Friendly customer service",
    "Comfortable family ambience"
  ],
  "top_negatives": [
    "Delayed delivery",
    "Food arriving cold",
    "High prices relative to quantity"
  ],
  "customer_pain_points": [
    "Delivery delays",
    "Inconsistent delivery temperature",
    "Concerns about value for money"
  ],
  "business_suggestions": [
    "Improve delivery coordination",
    "Introduce better insulated packaging",
    "Review pricing and portion sizes"
  ],
  "best_for": [
    "Families",
    "Food enthusiasts"
  ],
  "keywords": [
    "Food quality",
    "Delivery",
    "Pricing",
    "Customer service",
    "Ambience"
  ]
}
```

### Business interpretation

This example suggests that the restaurant's food quality is a competitive strength, while delivery performance and perceived value require attention.

The business might prioritize delivery operations before investing heavily in menu expansion.

This is an example of moving from raw customer text to actionable decision support.

---

## 11. Generative AI and NLP Concepts Used

### 11.1 Large Language Models

Qwen2.5:3b is used to interpret natural-language feedback and generate structured analytical outputs.

### 11.2 Prompt Engineering

The application uses system and user prompts to define the model's role, task, constraints, response language, and expected schema.

### 11.3 Sentiment Analysis

The model classifies the overall emotional tone of the supplied feedback.

### 11.4 Aspect-Based Analysis

The application prompts the LLM to identify different aspects of the customer experience, including food, service, delivery, and pricing.

This is a prompt-based approximation of aspect-level sentiment analysis rather than a separately trained or formally evaluated aspect-based sentiment model.

### 11.5 Topic and Pattern Discovery

The model identifies themes in the submitted reviews and attempts to recognize recurring customer experiences.

It does not currently calculate validated topic frequencies or statistically significant trends.

### 11.6 Text Summarization

Multiple customer opinions are consolidated into an executive summary.

### 11.7 Structured Generation

The model is instructed to produce JSON rather than unrestricted narrative text.

This makes the response easier to display and export.

### 11.8 Local LLM Inference

Ollama hosts the model locally and exposes it through an HTTP API.

### 11.9 Inference Configuration

The application uses a low fixed temperature for structured output and adjusts token limits based on the selected analysis depth.

### 11.10 Business Insight Generation

The model transforms the interpreted feedback into business-oriented recommendations.

This is a decision-support use case, not an autonomous decision-making system.

---

## 12. Design and Engineering Decisions

### Why not use a traditional sentiment classifier?

A traditional sentiment-classification model can efficiently predict positive, negative, or neutral labels.

However, the goal of Reviewly is broader: it also generates summaries, extracts business problems, and suggests improvements.

An LLM allows these tasks to be combined in one prompt-driven workflow.

The trade-off is that generated outputs may be less deterministic and more difficult to evaluate than a narrowly trained classifier.

### Why use JSON output?

JSON creates a predictable structure that can be consumed by the frontend and other applications.

It also makes the results easier to export and potentially integrate with databases, dashboards, or APIs.

### Why use Streamlit?

Streamlit simplifies the development of interactive Python applications.

It supports rapid prototyping, UI components, session state, and visualization without requiring a separate JavaScript frontend.

### Why local inference?

Local inference reduces reliance on paid hosted inference APIs and gives the developer direct control over model execution.

The trade-offs include local hardware requirements, slower processing on some machines, and responsibility for model updates and deployment configuration.

### Why avoid a sidebar?

The updated interface places review input, model preferences, and actions together.

This improves task focus and provides a more streamlined experience on smaller screens.

---

## 13. Error Handling

The application includes basic handling for common runtime problems.

| Scenario                     | Application behavior                  |
| ---------------------------- | ------------------------------------- |
| Ollama service unavailable   | Displays an Ollama connection warning |
| Required model missing       | Displays a model download instruction |
| Empty review input           | Requests review text                  |
| HTTP request failure         | Displays an API error                 |
| Inference timeout            | Displays a timeout message            |
| Invalid model-generated JSON | Displays a parsing error              |

The application also escapes dynamic text inserted into custom HTML components, reducing the risk of unintended HTML rendering from model outputs.

More extensive schema validation, retries, input limits, and logging can be added in future releases.

---

## 14. Current Limitations

The project is a functional prototype with several important limitations.

**1. No live Google Reviews integration**

Users manually provide review text. The application does not retrieve live reviews directly from Google.

**2. No persistent database**

Reports are stored in Streamlit session state and can be downloaded, but there is no integrated persistent report database.

**3. No independently trained sentiment classifier**

The application uses LLM inference and prompt engineering rather than training a dedicated sentiment model.

**4. No formal accuracy evaluation**

The project does not currently include a labeled test dataset, confusion matrix, precision, recall, or F1-score benchmark.

**5. AI-generated ratings are subjective estimates**

The rating may vary across model runs and should not be interpreted as an official Google rating.

**6. No validated trend-frequency calculations**

The model identifies apparent themes but the application does not independently count how many reviews mention each topic.

**7. Local hardware dependency**

Inference performance depends on the user's system.

**8. Limited validation**

The application checks whether the generated response can be parsed as a JSON object, but does not fully validate all fields against a formal schema.

**9. Prompt-injection risks**

Customer reviews are untrusted input. Malicious review text could attempt to influence the model's instructions. The application does not currently include a comprehensive prompt-injection defense.

**10. Input-size limitations**

The configured context window and output-token budget limit how much review content can be analyzed in a single request.

These limitations inform the future engineering roadmap.

---

## 15. Future Improvements

### Phase 1 — Data ingestion

- Add an authorized Google Places API integration where supported.
- Support CSV and Excel review uploads.
- Add review preprocessing and deduplication.
- Capture review dates and source metadata.

### Phase 2 — Advanced analytics

- Classify sentiment for individual reviews.
- Generate aspect-level sentiment scores.
- Calculate topic frequencies.
- Identify sentiment changes over time.
- Add interactive charts and trend dashboards.

### Phase 3 — Model evaluation

- Build a labeled restaurant review evaluation dataset.
- Measure precision, recall, accuracy, and F1-score.
- Compare Qwen2.5 against traditional NLP baselines.
- Evaluate hallucinations and unsupported recommendations.
- Benchmark latency and resource consumption.

### Phase 4 — Scalable inference

- Add batching and review chunking.
- Implement structured schema validation.
- Add retry and response-repair strategies.
- Introduce inference caching.
- Evaluate larger models for improved analysis quality.

### Phase 5 — Production readiness

- Add authentication and access control.
- Introduce persistent storage.
- Add application logging and observability.
- Containerize the application with Docker.
- Implement automated testing and CI/CD.
- Establish privacy and data-retention policies.

### Phase 6 — Conversational analytics

A future version could support follow-up questions such as:

> "What are the three most common customer complaints?"

> "Which operational issue should the restaurant prioritize?"

> "Compare customer sentiment between the last two months."

> "Create a 30-day action plan based on the negative reviews."

This would expand Reviewly from a one-time analysis tool into an interactive AI-powered customer-experience assistant.

---

## 16. Responsible AI Considerations

Reviewly generates interpretations and recommendations using a probabilistic language model.

Users should consider the following:

- Generated insights may contain inaccuracies.
- The model may exaggerate patterns when the sample is small.
- Model-generated ratings are not official review-platform ratings.
- Recommendations require human judgment.
- Customer data should be handled according to applicable privacy requirements.
- Review text should be sourced and processed through authorized methods.
- AI outputs should not be represented as verified business statistics without independent validation.

For consequential business decisions, model-generated findings should be cross-checked against the original reviews and quantitative data.

---

## 17. Project Outcomes and Learning

This project demonstrates an end-to-end local Generative AI application that connects an interactive frontend to an LLM inference service.

### Engineering skills demonstrated

- Python application development.
- Streamlit frontend development.
- REST API integration.
- Ollama local model serving.
- LLM prompt engineering.
- Structured JSON generation.
- Natural Language Processing.
- Sentiment interpretation.
- Text summarization.
- Business insight generation.
- Session-state management.
- Error handling.
- Responsive UI development.

### Key learning

The central engineering challenge is transforming unstructured natural-language feedback into a format that is understandable, actionable, and easy for downstream systems to consume.

Reviewly demonstrates how prompt engineering, structured generation, and local LLM inference can be combined to create a practical business analytics application.

---

## 18. Conclusion

Reviewly is an AI-powered restaurant review intelligence application developed to explore how Generative AI can help businesses understand customer experiences more effectively.

By combining **Streamlit, Ollama, and Qwen2.5:3b**, the project demonstrates how unstructured Google-style restaurant reviews can be transformed into sentiment summaries, recurring feedback themes, customer pain points, and practical improvement recommendations.

The current implementation provides a foundation for future enhancements, including automated review ingestion, quantitative sentiment analytics, model evaluation, historical trend analysis, and conversational business intelligence.

**Core idea:** Move beyond knowing whether customers are satisfied and toward understanding *why they are satisfied, what problems recur, and what a business can improve.*

Built using the Python and Streamlit ecosystems, with local LLM inference powered by Ollama and Qwen2.5.

**Project category:** Generative AI · NLP · Sentiment Analysis · Customer Experience Analytics · Local LLM Applications
