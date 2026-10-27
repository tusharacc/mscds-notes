# Week 3: Intermediate SQL

## Overview

This week advances SQL knowledge beyond basics, covering nested subqueries, various join types (natural, inner, outer), views for data abstraction and security, transactions, integrity constraints, custom data types, indexing for performance, and authorization mechanisms. The content focuses on making SQL more effective for complex applications and understanding how databases maintain data consistency and security.

## Nested Subqueries

Subqueries allow embedding one query within another, enabling powerful multi-step data retrieval.

### Subquery Locations

1. **FROM clause**: Subquery result becomes a temporary table
2. **WHERE clause**: Subquery result used in conditions
3. **SELECT clause**: Must return single value (scalar subquery)

### Set Membership: IN and NOT IN

```sql
-- Courses in Fall 2017 AND Spring 2018 (intersection)
SELECT DISTINCT course_id
FROM section
WHERE semester = 'Fall' AND year = 2017
  AND course_id IN (
      SELECT course_id
      FROM section
      WHERE semester = 'Spring' AND year = 2018
  );

-- Courses in Fall 2017 but NOT in Spring 2018 (difference)
SELECT DISTINCT course_id
FROM section
WHERE semester = 'Fall' AND year = 2017
  AND course_id NOT IN (
      SELECT course_id
      FROM section
      WHERE semester = 'Spring' AND year = 2018
  );

-- Simple usage
SELECT name
FROM instructor
WHERE name NOT IN ('Mozart', 'Einstein');
```

### Set Comparison: SOME and ALL

**SOME (or ANY)**: True if condition holds for **at least one** value

```sql
-- Find instructors with salary > SOME instructor in Biology
-- (i.e., greater than the minimum Biology salary)
SELECT name
FROM instructor
WHERE salary > SOME (
    SELECT salary
    FROM instructor
    WHERE dept_name = 'Biology'
);
```

**Semantics of SOME**:
- `5 < SOME (0, 5, 6)` → TRUE (5 < 6)
- `5 < SOME (0, 5)` → FALSE (not less than any)
- `5 = SOME (0, 5)` → TRUE (equals 5)
- `5 <> SOME (4, 6)` → TRUE (5 ≠ 4)
- `= SOME` is equivalent to `IN`
- `<> SOME` is **NOT** equivalent to `NOT IN`

**ALL**: True if condition holds for **all** values

```sql
-- Find instructors with salary > ALL instructors in Biology
-- (i.e., greater than the maximum Biology salary)
SELECT name
FROM instructor
WHERE salary > ALL (
    SELECT salary
    FROM instructor
    WHERE dept_name = 'Biology'
);
```

**Semantics of ALL**:
- `5 < ALL (6, 10)` → TRUE (less than both)
- `5 < ALL (4, 5, 6)` → FALSE (not less than 4 or 5)
- `5 = ALL (5, 5)` → Could be TRUE if all are 5
- `5 <> ALL (4, 6)` → TRUE (not equal to any)
- `<> ALL` is equivalent to `NOT IN`

### EXISTS and NOT EXISTS

**EXISTS**: Returns TRUE if subquery returns any results (non-empty set)

```sql
-- Courses offered in both Fall 2017 and Spring 2018
SELECT course_id
FROM section AS S
WHERE semester = 'Fall' AND year = 2017
  AND EXISTS (
      SELECT *
      FROM section AS T
      WHERE semester = 'Spring' AND year = 2018
        AND S.course_id = T.course_id
  );
```

**NOT EXISTS**: Returns TRUE if subquery returns no results (empty set)

```sql
-- Students who have taken ALL courses offered by Biology department
SELECT S.id, S.name
FROM student AS S
WHERE NOT EXISTS (
    -- Courses in Biology that student S has NOT taken
    (SELECT course_id FROM course WHERE dept_name = 'Biology')
    EXCEPT
    (SELECT T.course_id FROM takes AS T WHERE S.id = T.id)
);
```

**Key Insight**: `X - Y = ∅` is equivalent to `X ⊆ Y` (X is subset of Y)

### UNIQUE

Tests whether subquery has duplicate tuples (returns TRUE if no duplicates)

