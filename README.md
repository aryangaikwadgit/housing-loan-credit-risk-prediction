# 🏠 Home Credit Risk Predictor

> Predict home loan repayment risk before it becomes a problem.  
> A full-stack machine learning application that scores credit risk from applicant profiles — giving lenders a probability-based view of default risk, not just a binary yes/no.

\---

## What It Does

Banks and lenders face a critical challenge: **most loan applicants look similar on paper, but their repayment behaviour differs significantly.** This system goes beyond simple approval/rejection by producing a **continuous risk score (0–100%)** — the probability that an applicant will default.

```
12% → ✅ Low Risk       (likely repays on time)
54% → ⚠️  Moderate Risk  (needs closer review)
87% → ❌ High Risk       (likely to default)
```

This score-based approach gives loan officers meaningful signal to act on, rather than a black-box decision.

\---

## The Core Problem: Class Imbalance

The Home Credit dataset is heavily skewed:

|Class|Meaning|Share|
|-|-|-|
|`0`|Non-defaulter|\~92%|
|`1`|Defaulter|\~8%|

A naive model that always predicts "safe" would be **92% accurate but completely useless**. This project addresses that with:

* Custom feature engineering that amplifies weak signals
* `class\_weight="balanced"` to penalise missed defaulters more heavily
* Threshold tuning to optimise recall on the minority class
* Probability-based scoring instead of hard classification

\---

## Project Structure

```
credit\_risk\_prediction/
│
├── backend/
│   └── main.py                    ← FastAPI prediction API
│
├── data/
│   └── application\_train.csv      ← not committed (see Setup)
│
├── frontend/
│   └── app2.py                    ← Streamlit multi-step UI
│
├── models/
│   └── model\_rf\_v2                ← serialised Random Forest model
│
├── notebook/
│   ├── feature\_engineering.py     ← custom sklearn transformer
│   └── home\_credit\_risk.ipynb     ← training \& evaluation notebook
│
├── requirements.txt
└── README.md
```

\---

## Tech Stack

|Layer|Technology|
|-|-|
|ML Model|Random Forest (scikit-learn)|
|Feature Engineering|Custom `sklearn` Transformer|
|Backend API|FastAPI + Pydantic|
|Frontend|Streamlit|
|Serialisation|joblib|
|Data Processing|pandas, NumPy|

\---

## Feature Engineering

Raw loan application data is sparse and noisy. A custom `FeatureEngineering` transformer (compatible with `sklearn` pipelines) derives richer signals before the model ever sees the data.

### Engineered Features

|Feature|Formula|What It Captures|
|-|-|-|
|`AGE`|`DAYS\_BIRTH / 365`|Applicant maturity \& stability|
|`EMPLOYMENT\_YEARS`|`DAYS\_EMPLOYED / 365`|Job stability|
|`CREDIT\_INCOME\_RATIO`|`AMT\_CREDIT / AMT\_INCOME\_TOTAL`|Debt burden relative to income|
|`INCOME\_PER\_MEMBER`|`AMT\_INCOME\_TOTAL / CNT\_FAM\_MEMBERS`|Financial pressure per dependent|
|`EMI\_INCOME\_RATIO`|`AMT\_ANNUITY / AMT\_INCOME\_TOTAL`|Monthly repayment affordability|

### Category Grouping

**Organisation Type** — 58 raw categories collapsed into 7 meaningful groups:

`Government` · `Healthcare` · `Business` · `Industrial` · `Transport` · `Trade\_Service` · `Finance\_Telecom` · `Other`

**Income Type** — rare categories (`Student`, `Unemployed`, `Businessman`, `Maternity leave`) merged into `Other`.

### Anomaly Handling

* `DAYS\_EMPLOYED = 365243` is a dataset sentinel for pensioners/non-employed — replaced with `NaN`
* `CODE\_GENDER = "XNA"` replaced with `"F"` (rare encoding artefact)

\---

## Model

**Random Forest Classifier** trained with:

