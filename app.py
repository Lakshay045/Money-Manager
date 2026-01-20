# =====================================================
# IMPORTS
# =====================================================
import pdfplumber
import pandas as pd
import plotly.express as px
import streamlit as st
import tempfile
import re

APP_PASSWORD = "Lakshay@2193"  # apna strong password rakh

pwd = st.text_input("🔐 Enter Password", type="password")

if pwd != APP_PASSWORD:
    st.stop()


# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="Personal Money Manager", layout="wide")
st.title("💰 Personal Money Manager")
st.caption("Complete A–Z Personal Finance Analyzer (Local & Secure)")

st.markdown("""
<style>
/* App background */
.stApp {
    background-color: #0b0f19;
    color: #e6e6eb;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Headings */
h1, h2, h3 {
    color: #f9fafb;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #1f2933, #111827);
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}

/* Metric labels */
[data-testid="stMetricLabel"] {
    color: #9ca3af;
}

/* Metric values */
[data-testid="stMetricValue"] {
    color: #38bdf8;
    font-size: 28px;
}

/* Tables */
[data-testid="stDataFrame"] {
    background-color: #020617;
    border-radius: 14px;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #2563eb, #1e40af);
    color: white;
    border-radius: 12px;
    padding: 0.6em 1.2em;
    border: none;
    font-weight: 600;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #1d4ed8, #1e3a8a);
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# THEME TOGGLE
# =====================================================
# st.sidebar.header("🎨 Appearance")
# theme = st.sidebar.radio("Theme", ["Light", "Dark"])

# if theme == "Dark":
#     st.markdown("""
#     <style>
#     .stApp { background-color: #0E1117; color: #FAFAFA; }
#     </style>
#     """, unsafe_allow_html=True)

# =====================================================
# FILE UPLOAD
# =====================================================
uploaded_file = st.file_uploader("📄 Upload Kotak Bank Statement (PDF)", type=["pdf"])

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getbuffer())
        pdf_path = tmp.name
else:
    st.info("Please upload a PDF statement to continue.")
    st.stop()

# =====================================================
# HELPER FUNCTIONS
# =====================================================
def clean_number(v):
    if v is None:
        return None
    v = v.replace(",", "").strip()
    if v == "" or not v.replace(".", "").isdigit():
        return None
    return float(v)

def get_category(desc):
    if not isinstance(desc, str):
        return "Other"

    d = desc.lower()

    # ---------- FIXED OBLIGATIONS ----------
    if any(x in d for x in ["emi", "installment"]):
        return "EMI"

    if any(x in d for x in ["rent", "pg", "hostel"]):
        return "Rent"

    if any(x in d for x in ["insurance", "policy", "premium"]):
        return "Insurance"

    # ---------- SUBSCRIPTIONS ----------
    if any(x in d for x in [
        "netflix", "spotify", "prime", "hotstar",
        "subscription", "google one", "icloud"
    ]):
        return "Subscription"

    # ---------- FOOD & LIFESTYLE ----------
    if any(x in d for x in ["swiggy", "zomato", "restaurant", "food", "cafe"]):
        return "Food"

    if any(x in d for x in ["blinkit", "zepto", "instamart", "grocery"]):
        return "Groceries"

    # ---------- SHOPPING ----------
    if any(x in d for x in ["amazon", "flipkart", "myntra", "ajio"]):
        return "Online Shopping"

    if any(x in d for x in ["mall", "store", "retail"]):
        return "Offline Shopping"

    # ---------- TRAVEL ----------
    if any(x in d for x in ["uber", "ola", "rapido"]):
        return "Cab / Travel"

    if any(x in d for x in ["irctc", "rail", "metro", "bus"]):
        return "Public Transport"

    if any(x in d for x in ["hotel", "oyo", "makemytrip"]):
        return "Stay / Hotels"

    # ---------- UTILITIES ----------
    if any(x in d for x in ["electricity", "water", "gas", "bill", "recharge"]):
        return "Utilities"

    if any(x in d for x in ["wifi", "broadband", "internet", "jio", "airtel"]):
        return "Internet / Mobile"

    # ---------- FINANCIAL ----------
    if any(x in d for x in ["navi", "loan", "finance", "credit card"]):
        return "Loan / Finance"

    if any(x in d for x in ["investment", "mutual fund", "sip"]):
        return "Investments"

    # ---------- TRANSFERS ----------
    if any(x in d for x in ["upi", "imps", "neft", "rtgs"]):
        return "UPI / Bank Transfer"

    # ---------- DEFAULT ----------
    return "Other"



