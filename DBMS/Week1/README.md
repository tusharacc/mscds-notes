# Week 1: Introduction to Database Management Systems

## Course Overview

**Instructor:** Professor Vikram Pudi, IIIT Hyderabad

This introductory course on Database Management Systems (DBMS) focuses on how to model, design, and implement databases from an application developer's perspective. The course emphasizes practical application development rather than deep internals of database systems.

### What This Course Covers
- Database modeling and design
- Implementation techniques for databases
- Application development using databases
- Brief overview of database internals
- Query processing and relational algebra

### What This Course Does NOT Cover
- Comprehensive textbook-level detail (textbook reading is required)
- Speech-to-text conversion of textbooks
- Installation guides and spoon-feeding
- Deep database internals (focus is on usage)

## Why Study Database Management Systems?

DBMS represents "computer science in action" and caters to diverse interests:

1. **Theory enthusiasts:** Mathematical foundations including sets, relations, theorems, and proofs
2. **Algorithm designers:** Implementation of sorting, searching, divide-and-conquer algorithms
3. **Systems builders:** Large-scale application development
4. **Simulation experts:** Performance analysis across different scenarios

### Practical Importance
- Required in all non-trivial applications (web apps, mobile apps, etc.)
- Eliminates need to build everything from scratch
- Provides ready-to-use features for data storage and retrieval
- Essential for startups and career opportunities

### The DRY Principle
"Do Not Repeat Yourself" - DBMS provides features out-of-the-box that developers would otherwise need to build repeatedly for each application.

## Recommended Textbooks

1. **Ramakrishnan and Gehrke** - Database Management Systems
2. **Elmasri and Navathe** - Fundamentals of Database Systems
3. **Silberschatz, Korth, and Sudarshan** - Database System Concepts (course follows this)

## The Relational Model

### Structure of Relational Databases

A **relation** is essentially a table consisting of:
- **Rows** (also called **tuples**): Represent actual data records
- **Columns** (also called **attributes**): Represent the structure/schema

### Example: Instructor Relation

```
Instructor
+--------+-------------+---------------+--------+
| ID     | Name        | Dept_Name     | Salary |
+--------+-------------+---------------+--------+
| 10101  | Srinivasan  | Comp. Sci.    | 65000  |
| 12121  | Wu          | Finance       | 90000  |
| 15151  | Mozart      | Music         | 40000  |
| 22222  | Einstein    | Physics       | 95000  |
| 32343  | El Said     | History       | 60000  |
| 33456  | Gold        | Physics       | 87000  |
+--------+-------------+---------------+--------+
```

### Mathematical View of Relations

- **Relation schema:** R = (A₁, A₂, A₃, ..., Aₙ) - The template/design of the table
- **Relation instance:** The actual table with data at a given time
- **Tuple:** An element t of relation r, represented by a row
- **Domain:** Set of allowed values for each attribute
- **Atomic values:** Attributes are indivisible units
- **Null value:** Special value indicating unknown data (member of every domain)

**Important:** Relations are unordered - the order of tuples is irrelevant (set theory principle).

## Database Schema vs. Instance

- **Database Schema:** Logical structure/design of the database (fixed at design time)
- **Database Instance:** Snapshot of data at a given instant (changes as data is added/modified)

**Best Practice:** Fix your schema during database design and avoid frequent changes. Adding columns later requires populating existing records, which is problematic.

## Keys

### Super Key
A subset K of attributes R is a **super key** if K's values are sufficient to uniquely identify each tuple.

**Example:** In the Instructor table:
- ID is a super key
- {ID, Name} is also a super key (any superset of a super key is also a super key)

### Candidate Key
A **candidate key** is a minimal super key - no proper subset is a super key.

**Example:** ID is a candidate key (minimal), but {ID, Name} is not (not minimal).

### Primary Key
One of the candidate keys chosen by the database designer to uniquely identify records.

**Example:** ID is the primary key for the Instructor table.

### Foreign Key
An attribute in one relation that references the primary key of another relation.