```python
class\_weight = "balanced"       # or {0: 1, 1: 4} for custom weighting
```

Output is `predict\_proba()\[:, 1]` — the probability of default — scaled to a 0–100% risk score.

\---

## Input Features

The model accepts 17 raw applicant features:

```
NAME\_CONTRACT\_TYPE    CODE\_GENDER         FLAG\_OWN\_CAR
FLAG\_OWN\_REALTY       CNT\_CHILDREN        AMT\_INCOME\_TOTAL
AMT\_CREDIT            AMT\_ANNUITY         AMT\_GOODS\_PRICE
NAME\_INCOME\_TYPE      NAME\_FAMILY\_STATUS  NAME\_HOUSING\_TYPE
DAYS\_BIRTH            DAYS\_EMPLOYED       OCCUPATION\_TYPE
CNT\_FAM\_MEMBERS       ORGANIZATION\_TYPE
```

The feature engineering transformer handles all derived fields internally — the API and frontend only need to send raw values.

\---

## Dataset

**Source:** [Home Credit Default Risk — Kaggle](https://www.kaggle.com/competitions/home-credit-default-risk)

Files used:

* `application\_train.csv`
* `application\_test.csv`
* `HomeCredit\_columns\_description.csv`
* `sample\_submission.csv`

**Target variable:**

|Value|Meaning|
|-|-|
|`0`|No payment difficulty|
|`1`|Payment difficulty / default|

\---

## Running the Project

### 1\. Clone

```bash
git clone https://github.com/your-username/credit\_risk\_prediction\_git.git
cd credit\_risk\_prediction\_git
```

### 2\. Create Virtual Environment

```bash
python -m venv venv
venv\\Scripts\\activate        # Windows
# source venv/bin/activate   # macOS/Linux
```

### 3\. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4\. Run the Backend

```bash
cd backend
uvicorn main:app --reload
```

API docs available at: `http://127.0.0.1:8000/docs`

### 5\. Run the Frontend

```bash
streamlit run frontend/app2.py
```

Frontend available at: `http://localhost:8501`

\---

## API Reference

### `POST /predict`

**Request**

```json
{
  "NAME\_CONTRACT\_TYPE": "Cash loans",
  "CODE\_GENDER": "M",
  "FLAG\_OWN\_CAR": "N",
  "FLAG\_OWN\_REALTY": "Y",
  "CNT\_CHILDREN": 0,
  "AMT\_INCOME\_TOTAL": 300000,
  "AMT\_CREDIT": 500000,
  "AMT\_ANNUITY": 25000,
  "AMT\_GOODS\_PRICE": 600000,
  "NAME\_INCOME\_TYPE": "Working",
  "NAME\_FAMILY\_STATUS": "Married",
  "NAME\_HOUSING\_TYPE": "House / apartment",
  "DAYS\_BIRTH": -12000,
  "DAYS\_EMPLOYED": -2000,
  "OCCUPATION\_TYPE": "Laborers",
  "CNT\_FAM\_MEMBERS": 2.0,
  "ORGANIZATION\_TYPE": "Business Entity Type 3"
}
```

**Response**

```json
{
  "risk\_score": 34.82
}
```

\---

## Frontend Highlights

The Streamlit UI walks users through a clean 4-step flow:

```
① Personal Details  →  ② Employment  →  ③ Loan Details  →  ④ Risk Result
```

* Real-time EMI calculation on the loan details page
* Risk result displayed as a colour-coded score card (green / amber / red)
* Application summary with key metrics alongside the score

\---

## Future Improvements

* \[ ] SHAP explainability — show *why* a score is high or low
* \[ ] Model calibration for better probability estimates
* \[ ] Docker containerisation for one-command deployment
* \[ ] Cloud deployment (AWS / GCP / Railway)
* \[ ] Model monitoring \& drift detection in production
* \[ ] Threshold optimisation dashboard

\---

## License

This project is licensed under the terms of the [LICENSE](./LICENSE) file.

