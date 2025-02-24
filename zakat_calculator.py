import streamlit as st
import plotly.express as px
from fpdf import FPDF

# ---- Custom Page Config ----
st.set_page_config(page_title="Zakat Calculator", page_icon="🕌", layout="wide")

# ---- Custom Styling ----
st.markdown("""
    <style>
    body {background-color: #121212; color: white;}
    .title {text-align: center; font-size: 40px; font-weight: bold; color: #003593;}
    .subtitle {text-align: center; font-size: 20px; color: #888000;}
    .note {text-align: center; font-size: 18px; color: #FFFFFF; font-style: italic;}
    .highlight {color: #FF4500; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

# ---- Header ----
st.markdown('<p class="title">📿 بسم الله الرحمن الرحيم</p>', unsafe_allow_html=True)
st.markdown('<p class="title">Zakat Calculator - حساب الزكاة</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">🕌 Calculate your Zakat and fulfill your obligation</p>', unsafe_allow_html=True)

# ---- Sidebar Inputs ----
st.sidebar.header("📊 Enter Your Assets")
cash = st.sidebar.number_input("💵 Cash in Hand (PKR)", min_value=0.0)
gold_tola = st.sidebar.number_input("🪙 Gold (Tola)", min_value=0.0)  # Tola Input
silver_tola = st.sidebar.number_input("🔗 Silver (Tola)", min_value=0.0)  # Tola Input
assets = st.sidebar.number_input("🏠 Other Assets (PKR)", min_value=0.0)

# ---- Gold & Silver Calculation ----
gold_price_per_gram = 17000  # Price per gram
silver_price_per_gram = 200

gold_grams = gold_tola * 11.664  # Convert to grams
silver_grams = silver_tola * 11.664  # Convert to grams

gold_value = gold_grams * gold_price_per_gram
silver_value = silver_grams * silver_price_per_gram

# ---- Zakat Calculation ----
nisab = min(87.48 * gold_price_per_gram, 612.36 * silver_price_per_gram)
total_wealth = gold_value + silver_value + cash + assets
zakat = total_wealth * 0.025 if total_wealth >= nisab else 0

# ---- Display Result ----
st.metric("💰 Total Wealth", f"PKR {total_wealth:,.2f}")

if zakat > 0:
    st.metric("🕌 Zakat Payable", f"PKR {zakat:,.2f}")
    st.markdown('<p class="note">🤲 Give Zakat to those in need. May Allah bless you!</p>', unsafe_allow_html=True)
else:
    st.markdown('<p class="note"><span class="highlight">❌ Your wealth is below the Nisab threshold. No Zakat is due.</span></p>', unsafe_allow_html=True)

# ---- Breakdown Table ----
st.write("### 📊 Wealth Breakdown:")
st.write(f"**Gold Value:** {gold_tola} Tola → PKR {gold_value:,.2f}")
st.write(f"**Silver Value:** {silver_tola} Tola → PKR {silver_value:,.2f}")
st.write(f"**Cash:** PKR {cash:,.2f}")
st.write(f"**Other Assets:** PKR {assets:,.2f}")

# ---- Pie Chart for Wealth Breakdown ----
fig = px.pie(values=[cash, gold_value, silver_value, assets],
             names=["Cash", "Gold", "Silver", "Other Assets"],
             title="Wealth Distribution")
st.plotly_chart(fig)

# ---- PDF Report Generation ----
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Zakat Calculation Report", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Gold ({gold_tola} Tola): PKR {gold_value:,.2f}", ln=True)
    pdf.cell(200, 10, f"Silver ({silver_tola} Tola): PKR {silver_value:,.2f}", ln=True)
    pdf.cell(200, 10, f"Cash: PKR {cash:,.2f}", ln=True)
    pdf.cell(200, 10, f"Other Assets: PKR {assets:,.2f}", ln=True)
    pdf.cell(200, 10, f"Total Wealth: PKR {total_wealth:,.2f}", ln=True)
    pdf.cell(200, 10, f"Zakat Payable: PKR {zakat:,.2f}", ln=True)
    pdf.output("Zakat_Report.pdf")

if st.button("📄 Download PDF Report"):
    generate_pdf()
    st.success("✅ Report Generated! Check your folder.")

st.write("💡 **Pay your Zakat on time & help those in need!** 🤲")

