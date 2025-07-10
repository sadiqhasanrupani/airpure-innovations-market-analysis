my_data_project/
├── data/
│   ├── raw/
│   │   ├── idsp_raw.csv           # Original, untouched data
│   │   └── aqi_raw.csv
│   └── processed/
│       ├── idsp_cleaned.csv       # Cleaned and augmented IDSP data
│       └── aqi_cleaned.csv        # Cleaned and augmented AQI data
├── notebooks/
│   ├── 01_data_ingestion.ipynb
│   ├── 02_data_cleaning.ipynb     # Jupyter notebook for cleaning process
│   ├── 03_data_augmentation.ipynb # Jupyter notebook for augmentation process
│   └── 04_exploratory_analysis.ipynb
├── src/                           # Python scripts for reusable functions
│   ├── data_cleaning_utils.py
│   └── data_augmentation_funcs.py
├── reports/
│   ├── insights_report.pdf
│   └── data_quality_report.md     # Markdown file containing issues log & documentation
├── README.md                      # Project overview, setup instructions
├── requirements.txt               # Project dependencies
└── documentation/                 # Dedicated folder for detailed docs
    └── issues_log.md              # Detailed markdown version of the issues log
    └── data_dictionary.md         # Definitions of columns, including new ones
    └── data_sources.md            # Information on where raw data came from