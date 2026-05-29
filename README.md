# Home Credit Risk Predictor

> Predict home loan repayment risk before it becomes a problem.  
> A full-stack machine learning application that scores credit risk from applicant profiles — giving lenders a probability-based view of default risk, not just a binary yes/no.

---

## What It Does

Banks and lenders face a critical challenge: **most loan applicants look similar on paper, but their repayment behaviour differs significantly.** This system goes beyond simple approval/rejection by producing a **continuous risk score (0–100%)** — the probability that an applicant will default.

```
12%  ->  Low Risk       (likely repays on time)
54%  ->  Moderate Risk  (needs closer review)
87%  ->  High Risk      (likely to default)
```

This score-based approach gives loan officers meaningful signal to act on, rather than a black-box decision.

---

## The Core Problem: Class Imbalance

The Home Credit dataset is heavily skewed:

| Class | Meaning | Share |
|-------|---------|-------|
| 0 | Non-defaulter | ~92% |
| 1 | Defaulter | ~8% |

A naive model that always predicts "safe" would be **92% accurate but completely useless**. This project addresses that with:

- Custom feature engineering that amplifies weak signals
- `class_weight="balanced"` to penalise missed defaulters more heavily
- Threshold tuning to optimise recall on the minority class
- Probability-based scoring instead of hard classification

---

## Project Structure

```
credit_risk_prediction/
│
├── backend/
│   └── main.py                    <- FastAPI prediction API
│
├── data/
│   └── application_train.csv      <- not committed (see Setup)
│
├── frontend/
│   └── app2.py                    <- Streamlit multi-step UI
│
├── models/
│   └── model_rf_v2                <- serialised Random Forest model
│
├── notebook/
│   ├── feature_engineering.py     <- custom sklearn transformer
│   └── home_credit_risk.ipynb     <- training & evaluation notebook
│
├── requirements.txt
└── README.md
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| ML Model | Random Forest (scikit-learn) |
| Feature Engineering | Custom sklearn Transformer |
| Backend API | FastAPI + Pydantic |
| Frontend | Streamlit |
| Serialisation | joblib |
| Data Processing | pandas, NumPy |

---

## Feature Engineering

Raw loan application data is sparse and noisy. A custom `FeatureEngineering` transformer (compatible with sklearn pipelines) derives richer signals before the model ever sees the data.

### Engineered Features

| Feature | Formula | What It Captures |
|---------|---------|-----------------|
| AGE | DAYS_BIRTH / 365 | Applicant maturity and stability |
| EMPLOYMENT_YEARS | DAYS_EMPLOYED / 365 | Job stability |
| CREDIT_INCOME_RATIO | AMT_CREDIT / AMT_INCOME_TOTAL | Debt burden relative to income |
| INCOME_PER_MEMBER | AMT_INCOME_TOTAL / CNT_FAM_MEMBERS | Financial pressure per dependent |
| EMI_INCOME_RATIO | AMT_ANNUITY / AMT_INCOME_TOTAL | Monthly repayment affordability |

### Category Grouping

**Organisation Type** — 58 raw categories collapsed into 7 meaningful groups:

`Government` · `Healthcare` · `Business` · `Industrial` · `Transport` · `Trade_Service` · `Finance_Telecom` · `Other`

**Income Type** — rare categories (Student, Unemployed, Businessman, Maternity leave) merged into `Other`.

### Anomaly Handling

- `DAYS_EMPLOYED = 365243` is a dataset sentinel for pensioners/non-employed — replaced with `NaN`
- `CODE_GENDER = "XNA"` replaced with `"F"` (rare encoding artefact)

---

## Model

**Random Forest Classifier** trained with:

```python
class_weight = "balanced"       # or {0: 1, 1: 4} for custom weighting
```

Output is `predict_proba()[:, 1]` — the probability of default — scaled to a 0–100% risk score.

---

## Input Features

The model accepts 17 raw applicant features:

```
NAME_CONTRACT_TYPE    CODE_GENDER         FLAG_OWN_CAR
FLAG_OWN_REALTY       CNT_CHILDREN        AMT_INCOME_TOTAL
AMT_CREDIT            AMT_ANNUITY         AMT_GOODS_PRICE
NAME_INCOME_TYPE      NAME_FAMILY_STATUS  NAME_HOUSING_TYPE
DAYS_BIRTH            DAYS_EMPLOYED       OCCUPATION_TYPE
CNT_FAM_MEMBERS       ORGANIZATION_TYPE
```

The feature engineering transformer handles all derived fields internally — the API and frontend only need to send raw values.

---

## Dataset

**Source:** [Home Credit Default Risk — Kaggle](https://www.kaggle.com/competitions/home-credit-default-risk)

Files used:

- `application_train.csv`
- `application_test.csv`
- `HomeCredit_columns_description.csv`
- `sample_submission.csv`

**Target variable:**

| Value | Meaning |
|-------|---------|
| 0 | No payment difficulty |
| 1 | Payment difficulty / default |

---

## Running the Project

### 1. Clone

```bash
git clone https://github.com/your-username/credit_risk_prediction_git.git
cd credit_risk_prediction_git
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Backend

```bash
cd backend
uvicorn main:app --reload
```

API docs available at: `http://127.0.0.1:8000/docs`

### 5. Run the Frontend

```bash
streamlit run frontend/app2.py
```

Frontend available at: `http://localhost:8501`

---

## API Reference

### POST /predict

**Request**

```json
{
  "NAME_CONTRACT_TYPE": "Cash loans",
  "CODE_GENDER": "M",
  "FLAG_OWN_CAR": "N",
  "FLAG_OWN_REALTY": "Y",
  "CNT_CHILDREN": 0,
  "AMT_INCOME_TOTAL": 300000,
  "AMT_CREDIT": 500000,
  "AMT_ANNUITY": 25000,
  "AMT_GOODS_PRICE": 600000,
  "NAME_INCOME_TYPE": "Working",
  "NAME_FAMILY_STATUS": "Married",
  "NAME_HOUSING_TYPE": "House / apartment",
  "DAYS_BIRTH": -12000,
  "DAYS_EMPLOYED": -2000,
  "OCCUPATION_TYPE": "Laborers",
  "CNT_FAM_MEMBERS": 2.0,
  "ORGANIZATION_TYPE": "Business Entity Type 3"
}
```

**Response**

```json
{
  "risk_score": 34.82
}
```

---

## Frontend Highlights

The Streamlit UI walks users through a clean 4-step flow:

```
(1) Personal Details  ->  (2) Employment  ->  (3) Loan Details  ->  (4) Risk Result
```

- Real-time EMI calculation on the loan details page
- Risk result displayed as a colour-coded score card (green / amber / red)
- Application summary with key metrics alongside the score

---

## Future Improvements

- [ ] Model calibration for better probability estimates
- [ ] Docker containerisation for one-command deployment
- [ ] Cloud deployment (AWS / GCP / Railway)
- [ ] Model monitoring and drift detection in production
- [ ] Threshold optimisation dashboard

---

## License

This project is licensed under the terms of the [LICENSE](./LICENSE) file.
