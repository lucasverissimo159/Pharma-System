# English Version

# Workbook — Systems Engineering Portfolio in 12 Weeks

**Umbrella Project: PharmaSystem — Management System for Pharmacy Network**

> Each week is a module from the same ecosystem. In the end, the recruiter will see a coherent evolution in your GitHub: modeling → API → dashboard → architecture → full integration.

---

## How to Use This Workbook

Each module follows the same structure:

- **Context:** where this module fits into the PharmaSystem.
- **What to study:** theoretical content with free sources.
- **Daily itinerary:** practical division from Monday to Sunday.
- **Deliverables:** what needs to be ready on Sunday night.
- **Publishing checklist:** GitHub + LinkedIn.

**Rule of thumb:** study Monday to Wednesday, build Thursday to Saturday, publish on Sunday.

---

## PharmaSystem Overview

PharmaSystem is a fictional (but realistic) system for a pharmacy chain with 100 branches. Over the 12 weeks, you will build layer by layer:

```
Week 1 → Database (sales)
Week 2 → Executive dashboard (Power BI)
Week 3 → Analysis with Python/Pandas
Week 4 → Automated ETL Pipeline
Week 5 → REST API
Week 6 → Web System (Internal Help Desk)
Week 7 → Requirements Engineering Documentation
Week 8 → Complete system architecture design
Week 9 → Data Engineering Pipeline
Week 10 → MBSE Modeling
Week 11 → Integration of all modules
Week 12 → Complete final project + professional README
```

**GitHub repository:** create a repository called `pharma-system` with one folder per module:

```
pharma-system/
├── README.md ← project overview
├── module-01-sql/
├── module-02-powerbi/
├── module-03-python-pandas/
├── module-04-etl/
├── module-05-api-rest/
├── module-06-sistema-web/
├── module-07-requirements/
├── module-08-architecture/
├── module-09-data-engineering/
├── module-10-mbse/
├── module-11-integration/
└── module-12-final-project/
```

---

---

# MODULE 01 — SQL for Data Analysis

## Context in PharmaSystem

Every pharmacy chain needs a robust sales database. In this module, you create the data foundation upon which the rest of the portfolio will be built. Without this database, there is no dashboard, there is no ETL, there is no API.

## What to Study

### Mandatory concepts (Monday and Tuesday)

1. **Relational Model:** entities, attributes, primary keys, foreign keys, normalization (1NF, 2NF, 3NF).
2. **DDL:** CREATE TABLE, ALTER TABLE, DROP TABLE, data types (INT, VARCHAR, DECIMAL, DATE, TIMESTAMP).
3. **DML:** INSERT, UPDATE, DELETE.
4. **Queries:** SELECT, WHERE, ORDER BY, GROUP BY, HAVING, LIMIT.
5. **Joins:** INNER JOIN, LEFT JOIN, RIGHT JOIN.
6. **Aggregation functions:** COUNT, SUM, AVG, MIN, MAX.
7. **Subqueries and CTEs (WITH).**

### Free study sources

- **W3Schools SQL Tutorial** — quick reference for syntax.
- **SQLBolt** (sqlbolt.com) — progressive interactive exercises.
- **Mode Analytics SQL Tutorial** — focus on data analysis with SQL.
- **Official PostgreSQL documentation** — for consultation of specific functions.

### Estimated theoretical study time

Around 6 to 8 hours spread over two days (Monday and Tuesday). If you are already familiar with SQL, you can reduce it to 3 to 4 hours and advance the construction.

## Daily Itinerary

### Monday — Fundamentals and Modeling

**Morning/Afternoon (study):**

- Study relational model and normalization.
- Watch a video or read a tutorial on database modeling.

**Night (initial practice):**

