#  Volvo Inventory & Sales Dashboard

This interactive dashboard allows you to analyse sales performance, inventory risk levels, and profitability across different Volvo models and categories.

It is built using **Python**, **Pandas**, and **Streamlit**, and can be used by operations analysts, sales teams, or warehouse planners.

---

##  Features

- **Filterable Insights**: Analyse KPIs by model and category.
- **KPI Metrics**: Sales, revenue, profit, inventory value, stock turnover.
- **Visual Charts**:
  - Sales by model and category
  - Inventory vs. sales comparison
  - Top profit generators
  - Inventory risk levels and turnover
- **Risk Tables**:
  - High-demand, low-stock items
  - Slow-moving products
  - Dead stock and zero-zero items
- **Insight Summary**: Auto-generated business insight text.
- **PDF Export**: Download a full analytical report with charts.

---

##  Project Structure

```
├── app/
│   └── streamlit_app.py         # Main app file
├── core/
│   ├── data_loader.py
│   ├── kpi_calculator.py
│   └── inventory_analysis.py
├── report/
│   ├── chart_generator.py
│   ├── insight_text.py
│   └── report_exporter.py
├── data/
│   └── volvo_data.csv           # Sample dataset
└── README.md
```

---

##  How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/Hoda834/Sales-Dashboard.git
   cd Sales-Dashboard
   ```

2. Create virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the dashboard:
   ```bash
   streamlit run app/streamlit_app.py
   ```

---

## Requirements

Make sure to install packages listed in `requirements.txt`. 

---

## License

This project is for demonstration and educational use. For any business use or extension, please contact the author.

---

## Author

**Hoda Rezvanjoo**  
Insight Analyst | Data Storyteller | Digital Optimiser  
[LinkedIn](https://www.linkedin.com/in/hoda-rezvanjoo/)  

