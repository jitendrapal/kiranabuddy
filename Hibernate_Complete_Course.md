# 📚 HIBERNATE COMPLETE COURSE

## _Master Object-Relational Mapping (ORM) with Hibernate_

---

## 📖 TABLE OF CONTENTS

### **PART 1: HIBERNATE FUNDAMENTALS**

1. Introduction to Hibernate
2. Setting Up Hibernate Environment
3. Hibernate Architecture
4. First Hibernate Application
5. Hibernate Configuration
6. Session and SessionFactory

### **PART 2: MAPPING CONCEPTS**

7. Entity Mapping
8. Primary Key Generation Strategies
9. Value Type Mapping
10. Embedded Objects
11. Collections Mapping
12. Component Mapping

### **PART 3: ASSOCIATIONS**

13. One-to-One Mapping
14. One-to-Many Mapping
15. Many-to-One Mapping
16. Many-to-Many Mapping
17. Bidirectional Associations
18. Cascade Operations

### **PART 4: ADVANCED CONCEPTS**

19. Inheritance Mapping
20. HQL (Hibernate Query Language)
21. Criteria API
22. Native SQL Queries
23. Named Queries
24. Caching in Hibernate

### **PART 5: PERFORMANCE & BEST PRACTICES**

25. Lazy vs Eager Loading
26. Fetching Strategies
27. N+1 Problem and Solutions
28. Transaction Management
29. Hibernate Best Practices
30. Integration with Spring

---

## 📘 PART 1: HIBERNATE FUNDAMENTALS

---

## Chapter 1: Introduction to Hibernate

### 📌 What is Hibernate?

**Hibernate** is a powerful, high-performance **Object-Relational Mapping (ORM)** framework for Java. It simplifies database programming by mapping Java objects to database tables and vice versa, eliminating the need to write complex JDBC code.

**Think of Hibernate as a Translator:**

Imagine you're traveling to a foreign country where you don't speak the language. You need a translator to communicate with locals. Similarly:

- **You (Java Developer)** speak "Object-Oriented Language" (Java objects, classes)
- **Database** speaks "Relational Language" (tables, rows, columns, SQL)
- **Hibernate (Translator)** converts between these two languages automatically

**Real-World Analogy - Library Management System:**

Without Hibernate (Traditional JDBC):

```
You want to save a Book object:
1. Write SQL: "INSERT INTO books (id, title, author, price) VALUES (?, ?, ?, ?)"
2. Create PreparedStatement
3. Set parameters manually: stmt.setInt(1, book.getId())
4. Execute query
5. Handle exceptions
6. Close resources
7. Repeat for every operation!
```

With Hibernate (ORM):

```
You want to save a Book object:
1. session.save(book);  // That's it! Hibernate handles everything!
```

### 🎯 Why Do We Need Hibernate?

**Problems with Traditional JDBC:**

1. **Too Much Boilerplate Code**

   - Writing repetitive SQL queries
   - Manual object-to-table mapping
   - Resource management (connections, statements)

2. **Database Dependency**

   - SQL queries are database-specific
   - Changing database requires code changes

3. **No Object-Oriented Approach**

   - Working with ResultSets instead of objects
   - Manual conversion between objects and data

4. **Difficult Relationship Management**

   - Complex code for handling associations
   - Manual foreign key management

5. **No Caching**
   - Every query hits the database
   - Performance issues

**How Hibernate Solves These Problems:**

| Problem             | Hibernate Solution               |
| ------------------- | -------------------------------- |
| Boilerplate Code    | Automatic SQL generation         |
| Database Dependency | Database-independent HQL         |
| Object Mapping      | Automatic ORM                    |
| Relationships       | Automatic association handling   |
| Performance         | Built-in caching mechanisms      |
| Transactions        | Automatic transaction management |

### 🏗️ Hibernate Architecture Overview

**Analogy: Restaurant Kitchen System**

Think of Hibernate like a restaurant kitchen:

- **Your Application (Customer)** - Orders food (requests data)
- **Session (Waiter)** - Takes orders and serves food
- **SessionFactory (Kitchen Manager)** - Manages all waiters
- **Configuration (Recipe Book)** - Contains all instructions
- **Transaction (Order Ticket)** - Ensures order is complete
- **Database (Storage/Pantry)** - Where ingredients (data) are stored

**Hibernate Architecture Diagram:**

```
┌─────────────────────────────────────────────────────────┐
│                  Java Application                        │
│                  (Your Code)                             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Hibernate Framework                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │Configuration │→ │SessionFactory│→ │   Session    │  │
│  └──────────────┘  └──────────────┘  └──────┬───────┘  │
│                                              │          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────▼───────┐  │
│  │ Transaction  │  │    Query     │  │  Criteria    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                    JDBC Layer                            │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Database (MySQL, Oracle, etc.)              │
└─────────────────────────────────────────────────────────┘
```

### 🔑 Key Features of Hibernate

**1. Object-Relational Mapping (ORM)**

- Maps Java classes to database tables
- Maps Java objects to table rows
- Maps Java properties to table columns

**2. Database Independence**

- Write once, run on any database
- Uses HQL (Hibernate Query Language) instead of SQL
- Automatic SQL generation for different databases

**3. Automatic Table Creation**

- Can create/update database schema automatically
- No need to write DDL statements

**4. Caching**

- **First-Level Cache** (Session-level) - Enabled by default
- **Second-Level Cache** (SessionFactory-level) - Optional
- **Query Cache** - Caches query results

**5. Lazy Loading**

- Loads data only when needed
- Improves performance
- Reduces memory usage

**6. Association Management**

- Automatic handling of relationships
- One-to-One, One-to-Many, Many-to-One, Many-to-Many
- Cascade operations

**7. Transaction Management**

- ACID properties support
- Integration with JTA
- Automatic rollback on errors

### 📊 Hibernate vs JDBC Comparison

