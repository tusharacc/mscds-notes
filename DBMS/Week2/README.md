# Week 2: Introduction to SQL

## Overview

This week introduces SQL (Structured Query Language), the practical query language used across relational database systems. We cover SQL history and standardization, data definition language (DDL) for creating database schemas, basic query structure with SELECT-FROM-WHERE, and data manipulation operations. The content emphasizes practical SQL usage with SQLite demonstrations and covers essential concepts like joins, string operations, and aggregate functions.

## Key Concepts

- **SQL vs Relational Algebra**: SQL is a practical, standardized language for database operations, while relational algebra is a mathematical foundation
- **SQL Standardization**: ANSI/ISO standards (SQL-86, SQL-92, SQL-99, SQL:2003, SQL:2023) ensure portability across database vendors
- **Data Definition Language (DDL)**: Commands for creating and modifying database structure (CREATE, ALTER, DROP)
- **Data Manipulation Language (DML)**: Commands for querying and modifying data (SELECT, INSERT, UPDATE, DELETE)
- **Primary Key**: Unique identifier for records in a table
- **Foreign Key**: Reference to a primary key in another table, maintaining referential integrity
- **Natural Join**: Joins tables by matching all common attributes automatically

## SQL Components

### Parts of SQL
1. **Data Manipulation Language (DML)**: Insert, delete, modify records
2. **Data Definition Language (DDL)**: Define schemas, integrity constraints, views
3. **Transaction Control**: Begin/end transactions with atomicity guarantees
4. **Embedded SQL**: Integrate SQL within general-purpose languages (C, Python, Java)
5. **Authorization**: Control user access to tables and columns

## Domain Types (Data Types)

### String Types
- `CHAR(n)`: Fixed-length string of exactly n characters (padded with spaces)
- `VARCHAR(n)`: Variable-length string up to n characters (more space-efficient)

### Numeric Types
- `INT`: Machine-dependent integer (typically 64-bit)
- `SMALLINT`: Smaller integer (typically 2 bytes)
- `NUMERIC(p, d)`: Fixed precision decimal with p total digits, d after decimal point
  - Example: `NUMERIC(3,1)` can store 44.5 but not 444.5 or 0.32
- `REAL`, `DOUBLE PRECISION`: Floating-point numbers
- `FLOAT(n)`: Floating-point with precision n

### Other Types
- `DATE`: Calendar date
- `TIME`: Time of day

## Data Definition Language (DDL)

### Creating Tables

```sql
CREATE TABLE instructor (
    id CHAR(5),
    name VARCHAR(20) NOT NULL,
    dept_name VARCHAR(20),
    salary NUMERIC(8,2),
    PRIMARY KEY (id),
    FOREIGN KEY (dept_name) REFERENCES department
);
```

### Integrity Constraints

- **PRIMARY KEY**: Unique, non-null identifier
- **FOREIGN KEY**: References another table's primary key
- **NOT NULL**: Attribute cannot have null values

### Table Modification

```sql
-- Add a column
ALTER TABLE instructor ADD COLUMN office VARCHAR(10);

-- Remove a column
ALTER TABLE instructor DROP COLUMN office;

-- Delete all records
DELETE FROM instructor;

-- Remove entire table
DROP TABLE instructor;
```

**Warning**: When adding columns to existing tables, all current records get NULL values for the new column.

## Basic SQL Query Structure

### SELECT-FROM-WHERE Pattern

```sql
SELECT A1, A2, ..., An
FROM r1, r2, ..., rm
WHERE P;
```

- **SELECT clause**: Specifies attributes to retrieve (corresponds to **projection** in relational algebra)
- **FROM clause**: Lists relations to query (performs Cartesian product)
- **WHERE clause**: Specifies conditions/predicates (corresponds to **selection** in relational algebra)

**Important**: SQL's SELECT corresponds to relational algebra's **project** (π), not select (σ)

### Examples

```sql
-- Simple selection
SELECT name FROM instructor;

-- With condition
SELECT name
FROM instructor
WHERE dept_name = 'Comp. Sci.' AND salary > 70000;

-- Select all columns
SELECT * FROM instructor;

-- Rename output column
SELECT salary/12 AS monthly_salary FROM instructor;
```

