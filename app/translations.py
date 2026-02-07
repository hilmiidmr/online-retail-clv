# Dashboard UI strings: en (English) and tr (Turkish)
# Written for a non-technical audience (presentation / storytelling).

TRANSLATIONS = {
    "en": {
        "page_overview": "Overview",
        "page_performance": "Performance",
        "page_retention": "Retention",
        "page_segments": "Segments",
        "page_customers": "Customers",
        "page_clv_distribution": "CLV Distribution",
        "page_about": "About",
        "app_title": "Online Retail CLV",
        "data_not_found": (
            "Dashboard data not found. Run from project root: `python app/export_dashboard_data.py` "
            "(after running notebook 01 to generate `data/online_retail_clean.parquet` and `data/rfm_segments.csv`)."
        ),
        "customers_with_clv": "customers with CLV",
        "refresh_caption": "Refresh: `python app/export_dashboard_data.py`",
        "data_period": "Data period: {start} to {end}",
        "data_period_sidebar": "Period: {start} - {end}",
        "insights_header": "Key insights",
        "insight_coverage": "CLV coverage is {share:.1f}% of customers (repeat purchasers).",
        "insight_concentration": "Top 1% of customers contribute {pct:.1f}% of predicted 1Y CLV.",
        "insight_top_segment": "Highest total CLV segment: {segment} ({total}).",
        "insight_retention_m2": "Average retention drops to {m2:.0f}% by month 2.",
        "customers_axis_label": "Customers",
        "total_clv_axis_label": "Total CLV (£M)",
        "median_clv_axis_label": "Median CLV (£)",
        "month_axis_label": "Month",
        "orders_axis_label": "Orders",
        "revenue_axis_label": "Revenue (£)",
        "aov_axis_label": "AOV (£)",
        "revenue_share_axis_label": "Revenue share (%)",
        "count_axis_label": "Count",
        "clv_bin_axis_label": "CLV (£) bin",
        "clv_log_axis_label": "log₁₀(CLV) bin",
        "cohort_index_label": "Cohort index (month)",
        "cohort_month_label": "Cohort month",
        "retention_rate_label": "Retention rate",
        "country_axis_label": "Country",
        

        "what_is_clv_title": "What is Customer Lifetime Value (CLV)?",
        "what_is_clv": (
            "**Customer Lifetime Value (CLV)** = the total revenue we expect from a customer over a chosen period (2009/12/01 to 2011/12/09). "
            "It is estimated using two models: one predicts *how often* they will buy, the other *how much* they will spend per purchase. "
            "We use revenue (not profit) because margin data is not available in this dataset."
        ),
        # ---- Overview ----
        "overview_header": "Overview",
        "overview_intro": "This dashboard summarizes an end-to-end CLV project on Online Retail II data. "
            "It combines historical performance, cohort retention, and 12-month revenue CLV predictions.",
        "overview_caption": "Key metrics and segment-level summary from CLV modeling (revenue-based, 1-year horizon).",
        "total_customers": "Total customers",
        "total_customers_hint": "All unique customers in the cleaned dataset (Online Retail II, 2009-2011).",
        "with_clv_repeat": "With CLV (repeat)",
        "with_clv_repeat_hint": "Customers who bought more than once; only they get a CLV prediction (the model needs repeat behaviour).",
        "new_single_purchase": "New (single purchase)",
        "new_single_purchase_hint": "Customers with only one purchase so far; they are not included in CLV (no repeat pattern to model).",
        "top_1pct_share_clv": "Top 1% share of CLV",
        "top_1pct_share_clv_hint": "Share of total predicted revenue coming from the top 1% of customers. High % means value is concentrated in few customers.",
        "total_predicted_1y_revenue": "Total predicted 1Y revenue",
        "total_predicted_1y_revenue_hint": "Sum of all customers’ 1-year CLV; expected revenue from this customer base over the next 12 months.",
        "coverage_concentration_title": "What do “Coverage” and “Concentration” mean?",
        "coverage_text": "**Coverage:** {share_repeat:.1f}% of customers have a CLV prediction (repeat purchasers); single-purchase customers are excluded from the monetary model (Gamma-Gamma).",
        "concentration_text": "**Concentration:** The top {n} customers (1%) account for **{pct:.1f}%** of total predicted revenue — prioritise retention and care for this group.",
        "segment_size_customers": "Segment size (customers)",
        "segment_size_hint": "Number of customers in each RFM segment (e.g. Champions, Loyal, At Risk).",
        "median_1y_revenue_clv_by_segment": "Median 1Y revenue CLV by segment",
        "median_clv_hint": "Typical (median) predicted 1-year revenue per customer in each segment; robust to a few very high spenders.",
        "segment_summary_by_total_clv": "Segment summary (by total CLV)",
        "segment_summary_hint": "Per segment: customer count, total predicted revenue, mean and median CLV. Sorted by total CLV.",
        # ---- Performance ----
        "performance_header": "Performance",
        "performance_intro": "Historical performance from cleaned transactions: orders, revenue, AOV, and geography.",
        "performance_data_missing": "Performance data not found. Re-run the export script.",
        "total_revenue": "Total revenue (historical)",
        "total_orders": "Total orders",
        "avg_order_value": "Average order value",
        "monthly_orders": "Monthly orders",
        "monthly_revenue": "Monthly revenue",
        "monthly_aov": "Average order value (AOV)",
        "country_revenue_title": "Top countries by revenue",
        "exclude_uk": "Exclude United Kingdom",
        "top_n_countries": "Top N countries",
        "country_table_expander": "Show country table",
        # ---- Retention ----
        "retention_header": "Retention",
        "retention_intro": "Cohort analysis shows how retention changes by month since a customer’s first purchase.",
        "retention_data_missing": "Retention data not found. Re-run the export script.",
        "show_values": "Show values on heatmap",
        "customer_retention_tab": "Customer retention",
        "revenue_retention_tab": "Revenue retention",
        "cohort_heatmap_customers": "Customer retention heatmap",
        "cohort_heatmap_revenue": "Revenue retention heatmap",
        "avg_retention_curve": "Average retention by cohort index",
        "cohort_size_chart": "Cohort size (month 1 customers)",
        "retention_note": "Month 1 equals the first purchase month. Values are relative to month 1.",
        # ---- Segments ----
        "segments_header": "Segments",
        "segments_intro": (
            "Customers are grouped into **segments** using **RFM** (Recency, Frequency, Monetary): "
            "how recently they bought, how often, and how much they spent. "
            "Segments like **Champions** (recent, frequent, high spend) and **Loyal** are your best customers; "
            "**At Risk** and **Lost** need win-back campaigns. **VIP** and **B2B/Wholesale** are special flags (high value or bulk buyers)."
        ),
        "segments_caption": "Segment-level CLV metrics: customers, total/mean/median 1-year revenue CLV.",
        "tab_clv": "CLV view",
        "tab_rfm": "RFM view",
        "rfm_segment_summary": "RFM segment summary (historical)",
        "rfm_segment_hint": "Historical segment size and monetary value, before CLV modeling.",
        "total_clv_by_segment": "Total CLV by segment (£M)",
        "total_clv_segment_hint": "Total predicted 1-year revenue from all customers in that segment; shows which segments drive most revenue.",
        "median_clv_by_segment": "Median CLV by segment",
        "median_clv_segment_hint": "Typical customer value in the segment; use with segment size to prioritise retention vs growth.",
        "download_segment_summary": "Download segment summary (CSV)",
        # ---- Customers ----
        "customers_header": "Customers (CLV predictions)",
        "customers_intro": (
            "Here you see **per-customer** predictions: 1-year revenue CLV, probability they are still active (**P(Alive)**), "
            "and expected number of purchases in the next 12 months. Filter by segment, set thresholds, or search by Customer ID. "
            "Use this to list top customers for retention campaigns or to look up a specific account."
        ),
        "customers_caption": "Per-customer 1-year revenue CLV, P(Alive), and expected purchases. Filter and download.",
        "segment": "Segment",
        "vip_b2b": "VIP / B2B",
        "customer_id_optional": "Customer ID (optional)",
        "customer_id_placeholder": "e.g. 12347",
        "all": "All",
        "vip_only": "VIP only",
        "b2b_only": "B2B only",
        "non_vip": "Non-VIP",
        "non_b2b": "Non-B2B",
        "show_top_n_by_clv": "Show top N by CLV",
        "p_alive_min": "Minimum P(Alive)",
        "min_clv": "Minimum CLV (£)",
        "rows_shown": "Rows shown",
        "sum_displayed_clv": "Sum of displayed CLV",
        "sum_displayed_clv_hint": "Total predicted 1-year revenue of the customers currently shown in the table.",
        "download_current_table": "Download current table (CSV)",
        "customers_columns_expander_title": "What do the table columns mean?",
        "column_p_alive": "P(Alive) = probability the customer is still active (has not churned).",
        "column_expected_purchases": "Expected purchases (365 days) = predicted number of transactions in the next 12 months.",
        "column_clv_1y": "CLV (1Y revenue) = predicted revenue from this customer over the next 12 months.",
        # ---- CLV Distribution ----
        "clv_distribution_header": "CLV Distribution",
        "clv_distribution_intro": (
            "CLV is usually **right-skewed**: many customers have low predicted value, a few have very high value. "
            "The **raw** histogram shows this directly; the **log-scale** histogram makes the shape easier to see. "
            "You can filter by segment to compare distributions (e.g. VIP vs Loyal)."
        ),
        "clv_distribution_caption": "Distribution of predicted 1-year revenue CLV (raw and log scale). Optionally by segment.",
        "segment_for_distribution": "Segment (for distribution)",
        "clv_raw_histogram": "CLV (raw) — histogram",
        "clv_log_histogram": "CLV (log₁₀) — histogram",
        "no_data_segment": "No data for the selected segment.",
        "no_positive_log": "No positive CLV values for log scale.",
        "summary_stats_clv": "Summary stats (CLV)",
        "summary_stats_hint": "Count, mean, median, min, max of predicted 1-year CLV for the selected segment (or all).",
        # ---- About ----
        "about_header": "About this project",
        "about_intro": "Short story of the project: what we did, what the data and models are, and how to interpret the dashboard.",
        "about_body": """
This dashboard is the output of an end-to-end analytics project on Online Retail II (UCI) data.

What we did:
- Cleaned transactions and created RFM segments.
- Analyzed cohort retention (customer and revenue).
- Trained BG/NBD + Gamma-Gamma to estimate 12-month revenue CLV.

How to interpret:
- CLV is revenue-based because profit margin is not available.
- Only repeat customers receive CLV predictions.
- Use CLV together with P(Alive) to prioritize retention.

Refresh: After re-running the notebooks, run `python app/export_dashboard_data.py`.
        """,
        "how_to_use_title": "How to use this dashboard",
        "how_to_use_body": """
1. **Overview** — Main numbers (customers, CLV coverage, top 1% share, total predicted revenue) and segment charts. Start here for the big picture.
2. **Performance** — Historical revenue, orders, AOV, and country mix.
3. **Retention** — Cohort heatmaps and average retention curve.
4. **Segments** — Full segment table and charts (total CLV, median CLV). Use for “which segment to invest in” and download CSV.
5. **Customers** — Per-customer CLV, P(Alive), expected purchases. Filter by segment/VIP/B2B or search by ID; download the table.
6. **CLV Distribution** — Histograms (raw and log) and summary stats. Use to describe skew or compare segments.
        """,
    },
    "tr": {
        "page_overview": "Özet",
        "page_performance": "Performans",
        "page_retention": "Elde Tutma",
        "page_segments": "Segmentler",
        "page_customers": "Müşteriler",
        "page_clv_distribution": "CLV Dağılımı",
        "page_about": "Hakkında",
        "app_title": "Online Retail CLV",
        "data_not_found": (
            "Dashboard verisi bulunamadı. Proje kökünden çalıştırın: `python app/export_dashboard_data.py` "
            "(önce notebook 01 ile `data/online_retail_clean.parquet` ve `data/rfm_segments.csv` oluşturulmalı)."
        ),
        "customers_with_clv": "müşteriye CLV tahmini var",
        "refresh_caption": "Yenile: `python app/export_dashboard_data.py`",
        "data_period": "Veri dönemi: {start} - {end}",
        "data_period_sidebar": "Dönem: {start}-{end}",
        "insights_header": "Öne çıkan bulgular",
        "insight_coverage": "CLV kapsamı müşterilerin %{share:.1f}'i (tekrar alışveriş yapanlar).",
        "insight_concentration": "En üst %1 müşteri, 1 yıllık CLV’nin %{pct:.1f}'ini oluşturuyor.",
        "insight_top_segment": "Toplam CLV’de lider segment: {segment} ({total}).",
        "insight_retention_m2": "Ortalama elde tutma 2. ayda %{m2:.0f} seviyesine düşüyor.",
        "customers_axis_label": "Müşteri",
        "total_clv_axis_label": "Toplam CLV (£M)",
        "median_clv_axis_label": "Medyan CLV (£)",
        "month_axis_label": "Ay",
        "orders_axis_label": "Sipariş",
        "revenue_axis_label": "Gelir (£)",
        "aov_axis_label": "AOV (£)",
        "revenue_share_axis_label": "Gelir payı (%)",
        "count_axis_label": "Adet",
        "clv_bin_axis_label": "CLV (£) bin",
        "clv_log_axis_label": "log₁₀(CLV) bin",
        "cohort_index_label": "Kohort indeksi (ay)",
        "cohort_month_label": "Kohort ayı",
        "retention_rate_label": "Elde tutma oranı",
        "country_axis_label": "Ülke",
        
        "what_is_clv_title": "Müşteri Yaşam Boyu Değeri (CLV) nedir?",
        "what_is_clv": (
            "**Müşteri Yaşam Boyu Değeri (CLV)** = Seçilen dönemde (2009/12/01 - 2011/12/09) bir müşteriden beklenen toplam gelir. "
            "İki model ile tahmin edilir: biri *ne sıklıkla* alışveriş yapacağını, diğeri *alışveriş başına ne kadar* harcayacağını tahmin eder. "
            "Bu veri setinde kâr marjı olmadığı için **gelir** bazlı CLV kullanıyoruz."
        ),
        # ---- Özet ----
        "overview_header": "Özet",
        "overview_intro": "Bu dashboard, Online Retail II verisi üzerinde yapılan uçtan uca CLV projesinin özetini sunar. "
            "Geçmiş performans, kohort elde tutma ve 12 aylık gelir CLV tahminleri birlikte gösterilir.",
        "overview_caption": "CLV modellemesinden temel metrikler ve segment özeti (gelir bazlı, 1 yıllık ufuk).",
        "total_customers": "Toplam müşteri",
        "total_customers_hint": "Temizlenmiş veri setindeki tüm benzersiz müşteriler (Online Retail II, 2009-2011).",
        "with_clv_repeat": "CLV (tekrar alışveriş)",
        "with_clv_repeat_hint": "Birden fazla kez alan müşteriler; yalnızca onlara CLV tahmini yapılıyor (model tekrarlayan davranış ister).",
        "new_single_purchase": "Yeni (tek alışveriş)",
        "new_single_purchase_hint": "Şu ana kadar yalnızca bir alışveriş yapan müşteriler; CLV hesabına dahil değiller (modelleyecek tekrar yok).",
        "top_1pct_share_clv": "En üst %1 CLV payı",
        "top_1pct_share_clv_hint": "Toplam tahmini gelirin en zengin %1 müşteriden gelen oranı. Yüksek % değer birkaç müşteride toplanıyor demektir.",
        "total_predicted_1y_revenue": "Toplam tahmini 1Y gelir",
        "total_predicted_1y_revenue_hint": "Tüm müşterilerin 1 yıllık CLV toplamı; bu müşteri tabanından önümüzdeki 12 ayda beklenen gelir.",
        "coverage_concentration_title": "“Kapsam” ve “Yoğunlaşma” ne anlama geliyor?",
        "coverage_text": "**Kapsam:** Müşterilerin %{share_repeat:.1f}'inin CLV tahmini var (tekrar alışveriş yapanlar); tek alışverişliler parasal model (Gamma-Gamma) dışında.",
        "concentration_text": "**Yoğunlaşma:** En üst {n} müşteri (%1), toplam tahmini gelirin **%{pct:.1f}**'ini oluşturuyor — bu gruba elde tutma ve özen gösterin.",
        "segment_size_customers": "Segment büyüklüğü (müşteri sayısı)",
        "segment_size_hint": "Her RFM segmentindeki müşteri sayısı (Champions, Loyal, At Risk vb.).",
        "median_1y_revenue_clv_by_segment": "Segmente göre medyan 1Y gelir CLV",
        "median_clv_hint": "Segmentteki tipik (medyan) müşteri başı tahmini 1 yıllık gelir; birkaç çok yüksek harcayanı etkilemez.",
        "segment_summary_by_total_clv": "Segment özeti (toplam CLV'ye göre)",
        "segment_summary_hint": "Segment bazında: müşteri sayısı, toplam tahmini gelir, ortalama ve medyan CLV. Toplam CLV'ye göre sıralı.",
        # ---- Performans ----
        "performance_header": "Performans",
        "performance_intro": "Temizlenmiş işlemlerden geçmiş performans: sipariş, gelir, AOV ve coğrafya.",
        "performance_data_missing": "Performans verisi bulunamadı. Dışa aktarma scriptini yeniden çalıştırın.",
        "total_revenue": "Toplam gelir (geçmiş)",
        "total_orders": "Toplam sipariş",
        "avg_order_value": "Ortalama sepet (AOV)",
        "monthly_orders": "Aylık sipariş",
        "monthly_revenue": "Aylık gelir",
        "monthly_aov": "Ortalama sepet (AOV)",
        "country_revenue_title": "Gelire göre ülkeler (Top)",
        "exclude_uk": "Birleşik Krallık hariç",
        "top_n_countries": "Üst N ülke",
        "country_table_expander": "Ülke tablosunu göster",
        # ---- Elde Tutma ----
        "retention_header": "Elde Tutma",
        "retention_intro": "Kohort analizi, ilk alışverişten sonra aylara göre elde tutmayı gösterir.",
        "retention_data_missing": "Elde tutma verisi bulunamadı. Dışa aktarma scriptini yeniden çalıştırın.",
        "show_values": "Heatmap üzerinde değerleri göster",
        "customer_retention_tab": "Müşteri elde tutma",
        "revenue_retention_tab": "Gelir elde tutma",
        "cohort_heatmap_customers": "Müşteri elde tutma ısı haritası",
        "cohort_heatmap_revenue": "Gelir elde tutma ısı haritası",
        "avg_retention_curve": "Kohort indeksine göre ortalama elde tutma",
        "cohort_size_chart": "Kohort büyüklüğü (1. ay müşterileri)",
        "retention_note": "1. ay = ilk alışveriş ayı. Değerler 1. aya göre normalize edilmiştir.",
        # ---- Segmentler ----
        "segments_header": "Segmentler",
        "segments_intro": (
            "Müşteriler **RFM** (Recency, Frequency, Monetary) ile **segmentlere** ayrıldı: "
            "ne kadar yakın zamanda aldıkları, ne sıklıkla aldıkları ve ne kadar harcadıkları. "
            "**Champions** (yakın, sık, yüksek harcama) ve **Loyal** en iyi müşterileriniz; "
            "**At Risk** ve **Lost** geri kazanım kampanyalarına aday. **VIP** ve **B2B/Wholesale** özel işaretler (yüksek değer veya toptan alıcı)."
        ),
        "segments_caption": "Segment bazlı CLV metrikleri: müşteri sayısı, toplam/ortalama/medyan 1 yıllık gelir CLV.",
        "tab_clv": "CLV görünümü",
        "tab_rfm": "RFM görünümü",
        "rfm_segment_summary": "RFM segment özeti (geçmiş)",
        "rfm_segment_hint": "CLV öncesi, geçmiş harcama ve segment büyüklüğü.",
        "total_clv_by_segment": "Segmente göre toplam CLV (£M)",
        "total_clv_segment_hint": "O segmentteki tüm müşterilerin toplam tahmini 1 yıllık geliri; hangi segmentin en çok geliri getirdiğini gösterir.",
        "median_clv_by_segment": "Segmente göre medyan CLV",
        "median_clv_segment_hint": "Segmentteki tipik müşteri değeri; segment büyüklüğü ile birlikte elde tutma vs büyüme önceliği için kullanın.",
        "download_segment_summary": "Segment özetini indir (CSV)",
        # ---- Müşteriler ----
        "customers_header": "Müşteriler (CLV tahminleri)",
        "customers_intro": (
            "Burada **müşteri bazlı** tahminler var: 1 yıllık gelir CLV, hâlâ aktif olma olasılığı (**P(Alive)**) "
            "ve önümüzdeki 12 ayda beklenen alışveriş sayısı. Segment filtresi ve eşiklerle çalışabilir, Müşteri ID ile arayabilirsiniz. "
            "Elde tutma kampanyaları için en üst müşterileri listelemek veya belirli bir hesabı görmek için kullanın."
        ),
        "customers_caption": "Müşteri bazlı 1 yıllık gelir CLV, P(Alive) ve beklenen alışveriş. Filtrele ve indir.",
        "segment": "Segment",
        "vip_b2b": "VIP / B2B",
        "customer_id_optional": "Müşteri ID (isteğe bağlı)",
        "customer_id_placeholder": "örn. 12347",
        "all": "Tümü",
        "vip_only": "Sadece VIP",
        "b2b_only": "Sadece B2B",
        "non_vip": "VIP değil",
        "non_b2b": "B2B değil",
        "show_top_n_by_clv": "CLV'ye göre ilk N müşteri",
        "p_alive_min": "Minimum P(Alive)",
        "min_clv": "Minimum CLV (£)",
        "rows_shown": "Gösterilen satır",
        "sum_displayed_clv": "Gösterilen CLV toplamı",
        "sum_displayed_clv_hint": "Tabloda şu an gösterilen müşterilerin toplam tahmini 1 yıllık geliri.",
        "download_current_table": "Mevcut tabloyu indir (CSV)",
        "customers_columns_expander_title": "Tablo sütunları ne anlama geliyor?",
        "column_p_alive": "P(Alive) = müşterinin hâlâ aktif (churn olmamış) olma olasılığı.",
        "column_expected_purchases": "Beklenen alışveriş (365 gün) = önümüzdeki 12 ayda tahmin edilen işlem sayısı.",
        "column_clv_1y": "CLV (1Y gelir) = bu müşteriden önümüzdeki 12 ayda tahmin edilen gelir.",
        # ---- CLV Dağılımı ----
        "clv_distribution_header": "CLV Dağılımı",
        "clv_distribution_intro": (
            "CLV genelde **sağa çarpıktır**: çok müşteri düşük tahmini değere sahipken az sayıda müşteri çok yüksek değere sahip olur. "
            "**Ham** histogram bunu doğrudan gösterir; **log ölçek** histogram şekli daha rahat okunur kılar. "
            "Segment seçerek dağılımları karşılaştırabilirsiniz (örn. VIP vs Loyal)."
        ),
        "clv_distribution_caption": "Tahmini 1 yıllık gelir CLV dağılımı (ham ve log ölçek). İsteğe bağlı segment.",
        "segment_for_distribution": "Dağılım için segment",
        "clv_raw_histogram": "CLV (ham) — histogram",
        "clv_log_histogram": "CLV (log₁₀) — histogram",
        "no_data_segment": "Seçilen segment için veri yok.",
        "no_positive_log": "Log ölçek için pozitif CLV yok.",
        "summary_stats_clv": "Özet istatistikler (CLV)",
        "summary_stats_hint": "Seçilen segment (veya tümü) için tahmini 1 yıllık CLV’nin adet, ortalama, medyan, min, max değerleri.",
        # ---- Hakkında ----
        "about_header": "Proje hakkında",
        "about_intro": "Projenin kısa hikâyesi: ne yaptık, veri ve modeller ne, dashboard nasıl yorumlanır.",
        "about_body": """
Bu dashboard, Online Retail II (UCI) verisi üzerinde yapılan uçtan uca bir analitik projenin çıktısıdır.

Ne yaptık:
- İşlem verisini temizledik ve RFM segmentleri oluşturduk.
- Kohort elde tutma analizleri yaptık (müşteri ve gelir).
- BG/NBD + Gamma-Gamma ile 12 aylık gelir CLV tahmini ürettik.

Nasıl yorumlanır:
- CLV gelir bazlıdır; kâr marjı bulunmuyor.
- Yalnızca tekrar alışveriş yapan müşterilere CLV atanır.
- Elde tutma önceliği için CLV’yi P(Alive) ile birlikte kullanın.

Yenile: Notebook’ları yeniden çalıştırdıktan sonra `python app/export_dashboard_data.py` çalıştırın.
        """,
        "how_to_use_title": "Bu dashboard nasıl kullanılır",
        "how_to_use_body": """
1. **Özet** — Ana sayılar (müşteri sayısı, CLV kapsamı, en üst %1 payı, toplam tahmini gelir) ve segment grafikleri. Genel resim için buradan başlayın.
2. **Performans** — Geçmiş gelir, sipariş, AOV ve ülke dağılımı.
3. **Elde Tutma** — Kohort ısı haritaları ve ortalama elde tutma eğrisi.
4. **Segmentler** — Tam segment tablosu ve grafikler (toplam CLV, medyan CLV). “Hangi segmente yatırım yapalım” için kullanın ve CSV indirin.
5. **Müşteriler** — Müşteri bazlı CLV, P(Alive), beklenen alışveriş. Segment/VIP/B2B ile filtreleyin veya ID ile arayın; tabloyu indirin.
6. **CLV Dağılımı** — Histogramlar (ham ve log) ve özet istatistikler. Çarpıklığı veya segmentleri karşılaştırmak için kullanın.
        """,
    },
}


def get(lang: str, key: str, **kwargs) -> str:
    """Get translation for key in language; format with kwargs if given."""
    s = TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, TRANSLATIONS["en"].get(key, key))
    if kwargs:
        return s.format(**kwargs)
    return s
