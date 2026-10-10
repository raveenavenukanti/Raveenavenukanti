from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

def make_ads(d):
    product = d.get("product", "Your Product").strip()
    benefit = d.get("benefit", "Discover the benefits").strip()
    audience = d.get("audience", "your audience").strip() or "your audience"
    offer = d.get("offer", "").strip()
    offer_text = f" Offer: {offer}." if offer else ""
    return {
      "Instagram": {
        "A": {"headline": f"Meet {product} ✨", "copy": f"{benefit}. Discover {product} and see if it fits your needs.{offer_text}", "cta": "Learn More"},
        "B": {"headline": "Something worth discovering", "copy": f"Looking for {benefit.lower()}? Explore {product}.{offer_text}", "cta": "Get Started"}},
      "Google": {
        "A": {"headline": f"{product} | Learn More", "copy": f"{benefit}. Explore details about {product}.", "cta": "Learn More"},
        "B": {"headline": f"Discover {product}", "copy": f"Find out more about {product} and its features.", "cta": "Explore Now"}},
      "LinkedIn": {
        "A": {"headline": f"{product} for {audience}", "copy": f"Discover how {product} may support {audience}. {benefit}.", "cta": "Learn More"},
        "B": {"headline": "Explore a new option", "copy": f"Considering options for {audience}? Learn more about {product}.", "cta": "Discover More"}},
      "WhatsApp": {
        "A": {"headline": "A quick introduction", "copy": f"Hi! We wanted to share {product} with you. {benefit}.{offer_text} Reply if you'd like to know more.", "cta": "Reply to Learn More"},
        "B": {"headline": f"Curious about {product}?", "copy": f"Hello! Here's a quick look at {product}: {benefit}. Message us for details.", "cta": "Message Us"}}
    }

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/generate")
def generate():
    data = request.get_json(silent=True) or {}
    if not data.get("product", "").strip() or not data.get("benefit", "").strip():
        return jsonify({"error": "Enter a product name and its main benefit."}), 400
    ads = make_ads(data)
    return jsonify({
      "ads": ads,
      "languages": {
        "English": f"{data['product']}: {data['benefit']}. Learn more today.",
        "Telugu": f"{data['product']} గురించి తెలుసుకోండి. {data['benefit']}. మరిన్ని వివరాల కోసం సంప్రదించండి.",
        "Hindi": f"{data['product']} के बारे में जानें। {data['benefit']}। अधिक जानकारी के लिए संपर्क करें।"
      },
      "audiences": [
        {"audience": data.get("audience") or "Target audience", "copy": f"{data['benefit']}. Explore {data['product']}.", "cta": "Learn More"},
        {"audience": "First-time customers", "copy": f"New to {data['product']}? Explore its details and features.", "cta": "Discover More"},
        {"audience": "People comparing options", "copy": f"Compare your options and learn more about {data['product']}.", "cta": "Compare Options"}
      ],
      "doctor": "Check that claims are accurate, add a real differentiator, and match the CTA to your landing page.",
      "trust": "Verify every product claim before publishing. This is a drafting aid, not legal advice.",
      "budget": "Suggested testing framework: 40% initial creative tests, 40% on promising results, 20% for retesting. Adjust to your real budget; this is not a forecast.",
      "campaign": f"Campaign concept: Introduce {data['product']} to {data.get('audience') or 'your audience'} with the main benefit: {data['benefit']}.",
      "ab": "Test benefit-led copy against curiosity-led copy. Keep audience and budget comparable, and select one primary metric before testing."
    })

if __name__ == "__main__":
    app.run(debug=True)
