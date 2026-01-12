from flask import Flask, request, render_template_string

app = Flask(__name__)

# =========================
# HTML INPUT (GRADIENT & ELEGAN)
# =========================
INPUT_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Kalkulator Antrian M/M/2</title>
  <style>
    body {
      font-family: 'Segoe UI', Arial, sans-serif;
      background: linear-gradient(135deg, #6a11cb, #2575fc);
      padding: 40px;
    }
    h2 {
      text-align: center;
      color: white;
      margin-bottom: 30px;
    }
    .card {
      background: white;
      max-width: 720px;
      margin: auto;
      padding: 30px;
      border-radius: 16px;
      box-shadow: 0 12px 30px rgba(0,0,0,0.25);
    }
    label {
      font-weight: 600;
      margin-top: 15px;
      display: block;
    }
    input {
      width: 100%;
      padding: 12px;
      margin-top: 6px;
      border-radius: 8px;
      border: 1px solid #ccc;
      font-size: 15px;
    }
    button {
      margin-top: 25px;
      padding: 14px;
      width: 100%;
      border: none;
      background: #2575fc;
      color: white;
      font-size: 16px;
      border-radius: 10px;
      cursor: pointer;
      font-weight: bold;
    }
    button:hover {
      background: #1a5fd0;
    }
    .hint {
      margin-top: 20px;
      font-size: 0.9em;
      color: #444;
      background: #f2f5ff;
      padding: 14px;
      border-radius: 10px;
    }
  </style>
</head>
<body>

<h2>Kalkulator Sistem Antrian M/M/2<br>(2 Pelayan)</h2>

<div class="card">
  <form method="post" action="/hasil">
    <label>Waktu antar kedatangan (menit)</label>
    <input name="interarrival" type="number" step="any" min="0" placeholder="contoh: 4" required>

    <label>Waktu pelayanan per pelayan (menit)</label>
    <input name="service_time" type="number" step="any" min="0" placeholder="contoh: 3" required>

    <button type="submit">Hitung</button>

    <div class="hint">
      λ = 1 / antar kedatangan<br>
      μ = 1 / waktu pelayanan<br>
      ρ = λ / (2μ), W = 1 / (μ − λ/2), Wq = λ² / (2μ(μ − λ/2))
    </div>
  </form>
</div>

</body>
</html>
"""

# =========================
# HTML HASIL (SAMA PERSIS STYLING INPUT)
# =========================
HASIL_HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Hasil Perhitungan M/M/2</title>
  <style>
    body {
      font-family: 'Segoe UI', Arial, sans-serif;
      background: linear-gradient(135deg, #6a11cb, #2575fc);
      padding: 40px;
    }
    h2 {
      text-align: center;
      color: white;
      margin-bottom: 30px;
    }
    .card {
      background: white;
      max-width: 860px;
      margin: auto;
      padding: 30px;
      border-radius: 16px;
      box-shadow: 0 12px 30px rgba(0,0,0,0.25);
      margin-bottom: 30px;
    }
    .mono {
      font-family: "Times New Roman", serif;
      font-size: 18px;
      line-height: 2;
    }

    /* ===== PECahan MATEMATIKA RAPAT ===== */
    .fraction {
      display: inline-flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      vertical-align: middle;
      margin: 0 6px;
      line-height: 1;
    }
    .fraction .top {
      border-bottom: 2px solid #000;
      padding: 0 6px;
      margin-bottom: -2px;
    }
    .fraction .bottom {
      padding: 0 6px;
      margin-top: -2px;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 15px;
    }
    th, td {
      padding: 12px;
      border-bottom: 1px solid #ddd;
    }
    th {
      background: #eef1f8;
      text-align: left;
    }
    a {
      display: block;
      text-align: center;
      margin-top: 20px;
      font-weight: bold;
      color: #2575fc;
      text-decoration: none;
    }
    a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>

<h2>Hasil Perhitungan Sistem Antrian M/M/2</h2>

<div class="card">
  <h3>Proses Perhitungan</h3>
  <div class="mono">

    λ =
    <span class="fraction">
      <span class="top">1</span>
      <span class="bottom">{{ interarrival }}</span>
    </span>
    = {{ lam }} <br>

    μ =
    <span class="fraction">
      <span class="top">1</span>
      <span class="bottom">{{ service_time }}</span>
    </span>
    = {{ mu }} <br>

    ρ = λ / (2μ) = {{ rho }} ({{ rho_pct }}%) <br><br>

    W = 1 / (μ − λ/2) = {{ W }} menit <br>
    Wq = λ² / (2μ(μ − λ/2)) = {{ Wq }} menit

  </div>
</div>

<div class="card">
  <h3>Ringkasan Hasil</h3>
  <table>
    <tr><th>λ</th><td>{{ lam }}</td></tr>
    <tr><th>μ</th><td>{{ mu }}</td></tr>
    <tr><th>ρ</th><td>{{ rho }}</td></tr>
    <tr><th>W</th><td>{{ W }} menit</td></tr>
    <tr><th>Wq</th><td>{{ Wq }} menit</td></tr>
  </table>
</div>

<a href="/">← Kembali ke Input</a>

</body>
</html>
"""

def fmt(x, nd=6):
    return f"{x:.{nd}f}".rstrip("0").rstrip(".")

# =========================
# ROUTES
# =========================
@app.route("/", methods=["GET"])
def home():
    return render_template_string(INPUT_HTML)

@app.route("/hasil", methods=["POST"])
def hasil():
    interarrival = float(request.form["interarrival"])
    service_time = float(request.form["service_time"])

    lam = 1 / interarrival
    mu = 1 / service_time
    rho = lam / (2 * mu)

    W = 1 / (mu - lam / 2)
    Wq = (lam ** 2) / (2 * mu * (mu - lam / 2))

    return render_template_string(
        HASIL_HTML,
        interarrival=fmt(interarrival),
        service_time=fmt(service_time),
        lam=fmt(lam),
        mu=fmt(mu),
        rho=fmt(rho),
        rho_pct=fmt(rho * 100),
        W=fmt(W),
        Wq=fmt(Wq)
    )

# =========================
# RUN APP
# =========================
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