## Distinct and Duplicate Handling

### Handling Duplicates

```sql
-- SQL allows duplicates by default (unlike relational algebra)
SELECT dept_name FROM instructor;  -- May show duplicates

-- Remove duplicates
SELECT DISTINCT dept_name FROM instructor;

-- Force showing all (including duplicates)
SELECT ALL dept_name FROM instructor;
```

## String Operations

### Pattern Matching with LIKE

- `%` matches any substring (like `*` in Unix)
- `_` matches exactly one character (like `?` in Unix)

```sql
-- Names starting with 'j'
SELECT name FROM instructor WHERE name LIKE 'j%';

-- Names containing 'dir'
SELECT name FROM instructor WHERE name LIKE '%dir%';

-- Exactly 3 characters
SELECT name FROM instructor WHERE name LIKE '___';

-- At least 3 characters
SELECT name FROM instructor WHERE name LIKE '___%';

-- Escape literal %
SELECT name WHERE name LIKE 'ab\%cd%' ESCAPE '\';
```

**Note**: Patterns are case-sensitive in most SQL implementations (though SQLite may differ)

### String Functions

- `||` : String concatenation
- `UPPER()`, `LOWER()`: Case conversion
- `LENGTH()`: String length
- `SUBSTRING()`: Extract substring

## Ordering Results

```sql
-- Ascending order (default)
ORDER BY name;

-- Descending order
ORDER BY salary DESC;

-- Multiple attributes
ORDER BY dept_name, name;  -- First by dept, then by name within each dept
```

## Comparison and Range Operators

### Comparison Operators
- `=` : Equal (single equals, not `==`)
- `<>` : Not equal (NOT `!=`)
- `<`, `<=`, `>`, `>=` : Standard comparisons

### BETWEEN Operator

```sql
-- Shorthand for range
WHERE salary BETWEEN 90000 AND 100000;

-- Equivalent to
WHERE salary >= 90000 AND salary <= 100000;
```

### Tuple Comparison

```sql
-- Compare multiple values at once
WHERE (instructor.id, dept_name) = (teaches.id, 'Biology');

-- Equivalent to
WHERE instructor.id = teaches.id AND dept_name = 'Biology';
```

## Joins

### Cartesian Product (Cross Join)

```sql
SELECT * FROM instructor, teaches;
```

Generates every possible combination of records from both tables.

### Natural Join (Implicit)

```sql
-- Using WHERE clause
SELECT name, course_id
FROM instructor, teaches
WHERE instructor.id = teaches.id;
```

### Self-Join with Renaming

```sql
-- Find instructors with salary > some CS instructor
SELECT T.name
FROM instructor AS T, instructor AS S
WHERE T.salary > S.salary AND S.dept_name = 'Comp. Sci.';

-- Note: AS keyword is optional
FROM instructor T, instructor S
```

### Self-Join Example: Employee-Supervisor

```sql
-- Find supervisor of Bob
SELECT supervisor
FROM emp_super
WHERE person = 'Bob';

-- Find supervisor of supervisor of Bob
SELECT S2.supervisor
FROM emp_super S1, emp_super S2
WHERE S1.person = 'Bob' AND S1.supervisor = S2.person;
```

## Set Operations

### UNION, INTERSECT, EXCEPT

```sql
-- Courses in Fall 2017 OR Spring 2018
(SELECT course_id FROM section WHERE semester = 'Fall' AND year = 2017)
UNION
(SELECT course_id FROM section WHERE semester = 'Spring' AND year = 2018);

-- Courses in BOTH semesters (intersection)
(SELECT course_id FROM section WHERE semester = 'Fall' AND year = 2017)
INTERSECT
(SELECT course_id FROM section WHERE semester = 'Spring' AND year = 2018);

-- Courses in Fall 2017 but NOT Spring 2018
(SELECT course_id FROM section WHERE semester = 'Fall' AND year = 2017)
EXCEPT
(SELECT course_id FROM section WHERE semester = 'Spring' AND year = 2018);
```

**Note**: Set operations automatically eliminate duplicates. Use `UNION ALL`, `INTERSECT ALL`, `EXCEPT ALL` to retain duplicates.

## Null Values

### Handling NULL