**Example:**
- `Dept_Name` in Instructor table references the Department table
- **Referencing relation:** Instructor
- **Referenced relation:** Department

## University Database Schema Example

A realistic database contains multiple related tables:

### Core Tables
1. **Instructor** (ID, Name, Dept_Name, Salary)
2. **Department** (Dept_Name, Building, Budget)
3. **Student** (ID, Name, Dept_Name, Tot_Credits)
4. **Course** (Course_ID, Title, Dept_Name, Credits)
5. **Section** (Course_ID, Sec_ID, Semester, Year, Building, Room_Number, Time_Slot_ID)
6. **Teaches** (ID, Course_ID, Sec_ID, Semester, Year)
7. **Takes** (ID, Course_ID, Sec_ID, Semester, Year, Grade)
8. **Prereq** (Course_ID, Prereq_ID)
9. **Advisor** (S_ID, I_ID)
10. **Classroom** (Building, Room_Number, Capacity)
11. **Time_Slot** (Time_Slot_ID, Day, Start_Time, End_Time)

### Design Considerations
- Avoid redundancy (e.g., semester appears in both Takes and Section - redundant)
- Don't store instructor name in Course table (multiple instructors, multiple semesters)
- Prerequisites can have multiple rows for one course (one row per prerequisite)

## Relational Query Languages

### Types of Query Languages

1. **Procedural:** Specify WHAT data is needed AND HOW to get it
2. **Non-procedural (Declarative):** Specify WHAT data is needed only

### Pure Mathematical Languages
- **Relational Algebra** (procedural)
- **Tuple Relational Calculus** (non-procedural)
- **Domain Relational Calculus** (non-procedural)

These languages are:
- Equivalent in computing power
- NOT Turing complete (cannot do everything C/Python can do)
- Designed specifically for database queries

## Relational Algebra

A procedural, mathematically-oriented query language based on six basic operations.

### Six Basic Operations

#### 1. Select (σ)
Selects tuples satisfying a given predicate (condition).

**Notation:** σₚ(r)

**Example:**
```
σ_Dept_Name="Physics"(Instructor)
```
Returns all instructors in the Physics department.

**Comparison Operations Allowed:**
- = (equal)
- ≠ (not equal)
- > (greater than)
- ≥ (greater than or equal)
- < (less than)
- ≤ (less than or equal)

**Combining Predicates:**
- AND (∧)
- OR (∨)
- NOT (¬)

**Example:**
```
σ_Dept_Name="Physics" ∧ Salary>90000(Instructor)
```

**Attribute Comparisons:**
```
σ_Dept_Name=Building(Department)
```

#### 2. Project (Π)
Returns a relation with only specified attributes, removing duplicates.

**Notation:** Π_{A₁, A₂, ..., Aₖ}(r)

**Example:**
```
Π_ID,Name,Salary(Instructor)
```
Returns only ID, Name, and Salary columns (department name excluded).

**Composition Example:**
```
Π_Name(σ_Dept_Name="Physics"(Instructor))
```
Returns names of all physics department instructors.

#### 3. Cartesian Product (×)
Combines information from two relations by creating all possible pairs.

**Notation:** r × s

**Result:** For every row in r and every row in s, create a combined row.

**Example:**
```
Instructor × Teaches
```

**Important Notes:**
- Number of result rows = (rows in r) × (rows in s)
- Attributes with same name get prefixed: `Instructor.ID`, `Teaches.ID`
- Often creates many irrelevant combinations (needs filtering)
- Computationally expensive - use carefully

#### 4. Join (⋈)
Combines Cartesian product with selection - more efficient than separate operations.

**Notation:** r ⋈_θ s

**Mathematical Definition:**
```
r ⋈_θ s = σ_θ(r × s)
```

**Example:**
```
Instructor ⋈_Instructor.ID=Teaches.ID Teaches
```
Returns only rows where instructor ID matches teaches ID.

**Why Join is Important:**
- Combines information across tables efficiently
- Result is typically much smaller than Cartesian product
- Backend implementations optimize joins beyond simple cross-product filtering