```sql
-- Find courses offered at most once in 2017
SELECT T.course_id
FROM course AS T
WHERE UNIQUE (
    SELECT R.course_id
    FROM section AS R
    WHERE T.course_id = R.course_id AND year = 2017
);
```

### Subqueries in FROM Clause

```sql
-- Departments with average salary > 42000 (without HAVING)
SELECT dept_name, avg_salary
FROM (
    SELECT dept_name, AVG(salary) AS avg_salary
    FROM instructor
    GROUP BY dept_name
) AS dept_avg
WHERE avg_salary > 42000;

-- Rename entire result table
SELECT dept_name, average
FROM (
    SELECT dept_name, AVG(salary)
    FROM instructor
    GROUP BY dept_name
) AS dept_avg(dept_name, average)
WHERE average > 42000;
```

### WITH Clause

Defines temporary named result sets for cleaner queries:

```sql
-- Find departments with maximum budget
WITH max_budget(value) AS (
    SELECT MAX(budget)
    FROM department
)
SELECT dept_name
FROM department, max_budget
WHERE department.budget = max_budget.value;

-- Complex query with multiple WITH clauses
WITH dept_total(dept_name, value) AS (
    SELECT dept_name, SUM(salary)
    FROM instructor
    GROUP BY dept_name
),
dept_total_avg(value) AS (
    SELECT AVG(value)
    FROM dept_total
)
SELECT dept_name
FROM dept_total, dept_total_avg
WHERE dept_total.value > dept_total_avg.value;
```

### Scalar Subqueries

Must return exactly one value (single row, single column):

```sql
-- List departments with number of instructors
SELECT dept_name, (
    SELECT COUNT(*)
    FROM instructor
    WHERE department.dept_name = instructor.dept_name
) AS num_instructors
FROM department;
```

**Error if subquery returns multiple values!**

## Join Operations

### Join Types and Conditions

SQL supports combining **join type** with **join condition**:

**Join Types** (how to handle non-matching tuples):
- `INNER JOIN`: Discard non-matching tuples (default)
- `LEFT OUTER JOIN`: Preserve tuples from left relation
- `RIGHT OUTER JOIN`: Preserve tuples from right relation
- `FULL OUTER JOIN`: Preserve tuples from both relations

**Join Conditions** (how to match tuples):
- `NATURAL`: Match all common attributes
- `USING (A1, A2, ...)`: Match specified attributes
- `ON <predicate>`: Match using custom condition

### Natural Join

Automatically matches **all** attributes with the same name:

```sql
-- List student names with courses they've taken
SELECT name, course_id
FROM student NATURAL JOIN takes;
```

**Without natural join (equivalent)**:
```sql
SELECT name, course_id
FROM student, takes
WHERE student.id = takes.id;
```

**Caution**: Natural join matches ALL common attributes, which may cause issues if unrelated attributes share names (e.g., `name` in student vs `name` in course).

### Inner Join with ON

Explicitly specify join condition:

```sql
SELECT *
FROM student JOIN takes ON student.id = takes.id;
```

**Key Difference from Natural Join**: Common attributes appear **twice** in result (e.g., `student.id` and `takes.id` both present)

### Outer Joins

Preserve information from relations even when no match exists.

#### Example Tables

**course**:
| course_id | title | dept_name | credits |
|-----------|-------|-----------|---------|
| BIO-301 | Genetics | Biology | 4 |
| CS-190 | Game Design | Comp. Sci. | 4 |
| CS-315 | Robotics | Comp. Sci. | 3 |

**prereq**:
| course_id | prereq_id |
|-----------|-----------|
| BIO-301 | BIO-101 |
| CS-190 | CS-101 |
| CS-347 | CS-101 |

**Note**: CS-315 has no prerequisites; CS-347 exists in prereq but not in course table.

#### LEFT OUTER JOIN

Preserve all tuples from **left** relation:

```sql
SELECT *
FROM course NATURAL LEFT OUTER JOIN prereq;
```

**Result**:
| course_id | title | dept_name | credits | prereq_id |
|-----------|-------|-----------|---------|-----------|
| BIO-301 | Genetics | Biology | 4 | BIO-101 |
| CS-190 | Game Design | Comp. Sci. | 4 | CS-101 |
| CS-315 | Robotics | Comp. Sci. | 3 | **NULL** |

