import streamlit as st
import plotly.express as px
from fpdf import FPDF

# ---- Custom Page Config ----
st.set_page_config(page_title="Zakat Calculator", page_icon="🕌", layout="wide")

# ---- Header ----
st.title("📿 بسم الله الرحمن الرحيم")
st.header("Zakat Calculator - حساب الزكاة")
st.subheader("🕌 Calculate your Zakat and fulfill your obligation")

# ---- Sidebar Inputs ----
st.sidebar.header("📊 Enter Your Assets")
cash = st.sidebar.number_input("💵 Cash in Hand (PKR)", min_value=0.0)
gold_tola = st.sidebar.number_input("🪙 Gold (Tola)", min_value=0.0)
silver_tola = st.sidebar.number_input("🔗 Silver (Tola)", min_value=0.0)
assets = st.sidebar.number_input("🏠 Other Assets (PKR)", min_value=0.0)

# ---- Gold & Silver Prices ----
gold_price_per_gram = 17000  # Price per gram
silver_price_per_gram = 200

gold_grams = gold_tola * 11.664  # Convert to grams
silver_grams = silver_tola * 11.664  # Convert to grams

gold_value = gold_grams * gold_price_per_gram
silver_value = silver_grams * silver_price_per_gram

total_wealth = gold_value + silver_value + cash + assets

# ---- Nisab Thresholds ----
gold_nisab = 7.5 * 11.664 * gold_price_per_gram  # 7.5 Tola Gold
silver_nisab = 52.5 * 11.664 * silver_price_per_gram  # 52.5 Tola Silver
cash_nisab = 100000  # 1 Lakh PKR

# ---- Zakat Calculation ----
if gold_tola >= 7.5 or silver_tola >= 52.5 or cash >= 100000:
    zakat = total_wealth * 0.025
    st.metric("🕌 Zakat Payable", f"PKR {zakat:,.2f}")
    st.markdown("🤲 **Give Zakat to those in need. May Allah bless you!**")
else:
    zakat = 0
    st.markdown("❌ **Your wealth is below the Nisab threshold. No Zakat is due.**")

# ---- Wealth Breakdown ----
st.write("### 📊 Wealth Breakdown:")
st.write(f"**Gold Value:** {gold_tola} Tola → PKR {gold_value:,.2f}")
st.write(f"**Silver Value:** {silver_tola} Tola → PKR {silver_value:,.2f}")
st.write(f"**Cash:** PKR {cash:,.2f}")
st.write(f"**Other Assets:** PKR {assets:,.2f}")

# ---- Pie Chart ----
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
st.write("📚 **Learn more about Zakat:** [Zakat Calculator](https://www.islamic-relief.org/zakat/zakat-calculator/)")