| Feature              | JDBC                 | Hibernate                |
| -------------------- | -------------------- | ------------------------ |
| **Code Length**      | 100+ lines for CRUD  | 10-20 lines              |
| **SQL Writing**      | Manual               | Automatic                |
| **Object Mapping**   | Manual               | Automatic                |
| **Database Change**  | Requires code change | No code change           |
| **Caching**          | No built-in support  | Built-in caching         |
| **Lazy Loading**     | Not supported        | Supported                |
| **Associations**     | Manual handling      | Automatic                |
| **Learning Curve**   | Easy                 | Moderate                 |
| **Performance**      | Good (if optimized)  | Excellent (with caching) |
| **Boilerplate Code** | High                 | Low                      |

### 🌟 Hibernate Versions

**Evolution of Hibernate:**

- **Hibernate 1.x** (2001) - Initial release
- **Hibernate 2.x** (2003) - Added collections support
- **Hibernate 3.x** (2005) - Major improvements, annotations
- **Hibernate 4.x** (2011) - Multi-tenancy, improved performance
- **Hibernate 5.x** (2015) - Java 8 support, better performance
- **Hibernate 6.x** (2022) - Latest version, Jakarta EE support

**Current Version:** Hibernate 6.x (as of 2024)

### 🎓 What You'll Learn in This Course

**By the end of this course, you will be able to:**

✅ Understand ORM concepts and Hibernate architecture
✅ Set up Hibernate in Java projects
✅ Map Java classes to database tables
✅ Perform CRUD operations without writing SQL
✅ Handle complex associations (One-to-One, One-to-Many, etc.)
✅ Write queries using HQL and Criteria API
✅ Implement caching for better performance
✅ Optimize Hibernate applications
✅ Integrate Hibernate with Spring Framework
✅ Build real-world applications using Hibernate

### 📋 Prerequisites

**Before starting this course, you should have:**

✅ **Core Java Knowledge**

- OOP concepts (Classes, Objects, Inheritance)
- Collections Framework
- Exception Handling

✅ **Basic SQL Knowledge**

- SELECT, INSERT, UPDATE, DELETE
- Table creation and relationships
- Primary and Foreign keys

✅ **JDBC Basics** (Helpful but not mandatory)

- Understanding of database connectivity
- Basic CRUD operations

### 💼 Career Opportunities

**After mastering Hibernate, you can work as:**

- Java Developer
- Backend Developer
- Hibernate Developer
- Full Stack Java Developer
- Spring Boot Developer
- Enterprise Application Developer

**Average Salary Range:**

- Fresher: ₹3-5 LPA
- 2-3 Years: ₹6-10 LPA
- 5+ Years: ₹12-20 LPA

---

## Chapter 2: Setting Up Hibernate Environment

### 🛠️ Required Tools and Software

**Analogy: Setting Up a Professional Workshop**

Just like a carpenter needs tools (hammer, saw, drill) to build furniture, you need specific tools to develop Hibernate applications.

**Tools You'll Need:**

1. **JDK (Java Development Kit)** - The foundation
2. **IDE (Eclipse/IntelliJ IDEA)** - Your workspace
3. **Database (MySQL/PostgreSQL)** - Data storage
4. **Maven/Gradle** - Dependency management
5. **Hibernate JARs** - The ORM framework

### 📥 Step 1: Install Java Development Kit (JDK)

**What is JDK?**
JDK is like the engine of a car - without it, nothing runs!

**Installation Steps:**

1. **Download JDK:**

   - Visit: https://www.oracle.com/java/technologies/downloads/
   - Download JDK 17 or later (LTS version recommended)

2. **Install JDK:**

   - Run the installer
   - Follow installation wizard
   - Note the installation path

3. **Set Environment Variables:**

**Windows:**

```
JAVA_HOME = C:\Program Files\Java\jdk-17
Path = %JAVA_HOME%\bin
```

**Linux/Mac:**

```bash
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk
export PATH=$JAVA_HOME/bin:$PATH
```

4. **Verify Installation:**

```bash
java -version
javac -version
```

**Expected Output:**

```
java version "17.0.8" 2023-07-18 LTS
Java(TM) SE Runtime Environment (build 17.0.8+9-LTS-211)
```

### 📥 Step 2: Install IDE (IntelliJ IDEA / Eclipse)

**Option 1: IntelliJ IDEA (Recommended)**

1. Download from: https://www.jetbrains.com/idea/download/
2. Choose Community Edition (Free) or Ultimate (Paid)
3. Install and launch
4. Configure JDK in IDE settings

**Option 2: Eclipse**

1. Download from: https://www.eclipse.org/downloads/
2. Choose "Eclipse IDE for Java Developers"
3. Extract and run
4. Set workspace location

### 📥 Step 3: Install Database (MySQL)

**What is MySQL?**
MySQL is like a warehouse where all your data is stored in organized shelves (tables).

**Installation Steps:**

1. **Download MySQL:**

   - Visit: https://dev.mysql.com/downloads/mysql/
   - Download MySQL Community Server

2. **Install MySQL:**

   - Run installer
   - Set root password (remember this!)
   - Choose default settings

3. **Install MySQL Workbench** (GUI Tool):

   - Download from same website
   - Useful for managing databases visually

4. **Verify Installation:**

```bash
mysql --version
```

5. **Create Database:**

```sql
CREATE DATABASE hibernate_db;
USE hibernate_db;
```

### 📥 Step 4: Set Up Maven Project

**What is Maven?**
Maven is like a smart assistant that automatically downloads and manages all the libraries (JARs) your project needs.

**Create Maven Project:**

**Using IntelliJ IDEA:**

1. File → New → Project
2. Select "Maven"
3. Enter:
   - GroupId: com.example
   - ArtifactId: hibernate-demo
4. Click Finish

**Using Eclipse:**

1. File → New → Maven Project
2. Check "Create a simple project"
3. Enter GroupId and ArtifactId
4. Click Finish

**Project Structure:**