#### 5. Union (∪)
Combines two relations into one.

**Requirements:**
- Same arity (number of attributes)
- Compatible attribute domains (same types in same order)

**Example:**
```
Π_Course_ID(σ_Semester="Fall" ∧ Year=2017(Section))
∪
Π_Course_ID(σ_Semester="Spring" ∧ Year=2018(Section))
```
Returns courses taught in Fall 2017 OR Spring 2018.

#### 6. Set Difference (−)
Returns tuples in first relation but not in second.

**Requirements:** Same as union (same arity, compatible domains)

**Example:**
```
Π_Course_ID(σ_Semester="Fall" ∧ Year=2017(Section))
−
Π_Course_ID(σ_Semester="Spring" ∧ Year=2018(Section))
```
Returns courses taught in Fall 2017 but NOT in Spring 2018.

### Additional Operations

#### Set Intersection (∩)
Returns tuples present in both relations.

**Example:**
```
Π_Course_ID(σ_Semester="Fall" ∧ Year=2017(Section))
∩
Π_Course_ID(σ_Semester="Spring" ∧ Year=2018(Section))
```
Returns courses taught in BOTH Fall 2017 AND Spring 2018.

#### Assignment (←)
Stores intermediate results in variables for readability.

**Example:**
```
physics ← σ_Dept_Name="Physics"(Instructor)
music ← σ_Dept_Name="Music"(Instructor)
physics ∪ music
```

#### Rename (ρ)
Returns result under a new name, enabling use in larger expressions.

**Notation:** ρ_x(E)

Returns relation E under name x.

### Query Equivalence and Optimization

Multiple queries can produce the same result with different efficiency.

**Example 1:**
```
Query 1: σ_Dept_Name="Physics" ∧ Salary>90000(Instructor)
Query 2: σ_Dept_Name="Physics"(σ_Salary>90000(Instructor))
```
Both return the same result, but Query 2 may be more efficient if few instructors have salary > 90000.

**Example 2:**
```
Query 1: σ_Dept_Name="Physics"(Instructor ⋈ Teaches)
Query 2: σ_Dept_Name="Physics"(Instructor) ⋈ Teaches
```
Query 2 is more efficient - filters before expensive join operation.

**Query Optimizer:** Database systems automatically choose the most efficient execution plan regardless of how the query is written.

## Data Definition Language (DDL)

Language for defining database schema (structure).

### SQL DDL Example

```sql
CREATE TABLE Instructor (
    ID          CHAR(5),
    Name        VARCHAR(20),
    Dept_Name   VARCHAR(20),
    Salary      NUMERIC(8,2)
);
```

**Data Types:**
- `CHAR(n)`: Fixed-length character string (exactly n characters)
- `VARCHAR(n)`: Variable-length character string (up to n characters)
- `NUMERIC(p,d)`: Numeric with p total digits, d after decimal point

### DDL Compiler and Data Dictionary

**DDL Compiler** generates table templates stored in the **data dictionary**.

**Data Dictionary Contains (Metadata):**
- Database schema (table structures, column types)
- Integrity constraints (e.g., primary keys, salary ≥ 0)
- Authorization information (who can access what)

**Primary Key Constraint:**
```sql
CREATE TABLE Instructor (
    ID CHAR(5) PRIMARY KEY,
    ...
);
```

## Data Manipulation Language (DML)

Language for querying and modifying data.

### Types of DML

1. **Procedural DML:**
   - Specify WHAT data is needed AND HOW to get it
   - User describes exact procedure to retrieve data

2. **Declarative (Non-procedural) DML:**
   - Specify WHAT data is needed only
   - Easier to learn and use
   - SQL is a declarative DML

### SQL Query Example

```sql
SELECT Name
FROM Instructor
WHERE Dept_Name = 'Comp. Sci.';
```

**Components:**
- `SELECT`: Specifies attributes to retrieve
- `FROM`: Specifies table(s)
- `WHERE`: Specifies conditions

**Input:** One or more tables
**Output:** Single table (single column in this example)

### SQL is NOT Turing Complete

