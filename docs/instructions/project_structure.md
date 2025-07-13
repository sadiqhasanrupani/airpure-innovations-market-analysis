## ✅ **Recommended Folder Structure**

```
AIRPURE_INNOVATIONS/
│
├── data/
│   ├── raw/                             # Unmodified original files
│   │   ├── aqi.csv
│   │   ├── idsp.csv
│   │   ├── population_projection.csv
│   │   ├── vahan.csv
│   │   └── AirPure Innovations.csv
│   ├── processed/                       # Cleaned and feature-engineered files
│   └── external/                        # Any external data you add (e.g. Google Trends, EV data)
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb           # Data cleaning and formatting
│   ├── 02_feature_engineering.ipynb     # Derived features like AQI severity, weekend flag, etc.
│   ├── 03_analysis_primary.ipynb        # Answers to primary analysis questions
│   ├── 04_analysis_secondary.ipynb      # Answers to secondary analysis questions
│   └── 05_eda_summary.ipynb             # Overview / dashboard exploration
│
├── src/
│   ├── data/                            # Data loading and preprocessing functions
│   │   └── load_data.py
│   └── utils/                           # Common utility functions (e.g., AQI categorization)
│       └── helpers.py
│
├── PowerBI/
│   └── AirPure Innovations.pbix         # Power BI Dashboard file
│
├── docs/
│   ├── problem_statement.pdf
│   ├── evaluation_criteria.pdf
│   ├── Primary_and_Secondary_Analysis.pdf
│   └── video_presentation_background_img.jpg
│
├── presentation/
│   ├── AirPure_Presentation.pptx        # Final slide deck
│   ├── PRD_AirPurifier.docx             # Product Requirements Document
│   └── script.md                        # Script or notes for video recording
│
├── README.md                            # Overview of the project
├── requirements.txt                     # Python dependencies
└── .gitignore                           # Ignore checkpoints, pbix cache, etc.
```

---

## 🧠 Why this Structure?

| Folder          | Purpose                                                                |
| --------------- | ---------------------------------------------------------------------- |
| `data/`         | Keep raw, cleaned, and external data separate for reproducibility      |
| `notebooks/`    | Logical pipeline from cleaning → feature engineering → insights        |
| `src/`          | Makes your code modular, reusable (e.g. custom `load_data()` function) |
| `PowerBI/`      | Dedicated to Power BI assets                                           |
| `presentation/` | All final deliverables in one place                                    |
| `docs/`         | All reference materials & PDFs from Codebasics                         |
| `README.md`     | Explain what this project is about (required for GitHub!)              |

---

## ✨ Bonus: Professional `README.md` Template

```markdown
# 🚀 AirPure Innovations - Market Fit Research (Codebasics Resume Project)

## 🧠 Project Overview

This project aims to identify market fit for AirPure Innovations' air purifier using AQI analytics and public health data from India.

**Challenge Role**: Peter Pandey (Data Analyst)  
**Company**: AirPure Innovations  
**Guided by**: COO Tony Sharma  

## 🎯 Goals

- Identify cities with high and sustained pollution
- Correlate pollution with public health impact
- Analyze consumer demand triggers for air purifiers

## 📊 Tools Used

- Python (Pandas, NumPy, Seaborn)
- Power BI (Dashboard)
- External sources (Google Trends, EV data)

## 📁 Folder Structure

```

AIRPURE\_INNOVATIONS/
├── data/
├── notebooks/
├── src/
├── PowerBI/
├── presentation/
├── docs/

```

## 📌 Key Deliverables

- 🔍 Primary & Secondary Question Analysis
- 📊 Power BI Dashboard with city risk score
- 📄 Product Requirements Document
- 🎥 [Video Presentation](your_youtube_link_here)
- 🔗 [LinkedIn Post](your_post_link_here)

## ✍️ Author

Sadiqhasan Rupani  
[LinkedIn](https://linkedin.com/in/sadiqhasanrupani) • [GitHub](https://github.com/sadiqhasanrupani)
```