def extract_merchant(desc):
    if not isinstance(desc, str):
        return "Unknown"
    d = desc.upper()

    d = re.sub(r"UPI/|IMPS/|NEFT/|/\d+|\(VALUE DATE.*?\)", "", d)
    d = re.sub(r"\s+", " ", d).strip()
    return d.split("/")[0][:25]

# =====================================================
# PDF PARSING
# =====================================================
rows = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                if not row or len(row) < 6:
                    continue
                date = row[1]
                desc = row[2]
                wd = clean_number(row[4])
                cr = clean_number(row[5])

                if wd is not None:
                    amt = -wd
                elif cr is not None:
                    amt = cr
                else:
                    continue

                rows.append([date, desc, amt])

df = pd.DataFrame(rows, columns=["Date", "Description", "Amount"])
df["Date"] = pd.to_datetime(
    df["Date"],
    dayfirst=True,
    errors="coerce"
)

df = df.dropna(subset=["Date"])


# =====================================================
# INTELLIGENCE LAYER
# =====================================================
df["Category"] = df["Description"].apply(get_category)
df["Merchant"] = df["Description"].apply(extract_merchant)

# =====================================================
# SIDEBAR FILTERS
# =====================================================
if df.empty:
    st.error("❌ No valid transactions found in this PDF")
    st.stop()

st.sidebar.header("🔍 Filters")
# =========================
# ADVANCED SEARCH INPUT
# =========================
st.sidebar.subheader("🔎 Advanced Search")

search_query = st.sidebar.text_input(
    "Search by name, merchant, category, keyword",
    placeholder="e.g. Aarav, Swiggy, EMI, Rent",
    key="advanced_search_input"
)



min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

start, end = st.sidebar.date_input(
    "Date Range",
    value=[min_date, max_date]
)


df = df[(df["Date"] >= pd.to_datetime(start)) & (df["Date"] <= pd.to_datetime(end))]



cat = st.sidebar.selectbox("Category", ["All"] + sorted(df["Category"].unique()))
# =====================================================
# SIDEBAR SEARCH (PEHLE)
# =====================================================
st.sidebar.subheader("🔎 Advanced Search")

search_query = st.sidebar.text_input(
    "Search by name, merchant, category, keyword",
    placeholder="e.g. Aarav, Swiggy, EMI, Rent",
    key="advanced_search"
)

# =====================================================
# APPLY CATEGORY FILTER
# =====================================================
if cat != "All":
    df = df[df["Category"] == cat]

# =====================================================
# APPLY ADVANCED SEARCH FILTER
# =====================================================
if search_query:
    q = search_query.lower().strip()

    df = df[
        df["Description"].fillna("").str.lower().str.contains(q)
        | df["Merchant"].fillna("").str.lower().str.contains(q)
        | df["Category"].fillna("").str.lower().str.contains(q)
    ]

# =====================================================
# EMPTY RESULT GUARD
# =====================================================
if df.empty:
    st.warning("🔍 No transactions match your search / filter.")
    st.stop()




# =====================================================
# ANALYTICS
# =====================================================
summary = (
    df[df["Amount"] < 0]
    .groupby("Category")["Amount"]
    .sum()
    .abs()
    .reset_index()
    .sort_values("Amount", ascending=False)
)

daily = (
    df[df["Amount"] < 0]
    .groupby("Date")["Amount"]
    .sum()
    .abs()
    .reset_index()
)

total_spend = df[df["Amount"] < 0]["Amount"].abs().sum()
avg_daily = daily["Amount"].mean()
top_category = summary.iloc[0]["Category"] if not summary.empty else "N/A"

# =========================
# INCOME vs EXPENSE
# =========================
total_income = df[df["Amount"] > 0]["Amount"].sum()
total_expense = df[df["Amount"] < 0]["Amount"].abs().sum()

net_savings = total_income - total_expense

if total_income > 0:
    savings_percent = (net_savings / total_income) * 100
else:
    savings_percent = 0


# =====================================================
# ADVANCED FEATURES
# =====================================================
# Recurring merchants
recurring = (
    df[df["Amount"] < 0]
    .groupby("Merchant")["Amount"]
    .count()
    .reset_index(name="TxnCount")
    .query("TxnCount >= 3")
)