```
hibernate-demo/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/example/
│   │   │       ├── entity/
│   │   │       ├── dao/
│   │   │       └── util/
│   │   └── resources/
│   │       └── hibernate.cfg.xml
│   └── test/
├── pom.xml
└── target/
```

### 📥 Step 5: Add Hibernate Dependencies

**Edit pom.xml:**

```xml
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">

    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>hibernate-demo</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <hibernate.version>6.2.7.Final</hibernate.version>
    </properties>

    <dependencies>
        <!-- Hibernate Core -->
        <dependency>
            <groupId>org.hibernate.orm</groupId>
            <artifactId>hibernate-core</artifactId>
            <version>${hibernate.version}</version>
        </dependency>

        <!-- MySQL Connector -->
        <dependency>
            <groupId>com.mysql</groupId>
            <artifactId>mysql-connector-j</artifactId>
            <version>8.0.33</version>
        </dependency>

        <!-- Logging (Optional but recommended) -->
        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-simple</artifactId>
            <version>2.0.7</version>
        </dependency>
    </dependencies>
</project>
```

**What Each Dependency Does:**

| Dependency        | Purpose                  |
| ----------------- | ------------------------ |
| hibernate-core    | Main Hibernate framework |
| mysql-connector-j | MySQL database driver    |
| slf4j-simple      | Logging framework        |

**After adding dependencies:**

1. Right-click on project → Maven → Reload Project (IntelliJ)
2. Or Right-click on project → Maven → Update Project (Eclipse)

### 📥 Step 6: Create Hibernate Configuration File

**Create file:** `src/main/resources/hibernate.cfg.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">

<hibernate-configuration>
    <session-factory>
        <!-- Database Connection Settings -->
        <property name="hibernate.connection.driver_class">
            com.mysql.cj.jdbc.Driver
        </property>
        <property name="hibernate.connection.url">
            jdbc:mysql://localhost:3306/hibernate_db?useSSL=false
        </property>
        <property name="hibernate.connection.username">root</property>
        <property name="hibernate.connection.password">your_password</property>

        <!-- SQL Dialect -->
        <property name="hibernate.dialect">
            org.hibernate.dialect.MySQLDialect
        </property>

        <!-- Echo SQL to console -->
        <property name="hibernate.show_sql">true</property>
        <property name="hibernate.format_sql">true</property>

        <!-- Auto create/update database schema -->
        <property name="hibernate.hbm2ddl.auto">update</property>

        <!-- Connection Pool Settings -->
        <property name="hibernate.connection.pool_size">10</property>

        <!-- Current Session Context -->
        <property name="hibernate.current_session_context_class">thread</property>
    </session-factory>
</hibernate-configuration>
```

**Configuration Properties Explained:**

| Property                | Description                                     |
| ----------------------- | ----------------------------------------------- |
| connection.driver_class | JDBC driver class                               |
| connection.url          | Database URL                                    |
| connection.username     | Database username                               |
| connection.password     | Database password                               |
| dialect                 | SQL dialect for database                        |
| show_sql                | Print SQL to console                            |
| format_sql              | Format SQL for readability                      |
| hbm2ddl.auto            | Auto schema generation (create/update/validate) |

**hbm2ddl.auto Values:**

| Value       | Description                                    |
| ----------- | ---------------------------------------------- |
| create      | Drop and create tables every time              |
| create-drop | Create on start, drop on exit                  |
| update      | Update schema if needed (safe for development) |
| validate    | Only validate schema, don't change             |
| none        | Do nothing                                     |

### ✅ Step 7: Verify Setup

**Create a utility class:** `src/main/java/com/example/util/HibernateUtil.java`

```java
package com.example.util;

import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;

public class HibernateUtil {
    private static SessionFactory sessionFactory;

    static {
        try {
            // Create SessionFactory from hibernate.cfg.xml
            sessionFactory = new Configuration()
                    .configure("hibernate.cfg.xml")
                    .buildSessionFactory();
            System.out.println("✅ Hibernate SessionFactory created successfully!");
        } catch (Exception e) {
            System.err.println("❌ Error creating SessionFactory: " + e.getMessage());
            e.printStackTrace();
        }
    }

    public static SessionFactory getSessionFactory() {
        return sessionFactory;
    }

    public static void shutdown() {
        if (sessionFactory != null) {
            sessionFactory.close();
        }
    }

    // Test method
    public static void main(String[] args) {
        SessionFactory sf = HibernateUtil.getSessionFactory();
        if (sf != null) {
            System.out.println("🎉 Hibernate setup is successful!");
            System.out.println("SessionFactory: " + sf);
        }
        HibernateUtil.shutdown();
    }
}
```

**Run the test:**

- Right-click on HibernateUtil.java → Run As → Java Application

**Expected Output:**

```
✅ Hibernate SessionFactory created successfully!
🎉 Hibernate setup is successful!
SessionFactory: org.hibernate.internal.SessionFactoryImpl@...
```

**Common Setup Issues:**

| Issue                         | Solution                                            |
| ----------------------------- | --------------------------------------------------- |
| ClassNotFoundException        | Check if all dependencies are added                 |
| Unable to connect to database | Verify MySQL is running and credentials are correct |
| Dialect error                 | Use correct dialect for your database version       |
| Port 3306 already in use      | Change MySQL port or stop conflicting service       |

**Key Takeaways:**

- ✅ Hibernate requires JDK, IDE, Database, and Maven
- ✅ Add Hibernate dependencies in pom.xml
- ✅ Configure database connection in hibernate.cfg.xml
- ✅ SessionFactory is created once and reused
- ✅ Use HibernateUtil for centralized SessionFactory management
- ✅ Always test your setup before writing business logic

---

## Chapter 3: Hibernate Architecture

### 🏗️ Understanding Hibernate Architecture

**Analogy: Hotel Management System**

Think of Hibernate architecture like a **5-star hotel**:

