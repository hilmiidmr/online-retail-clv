# Online Retail II — CLV Analytics Project

## English
This project delivers end-to-end customer analytics and CLV (Customer Lifetime Value) modeling on the Online Retail II (UCI) dataset. The results are summarized in a Streamlit dashboard designed for a professional data science presentation.

### Project Goal
Understand customer behavior, build RFM segments, analyze retention, and estimate 12‑month revenue-based CLV to support business decisions.

### Workflow
1. Data cleaning and EDA
2. RFM segmentation
3. Cohort and retention analysis
4. BG/NBD + Gamma-Gamma CLV modeling
5. Exporting dashboard-ready datasets

### Notebooks
- `notebooks/01_eda_rfm.ipynb` — Data cleaning, EDA, RFM segmentation
- `notebooks/02_cohort_retention.ipynb` — Cohort and retention analysis (customer and revenue)
- `notebooks/03_clv_modeling.ipynb` — CLV modeling and segment-level outputs

### Streamlit Dashboard
The dashboard presents a clean story flow:
- Overview KPIs and insights
- Performance (revenue, orders, AOV, geography)
- Retention (cohort heatmaps and average curve)
- Segments (CLV and RFM views)
- Customers (filtered CLV table)
- CLV distribution

#### Live Dashboard Link
https://online-retail-clv.streamlit.app/

### Setup
1. Create and activate a virtual environment.
2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Run with Docker

Requires [Docker Desktop](https://www.docker.com/products/docker-desktop/).

1. Clone the repository and open a terminal in the project root.
2. Start the Streamlit dashboard and Jupyter Lab:

```bash
docker compose up --build -d
```

3. Open in your browser:
   - **Dashboard:** http://localhost:8502
   - **Jupyter Lab:** http://localhost:8889/lab

4. Stop services:

```bash
docker compose down
```

### Data
The raw dataset is not included in the repository.

Source:
https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci/data

Place the file here:
`data/online_retail_II.csv`

If the file name is different, rename it or update the notebook path.

### Export Dashboard Data
After running the notebooks, export summary data for the dashboard:
```bash
python app/export_dashboard_data.py
```

Generated files:
- `data/clv_predictions.parquet`
- `data/segment_summary.csv`
- `data/rfm_segment_summary.csv`
- `data/monthly_kpis.csv`
- `data/country_revenue.csv`
- `data/cohort_retention_customers.csv`
- `data/cohort_retention_revenue.csv`
- `data/cohort_size.csv`
- `data/cohort_avg_retention.csv`
- `data/coverage_stats.json`

### Run the Dashboard
```bash
streamlit run app/app.py
```

### Tech Stack
Python, Pandas, NumPy, Matplotlib/Seaborn, Lifetimes (CLV), Streamlit, Altair, Docker, Docker Compose

---

## Türkçe
Bu proje, Online Retail II (UCI) verisi üzerinde uçtan uca müşteri analitiği ve CLV (Müşteri Yaşam Boyu Değeri) modellemesi yapar. Sonuçlar, profesyonel bir veri bilimi sunumu formatında hazırlanmış Streamlit dashboardunda özetlenir.

### Proje Hedefi
Müşteri davranışını anlamak, RFM segmentleri oluşturmak, elde tutma analizi yapmak ve 12 aylık gelir bazlı CLV tahminleriyle iş kararlarını desteklemek.

### Proje Akışı
1. Veri temizleme ve EDA
2. RFM segmentasyonu
3. Kohort ve elde tutma analizi
4. BG/NBD + Gamma-Gamma ile CLV modelleme
5. Dashboard için özet veri setlerinin export edilmesi

### Notebooklar
- `notebooks/01_eda_rfm.ipynb` — Veri temizleme, EDA, RFM segmentasyonu
- `notebooks/02_cohort_retention.ipynb` — Kohort ve elde tutma analizi (müşteri ve gelir)
- `notebooks/03_clv_modeling.ipynb` — CLV modelleme ve segment çıktıları

### Streamlit Dashboard
Dashboard, iş tarafı için sade ve anlaşılır bir hikaye akışı sunar:
- Özet KPI ve içgörüler
- Performans (gelir, sipariş, AOV, ülke kırılımı)
- Elde tutma (cohort heatmap ve ortalama eğri)
- Segmentler (CLV ve RFM görünümü)
- Müşteriler (filtrelenebilir CLV tablosu)
- CLV dağılımı

#### Canlı Dashboard Linki
https://online-retail-clv.streamlit.app/

### Kurulum
1. Sanal ortam oluşturup aktif edin.
2. Gereksinimleri yükleyin:
```bash
pip install -r requirements.txt
```

### Docker ile çalıştırma

[Docker Desktop](https://www.docker.com/products/docker-desktop/) kurulu olmalıdır.

1. Repoyu klonlayın ve proje kökünde terminal açın.
2. Streamlit dashboard ve Jupyter Lab'i başlatın:

```bash
docker compose up --build -d
```

3. Tarayıcıda açın:
   - **Dashboard:** http://localhost:8502
   - **Jupyter Lab:** http://localhost:8889/lab

4. Durdurmak için:

```bash
docker compose down
```

### Veri
Ham veri dosyası repoda yoktur.

Kaynak:
https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci/data

Dosyayı buraya koyun:
`data/online_retail_II.csv`

Dosya adı farklıysa yeniden adlandırın veya notebook pathini güncelleyin.

### Dashboard Verisini Üretme
Notebookları çalıştırdıktan sonra dashboard için özet veri dosyalarını üretin:
```bash
python app/export_dashboard_data.py
```

Üretilen dosyalar:
- `data/clv_predictions.parquet`
- `data/segment_summary.csv`
- `data/rfm_segment_summary.csv`
- `data/monthly_kpis.csv`
- `data/country_revenue.csv`
- `data/cohort_retention_customers.csv`
- `data/cohort_retention_revenue.csv`
- `data/cohort_size.csv`
- `data/cohort_avg_retention.csv`
- `data/coverage_stats.json`

### Dashboard Çalıştırma
```bash
streamlit run app/app.py
```

### Tech Stack
Python, Pandas, NumPy, Matplotlib/Seaborn, Lifetimes (CLV), Streamlit, Altair, Docker, Docker Compose