**Symbol**: `⟕` (left side preserved)

#### RIGHT OUTER JOIN

Preserve all tuples from **right** relation:

```sql
SELECT *
FROM course NATURAL RIGHT OUTER JOIN prereq;
```

**Result**:
| course_id | title | dept_name | credits | prereq_id |
|-----------|-------|-----------|---------|-----------|
| BIO-301 | Genetics | Biology | 4 | BIO-101 |
| CS-190 | Game Design | Comp. Sci. | 4 | CS-101 |
| CS-347 | **NULL** | **NULL** | **NULL** | CS-101 |

**Symbol**: `⟖` (right side preserved)

#### FULL OUTER JOIN

Preserve tuples from **both** relations:

```sql
SELECT *
FROM course NATURAL FULL OUTER JOIN prereq;
```

**Result**:
| course_id | title | dept_name | credits | prereq_id |
|-----------|-------|-----------|---------|-----------|
| BIO-301 | Genetics | Biology | 4 | BIO-101 |
| CS-190 | Game Design | Comp. Sci. | 4 | CS-101 |
| CS-315 | Robotics | Comp. Sci. | 3 | **NULL** |
| CS-347 | **NULL** | **NULL** | **NULL** | CS-101 |

**Symbol**: `⟗` (both sides preserved)

### USING Clause

Specify which attributes to use for natural join:

```sql
-- Join only on course_id (not all common attributes)
SELECT *
FROM course FULL OUTER JOIN prereq USING (course_id);
```

**Advantage**: Prevents unintended matches on attributes like `name` that may have different meanings.

**Difference from ON**: With USING, common attribute appears **once** in output; with ON, it appears **twice**.

### Join Examples Summary

```sql
-- Natural inner join (default)
course NATURAL JOIN prereq

-- Natural left outer join
course NATURAL LEFT OUTER JOIN prereq

-- Using specific columns
course FULL OUTER JOIN prereq USING (course_id)

-- Explicit condition
course LEFT OUTER JOIN prereq ON course.course_id = prereq.course_id
```

## Views

Views are virtual tables defined by queries, providing:
1. **Data abstraction**: Hide complexity
2. **Security**: Restrict access to specific data
3. **Simplification**: Reuse complex queries

### Creating Views

```sql
-- View of instructors without salary information
CREATE VIEW faculty AS
SELECT id, name, dept_name
FROM instructor;

-- View with aggregation
CREATE VIEW dept_stats AS
SELECT dept_name, COUNT(*) AS num_instructors
FROM instructor
GROUP BY dept_name;
```

### Using Views

```sql
-- Query view like a table
SELECT name FROM faculty WHERE dept_name = 'Biology';

-- Views can reference other views
CREATE VIEW physics_faculty AS
SELECT * FROM faculty WHERE dept_name = 'Physics';
```

### Materialized Views

- **Logical views**: Recomputed each query (standard)
- **Materialized views**: Stored physically, updated when base tables change
  - Faster queries but requires maintenance
  - Not in standard SQL but supported by many vendors

### Updating Views

**Simple views** (single table, no aggregates) are updatable:

```sql
-- Allowed
INSERT INTO faculty VALUES ('30128', 'Green', 'Music');

-- Translates to
INSERT INTO instructor VALUES ('30128', 'Green', 'Music', NULL);
```

**Complex views** (joins, aggregates) generally **not updatable**:

```sql
-- Most systems reject this
INSERT INTO dept_stats VALUES ('Psychology', 10);
```

**Reason**: Ambiguous how to update base tables.

## Transactions

A **transaction** is a sequence of queries/updates treated as a **single unit**:

```sql
-- Transfer $50 from A to B
BEGIN TRANSACTION;
UPDATE account SET balance = balance - 50 WHERE account_number = 'A-101';
UPDATE account SET balance = balance + 50 WHERE account_number = 'A-201';
COMMIT;
```

### ACID Properties

- **Atomicity**: All operations succeed or all fail (no partial execution)
- **Consistency**: Database remains in valid state
- **Isolation**: Concurrent transactions don't interfere
- **Durability**: Committed changes survive crashes

### Transaction Commands