- **Configuration** = Hotel Blueprint (how everything is set up)
- **SessionFactory** = Hotel Building (one per city, expensive to build)
- **Session** = Hotel Room (one per guest, many rooms in building)
- **Transaction** = Room Service Order (must be completed or cancelled)
- **Query** = Room Service Menu (different ways to order food)
- **Criteria** = Custom Order (specific dietary requirements)

Just like a hotel has a structure to serve guests efficiently, Hibernate has an architecture to manage database operations efficiently!

### 📊 Hibernate Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Java Application Layer                    │
│              (Your Business Logic & Entities)                │
│                  Student, Employee, Product                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Hibernate Framework Layer                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Configuration Object                     │   │
│  │  • Reads hibernate.cfg.xml                           │   │
│  │  • Loads mapping files/annotations                   │   │
│  │  • Validates settings                                │   │
│  └────────────────────┬─────────────────────────────────┘   │
│                       │                                      │
│                       ▼                                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            SessionFactory (Immutable)                 │   │
│  │  • Created once per application                      │   │
│  │  • Thread-safe (can be shared)                       │   │
│  │  • Heavy object (expensive to create)                │   │
│  │  • Holds second-level cache                          │   │
│  └────────────────────┬─────────────────────────────────┘   │
│                       │                                      │
│                       ▼                                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Session (Not Thread-safe)                │   │
│  │  • Created per request/transaction                   │   │
│  │  • Lightweight object                                │   │
│  │  • Wraps JDBC connection                             │   │
│  │  • Holds first-level cache                           │   │
│  └────────────────────┬─────────────────────────────────┘   │
│                       │                                      │
│         ┌─────────────┼─────────────┐                       │
│         ▼             ▼             ▼                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │Transaction│  │  Query   │  │ Criteria │                  │
│  │  (ACID)  │  │  (HQL)   │  │  (API)   │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                      JDBC Layer                              │
│              (Database Driver & Connection)                  │
│                  Connection, Statement                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Database Layer                            │
│              (MySQL, Oracle, PostgreSQL, etc.)               │
│                    Tables, Rows, Columns                     │
└─────────────────────────────────────────────────────────────┘
```

### 🔑 Core Components of Hibernate

#### **1. Configuration**

**What is it?**
Configuration is the **first object** you create in Hibernate. It reads configuration files and prepares Hibernate for initialization.

**Real-World Analogy:**
Think of Configuration as a **recipe book** that contains all instructions for cooking (setting up Hibernate). Before you start cooking, you read the recipe to know what ingredients you need and how to prepare them.

**How it works:**

```java
// Create Configuration object
Configuration config = new Configuration();

// Read hibernate.cfg.xml from classpath
config.configure("hibernate.cfg.xml");

// Add entity classes
config.addAnnotatedClass(Student.class);
config.addAnnotatedClass(Employee.class);

// Build SessionFactory
SessionFactory factory = config.buildSessionFactory();
```

**Key Responsibilities:**

| Responsibility       | Description                                           |
| -------------------- | ----------------------------------------------------- |
| Read Configuration   | Reads hibernate.cfg.xml or hibernate.properties       |
| Load Mappings        | Loads entity classes with annotations or XML mappings |
| Validate Settings    | Validates database connection and dialect             |
| Build SessionFactory | Creates SessionFactory object                         |

**Configuration Methods:**

```java
// Different ways to configure
Configuration config = new Configuration();

// 1. Default configuration file (hibernate.cfg.xml)
config.configure();

// 2. Custom configuration file
config.configure("custom-hibernate.cfg.xml");

// 3. Programmatic configuration
config.setProperty("hibernate.connection.url", "jdbc:mysql://localhost:3306/mydb");
config.setProperty("hibernate.dialect", "org.hibernate.dialect.MySQLDialect");

// 4. Add annotated classes
config.addAnnotatedClass(Student.class);
```

#### **2. SessionFactory**

**What is it?**
SessionFactory is a **factory** for Session objects. It's created once per application and is **thread-safe**.

**Real-World Analogy:**
Think of SessionFactory as a **Car Factory** 🏭:

- You build the factory once (expensive and time-consuming)
- The factory produces many cars (Sessions)
- The factory can serve multiple customers simultaneously (thread-safe)
- You don't destroy the factory after making one car (reusable)

**Characteristics:**

| Feature           | Description                                       |
| ----------------- | ------------------------------------------------- |
| **Creation**      | Created once per application (singleton pattern)  |
| **Thread-Safety** | Thread-safe (can be shared across threads)        |
| **Weight**        | Heavy object (expensive to create)                |
| **Immutability**  | Immutable after creation (cannot be modified)     |
| **Caching**       | Holds second-level cache (shared across sessions) |
| **Lifecycle**     | Lives throughout application lifecycle            |
| **Cost**          | High creation cost, low usage cost                |

**Code Example:**

```java
public class HibernateUtil {
    // Create SessionFactory only once (singleton)
    private static SessionFactory sessionFactory;