- Install PostgreSQL and DBeaver (if you don't already have it).
- Create the `pharma_system` database.
- Design the ER diagram on paper or in draw.io with these entities:

```
branches (id, name, city, state, opening_date)
categories (id, name)
products (id, name, category_id, cost_price, sales_price, minimum_stock)
customers (id, name, cpf, email, telephone, registration_date)
sales (id, branch_id, customer_id, sales_date, total_amount, payment_method)
sale_items (id, sale_id, product_id, quantity, unit_price, subtotal)
```

### Tuesday — DDL and Data Insertion

**Morning (study):**

- Study DDL, data types, constraints (NOT NULL, UNIQUE, CHECK, FOREIGN KEY).

**Afternoon/Night (construction):**

- Write the `CREATE TABLE` scripts with all the constraints.
- Enter realistic data: at least 10 branches, 50 products, 100 customers and 500 sales.
- Tip: use ChatGPT or a Python script to generate bulk INSERTs with data that makes sense for pharmacies (medicines, cosmetics, hygiene).

### Wednesday — Basic and Intermediate Consultations

**Full day (construction):**

Create at least 20 SQL queries organized by category. Examples:

**General sales:**

1. Total network billing.
2. Billing by branch.
3. Billing per month.
4. General average ticket.
5. Average ticket per branch.

**Products:**

6. Top 10 best-selling products (quantity).
7. Top 10 products with the highest revenue.
8. Products that were never sold.
9. Average price per category.
10. Profit margin per product (sale_price - cost_price).

**Clients:**

11. Customers who purchased the most (value).
12. Customers who purchased the most (frequency).
13. Customers without purchases in the last 90 days.
14. Distribution of customers by branch.

**Time:**

15. Sales by day of the week.
16. Month-to-month comparison.
17. Best and worst sales month.

**Advanced:**

18. Ranking of branches using Window Function (RANK, ROW_NUMBER).
19. Moving average of sales per month (Window Function).
20. CTE to calculate month-to-month percentage growth.

### Thursday — Advanced Queries and Refinement

**Full day:**

- Review and optimize queries.
- Add indexes on the most consulted columns.
- Create at least 2 Views for frequent queries (e.g.: `vw_faturamento_mensal`, `vw_ranking_produtos`).
- Document each query with SQL comments explaining the objective.

### Friday — Organization and Documentation

- Organize scripts into separate files:
  - `01_schema.sql` — creation of tables.
  - `02_inserts.sql` — example data.
  - `03_consultas.sql` — all 20+ queries documented.
  - `04_views.sql` — views created.
- Take screenshots of the most interesting results in DBeaver.
- Write the module's `README.md`.

### Saturday — Review and Polishing

- Reread everything with a critical eye: is the README clear? Do queries make business sense?
- Add an ER diagram exported as an image to the repository.
- Test running everything from scratch (drop → create → insert → queries) to ensure it works.

### Sunday — Publication

- Push to GitHub.
- Publish on LinkedIn.

## Deliverables

- ER diagram in image (PNG or SVG).
- Database creation script (`01_schema.sql`).
- Data insertion script (`02_inserts.sql`).
- At least 20 documented SQL queries (`03_consultas.sql`).
- At least 2 Views (`04_views.sql`).
- README.md with: project description, ER diagram, how to execute, query examples and printouts of results.

## Publication Checklist

**GitHub:**

- [ ] Clean and commented code.
- [ ] README with sections: Description, ER Diagram, Technologies, How to Execute, Query Examples, Prints.
- [ ] Images in the `docs/` or `assets/` folder.

**LinkedIn:**

- [ ] Text of 3 to 5 paragraphs.
- [ ] Mention: the business problem, the technologies used, what you learned.
- [ ] Include 2 to 3 images (ER diagram, interesting query result).
- [ ] Link to GitHub repository.
- [ ] Hashtags: #SQL #PostgreSQL #Data Analysis #Dev Portfolio #SystemEngineering

---

---

# MODULE 02 — Power BI

## Context in PharmaSystem

The data exists in the bank, but the management of a pharmacy chain needs quick visibility. In this module, you transform the raw data from Module 01 into an interactive executive dashboard — exactly the type of deliverable that data analysts produce on a daily basis.

## What to Study

### Mandatory concepts (Monday and Tuesday)

1. **Power BI Desktop Interface:** panels, tabs (Report, Data, Model).
2. **Connection to data sources:** import from PostgreSQL or CSV file.
3. **Power Query (M):** rename columns, change types, remove duplicates, create calculated columns.
4. **Data model:** relationships between tables (1:N, N:N), fact table vs. dimension (basic Star Schema).
5. **Basic DAX:** CALCULATE, SUM, AVERAGE, COUNTROWS, DIVIDE, FILTER, ALL, DATEADD, SAMEPERIODLASTYEAR.
6. **Visual:** bar chart, line chart, pie chart, cards (KPI), tables, slicers, maps.
7. **Formatting and design:** color palette, alignment, contrast, visual hierarchy.

### Free study sources

- **Microsoft Learn — Power BI** (learn.microsoft.com) — official trail, free and with certificate.
- **Hashtag Training Channel** (YouTube, PT-BR) — practical Power BI tutorials.
- **Karine Lago Channel** (YouTube, PT-BR) — focus on professional dashboards.
- **DAX Guide** (dax.guide) — reference for DAX functions.

### Estimated time

Around 6 hours of theoretical study. If you've used Power BI before, jump right into building it.

## Daily Itinerary

### Monday — Study and Data Preparation

**Morning (study):**

- Watch tutorials on data connection and Power Query.
- Understand the concept of Star Schema (fact table + dimensions).

**Afternoon/Night (practice):**

- Export data from the Module 01 database to CSVs (one table per file) or connect directly to PostgreSQL.
- Import into Power BI and configure relationships in the model.
- Clean data in Power Query: correct types, clear names, removing inconsistencies.

### Tuesday — DAX Study and First Measurements

**Morning (study):**

- Study the most used DAX functions: SUM, AVERAGE, CALCULATE, COUNTROWS.
- Understand the concept of filter context.

**Afternoon/Night (construction):**

Create these DAX measures:

- `Total Revenue = SUM(items_sale[subtotal])`
- `Average Ticket = DIVIDE([Total Revenue], COUNTROWS(sales))`
- `Total Sales = COUNTROWS(sales)`
- `Previous Month Billing = CALCULATE([Total Billing], DATEADD(calendar[Data], -1, MONTH))`
- `Growth % = DIVIDE([Total Revenue] - [Previous Month Revenue], [Previous Month Revenue])`
- Create a calendar table (Calendar) with `CALENDAR(MIN(sales[sales_date]), MAX(sales[sales_date]))`.

### Wednesday — Dashboard Construction (Page 1: Overview)

**Full day (construction):**

Create the first page of the dashboard with:

- **Cards (KPIs):** Total Revenue, Total Sales, Average Ticket, % Growth.
- **Line graph:** Monthly revenue (X axis = month, Y axis = revenue).
- **Horizontal bar chart:** Top 10 branches by revenue.
- **Segmenters:** Period (month/year), State, Branch.
- Apply a consistent color palette (use drugstore green/blue tones).

### Thursday — Dashboard (Page 2: Products + Page 3: Customers)

**Page 2 — Products:**

- Bar graph: Top 10 best-selling products.
- Pie/donut chart: Revenue by category.
- Table: Products with profit margin (sale_price - cost_price).
- Card: Best-selling product of the selected period.

**Page 3 — Customers:**

- Cards: Total customers, Active customers (purchased in the last 90 days).
- Bar graph: Top 10 customers by amount spent.
- Line graph: Evolution of new registrations per month.
- Segmenter: Branch.

### Friday — Visual Refinement and Interactivity

- Add custom tooltips (when hovering, show details).
- Configure drill-down: when clicking on a branch, filter everything for it.
- Add navigation buttons between pages.
- Adjust fonts, colors, alignments — everything professional.
- Add a fictitious title and logo "PharmaSystem" in the header.

### Saturday — Documentation and Prints

- Take screenshots of each dashboard page (high quality PNG).
- Export the .pbix.
- Write the README.md with: dashboard description, prints, DAX measurements created, how to connect to the data, what each page shows.

### Sunday — Publication

- Push on GitHub (`modulo-02-powerbi/` folder).
- Publish on LinkedIn with screenshots of the dashboard.

## Deliverables

- Power BI `.pbix` file.
- At least 3 dashboard pages (Overview, Products, Customers).
- Minimum of 5 DAX measurements.
- Prints of each dashboard page.
- Complete README.md.

## Publication Checklist

**GitHub:**

- [ ] .pbix file in the module folder.
- [ ] Prints in `docs/`.
- [ ] README with: Description, Prints, DAX Measurements, Data Source, How to Open.

**LinkedIn:**

- [ ] Prints of the dashboard (2 to 3 flashy images).
- [ ] Text explaining: which business problem the dashboard solves, KPIs chosen, design decision.
- [ ] Hashtags: #PowerBI #Dashboard #DataAnalytics #BusinessIntelligence #PortfolioDev

---

---

# MODULE 03 — Python + Pandas

## Context in PharmaSystem

The pharmacy chain's data team needs deeper analysis that pure SQL doesn't easily deliver — cleaning dirty data, descriptive statistics, correlations, and exporting automated reports. In this module, you use Python and Pandas to perform exploratory analysis of sales data.

## What to Study

### Mandatory concepts (Monday and Tuesday)

1. **Pandas:** DataFrame, Series, CSV/Excel/SQL reading, selection (loc, iloc), filters, groupby, merge, pivot_table.
2. **Data cleaning:** treat nulls (fillna, dropna), duplicates, data types, outliers.
3. **Descriptive statistics:** describe(), mean, median, std, correlation.
4. **Matplotlib/Seaborn:** bar charts, lines, histogram, boxplot, correlation heatmap.
5. **Export:** to_excel(), to_csv().

### Free study sources

- **Official Pandas** (pandas.pydata.org/docs/getting_started) — excellent tutorials.
- **Kaggle Learn — Pandas** (kaggle.com/learn/pandas) — short interactive course.
- **Real Python — Pandas Tutorials** — in-depth articles.
- **Seaborn Gallery** (seaborn.pydata.org/examples) — visual examples of charts.

### Estimated time

If you already know Python, 4 to 5 hours of study focused on Pandas. If you are new to Python, set aside 8 to 10 hours including the basics of the language.

## Daily Itinerary

### Monday — Panda Study

- Take the Pandas Kaggle Learn course (takes about 4 hours).
- Practice basic operations in a Jupyter notebook: read CSV, filter, group.

### Tuesday — Visualization Study + Bank Connection

- Study Matplotlib and Seaborn: at least 5 chart types.
- Connect to the PostgreSQL database using `psycopg2` or `sqlalchemy`:

```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://usuario:senha@localhost:5432/pharma_system')
df_vendas = pd.read_sql('SELECT * FROM sales', engine)
```

### Wednesday — Cleaning and Preparation

- Load all database tables into DataFrames.
- Clean up: check nulls, types, duplicates.
- Create derived columns:
  - `mes_venda` extracted from `data_venda`.
  - `week_day` extracted from `sales_date`.
  - `profit_margin` = sales_price - cost_price.
- Make the necessary merges (sales + items + products + branches).

### Thursday — Exploratory Analysis

Create an organized Jupyter notebook with these sections:

1. **General summary:** shape, describe(), info().
2. **Sales analysis:** revenue per month, per branch, per category.
3. **Product analysis:** top 10, price distribution (histogram), margin boxplot by category.
4. **Customer analysis:** purchase frequency distribution, segmentation by value (quartiles).
5. **Correlations:** correlation heatmap between numerical variables.
6. **Insights:** write in Markdown in your notebook at least 5 business insights that the data reveals.

### Friday — Export and Report

- Export an Excel report with multiple tabs:
  - Tab 1: Monthly billing.
  - Tab 2: Product ranking.
  - Tab 3: Branch ranking.
  - Tab 4: Filtered raw data.
- Use `openpyxl` to format Excel (bold headers, column widths).
- Save all graphics as PNG images.

### Saturday — Documentation

- Clean the notebook: remove test cells, add titles and explanations.
- Write the README.md.
- Organize the folder: `notebooks/`, `exports/`, `graficos/`, `README.md`.

### Sunday — Publication

- Push on GitHub.
- Publish on LinkedIn with 2 to 3 graphs generated by Seaborn/Matplotlib.

## Deliverables

- Complete Jupyter notebook with exploratory analysis.
- At least 8 graphs (bars, lines, histogram, boxplot, heatmap, etc.).
- Report exported in Excel with multiple tabs.
- Complete README.md.

## Publication Checklist

**GitHub:**

- [ ] Clean and documented `.ipynb` notebook.
- [ ] Graphics exported in `graficos/`.
- [ ] Excel in `exports/`.
- [ ] README with: Description, Prints/Graphs, Technologies, How to Execute, Insights Found.

**LinkedIn:**

- [ ] 2 to 3 most impactful graphics.
- [ ] Text focusing on business insights (not pure technique).
- [ ] Hashtags: #Python #Pandas #DataAnalysis #DataAnalysis #DevPortfólio

---

---

# MODULE 04 — ETL (Extract, Transform, Load)

## Context in PharmaSystem

In the real world, sales data from 100 branches arrives in CSV files exported from cashiers. The data team needs an automated pipeline that reads these CSVs, cleans, transforms, and loads them into the database — and then Power BI automatically updates itself. This module demonstrates a competence that is highly valued in the market.

## What to Study

### Mandatory concepts (Monday and Tuesday)

1. **What is ETL:** Extract (extract from sources), Transform (clean, validate, enrich), Load (load into destination).
2. **Difference between ETL and ELT.**
3. **Logging in Python:** `logging` module to record each step.
4. **Error handling:** try/except for corrupted or unexpectedly formatted files.
5. **Scheduling (concept):** cron, Task Scheduler, or libraries like `schedule`.
6. **Best practices:** idempotence (run 2x without duplication), schema validation, processed file folder vs. new ones.

### Free study sources

- **Real Python — ETL Pipeline** — search for "build etl pipeline python" in Real Python.
- **Python logging module documentation** — essential for pipelines.
- **Articles about data pipeline patterns** — Medium and Towards Data Science.

### Estimated time

4 to 6 hours of study. The focus is more practice than theory.

## Daily Itinerary

### Monday — Study and Planning

**Morning (study):**

- Study ETL concepts and good practices.
- Study the Python `logging` module.

**Afternoon/Night:**

- Plan the pipeline architecture:

```
raw_data/ ← New CSVs arrive here
processed_data/ ← Already processed CSVs are moved here
logs/ ← logs of each execution
scripts/
  ├── extract.py ← reads the CSVs
  ├── transform.py ← cleaning and validation
  ├── load.py ← loads in PostgreSQL
  └── pipeline.py ← orchestrates everything
config/
  └── config.yaml ← settings (bank path, etc.)
```

### Tuesday — Extract

- Generate 5 to 10 CSV files simulating branch data (use Python or data from Module 01).
- Purposefully include problems: blank lines, dates in different formats, negative values, duplicate CPFs.
- Write `extract.py`:
  - Reads all CSVs from `raw_data/`.
  - Returns a list of DataFrames.
  - Log how many files it found, how many lines each one has.

### Wednesday — Transform

- Write `transform.py`:
  - Standardizes column names (snake_case).
  - Converts types (dates, decimals).
  - Removes duplicates.
  - Treats nulls (fill in or discard, with justification).
  - Validates business rules (e.g.: quantity > 0, price > 0).
  - Logs each transformation and how many rows were affected.
  - Returns clean DataFrame.

### Thursday — Load

- Write `load.py`:
  - Connects to PostgreSQL.
  - Uses `UPSERT` (INSERT ... ON UPDATE CONFLICT) for idempotence.
  - Logs how many lines were inserted/updated.
- Write `pipeline.py`:
  - Call extract → transform → load in sequence.
  - At the end, move processed CSVs to `processed_data/`.
  - Generates a final summary log (total files, lines processed, errors).

### Friday — Tests and Robustness

- Test scenarios:
  - Empty CSV.
  - CSV with missing columns.
  - CSV with different encoding (UTF-8 vs. Latin-1).
  - Run the pipeline 2x without duplicating data (test idempotence).
- Add error handling for each scenario.
- (Optional) Add a report email send to the end of the pipeline using `smtplib`.

### Saturday — Documentation and Diagram

- Create an ETL flow diagram (use draw.io or Mermaid):

```
CSV Branches → [Extract] → [Transform] → [Load] → PostgreSQL → Power BI
```

- Write the README.md with: business problem, architecture, how to execute, example logs, error handling.

### Sunday — Publication

- Push on GitHub.
- Publish on LinkedIn with the flow diagram and a printout of the execution log.

## Deliverables

- Python scripts separated by responsibility (extract, transform, load, pipeline).
- YAML configuration file.
- Example CSVs (with and without errors).
- Pipeline flow diagram.
- Example execution logs.
- Complete README.md.

## Publication Checklist

**GitHub:**

- [ ] Modular and documented code.
- [ ] Example CSVs in `raw_data/`.
- [ ] Flow diagram in `docs/`.
- [ ] README with: Problem, Architecture, How to Execute, Log Examples.

**LinkedIn:**

- [ ] ETL flow diagram.
- [ ] Print the successful execution log.
- [ ] Text explaining: why ETL is important, what the pipeline does, error handling.
- [ ] Hashtags: #ETL #Python #DataEngineering #Pipeline #PortfolioDev

---

---

# MODULE 05 — REST API

## Context in PharmaSystem

The PharmaSystem needs to expose data to other systems: the branches' mobile app queries products, the e-commerce system places orders, the dashboard consumes indicators. A REST API is the interface that connects everything. This is one of the most valued modules in selection processes.

## What to Study

### Mandatory concepts (Monday and Tuesday)

1. **REST:** resources, HTTP verbs (GET, POST, PUT, DELETE), status codes (200, 201, 400, 404, 500).
2. **JSON:** structure, serialization, deserialization.
3. **Flask (Python option)** or **Spring Boot (Java option):** routes, controllers, models, serialization.
4. **ORM:** SQLAlchemy (Flask) or JPA/Hibernate (Spring Boot) — object-relational mapping.
5. **Swagger/OpenAPI:** automatic API documentation.
6. **API Testing:** Postman or Insomnia to test endpoints.

**Recommendation:** as your portfolio already has a lot of Python, consider using Spring Boot to demonstrate versatility. But if you need to save time, Flask is faster to implement.

### Free study sources

**Flask:**
- **Miguel Grinberg — Flask Mega-Tutorial** (blog.miguelgrinberg.com).
- **Real Python — Flask REST API** — search for "flask rest api tutorial".
- **Flask Documentation** (flask.palletsprojects.com).

**Spring Boot:**
- **Baeldung** (baeldung.com) — reference for Spring Boot REST.
- **Spring Initializr** (start.spring.io) — to generate the base project.
- **Michelli Brito Channel** (YouTube, PT-BR) — Spring Boot tutorials.

### Estimated time

Flask: 6 to 8 hours. Spring Boot: 8 to 12 hours (more setup, more concepts).

## Daily Itinerary

### Monday — REST Study + Setup

**Morning (study):**

- Study REST concepts, HTTP verbs, status codes.
- Watch an introductory tutorial on the chosen framework.

**Afternoon/Night:**

- Create the base project.
- Configure the connection to the Module 01 PostgreSQL database.
- Create the `Product` model (entity/class mapped to the `products` table).

### Tuesday — Product CRUD

- Implement the Product endpoints:
  - `GET /api/produtos` — list all (with pagination).
  - `GET /api/produtos/{id}` — search by ID.
  - `POST /api/produtos` — create new product.
  - `PUT /api/produtos/{id}` — update product.
  - `DELETE /api/produtos/{id}` — delete product.
- Test them all in Postman.

### Wednesday — Customer and Branch CRUD

- Repeat the same structure for:
  - `GET/POST/PUT/DELETE /api/clientes`
  - `GET/POST/PUT/DELETE /api/filiais`
- Add validations: mandatory fields, CPF format, email.
- Return proper errors (400 for validation, 404 for not found).

### Thursday — Sales Endpoints and Indicators

- Implement:
  - `POST /api/vendas` — register a sale (with items).
  - `GET /api/vendas?filial_id=X&mes=Y` — list sales with filters.
  - `GET /api/indicadores/invoicing-monthly` — returns aggregate billing per month.
  - `GET /api/indicadores/top-produtos?limit=10` — top N products.
  - `GET /api/indicadores/top-filiais` — branch ranking.

### Friday — Documentation and Swagger

- Configure Swagger/OpenAPI for automatic documentation.
  - Flask: use `flask-smorest` or `flasgger`.
  - Spring Boot: use `springdoc-openapi`.
- Ensure all endpoints are documented with examples.
- Test error scenarios (non-existent IDs, invalid payloads).

### Saturday — README and Prints

- Take screenshots of Swagger showing the endpoints.
- Take screenshots of Postman with examples of requests and responses.
- Write the README.md with: API description, available endpoints, how to execute, prints.

### Sunday — Publication

- Push on GitHub.
- Publish on LinkedIn with screenshots from Swagger and Postman.

## Deliverables

- API code (Flask or Spring Boot).
- At least 15 functional endpoints.
- Swagger/OpenAPI documentation.
- Prints from Postman with sample requests.
- Complete README.md.

## Publication Checklist

**GitHub:**

- [ ] Organized code (controllers, models, services, repositories).
- [ ] requirements.txt (Flask) or pom.xml (Spring Boot).
- [ ] Prints from Swagger and Postman in `docs/`.
- [ ] README with: Description, Endpoints, How to Execute, Prints, Technologies.

**LinkedIn:**

- [ ] Print from Swagger showing the list of endpoints.
- [ ] Print a request/response in Postman.
- [ ] Text explaining: what the API does, design decisions, validations.
- [ ] Hashtags: #API #REST #Flask #SpringBoot #Backend #PortfolioDev

---

---

# MODULE 06 — Web System

## Context in PharmaSystem

A network of 100 branches generates many IT calls: printer stopped, system crashed, cashier crashed. In this module, you build the PharmaSystem Help Desk module — a web system for opening, monitoring and resolving technical tickets. This connects directly with your professional experience in IT and infrastructure.

## What to Study

### Mandatory concepts (Monday and Tuesday)

1. **MVC (Model-View-Controller):** separation of responsibilities.
2. **HTML Templates:** Jinja2 (Flask) or Thymeleaf (Spring Boot).
3. **Forms and server-side validation.**
4. **Basic authentication:** login/logout, sessions, roles (admin vs. operator).
5. **Basic CSS:** Bootstrap for a fast, professional layout.
6. **Full CRUD via web interface.**

### Free study sources

**Flask + Jinja2:**
- **Flask Mega-Tutorial (Miguel Grinberg)** — chapters on templates and login.
- **Real Python — Flask Tutorial.**

**Spring Boot + Thymeleaf:**
- **Baeldung — Spring MVC + Thymeleaf.**
- **Michelli Brito Channel** (YouTube) — Spring MVC projects.

**Bootstrap:**
- **getbootstrap.com** — ready-made documentation and components.

### Estimated time

8 to 12 hours of study + construction. This module is denser.

## Daily Itinerary

### Monday — Study and Setup

- Study MVC, templates and authentication.
- Create the project and configure the database (reuse existing PostgreSQL).
- Create new tables:

```sql
users (id, name, email, password_hash, role, filial_id)
called (id, title, description, category, priority, status,
          filial_id, usuario_abertura_id, usuario_responsavel_id,
          opening_date, closing_date)
comments_call (id, called_id, user_id, text, date)
```

### Tuesday — Authentication

- Implement user registration and login.
- Configure sessions and route protection.
- Create two roles: `admin` (central IT) and `operator` (branch employee).
- Login page with Bootstrap.

### Wednesday — CRUD of Calls

- Call opening screen (form with: title, description, category, priority).
- List of tickets (table with filters: status, priority, branch).
- Call details screen (view information, add comments).
- Functionality to change status (Open → In Progress → Resolved → Closed).

### Thursday — Internal Dashboard + Extra Features

- Dashboard page with counters:
  - Open calls.
  - Calls in progress.
  - Tickets resolved this month.
  - Average resolution time.
- Add filter by branch and period.
- Admin can assign ticket to a technician.
- Operator only sees calls from his branch.

### Friday — Visual Polishing and Testing

- Review all screens: alignment, responsiveness, clear error messages.
- Test complete flows: register → log in → open ticket → comment → resolve → view on dashboard.
- Add visual feedback: success toast, priority badge (red = urgent), icons.

### Saturday — Documentation and Prints

- Take screenshots of each main screen (login, list, details, dashboard).
- Write the README.md.
- Create a visual navigation flow (simple diagram showing screens and transitions).

### Sunday — Publication

- Push on GitHub.
- Publish on LinkedIn with screenshots.

## Deliverables

- Functional web system with authentication and CRUD.
- At least 6 screens (login, registration, list, new ticket, details, dashboard).
- Two roles with different permissions.
- Prints of each screen.
- Complete README.md.

## Publication Checklist

**GitHub:**

- [ ] Organized MVC code.
- [ ] requirements.txt or pom.xml.
- [ ] Prints of screens in `docs/`.
- [ ] README with: Description, Features, Prints, How to Execute, Technologies.

**LinkedIn:**

- [ ] 3 to 4 prints of the most beautiful screens (dashboard, call list, details).
- [ ] Text explaining: problem solved (IT ticket management), features, design decisions.
- [ ] Hashtags: #WebDev #Flask #SpringBoot #HelpDesk #FullStack #PortfólioDev

---

---

# MODULE 07 — Requirements Engineering

## Context in PharmaSystem

Now you change hats: instead of a developer, you are the systems engineer who formally documents the PharmaSystem. This module is what differentiates a programmer from an engineer. You produce a professional requirements document that could be presented to a real client.

## What to Study

### Mandatory concepts (Monday and Tuesday)

1. **Types of requirements:** functional (RF) vs. non-functional (RNF).
2. **Elicitation techniques:** interviews, brainstorming, document analysis.
3. **Requirements specification:** IEEE 830 (simplified) format.
4. **Use cases:** actors, main and alternative flows, pre/post-conditions.
5. **UML — Use case diagrams:** actors, ellipses, relationships (include, extend).
6. **UML — Class diagram:** classes, attributes, methods, relationships (association, aggregation, composition, inheritance).
7. **UML — Sequence diagram:** lifelines, messages, returns.
8. **UML — Activity diagram:** process flow.

### Free study sources

- **Lucidchart UML Tutorials** — visual examples of each diagram.
- **UML Diagrams (uml-diagrams.org)** — complete reference.
- **draw.io (app.diagrams.net)** — free tool for creating UML diagrams.
- **PlantUML** (plantuml.com) — generates UML diagrams from text (ideal for versioning on GitHub).

### Estimated time

6 to 8 hours of study (concepts + practice with the diagram tool).

## Daily Itinerary

### Monday — Requirements Study

- Study types of requirements and the IEEE 830 format.
- Study use cases: how to write, examples.
- Start listing PharmaSystem requirements based on everything you've already built.

### Tuesday — UML Study + Survey

- Study use case, class, sequence and activity diagrams.
- Install draw.io or configure PlantUML.
- Complete the list of requirements.

### Wednesday — Requirements Document

Write the PharmaSystem Requirements Document with these sections:

1. **Introduction:** purpose, scope, definitions.
2. **General description:** product perspective, main functions, user characteristics, restrictions.
3. **Functional requirements (RF):**
   - RF01: The system must allow the registration of branches.
   - RF02: The system must allow the registration of products with cost and sales prices.
   - RF03: The system must record sales with items and payment methods.
   - RF04: The system must generate monthly billing reports.
   - (Continue until at least RF20.)
4. **Non-functional requirements (RNF):**
   - RNF01: The system must support 100 simultaneous branches.
   - RNF02: API response time must be less than 500ms.
   - RNF03: The system must maintain audit logs.
   - (At least 10 RNFs.)
5. **Business rules.**

### Thursday — Use Cases and UML Diagrams

**Use cases (write 5 complete):**

Example use case:

- **UC01 — Register Sale**
  - Actor: Cashier.
  - Precondition: Operator authenticated in the system.
  - Main flow: (step by step).
  - Alternative flows: product out of stock, customer not registered.
  - Post-condition: registered sale, updated stock.

**Diagrams:**

- Use Case Diagram (system general).
- Class Diagram (all entities + relationships).

### Friday — Sequence and Activity Diagrams

- Sequence Diagram for the "Register Sale" use case (showing: Operator → Interface → Controller → Service → Database).
- Sequence Diagram for "Open IT Call".
- Activity Diagram for the complete flow of a ticket (Open → Triage → In Progress → Resolved → Closed).

### Saturday — Review and Documentation

- Review the requirements document: is it clear? Would a new developer be able to implement the system just by reading it?
- Export all diagrams as images.
- Write the README.md.

### Sunday — Publication

- Push on GitHub (document in `.md` or `.pdf`, diagrams in `diagrams/`).
- Post on LinkedIn with one or two UML diagrams.

## Deliverables

- Complete Requirements Document (20+ RF, 10+ RNF).
- 5 written Use Cases.
- Use Case Diagram.
- Class Diagram.
- 2 Sequence Diagrams.
- 1 Activity Diagram.
- README.md.

## Publication Checklist

**GitHub:**

- [ ] Requirements document in `docs/`.
- [ ] Diagrams in `diagrams/` (PNG + PlantUML source or draw.io).
- [ ] README with: Description, Prints of Diagrams, Methodology Used.

**LinkedIn:**

- [ ] Class or sequence diagram (strong visual).
- [ ] Text focusing: "in addition to programming, I formally documented the system engineering".
- [ ] Hashtags: #UML #SystemsEngineering #Requirements #SystemsEngineering #DevPortfolio

---

---

# MODULE 08 — Systems Architecture

## Context in PharmaSystem

Now you are the architect. In this module, you design the complete PharmaSystem architecture as if you were going to present it to a company's CTO. This includes components, integrations, databases, APIs, queues, and infrastructure. This module shows end-to-end engineering vision.

## What to Study

### Mandatory concepts (Monday and Tuesday)

1. **Architectural styles:** monolithic, microservices, serverless, event-driven.
2. **Standards:** API Gateway, BFF (Backend for Frontend), CQRS, Event Sourcing.
3. **C4 Model:** Context, Container, Component, Code — abstraction levels for documenting architecture.
4. **Infrastructure diagrams:** servers, load balancers, banks, caches, queues.
5. **Integrations:** REST, messaging (RabbitMQ, conceptual Kafka), webhooks.
6. **Architectural Decisions (ADR — Architecture Decision Record):** format for documenting "why" you chose something.

### Free study sources

- **C4 Model** (c4model.com) — official reference with examples.
- **Martin Fowler — Architecture** (martinfowler.com) — articles about patterns.
- **draw.io / Mermaid** — to create diagrams.
- **GitHub — ADR Templates** — search for "adr template" to see examples.

### Estimated time

6 to 8 hours of study. The rest is construction of diagrams and documents.

## Daily Itinerary

### Monday — Study

- Study architectural styles and when to use each one.
- Study the C4 Model (Context, Container, Component).
- Read 2 to 3 examples of ADRs.

### Tuesday — Definition of Architecture

Define the PharmaSystem architecture. Structure suggestion:

```
[App Mobile Branches] → [API Gateway] → [Sales Service] → [PostgreSQL]
[Web Admin Portal] → [API Gateway] → [Inventory Service] → [PostgreSQL]
[Dashboard BI] → [Reporting Service] → [PostgreSQL]
                                           [Help Desk Service] → [PostgreSQL]
                                           [ETL Pipeline] → [PostgreSQL]
                           [Message Queue (RabbitMQ)]
                              ↑ sale events, called
```

### Wednesday — C4 Diagrams

Create the first 3 levels of C4:

**Level 1 — Context:** PharmaSystem and its external actors (operators, managers, IT technicians, external systems such as SEFAZ, suppliers).

**Level 2 — Container:** API Gateway, each microservice, database, queue, dashboard.

**Level 3 — Component:** internal detail of 1 microservice (e.g.: Sales Service → Controller, Service, Repository, Validator).

### Thursday — Infrastructure Diagram + Flows

- Infrastructure diagram: where each component runs (servers, cloud, containers).
- Flow diagram: how a sale moves through the system (cash → API → validation → bank → event → stock update → notification).
- Integration diagram: how PharmaSystem would integrate with external systems (SEFAZ for NF-e, suppliers for replacement).

### Friday — ADRs (Architecture Decision Records)

Write at least 3 ADRs:

- **ADR-001:** Why we choose microservices architecture over monolith.
- **ADR-002:** Why PostgreSQL as primary database.
- **ADR-003:** Why REST API instead of GraphQL.

Format of each ADR:

```
#ADR-001: Microservices Architecture

## Status
Accept

## Context
PharmaSystem serves 100 branches with sales, inventory,
help desk and reports. Each module has different update cycles.

## Decision
Adopt microservices architecture with API Gateway.

## Consequences
Positive: independent deployment, scalability per module.
Negatives: operational complexity, need for orchestration.
```

### Saturday — Final Documentation

- Compile everything into a cohesive architecture document.
- Organize: Overview → C4 (Context, Container, Component) → Infrastructure → Flows → ADRs.
- Write the README.md.

### Sunday — Publication

- Push on GitHub.
- Publish on LinkedIn with the C4 Container diagram (the most visual and impactful).

## Deliverables

- Diagram C4 — Level 1 (Context).
- Diagram C4 — Level 2 (Container).
- Diagram C4 — Level 3 (Component) of 1 service.
- Infrastructure diagram.
- Sales flow diagram.
- 3 ADRs.
- README.md.

## Publication Checklist

**GitHub:**

- [ ] Diagrams in `diagrams/`.
- [ ] ADRs in `docs/adrs/`.
- [ ] Architecture document in `docs/`.
- [ ] README with: Overview, Diagrams, ADRs, Technologies.

**LinkedIn:**

- [ ] C4 Container Diagram (the most visual).
- [ ] Text explaining: systemic vision, decisions made and their trade-offs.
- [ ] Hashtags: #Architecture #SystemDesign #C4Model #Microservices #PortfólioDev

---

---

# MODULE 09 — Data Engineering

## Context in PharmaSystem

The pharmacy chain doesn't want to rely on manual CSVs. In this module, you build a data engineering pipeline that consumes an external (mock) API, processes the data, and feeds an automated dashboard. This complements Module 04's ETL with a more modern, API-driven approach.

## What to Study

### Mandatory concepts (Monday and Tuesday)

1. **Difference between ETL and modern ELT.**
2. **Consumption of APIs with Python:** `requests`, pagination, authentication.
3. **Data Lake vs. Data Warehouse (conceptual).**
4. **Airflow (conceptual):** DAGs, tasks, scheduling — understand the concept even without installing.
5. **Data quality:** validations, schema tests, Great Expectations (conceptual).

### Free study sources

- **Real Python — Working with APIs** — API consumption tutorial.
- **Requests documentation** (docs.python-requests.org).
- **Airflow official docs** — read the "Concepts" section to understand DAGs.
- **Articles on Modern Data Stack** — Towards Data Science, Data Engineering Weekly.

### Estimated time

5 to 7 hours of study.

## Daily Itinerary

### Monday — Study and Planning

- Study the concepts and the difference between traditional ETL and modern data pipelines.
- Plan the pipeline:

```
[PharmaSystem API (Module 05)] → [Python Ingestion] → [Staging SQL] → [Transformation] → [Analytical Tables] → [Dashboard]
```

### Tuesday — Mock API (if needed) + Ingestion

- If the Module 05 API is not running, create a mock version with Flask that returns JSONs for sales, products and branches.
- Write the ingestion script:
  - Consumes all API endpoints.
  - Saves the raw data in `staging_*` tables in the database.
  - Log everything.

### Wednesday — Transformation

- Write transformation scripts that read from `staging_*` and create analytic tables:
  - `fato_vendas` — denormalized fact table with all sales information.
  - `dim_tempo` — temporal dimension (year, month, quarter, day of the week).
  - `dim_filial` — dimension of branches.
  - `dim_produto` — product dimension with category.
- Apply the concept of Star Schema.

### Thursday — Data Quality + Dashboard

- Add validations: record counting (staging vs. analytics), null checking, duplicate key checking.
- Create a simple dashboard (can be with Streamlit to be different from Module 02):
  - Billing per period.
  - Top products.
  - Comparison between branches.
  - Powered directly from analytical tables.

### Friday — Orchestration (Conceptual) + Master Script

- Create an `orquestrador.py` script that runs the complete pipeline in order:
  1. Ingestion.
  2. Transformation.
  3. Validation.
  4. (Optional) Update the dashboard.
- Write a document explaining how this would be orchestrated with Airflow in production (conceptual DAG, schedule, dependencies).

### Saturday — Documentation

- Create complete pipeline diagram.
- Document the Star Schema with ER diagram of analytical tables.
- Write the README.md.

### Sunday — Publication

- Push on GitHub.
- Publish on LinkedIn with the pipeline diagram and a screenshot of the dashboard.

## Deliverables

- Ingestion, transformation, validation and orchestration scripts.
- Analytical tables with Star Schema implemented.
- Dashboard (Streamlit or other).
- Pipeline diagram.
- Star Schema Diagram.
- Conceptual document for orchestration with Airflow.
- README.md.

## Publication Checklist

**GitHub:**

- [ ] Scripts organized into `ingestao/`, `transformacao/`, `validacao/`.
- [ ] Diagrams in `docs/`.
- [ ] README with: Pipeline, Star Schema, How to Execute, Dashboard.

**LinkedIn:**

- [ ] Pipeline diagram.
- [ ] Print from the Streamlit dashboard.
- [ ] Text: difference between simple ETL and data pipeline, modeling decisions.
- [ ] Hashtags: #DataEngineering #Pipeline #StarSchema #Streamlit #PortfolioDev

---

---

# MODULE 10 — MBSE (Model-Based Systems Engineering)

## Context in PharmaSystem

MBSE is what turns a developer into a systems engineer. In this module, you apply model-based modeling to PharmaSystem, treating it as a complete system with requirements, blocks, interfaces, and flows — using the same approach you would use to design a drone, a satellite, or an industrial plant.

## What to Study

### Mandatory concepts (Monday and Tuesday)

1. **What is MBSE:** modeling as a source of truth (vs. traditional textual documentation).
2. **SysML (summary):** difference between UML and SysML, main diagrams.
3. **Requirements Diagram (SysML):** represent requirements as blocks with traceability.
4. **Block Diagram (BDD — Block Definition Diagram):** system structure.
5. **Internal Block Diagram (IBD — Internal Block Diagram):** interfaces and flows between blocks.
6. **Activity Diagram (already studied in Module 07, now with data flows between subsystems).**
7. **Requirements traceability:** how to link each requirement to a block, test and use case.

### Free study sources

- **INCOSE Systems Engineering Handbook** — summaries available online.
- **SysML Distilled (summaries)** — search for "SysML tutorial" on YouTube.
- **Sparx Systems — SysML Tutorial** (sparxsystems.com/resources/tutorials/sysml).
- **PlantUML** — supports some SysML diagrams.
- **draw.io** — BDD and IBD templates available.

### Estimated time

6 to 10 hours. MBSE is more conceptual and may be new to you, so allow extra time.

## Daily Itinerary

### Monday — MBSE and SysML Study

- Watch 2-3 videos on MBSE and SysML.
- Read the Sparx Systems tutorial.
- Understand the difference between UML (software focus) and SysML (system focus).

### Tuesday — Requirements Diagram

- Take the requirements from Module 07 and represent them in a SysML Requirements Diagram.
- Show:
  - High-level requirements deriving into sub-requirements.
  - Relationships: derive, satisfy, verify.
- Example: `REQ-001: Sales Management` → derives into `REQ-001.1: Register Sale`, `REQ-001.2: Cancel Sale`, etc.

### Wednesday — Block Diagram (BDD)

- Model the PharmaSystem as a block system:

```
<<system>> PharmaSystem
  ├── <<subsystem>> Sales Module
  ├── <<subsystem>> Stock Module
  ├── <<subsystem>> Help Desk Module
  ├── <<subsystem>> Reporting Module
  ├── <<subsystem>> Data Pipeline
  └── <<subsystem>> Integration Gateway
```

- Show composition and associations between blocks.

### Thursday — Internal Block Diagram (IBD)

- Choose a subsystem (e.g.: Sales Module) and detail internally:
  - Ports: cashier data input, sales event output.
  - Flows: data, signals, calls.
  - Interfaces with other subsystems.
- Create an IBD showing how the Sales Module connects to the Inventory Module and the Data Pipeline.

### Friday — Traceability Matrix

- Create a traceability matrix by linking:
  - Requirement → Block that satisfies → Related use case → Test that verifies.
- Example in table format:

| Requirement | Block | Use Case | Test |
|---|---|---|---|
| RF01 | Sales Module | UC01 — Register Sale | TC01 — Successful sale |
| RF05 | Stock Module | UC03 — Check Stock | TC05 — Updated stock |

- At least 10 lines.

### Saturday — Documentation

- Compile the diagrams into a cohesive MBSE document.
- Write an introduction explaining what MBSE is and why it was applied.
- Write the README.md.

### Sunday — Publication

- Push on GitHub.
- Publish on LinkedIn with BDD (more visual and differentiated diagram).

## Deliverables

- SysML Requirements Diagram.
- Block Diagram (BDD) of the complete system.
- Internal Block Diagram (IBD) of a subsystem.
- Activity Diagram with flow between subsystems.
- Traceability Matrix (10+ lines).
- Compiled MBSE document.
- README.md.

## Publication Checklist

**GitHub:**

- [ ] Diagrams in `diagrams/`.
- [ ] MBSE document in `docs/`.
- [ ] Traceability matrix in `docs/`.
- [ ] README with: What is MBSE, Diagrams, Traceability.

**LinkedIn:**

- [ ] BDD diagram (strong and differentiated visual).
- [ ] Text explaining: what MBSE is, why you applied to PharmaSystem, how it adds value.
- [ ] Hashtags: #MBSE #SysML #SystemsEngineering #SystemEngineering #PortfólioDev

---

---

# MODULE 11 — Integrative Project

## Context in PharmaSystem

This is the convergence module. You take everything you built — database, API, dashboard, pipeline, web system — and integrate it into an end-to-end flow that works together. The goal is to prove that you not only know how to make each part, but you know how to make the entire system work.

## What to Study

In this module, study is replaced by review. You don't learn anything new; you make the previous modules talk to each other.

### What to review (Monday)

- Review the API (Module 05): does it still work? Are the endpoints accessible?
- Review the ETL (Module 04): does it load data correctly?
- Review the web system (Module 06): can you consume the API?
- Review the dashboard (Module 02/09): is it connected to the analytical tables?

## Daily Itinerary

### Monday — Inventory and Integration Planning

- List all existing components and their current state.
- Set the integrated flow:

```
[Branch] → Sale registered via [Web System or API]
       → Data persisted in [PostgreSQL]
       → [Pipeline ETL] processes and feeds [analytical tables]
       → [Dashboard] shows updated indicators
       → [Help Desk] allows opening calls
       → Everything documented in [Requirements + Architecture + MBSE]
```

- Identify integration points that are disconnected.

### Tuesday — Connect API to the Web System

- Make the Module 06 web system consume the Module 05 API to list products and branches (instead of querying the bank directly).
- Example: the ticket opening screen loads the list of branches via `GET /api/filiais`.

### Wednesday — Connect Pipeline to Dashboard

- Ensure that the Module 09 pipeline feeds the tables that the dashboard consumes.
- Run: API → Ingestion → Transformation → Dashboard updated.
- Add a "last updated" feature to the dashboard.

### Thursday — Complete End-to-End Flow

- Demonstrate the complete flow:
  1. Register a product via API.
  2. Register a sale via API or web system.
  3. Run the pipeline.
  4. Check the updated indicator on the dashboard.
  5. Open a ticket in the Help Desk.
- Record prints or GIFs of each step.

### Friday — Integration Tests and Fixes

- Run everything from scratch and note problems.
- Fix integration bugs.
- Write a step-by-step demonstration script (like a "demo script" to present to a recruiter or teacher).

### Saturday — Integrator Documentation

- Create an integration diagram showing how each module connects.
- Write the README.md explaining: what was integrated, how to run, demo script.
- Update the root README.md of the `pharma-system/` repository with the overview of all modules.

### Sunday — Publication

- Push on GitHub.
- Publish on LinkedIn showing the end-to-end flow.

## Deliverables

- Functional integrations between modules.
- Demonstration of the end-to-end flow documented (prints or GIFs).
- Demo script (presentation script).
- Integration diagram.
- Module README.md + root README.md updated.

## Publication Checklist

**GitHub:**

- [ ] Integration code.
- [ ] Prints/GIFs from the end-to-end flow in `docs/`.
- [ ] Demo script in `docs/`.
- [ ] Root README updated with overview of all 11 modules.

**LinkedIn:**

- [ ] Integration diagram.
- [ ] GIF or sequence of prints from the end-to-end flow.
- [ ] Text: "I integrated all the modules in my portfolio into a functional system".
- [ ] Hashtags: #Integração #FullStack #EndToEnd #EngenhariaDeSistemas #PortfólioDev

---

---

# MODULE 12 — Final Project

## Context in PharmaSystem

This is the closing module. Here you don't build anything new — you polish, refine, and package everything like a professional product. The goal is for any recruiter who logs into your GitHub to see a cohesive, well-documented, and impressive project.

## What to Do

### Monday — General Code Review

- Go through all the modules.
- Standardize variable and function names.
- Remove commented code and forgotten debugs.
- Ensure that each module has a `requirements.txt` or equivalent.
- Check that everything runs from the README (if someone follows the instructions, will it work?).

### Tuesday — README Raiz Profissional

Rewrite the repository root README.md with professional quality:

```markdown
# PharmaSystem — Management System for Pharmacy Network

## About the Project
PharmaSystem is a complete ecosystem for managing a network
of pharmacies with 100 branches, developed as an academic portfolio
of Systems Engineering.

## Architecture
[Image of C4 Container diagram]

## Modules
| # | Module | Technologies | Description |
|---|-----------|-------------|-----------|
| 01 | SQL | PostgreSQL | Sales Database |
| 02 | Power BI | Power BI, DAX | Executive dashboard |
| ... | ... | ... | ... |

## Technology Stack
Python, Flask/Spring Boot, PostgreSQL, Power BI, Streamlit,
Pandas, UML, SysML, MBSE

## How to Execute
[General instructions + links to each module]

## About the Author
[Your name, course, university, LinkedIn, contact]
```

### Wednesday — Visual Documentation

- Re-export all diagrams in high resolution.
- Create a folder `docs/presentation/` with the best images from each module.
- If possible, record a 2 to 3 minute video showing the system running (Loom or OBS).

### Thursday — Feature Extra (Differential)

Add extra functionality that impresses:

Suggestions:

- **Simple prediction:** use scikit-learn to predict next month's sales with linear regression (even if simple, it shows that you know how to integrate ML).
- **Notification:** the pipeline sends a summary via email when it processes new data.
- **JWT authentication in the API:** replace sessions with JWT tokens (more professional).
- **Docker Compose:** create a `docker-compose.yml` that runs database + API + dashboard with one command.

Choose ONE and implement.

### Friday — Final Test + Video

- Run the entire system from scratch by following just the README.
- If something doesn't work, fix it.
- Record the demonstration video (if you didn't do it on Thursday).

### Saturday — Final Publication on GitHub

- Make the final push.
- Add tags/releases on GitHub (v1.0).
- Pin the repository to your GitHub profile.
- Verify that the root README renders beautifully with images and tables.

### Sunday — Final Publication on LinkedIn

- Publish the final post: a look back at the 12 weeks.
- Post template:

> Over the past 12 weeks, I have built PharmaSystem — a complete system
> management for a pharmacy chain with 100 branches.
>
> What I learned and applied:
> - SQL and data modeling
> - Dashboards with Power BI and Streamlit
> - Exploratory analysis with Python and Pandas
> - Automated ETL Pipeline
> - REST API with [Flask/Spring Boot]
> - Web system with authentication
> - Requirements engineering and UML
> - Systems architecture (C4 Model)
> - Data engineering with Star Schema
> - MBSE with SysML
> - End-to-end integration
>
> Everything documented, versioned and accessible on GitHub.
>
> [Link to repository]

## Final Deliverables

- Complete and polished repository.
- PRO ROOT README.
- Extra feature implemented.
- Demo video (optional, but highly recommended).
- Final post on LinkedIn.

---

---

# Visual Schedule Summary

```
Week Module Main Focus Key Delivery
────── ──────────────────────── ───────────────────────── ──────────────────────
  01 SQL Data Foundation 20+ SQL Queries
  02 Power BI Executive view Dashboard 3 pages
  03 Python + Pandas Exploratory analysis Notebook + graphs
  04 ETL Automated Pipeline Modular Scripts
  05 REST API Backend 15+ endpoints
  06 Functional Full Stack Help Desk Web System
  07 Requirements Engineering Formal documentation Requirements + UML
  08 Architecture Systemic view C4 + ADRs
  09 Data Engineering Modern data pipeline Star Schema + Streamlit
  10 MBSE Systems Modeling BDD + IBD + Trace
  11 Integrator Connect everything End-to-end flow
  12 Final Project Polishing + professional README publication
```

---

# General Tips for Success

**1. Don't aim for perfection in the first version.** Publish the working minimum on Sunday and then improve over the following week if necessary. Publishing consistently is more valuable than having a perfect project 6 months from now.

**2. Use transportation and waiting time to study.** Videos and study articles can be consumed on your cell phone. Reserve the computer for construction.

**3. If you get stuck on a module, simplify the scope, don't delay.** Better to deliver 15 SQL queries than not publish anything because you wanted to do 30. You can always come back and improve later.

**4. The README is as important as the code.** Recruiters rarely read the entire code. They read the README. Dedicate time to it.

**5. Every LinkedIn post should tell a story:** what the problem was → what you did → what you learned. Don't be too technical; think about the recruiter who is not a programmer.

**6. Keep a personal “learnings” file.** Write down mistakes, solutions, and insights from each week. At the end of the 12 weeks, this material is interview gold: "in week 4, I faced an idempotence problem in ETL and solved it with UPSERT" demonstrates technical maturity.

---

# Versão em Português

# Apostila — Portfólio de Engenharia de Sistemas em 12 Semanas

**Projeto Guarda-Chuva: PharmaSystem — Sistema de Gestão para Rede de Farmácias**

> Cada semana é um módulo do mesmo ecossistema. Ao final, o recrutador verá no seu GitHub uma evolução coerente: modelagem → API → dashboard → arquitetura → integração total.

---

## Como Usar Esta Apostila

Cada módulo segue a mesma estrutura:

- **Contexto:** onde este módulo se encaixa no PharmaSystem.
- **O que estudar:** conteúdos teóricos com fontes gratuitas.
- **Roteiro diário:** divisão prática de segunda a domingo.
- **Entregáveis:** o que precisa estar pronto no domingo à noite.
- **Checklist de publicação:** GitHub + LinkedIn.

**Regra de ouro:** estude de segunda a quarta, construa de quinta a sábado, publique no domingo.

---

## Visão Geral do PharmaSystem

O PharmaSystem é um sistema fictício (mas realista) para uma rede de farmácias com 100 filiais. Ao longo das 12 semanas, você vai construir camada por camada:

```
Semana 1   → Banco de dados (vendas)
Semana 2   → Dashboard executivo (Power BI)
Semana 3   → Análise com Python/Pandas
Semana 4   → Pipeline ETL automatizado
Semana 5   → API REST
Semana 6   → Sistema Web (Help Desk interno)
Semana 7   → Documentação de Engenharia de Requisitos
Semana 8   → Projeto de Arquitetura do sistema completo
Semana 9   → Pipeline de Engenharia de Dados
Semana 10  → Modelagem MBSE
Semana 11  → Integração de todos os módulos
Semana 12  → Projeto final completo + README profissional
```

**Repositório GitHub:** crie um repositório chamado `pharma-system` com uma pasta por módulo:

```
pharma-system/
├── README.md                  ← visão geral do projeto
├── modulo-01-sql/
├── modulo-02-powerbi/
├── modulo-03-python-pandas/
├── modulo-04-etl/
├── modulo-05-api-rest/
├── modulo-06-sistema-web/
├── modulo-07-requisitos/
├── modulo-08-arquitetura/
├── modulo-09-engenharia-dados/
├── modulo-10-mbse/
├── modulo-11-integracao/
└── modulo-12-projeto-final/
```

---

---

# MÓDULO 01 — SQL para Análise de Dados

## Contexto no PharmaSystem

Toda rede de farmácias precisa de um banco de dados de vendas robusto. Neste módulo, você cria a fundação de dados sobre a qual todo o restante do portfólio será construído. Sem este banco, não há dashboard, não há ETL, não há API.

## O Que Estudar

### Conceitos obrigatórios (segunda e terça)

1. **Modelo Relacional:** entidades, atributos, chaves primárias, chaves estrangeiras, normalização (1FN, 2FN, 3FN).
2. **DDL:** CREATE TABLE, ALTER TABLE, DROP TABLE, tipos de dados (INT, VARCHAR, DECIMAL, DATE, TIMESTAMP).
3. **DML:** INSERT, UPDATE, DELETE.
4. **Consultas:** SELECT, WHERE, ORDER BY, GROUP BY, HAVING, LIMIT.
5. **Junções:** INNER JOIN, LEFT JOIN, RIGHT JOIN.
6. **Funções de agregação:** COUNT, SUM, AVG, MIN, MAX.
7. **Subconsultas e CTEs (WITH).**

### Fontes de estudo gratuitas

- **W3Schools SQL Tutorial** — referência rápida para sintaxe.
- **SQLBolt** (sqlbolt.com) — exercícios interativos progressivos.
- **Mode Analytics SQL Tutorial** — foco em análise de dados com SQL.
- **Documentação oficial do PostgreSQL** — para consulta de funções específicas.

### Tempo estimado de estudo teórico

Cerca de 6 a 8 horas distribuídas em dois dias (segunda e terça). Se você já tem familiaridade com SQL, pode reduzir para 3 a 4 horas e adiantar a construção.

## Roteiro Diário

### Segunda-feira — Fundamentos e Modelagem

**Manhã/Tarde (estudo):**

- Estude modelo relacional e normalização.
- Assista a um vídeo ou leia um tutorial sobre modelagem de banco de dados.

**Noite (prática inicial):**

- Instale o PostgreSQL e o DBeaver (se ainda não tiver).
- Crie o banco `pharma_system`.
- Projete o diagrama ER no papel ou no draw.io com estas entidades:

```
filiais (id, nome, cidade, estado, data_abertura)
categorias (id, nome)
produtos (id, nome, categoria_id, preco_custo, preco_venda, estoque_minimo)
clientes (id, nome, cpf, email, telefone, data_cadastro)
vendas (id, filial_id, cliente_id, data_venda, valor_total, forma_pagamento)
itens_venda (id, venda_id, produto_id, quantidade, preco_unitario, subtotal)
```

### Terça-feira — DDL e Inserção de Dados

**Manhã (estudo):**

- Estude DDL, tipos de dados, constraints (NOT NULL, UNIQUE, CHECK, FOREIGN KEY).

**Tarde/Noite (construção):**

- Escreva os scripts `CREATE TABLE` com todas as constraints.
- Insira dados realistas: pelo menos 10 filiais, 50 produtos, 100 clientes e 500 vendas.
- Dica: use ChatGPT ou um script Python para gerar INSERTs em massa com dados que façam sentido para farmácias (medicamentos, cosméticos, higiene).

### Quarta-feira — Consultas Básicas e Intermediárias

**Dia inteiro (construção):**

Crie pelo menos 20 consultas SQL organizadas por categoria. Exemplos:

**Vendas gerais:**

1. Faturamento total da rede.
2. Faturamento por filial.
3. Faturamento por mês.
4. Ticket médio geral.
5. Ticket médio por filial.

**Produtos:**

6. Top 10 produtos mais vendidos (quantidade).
7. Top 10 produtos com maior faturamento.
8. Produtos que nunca foram vendidos.
9. Média de preço por categoria.
10. Margem de lucro por produto (preco_venda - preco_custo).

**Clientes:**

11. Clientes que mais compraram (valor).
12. Clientes que mais compraram (frequência).
13. Clientes sem compra nos últimos 90 dias.
14. Distribuição de clientes por filial.

**Temporal:**

15. Vendas por dia da semana.
16. Comparativo mês a mês.
17. Melhor e pior mês de vendas.

**Avançadas:**

18. Ranking de filiais usando Window Function (RANK, ROW_NUMBER).
19. Média móvel de vendas por mês (Window Function).
20. CTE para calcular o crescimento percentual mês a mês.

### Quinta-feira — Consultas Avançadas e Refinamento

**Dia inteiro:**

- Revise e otimize as consultas.
- Adicione índices nas colunas mais consultadas.
- Crie pelo menos 2 Views para consultas frequentes (ex.: `vw_faturamento_mensal`, `vw_ranking_produtos`).
- Documente cada consulta com comentários no SQL explicando o objetivo.

### Sexta-feira — Organização e Documentação

- Organize os scripts em arquivos separados:
  - `01_schema.sql` — criação das tabelas.
  - `02_inserts.sql` — dados de exemplo.
  - `03_consultas.sql` — todas as 20+ consultas documentadas.
  - `04_views.sql` — views criadas.
- Tire prints dos resultados mais interessantes no DBeaver.
- Escreva o `README.md` do módulo.

### Sábado — Revisão e Polimento

- Releia tudo com olhar crítico: o README está claro? As consultas fazem sentido de negócio?
- Adicione um diagrama ER exportado como imagem ao repositório.
- Teste executar tudo do zero (drop → create → insert → consultas) para garantir que funciona.

### Domingo — Publicação

- Faça o push para o GitHub.
- Publique no LinkedIn.

## Entregáveis

- Diagrama ER em imagem (PNG ou SVG).
- Script de criação do banco (`01_schema.sql`).
- Script de inserção de dados (`02_inserts.sql`).
- No mínimo 20 consultas SQL documentadas (`03_consultas.sql`).
- Pelo menos 2 Views (`04_views.sql`).
- README.md com: descrição do projeto, diagrama ER, como executar, exemplos de consultas e prints dos resultados.

## Checklist de Publicação

**GitHub:**

- [ ] Código limpo e comentado.
- [ ] README com seções: Descrição, Diagrama ER, Tecnologias, Como Executar, Exemplos de Consultas, Prints.
- [ ] Imagens na pasta `docs/` ou `assets/`.

**LinkedIn:**

- [ ] Texto de 3 a 5 parágrafos.
- [ ] Mencionar: o problema de negócio, as tecnologias usadas, o que aprendeu.
- [ ] Incluir 2 a 3 imagens (diagrama ER, resultado de query interessante).
- [ ] Link para o repositório GitHub.
- [ ] Hashtags: #SQL #PostgreSQL #AnáliseDeDados #PortfólioDev #EngenhariaDeSistemas

---

---

# MÓDULO 02 — Power BI

## Contexto no PharmaSystem

Os dados existem no banco, mas a diretoria de uma rede de farmácias precisa de visibilidade rápida. Neste módulo, você transforma os dados brutos do Módulo 01 em um dashboard executivo interativo — exatamente o tipo de entregável que analistas de dados produzem no dia a dia.

## O Que Estudar

### Conceitos obrigatórios (segunda e terça)

1. **Interface do Power BI Desktop:** painéis, abas (Relatório, Dados, Modelo).
2. **Conexão a fontes de dados:** importar de PostgreSQL ou de arquivo CSV.
3. **Power Query (M):** renomear colunas, alterar tipos, remover duplicatas, criar colunas calculadas.
4. **Modelo de dados:** relacionamentos entre tabelas (1:N, N:N), tabela fato vs. dimensão (Star Schema básico).
5. **DAX básico:** CALCULATE, SUM, AVERAGE, COUNTROWS, DIVIDE, FILTER, ALL, DATEADD, SAMEPERIODLASTYEAR.
6. **Visuais:** gráfico de barras, de linhas, de pizza, cartões (KPI), tabelas, segmentadores (slicers), mapas.
7. **Formatação e design:** paleta de cores, alinhamento, contraste, hierarquia visual.

### Fontes de estudo gratuitas

- **Microsoft Learn — Power BI** (learn.microsoft.com) — trilha oficial, gratuita e com certificado.
- **Canal Hashtag Treinamentos** (YouTube, PT-BR) — tutoriais práticos de Power BI.
- **Canal Karine Lago** (YouTube, PT-BR) — foco em dashboards profissionais.
- **DAX Guide** (dax.guide) — referência para funções DAX.

### Tempo estimado

Cerca de 6 horas de estudo teórico. Se já usou Power BI antes, vá direto para a construção.

## Roteiro Diário

### Segunda-feira — Estudo e Preparação dos Dados

**Manhã (estudo):**

- Assista a tutoriais sobre conexão de dados e Power Query.
- Entenda o conceito de Star Schema (tabela fato + dimensões).

**Tarde/Noite (prática):**

- Exporte os dados do banco do Módulo 01 para CSVs (uma tabela por arquivo) ou conecte diretamente ao PostgreSQL.
- Importe no Power BI e configure os relacionamentos no modelo.
- Limpe os dados no Power Query: tipos corretos, nomes claros, remoção de inconsistências.

### Terça-feira — Estudo de DAX e Primeiras Medidas

**Manhã (estudo):**

- Estude as funções DAX mais usadas: SUM, AVERAGE, CALCULATE, COUNTROWS.
- Entenda o conceito de contexto de filtro.

**Tarde/Noite (construção):**

Crie estas medidas DAX:

- `Faturamento Total = SUM(itens_venda[subtotal])`
- `Ticket Médio = DIVIDE([Faturamento Total], COUNTROWS(vendas))`
- `Total de Vendas = COUNTROWS(vendas)`
- `Faturamento Mês Anterior = CALCULATE([Faturamento Total], DATEADD(calendario[Data], -1, MONTH))`
- `Crescimento % = DIVIDE([Faturamento Total] - [Faturamento Mês Anterior], [Faturamento Mês Anterior])`
- Crie uma tabela de calendário (Calendario) com `CALENDAR(MIN(vendas[data_venda]), MAX(vendas[data_venda]))`.

### Quarta-feira — Construção do Dashboard (Página 1: Visão Geral)

**Dia inteiro (construção):**

Crie a primeira página do dashboard com:

- **Cartões (KPIs):** Faturamento Total, Total de Vendas, Ticket Médio, Crescimento %.
- **Gráfico de linhas:** Faturamento mensal (eixo X = mês, eixo Y = faturamento).
- **Gráfico de barras horizontal:** Top 10 filiais por faturamento.
- **Segmentadores:** Período (mês/ano), Estado, Filial.
- Aplique uma paleta de cores consistente (use tons de verde/azul para farmácia).

### Quinta-feira — Dashboard (Página 2: Produtos + Página 3: Clientes)

**Página 2 — Produtos:**

- Gráfico de barras: Top 10 produtos mais vendidos.
- Gráfico de pizza/donut: Faturamento por categoria.
- Tabela: Produtos com margem de lucro (preco_venda - preco_custo).
- Cartão: Produto mais vendido do período selecionado.

**Página 3 — Clientes:**

- Cartões: Total de clientes, Clientes ativos (compraram nos últimos 90 dias).
- Gráfico de barras: Top 10 clientes por valor gasto.
- Gráfico de linhas: Evolução de novos cadastros por mês.
- Segmentador: Filial.

### Sexta-feira — Refinamento Visual e Interatividade

- Adicione tooltips customizados (ao passar o mouse, mostrar detalhes).
- Configure drill-down: ao clicar em uma filial, filtrar tudo para ela.
- Adicione botões de navegação entre páginas.
- Ajuste fontes, cores, alinhamentos — tudo profissional.
- Adicione um título e logotipo fictício "PharmaSystem" no cabeçalho.

### Sábado — Documentação e Prints

- Tire prints de cada página do dashboard (PNG de alta qualidade).
- Exporte o .pbix.
- Escreva o README.md com: descrição do dashboard, prints, medidas DAX criadas, como conectar aos dados, o que cada página mostra.

### Domingo — Publicação

- Push no GitHub (pasta `modulo-02-powerbi/`).
- Publique no LinkedIn com prints do dashboard.

## Entregáveis

- Arquivo `.pbix` do Power BI.
- Pelo menos 3 páginas de dashboard (Visão Geral, Produtos, Clientes).
- Mínimo de 5 medidas DAX.
- Prints de cada página do dashboard.
- README.md completo.

## Checklist de Publicação

**GitHub:**

- [ ] Arquivo .pbix na pasta do módulo.
- [ ] Prints em `docs/`.
- [ ] README com: Descrição, Prints, Medidas DAX, Fonte dos Dados, Como Abrir.

**LinkedIn:**

- [ ] Prints do dashboard (2 a 3 imagens chamativas).
- [ ] Texto explicando: qual problema de negócio o dashboard resolve, KPIs escolhidos, decisão de design.
- [ ] Hashtags: #PowerBI #Dashboard #DataAnalytics #BusinessIntelligence #PortfólioDev

---

---

# MÓDULO 03 — Python + Pandas

## Contexto no PharmaSystem

A equipe de dados da rede de farmácias precisa de análises mais profundas que o SQL puro não entrega facilmente — limpeza de dados sujos, estatísticas descritivas, correlações, e exportação de relatórios automatizados. Neste módulo, você usa Python e Pandas para fazer análise exploratória dos dados de vendas.

## O Que Estudar

### Conceitos obrigatórios (segunda e terça)

1. **Pandas:** DataFrame, Series, leitura de CSV/Excel/SQL, seleção (loc, iloc), filtros, groupby, merge, pivot_table.
2. **Limpeza de dados:** tratar nulos (fillna, dropna), duplicatas, tipos de dados, outliers.
3. **Estatística descritiva:** describe(), mean, median, std, correlação.
4. **Matplotlib/Seaborn:** gráficos de barras, linhas, histograma, boxplot, heatmap de correlação.
5. **Exportação:** to_excel(), to_csv().

### Fontes de estudo gratuitas

- **Pandas oficial** (pandas.pydata.org/docs/getting_started) — tutorials excelentes.
- **Kaggle Learn — Pandas** (kaggle.com/learn/pandas) — curso interativo curto.
- **Real Python — Pandas Tutorials** — artigos aprofundados.
- **Seaborn Gallery** (seaborn.pydata.org/examples) — exemplos visuais de gráficos.

### Tempo estimado

Se já conhece Python, 4 a 5 horas de estudo focado em Pandas. Se é iniciante em Python, reserve 8 a 10 horas incluindo o básico da linguagem.

## Roteiro Diário

### Segunda-feira — Estudo de Pandas

- Faça o curso do Kaggle Learn de Pandas (leva cerca de 4 horas).
- Pratique operações básicas em um notebook Jupyter: ler CSV, filtrar, agrupar.

### Terça-feira — Estudo de Visualização + Conexão ao Banco

- Estude Matplotlib e Seaborn: pelo menos 5 tipos de gráfico.
- Conecte ao banco PostgreSQL usando `psycopg2` ou `sqlalchemy`:

```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://usuario:senha@localhost:5432/pharma_system')
df_vendas = pd.read_sql('SELECT * FROM vendas', engine)
```

### Quarta-feira — Limpeza e Preparação

- Carregue todas as tabelas do banco em DataFrames.
- Faça a limpeza: verifique nulos, tipos, duplicatas.
- Crie colunas derivadas:
  - `mes_venda` extraído de `data_venda`.
  - `dia_semana` extraído de `data_venda`.
  - `margem_lucro` = preco_venda - preco_custo.
- Faça os merges necessários (vendas + itens + produtos + filiais).

### Quinta-feira — Análise Exploratória

Crie um notebook Jupyter organizado com estas seções:

1. **Resumo geral:** shape, describe(), info().
2. **Análise de vendas:** faturamento por mês, por filial, por categoria.
3. **Análise de produtos:** top 10, distribuição de preços (histograma), boxplot de margem por categoria.
4. **Análise de clientes:** distribuição de frequência de compra, segmentação por valor (quartis).
5. **Correlações:** heatmap de correlação entre variáveis numéricas.
6. **Insights:** escreva em Markdown dentro do notebook pelo menos 5 insights de negócio que os dados revelam.

### Sexta-feira — Exportação e Relatório

- Exporte um relatório em Excel com múltiplas abas:
  - Aba 1: Faturamento mensal.
  - Aba 2: Ranking de produtos.
  - Aba 3: Ranking de filiais.
  - Aba 4: Dados brutos filtrados.
- Use `openpyxl` para formatar o Excel (cabeçalhos em negrito, largura de colunas).
- Salve todos os gráficos como imagens PNG.

### Sábado — Documentação

- Limpe o notebook: remova células de teste, adicione títulos e explicações.
- Escreva o README.md.
- Organize a pasta: `notebooks/`, `exports/`, `graficos/`, `README.md`.

### Domingo — Publicação

- Push no GitHub.
- Publique no LinkedIn com 2 a 3 gráficos gerados pelo Seaborn/Matplotlib.

## Entregáveis

- Notebook Jupyter completo com análise exploratória.
- Pelo menos 8 gráficos (barras, linhas, histograma, boxplot, heatmap, etc.).
- Relatório exportado em Excel com múltiplas abas.
- README.md completo.

## Checklist de Publicação

**GitHub:**

- [ ] Notebook `.ipynb` limpo e documentado.
- [ ] Gráficos exportados em `graficos/`.
- [ ] Excel em `exports/`.
- [ ] README com: Descrição, Prints/Gráficos, Tecnologias, Como Executar, Insights Encontrados.

**LinkedIn:**

- [ ] 2 a 3 gráficos mais impactantes.
- [ ] Texto focando nos insights de negócio (não na técnica pura).
- [ ] Hashtags: #Python #Pandas #DataAnalysis #AnáliseDeDados #PortfólioDev

---

---

# MÓDULO 04 — ETL (Extract, Transform, Load)

## Contexto no PharmaSystem

No mundo real, os dados de vendas das 100 filiais chegam em arquivos CSV exportados dos caixas. A equipe de dados precisa de um pipeline automatizado que leia esses CSVs, limpe, transforme e carregue no banco de dados — e então o Power BI se atualiza automaticamente. Esse módulo demonstra uma competência muito valorizada no mercado.

## O Que Estudar

### Conceitos obrigatórios (segunda e terça)

1. **O que é ETL:** Extract (extrair de fontes), Transform (limpar, validar, enriquecer), Load (carregar no destino).
2. **Diferença entre ETL e ELT.**
3. **Logging em Python:** módulo `logging` para registrar cada etapa.
4. **Tratamento de erros:** try/except para arquivos corrompidos ou com formato inesperado.
5. **Agendamento (conceito):** cron, Task Scheduler, ou bibliotecas como `schedule`.
6. **Boas práticas:** idempotência (rodar 2x sem duplicar), validação de schema, pasta de arquivos processados vs. novos.

### Fontes de estudo gratuitas

- **Real Python — ETL Pipeline** — busque "build etl pipeline python" no Real Python.
- **Documentação do módulo logging do Python** — essencial para pipelines.
- **Artigos sobre data pipeline patterns** — Medium e Towards Data Science.

### Tempo estimado

4 a 6 horas de estudo. O foco é mais prática do que teoria.

## Roteiro Diário

### Segunda-feira — Estudo e Planejamento

**Manhã (estudo):**

- Estude conceitos de ETL e boas práticas.
- Estude o módulo `logging` do Python.

**Tarde/Noite:**

- Planeje a arquitetura do pipeline:

```
dados_brutos/           ← CSVs novos chegam aqui
dados_processados/      ← CSVs já processados são movidos para cá
logs/                   ← logs de cada execução
scripts/
  ├── extract.py        ← lê os CSVs
  ├── transform.py      ← limpeza e validação
  ├── load.py           ← carrega no PostgreSQL
  └── pipeline.py       ← orquestra tudo
config/
  └── config.yaml       ← configurações (caminho do banco, etc.)
```

### Terça-feira — Extract

- Gere 5 a 10 arquivos CSV simulando dados das filiais (use Python ou dados do Módulo 01).
- Inclua propositalmente problemas: linhas em branco, datas em formatos diferentes, valores negativos, CPFs duplicados.
- Escreva `extract.py`:
  - Lê todos os CSVs de `dados_brutos/`.
  - Retorna uma lista de DataFrames.
  - Loga quantos arquivos encontrou, quantas linhas cada um tem.

### Quarta-feira — Transform

- Escreva `transform.py`:
  - Padroniza nomes de colunas (snake_case).
  - Converte tipos (datas, decimais).
  - Remove duplicatas.
  - Trata nulos (preencher ou descartar, com justificativa).
  - Valida regras de negócio (ex.: quantidade > 0, preço > 0).
  - Registra em log cada transformação e quantas linhas foram afetadas.
  - Retorna DataFrame limpo.

### Quinta-feira — Load

- Escreva `load.py`:
  - Conecta ao PostgreSQL.
  - Usa `UPSERT` (INSERT ... ON CONFLICT DO UPDATE) para idempotência.
  - Loga quantas linhas foram inseridas/atualizadas.
- Escreva `pipeline.py`:
  - Chama extract → transform → load em sequência.
  - Ao final, move CSVs processados para `dados_processados/`.
  - Gera um log de resumo final (total de arquivos, linhas processadas, erros).

### Sexta-feira — Testes e Robustez

- Teste cenários:
  - CSV vazio.
  - CSV com colunas faltando.
  - CSV com encoding diferente (UTF-8 vs. Latin-1).
  - Rodar o pipeline 2x sem duplicar dados (testar idempotência).
- Adicione tratamento de erros para cada cenário.
- (Opcional) Adicione um envio de e-mail de relatório ao final do pipeline usando `smtplib`.

### Sábado — Documentação e Diagrama

- Crie um diagrama do fluxo ETL (use draw.io ou Mermaid):

```
CSV Filiais → [Extract] → [Transform] → [Load] → PostgreSQL → Power BI
```

- Escreva o README.md com: problema de negócio, arquitetura, como executar, logs de exemplo, tratamento de erros.

### Domingo — Publicação

- Push no GitHub.
- Publique no LinkedIn com o diagrama de fluxo e um print do log de execução.

## Entregáveis

- Scripts Python separados por responsabilidade (extract, transform, load, pipeline).
- Arquivo de configuração YAML.
- CSVs de exemplo (com e sem erros).
- Diagrama de fluxo do pipeline.
- Logs de execução de exemplo.
- README.md completo.

## Checklist de Publicação

**GitHub:**

- [ ] Código modular e documentado.
- [ ] CSVs de exemplo em `dados_brutos/`.
- [ ] Diagrama de fluxo em `docs/`.
- [ ] README com: Problema, Arquitetura, Como Executar, Exemplos de Log.

**LinkedIn:**

- [ ] Diagrama do fluxo ETL.
- [ ] Print do log de execução com sucesso.
- [ ] Texto explicando: por que ETL é importante, o que o pipeline faz, tratamento de erros.
- [ ] Hashtags: #ETL #Python #DataEngineering #Pipeline #PortfólioDev

---

---

# MÓDULO 05 — API REST

## Contexto no PharmaSystem

O PharmaSystem precisa expor dados para outros sistemas: o app mobile das filiais consulta produtos, o sistema de e-commerce faz pedidos, o dashboard consome indicadores. Uma API REST é a interface que conecta tudo. Este é um dos módulos mais valorizados em processos seletivos.

## O Que Estudar

### Conceitos obrigatórios (segunda e terça)

1. **REST:** recursos, verbos HTTP (GET, POST, PUT, DELETE), status codes (200, 201, 400, 404, 500).
2. **JSON:** estrutura, serialização, deserialização.
3. **Flask (opção Python)** ou **Spring Boot (opção Java):** rotas, controllers, models, serialização.
4. **ORM:** SQLAlchemy (Flask) ou JPA/Hibernate (Spring Boot) — mapeamento objeto-relacional.
5. **Swagger/OpenAPI:** documentação automática da API.
6. **Testes de API:** Postman ou Insomnia para testar endpoints.

**Recomendação:** como seu portfólio já tem bastante Python, considere fazer em Spring Boot para demonstrar versatilidade. Mas se precisar economizar tempo, Flask é mais rápido de implementar.

### Fontes de estudo gratuitas

**Flask:**
- **Miguel Grinberg — Flask Mega-Tutorial** (blog.miguelgrinberg.com).
- **Real Python — Flask REST API** — busque "flask rest api tutorial".
- **Documentação Flask** (flask.palletsprojects.com).

**Spring Boot:**
- **Baeldung** (baeldung.com) — referência para Spring Boot REST.
- **Spring Initializr** (start.spring.io) — para gerar o projeto base.
- **Canal Michelli Brito** (YouTube, PT-BR) — tutoriais de Spring Boot.

### Tempo estimado

Flask: 6 a 8 horas. Spring Boot: 8 a 12 horas (mais setup, mais conceitos).

## Roteiro Diário

### Segunda-feira — Estudo de REST + Setup

**Manhã (estudo):**

- Estude conceitos REST, verbos HTTP, status codes.
- Assista a um tutorial introdutório do framework escolhido.

**Tarde/Noite:**

- Crie o projeto base.
- Configure a conexão com o banco PostgreSQL do Módulo 01.
- Crie o modelo de `Produto` (entidade/classe mapeada para a tabela `produtos`).

### Terça-feira — CRUD de Produtos

- Implemente os endpoints de Produto:
  - `GET /api/produtos` — listar todos (com paginação).
  - `GET /api/produtos/{id}` — buscar por ID.
  - `POST /api/produtos` — criar novo produto.
  - `PUT /api/produtos/{id}` — atualizar produto.
  - `DELETE /api/produtos/{id}` — deletar produto.
- Teste todos no Postman.

### Quarta-feira — CRUD de Clientes e Filiais

- Repita a mesma estrutura para:
  - `GET/POST/PUT/DELETE /api/clientes`
  - `GET/POST/PUT/DELETE /api/filiais`
- Adicione validações: campos obrigatórios, formato de CPF, e-mail.
- Retorne erros adequados (400 para validação, 404 para não encontrado).

### Quinta-feira — Endpoints de Vendas e Indicadores

- Implemente:
  - `POST /api/vendas` — registrar uma venda (com itens).
  - `GET /api/vendas?filial_id=X&mes=Y` — listar vendas com filtros.
  - `GET /api/indicadores/faturamento-mensal` — retorna faturamento agregado por mês.
  - `GET /api/indicadores/top-produtos?limit=10` — top N produtos.
  - `GET /api/indicadores/top-filiais` — ranking de filiais.

### Sexta-feira — Documentação e Swagger

- Configure Swagger/OpenAPI para documentação automática.
  - Flask: use `flask-smorest` ou `flasgger`.
  - Spring Boot: use `springdoc-openapi`.
- Garanta que todos os endpoints apareçam documentados com exemplos.
- Teste cenários de erro (IDs inexistentes, payloads inválidos).

### Sábado — README e Prints

- Tire prints do Swagger mostrando os endpoints.
- Tire prints do Postman com exemplos de requisições e respostas.
- Escreva o README.md com: descrição da API, endpoints disponíveis, como executar, prints.

### Domingo — Publicação

- Push no GitHub.
- Publique no LinkedIn com prints do Swagger e do Postman.

## Entregáveis

- Código da API (Flask ou Spring Boot).
- Pelo menos 15 endpoints funcionais.
- Documentação Swagger/OpenAPI.
- Prints do Postman com exemplos de requisições.
- README.md completo.

## Checklist de Publicação

**GitHub:**

- [ ] Código organizado (controllers, models, services, repositories).
- [ ] requirements.txt (Flask) ou pom.xml (Spring Boot).
- [ ] Prints do Swagger e Postman em `docs/`.
- [ ] README com: Descrição, Endpoints, Como Executar, Prints, Tecnologias.

**LinkedIn:**

- [ ] Print do Swagger mostrando a lista de endpoints.
- [ ] Print de uma requisição/resposta no Postman.
- [ ] Texto explicando: o que a API faz, decisões de design, validações.
- [ ] Hashtags: #API #REST #Flask #SpringBoot #Backend #PortfólioDev

---

---

# MÓDULO 06 — Sistema Web

## Contexto no PharmaSystem

Uma rede de 100 filiais gera muitos chamados de TI: impressora parou, sistema caiu, caixa travou. Neste módulo, você constrói o módulo de Help Desk do PharmaSystem — um sistema web para abertura, acompanhamento e resolução de chamados técnicos. Isso conecta diretamente com sua experiência profissional em TI e infraestrutura.

## O Que Estudar

### Conceitos obrigatórios (segunda e terça)

1. **MVC (Model-View-Controller):** separação de responsabilidades.
2. **Templates HTML:** Jinja2 (Flask) ou Thymeleaf (Spring Boot).
3. **Formulários e validação do lado do servidor.**
4. **Autenticação básica:** login/logout, sessões, roles (admin vs. operador).
5. **CSS básico:** Bootstrap para ter um layout profissional rápido.
6. **CRUD completo via interface web.**

### Fontes de estudo gratuitas

**Flask + Jinja2:**
- **Flask Mega-Tutorial (Miguel Grinberg)** — capítulos sobre templates e login.
- **Real Python — Flask Tutorial.**

**Spring Boot + Thymeleaf:**
- **Baeldung — Spring MVC + Thymeleaf.**
- **Canal Michelli Brito** (YouTube) — projetos Spring MVC.

**Bootstrap:**
- **getbootstrap.com** — documentação e componentes prontos.

### Tempo estimado

8 a 12 horas de estudo + construção. Este módulo é mais denso.

## Roteiro Diário

### Segunda-feira — Estudo e Setup

- Estude MVC, templates e autenticação.
- Crie o projeto e configure o banco (reuse o PostgreSQL existente).
- Crie as tabelas novas:

```sql
usuarios (id, nome, email, senha_hash, role, filial_id)
chamados (id, titulo, descricao, categoria, prioridade, status, 
          filial_id, usuario_abertura_id, usuario_responsavel_id,
          data_abertura, data_fechamento)
comentarios_chamado (id, chamado_id, usuario_id, texto, data)
```

### Terça-feira — Autenticação

- Implemente registro de usuário e login.
- Configure sessões e proteção de rotas.
- Crie dois roles: `admin` (TI central) e `operador` (funcionário da filial).
- Página de login com Bootstrap.

### Quarta-feira — CRUD de Chamados

- Tela de abertura de chamado (formulário com: título, descrição, categoria, prioridade).
- Lista de chamados (tabela com filtros: status, prioridade, filial).
- Tela de detalhes do chamado (ver informações, adicionar comentários).
- Funcionalidade de alterar status (Aberto → Em Andamento → Resolvido → Fechado).

### Quinta-feira — Dashboard Interno + Funcionalidades Extras

- Página de dashboard com contadores:
  - Chamados abertos.
  - Chamados em andamento.
  - Chamados resolvidos este mês.
  - Tempo médio de resolução.
- Adicione filtro por filial e por período.
- Admin pode atribuir chamado a um técnico.
- Operador vê apenas chamados da sua filial.

### Sexta-feira — Polimento Visual e Testes

- Revise todas as telas: alinhamento, responsividade, mensagens de erro claras.
- Teste fluxos completos: registrar → logar → abrir chamado → comentar → resolver → ver no dashboard.
- Adicione feedbacks visuais: toast de sucesso, badge de prioridade (vermelho = urgente), ícones.

### Sábado — Documentação e Prints

- Tire prints de cada tela principal (login, lista, detalhes, dashboard).
- Escreva o README.md.
- Crie um fluxo de navegação visual (diagrama simples mostrando as telas e transições).

### Domingo — Publicação

- Push no GitHub.
- Publique no LinkedIn com prints das telas.

## Entregáveis

- Sistema web funcional com autenticação e CRUD.
- Pelo menos 6 telas (login, registro, lista, novo chamado, detalhes, dashboard).
- Dois roles com permissões diferentes.
- Prints de cada tela.
- README.md completo.

## Checklist de Publicação

**GitHub:**

- [ ] Código MVC organizado.
- [ ] requirements.txt ou pom.xml.
- [ ] Prints das telas em `docs/`.
- [ ] README com: Descrição, Funcionalidades, Prints, Como Executar, Tecnologias.

**LinkedIn:**

- [ ] 3 a 4 prints das telas mais bonitas (dashboard, lista de chamados, detalhes).
- [ ] Texto explicando: problema resolvido (gestão de chamados de TI), funcionalidades, decisões de design.
- [ ] Hashtags: #WebDev #Flask #SpringBoot #HelpDesk #FullStack #PortfólioDev

---

---

# MÓDULO 07 — Engenharia de Requisitos

## Contexto no PharmaSystem

Agora você muda de chapéu: em vez de desenvolvedor, você é o engenheiro de sistemas que documenta formalmente o PharmaSystem. Este módulo é o que diferencia um programador de um engenheiro. Você produz um documento de requisitos profissional que poderia ser apresentado a um cliente real.

## O Que Estudar

### Conceitos obrigatórios (segunda e terça)

1. **Tipos de requisitos:** funcionais (RF) vs. não-funcionais (RNF).
2. **Técnicas de elicitação:** entrevistas, brainstorming, análise de documentos.
3. **Especificação de requisitos:** formato IEEE 830 (simplificado).
4. **Casos de uso:** atores, fluxos principal e alternativo, pré/pós-condições.
5. **UML — Diagramas de caso de uso:** atores, elipses, relacionamentos (include, extend).
6. **UML — Diagrama de classes:** classes, atributos, métodos, relacionamentos (associação, agregação, composição, herança).
7. **UML — Diagrama de sequência:** lifelines, mensagens, retornos.
8. **UML — Diagrama de atividade:** fluxo de processos.

### Fontes de estudo gratuitas

- **Lucidchart UML Tutorials** — exemplos visuais de cada diagrama.
- **UML Diagrams (uml-diagrams.org)** — referência completa.
- **draw.io (app.diagrams.net)** — ferramenta gratuita para criar diagramas UML.
- **PlantUML** (plantuml.com) — gera diagramas UML a partir de texto (ideal para versionamento no GitHub).

### Tempo estimado

6 a 8 horas de estudo (conceitos + prática com a ferramenta de diagramas).

## Roteiro Diário

### Segunda-feira — Estudo de Requisitos

- Estude tipos de requisitos e o formato IEEE 830.
- Estude casos de uso: como escrever, exemplos.
- Comece a listar os requisitos do PharmaSystem com base em tudo que você já construiu.

### Terça-feira — Estudo de UML + Levantamento

- Estude diagramas de caso de uso, classes, sequência e atividade.
- Instale o draw.io ou configure o PlantUML.
- Complete a lista de requisitos.

### Quarta-feira — Documento de Requisitos

Escreva o Documento de Requisitos do PharmaSystem com estas seções:

1. **Introdução:** propósito, escopo, definições.
2. **Descrição geral:** perspectiva do produto, funções principais, características dos usuários, restrições.
3. **Requisitos funcionais (RF):**
   - RF01: O sistema deve permitir o cadastro de filiais.
   - RF02: O sistema deve permitir o cadastro de produtos com preço de custo e venda.
   - RF03: O sistema deve registrar vendas com itens e formas de pagamento.
   - RF04: O sistema deve gerar relatórios de faturamento mensal.
   - (Continue até pelo menos RF20.)
4. **Requisitos não-funcionais (RNF):**
   - RNF01: O sistema deve suportar 100 filiais simultâneas.
   - RNF02: O tempo de resposta da API deve ser inferior a 500ms.
   - RNF03: O sistema deve manter logs de auditoria.
   - (Pelo menos 10 RNFs.)
5. **Regras de negócio.**

### Quinta-feira — Casos de Uso e Diagramas UML

**Casos de uso (escreva 5 completos):**

Exemplo de caso de uso:

- **UC01 — Registrar Venda**
  - Ator: Operador de Caixa.
  - Pré-condição: Operador autenticado no sistema.
  - Fluxo principal: (passo a passo).
  - Fluxos alternativos: produto sem estoque, cliente não cadastrado.
  - Pós-condição: venda registrada, estoque atualizado.

**Diagramas:**

- Diagrama de Casos de Uso (geral do sistema).
- Diagrama de Classes (todas as entidades + relacionamentos).

### Sexta-feira — Diagramas de Sequência e Atividade

- Diagrama de Sequência para o caso de uso "Registrar Venda" (mostrando: Operador → Interface → Controller → Service → Database).
- Diagrama de Sequência para "Abrir Chamado de TI".
- Diagrama de Atividade para o fluxo completo de um chamado (Aberto → Triagem → Em Andamento → Resolvido → Fechado).

### Sábado — Revisão e Documentação

- Revise o documento de requisitos: está claro? Um desenvolvedor novo conseguiria implementar o sistema só lendo?
- Exporte todos os diagramas como imagens.
- Escreva o README.md.

### Domingo — Publicação

- Push no GitHub (documento em `.md` ou `.pdf`, diagramas em `diagramas/`).
- Publique no LinkedIn com um ou dois diagramas UML.

## Entregáveis

- Documento de Requisitos completo (20+ RF, 10+ RNF).
- 5 Casos de Uso escritos.
- Diagrama de Casos de Uso.
- Diagrama de Classes.
- 2 Diagramas de Sequência.
- 1 Diagrama de Atividade.
- README.md.

## Checklist de Publicação

**GitHub:**

- [ ] Documento de requisitos em `docs/`.
- [ ] Diagramas em `diagramas/` (PNG + fonte PlantUML ou draw.io).
- [ ] README com: Descrição, Prints dos Diagramas, Metodologia Usada.

**LinkedIn:**

- [ ] Diagrama de classes ou de sequência (visual forte).
- [ ] Texto focando: "além de programar, documentei formalmente a engenharia do sistema".
- [ ] Hashtags: #UML #EngenhariaDeSistemas #Requisitos #SystemsEngineering #PortfólioDev

---

---

# MÓDULO 08 — Arquitetura de Sistemas

## Contexto no PharmaSystem

Agora você é o arquiteto. Neste módulo, você projeta a arquitetura completa do PharmaSystem como se fosse apresentá-la ao CTO de uma empresa. Isso inclui componentes, integrações, bancos de dados, APIs, filas e infraestrutura. Este módulo mostra visão de engenharia de ponta a ponta.

## O Que Estudar

### Conceitos obrigatórios (segunda e terça)

1. **Estilos arquiteturais:** monolítico, microsserviços, serverless, event-driven.
2. **Padrões:** API Gateway, BFF (Backend for Frontend), CQRS, Event Sourcing.
3. **Modelo C4:** Context, Container, Component, Code — níveis de abstração para documentar arquitetura.
4. **Diagramas de infraestrutura:** servidores, load balancers, bancos, caches, filas.
5. **Integrações:** REST, mensageria (RabbitMQ, Kafka conceitual), webhooks.
6. **Decisões arquiteturais (ADR — Architecture Decision Record):** formato de documentar "por que" escolheu algo.

### Fontes de estudo gratuitas

- **C4 Model** (c4model.com) — referência oficial com exemplos.
- **Martin Fowler — Architecture** (martinfowler.com) — artigos sobre padrões.
- **draw.io / Mermaid** — para criar os diagramas.
- **GitHub — ADR Templates** — busque "adr template" para ver exemplos.

### Tempo estimado

6 a 8 horas de estudo. O restante é construção dos diagramas e documentos.

## Roteiro Diário

### Segunda-feira — Estudo

- Estude os estilos arquiteturais e quando usar cada um.
- Estude o Modelo C4 (Context, Container, Component).
- Leia 2 a 3 exemplos de ADRs.

### Terça-feira — Definição da Arquitetura

Defina a arquitetura do PharmaSystem. Sugestão de estrutura:

```
[App Mobile Filiais]  →  [API Gateway]  →  [Serviço de Vendas]     →  [PostgreSQL]
[Portal Web Admin]    →  [API Gateway]  →  [Serviço de Estoque]    →  [PostgreSQL]
[Dashboard BI]        →                    [Serviço de Relatórios]  →  [PostgreSQL]
                                           [Serviço de Help Desk]  →  [PostgreSQL]
                                           [Pipeline ETL]          →  [PostgreSQL]
                           [Fila de Mensagens (RabbitMQ)]
                              ↑ eventos de venda, chamados
```

### Quarta-feira — Diagramas C4

Crie os 3 primeiros níveis do C4:

**Nível 1 — Context:** PharmaSystem e seus atores externos (operadores, gestores, técnicos TI, sistemas externos como SEFAZ, fornecedores).

**Nível 2 — Container:** API Gateway, cada microsserviço, banco de dados, fila, dashboard.

**Nível 3 — Component:** detalhe interno de 1 microsserviço (ex.: Serviço de Vendas → Controller, Service, Repository, Validador).

### Quinta-feira — Diagrama de Infraestrutura + Fluxos

- Diagrama de infraestrutura: onde cada componente roda (servidores, cloud, containers).
- Diagrama de fluxo: como uma venda percorre o sistema (caixa → API → validação → banco → evento → atualização de estoque → notificação).
- Diagrama de integração: como o PharmaSystem se integraria a sistemas externos (SEFAZ para NF-e, fornecedores para reposição).

### Sexta-feira — ADRs (Architecture Decision Records)

Escreva pelo menos 3 ADRs:

- **ADR-001:** Por que escolhemos arquitetura de microsserviços em vez de monolito.
- **ADR-002:** Por que PostgreSQL como banco de dados principal.
- **ADR-003:** Por que API REST em vez de GraphQL.

Formato de cada ADR:

```
# ADR-001: Arquitetura de Microsserviços

## Status
Aceita

## Contexto
O PharmaSystem atende 100 filiais com módulos de vendas, estoque, 
help desk e relatórios. Cada módulo tem ciclos de atualização diferentes.

## Decisão
Adotar arquitetura de microsserviços com API Gateway.

## Consequências
Positivas: deploy independente, escalabilidade por módulo.
Negativas: complexidade operacional, necessidade de orquestração.
```

### Sábado — Documentação Final

- Compile tudo em um documento de arquitetura coeso.
- Organize: Visão Geral → C4 (Context, Container, Component) → Infraestrutura → Fluxos → ADRs.
- Escreva o README.md.

### Domingo — Publicação

- Push no GitHub.
- Publique no LinkedIn com o diagrama C4 de Container (o mais visual e impactante).

## Entregáveis

- Diagrama C4 — Nível 1 (Context).
- Diagrama C4 — Nível 2 (Container).
- Diagrama C4 — Nível 3 (Component) de 1 serviço.
- Diagrama de infraestrutura.
- Diagrama de fluxo de venda.
- 3 ADRs.
- README.md.

## Checklist de Publicação

**GitHub:**

- [ ] Diagramas em `diagramas/`.
- [ ] ADRs em `docs/adrs/`.
- [ ] Documento de arquitetura em `docs/`.
- [ ] README com: Visão Geral, Diagramas, ADRs, Tecnologias.

**LinkedIn:**

- [ ] Diagrama C4 Container (o mais visual).
- [ ] Texto explicando: visão sistêmica, decisões tomadas e seus trade-offs.
- [ ] Hashtags: #Arquitetura #SystemDesign #C4Model #Microsserviços #PortfólioDev

---

---

# MÓDULO 09 — Engenharia de Dados

## Contexto no PharmaSystem

A rede de farmácias não quer depender de CSVs manuais. Neste módulo, você constrói um pipeline de engenharia de dados que consome uma API externa (simulada), processa os dados e alimenta um dashboard automatizado. Isso complementa o ETL do Módulo 04 com uma abordagem mais moderna e orientada a API.

## O Que Estudar

### Conceitos obrigatórios (segunda e terça)

1. **Diferença entre ETL e ELT moderno.**
2. **Consumo de APIs com Python:** `requests`, paginação, autenticação.
3. **Data Lake vs. Data Warehouse (conceitual).**
4. **Airflow (conceitual):** DAGs, tasks, scheduling — entender o conceito mesmo sem instalar.
5. **Qualidade de dados:** validações, testes de schema, Great Expectations (conceitual).

### Fontes de estudo gratuitas

- **Real Python — Working with APIs** — tutorial de consumo de APIs.
- **Documentação do requests** (docs.python-requests.org).
- **Airflow official docs** — leia a seção "Concepts" para entender DAGs.
- **Artigos sobre Modern Data Stack** — Towards Data Science, Data Engineering Weekly.

### Tempo estimado

5 a 7 horas de estudo.

## Roteiro Diário

### Segunda-feira — Estudo e Planejamento

- Estude os conceitos e a diferença entre ETL tradicional e data pipelines modernos.
- Planeje o pipeline:

```
[API PharmaSystem (Módulo 05)] → [Ingestão Python] → [Staging SQL] → [Transformação] → [Tabelas Analíticas] → [Dashboard]
```

### Terça-feira — API Mock (se necessário) + Ingestão

- Se a API do Módulo 05 não estiver rodando, crie uma versão mock com Flask que retorna JSONs de vendas, produtos e filiais.
- Escreva o script de ingestão:
  - Consome todos os endpoints da API.
  - Salva os dados brutos em tabelas `staging_*` no banco.
  - Loga tudo.

### Quarta-feira — Transformação

- Escreva scripts de transformação que leem de `staging_*` e criam tabelas analíticas:
  - `fato_vendas` — tabela fato desnormalizada com todas as informações de venda.
  - `dim_tempo` — dimensão temporal (ano, mês, trimestre, dia da semana).
  - `dim_filial` — dimensão de filiais.
  - `dim_produto` — dimensão de produtos com categoria.
- Aplique o conceito de Star Schema.

### Quinta-feira — Qualidade de Dados + Dashboard

- Adicione validações: contagem de registros (staging vs. analítico), verificação de nulos, verificação de chaves duplicadas.
- Crie um dashboard simples (pode ser com Streamlit para ser diferente do Módulo 02):
  - Faturamento por período.
  - Top produtos.
  - Comparativo entre filiais.
  - Alimentado diretamente das tabelas analíticas.

### Sexta-feira — Orquestração (Conceitual) + Script Mestre

- Crie um script `orquestrador.py` que executa o pipeline completo em ordem:
  1. Ingestão.
  2. Transformação.
  3. Validação.
  4. (Opcional) Atualização do dashboard.
- Escreva um documento explicando como isso seria orquestrado com Airflow em produção (DAG conceitual, schedule, dependências).

### Sábado — Documentação

- Crie diagrama do pipeline completo.
- Documente o Star Schema com diagrama ER das tabelas analíticas.
- Escreva o README.md.

### Domingo — Publicação

- Push no GitHub.
- Publique no LinkedIn com o diagrama do pipeline e um print do dashboard.

## Entregáveis

- Scripts de ingestão, transformação, validação e orquestração.
- Tabelas analíticas com Star Schema implementado.
- Dashboard (Streamlit ou outro).
- Diagrama do pipeline.
- Diagrama do Star Schema.
- Documento conceitual de orquestração com Airflow.
- README.md.

## Checklist de Publicação

**GitHub:**

- [ ] Scripts organizados em `ingestao/`, `transformacao/`, `validacao/`.
- [ ] Diagramas em `docs/`.
- [ ] README com: Pipeline, Star Schema, Como Executar, Dashboard.

**LinkedIn:**

- [ ] Diagrama do pipeline.
- [ ] Print do dashboard Streamlit.
- [ ] Texto: diferença entre ETL simples e data pipeline, decisões de modelagem.
- [ ] Hashtags: #DataEngineering #Pipeline #StarSchema #Streamlit #PortfólioDev

---

---

# MÓDULO 10 — MBSE (Model-Based Systems Engineering)

## Contexto no PharmaSystem

MBSE é o que transforma um desenvolvedor em engenheiro de sistemas. Neste módulo, você aplica modelagem baseada em modelos ao PharmaSystem, tratando-o como um sistema completo com requisitos, blocos, interfaces e fluxos — usando a mesma abordagem que seria usada para projetar um drone, um satélite ou uma planta industrial.

## O Que Estudar

### Conceitos obrigatórios (segunda e terça)

1. **O que é MBSE:** modelagem como fonte de verdade (vs. documentação textual tradicional).
2. **SysML (resumo):** diferença entre UML e SysML, principais diagramas.
3. **Diagrama de Requisitos (SysML):** representar requisitos como blocos com rastreabilidade.
4. **Diagrama de Blocos (BDD — Block Definition Diagram):** estrutura do sistema.
5. **Diagrama de Blocos Internos (IBD — Internal Block Diagram):** interfaces e fluxos entre blocos.
6. **Diagrama de Atividade (já estudado no Módulo 07, agora com fluxos de dados entre subsistemas).**
7. **Rastreabilidade de requisitos:** como ligar cada requisito a um bloco, teste e caso de uso.

### Fontes de estudo gratuitas

- **INCOSE Systems Engineering Handbook** — resumos disponíveis online.
- **SysML Distilled (resumos)** — busque "SysML tutorial" no YouTube.
- **Sparx Systems — SysML Tutorial** (sparxsystems.com/resources/tutorials/sysml).
- **PlantUML** — suporta alguns diagramas SysML.
- **draw.io** — templates de BDD e IBD disponíveis.

### Tempo estimado

6 a 10 horas. MBSE é mais conceitual e pode ser novo para você, então reserve tempo extra.

## Roteiro Diário

### Segunda-feira — Estudo de MBSE e SysML

- Assista a 2 a 3 vídeos sobre MBSE e SysML.
- Leia o tutorial da Sparx Systems.
- Entenda a diferença entre UML (foco em software) e SysML (foco em sistema).

### Terça-feira — Diagrama de Requisitos

- Pegue os requisitos do Módulo 07 e represente-os em um Diagrama de Requisitos SysML.
- Mostre:
  - Requisitos de alto nível derivando em sub-requisitos.
  - Relacionamentos: derive, satisfy, verify.
- Exemplo: `REQ-001: Gestão de Vendas` → deriva em `REQ-001.1: Registrar Venda`, `REQ-001.2: Cancelar Venda`, etc.

### Quarta-feira — Diagrama de Blocos (BDD)

- Modele o PharmaSystem como um sistema de blocos:

```
<<system>> PharmaSystem
  ├── <<subsystem>> Módulo de Vendas
  ├── <<subsystem>> Módulo de Estoque
  ├── <<subsystem>> Módulo de Help Desk
  ├── <<subsystem>> Módulo de Relatórios
  ├── <<subsystem>> Pipeline de Dados
  └── <<subsystem>> Gateway de Integração
```

- Mostre composição e associações entre blocos.

### Quinta-feira — Diagrama de Blocos Internos (IBD)

- Escolha um subsistema (ex.: Módulo de Vendas) e detalhe internamente:
  - Portas (ports): entrada de dados do caixa, saída de eventos de venda.
  - Fluxos: dados, sinais, chamadas.
  - Interfaces com outros subsistemas.
- Crie um IBD mostrando como o Módulo de Vendas se conecta ao Módulo de Estoque e ao Pipeline de Dados.

### Sexta-feira — Matriz de Rastreabilidade

- Crie uma matriz de rastreabilidade ligando:
  - Requisito → Bloco que satisfaz → Caso de uso relacionado → Teste que verifica.
- Exemplo em formato de tabela:

| Requisito | Bloco | Caso de Uso | Teste |
|---|---|---|---|
| RF01 | Módulo de Vendas | UC01 — Registrar Venda | TC01 — Venda com sucesso |
| RF05 | Módulo de Estoque | UC03 — Consultar Estoque | TC05 — Estoque atualizado |

- Pelo menos 10 linhas.

### Sábado — Documentação

- Compile os diagramas em um documento MBSE coeso.
- Escreva uma introdução explicando o que é MBSE e por que foi aplicado.
- Escreva o README.md.

### Domingo — Publicação

- Push no GitHub.
- Publique no LinkedIn com o BDD (diagrama mais visual e diferenciado).

## Entregáveis

- Diagrama de Requisitos SysML.
- Diagrama de Blocos (BDD) do sistema completo.
- Diagrama de Blocos Internos (IBD) de um subsistema.
- Diagrama de Atividade com fluxo entre subsistemas.
- Matriz de Rastreabilidade (10+ linhas).
- Documento MBSE compilado.
- README.md.

## Checklist de Publicação

**GitHub:**

- [ ] Diagramas em `diagramas/`.
- [ ] Documento MBSE em `docs/`.
- [ ] Matriz de rastreabilidade em `docs/`.
- [ ] README com: O que é MBSE, Diagramas, Rastreabilidade.

**LinkedIn:**

- [ ] Diagrama BDD (visual forte e diferenciado).
- [ ] Texto explicando: o que é MBSE, por que você aplicou ao PharmaSystem, como isso agrega valor.
- [ ] Hashtags: #MBSE #SysML #SystemsEngineering #EngenhariaDeSistemas #PortfólioDev

---

---

# MÓDULO 11 — Projeto Integrador

## Contexto no PharmaSystem

Este é o módulo de convergência. Você pega tudo que construiu — banco, API, dashboard, pipeline, sistema web — e integra em um fluxo ponta a ponta que funciona junto. O objetivo é provar que você não só sabe fazer cada peça, mas sabe fazer o sistema inteiro funcionar.

## O Que Estudar

Neste módulo, o estudo é substituído por revisão. Você não aprende nada novo; você faz os módulos anteriores conversarem.

### O que revisar (segunda)

- Revise a API (Módulo 05): ela ainda funciona? Os endpoints estão acessíveis?
- Revise o ETL (Módulo 04): ele carrega dados corretamente?
- Revise o sistema web (Módulo 06): consegue consumir a API?
- Revise o dashboard (Módulo 02/09): está conectado às tabelas analíticas?

## Roteiro Diário

### Segunda-feira — Inventário e Planejamento de Integração

- Liste todos os componentes existentes e seu estado atual.
- Defina o fluxo integrado:

```
[Filial] → Venda registrada via [Sistema Web ou API]
       → Dados persistidos no [PostgreSQL]
       → [Pipeline ETL] processa e alimenta [tabelas analíticas]
       → [Dashboard] mostra indicadores atualizados
       → [Help Desk] permite abertura de chamados
       → Tudo documentado em [Requisitos + Arquitetura + MBSE]
```

- Identifique pontos de integração que estão desconectados.

### Terça-feira — Conectar API ao Sistema Web

- Faça o sistema web do Módulo 06 consumir a API do Módulo 05 para listar produtos e filiais (em vez de consultar diretamente o banco).
- Exemplo: a tela de abertura de chamado carrega a lista de filiais via `GET /api/filiais`.

### Quarta-feira — Conectar Pipeline ao Dashboard

- Garanta que o pipeline do Módulo 09 alimenta as tabelas que o dashboard consome.
- Execute: API → Ingestão → Transformação → Dashboard atualizado.
- Adicione uma funcionalidade de "última atualização" no dashboard.

### Quinta-feira — Fluxo Completo End-to-End

- Demonstre o fluxo completo:
  1. Cadastre um produto via API.
  2. Registre uma venda via API ou sistema web.
  3. Execute o pipeline.
  4. Verifique o indicador atualizado no dashboard.
  5. Abra um chamado no Help Desk.
- Grave prints ou GIFs de cada etapa.

### Sexta-feira — Testes de Integração e Correções

- Execute tudo do zero e anote problemas.
- Corrija bugs de integração.
- Escreva um roteiro de demonstração passo a passo (como um "demo script" para apresentar a um recrutador ou professor).

### Sábado — Documentação do Integrador

- Crie um diagrama de integração mostrando como cada módulo se conecta.
- Escreva o README.md explicando: o que foi integrado, como executar, demo script.
- Atualize o README.md raiz do repositório `pharma-system/` com a visão geral de todos os módulos.

### Domingo — Publicação

- Push no GitHub.
- Publique no LinkedIn mostrando o fluxo end-to-end.

## Entregáveis

- Integrações funcionais entre os módulos.
- Demonstração do fluxo end-to-end documentada (prints ou GIFs).
- Demo script (roteiro de apresentação).
- Diagrama de integração.
- README.md do módulo + README.md raiz atualizado.

## Checklist de Publicação

**GitHub:**

- [ ] Código de integração.
- [ ] Prints/GIFs do fluxo end-to-end em `docs/`.
- [ ] Demo script em `docs/`.
- [ ] README raiz atualizado com visão geral de todos os 11 módulos.

**LinkedIn:**

- [ ] Diagrama de integração.
- [ ] GIF ou sequência de prints do fluxo end-to-end.
- [ ] Texto: "integrei todos os módulos do meu portfólio em um sistema funcional".
- [ ] Hashtags: #Integração #FullStack #EndToEnd #EngenhariaDeSistemas #PortfólioDev

---

---

# MÓDULO 12 — Projeto Final

## Contexto no PharmaSystem

Este é o módulo de fechamento. Aqui você não constrói nada novo — você poliu, refina e empacota tudo como um produto profissional. O objetivo é que qualquer recrutador que entre no seu GitHub veja um projeto coeso, bem documentado e impressionante.

## O Que Fazer

### Segunda-feira — Revisão Geral de Código

- Percorra todos os módulos.
- Padronize nomes de variáveis e funções.
- Remova código comentado e debugs esquecidos.
- Garanta que cada módulo tem um `requirements.txt` ou equivalente.
- Verifique que tudo roda a partir do README (se alguém seguir as instruções, funciona?).

### Terça-feira — README Raiz Profissional

Reescreva o README.md raiz do repositório com qualidade profissional:

```markdown
# PharmaSystem — Sistema de Gestão para Rede de Farmácias

## Sobre o Projeto
O PharmaSystem é um ecossistema completo para gestão de uma rede 
de farmácias com 100 filiais, desenvolvido como portfólio acadêmico 
de Engenharia de Sistemas.

## Arquitetura
[Imagem do diagrama C4 Container]

## Módulos
| # | Módulo | Tecnologias | Descrição |
|---|--------|-------------|-----------|
| 01 | SQL | PostgreSQL | Banco de dados de vendas |
| 02 | Power BI | Power BI, DAX | Dashboard executivo |
| ... | ... | ... | ... |

## Stack Tecnológico
Python, Flask/Spring Boot, PostgreSQL, Power BI, Streamlit, 
Pandas, UML, SysML, MBSE

## Como Executar
[Instruções gerais + links para cada módulo]

## Sobre o Autor
[Seu nome, curso, universidade, LinkedIn, contato]
```

### Quarta-feira — Documentação Visual

- Reexporte todos os diagramas em alta resolução.
- Crie uma pasta `docs/apresentacao/` com as melhores imagens de cada módulo.
- Se possível, grave um vídeo de 2 a 3 minutos mostrando o sistema rodando (Loom ou OBS).

### Quinta-feira — Feature Extra (Diferencial)

Adicione uma funcionalidade extra que impressione:

Sugestões:

- **Predição simples:** use scikit-learn para prever vendas do próximo mês com regressão linear (mesmo que simples, mostra que você sabe integrar ML).
- **Notificação:** o pipeline envia um resumo por e-mail quando processa novos dados.
- **Autenticação JWT na API:** substitua sessões por tokens JWT (mais profissional).
- **Docker Compose:** crie um `docker-compose.yml` que sobe banco + API + dashboard com um comando.

Escolha UMA e implemente.

### Sexta-feira — Teste Final + Vídeo

- Execute o sistema inteiro do zero seguindo apenas o README.
- Se algo não funcionar, corrija.
- Grave o vídeo de demonstração (se não fez na quinta).

### Sábado — Publicação Final no GitHub

- Faça o push final.
- Adicione tags/releases no GitHub (v1.0).
- Fixe o repositório no perfil do GitHub.
- Verifique que o README raiz renderiza bonito com imagens e tabelas.

### Domingo — Publicação Final no LinkedIn

- Publique o post final: um retrospecto das 12 semanas.
- Modelo de post:

> Nas últimas 12 semanas, construí o PharmaSystem — um sistema completo 
> de gestão para uma rede de farmácias com 100 filiais.
>
> O que eu aprendi e apliquei:
> - SQL e modelagem de dados
> - Dashboards com Power BI e Streamlit
> - Análise exploratória com Python e Pandas
> - Pipeline ETL automatizado
> - API REST com [Flask/Spring Boot]
> - Sistema web com autenticação
> - Engenharia de requisitos e UML
> - Arquitetura de sistemas (C4 Model)
> - Engenharia de dados com Star Schema
> - MBSE com SysML
> - Integração de ponta a ponta
>
> Tudo documentado, versionado e acessível no GitHub.
>
> [Link para o repositório]

## Entregáveis Finais

- Repositório completo e polido.
- README raiz profissional.
- Feature extra implementada.
- Vídeo de demonstração (opcional, mas muito recomendado).
- Post final no LinkedIn.

---

---

# Resumo Visual do Cronograma

```
Semana  Módulo                    Foco Principal               Entrega Chave
──────  ────────────────────────  ─────────────────────────    ──────────────────────
  01    SQL                       Fundação de dados            20+ consultas SQL
  02    Power BI                  Visualização executiva       Dashboard 3 páginas
  03    Python + Pandas           Análise exploratória         Notebook + gráficos
  04    ETL                       Pipeline automatizado        Scripts modulares
  05    API REST                  Backend                      15+ endpoints
  06    Sistema Web               Full Stack                   Help Desk funcional
  07    Engenharia de Requisitos  Documentação formal          Requisitos + UML
  08    Arquitetura               Visão sistêmica              C4 + ADRs
  09    Engenharia de Dados       Data pipeline moderno        Star Schema + Streamlit
  10    MBSE                      Modelagem de sistemas        BDD + IBD + Rastreio
  11    Integrador                Conectar tudo                Fluxo end-to-end
  12    Projeto Final             Polimento + publicação       README profissional
```

---

# Dicas Gerais Para o Sucesso

**1. Não busque perfeição na primeira versão.** Publique o mínimo funcional no domingo e depois melhore durante a semana seguinte se necessário. Publicar com consistência é mais valioso do que ter um projeto perfeito daqui a 6 meses.

**2. Use o tempo de transporte e espera para estudar.** Os vídeos e artigos de estudo podem ser consumidos no celular. Reserve o computador para a construção.

**3. Se travar em um módulo, simplifique o escopo, não atrase.** Melhor entregar 15 consultas SQL do que não publicar nada porque queria fazer 30. Você pode sempre voltar e melhorar depois.

**4. O README é tão importante quanto o código.** Recrutadores raramente leem o código inteiro. Eles leem o README. Dedique tempo a ele.

**5. Cada post no LinkedIn deve contar uma história:** qual era o problema → o que você fez → o que aprendeu. Não seja técnico demais; pense no recrutador que não é programador.

**6. Mantenha um arquivo de "aprendizados" pessoal.** Anote erros, soluções, e insights de cada semana. Ao final das 12 semanas, esse material é ouro para entrevistas: "na semana 4, enfrentei um problema de idempotência no ETL e resolvi com UPSERT" demonstra maturidade técnica.
