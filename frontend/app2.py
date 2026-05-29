import streamlit as st
import requests
from datetime import date

# ─────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────
st.set_page_config(
    page_title="Home Credit Risk Predictor",
    page_icon="",
    layout="centered"
)

API_URL = "http://127.0.0.1:8000/predict"
today = date.today()

# ─────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 760px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    font-family: 'DM Serif Display', serif;
    font-weight: 400;
}

/* Page header */
.page-header {
    border-left: 3px solid #1E3A8A;
    padding-left: 14px;
    margin-bottom: 2rem;
}
.page-header h2 {
    margin: 0 0 4px 0;
    font-size: 1.6rem;
    color: #0f172a;
}
.page-header p {
    margin: 0;
    font-size: 0.88rem;
    color: #64748b;
}

/* Step indicator */
.step-bar {
    display: flex;
    align-items: center;
    gap: 0;
    margin-bottom: 2.2rem;
}
.step-item {
    display: flex;
    align-items: center;
    gap: 8px;
    flex: 1;
}
.step-circle {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 600;
    flex-shrink: 0;
}
.step-circle.done   { background: #1E3A8A; color: #fff; }
.step-circle.active { background: #3B82F6; color: #fff; }
.step-circle.pending{ background: #e2e8f0; color: #94a3b8; }
.step-label {
    font-size: 0.78rem;
    font-weight: 500;
    color: #64748b;
    white-space: nowrap;
}
.step-label.active { color: #1E3A8A; font-weight: 600; }
.step-line {
    flex: 1;
    height: 2px;
    background: #e2e8f0;
    margin: 0 6px;
}
.step-line.done { background: #1E3A8A; }

/* Section label */
.section-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 0.75rem;
    margin-top: 1.6rem;
}

/* Result card */
.result-card {
    border-radius: 12px;
    padding: 2rem 2.4rem;
    margin-top: 1rem;
    text-align: center;
    border: 1px solid transparent;
}
.result-score {
    font-family: 'DM Serif Display', serif;
    font-size: 3.8rem;
    line-height: 1;
    margin-bottom: 6px;
}
.result-label {
    font-size: 0.9rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.result-low  { background: #f0fdf4; border-color: #86efac; color: #15803d; }
.result-med  { background: #fffbeb; border-color: #fcd34d; color: #b45309; }
.result-high { background: #fef2f2; border-color: #fca5a5; color: #b91c1c; }

/* EMI callout */
.emi-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 0.9rem;
    color: #334155;
    margin-top: 0.5rem;
}
.emi-box span {
    font-family: 'DM Serif Display', serif;
    font-size: 1.3rem;
    color: #1E3A8A;
}

/* Nav buttons */
div[data-testid="column"] .stButton > button {
    width: 100%;
    border-radius: 8px;
    padding: 0.55rem 1rem;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 0.9rem;
}

/* Primary button override */
.stButton > button[kind="primary"] {
    background: #1E3A8A;
    border: none;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = 1

if "form" not in st.session_state:
    st.session_state.form = {}


# ─────────────────────────────────────
# HELPERS
# ─────────────────────────────────────
def calculate_emi(principal, roi, tenure_years):
    monthly_rate = roi / (12 * 100)
    months = tenure_years * 12
    if monthly_rate == 0:
        return principal / months
    return (
        principal * monthly_rate * ((1 + monthly_rate) ** months)
    ) / (((1 + monthly_rate) ** months) - 1)


STEPS = ["Personal", "Employment", "Loan", "Result"]

def render_steps(current):
    """Render horizontal step indicator."""
    html = '<div class="step-bar">'
    for i, label in enumerate(STEPS, 1):
        if i < current:
            circle_cls = "done"
            label_cls  = ""
            line_cls   = "done"
        elif i == current:
            circle_cls = "active"
            label_cls  = "active"
            line_cls   = ""
        else:
            circle_cls = "pending"
            label_cls  = ""
            line_cls   = ""

        html += f'''
        <div class="step-item">
            <div class="step-circle {circle_cls}">{i}</div>
            <span class="step-label {label_cls}">{label}</span>
        </div>
        '''
        if i < len(STEPS):
            html += f'<div class="step-line {line_cls}"></div>'

    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def nav_buttons(back_label=None, next_label="Next"):
    """Render back / next navigation."""
    cols = st.columns([1, 1]) if back_label else [None, st.columns(1)[0]]

    if back_label:
        with cols[0]:
            if st.button(back_label, use_container_width=True):
                st.session_state.page -= 1
                st.rerun()

    target_col = cols[1] if back_label else cols[1]
    with target_col:
        return st.button(next_label, use_container_width=True, type="primary")


# ─────────────────────────────────────
# APP TITLE
# ─────────────────────────────────────
st.markdown(
    '<h1 style="margin-bottom:0.1rem;font-size:2rem;color:#0f172a;">'
    'Home Credit Risk Predictor</h1>'
    '<p style="color:#64748b;font-size:0.9rem;margin-top:0;margin-bottom:1.8rem;">'
    'Predict home loan repayment risk using machine learning.</p>',
    unsafe_allow_html=True
)

# API status — compact badge
try:
    requests.get("http://127.0.0.1:8000", timeout=1)
    st.markdown(
        '<span style="font-size:0.78rem;color:#16a34a;font-weight:500;">'
        '&#9679; API connected</span>', unsafe_allow_html=True
    )
except Exception:
    st.markdown(
        '<span style="font-size:0.78rem;color:#dc2626;font-weight:500;">'
        '&#9679; API not reachable</span>', unsafe_allow_html=True
    )

st.write("")

render_steps(st.session_state.page)

# ─────────────────────────────────────
# PAGE 1 — PERSONAL DETAILS
# ─────────────────────────────────────
if st.session_state.page == 1:

    st.markdown('<div class="page-header"><h2>Personal Details</h2><p>Basic applicant information</p></div>', unsafe_allow_html=True)

    f = st.session_state.form

    st.markdown('<div class="section-label">Identity</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox(
            "Gender",
            ["M", "F"],
            index=["M","F"].index(f.get("gender","M"))
        )
    with col2:
        family_status = st.selectbox(
            "Family Status",
            ["Single / not married","Married","Civil marriage","Separated","Widow"],
            index=["Single / not married","Married","Civil marriage","Separated","Widow"]
                  .index(f.get("family_status","Married"))
        )

    st.markdown('<div class="section-label">Household</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        children = st.slider("Number of Children", 0, 10, f.get("children", 0))
    with col2:
        family_members = st.slider("Family Members", 1, 15, f.get("family_members", 2))

    st.markdown('<div class="section-label">Housing & Date of Birth</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        housing = st.selectbox(
            "Housing Type",
            ["House / apartment","Rented apartment","Municipal apartment",
             "With parents","Co-op apartment","Office apartment"],
            index=["House / apartment","Rented apartment","Municipal apartment",
                   "With parents","Co-op apartment","Office apartment"]
                  .index(f.get("housing","House / apartment"))
        )
    with col2:
        dob = st.date_input(
            "Date of Birth",
            value=f.get("dob", date(1985, 1, 1)),
            min_value=date(1950, 1, 1),
            max_value=today
        )

    st.write("")
    go = nav_buttons(next_label="Next  →")
    if go:
        st.session_state.form.update({
            "gender": gender,
            "family_status": family_status,
            "children": children,
            "family_members": family_members,
            "housing": housing,
            "dob": dob,
            "days_birth": -(today - dob).days
        })
        st.session_state.page = 2
        st.rerun()


# ─────────────────────────────────────
# PAGE 2 — EMPLOYMENT DETAILS
# ─────────────────────────────────────
elif st.session_state.page == 2:

    st.markdown('<div class="page-header"><h2>Employment Details</h2><p>Income and workplace information</p></div>', unsafe_allow_html=True)

    f = st.session_state.form

    INCOME_MAP = {
        "Working": "Working",
        "Commercial associate": "Commercial associate",
        "Pensioner": "Pensioner",
        "State servant": "State servant",
        "Other": "Student"
    }

    ORGANIZATION_MAP = {
        "Government": "School",
        "Healthcare": "Medicine",
        "Business": "Business Entity Type 3",
        "Trade / Service": "Trade: type 7",
        "Industrial": "Construction",
        "Transport": "Transport: type 4",
        "Finance / Telecom": "Bank",
        "Unknown": "XNA",
        "Other": "Other"
    }

    income_opts = list(INCOME_MAP.keys())
    org_opts    = list(ORGANIZATION_MAP.keys())

    occupation_opts = [
        "Laborers","Sales staff","Core staff","Managers","Drivers",
        "High skill tech staff","Accountants","Medicine staff","Security staff",
        "Cooking staff","Cleaning staff","Private service staff",
        "Low-skill Laborers","IT staff","HR staff","Realty agents"
    ]

    st.markdown('<div class="section-label">Income & Occupation</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        income_group = st.selectbox(
            "Income Type",
            income_opts,
            index=income_opts.index(f.get("income_group","Working"))
        )
        occupation = st.selectbox(
            "Occupation",
            occupation_opts,
            index=occupation_opts.index(f.get("occupation","Laborers"))
        )
    with col2:
        organization_group = st.selectbox(
            "Organization Type",
            org_opts,
            index=org_opts.index(f.get("organization_group","Business"))
        )
        annual_income = st.number_input(
            "Annual Income (INR)",
            min_value=10_000,
            value=f.get("annual_income", 300_000),
            step=10_000
        )

    st.markdown('<div class="section-label">Employment Duration</div>', unsafe_allow_html=True)
    employment_date = st.date_input(
        "Employment Start Date",
        value=f.get("employment_date", date(2015, 1, 1)),
        min_value=date(1980, 1, 1),
        max_value=today
    )

    st.write("")
    go = nav_buttons(back_label="← Back", next_label="Next  →")
    if go:
        st.session_state.form.update({
            "income_group": income_group,
            "income_type": INCOME_MAP[income_group],
            "occupation": occupation,
            "organization_group": organization_group,
            "organization": ORGANIZATION_MAP[organization_group],
            "annual_income": annual_income,
            "employment_date": employment_date,
            "days_employed": -(today - employment_date).days
        })
        st.session_state.page = 3
        st.rerun()


# ─────────────────────────────────────
# PAGE 3 — LOAN DETAILS
# ─────────────────────────────────────
elif st.session_state.page == 3:

    st.markdown('<div class="page-header"><h2>Loan Details</h2><p>Credit and property information</p></div>', unsafe_allow_html=True)

    f = st.session_state.form

    st.markdown('<div class="section-label">Contract & Assets</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        contract_type = st.selectbox(
            "Contract Type",
            ["Cash loans","Revolving loans"],
            index=["Cash loans","Revolving loans"]
                  .index(f.get("contract_type","Cash loans"))
        )
    with col2:
        own_car = st.radio(
            "Own Car?",
            ["Y","N"],
            index=["Y","N"].index(f.get("own_car","N")),
            horizontal=True
        )
    with col3:
        own_realty = st.radio(
            "Own Property?",
            ["Y","N"],
            index=["Y","N"].index(f.get("own_realty","N")),
            horizontal=True
        )

    st.markdown('<div class="section-label">Financials</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        loan_amount = st.number_input(
            "Loan Amount (INR)",
            min_value=10_000,
            value=f.get("loan_amount", 500_000),
            step=10_000
        )
        roi = st.slider(
            "Interest Rate (%)",
            1.0, 20.0,
            f.get("roi", 8.5),
            step=0.1
        )
    with col2:
        goods_price = st.number_input(
            "Property Price (INR)",
            min_value=10_000,
            value=f.get("goods_price", 600_000),
            step=10_000
        )
        tenure = st.slider(
            "Loan Tenure (Years)",
            1, 35,
            f.get("tenure", 20)
        )

    emi = calculate_emi(loan_amount, roi, tenure)
    st.markdown(
        f'<div class="emi-box">Estimated Monthly EMI &nbsp; '
        f'<span>INR {emi:,.0f}</span></div>',
        unsafe_allow_html=True
    )

    st.write("")
    go = nav_buttons(back_label="← Back", next_label="Predict Risk")
    if go:
        st.session_state.form.update({
            "contract_type": contract_type,
            "own_car": own_car,
            "own_realty": own_realty,
            "loan_amount": loan_amount,
            "goods_price": goods_price,
            "roi": roi,
            "tenure": tenure,
            "emi": emi
        })
        st.session_state.page = 4
        st.rerun()


# ─────────────────────────────────────
# PAGE 4 — RESULT
# ─────────────────────────────────────
elif st.session_state.page == 4:

    st.markdown('<div class="page-header"><h2>Risk Assessment</h2><p>ML model prediction result</p></div>', unsafe_allow_html=True)

    f = st.session_state.form

    payload = {
        "NAME_CONTRACT_TYPE":  f["contract_type"],
        "CODE_GENDER":         f["gender"],
        "FLAG_OWN_CAR":        f["own_car"],
        "FLAG_OWN_REALTY":     f["own_realty"],
        "CNT_CHILDREN":        f["children"],
        "AMT_INCOME_TOTAL":    float(f["annual_income"]),
        "AMT_CREDIT":          float(f["loan_amount"]),
        "AMT_ANNUITY":         float(f["emi"]),
        "AMT_GOODS_PRICE":     float(f["goods_price"]),
        "NAME_INCOME_TYPE":    f["income_type"],
        "NAME_FAMILY_STATUS":  f["family_status"],
        "NAME_HOUSING_TYPE":   f["housing"],
        "DAYS_BIRTH":          f["days_birth"],
        "DAYS_EMPLOYED":       f["days_employed"],
        "OCCUPATION_TYPE":     f["occupation"],
        "CNT_FAM_MEMBERS":     float(f["family_members"]),
        "ORGANIZATION_TYPE":   f["organization"]
    }

    with st.spinner("Running prediction..."):
        try:
            response = requests.post(API_URL, json=payload, timeout=10)

            if response.status_code == 200:
                result     = response.json()
                risk_score = result.get("risk_score", 0)

                # Determine bucket purely from score
                if risk_score < 35:
                    card_cls   = "result-low"
                    risk_label = "Low Risk"
                elif risk_score < 65:
                    card_cls   = "result-med"
                    risk_label = "Moderate Risk"
                else:
                    card_cls   = "result-high"
                    risk_label = "High Risk"

                st.markdown(
                    f'''
                    <div class="result-card {card_cls}">
                        <div class="result-score">{risk_score}%</div>
                        <div class="result-label">{risk_label}</div>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )

                # Summary row
                st.write("")
                st.markdown('<div class="section-label">Application Summary</div>', unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                c1.metric("Loan Amount",   f"INR {f['loan_amount']:,}")
                c2.metric("Monthly EMI",   f"INR {f['emi']:,.0f}")
                c3.metric("Annual Income", f"INR {f['annual_income']:,}")

            else:
                st.error(f"API error {response.status_code}: {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the FastAPI server. Make sure it is running on port 8000.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Loan Details", use_container_width=True):
            st.session_state.page = 3
            st.rerun()
            
    with col2:
        if st.button("Start New Application", use_container_width=True, type="primary"):
            st.session_state.page = 1
            st.session_state.form = {}
            st.rerun()