    static {
        try {
            sessionFactory = new Configuration()
                    .configure()
                    .addAnnotatedClass(Student.class)
                    .buildSessionFactory();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static SessionFactory getSessionFactory() {
        return sessionFactory;
    }

    public static void shutdown() {
        if (sessionFactory != null) {
            sessionFactory.close();
        }
    }
}
```

**Best Practices:**

| Practice                                        | Reason                      |
| ----------------------------------------------- | --------------------------- |
| ✅ Create only ONE SessionFactory per database  | Expensive to create         |
| ✅ Make it a singleton                          | Ensure single instance      |
| ✅ Create at application startup                | Avoid delays during runtime |
| ✅ Close at application shutdown                | Release resources           |
| ❌ Don't create multiple SessionFactory objects | Wastes memory and resources |
| ❌ Don't create SessionFactory per request      | Very slow and inefficient   |

**SessionFactory Methods:**

```java
SessionFactory factory = HibernateUtil.getSessionFactory();

// Open a new Session
Session session = factory.openSession();

// Get current Session (requires configuration)
Session currentSession = factory.getCurrentSession();

// Check if SessionFactory is closed
boolean isClosed = factory.isClosed();

// Close SessionFactory
factory.close();
```

#### **3. Session**

**What is it?**
Session is a **single-threaded, short-lived** object that represents a conversation between application and database.

**Real-World Analogy:**
Think of Session as a **Shopping Cart** 🛒:

- You get a new cart for each shopping trip (short-lived)
- You can't share your cart with others (not thread-safe)
- You add/remove items during shopping (CRUD operations)
- You checkout when done (commit transaction)
- You return the cart after checkout (close session)
- Next time you shop, you get a new cart (new session)

**Characteristics:**

| Feature           | Description                                            |
| ----------------- | ------------------------------------------------------ |
| **Creation**      | Created per request/transaction                        |
| **Thread-Safety** | NOT thread-safe (one per thread)                       |
| **Weight**        | Lightweight object (cheap to create)                   |
| **Lifecycle**     | Short-lived (open → use → close)                       |
| **Caching**       | Holds first-level cache (session-specific)             |
| **JDBC**          | Wraps JDBC connection                                  |
| **State**         | Tracks entity states (transient, persistent, detached) |

**Session Lifecycle:**

```
┌─────────────────────────────────────────────────────┐
│  1. OPEN SESSION                                    │
│     Session session = factory.openSession();        │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│  2. BEGIN TRANSACTION                               │
│     Transaction tx = session.beginTransaction();    │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│  3. PERFORM OPERATIONS                              │
│     session.save(student);                          │
│     session.update(employee);                       │
│     session.delete(product);                        │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│  4. COMMIT TRANSACTION                              │
│     tx.commit();                                    │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│  5. CLOSE SESSION                                   │
│     session.close();                                │
└─────────────────────────────────────────────────────┘
```

**Session Methods:**

| Method           | Description                | Example                               |
| ---------------- | -------------------------- | ------------------------------------- |
| save()           | Insert new record          | session.save(student)                 |
| persist()        | Insert (JPA standard)      | session.persist(student)              |
| update()         | Update existing record     | session.update(student)               |
| merge()          | Update or insert           | session.merge(student)                |
| delete()         | Delete record              | session.delete(student)               |
| get()            | Retrieve by ID (immediate) | session.get(Student.class, 1)         |
| load()           | Retrieve by ID (lazy)      | session.load(Student.class, 1)        |
| createQuery()    | Create HQL query           | session.createQuery("FROM Student")   |
| createCriteria() | Create Criteria query      | session.createCriteria(Student.class) |

**Code Example:**

```java
// Open session
Session session = HibernateUtil.getSessionFactory().openSession();
Transaction tx = null;

try {
    // Begin transaction
    tx = session.beginTransaction();

    // Create new student
    Student student = new Student("John Doe", "john@email.com");
    session.save(student);

    // Retrieve student
    Student retrieved = session.get(Student.class, 1);
    System.out.println("Student: " + retrieved.getName());

    // Update student
    retrieved.setEmail("newemail@email.com");
    session.update(retrieved);

    // Commit transaction
    tx.commit();
    System.out.println("✅ Transaction successful!");

} catch (Exception e) {
    // Rollback on error
    if (tx != null) {
        tx.rollback();
    }
    e.printStackTrace();
} finally {
    // Always close session
    session.close();
}
```

#### **4. Transaction**

**What is it?**
Transaction represents a unit of work with the database. It ensures **ACID properties** (Atomicity, Consistency, Isolation, Durability).

**Real-World Analogy:**
Think of Transaction as a **Bank Transfer** 💰:

- Either the complete transfer happens (commit) or nothing happens (rollback)
- You can't have half a transfer (atomicity)
- If something goes wrong, money returns to original account (rollback)
- Multiple people can do transfers simultaneously (isolation)

**ACID Properties:**

| Property        | Description                  | Example                                                |
| --------------- | ---------------------------- | ------------------------------------------------------ |
| **Atomicity**   | All or nothing               | Transfer $100: debit AND credit both happen or neither |
| **Consistency** | Database remains valid       | Total money before = Total money after                 |
| **Isolation**   | Transactions don't interfere | Your transfer doesn't affect others                    |
| **Durability**  | Changes are permanent        | After commit, data survives system crash               |

**Transaction Methods:**

```java
Session session = factory.openSession();
Transaction tx = session.beginTransaction();

try {
    // Perform operations
    session.save(student);
    session.update(employee);

    // Commit transaction
    tx.commit();  // Make changes permanent

} catch (Exception e) {
    // Rollback on error
    tx.rollback();  // Undo all changes
    e.printStackTrace();
} finally {
    session.close();
}
```

**Transaction States:**

```
┌──────────────┐
│   CREATED    │  tx = session.beginTransaction()
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    ACTIVE    │  Performing database operations
└──────┬───────┘
       │
       ├─────────────┐
       ▼             ▼
┌──────────────┐  ┌──────────────┐
│  COMMITTED   │  │  ROLLED BACK │
│ (Success)    │  │   (Failed)   │
└──────────────┘  └──────────────┘
```

#### **5. Query (HQL)**

**What is it?**
Query allows you to execute **HQL (Hibernate Query Language)** - an object-oriented query language similar to SQL.

**Real-World Analogy:**
Think of HQL as **ordering food in your language** instead of kitchen language:

- SQL: "SELECT \* FROM student_table WHERE student_id = 1"
- HQL: "FROM Student WHERE id = 1" (more natural, object-oriented)

**HQL vs SQL:**

| Feature            | SQL                     | HQL                       |
| ------------------ | ----------------------- | ------------------------- |
| Works with         | Tables and columns      | Classes and properties    |
| Database dependent | Yes                     | No (database independent) |
| Syntax             | SELECT \* FROM students | FROM Student              |
| Case sensitive     | No                      | Yes (for class names)     |

**HQL Examples:**

```java
Session session = factory.openSession();

// 1. Get all students
Query<Student> query1 = session.createQuery("FROM Student", Student.class);
List<Student> students = query1.list();

// 2. Get students with condition
Query<Student> query2 = session.createQuery(
    "FROM Student WHERE email LIKE '%gmail.com'", Student.class);
List<Student> gmailStudents = query2.list();

// 3. Get specific columns
Query<Object[]> query3 = session.createQuery(
    "SELECT s.name, s.email FROM Student s", Object[].class);
List<Object[]> results = query3.list();

// 4. Parameterized query (safe from SQL injection)
Query<Student> query4 = session.createQuery(
    "FROM Student WHERE id = :studentId", Student.class);
query4.setParameter("studentId", 1);
Student student = query4.uniqueResult();

// 5. Update query
Query updateQuery = session.createQuery(
    "UPDATE Student SET email = :newEmail WHERE id = :id");
updateQuery.setParameter("newEmail", "new@email.com");
updateQuery.setParameter("id", 1);
int rowsAffected = updateQuery.executeUpdate();

session.close();
```

### 📋 Architecture Summary

**How Components Work Together:**

```
Application Code
      │
      ▼
1. Configuration.configure() → Reads hibernate.cfg.xml
      │
      ▼
2. Configuration.buildSessionFactory() → Creates SessionFactory (once)
      │
      ▼
3. SessionFactory.openSession() → Creates Session (per request)
      │
      ▼
4. Session.beginTransaction() → Starts Transaction
      │
      ▼
5. Session.save/update/delete() → Performs operations
      │
      ▼
6. Transaction.commit() → Saves changes to database
      │
      ▼
7. Session.close() → Releases resources
```

**Component Comparison:**

| Component      | Created       | Thread-Safe | Lifecycle            | Purpose             |
| -------------- | ------------- | ----------- | -------------------- | ------------------- |
| Configuration  | Once          | Yes         | Startup only         | Read settings       |
| SessionFactory | Once          | Yes         | Application lifetime | Create Sessions     |
| Session        | Per request   | No          | Request lifetime     | Database operations |
| Transaction    | Per operation | No          | Operation lifetime   | Ensure ACID         |
| Query          | Per query     | No          | Query lifetime       | Execute HQL         |

**Key Takeaways:**

- ✅ **Configuration** reads settings and builds SessionFactory
- ✅ **SessionFactory** is created once, thread-safe, and expensive
- ✅ **Session** is created per request, not thread-safe, and lightweight
- ✅ **Transaction** ensures ACID properties (all or nothing)
- ✅ **Query** executes HQL (object-oriented queries)
- ✅ Always follow: Open Session → Begin Transaction → Operations → Commit → Close Session
- ✅ Always use try-catch-finally to handle transactions properly
- ✅ Always close Session in finally block to prevent resource leaks

---

## Chapter 4: First Hibernate Application

### 🚀 Building Your First Hibernate Application

**What We'll Build:**
A complete **Student Management System** that performs CRUD operations (Create, Read, Update, Delete) on a Student entity.

**Analogy: Building a House** 🏠

Creating a Hibernate application is like building a house:

1. **Foundation** = Database and tables
2. **Blueprint** = Entity class (Student.java)
3. **Plumbing** = Configuration (hibernate.cfg.xml)
4. **Electricity** = Utility class (HibernateUtil.java)
5. **Furniture** = Main application (StudentApp.java)

### 📝 Step 1: Create Database and Table

**Open MySQL and create database:**

```sql
-- Create database
CREATE DATABASE IF NOT EXISTS hibernate_db;

-- Use database
USE hibernate_db;

-- Note: Table will be auto-created by Hibernate
-- But you can create it manually if needed:
CREATE TABLE IF NOT EXISTS student (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    age INT
);
```

### 📦 Step 2: Create Entity Class

**Create:** `src/main/java/com/example/entity/Student.java`

```java
package com.example.entity;

import jakarta.persistence.*;

@Entity  // Marks this class as a Hibernate entity
@Table(name = "student")  // Maps to 'student' table
public class Student {

    @Id  // Primary key
    @GeneratedValue(strategy = GenerationType.IDENTITY)  // Auto-increment
    @Column(name = "id")
    private int id;

    @Column(name = "name", nullable = false, length = 100)
    private String name;

    @Column(name = "email", nullable = false, unique = true, length = 100)
    private String email;

    @Column(name = "age")
    private int age;

    // Default constructor (required by Hibernate)
    public Student() {
    }

    // Parameterized constructor
    public Student(String name, String email, int age) {
        this.name = name;
        this.email = email;
        this.age = age;
    }

    // Getters and Setters
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    // toString() for easy printing
    @Override
    public String toString() {
        return "Student{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", email='" + email + '\'' +
                ", age=" + age +
                '}';
    }
}
```

**Annotations Explained:**

| Annotation      | Purpose               | Example                                |
| --------------- | --------------------- | -------------------------------------- |
| @Entity         | Marks class as entity | @Entity                                |
| @Table          | Specifies table name  | @Table(name = "student")               |
| @Id             | Marks primary key     | @Id                                    |
| @GeneratedValue | Auto-generate ID      | @GeneratedValue(strategy = IDENTITY)   |
| @Column         | Maps to column        | @Column(name = "email", unique = true) |

### ⚙️ Step 3: Update hibernate.cfg.xml

**Update:** `src/main/resources/hibernate.cfg.xml`

Add the entity mapping at the end (before closing session-factory tag):

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE hibernate-configuration PUBLIC
        "-//Hibernate/Hibernate Configuration DTD 3.0//EN"
        "http://www.hibernate.org/dtd/hibernate-configuration-3.0.dtd">

<hibernate-configuration>
    <session-factory>
        <!-- Database Connection Settings -->
        <property name="hibernate.connection.driver_class">
            com.mysql.cj.jdbc.Driver
        </property>
        <property name="hibernate.connection.url">
            jdbc:mysql://localhost:3306/hibernate_db?useSSL=false
        </property>
        <property name="hibernate.connection.username">root</property>
        <property name="hibernate.connection.password">your_password</property>

        <!-- SQL Dialect -->
        <property name="hibernate.dialect">
            org.hibernate.dialect.MySQLDialect
        </property>

        <!-- Echo SQL to console -->
        <property name="hibernate.show_sql">true</property>
        <property name="hibernate.format_sql">true</property>

        <!-- Auto create/update database schema -->
        <property name="hibernate.hbm2ddl.auto">update</property>

        <!-- Connection Pool Settings -->
        <property name="hibernate.connection.pool_size">10</property>

        <!-- Current Session Context -->
        <property name="hibernate.current_session_context_class">thread</property>

        <!-- Entity Mappings -->
        <mapping class="com.example.entity.Student"/>
    </session-factory>
</hibernate-configuration>
```

### 🔧 Step 4: Create HibernateUtil Class

**Create:** `src/main/java/com/example/util/HibernateUtil.java`

```java
package com.example.util;

import org.hibernate.SessionFactory;
import org.hibernate.cfg.Configuration;
import com.example.entity.Student;

public class HibernateUtil {

    private static SessionFactory sessionFactory;

    static {
        try {
            // Create SessionFactory from hibernate.cfg.xml
            sessionFactory = new Configuration()
                    .configure("hibernate.cfg.xml")
                    .addAnnotatedClass(Student.class)
                    .buildSessionFactory();

            System.out.println("✅ SessionFactory created successfully!");

        } catch (Exception e) {
            System.err.println("❌ Error creating SessionFactory!");
            e.printStackTrace();
        }
    }

    public static SessionFactory getSessionFactory() {
        return sessionFactory;
    }

    public static void shutdown() {
        if (sessionFactory != null) {
            sessionFactory.close();
            System.out.println("✅ SessionFactory closed!");
        }
    }
}
```

### 💻 Step 5: Create Main Application (CRUD Operations)

**Create:** `src/main/java/com/example/StudentApp.java`

```java
package com.example;

import org.hibernate.Session;
import org.hibernate.Transaction;
import org.hibernate.query.Query;
import com.example.entity.Student;
import com.example.util.HibernateUtil;

import java.util.List;

public class StudentApp {

    public static void main(String[] args) {

        // CREATE - Add new students
        System.out.println("\n========== CREATE OPERATION ==========");
        createStudent("John Doe", "john@email.com", 20);
        createStudent("Jane Smith", "jane@email.com", 22);
        createStudent("Bob Johnson", "bob@email.com", 21);

        // READ - Get all students
        System.out.println("\n========== READ ALL OPERATION ==========");
        getAllStudents();

        // READ - Get student by ID
        System.out.println("\n========== READ BY ID OPERATION ==========");
        getStudentById(1);

        // UPDATE - Update student
        System.out.println("\n========== UPDATE OPERATION ==========");
        updateStudent(1, "john.doe@gmail.com");

        // DELETE - Delete student
        System.out.println("\n========== DELETE OPERATION ==========");
        deleteStudent(3);

        // READ - Get all students after delete
        System.out.println("\n========== FINAL LIST ==========");
        getAllStudents();

        // Shutdown
        HibernateUtil.shutdown();
    }

    // CREATE - Insert new student
    public static void createStudent(String name, String email, int age) {
        Session session = HibernateUtil.getSessionFactory().openSession();
        Transaction tx = null;

        try {
            tx = session.beginTransaction();

            Student student = new Student(name, email, age);
            session.save(student);

            tx.commit();
            System.out.println("✅ Student created: " + student);

        } catch (Exception e) {
            if (tx != null) tx.rollback();
            System.err.println("❌ Error creating student: " + e.getMessage());
        } finally {
            session.close();
        }
    }

    // READ - Get all students
    public static void getAllStudents() {
        Session session = HibernateUtil.getSessionFactory().openSession();

        try {
            Query<Student> query = session.createQuery("FROM Student", Student.class);
            List<Student> students = query.list();

            System.out.println("📋 Total students: " + students.size());
            for (Student student : students) {
                System.out.println("   " + student);
            }

        } catch (Exception e) {
            System.err.println("❌ Error reading students: " + e.getMessage());
        } finally {
            session.close();
        }
    }

    // READ - Get student by ID
    public static void getStudentById(int id) {
        Session session = HibernateUtil.getSessionFactory().openSession();

        try {
            Student student = session.get(Student.class, id);

            if (student != null) {
                System.out.println("✅ Student found: " + student);
            } else {
                System.out.println("❌ Student not found with ID: " + id);
            }

        } catch (Exception e) {
            System.err.println("❌ Error reading student: " + e.getMessage());
        } finally {
            session.close();
        }
    }

    // UPDATE - Update student email
    public static void updateStudent(int id, String newEmail) {
        Session session = HibernateUtil.getSessionFactory().openSession();
        Transaction tx = null;

        try {
            tx = session.beginTransaction();

            Student student = session.get(Student.class, id);

            if (student != null) {
                String oldEmail = student.getEmail();
                student.setEmail(newEmail);
                session.update(student);

                tx.commit();
                System.out.println("✅ Student updated!");
                System.out.println("   Old email: " + oldEmail);
                System.out.println("   New email: " + newEmail);
            } else {
                System.out.println("❌ Student not found with ID: " + id);
            }

        } catch (Exception e) {
            if (tx != null) tx.rollback();
            System.err.println("❌ Error updating student: " + e.getMessage());
        } finally {
            session.close();
        }
    }

    // DELETE - Delete student
    public static void deleteStudent(int id) {
        Session session = HibernateUtil.getSessionFactory().openSession();
        Transaction tx = null;

        try {
            tx = session.beginTransaction();

            Student student = session.get(Student.class, id);

            if (student != null) {
                session.delete(student);
                tx.commit();
                System.out.println("✅ Student deleted: " + student);
            } else {
                System.out.println("❌ Student not found with ID: " + id);
            }

        } catch (Exception e) {
            if (tx != null) tx.rollback();
            System.err.println("❌ Error deleting student: " + e.getMessage());
        } finally {
            session.close();
        }
    }
}
```

### 📤 Step 6: Run the Application

**Right-click on StudentApp.java → Run As → Java Application**

**Expected Output:**

```
✅ SessionFactory created successfully!

========== CREATE OPERATION ==========
Hibernate: insert into student (age,email,name) values (?,?,?)
✅ Student created: Student{id=1, name='John Doe', email='john@email.com', age=20}
Hibernate: insert into student (age,email,name) values (?,?,?)
✅ Student created: Student{id=2, name='Jane Smith', email='jane@email.com', age=22}
Hibernate: insert into student (age,email,name) values (?,?,?)
✅ Student created: Student{id=3, name='Bob Johnson', email='bob@email.com', age=21}

========== READ ALL OPERATION ==========
Hibernate: select s1_0.id,s1_0.age,s1_0.email,s1_0.name from student s1_0
📋 Total students: 3
   Student{id=1, name='John Doe', email='john@email.com', age=20}
   Student{id=2, name='Jane Smith', email='jane@email.com', age=22}
   Student{id=3, name='Bob Johnson', email='bob@email.com', age=21}

========== READ BY ID OPERATION ==========
Hibernate: select s1_0.id,s1_0.age,s1_0.email,s1_0.name from student s1_0 where s1_0.id=?
✅ Student found: Student{id=1, name='John Doe', email='john@email.com', age=20}

========== UPDATE OPERATION ==========
Hibernate: select s1_0.id,s1_0.age,s1_0.email,s1_0.name from student s1_0 where s1_0.id=?
Hibernate: update student set age=?,email=?,name=? where id=?
✅ Student updated!
   Old email: john@email.com
   New email: john.doe@gmail.com

========== DELETE OPERATION ==========
Hibernate: select s1_0.id,s1_0.age,s1_0.email,s1_0.name from student s1_0 where s1_0.id=?
Hibernate: delete from student where id=?
✅ Student deleted: Student{id=3, name='Bob Johnson', email='bob@email.com', age=21}

========== FINAL LIST ==========
Hibernate: select s1_0.id,s1_0.age,s1_0.email,s1_0.name from student s1_0
📋 Total students: 2
   Student{id=1, name='John Doe', email='john.doe@gmail.com', age=20}
   Student{id=2, name='Jane Smith', email='jane@email.com', age=22}

✅ SessionFactory closed!
```

### 📊 Project Structure

```
hibernate-demo/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/
│   │   │       └── example/
│   │   │           ├── entity/
│   │   │           │   └── Student.java
│   │   │           ├── util/
│   │   │           │   └── HibernateUtil.java
│   │   │           └── StudentApp.java
│   │   └── resources/
│   │       └── hibernate.cfg.xml
│   └── test/
│       └── java/
├── pom.xml
└── README.md
```

### 🔍 Understanding the Flow

**Complete Application Flow:**

```
1. Application Starts
   ↓
2. HibernateUtil static block executes
   ↓
3. Configuration reads hibernate.cfg.xml
   ↓
4. SessionFactory is created (once)
   ↓
5. Main method starts
   ↓
6. For each operation:
   ├── Open Session
   ├── Begin Transaction
   ├── Perform Operation (save/update/delete/get)
   ├── Commit Transaction
   └── Close Session
   ↓
7. Shutdown SessionFactory
   ↓
8. Application Ends
```

### 📝 CRUD Operations Summary

| Operation  | Method           | SQL Generated | Transaction Required |
| ---------- | ---------------- | ------------- | -------------------- |
| **Create** | session.save()   | INSERT        | Yes                  |
| **Read**   | session.get()    | SELECT        | No                   |
| **Update** | session.update() | UPDATE        | Yes                  |
| **Delete** | session.delete() | DELETE        | Yes                  |

### ⚠️ Common Mistakes to Avoid

| Mistake                          | Problem            | Solution                      |
| -------------------------------- | ------------------ | ----------------------------- |
| Forgetting to close Session      | Resource leak      | Always use finally block      |
| Not handling transactions        | Data inconsistency | Always use try-catch-rollback |
| Creating multiple SessionFactory | Memory waste       | Use singleton pattern         |
| Forgetting @Entity annotation    | Table not created  | Add @Entity to class          |
| No default constructor           | Hibernate error    | Add no-arg constructor        |
| Wrong dialect                    | SQL errors         | Use correct dialect for DB    |

### 🎯 Best Practices

**1. Always use try-catch-finally:**

```java
Session session = factory.openSession();
Transaction tx = null;
try {
    tx = session.beginTransaction();
    // operations
    tx.commit();
} catch (Exception e) {
    if (tx != null) tx.rollback();
    e.printStackTrace();
} finally {
    session.close();
}
```

**2. Use parameterized queries:**

```java
// ❌ Bad (SQL injection risk)
Query query = session.createQuery("FROM Student WHERE name = '" + name + "'");

// ✅ Good (safe)
Query query = session.createQuery("FROM Student WHERE name = :name");
query.setParameter("name", name);
```

**3. Close SessionFactory on shutdown:**

```java
// Add shutdown hook
Runtime.getRuntime().addShutdownHook(new Thread(() -> {
    HibernateUtil.shutdown();
}));
```

**Key Takeaways:**

- ✅ Entity class must have @Entity annotation and default constructor
- ✅ Use @Id for primary key and @GeneratedValue for auto-increment
- ✅ Configure entity mapping in hibernate.cfg.xml
- ✅ HibernateUtil provides centralized SessionFactory management
- ✅ Always follow: Open Session → Begin Transaction → Operation → Commit → Close
- ✅ Use try-catch-finally for proper exception handling
- ✅ CREATE, UPDATE, DELETE require transactions; READ doesn't
- ✅ session.save() for INSERT, session.update() for UPDATE, session.delete() for DELETE
- ✅ session.get() for SELECT by ID, createQuery() for complex queries
- ✅ Always close Session to prevent resource leaks

---