**Cannot do:**
- Arbitrary programs
- User input
- Direct screen output
- Network communication

**Solution:** Embed SQL in host languages (C, Python, Java)

### Language Extensions and APIs

**Embedding SQL in Host Languages:**
- Python database modules (e.g., `sqlite3`, `psycopg2`)
- SQL queries passed as strings
- Results returned to host language

**Database APIs:**
- **ODBC** (Open Database Connectivity)
- **JDBC** (Java Database Connectivity)
- Neutral APIs independent of specific programming languages

## Application Programs and Database Access

Databases are used within larger application programs:
- Web applications (most common)
- Mobile applications
- Desktop applications

**Typical Flow:**
1. User interacts with application interface
2. Application generates SQL queries
3. Database returns results
4. Application formats and displays results

## Database Design

### Logical Design
- How to organize data into tables without redundancy
- Ensuring all necessary queries can be asked
- **Normal Forms:** Techniques for good database design (covered in future chapters)

### Physical Design
- How tables are stored on disk
- File organization and block allocation
- Contiguous vs. non-contiguous storage

## Database Engine Components

### 1. Storage Manager

Responsible for storing, retrieving, and updating data efficiently.

**Components:**
- **Authorization and Integrity Manager:** Ensures authorized access only
- **Transaction Manager:** Manages transaction execution
- **File Manager:** Interacts with OS to manage files on disk
- **Buffer Manager:** Manages data movement between disk and main memory

**Storage Structures:**
- **Data files:** Actual table data
- **Data dictionary:** Metadata (schema, authorization)
- **Indices:** Fast access structures (like textbook index)

**Performance Impact:** Poor storage management can make simple queries take hours instead of milliseconds.

### 2. Query Processor

Responsible for executing user queries efficiently.

**Components:**

#### DDL Interpreter
- Interprets DDL statements
- Stores definitions in data dictionary

#### DML Compiler
- Translates DML queries into query plans
- Performs **query optimization**
- Generates low-level instructions

#### Query Evaluation Engine
- Executes query plans
- Returns results

**Query Optimization Process:**
1. Parse user query
2. Translate to relational algebra
3. Generate multiple possible query plans
4. Use statistics (table sizes, data distribution) to estimate costs
5. Select lowest-cost plan
6. Execute plan

**Why Optimization Matters:** Can reduce execution time from hours to milliseconds.

### 3. Transaction Management

A **transaction** is a collection of operations performing a single logical function.

**Example:** Money transfer between bank accounts
```sql
-- Both must succeed or both must fail
UPDATE Account SET Balance = Balance - 100 WHERE Account_ID = 'A';
UPDATE Account SET Balance = Balance + 100 WHERE Account_ID = 'B';
```

**Transaction Properties Ensured:**
- **Atomicity:** All operations complete or none complete (indivisible)
- **Consistency:** Database remains in valid state
- **Isolation:** Concurrent transactions don't interfere
- **Durability:** Committed changes survive failures

**Components:**

#### Transaction Manager
- Ensures atomicity and consistency
- Handles recovery from failures (power, disk, OS crashes)

#### Concurrency Control Manager
- Allows multiple users to execute transactions simultaneously
- Prevents conflicts (e.g., two users modifying same account)
- Uses locking mechanisms
- Allows parallel read-only transactions

## Database Architecture

### 1. Centralized Architecture
- Database runs on single machine (possibly powerful server)
- Multiple cores, shared memory possible
- Users log into the machine to access database

### 2. Client-Server Architecture
- **Server:** Database engine runs here
- **Clients:** Applications connect remotely
- Most common for web/mobile applications
- No need to SSH into server

### 3. Parallel Databases
Speed up execution through parallelism:
- **Shared Memory:** Multiple cores, shared memory
- **Shared Disk:** Separate memory spaces, shared disk
- **Shared Nothing:** Separate machines, data partitioned across them

### 4. Distributed Databases
- Geographically distributed database servers
- Common for large enterprises (multinational corporations)
- May have schema heterogeneity (different schemas at different locations)
- Example: Supermarket chain with database at each store

