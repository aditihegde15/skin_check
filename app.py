from flask import Flask, jsonify, request, render_template_string

from skincare.parser import parse_ingredients
from skincare.scorer import analyze

app = Flask(__name__) 

HTML = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Skincare Check</title>

<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

:root {
  --kelp: #3d402f;
  --willow: #6b7f64;
  --whiskey: #d59a7a;
  --tamarillo: #9c0d0f;
  --cream: #f6f4ef;
}

body {
  font-family: 'Inter', sans-serif;
  background: var(--cream);
  color: #2f2f2f;
  padding: 48px 24px;
}

.container {
  max-width: 760px;
  margin: auto;
  background: #ffffff;
  border-radius: 22px;
  padding: 48px;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.08);
}

h1 {
  font-family: 'Playfair Display', serif;
  font-size: 40px;
  font-weight: 600;
  color: var(--kelp);
  text-align: center;
  margin-bottom: 12px;
}

.subtitle {
  text-align: center;
  color: #6e6e6e;
  font-size: 15px;
  margin-bottom: 40px;
}

label {
  font-weight: 500;
  font-size: 14px;
  letter-spacing: 0.02em;
  color: var(--kelp);
  margin-bottom: 8px;
  display: block;
}

textarea, select {
  width: 100%;
  padding: 16px 18px;
  border-radius: 14px;
  border: 1px solid #e6e2d9;
  font-size: 14px;
  margin-bottom: 24px;
  background: #faf9f6;
  font-family: 'Inter', sans-serif;
}

textarea::placeholder {
  color: #a5a5a5;
}

button {
  width: 100%;
  background: var(--kelp);
  color: #ffffff;
  border: none;
  border-radius: 999px;
  padding: 16px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.1s ease;
}

button:hover {
  background: #2f3224;
  transform: translateY(-1px);
}

.error {
  background: #fbeeee;
  color: var(--tamarillo);
  padding: 16px;
  border-radius: 14px;
  margin-top: 24px;
}

.result {
  margin-top: 40px;
  text-align: center;
}

.verdict {
  font-family: 'Playfair Display', serif;
  font-size: 28px;
  margin-bottom: 20px;
}

.safe {
  color: var(--willow);
}

.avoid {
  color: var(--tamarillo);
}

.card {
  background: #faf9f6;
  border-radius: 18px;
  padding: 24px;
  margin-top: 24px;
  text-align: left;
}

.card h3 {
  font-family: 'Playfair Display', serif;
  font-size: 20px;
  color: var(--kelp);
  margin-bottom: 16px;
}

.ingredient {
  padding: 12px 0;
  border-bottom: 1px solid #e6e2d9;
}

.ingredient:last-child {
  border-bottom: none;
}

.tag {
  display: inline-block;
  background: #e7eadf;
  color: var(--kelp);
  border-radius: 999px;
  padding: 4px 12px;
  font-size: 12px;
  margin-right: 6px;
  margin-top: 6px;
}

small {
  color: #6e6e6e;
}
</style>

</head>

<body>
<div class="container">

  <h1>Skincare Check</h1>
  <div class="subtitle">Paste a product's ingredients list to see how skin-friendly it is</div>

  <form method="post" action="/analyze">


    <label>Paste ingredients</label>
    <textarea name="ingredients" rows="6" placeholder="Water, Glycerin, Niacinamide...">{{ raw or "" }}</textarea>

    <label>Skin focus</label>
    <select name="skin_focus">
      <option value="">No specific concern</option>
      <option value="sensitive">Sensitive</option>
      <option value="acne_prone">Acne-prone</option>
    </select>

    <button type="submit">Analyze </button>
  </form>

  {% if error %}
    <div class="error">{{ error }}</div>
  {% endif %}

  {% if report %}
    <div class="result">

      <div class="verdict
        {% if report.verdict == 'Safe' %}safe{% endif %}
        {% if report.verdict == 'Caution' %}caution{% endif %}
        {% if report.verdict == 'Avoid' %}avoid{% endif %}
      ">
        {{ report.verdict }} · {{ report.score }}/100
      </div>

      <div class="card">
        <h3>Parsed Ingredients</h3>
        {% for ing in report.parsed_ingredients %}
          <div class="ingredient">{{ ing }}</div>
        {% endfor %}
      </div>

      <div class="card">
        <h3>Flags & Notes</h3>
        {% for f in report.findings %}
          <div class="ingredient">
            <b>{{ f.ingredient }}</b><br>
            {% for t in f.tags %}
              <span class="tag">{{ t }}</span>
            {% endfor %}
            <br>
            <small>{{ f.note }}</small>
          </div>
        {% endfor %}
      </div>

    </div>
  {% endif %}

</div>
</body>
</html>
"""

@app.get("/")
def home():
    return render_template_string(HTML, raw="", report=None)

@app.post("/analyze")
def analyze_form():
    raw = request.form.get("ingredients", "").strip()
    skin_focus = request.form.get("skin_focus") or None

    try:
        if raw:
            raw_ingredients = raw
        else:
            return render_template_string(
                HTML,
                error="Please paste product ingredients.",
                raw=raw,
                report=None
            )

        ingredients = parse_ingredients(raw_ingredients)
        report = analyze(ingredients, skin_focus=skin_focus)

        return render_template_string(
            HTML,
            raw=raw,
            report={
                "verdict": report.verdict,
                "score": report.score,
                "parsed_ingredients": ingredients,
                "findings": [f.__dict__ for f in report.findings],
            },
            error=None
        )

    except Exception as e:
        return render_template_string(
            HTML,
            error=str(e),
            raw=raw,
            report=None
        )

if __name__ == "__main__":
    app.run(debug=True)
