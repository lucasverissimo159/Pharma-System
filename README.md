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