- `BEGIN TRANSACTION`: Start transaction
- `COMMIT`: Finalize changes
- `ROLLBACK`: Undo all changes since BEGIN

```sql
BEGIN TRANSACTION;
DELETE FROM instructor WHERE dept_name = 'Finance';
-- Oops, mistake!
ROLLBACK;  -- Undo deletion
```

## Integrity Constraints

Ensure database consistency by preventing invalid data.

### Constraint Types

1. **NOT NULL**: Attribute cannot be null
2. **PRIMARY KEY**: Unique, non-null identifier
3. **FOREIGN KEY**: References primary key in another table
4. **UNIQUE**: No duplicate values (but allows multiple NULLs)
5. **CHECK**: Custom condition

### Examples

```sql
CREATE TABLE instructor (
    id CHAR(5) PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    dept_name VARCHAR(20),
    salary NUMERIC(8,2) CHECK (salary > 0),
    FOREIGN KEY (dept_name) REFERENCES department
);

-- Multiple column primary key
CREATE TABLE takes (
    id CHAR(5),
    course_id CHAR(7),
    sec_id CHAR(3),
    semester VARCHAR(6),
    year NUMERIC(4,0),
    PRIMARY KEY (id, course_id, sec_id, semester, year)
);

-- Unique constraint
CREATE TABLE department (
    dept_name VARCHAR(20) UNIQUE,
    building VARCHAR(15),
    budget NUMERIC(12,2)
);
```

### Referential Integrity

When foreign key constraint is violated, actions:

1. **Reject** (default): Disallow operation
2. **Cascade**: Propagate change
3. **Set NULL**: Set foreign key to NULL
4. **Set DEFAULT**: Set to default value

```sql
CREATE TABLE course (
    course_id CHAR(7) PRIMARY KEY,
    dept_name VARCHAR(20),
    FOREIGN KEY (dept_name) REFERENCES department
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
```

**Cascade Example**:
- Delete department → Automatically deletes all courses in that department
- Update department name → Automatically updates dept_name in all courses

### CHECK Constraints

```sql
-- Simple check
CREATE TABLE instructor (
    salary NUMERIC(8,2) CHECK (salary >= 0)
);

-- Complex check
CREATE TABLE section (
    semester VARCHAR(6),
    year NUMERIC(4,0),
    CHECK (semester IN ('Fall', 'Winter', 'Spring', 'Summer'))
);

-- Table-level check
CREATE TABLE time_slot (
    time_slot_id CHAR(4),
    day VARCHAR(1),
    start_time TIME,
    end_time TIME,
    CHECK (start_time < end_time)
);
```

### Assertions (Not Widely Supported)

Global constraints across tables:

```sql
-- Ensure every student has an advisor
CREATE ASSERTION student_advisor_check CHECK (
    NOT EXISTS (
        SELECT * FROM student
        WHERE tot_cred > 0 AND id NOT IN (SELECT student_id FROM advisor)
    )
);
```

**Note**: Few systems support assertions due to performance overhead.

## SQL Data Types and Schemas

### Built-in Types

- **BLOB**: Binary Large Object (images, files)
- **CLOB**: Character Large Object (documents)
- **XML**: XML documents
- **JSON**: JSON data (SQL:2023)

### User-Defined Types

```sql
-- Distinct type (strong typing)
CREATE TYPE Dollars AS NUMERIC(12,2) FINAL;

CREATE TABLE department (
    dept_name VARCHAR(20),
    budget Dollars
);

-- Cannot mix types
-- budget + 100  -- ERROR
-- budget + CAST(100 AS Dollars)  -- OK
```

### Domains

Create reusable constraints:

```sql
CREATE DOMAIN degree_level AS VARCHAR(10)
    CHECK (VALUE IN ('Bachelors', 'Masters', 'Doctorate'));

CREATE TABLE student (
    name VARCHAR(20),
    degree degree_level
);
```

### Large Objects

```sql
-- Store images
CREATE TABLE images (
    image_id INT,
    image BLOB
);

-- Store documents
CREATE TABLE documents (
    doc_id INT,
    content CLOB
);
```

## Indexes

Indexes dramatically speed up queries on specific attributes.

### Creating Indexes