# Small spend leakage
small_spends = df[(df["Amount"] < 0) & (df["Amount"].abs() <= 50)]
small_total = small_spends["Amount"].abs().sum()
cashflow_df = pd.DataFrame({
    "Type": ["Income", "Expense"],
    "Amount": [total_income, total_expense]
})

fig_cash = px.bar(
    cashflow_df,
    x="Type",
    y="Amount",
    text_auto=True,
    title="Income vs Expense"
)

fig_cash.update_layout(
    paper_bgcolor="#0b0f19",
    plot_bgcolor="#0b0f19",
    font_color="#e5e7eb"
)

st.plotly_chart(fig_cash, width="stretch")

# Top merchants
top_merchants = (
    df[df["Amount"] < 0]
    .groupby("Merchant")["Amount"]
    .sum()
    .abs()
    .reset_index()
    .sort_values("Amount", ascending=False)
    .head(5)
)

# =====================================================
# DASHBOARD KPIs
# =====================================================
st.markdown("## 📌 Overview")
st.caption("High-level snapshot of your financial behaviour")

st.divider()
c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Total Income", f"₹{total_income:.2f}")
c2.metric("💸 Total Expense", f"₹{total_expense:.2f}")
c3.metric("💾 Net Savings", f"₹{net_savings:.2f}")
c4.metric("📈 Savings %", f"{savings_percent:.1f}%")


# =====================================================
# GRAPHS
# =====================================================
st.divider()
fig1 = px.pie(summary, names="Category", values="Amount", hole=0.4)


fig2 = px.bar(summary, x="Category", y="Amount", text_auto=True)

st.plotly_chart(fig1, width="stretch")
st.plotly_chart(fig2, width="stretch")
for fig in [fig1, fig2]:
    fig.update_layout(
        paper_bgcolor="#0b0f19",
        plot_bgcolor="#0b0f19",
        font_color="#e5e7eb"
    )


# =====================================================
# TABLES
# =====================================================
st.divider()
st.subheader("✏️ Edit Transactions (Category / Merchant / Notes)")
# ✅ Apply edited data as source of truth



editable_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="dynamic",
    column_config={
        "Category": st.column_config.SelectboxColumn(
            "Category",
            options=[
                "Food",
                "Travel",
                "Shopping",
                "UPI Transfer",
                "Loan / EMI",
                "Bills",
                "Entertainment",
                "Other",
            ],
        ),
        "Merchant": st.column_config.TextColumn(
            "Merchant",
            help="Edit merchant name if auto-detected wrong"
        ),
        "Description": st.column_config.TextColumn(
            "Description",
            disabled=True
        ),
        "Amount": st.column_config.NumberColumn(
            "Amount",
            disabled=True
        ),
        "Date": st.column_config.DateColumn(
            "Date",
            disabled=True
        ),
    },
    key="transaction_editor"
)


st.subheader("🏪 Top Merchants")
st.dataframe(top_merchants, use_container_width=True)

if not recurring.empty:
    st.subheader("🔁 Recurring Transactions")
    st.dataframe(recurring, use_container_width=True)

# =====================================================
# INSIGHTS
# =====================================================
st.divider()
st.subheader("🧠 Key Insights")

st.write(f"• Total spending is ₹{total_spend:.2f}")
st.write(f"• Highest spending category is {top_category}")
st.write(f"• Average daily spend is ₹{avg_daily:.2f}")

if not recurring.empty:
    st.write(f"• {recurring.iloc[0]['Merchant']} is a recurring merchant")

if small_total > 0:
    st.warning(f"⚠️ Small spends ≤₹50 total ₹{small_total:.2f} (silent leakage)")

# =====================================================
# EXPORT (EXCEL)
# =====================================================
st.divider()
st.subheader("⬇️ Export Report")

@st.cache_data
def export_excel(df, summary):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        with pd.ExcelWriter(tmp.name, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Transactions")
            summary.to_excel(writer, index=False, sheet_name="Category Summary")
        return tmp.name

if st.button("📊 Download Excel Report"):
    path = export_excel(df, summary)
    with open(path, "rb") as f:
        st.download_button(
            "⬇️ Click to Download",
            f,
            file_name="Money_Manager_Report.xlsx"
        )