## Application Architecture

### Two-Tier Architecture
```
[Client Machine]          [Server Machine]
  Application   <----->   Database System
```
- Application on client directly accesses database server

### Three-Tier Architecture
```
[Client Machine]          [Application Server]     [Database Server]
  Web Browser    <----->   Web Application   <---> Database System
```
- Client accesses application server (e.g., web server)
- Application server accesses database
- Most common for modern web applications

## Database Users

### 1. Naive Users
- Don't know SQL or query languages
- Use applications built by programmers
- Applications execute pre-written queries

### 2. Application Programmers
- Write applications containing SQL queries
- Create compiled application programs
- Develop user interfaces

### 3. Sophisticated Users (Analysts)
- Know SQL or other query languages
- Don't necessarily write full applications
- Perform data analysis and generate reports
- Understand business domain and translate to queries
- Use query tools for analysis

### 4. Database Administrators (DBAs)

**Responsibilities:**
- **Schema definition:** Design table structures
- **Storage structure and access methods:** Decide physical organization
- **Schema modification:** Modify structure when needed
- **Authorization:** Grant user access rights
- **Routine maintenance:** Monitor disk space, backups, etc.

**Importance:** DBAs are key assets to organizations, often well-compensated, not just doing mundane tasks.

## History of Database Systems

### 1950s-1960s: Early Data Processing
- **Storage:** Magnetic tapes (sequential access, slow)
- **Input:** Punch cards
- **Impact:** Programmers were more careful due to difficulty of making changes

### 1960s-1970s: Hard Disks Emerge
- **Storage:** Hard disks enabled random access
- **Models:** Network and hierarchical data models popular

### 1970s: Relational Model Revolution
- **Ted Codd** defined the relational model (ACM Turing Award winner)
- **Prototypes:**
  - IBM's System R
  - UC Berkeley's Ingres (Michael Stonebraker)
- **Commercial:** Oracle released first commercial relational DBMS
- Still captures ~50% of database market today

### 1980s: Relational Systems Mature
- Research on query optimization, transaction processing, logging
- Development of parallel and distributed databases
- Object-oriented databases emerge (niche market)

### 1990s: Decision Support and Web
- **Data warehousing:** Multi-terabyte repositories
- **Data mining:** Decision support applications
- **OLAP:** Online Analytical Processing
- **Web commerce:** Database-backed web applications

### 2000s: Big Data Era
- **Big Data Systems:** Google BigTable, Yahoo PNUTS, Amazon systems
- **NoSQL:** Designed for horizontal scalability across machines
- **Criticism of SQL:** Limited to single-machine scalability
- **Use Case:** Very large-scale applications (Facebook, Google)
- **MapReduce:** Data analysis on distributed systems

### 2010s: SQL Reloaded
- **SQL front-ends:** For MapReduce systems
- **Massively parallel databases:** Using SQL
- **Main-memory databases:** Entire database fits in RAM
  - Main memory became cheaper
  - Eliminates disk I/O bottleneck
  - Hundreds of times faster than disk-based systems
- **Reality:** Both SQL and NoSQL coexist, serving different needs

### Current State
- **Relational databases:** Still dominant for medium-scale applications
- **NoSQL:** Best for very large-scale, horizontally-scalable applications
- **Main-memory databases:** For applications fitting in RAM
- **Trade-offs:** Relational provides flexibility and general queries; NoSQL provides scalability

## Key Takeaways

### Why Use DBMS?
- Avoid reinventing the wheel
- Proven, efficient data storage and retrieval
- Built-in transaction management, concurrency control, recovery
- Query optimization

### Relational Model Benefits
- Mathematical foundation (sets and relations)
- Proven over 50+ years
- Flexible query capabilities
- Broad tool and talent ecosystem

### Learning Approach
- Understand concepts, not just syntax
- Practice is essential (lectures alone insufficient)
- Ask "why" things work, not just "how"
- Study recommended textbooks alongside lectures

### Career Opportunities
- Application programmer
- Data analyst
- Database administrator
- Database engineer/architect