```sql
-- Single column index
CREATE INDEX instructor_name_idx ON instructor(name);

-- Multi-column index
CREATE INDEX takes_course_idx ON takes(course_id, semester, year);

-- Unique index (enforces uniqueness)
CREATE UNIQUE INDEX student_id_idx ON student(id);
```

### When to Use Indexes

**Create indexes on**:
- Primary keys (usually automatic)
- Foreign keys
- Frequently queried columns
- Columns in WHERE, ORDER BY, JOIN conditions

**Don't overuse**:
- Indexes consume space
- Slow down INSERT/UPDATE/DELETE

### Dropping Indexes

```sql
DROP INDEX instructor_name_idx;
```

### Example Impact

**Without index**:
```sql
SELECT * FROM instructor WHERE id = '10101';
-- Scans all 100,000 records (slow)
```

**With index**:
```sql
CREATE INDEX instructor_id_idx ON instructor(id);
SELECT * FROM instructor WHERE id = '10101';
-- Direct lookup (fast)
```

## Authorization

Control who can access/modify data.

### Privileges

- **SELECT**: Read data
- **INSERT**: Add records
- **UPDATE**: Modify records
- **DELETE**: Remove records
- **ALL PRIVILEGES**: All of the above

### Granting Privileges

```sql
-- Grant SELECT to specific user
GRANT SELECT ON instructor TO user1;

-- Grant multiple privileges
GRANT SELECT, INSERT ON student TO user2;

-- Grant all privileges
GRANT ALL PRIVILEGES ON course TO admin;

-- Grant to all users
GRANT SELECT ON department TO PUBLIC;

-- Grant with ability to grant to others
GRANT SELECT ON instructor TO user3 WITH GRANT OPTION;
```

### Revoking Privileges

```sql
-- Revoke SELECT
REVOKE SELECT ON instructor FROM user1;

-- Revoke with cascade
REVOKE SELECT ON instructor FROM user3 CASCADE;
-- Also revokes from anyone user3 granted to
```

### Roles

Group users with similar privileges:

```sql
-- Create role
CREATE ROLE teaching_assistant;

-- Grant privileges to role
GRANT SELECT ON course TO teaching_assistant;
GRANT SELECT ON section TO teaching_assistant;

-- Assign role to users
GRANT teaching_assistant TO user4;
GRANT teaching_assistant TO user5;
```

### Column-Level Authorization

```sql
-- Grant access only to specific columns
GRANT UPDATE (salary) ON instructor TO payroll_dept;

-- User can update salary but not other columns
```

## Important Notes and Best Practices

### Query Optimization

1. **Use EXISTS over IN** for correlated subqueries (often faster)
2. **Use INNER JOIN** explicitly rather than implicit joins in WHERE
3. **Create indexes** on frequently queried columns
4. **Avoid SELECT *** when you only need specific columns
5. **Use UNION ALL** instead of UNION if duplicates are acceptable (faster)

### Design Principles

1. **Minimize NULL values**: Complicate queries and indexes
2. **Use foreign keys**: Enforce referential integrity at database level
3. **Create views** for complex queries used repeatedly
4. **Use transactions** for multi-step operations requiring consistency
5. **Apply principle of least privilege**: Grant minimum necessary access

### Common Mistakes

1. **Forgetting NULL handling** in outer joins
2. **Using natural join carelessly** when attributes have same name but different meaning
3. **Not using indexes** on large tables
4. **Over-indexing**: Too many indexes slow down writes
5. **Granting excessive privileges**: Security risk

## Summary

Week 3 covers advanced SQL features essential for complex applications:

**Nested Subqueries**: IN/NOT IN, SOME/ALL, EXISTS/NOT EXISTS, UNIQUE, WITH clause
**Join Operations**: Natural, inner, left/right/full outer joins; USING vs ON
**Views**: Virtual tables for abstraction, security, and reusability
**Transactions**: ACID properties ensuring data consistency
**Integrity Constraints**: NOT NULL, PRIMARY/FOREIGN KEY, CHECK, referential integrity
**Custom Types**: User-defined types, domains, large objects
**Indexes**: Performance optimization for queries
**Authorization**: Privileges, roles, column-level access control

These concepts enable building robust, secure, and performant database applications while maintaining data integrity and consistency.
