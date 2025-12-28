# Online Retail II — CLV Project

End-to-end customer analytics on **Online Retail II (UCI)**: data cleaning, EDA, RFM segmentation, cohort retention, and CLV modeling.

## Project Goal
Build a customer-level understanding of purchasing behavior and prepare features for CLV modeling.

## Notebooks
- `notebooks/01_eda_rfm.ipynb` — EDA + RFM segmentation (CLV prep)
- `notebooks/02_cohort_retention.ipynb` — cohort & retention analysis (planned)
- `notebooks/03_clv_modeling.ipynb` — CLV modeling (planned)

## Data
The raw dataset is **not included** in this repository (file size).

Source (Kaggle):
https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci/data

To run the notebooks:
1. Download the dataset from Kaggle
2. Place it here: `data/online_retail_II.csv`

> If the downloaded file name is different, rename it to `online_retail_II.csv` (or update the path inside the notebook).

## Tech Stack
Python, Pandas, Matplotlib/Seaborn