```sql
-- Check for null
SELECT name FROM instructor WHERE salary IS NULL;

-- Check for non-null
SELECT name FROM instructor WHERE salary IS NOT NULL;
```

### NULL in Arithmetic and Comparisons

- Any arithmetic operation with NULL returns NULL: `5 + NULL = NULL`
- Any comparison with NULL returns **UNKNOWN** (not NULL): `5 < NULL = UNKNOWN`
- WHERE clause treats UNKNOWN as FALSE

### Three-Valued Logic

| AND | TRUE | FALSE | UNKNOWN |
|-----|------|-------|---------|
| TRUE | TRUE | FALSE | UNKNOWN |
| FALSE | FALSE | FALSE | FALSE |
| UNKNOWN | UNKNOWN | FALSE | UNKNOWN |

| OR | TRUE | FALSE | UNKNOWN |
|----|------|-------|---------|
| TRUE | TRUE | TRUE | TRUE |
| FALSE | TRUE | FALSE | UNKNOWN |
| UNKNOWN | TRUE | UNKNOWN | UNKNOWN |

## Aggregate Functions

### Functions
- `AVG()`: Average value
- `MIN()`: Minimum value
- `MAX()`: Maximum value
- `SUM()`: Sum of values
- `COUNT()`: Count of rows

### Examples

```sql
-- Average salary in CS department
SELECT AVG(salary)
FROM instructor
WHERE dept_name = 'Comp. Sci.';

-- Number of instructors
SELECT COUNT(*) FROM instructor;

-- Number of distinct salaries
SELECT COUNT(DISTINCT salary) FROM instructor;
```

### GROUP BY

```sql
-- Average salary per department
SELECT dept_name, AVG(salary) AS avg_salary
FROM instructor
GROUP BY dept_name;
```

**Rule**: Attributes in SELECT must either:
1. Appear in GROUP BY clause, OR
2. Be inside an aggregate function

```sql
-- WRONG: id not in GROUP BY
SELECT dept_name, id, AVG(salary) FROM instructor GROUP BY dept_name;

-- CORRECT
SELECT dept_name, AVG(salary) FROM instructor GROUP BY dept_name;
```

### HAVING Clause

Filters groups (like WHERE filters rows):

```sql
-- Departments with average salary > 42000
SELECT dept_name, AVG(salary) AS avg_salary
FROM instructor
GROUP BY dept_name
HAVING AVG(salary) > 42000;
```

**WHERE vs HAVING**:
- **WHERE**: Filters individual records before grouping
- **HAVING**: Filters groups after aggregation

## Data Manipulation

### INSERT

```sql
-- Single record
INSERT INTO instructor VALUES ('10211', 'Smith', 'Biology', 66000);

-- Specify columns (different order)
INSERT INTO course (title, course_id, credits, dept_name)
VALUES ('Database Systems', 'CS-437', 4, 'Comp. Sci.');

-- Insert with NULL
INSERT INTO student VALUES ('3003', 'Green', 'Finance', NULL);

-- Insert from query
INSERT INTO instructor
SELECT id, name, dept_name, 18000
FROM student
WHERE dept_name = 'Music' AND total_credits > 144;
```

### DELETE

```sql
-- Delete all records
DELETE FROM student;

-- Delete with condition
DELETE FROM instructor WHERE dept_name = 'Finance';

-- Delete with subquery
DELETE FROM instructor
WHERE dept_name IN (
    SELECT dept_name FROM department WHERE building = 'Watson'
);

-- Delete based on aggregate
DELETE FROM instructor
WHERE salary < (SELECT AVG(salary) FROM instructor);
```

**Important**: SQL evaluates the entire SELECT before deleting, so average is computed on original data.

### UPDATE

```sql
-- Give 5% raise to all
UPDATE instructor SET salary = salary * 1.05;

-- Conditional update
UPDATE instructor
SET salary = salary * 1.05
WHERE salary < 70000;

-- Update with subquery
UPDATE instructor
SET salary = salary * 1.05
WHERE salary < (SELECT AVG(salary) FROM instructor);

-- Conditional update with CASE
UPDATE instructor
SET salary = CASE
    WHEN salary <= 100000 THEN salary * 1.05
    ELSE salary * 1.03
END;
```

