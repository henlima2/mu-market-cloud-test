from flask import Flask, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h2>MU Market Cloud Test</h2>
    <p>Servidor funcionando.</p>
    <a href="/teste">Testar MuDomix</a>
    """


@app.route("/teste")
def teste():
    url = "https://mudomix.com/market/items?order=price_asc"

    resultado = {
        "http": None,
        "title": None,
        "url_final": None,
        "cards": None
    }

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage"
                ]
            )

            page = browser.new_page()

            response = page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000
            )

            resultado["http"] = response.status if response else None
            resultado["title"] = page.title()
            resultado["url_final"] = page.url
            resultado["cards"] = page.locator(".mu-item-card").count()

            browser.close()

    except Exception as e:
        resultado["erro"] = str(e)

    return jsonify(resultado)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