## SQLite Specifics

### Starting SQLite

```bash
# Open database file
sqlite3 mydb.db

# Show tables
.tables

# Show schema
.schema instructor

# Show help
.help

# Exit
.exit  # or Ctrl+D
```

### SQLite Differences from Standard SQL

1. **Types are optional**: SQLite infers types (defaults to VARCHAR for text)
2. **Foreign keys disabled by default**: Use `PRAGMA foreign_keys = ON;` to enable
3. **Case-insensitive LIKE**: Unlike most SQL implementations
4. **Dot commands**: Special commands starting with `.` (like `.tables`, `.schema`)

## Important Notes and Best Practices

### Design Principles

1. **Avoid NULL when possible**: NULL values complicate queries and can cause unexpected behavior
2. **Use appropriate data types**: Choose CHAR for fixed-length, VARCHAR for variable-length
3. **Define integrity constraints**: Use PRIMARY KEY and FOREIGN KEY to maintain data consistency
4. **Fixed table schemas**: Design tables upfront; rarely ALTER after deployment
5. **One table per entity type**: Don't create separate tables for each student/course (violates normalization)

### Common Mistakes

1. **Using `==` instead of `=`**: SQL uses single equals for comparison
2. **Using `!=` instead of `<>`**: Standard SQL uses `<>` for not-equal
3. **Forgetting DISTINCT**: SQL allows duplicates by default
4. **Mixing up WHERE and HAVING**: WHERE for rows, HAVING for groups
5. **Wrong attribute names in GROUP BY**: Attributes in SELECT must be in GROUP BY or aggregated

### Performance Tips

1. **Use indexes** for frequently queried columns (covered in later chapters)
2. **Aggregate in SQL** rather than application code (more efficient)
3. **Let SQL optimize joins**: Database engines optimize Cartesian products automatically

## Practical Examples

### University Database Schema

```sql
-- Instructor table
CREATE TABLE instructor (
    id CHAR(5) PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    dept_name VARCHAR(20),
    salary NUMERIC(8,2),
    FOREIGN KEY (dept_name) REFERENCES department
);

-- Course table
CREATE TABLE course (
    course_id CHAR(7) PRIMARY KEY,
    title VARCHAR(50),
    dept_name VARCHAR(20),
    credits NUMERIC(2,0),
    FOREIGN KEY (dept_name) REFERENCES department
);

-- Student table
CREATE TABLE student (
    id CHAR(5) PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    dept_name VARCHAR(20),
    tot_cred NUMERIC(3,0),
    FOREIGN KEY (dept_name) REFERENCES department
);

-- Takes table (students enrolled in courses)
CREATE TABLE takes (
    id CHAR(5),
    course_id CHAR(7),
    sec_id CHAR(3),
    semester VARCHAR(6),
    year NUMERIC(4,0),
    grade CHAR(2),
    PRIMARY KEY (id, course_id, sec_id, semester, year),
    FOREIGN KEY (id) REFERENCES student,
    FOREIGN KEY (course_id, sec_id, semester, year) REFERENCES section
);
```

### Complex Queries

```sql
-- List students and courses they've taken
SELECT name, course_id
FROM student NATURAL JOIN takes;

-- Instructors in Art department who taught courses
SELECT name, course_id
FROM instructor, teaches
WHERE instructor.id = teaches.id AND instructor.dept_name = 'Art';

-- Departments with more than one instructor
SELECT dept_name, COUNT(*) AS num_instructors
FROM instructor
GROUP BY dept_name
HAVING COUNT(*) > 1;
```

## Summary

Week 2 establishes SQL fundamentals covering:
- SQL history, standardization, and importance
- Data definition with CREATE, ALTER, DROP
- Basic queries with SELECT-FROM-WHERE
- String operations and pattern matching
- Joins (implicit cross product with WHERE conditions)
- Set operations (UNION, INTERSECT, EXCEPT)
- NULL handling and three-valued logic
- Aggregate functions (AVG, SUM, COUNT, MIN, MAX)
- Grouping with GROUP BY and HAVING
- Data manipulation with INSERT, UPDATE, DELETE

The foundation established this week is essential for building real-world database applications, with emphasis on practical usage through SQLite demonstrations.
