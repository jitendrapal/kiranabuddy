# 📚 CORE JAVA - Complete Guide for Students

## From Basics to Advanced with Theory & Practical Examples

---

## 📖 TABLE OF CONTENTS

### **PART 1: JAVA FUNDAMENTALS**

1. [Introduction to Java](#chapter-1-introduction-to-java)
2. [Setting Up Java Environment](#chapter-2-setting-up-java-environment)
3. [First Java Program](#chapter-3-first-java-program)
4. [Data Types and Variables](#chapter-4-data-types-and-variables)
5. [Operators](#chapter-5-operators)
6. [Control Flow Statements](#chapter-6-control-flow-statements)

### **PART 2: OBJECT-ORIENTED PROGRAMMING**

7. [Classes and Objects](#chapter-7-classes-and-objects)
8. [Constructors](#chapter-8-constructors)
9. [Inheritance](#chapter-9-inheritance)
10. [Polymorphism](#chapter-10-polymorphism)
11. [Abstraction](#chapter-11-abstraction)
12. [Encapsulation](#chapter-12-encapsulation)
13. [Interfaces](#chapter-13-interfaces)

### **PART 3: ADVANCED CONCEPTS**

14. [Exception Handling](#chapter-14-exception-handling)
15. [Collections Framework](#chapter-15-collections-framework)
16. [Multithreading](#chapter-16-multithreading)
17. [File I/O](#chapter-17-file-io)
18. [Java 8 Features](#chapter-18-java-8-features)

---

# PART 1: JAVA FUNDAMENTALS

---

## Chapter 1: Introduction to Java

### 📘 Theory

#### **1.1 What is Java?**

Java is a **high-level, class-based, object-oriented programming language** designed to have as few implementation dependencies as possible. It was developed by **James Gosling** and his team at **Sun Microsystems** (acquired by Oracle Corporation in 2010) in **1995**.

**Original Name:** Oak (named after an oak tree outside Gosling's office)
**Renamed to:** Java (inspired by Java coffee)
**First Public Release:** Java 1.0 (January 23, 1996)
**Current Version:** Java 21 LTS (Long-Term Support) as of 2024

#### **1.2 History and Evolution of Java**

**Timeline:**

- **1991** - James Gosling starts the "Green Project" for consumer electronics
- **1995** - Java 1.0 released with "Write Once, Run Anywhere" promise
- **1996** - JDK 1.0 released
- **1998** - Java 2 (J2SE 1.2) introduced Swing, Collections Framework
- **2004** - Java 5 (J2SE 5.0) added Generics, Annotations, Enums
- **2006** - Sun releases Java as open-source (GNU GPL)
- **2011** - Java 7 introduced try-with-resources, diamond operator
- **2014** - Java 8 (LTS) - Lambda expressions, Stream API, Date/Time API
- **2017** - Java 9 - Module system (Project Jigsaw)
- **2018** - Java 11 (LTS) - HTTP Client, var keyword
- **2021** - Java 17 (LTS) - Sealed classes, Pattern matching
- **2023** - Java 21 (LTS) - Virtual threads, Record patterns

#### **1.3 Philosophy: "Write Once, Run Anywhere" (WORA)**

Java's core philosophy is **platform independence**. This means:

- Write code on **Windows** → Run on **Linux, Mac, Solaris, etc.**
- No need to recompile for different platforms
- Achieved through **Java Virtual Machine (JVM)**

**Traditional Compiled Languages (C/C++):**

```
Source Code → Compiler → Platform-Specific Machine Code
(Must recompile for each OS)
```

**Java Approach:**

```
Source Code (.java) → Java Compiler (javac) → Bytecode (.class)
→ JVM (any platform) → Machine Code
```

#### **1.4 Key Features of Java (Detailed)**

**1. Simple and Easy to Learn**

- Syntax similar to C/C++ but simpler
- Removed complex features: pointers, operator overloading, multiple inheritance
- Automatic memory management (Garbage Collection)
- Rich standard library

**2. Object-Oriented**

- Everything is an object (except primitives)
- Supports 4 OOP pillars: Encapsulation, Inheritance, Polymorphism, Abstraction
- Promotes code reusability and modularity
- Class-based design

**3. Platform Independent**

- Bytecode runs on any platform with JVM
- "Write Once, Run Anywhere" (WORA)
- JVM acts as an abstraction layer between code and hardware
- No platform-specific features

**4. Secure**

- No explicit pointers (prevents direct memory access)
- Bytecode verification before execution
- Security Manager controls access to system resources
- Runs in a "sandbox" environment
- Cryptography support (java.security package)

**5. Robust (Strong and Reliable)**

- Strong type checking at compile-time and runtime
- Exception handling mechanism
- Automatic garbage collection (no memory leaks)
- Eliminates error-prone situations (pointer arithmetic)

**6. Multithreaded**

- Built-in support for concurrent programming
- Can execute multiple threads simultaneously
- Useful for GUI applications, servers, games
- Thread synchronization mechanisms

**7. Architecture Neutral**

- Bytecode is not specific to any processor architecture
- Fixed size for primitive types (int is always 32-bit)
- No "implementation-dependent" features

**8. Portable**

- Same bytecode runs on all platforms
- No platform-specific features
- Consistent behavior across systems

**9. High Performance**

- Just-In-Time (JIT) compiler improves performance
- Bytecode is close to native code
- Faster than interpreted languages
- Adaptive optimization

**10. Distributed**

- Supports networking (java.net package)
- RMI (Remote Method Invocation) for distributed applications
- Easy to create client-server applications

**11. Dynamic**

- Loads classes on demand (dynamic class loading)
- Supports dynamic memory allocation
- Adapts to evolving environments
- Reflection API for runtime introspection

#### **1.5 How Java Works: Compilation and Execution**

**Step-by-Step Process:**

**Step 1: Write Source Code (.java file)**

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

**Step 2: Compile with javac**

```bash
javac HelloWorld.java
```

- Checks for syntax errors
- Converts source code to bytecode
- Creates `HelloWorld.class` file

**Step 3: Bytecode (.class file)**

- Platform-independent intermediate code
- Not human-readable
- Verified for security

**Step 4: Execute with JVM**

```bash
java HelloWorld
```

- JVM loads the .class file
- Bytecode Verifier checks for illegal code
- JIT Compiler converts bytecode to machine code
- Executes on the specific platform

#### **1.6 JDK vs JRE vs JVM - Complete Explanation**

**1. JVM (Java Virtual Machine)**

- **Purpose:** Executes Java bytecode
- **Components:**
  - Class Loader - Loads .class files
  - Bytecode Verifier - Checks for illegal code
  - Execution Engine - Interprets/compiles bytecode
  - Garbage Collector - Manages memory
- **Platform-Specific:** Different JVM for Windows, Linux, Mac
- **You need:** JVM to **run** Java programs

**2. JRE (Java Runtime Environment)**

- **Purpose:** Provides runtime environment
- **Contains:** JVM + Core libraries + Supporting files
- **You need:** JRE to **run** Java applications (end-users)
- **Formula:** JRE = JVM + Libraries

**3. JDK (Java Development Kit)**

- **Purpose:** Complete development kit
- **Contains:** JRE + Development tools (javac, javadoc, jar, jdb)
- **You need:** JDK to **develop** Java applications (developers)
- **Formula:** JDK = JRE + Development Tools

### 💻 Practical Example

**Example 1.1: Understanding Java Compilation**

```java
// HelloWorld.java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, Java World!");
    }
}
```

**Compilation & Execution:**

```bash
# Compile
javac HelloWorld.java    # Creates HelloWorld.class

# Run
java HelloWorld          # Output: Hello, Java World!
```

**Example 1.2: Java vs Other Languages**

```java
// Java - Platform Independent
public class PlatformDemo {
    public static void main(String[] args) {
        System.out.println("OS: " + System.getProperty("os.name"));
        System.out.println("Java Version: " + System.getProperty("java.version"));
        System.out.println("This code runs on ANY operating system!");
    }
}
```

**Output (Windows):**

```
OS: Windows 10
Java Version: 17.0.1
This code runs on ANY operating system!
```

**Output (Linux/Mac):**

```
OS: Linux / Mac OS X
Java Version: 17.0.1
This code runs on ANY operating system!
```

### 🎯 Key Takeaways

- Java is platform-independent due to JVM
- Source code (.java) → Bytecode (.class) → Machine code
- JDK contains compiler, JRE contains runtime, JVM executes code

### 📝 Practice Questions

1. What is the difference between JDK, JRE, and JVM?
2. Why is Java called "platform-independent"?
3. What is bytecode?
4. Name 5 features of Java.

---

## Chapter 2: Setting Up Java Environment

### 📘 Theory

**Prerequisites:**

- Computer with Windows/Linux/Mac OS
- Internet connection to download JDK
- Text editor or IDE (VS Code, IntelliJ IDEA, Eclipse)

**Installation Steps:**

**1. Download JDK**

- Visit: https://www.oracle.com/java/technologies/downloads/
- Download latest JDK (Java 17 LTS or Java 21 LTS recommended)

**2. Install JDK**

- Windows: Run .exe installer
- Linux: `sudo apt install openjdk-17-jdk`
- Mac: Run .dmg installer or use Homebrew

**3. Set Environment Variables**

- **JAVA_HOME**: Points to JDK installation directory
- **PATH**: Add JDK bin directory

**4. Verify Installation**

```bash
java -version
javac -version
```

### 💻 Practical Example

**Example 2.1: Verify Java Installation**

```java
// VersionCheck.java
public class VersionCheck {
    public static void main(String[] args) {
        System.out.println("=== Java Environment Info ===");
        System.out.println("Java Version: " + System.getProperty("java.version"));
        System.out.println("Java Vendor: " + System.getProperty("java.vendor"));
        System.out.println("Java Home: " + System.getProperty("java.home"));
        System.out.println("OS Name: " + System.getProperty("os.name"));
        System.out.println("OS Version: " + System.getProperty("os.version"));
        System.out.println("User Name: " + System.getProperty("user.name"));
        System.out.println("User Home: " + System.getProperty("user.home"));
    }
}
```

**Output:**

```
=== Java Environment Info ===
Java Version: 17.0.1
Java Vendor: Oracle Corporation
Java Home: C:\Program Files\Java\jdk-17.0.1
OS Name: Windows 10
OS Version: 10.0
User Name: Student
User Home: C:\Users\Student
```

### 🎯 Key Takeaways

- JDK must be installed to compile and run Java programs
- JAVA_HOME and PATH must be set correctly
- Use `java -version` and `javac -version` to verify installation

---

## Chapter 3: First Java Program

### 📘 Theory

**Structure of a Java Program:**

```java
// 1. Package declaration (optional)
package com.example;

// 2. Import statements (optional)
import java.util.*;

// 3. Class declaration (mandatory)
public class ClassName {

    // 4. Main method (entry point)
    public static void main(String[] args) {
        // 5. Statements
        System.out.println("Hello World");
    }
}
```

**Key Components:**

1. **Class** - Container for code (must match filename)
2. **main() method** - Entry point of program
3. **public** - Access modifier (accessible everywhere)
4. **static** - Can be called without creating object
5. **void** - Returns nothing
6. **String[] args** - Command-line arguments

**Naming Conventions:**

- **Class names**: PascalCase (e.g., `StudentRecord`)
- **Method names**: camelCase (e.g., `calculateTotal`)
- **Variables**: camelCase (e.g., `studentName`)
- **Constants**: UPPER_CASE (e.g., `MAX_VALUE`)

### 💻 Practical Example

**Example 3.1: Basic Hello World**

```java
// HelloWorld.java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

**Example 3.2: Multiple Print Statements**

```java
// WelcomeMessage.java
public class WelcomeMessage {
    public static void main(String[] args) {
        System.out.println("================================");
        System.out.println("   Welcome to Java Programming  ");
        System.out.println("================================");
        System.out.println("Author: Student Name");
        System.out.println("Date: 2024-01-15");
        System.out.println();
        System.out.print("Java is ");  // print() - no newline
        System.out.print("awesome! "); // print() - no newline
        System.out.println();           // println() - newline
    }
}
```

**Output:**

```
================================
   Welcome to Java Programming
================================
Author: Student Name
Date: 2024-01-15

Java is awesome!
```

**Example 3.3: Command-Line Arguments**

```java
// CommandLineDemo.java
public class CommandLineDemo {
    public static void main(String[] args) {
        System.out.println("Number of arguments: " + args.length);

        if (args.length > 0) {
            System.out.println("Arguments received:");
            for (int i = 0; i < args.length; i++) {
                System.out.println("Argument " + i + ": " + args[i]);
            }
        } else {
            System.out.println("No arguments provided!");
        }
    }
}
```

**Run with arguments:**

```bash
java CommandLineDemo Hello World 123
```

**Output:**

```
Number of arguments: 3
Arguments received:
Argument 0: Hello
Argument 1: World
Argument 2: 123
```

**Example 3.4: Comments in Java**

```java
// CommentsDemo.java
public class CommentsDemo {
    public static void main(String[] args) {
        // This is a single-line comment
        System.out.println("Single-line comment above");

        /* This is a
           multi-line comment
           spanning multiple lines */
        System.out.println("Multi-line comment above");

        /**
         * This is a documentation comment (Javadoc)
         * Used to generate API documentation
         * @author Student Name
         * @version 1.0
         */
        System.out.println("Documentation comment above");
    }
}
```

### 🎯 Key Takeaways

- Every Java program must have at least one class
- `main()` method is the entry point
- Class name must match filename
- Use proper naming conventions

### 📝 Practice Questions

1. What is the purpose of the `main()` method?
2. Why is `main()` method `static`?
3. What is the difference between `print()` and `println()`?
4. Write a program that prints your name, age, and city.

---

## Chapter 4: Data Types and Variables

### 📘 Theory

**What is a Variable?**

A variable is a named memory location that stores data which can be changed during program execution. Think of a variable as a labeled container or box that holds a value.

**Detailed Explanation:**

In Java programming, a variable is a fundamental building block that allows you to store and manipulate data. Every variable has three essential characteristics:

1. **Name (Identifier)** - A unique name to identify the variable
2. **Type (Data Type)** - Specifies what kind of data the variable can hold
3. **Value** - The actual data stored in the variable

**Real-World Analogy:**

Think of a variable like a labeled storage box:

- **Box Label** = Variable Name (e.g., "age", "name", "price")
- **Box Type** = Data Type (e.g., number box, text box, true/false box)
- **Box Contents** = Value (e.g., 25, "John", true)

Just as you need to know what type of box you need before storing items (you wouldn't store liquids in a paper box), you need to declare the data type before storing values in a variable.

**Why Do We Need Variables?**

1. **Store Data** - Hold information for later use
2. **Reusability** - Use the same value multiple times without retyping
3. **Flexibility** - Change values during program execution
4. **Readability** - Make code more understandable (e.g., `price` instead of `99.99`)
5. **Memory Management** - Efficiently allocate and use memory

**How Variables Work in Memory:**

When you declare a variable, Java allocates a specific amount of memory based on the data type:

```
int age = 25;

Memory Representation:
┌──────────────┐
│ Variable: age│
│ Type: int    │
│ Value: 25    │
│ Memory: 4 bytes
└──────────────┘
```

**Variable Declaration and Initialization:**

**Declaration** - Creating a variable (allocating memory):

```java
int age;  // Variable declared but not initialized
```

**Initialization** - Assigning a value for the first time:

```java
age = 25;  // Variable initialized with value 25
```

**Declaration + Initialization** - Both in one step:

```java
int age = 25;  // Declare and initialize together (recommended)
```

**Example - Understanding Variables:**

```java
// Declare and initialize variables
int studentAge = 20;           // Integer variable
String studentName = "John";   // String variable
double marks = 85.5;           // Double variable
boolean isPassed = true;       // Boolean variable

// Using variables
System.out.println("Name: " + studentName);
System.out.println("Age: " + studentAge);
System.out.println("Marks: " + marks);
System.out.println("Passed: " + isPassed);

// Changing variable values
studentAge = 21;  // Age changed from 20 to 21
marks = 90.0;     // Marks changed from 85.5 to 90.0

System.out.println("Updated Age: " + studentAge);
System.out.println("Updated Marks: " + marks);
```

**Variable Naming Rules:**

1. **Must start with** - Letter (a-z, A-Z), underscore (\_), or dollar sign ($)
2. **Cannot start with** - Digit (0-9)
3. **Can contain** - Letters, digits, underscores, dollar signs
4. **Cannot use** - Java keywords (int, class, public, etc.)
5. **Case-sensitive** - `age` and `Age` are different variables

**Valid Variable Names:**

```java
int age;           // ✓ Valid
int _count;        // ✓ Valid
int $price;        // ✓ Valid
int studentAge;    // ✓ Valid (camelCase - recommended)
int student_age;   // ✓ Valid (snake_case)
```

**Invalid Variable Names:**

```java
int 2age;          // ✗ Invalid - starts with digit
int my-age;        // ✗ Invalid - contains hyphen
int class;         // ✗ Invalid - Java keyword
int my age;        // ✗ Invalid - contains space
```

**Variable Naming Conventions (Best Practices):**

1. **Use camelCase** - Start with lowercase, capitalize first letter of each subsequent word

   ```java
   int studentAge;
   String firstName;
   double accountBalance;
   ```

2. **Use meaningful names** - Names should describe the data

   ```java
   int age;           // ✓ Good - clear meaning
   int a;             // ✗ Bad - unclear meaning

   double salary;     // ✓ Good
   double x;          // ✗ Bad
   ```

3. **Avoid single-letter names** - Except for loop counters (i, j, k)

   ```java
   for (int i = 0; i < 10; i++) {  // ✓ Acceptable for loops
       // code
   }
   ```

4. **Constants in UPPERCASE** - Use all caps with underscores
   ```java
   final int MAX_AGE = 100;
   final double PI = 3.14159;
   ```

**Syntax:**

```java
dataType variableName = value;

// Examples:
int age = 25;
String name = "John";
double price = 99.99;
boolean isActive = true;
```

**Multiple Variable Declaration:**

```java
// Declare multiple variables of same type
int a, b, c;

// Declare and initialize multiple variables
int x = 10, y = 20, z = 30;

// Mixed declaration (some initialized, some not)
int p = 5, q, r = 10;
```

**Data Types in Java:**

**1. Primitive Data Types (8 types)**

| Type    | Size    | Range                 | Default  | Example             |
| ------- | ------- | --------------------- | -------- | ------------------- |
| byte    | 1 byte  | -128 to 127           | 0        | byte b = 100;       |
| short   | 2 bytes | -32,768 to 32,767     | 0        | short s = 1000;     |
| int     | 4 bytes | -2³¹ to 2³¹-1         | 0        | int i = 50000;      |
| long    | 8 bytes | -2⁶³ to 2⁶³-1         | 0L       | long l = 100000L;   |
| float   | 4 bytes | ~6-7 decimal digits   | 0.0f     | float f = 3.14f;    |
| double  | 8 bytes | ~15 decimal digits    | 0.0d     | double d = 3.14159; |
| char    | 2 bytes | 0 to 65,535 (Unicode) | '\u0000' | char c = 'A';       |
| boolean | 1 bit   | true or false         | false    | boolean b = true;   |

**2. Non-Primitive (Reference) Data Types**

- String, Arrays, Classes, Interfaces

**Variable Types:**

1. **Local Variables** - Declared inside methods
2. **Instance Variables** - Declared inside class, outside methods
3. **Static Variables** - Declared with `static` keyword

### 💻 Practical Example

**Example 4.1: Primitive Data Types**

```java
// DataTypesDemo.java
public class DataTypesDemo {
    public static void main(String[] args) {
        // Integer types
        byte age = 25;
        short year = 2024;
        int population = 1400000000;
        long distance = 9460730472580800L; // Light year in km

        // Floating-point types
        float pi = 3.14f;
        double gravity = 9.80665;

        // Character type
        char grade = 'A';

        // Boolean type
        boolean isPassed = true;

        // Print all values
        System.out.println("=== Primitive Data Types ===");
        System.out.println("Age (byte): " + age);
        System.out.println("Year (short): " + year);
        System.out.println("Population (int): " + population);
        System.out.println("Light Year (long): " + distance + " km");
        System.out.println("Pi (float): " + pi);
        System.out.println("Gravity (double): " + gravity + " m/s²");
        System.out.println("Grade (char): " + grade);
        System.out.println("Passed (boolean): " + isPassed);
    }
}
```

**Output:**

```
=== Primitive Data Types ===
Age (byte): 25
Year (short): 2024
Population (int): 1400000000
Light Year (long): 9460730472580800 km
Pi (float): 3.14
Gravity (double): 9.80665 m/s²
Grade (char): A
Passed (boolean): true
```

**Example 4.2: String and Type Conversion**

```java
// StringAndConversion.java
public class StringAndConversion {
    public static void main(String[] args) {
        // String (non-primitive)
        String name = "John Doe";
        String course = "Core Java";

        // Type conversion (Widening - automatic)
        int num1 = 100;
        long num2 = num1;  // int to long (automatic)
        float num3 = num2; // long to float (automatic)

        // Type casting (Narrowing - manual)
        double price = 99.99;
        int roundedPrice = (int) price;  // double to int (manual)

        // String to number conversion
        String strNum = "123";
        int convertedNum = Integer.parseInt(strNum);

        // Number to String conversion
        int marks = 95;
        String strMarks = String.valueOf(marks);

        // Print results
        System.out.println("=== String and Conversion ===");
        System.out.println("Name: " + name);
        System.out.println("Course: " + course);
        System.out.println("\nWidening Conversion:");
        System.out.println("int " + num1 + " → long " + num2 + " → float " + num3);
        System.out.println("\nNarrowing Conversion:");
        System.out.println("double " + price + " → int " + roundedPrice);
        System.out.println("\nString Conversion:");
        System.out.println("String \"" + strNum + "\" → int " + convertedNum);
        System.out.println("int " + marks + " → String \"" + strMarks + "\"");
    }
}
```

**Example 4.3: Variable Scope**

```java
// VariableScope.java
public class VariableScope {
    // Instance variable (belongs to object)
    int instanceVar = 100;

    // Static variable (belongs to class)
    static int staticVar = 200;

    public static void main(String[] args) {
        // Local variable (exists only in this method)
        int localVar = 300;

        System.out.println("=== Variable Scope ===");
        System.out.println("Local Variable: " + localVar);
        System.out.println("Static Variable: " + staticVar);

        // To access instance variable, create object
        VariableScope obj = new VariableScope();
        System.out.println("Instance Variable: " + obj.instanceVar);

        // Demonstrate scope
        if (true) {
            int blockVar = 400;  // Block scope
            System.out.println("Block Variable: " + blockVar);
        }
        // System.out.println(blockVar);  // ERROR: blockVar not accessible here
    }
}
```

### 🎯 Key Takeaways

- Java has 8 primitive data types
- Use appropriate data type to save memory
- Widening conversion is automatic, narrowing requires casting
- Variables have different scopes: local, instance, static

### 📝 Practice Questions

1. What is the difference between `int` and `long`?
2. Why do we use `f` suffix for float values?
3. What is type casting? Give an example.
4. Write a program to convert temperature from Celsius to Fahrenheit.

---

## Chapter 5: Operators

### 📘 Theory

**What are Operators?**

Operators are special symbols in Java that perform specific operations on one, two, or three operands, and then return a result. They are the building blocks for creating expressions and performing computations in your programs.

**Detailed Explanation:**

An operator is a symbol that tells the compiler to perform specific mathematical, logical, or relational operations. Operators work on operands (variables or values) to produce results.

**Real-World Analogy:**

Think of operators like tools in a toolbox:

- **Addition (+)** is like a calculator's plus button
- **Comparison (>)** is like a scale comparing weights
- **Logical AND (&&)** is like checking if both conditions are true (like "Is it raining AND cold?")

**Components of an Operation:**

```java
int result = 10 + 5;
//           ↑  ↑  ↑
//           │  │  └─ Operand 2 (value: 5)
//           │  └──── Operator (addition)
//           └─────── Operand 1 (value: 10)
```

**Why Do We Need Operators?**

1. **Perform Calculations** - Mathematical operations (add, subtract, multiply, divide)
2. **Make Comparisons** - Compare values (greater than, less than, equal to)
3. **Make Decisions** - Logical operations for conditional statements
4. **Assign Values** - Store results in variables
5. **Manipulate Data** - Increment, decrement, and modify values

**Types of Operators:**

Java provides a rich set of operators categorized into different types based on their functionality.

---

**1. Arithmetic Operators**

Arithmetic operators are used to perform basic mathematical operations like addition, subtraction, multiplication, division, and finding remainders.

| Operator | Name           | Description                   | Example  | Result |
| -------- | -------------- | ----------------------------- | -------- | ------ |
| `+`      | Addition       | Adds two operands             | `10 + 5` | `15`   |
| `-`      | Subtraction    | Subtracts second from first   | `10 - 5` | `5`    |
| `*`      | Multiplication | Multiplies two operands       | `10 * 5` | `50`   |
| `/`      | Division       | Divides first by second       | `10 / 5` | `2`    |
| `%`      | Modulus        | Returns remainder of division | `10 % 3` | `1`    |

**Example:**

```java
int a = 10, b = 3;
System.out.println("Addition: " + (a + b));        // 13
System.out.println("Subtraction: " + (a - b));     // 7
System.out.println("Multiplication: " + (a * b));  // 30
System.out.println("Division: " + (a / b));        // 3 (integer division)
System.out.println("Modulus: " + (a % b));         // 1 (remainder)
```

**Important Notes:**

- **Integer Division:** `10 / 3 = 3` (not 3.33, decimal part is truncated)
- **Modulus Use:** Finding even/odd numbers, remainders, cyclic patterns

---

**2. Assignment Operators**

Assignment operators are used to assign values to variables. They can also perform an operation and assign the result in one step.

| Operator | Name                | Description            | Example  | Equivalent To |
| -------- | ------------------- | ---------------------- | -------- | ------------- |
| `=`      | Simple assignment   | Assigns right to left  | `a = 10` | -             |
| `+=`     | Add and assign      | Adds and assigns       | `a += 5` | `a = a + 5`   |
| `-=`     | Subtract and assign | Subtracts and assigns  | `a -= 5` | `a = a - 5`   |
| `*=`     | Multiply and assign | Multiplies and assigns | `a *= 5` | `a = a * 5`   |
| `/=`     | Divide and assign   | Divides and assigns    | `a /= 5` | `a = a / 5`   |
| `%=`     | Modulus and assign  | Modulus and assigns    | `a %= 5` | `a = a % 5`   |

**Example:**

```java
int x = 10;
x += 5;  // x = x + 5 → x = 15
x -= 3;  // x = x - 3 → x = 12
x *= 2;  // x = x * 2 → x = 24
x /= 4;  // x = x / 4 → x = 6
x %= 4;  // x = x % 4 → x = 2
```

**Benefits:**

- **Shorter code** - Less typing
- **More readable** - Clear intent
- **Efficient** - Compiler optimization

---

**3. Comparison (Relational) Operators**

Comparison operators are used to compare two values. They return a boolean result (`true` or `false`).

| Operator | Name                  | Description            | Example  | Result  |
| -------- | --------------------- | ---------------------- | -------- | ------- |
| `==`     | Equal to              | Checks if equal        | `5 == 5` | `true`  |
| `!=`     | Not equal to          | Checks if not equal    | `5 != 3` | `true`  |
| `>`      | Greater than          | Checks if left > right | `5 > 3`  | `true`  |
| `<`      | Less than             | Checks if left < right | `5 < 3`  | `false` |
| `>=`     | Greater than or equal | Checks if left ≥ right | `5 >= 5` | `true`  |
| `<=`     | Less than or equal    | Checks if left ≤ right | `3 <= 5` | `true`  |

**Example:**

```java
int a = 10, b = 20;
System.out.println(a == b);  // false
System.out.println(a != b);  // true
System.out.println(a > b);   // false
System.out.println(a < b);   // true
System.out.println(a >= 10); // true
System.out.println(b <= 20); // true
```

**Common Use:** Used in conditional statements (if, while, for)

---

**4. Logical Operators**

Logical operators are used to combine multiple boolean expressions or to invert boolean values.

| Operator | Name        | Description                  | Example           | Result  |
| -------- | ----------- | ---------------------------- | ----------------- | ------- |
| `&&`     | Logical AND | True if both are true        | `true && false`   | `false` |
| `\|\|`   | Logical OR  | True if at least one is true | `true \|\| false` | `true`  |
| `!`      | Logical NOT | Inverts boolean value        | `!true`           | `false` |

**Truth Tables:**

**AND (&&):**
| A | B | A && B |
|---|---|--------|
| true | true | true |
| true | false | false |
| false | true | false |
| false | false | false |

**OR (||):**
| A | B | A \|\| B |
|---|---|--------|
| true | true | true |
| true | false | true |
| false | true | true |
| false | false | false |

**NOT (!):**
| A | !A |
|---|-----|
| true | false |
| false | true |

**Example:**

```java
int age = 25;
boolean hasLicense = true;

// AND - Both conditions must be true
if (age >= 18 && hasLicense) {
    System.out.println("Can drive");
}

// OR - At least one condition must be true
if (age < 18 || !hasLicense) {
    System.out.println("Cannot drive");
}

// NOT - Inverts the condition
if (!hasLicense) {
    System.out.println("No license");
}
```

**Short-Circuit Evaluation:**

- `&&` stops if first is false (no need to check second)
- `||` stops if first is true (no need to check second)

---

**5. Unary Operators**

Unary operators operate on a single operand to perform various operations like incrementing, decrementing, or negating values.

| Operator | Name        | Description              | Example        | Result      |
| -------- | ----------- | ------------------------ | -------------- | ----------- |
| `++`     | Increment   | Increases value by 1     | `x++` or `++x` | Increases x |
| `--`     | Decrement   | Decreases value by 1     | `x--` or `--x` | Decreases x |
| `+`      | Unary plus  | Indicates positive value | `+5`           | `5`         |
| `-`      | Unary minus | Negates the value        | `-5`           | `-5`        |
| `!`      | Logical NOT | Inverts boolean          | `!true`        | `false`     |

**Increment/Decrement - Pre vs Post:**

**Post-increment (x++):** Use current value, then increment

```java
int x = 5;
int y = x++;  // y = 5, then x becomes 6
// y = 5, x = 6
```

**Pre-increment (++x):** Increment first, then use new value

```java
int x = 5;
int y = ++x;  // x becomes 6, then y = 6
// y = 6, x = 6
```

**Example:**

```java
int a = 10;
System.out.println(a++);  // Prints 10, then a becomes 11
System.out.println(a);    // Prints 11

int b = 10;
System.out.println(++b);  // b becomes 11, then prints 11
System.out.println(b);    // Prints 11
```

**6. Ternary Operator**

- `condition ? value1 : value2`

### 💻 Practical Example

**Example 5.1: Arithmetic Operators**

```java
// ArithmeticOperators.java
public class ArithmeticOperators {
    public static void main(String[] args) {
        int a = 20;
        int b = 10;

        System.out.println("=== Arithmetic Operators ===");
        System.out.println("a = " + a + ", b = " + b);
        System.out.println("a + b = " + (a + b));  // 30
        System.out.println("a - b = " + (a - b));  // 10
        System.out.println("a * b = " + (a * b));  // 200
        System.out.println("a / b = " + (a / b));  // 2
        System.out.println("a % b = " + (a % b));  // 0

        // Division examples
        System.out.println("\n=== Division Examples ===");
        System.out.println("10 / 3 = " + (10 / 3));        // 3 (integer division)
        System.out.println("10.0 / 3 = " + (10.0 / 3));    // 3.333... (float division)
        System.out.println("10 % 3 = " + (10 % 3));        // 1 (remainder)
    }
}
```

**Example 5.2: Increment and Decrement**

```java
// IncrementDecrement.java
public class IncrementDecrement {
    public static void main(String[] args) {
        int x = 10;

        System.out.println("=== Increment/Decrement ===");
        System.out.println("Initial x = " + x);

        // Post-increment (use then increment)
        System.out.println("x++ = " + (x++));  // Prints 10, then x becomes 11
        System.out.println("After x++, x = " + x);  // 11

        // Pre-increment (increment then use)
        System.out.println("++x = " + (++x));  // x becomes 12, then prints 12
        System.out.println("After ++x, x = " + x);  // 12

        // Post-decrement
        System.out.println("x-- = " + (x--));  // Prints 12, then x becomes 11
        System.out.println("After x--, x = " + x);  // 11

        // Pre-decrement
        System.out.println("--x = " + (--x));  // x becomes 10, then prints 10
        System.out.println("After --x, x = " + x);  // 10
    }
}
```

**Example 5.3: Comparison and Logical Operators**

```java
// ComparisonLogical.java
public class ComparisonLogical {
    public static void main(String[] args) {
        int age = 20;
        int marks = 85;
        boolean hasLicense = true;

        System.out.println("=== Comparison Operators ===");
        System.out.println("age = " + age + ", marks = " + marks);
        System.out.println("age > 18: " + (age > 18));        // true
        System.out.println("age < 18: " + (age < 18));        // false
        System.out.println("marks >= 85: " + (marks >= 85));  // true
        System.out.println("marks == 85: " + (marks == 85));  // true
        System.out.println("marks != 85: " + (marks != 85));  // false

        System.out.println("\n=== Logical Operators ===");
        System.out.println("age > 18 AND marks > 80: " + (age > 18 && marks > 80));  // true
        System.out.println("age < 18 OR marks > 80: " + (age < 18 || marks > 80));   // true
        System.out.println("NOT hasLicense: " + (!hasLicense));  // false

        // Practical example
        boolean canDrive = (age >= 18) && hasLicense;
        System.out.println("\nCan drive? " + canDrive);  // true
    }
}
```

**Example 5.4: Ternary Operator**

```java
// TernaryOperator.java
public class TernaryOperator {
    public static void main(String[] args) {
        int marks = 75;

        // Syntax: condition ? value_if_true : value_if_false
        String result = (marks >= 60) ? "Pass" : "Fail";
        System.out.println("Result: " + result);  // Pass

        // Nested ternary
        String grade = (marks >= 90) ? "A" :
                       (marks >= 80) ? "B" :
                       (marks >= 70) ? "C" :
                       (marks >= 60) ? "D" : "F";
        System.out.println("Grade: " + grade);  // C

        // Find maximum
        int a = 50, b = 30;
        int max = (a > b) ? a : b;
        System.out.println("Maximum: " + max);  // 50
    }
}
```

### 🎯 Key Takeaways

- Operators perform operations on variables
- `++x` increments before use, `x++` increments after use
- Logical operators: `&&` (AND), `||` (OR), `!` (NOT)
- Ternary operator is shorthand for if-else

### 📝 Practice Questions

1. What is the difference between `++x` and `x++`?
2. What is the output of `10 % 3`?
3. Write a program to find the largest of three numbers using ternary operator.
4. What is the difference between `&` and `&&`?

---

## Chapter 6: Control Flow Statements

### 📘 Theory

#### **6.1 What are Control Flow Statements?**

Control flow statements determine the **order** in which statements are executed in a program. By default, statements execute sequentially (top to bottom), but control flow statements allow you to:

- Make decisions (if-else)
- Repeat code (loops)
- Jump to different parts of code (break, continue, return)

**Types of Control Flow Statements:**

1. **Decision-Making Statements** - if, if-else, if-else-if, switch
2. **Looping Statements** - for, while, do-while, enhanced for
3. **Branching Statements** - break, continue, return

#### **6.2 Decision-Making Statements**

**6.2.1 if Statement**

Executes a block of code **only if** the condition is true.

**Syntax:**

```java
if (condition) {
    // code to execute if condition is true
}
```

**Flowchart:**

```
    ┌─────────┐
    │  Start  │
    └────┬────┘
         │
    ┌────▼────┐
    │Condition│
    │  true?  │
    └─┬────┬──┘
      │Yes │No
      │    │
  ┌───▼──┐ │
  │Execute│ │
  │ Block │ │
  └───┬──┘ │
      │    │
    ┌─▼────▼─┐
    │  End   │
    └────────┘
```

**6.2.2 if-else Statement**

Executes one block if condition is true, another block if false.

**Syntax:**

```java
if (condition) {
    // code if true
} else {
    // code if false
}
```

**6.2.3 if-else-if Ladder**

Tests multiple conditions in sequence.

**Syntax:**

```java
if (condition1) {
    // code if condition1 is true
} else if (condition2) {
    // code if condition2 is true
} else if (condition3) {
    // code if condition3 is true
} else {
    // code if all conditions are false
}
```

**6.2.4 Nested if Statement**

An if statement inside another if statement.

**Syntax:**

```java
if (condition1) {
    if (condition2) {
        // code if both conditions are true
    }
}
```

**6.2.5 switch Statement**

Selects one of many code blocks to execute based on a variable's value.

**Syntax:**

```java
switch (expression) {
    case value1:
        // code
        break;
    case value2:
        // code
        break;
    default:
        // code if no case matches
}
```

**Key Points:**

- Expression can be: byte, short, int, char, String, enum
- `break` is optional (without it, execution "falls through")
- `default` is optional (executes if no case matches)
- Multiple cases can share the same code block

**switch vs if-else-if:**

- **switch:** Better for checking **equality** of a single variable
- **if-else-if:** Better for **range checks** or complex conditions

#### **6.3 Looping Statements**

Loops execute a block of code repeatedly until a condition becomes false.

**6.3.1 for Loop**

Used when you know **how many times** to repeat.

**Syntax:**

```java
for (initialization; condition; update) {
    // code to repeat
}
```

**Execution Flow:**

1. Initialization (executed once)
2. Check condition (if false, exit loop)
3. Execute loop body
4. Update
5. Go to step 2

**6.3.2 while Loop**

Used when you **don't know** how many times to repeat (condition-controlled).

**Syntax:**

```java
while (condition) {
    // code to repeat
}
```

**Key Point:** Condition is checked **before** executing the loop body (may not execute at all).

**6.3.3 do-while Loop**

Similar to while, but condition is checked **after** executing the loop body.

**Syntax:**

```java
do {
    // code to repeat
} while (condition);
```

**Key Point:** Loop body executes **at least once**, even if condition is false.

**6.3.4 Enhanced for Loop (for-each)**

Used to iterate over arrays or collections.

**Syntax:**

```java
for (dataType variable : array/collection) {
    // code
}
```

**Comparison:**

| Loop Type | When to Use            | Condition Check  |
| --------- | ---------------------- | ---------------- |
| for       | Known iterations       | Before execution |
| while     | Unknown iterations     | Before execution |
| do-while  | At least one execution | After execution  |
| for-each  | Iterate collections    | Automatic        |

#### **6.4 Branching Statements**

Branching statements alter the normal flow of control in loops and methods. They provide ways to exit loops early, skip iterations, or return from methods.

**6.4.1 break Statement**

The `break` statement is used to exit from a loop or switch statement immediately, regardless of the loop condition.

**Purpose:**

- Exit from a loop (for, while, do-while) completely
- Exit from a switch statement
- Terminates the nearest enclosing loop or switch

**How it works:**
When a `break` statement is encountered, the control immediately jumps to the statement following the loop or switch block.

**Syntax:**

```java
break;  // Simple break

break label;  // Labeled break (for nested loops)
```

**Example - break in loop:**

```java
for (int i = 1; i <= 10; i++) {
    if (i == 5) {
        break;  // Exit loop when i equals 5
    }
    System.out.println(i);
}
// Output: 1 2 3 4
```

**Use Cases:**

- Exit loop when a specific condition is met
- Stop searching when element is found
- Exit from infinite loops
- Terminate switch cases

**6.4.2 continue Statement**

The `continue` statement skips the current iteration of a loop and moves to the next iteration.

**Purpose:**

- Skip the current iteration and continue with the next
- Jumps to the loop's condition check (for while/do-while)
- Jumps to the update expression (for for-loop)

**How it works:**
When a `continue` statement is encountered, the remaining code in the current iteration is skipped, and the loop proceeds with the next iteration.

**Syntax:**

```java
continue;  // Simple continue

continue label;  // Labeled continue (for nested loops)
```

**Example - continue in loop:**

```java
for (int i = 1; i <= 5; i++) {
    if (i == 3) {
        continue;  // Skip when i equals 3
    }
    System.out.println(i);
}
// Output: 1 2 4 5 (3 is skipped)
```

**Use Cases:**

- Skip processing for specific values
- Skip invalid data in a loop
- Process only certain elements
- Avoid nested if-else blocks

**6.4.3 return Statement**

The `return` statement is used to exit from a method and optionally return a value to the caller.

**Purpose:**

- Exit from a method immediately
- Return control to the caller
- Return a value (for non-void methods)

**How it works:**
When a `return` statement is encountered, the method execution stops immediately, and control returns to the calling method.

**Syntax:**

```java
return;  // For void methods (no value)

return value;  // For methods with return type
```

**Example - return in method:**

```java
public int findMax(int a, int b) {
    if (a > b) {
        return a;  // Exit method and return a
    }
    return b;  // Exit method and return b
}
```

**Use Cases:**

- Return result from a method
- Exit method early based on condition
- Return from void methods
- Prevent further execution

**Comparison Table:**

| Feature              | break                      | continue                | return                     |
| -------------------- | -------------------------- | ----------------------- | -------------------------- |
| **Purpose**          | Exit loop/switch           | Skip current iteration  | Exit method                |
| **Scope**            | Loop or switch             | Loop only               | Method                     |
| **Effect**           | Terminates loop completely | Skips to next iteration | Exits method               |
| **Can return value** | No                         | No                      | Yes (for non-void methods) |
| **Use in switch**    | Yes                        | No                      | Yes                        |
| **Use in loops**     | Yes                        | Yes                     | Yes                        |

**Key Differences:**

- **break:** Exits loop/switch completely - no more iterations
- **continue:** Skips current iteration, continues loop - remaining iterations execute
- **return:** Exits the entire method - no more code in method executes

#### **6.5 Labeled Statements**

Java allows you to label loops and use labeled break/continue.

**Syntax:**

```java
outerLoop:
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        if (condition) {
            break outerLoop;  // Breaks outer loop
        }
    }
}
```

### 💻 Practical Example

**Example 6.1: if-else Statement**

```java
// GradeCalculator.java
public class GradeCalculator {
    public static void main(String[] args) {
        int marks = 75;

        System.out.println("=== Grade Calculator ===");
        System.out.println("Marks: " + marks);

        if (marks >= 90) {
            System.out.println("Grade: A+ (Excellent!)");
        } else if (marks >= 80) {
            System.out.println("Grade: A (Very Good)");
        } else if (marks >= 70) {
            System.out.println("Grade: B (Good)");
        } else if (marks >= 60) {
            System.out.println("Grade: C (Average)");
        } else if (marks >= 50) {
            System.out.println("Grade: D (Pass)");
        } else {
            System.out.println("Grade: F (Fail)");
        }
    }
}
```

**Example 6.2: switch Statement**

```java
// DayOfWeek.java
public class DayOfWeek {
    public static void main(String[] args) {
        int day = 3;
        String dayName;

        switch (day) {
            case 1:
                dayName = "Monday";
                break;
            case 2:
                dayName = "Tuesday";
                break;
            case 3:
                dayName = "Wednesday";
                break;
            case 4:
                dayName = "Thursday";
                break;
            case 5:
                dayName = "Friday";
                break;
            case 6:
                dayName = "Saturday";
                break;
            case 7:
                dayName = "Sunday";
                break;
            default:
                dayName = "Invalid day";
        }

        System.out.println("Day " + day + " is: " + dayName);
    }
}
```

**Example 6.3: for Loop**

```java
// MultiplicationTable.java
public class MultiplicationTable {
    public static void main(String[] args) {
        int number = 5;

        System.out.println("=== Multiplication Table of " + number + " ===");

        for (int i = 1; i <= 10; i++) {
            System.out.println(number + " × " + i + " = " + (number * i));
        }
    }
}
```

**Output:**

```
=== Multiplication Table of 5 ===
5 × 1 = 5
5 × 2 = 10
5 × 3 = 15
5 × 4 = 20
5 × 5 = 25
5 × 6 = 30
5 × 7 = 35
5 × 8 = 40
5 × 9 = 45
5 × 10 = 50
```

**Example 6.4: while Loop**

```java
// SumOfDigits.java
public class SumOfDigits {
    public static void main(String[] args) {
        int number = 12345;
        int sum = 0;
        int temp = number;

        System.out.println("Number: " + number);

        while (temp > 0) {
            int digit = temp % 10;  // Get last digit
            sum += digit;           // Add to sum
            temp /= 10;             // Remove last digit
        }

        System.out.println("Sum of digits: " + sum);  // 15
    }
}
```

**Example 6.5: do-while Loop**

```java
// MenuDriven.java
import java.util.Scanner;

public class MenuDriven {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int choice;

        do {
            System.out.println("\n=== MENU ===");
            System.out.println("1. Add");
            System.out.println("2. Subtract");
            System.out.println("3. Multiply");
            System.out.println("4. Divide");
            System.out.println("5. Exit");
            System.out.print("Enter choice: ");
            choice = sc.nextInt();

            if (choice >= 1 && choice <= 4) {
                System.out.print("Enter two numbers: ");
                int a = sc.nextInt();
                int b = sc.nextInt();

                switch (choice) {
                    case 1:
                        System.out.println("Result: " + (a + b));
                        break;
                    case 2:
                        System.out.println("Result: " + (a - b));
                        break;
                    case 3:
                        System.out.println("Result: " + (a * b));
                        break;
                    case 4:
                        if (b != 0) {
                            System.out.println("Result: " + (a / b));
                        } else {
                            System.out.println("Cannot divide by zero!");
                        }
                        break;
                }
            } else if (choice != 5) {
                System.out.println("Invalid choice!");
            }

        } while (choice != 5);

        System.out.println("Thank you!");
        sc.close();
    }
}
```

**Example 6.6: break and continue**

```java
// BreakContinueDemo.java
public class BreakContinueDemo {
    public static void main(String[] args) {
        System.out.println("=== break Example ===");
        for (int i = 1; i <= 10; i++) {
            if (i == 6) {
                break;  // Exit loop when i is 6
            }
            System.out.print(i + " ");
        }
        System.out.println("\n");

        System.out.println("=== continue Example ===");
        for (int i = 1; i <= 10; i++) {
            if (i % 2 == 0) {
                continue;  // Skip even numbers
            }
            System.out.print(i + " ");  // Only odd numbers printed
        }
    }
}
```

**Output:**

```
=== break Example ===
1 2 3 4 5

=== continue Example ===
1 3 5 7 9
```

**Example 6.7: Nested Loops - Pattern Printing**

```java
// PatternPrinting.java
public class PatternPrinting {
    public static void main(String[] args) {
        int rows = 5;

        System.out.println("=== Right Triangle ===");
        for (int i = 1; i <= rows; i++) {
            for (int j = 1; j <= i; j++) {
                System.out.print("* ");
            }
            System.out.println();
        }

        System.out.println("\n=== Number Pyramid ===");
        for (int i = 1; i <= rows; i++) {
            // Print spaces
            for (int j = 1; j <= rows - i; j++) {
                System.out.print(" ");
            }
            // Print numbers
            for (int j = 1; j <= i; j++) {
                System.out.print(j + " ");
            }
            System.out.println();
        }
    }
}
```

**Output:**

```
=== Right Triangle ===
*
* *
* * *
* * * *
* * * * *

=== Number Pyramid ===
    1
   1 2
  1 2 3
 1 2 3 4
1 2 3 4 5
```

### 🎯 Key Takeaways

- Use `if-else` for decision making
- Use `switch` for multiple equality checks
- Use `for` when iterations are known
- Use `while` when iterations are unknown
- Use `do-while` for at least one execution
- `break` exits loop, `continue` skips iteration

### 📝 Practice Questions

1. What is the difference between `while` and `do-while`?
2. When should you use `switch` instead of `if-else-if`?
3. Write a program to print all prime numbers between 1 and 100.
4. Write a program to find factorial of a number using loops.
5. What happens if you forget `break` in a switch case?

---

# PART 2: OBJECT-ORIENTED PROGRAMMING

---

## Chapter 7: Arrays

### 📘 Theory

#### **7.1 What is an Array?**

An **array** is a container object that holds a **fixed number of values** of a **single type**. Arrays are used to store multiple values in a single variable, instead of declaring separate variables for each value.

**Key Characteristics:**

- **Fixed Size** - Size is determined at creation time and cannot be changed
- **Homogeneous** - All elements must be of the same data type
- **Indexed** - Elements are accessed using index (starting from 0)
- **Contiguous Memory** - Elements are stored in consecutive memory locations
- **Reference Type** - Arrays are objects in Java

**Why Use Arrays?**

- Store multiple values of the same type
- Easy to access elements using index
- Efficient memory management
- Pass multiple values to methods
- Implement data structures (stacks, queues, etc.)

#### **7.2 Types of Arrays**

**1. Single-Dimensional Array (1D Array)**

- Linear collection of elements
- Accessed using single index
- Example: `int[] numbers = {10, 20, 30, 40, 50};`

**2. Multi-Dimensional Array (2D, 3D, etc.)**

- Array of arrays
- Accessed using multiple indices
- Example: `int[][] matrix = {{1, 2}, {3, 4}};`

#### **7.3 Declaring and Creating Arrays**

**Syntax:**

```java
// Declaration
dataType[] arrayName;              // Preferred
dataType arrayName[];              // Also valid (C-style)

// Creation
arrayName = new dataType[size];

// Declaration + Creation
dataType[] arrayName = new dataType[size];

// Declaration + Initialization
dataType[] arrayName = {value1, value2, value3, ...};
```

**Memory Representation:**

```
int[] numbers = new int[5];

Stack Memory          Heap Memory
┌──────────┐         ┌───┬───┬───┬───┬───┐
│ numbers  │────────>│ 0 │ 0 │ 0 │ 0 │ 0 │
└──────────┘         └───┴───┴───┴───┴───┘
(reference)          Index: 0   1   2   3   4
```

#### **7.4 Accessing Array Elements**

**Syntax:**

```java
arrayName[index]  // Access element at index
```

**Important Points:**

- **Index starts from 0** (first element is at index 0)
- **Last index is (length - 1)**
- **ArrayIndexOutOfBoundsException** - Thrown if index is invalid

**Example:**

```java
int[] numbers = {10, 20, 30, 40, 50};
System.out.println(numbers[0]);  // 10 (first element)
System.out.println(numbers[4]);  // 50 (last element)
System.out.println(numbers[5]);  // Error! ArrayIndexOutOfBoundsException
```

#### **7.5 Array Length**

Every array in Java has a built-in **length** property that returns the number of elements in the array. This is a final instance variable, not a method.

**Syntax:**

```java
arrayName.length  // Returns size of array (not a method, it's a property - no parentheses)
```

**Important Points:**

1. **Property, not a method** - Use `array.length` NOT `array.length()`
2. **Final value** - Cannot be changed after array creation
3. **Zero-based indexing** - Valid indices are 0 to (length - 1)
4. **Works with all arrays** - 1D, 2D, or multi-dimensional arrays

**Example:**

```java
int[] numbers = {10, 20, 30, 40, 50};
System.out.println(numbers.length);  // 5

// Last element index
int lastIndex = numbers.length - 1;  // 4
System.out.println(numbers[lastIndex]);  // 50
```

**Common Use Cases:**

**1. Loop through array:**

```java
for (int i = 0; i < numbers.length; i++) {
    System.out.println(numbers[i]);
}
```

**2. Check if array is empty:**

```java
if (numbers.length == 0) {
    System.out.println("Array is empty");
}
```

**3. Find last element:**

```java
int lastElement = numbers[numbers.length - 1];
```

**4. Multi-dimensional arrays:**

```java
int[][] matrix = new int[3][4];
System.out.println(matrix.length);       // 3 (number of rows)
System.out.println(matrix[0].length);    // 4 (number of columns in first row)
```

**Common Mistake:**

```java
// WRONG - length is not a method
int size = numbers.length();  // Compilation error

// CORRECT
int size = numbers.length;  // No parentheses
```

#### **7.6 Iterating Through Arrays**

**Method 1: Traditional for Loop**

```java
for (int i = 0; i < array.length; i++) {
    System.out.println(array[i]);
}
```

**Method 2: Enhanced for Loop (for-each)**

```java
for (dataType element : array) {
    System.out.println(element);
}
```

**Method 3: while Loop**

```java
int i = 0;
while (i < array.length) {
    System.out.println(array[i]);
    i++;
}
```

#### **7.7 Multi-Dimensional Arrays**

**2D Array (Matrix):**

```java
// Declaration and creation
int[][] matrix = new int[rows][columns];

// Initialization
int[][] matrix = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};

// Accessing elements
matrix[row][column]
```

**Memory Representation:**

```
int[][] matrix = {{1, 2}, {3, 4}, {5, 6}};

        ┌───────┐
matrix ─┤ ref   │
        └───┬───┘
            │
            ▼
        ┌───┬───┬───┐
        │ 0 │ 1 │ 2 │  (Array of references)
        └─┬─┴─┬─┴─┬─┘
          │   │   │
    ┌─────┘   │   └─────┐
    ▼         ▼         ▼
  ┌───┬───┐ ┌───┬───┐ ┌───┬───┐
  │ 1 │ 2 │ │ 3 │ 4 │ │ 5 │ 6 │
  └───┴───┘ └───┴───┘ └───┴───┘
```

**Jagged Array (Irregular Array):**

```java
// Array where each row can have different number of columns
int[][] jagged = new int[3][];
jagged[0] = new int[2];  // First row has 2 columns
jagged[1] = new int[4];  // Second row has 4 columns
jagged[2] = new int[3];  // Third row has 3 columns
```

#### **7.8 Array Operations**

**Common Operations:**

1. **Traversal** - Visit each element
2. **Insertion** - Add element (limited, as size is fixed)
3. **Deletion** - Remove element (shift elements)
4. **Searching** - Find element (linear/binary search)
5. **Sorting** - Arrange in order (bubble, selection, etc.)
6. **Copying** - Create duplicate array
7. **Merging** - Combine two arrays

#### **7.9 Arrays Class (java.util.Arrays)**

Java provides a utility class with useful methods:

```java
import java.util.Arrays;

// Sorting
Arrays.sort(array);

// Binary Search (array must be sorted)
int index = Arrays.binarySearch(array, key);

// Copying
int[] copy = Arrays.copyOf(array, newLength);

// Filling
Arrays.fill(array, value);

// Comparing
boolean equal = Arrays.equals(array1, array2);

// Converting to String
String str = Arrays.toString(array);
```

#### **7.10 Advantages and Disadvantages**

**Advantages:**

- ✅ Fast access using index (O(1) time complexity)
- ✅ Easy to implement and use
- ✅ Memory efficient (contiguous allocation)
- ✅ Cache-friendly (better performance)

**Disadvantages:**

- ❌ Fixed size (cannot grow or shrink)
- ❌ Insertion/deletion is expensive (shifting required)
- ❌ Homogeneous (only one data type)
- ❌ Wasted memory if not fully utilized

### 💻 Practical Examples

**Example 7.1: Basic Array Operations**

```java
// ArrayBasics.java
public class ArrayBasics {
    public static void main(String[] args) {
        // Declaration and initialization
        int[] numbers = {10, 20, 30, 40, 50};

        System.out.println("=== Array Elements ===");
        System.out.println("First element: " + numbers[0]);
        System.out.println("Last element: " + numbers[numbers.length - 1]);
        System.out.println("Array length: " + numbers.length);

        // Modifying elements
        numbers[2] = 100;
        System.out.println("\nAfter modification:");
        System.out.println("Element at index 2: " + numbers[2]);

        // Traversing array
        System.out.println("\n=== All Elements ===");
        for (int i = 0; i < numbers.length; i++) {
            System.out.println("numbers[" + i + "] = " + numbers[i]);
        }
    }
}
```

**Output:**

```
=== Array Elements ===
First element: 10
Last element: 50
Array length: 5

After modification:
Element at index 2: 100

=== All Elements ===
numbers[0] = 10
numbers[1] = 20
numbers[2] = 100
numbers[3] = 40
numbers[4] = 50
```

**Example 7.2: Array Input and Sum**

```java
// ArraySum.java
import java.util.Scanner;

public class ArraySum {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter array size: ");
        int size = sc.nextInt();

        int[] numbers = new int[size];

        // Input
        System.out.println("Enter " + size + " numbers:");
        for (int i = 0; i < size; i++) {
            numbers[i] = sc.nextInt();
        }

        // Calculate sum and average
        int sum = 0;
        for (int num : numbers) {
            sum += num;
        }
        double average = (double) sum / size;

        // Output
        System.out.println("\n=== Results ===");
        System.out.println("Sum: " + sum);
        System.out.println("Average: " + average);

        sc.close();
    }
}
```

**Example 7.3: Finding Maximum and Minimum**

```java
// ArrayMinMax.java
public class ArrayMinMax {
    public static void main(String[] args) {
        int[] numbers = {45, 12, 78, 23, 89, 34, 67};

        int max = numbers[0];
        int min = numbers[0];

        for (int i = 1; i < numbers.length; i++) {
            if (numbers[i] > max) {
                max = numbers[i];
            }
            if (numbers[i] < min) {
                min = numbers[i];
            }
        }

        System.out.println("Array: ");
        for (int num : numbers) {
            System.out.print(num + " ");
        }
        System.out.println("\n\nMaximum: " + max);
        System.out.println("Minimum: " + min);
    }
}
```

**Output:**

```
Array:
45 12 78 23 89 34 67

Maximum: 89
Minimum: 12
```

**Example 7.4: Searching in Array (Linear Search)**

```java
// LinearSearch.java
import java.util.Scanner;

public class LinearSearch {
    public static void main(String[] args) {
        int[] numbers = {10, 25, 30, 45, 50, 65, 70};
        Scanner sc = new Scanner(System.in);

        System.out.print("Enter number to search: ");
        int key = sc.nextInt();

        int index = -1;
        for (int i = 0; i < numbers.length; i++) {
            if (numbers[i] == key) {
                index = i;
                break;
            }
        }

        if (index != -1) {
            System.out.println(key + " found at index " + index);
        } else {
            System.out.println(key + " not found in array");
        }

        sc.close();
    }
}
```

**Example 7.5: Reversing an Array**

```java
// ReverseArray.java
public class ReverseArray {
    public static void main(String[] args) {
        int[] numbers = {10, 20, 30, 40, 50};

        System.out.println("Original Array:");
        printArray(numbers);

        // Reverse using two pointers
        int left = 0;
        int right = numbers.length - 1;

        while (left < right) {
            // Swap elements
            int temp = numbers[left];
            numbers[left] = numbers[right];
            numbers[right] = temp;

            left++;
            right--;
        }

        System.out.println("\nReversed Array:");
        printArray(numbers);
    }

    static void printArray(int[] arr) {
        for (int num : arr) {
            System.out.print(num + " ");
        }
        System.out.println();
    }
}
```

**Output:**

```
Original Array:
10 20 30 40 50

Reversed Array:
50 40 30 20 10
```

### 🎯 Key Takeaways

- Arrays store multiple values of the same type
- Index starts from 0, last index is (length - 1)
- Arrays have fixed size (cannot be changed after creation)
- Use `array.length` to get size (not `array.length()`)
- Enhanced for loop is best for simple traversal
- Traditional for loop is best when you need index

### 📝 Practice Questions

1. What is the difference between `int[] arr` and `int arr[]`?
2. What happens if you access `arr[arr.length]`?
3. Write a program to find the second largest element in an array.
4. Write a program to check if an array is sorted.
5. How do you copy an array in Java?

---

## Chapter 8: Methods (Functions)

### 📘 Theory

#### **8.1 What is a Method?**

A **method** is a block of code that performs a specific task. Methods are also called **functions** in other programming languages. They help in:

- **Code Reusability** - Write once, use multiple times
- **Modularity** - Break complex problems into smaller parts
- **Maintainability** - Easy to update and debug
- **Abstraction** - Hide implementation details

**Real-World Analogy:**
Think of a method like a **vending machine**:

- **Input** - You insert money (parameters)
- **Process** - Machine processes your selection (method body)
- **Output** - You get a product (return value)

#### **8.2 Method Syntax**

```java
accessModifier returnType methodName(parameterList) {
    // Method body
    // Statements
    return value;  // If returnType is not void
}
```

**Components:**

1. **Access Modifier** - public, private, protected, default
2. **Return Type** - Data type of value returned (void if nothing)
3. **Method Name** - Identifier (follows camelCase convention)
4. **Parameter List** - Input values (optional)
5. **Method Body** - Code to execute
6. **return Statement** - Returns value to caller (optional for void)

**Example:**

```java
public int add(int a, int b) {
    int sum = a + b;
    return sum;
}
```

#### **8.3 Types of Methods**

**1. Based on Return Type:**

**a) Methods with Return Value**

```java
public int square(int num) {
    return num * num;
}
```

**b) Methods without Return Value (void)**

```java
public void greet() {
    System.out.println("Hello!");
}
```

**2. Based on Parameters:**

**a) Methods with Parameters**

```java
public void printSum(int a, int b) {
    System.out.println("Sum: " + (a + b));
}
```

**b) Methods without Parameters**

```java
public void displayMenu() {
    System.out.println("1. Add");
    System.out.println("2. Subtract");
}
```

**3. Based on Definition:**

**a) Predefined Methods** - Built-in Java methods

```java
Math.sqrt(25);           // Returns 5.0
String.valueOf(100);     // Returns "100"
System.out.println();    // Prints to console
```

**b) User-Defined Methods** - Created by programmer

```java
public int factorial(int n) {
    // Your implementation
}
```

#### **8.4 Method Calling**

**Syntax:**

```java
methodName(arguments);              // For void methods
returnType variable = methodName(arguments);  // For methods with return
```

**Example:**

```java
public class Calculator {
    // Method definition
    public int add(int a, int b) {
        return a + b;
    }

    public static void main(String[] args) {
        Calculator calc = new Calculator();

        // Method calling
        int result = calc.add(10, 20);
        System.out.println("Result: " + result);  // 30
    }
}
```

#### **8.5 Method Parameters**

**1. Formal Parameters** - Variables in method definition
**2. Actual Parameters (Arguments)** - Values passed during method call

```java
public void display(int x, int y) {  // x, y are formal parameters
    System.out.println(x + ", " + y);
}

display(10, 20);  // 10, 20 are actual parameters (arguments)
```

**Parameter Passing in Java:**

- **Pass by Value** - Java always passes arguments by value
- For primitives: Copy of value is passed
- For objects: Copy of reference is passed (not the object itself)

```java
public void modify(int num) {
    num = 100;  // Changes local copy, not original
}

int x = 50;
modify(x);
System.out.println(x);  // Still 50 (unchanged)
```

#### **8.6 Method Overloading (Compile-Time Polymorphism)**

**Definition:** Multiple methods with the **same name** but **different parameters**.

**Rules:**

1. Method name must be same
2. Parameters must differ in:
   - Number of parameters, OR
   - Type of parameters, OR
   - Order of parameters
3. Return type alone is NOT sufficient

**Example:**

```java
public class Calculator {
    // Overloaded methods
    public int add(int a, int b) {
        return a + b;
    }

    public int add(int a, int b, int c) {
        return a + b + c;
    }

    public double add(double a, double b) {
        return a + b;
    }
}
```

**Why Use Overloading?**

- Same operation on different types
- Improves code readability
- Flexibility in method calling

#### **8.7 Recursion**

**Definition:** A method that calls itself is called a **recursive method**.

**Components:**

1. **Base Case** - Stopping condition (prevents infinite recursion)
2. **Recursive Case** - Method calls itself with modified parameters

**Example: Factorial**

```java
public int factorial(int n) {
    // Base case
    if (n == 0 || n == 1) {
        return 1;
    }
    // Recursive case
    return n * factorial(n - 1);
}
```

**How it works:**

```
factorial(5)
= 5 * factorial(4)
= 5 * (4 * factorial(3))
= 5 * (4 * (3 * factorial(2)))
= 5 * (4 * (3 * (2 * factorial(1))))
= 5 * (4 * (3 * (2 * 1)))
= 5 * (4 * (3 * 2))
= 5 * (4 * 6)
= 5 * 24
= 120
```

**Recursion vs Iteration:**

| Aspect   | Recursion                          | Iteration               |
| -------- | ---------------------------------- | ----------------------- |
| Approach | Function calls itself              | Loop repeats code       |
| Memory   | Uses call stack (more memory)      | Uses less memory        |
| Speed    | Slower (function call overhead)    | Faster                  |
| Code     | More elegant, concise              | More verbose            |
| Use Case | Tree traversal, divide-and-conquer | Simple repetitive tasks |

#### **8.8 Variable Arguments (Varargs)**

**Definition:** Method that accepts variable number of arguments.

**Syntax:**

```java
public returnType methodName(dataType... variableName) {
    // variableName is treated as an array
}
```

**Example:**

```java
public int sum(int... numbers) {
    int total = 0;
    for (int num : numbers) {
        total += num;
    }
    return total;
}

// Calling
sum(10, 20);           // 30
sum(10, 20, 30);       // 60
sum(10, 20, 30, 40);   // 100
```

**Rules:**

- Only one varargs parameter per method
- Varargs must be the last parameter

#### **8.9 Method Scope and Lifetime**

**Local Variables:**

- Declared inside method
- Scope: Within the method only
- Lifetime: Until method execution completes

**Example:**

```java
public void display() {
    int x = 10;  // Local variable
    System.out.println(x);
}  // x is destroyed here
```

#### **8.10 Static Methods**

**Definition:** Methods that belong to the class, not to objects.

**Characteristics:**

- Called using class name (no object needed)
- Can access only static members
- Cannot use `this` or `super` keywords

**Example:**

```java
public class MathUtils {
    public static int square(int n) {
        return n * n;
    }
}

// Calling
int result = MathUtils.square(5);  // No object needed
```

### 💻 Practical Examples

**Example 8.1: Basic Method with Return Value**

```java
// MethodDemo.java
public class MethodDemo {
    // Method to check if number is even
    public boolean isEven(int num) {
        return num % 2 == 0;
    }

    // Method to find maximum of two numbers
    public int max(int a, int b) {
        return (a > b) ? a : b;
    }

    public static void main(String[] args) {
        MethodDemo obj = new MethodDemo();

        // Calling methods
        System.out.println("Is 10 even? " + obj.isEven(10));  // true
        System.out.println("Is 15 even? " + obj.isEven(15));  // false

        System.out.println("Max of 25 and 40: " + obj.max(25, 40));  // 40
    }
}
```

**Output:**

```
Is 10 even? true
Is 15 even? false
Max of 25 and 40: 40
```

**Example 8.2: Method Overloading**

```java
// AreaCalculator.java
public class AreaCalculator {
    // Area of square
    public double area(double side) {
        return side * side;
    }

    // Area of rectangle
    public double area(double length, double width) {
        return length * width;
    }

    // Area of circle
    public double area(double radius, boolean isCircle) {
        if (isCircle) {
            return 3.14159 * radius * radius;
        }
        return 0;
    }

    public static void main(String[] args) {
        AreaCalculator calc = new AreaCalculator();

        System.out.println("Area of square (side=5): " + calc.area(5));
        System.out.println("Area of rectangle (4x6): " + calc.area(4, 6));
        System.out.println("Area of circle (radius=7): " + calc.area(7, true));
    }
}
```

**Output:**

```
Area of square (side=5): 25.0
Area of rectangle (4x6): 24.0
Area of circle (radius=7): 153.93791
```

**Example 8.3: Recursion - Fibonacci Series**

```java
// FibonacciRecursion.java
public class FibonacciRecursion {
    // Recursive method to find nth Fibonacci number
    public int fibonacci(int n) {
        // Base cases
        if (n == 0) return 0;
        if (n == 1) return 1;

        // Recursive case
        return fibonacci(n - 1) + fibonacci(n - 2);
    }

    public static void main(String[] args) {
        FibonacciRecursion fib = new FibonacciRecursion();

        System.out.println("First 10 Fibonacci numbers:");
        for (int i = 0; i < 10; i++) {
            System.out.print(fib.fibonacci(i) + " ");
        }
    }
}
```

**Output:**

```
First 10 Fibonacci numbers:
0 1 1 2 3 5 8 13 21 34
```

**Example 8.4: Varargs (Variable Arguments)**

```java
// VarargsDemo.java
public class VarargsDemo {
    // Method with varargs
    public int sum(int... numbers) {
        int total = 0;
        System.out.print("Numbers: ");
        for (int num : numbers) {
            System.out.print(num + " ");
            total += num;
        }
        System.out.println();
        return total;
    }

    public static void main(String[] args) {
        VarargsDemo obj = new VarargsDemo();

        System.out.println("Sum: " + obj.sum(10, 20) + "\n");
        System.out.println("Sum: " + obj.sum(10, 20, 30) + "\n");
        System.out.println("Sum: " + obj.sum(10, 20, 30, 40, 50) + "\n");
    }
}
```

**Output:**

```
Numbers: 10 20
Sum: 30

Numbers: 10 20 30
Sum: 60

Numbers: 10 20 30 40 50
Sum: 150
```

**Example 8.5: Static Methods**

```java
// MathOperations.java
public class MathOperations {
    // Static method to calculate power
    public static double power(double base, int exponent) {
        double result = 1;
        for (int i = 0; i < exponent; i++) {
            result *= base;
        }
        return result;
    }

    // Static method to check prime
    public static boolean isPrime(int num) {
        if (num <= 1) return false;
        for (int i = 2; i <= Math.sqrt(num); i++) {
            if (num % i == 0) return false;
        }
        return true;
    }

    public static void main(String[] args) {
        // Calling static methods without creating object
        System.out.println("2^10 = " + MathOperations.power(2, 10));
        System.out.println("Is 17 prime? " + MathOperations.isPrime(17));
        System.out.println("Is 20 prime? " + MathOperations.isPrime(20));
    }
}
```

**Output:**

```
2^10 = 1024.0
Is 17 prime? true
Is 20 prime? false
```

### 🎯 Key Takeaways

- Methods promote code reusability and modularity
- Method signature = method name + parameter list
- Java uses pass-by-value for all parameters
- Method overloading allows same name with different parameters
- Recursion is powerful but uses more memory than iteration
- Static methods belong to class, not objects
- Varargs allow flexible number of arguments

### 📝 Practice Questions

1. What is the difference between parameters and arguments?
2. Can we overload methods by changing only the return type?
3. Write a recursive method to calculate sum of digits of a number.
4. What is the difference between static and non-static methods?
5. Write a method to check if a string is palindrome.

---

## Chapter 9: Classes and Objects

### 📘 Theory

#### **9.1 What is Object-Oriented Programming (OOP)?**

**Object-Oriented Programming** is a programming paradigm based on the concept of "objects" that contain data (attributes) and code (methods). OOP focuses on organizing software design around data, or objects, rather than functions and logic.

**Why OOP?**

- **Real-World Modeling** - Represents real-world entities
- **Code Reusability** - Through inheritance
- **Modularity** - Code is organized in classes
- **Data Security** - Through encapsulation
- **Easy Maintenance** - Changes in one class don't affect others

**Four Pillars of OOP:**

1. **Encapsulation** - Bundling data and methods together
2. **Inheritance** - Acquiring properties from parent class
3. **Polymorphism** - One interface, multiple implementations
4. **Abstraction** - Hiding implementation details

#### **9.2 What is a Class?**

A **class** is a blueprint or template for creating objects. It defines the structure and behavior that the objects will have.

**Real-World Analogy:**

- **Class** = Blueprint of a house
- **Object** = Actual house built from the blueprint

**Syntax:**

```java
class ClassName {
    // Data members (fields/attributes/properties)
    dataType variable1;
    dataType variable2;

    // Member functions (methods/behaviors)
    returnType method1() {
        // code
    }

    returnType method2() {
        // code
    }
}
```

**Example:**

```java
class Car {
    // Attributes (Data members)
    String brand;
    String model;
    int year;

    // Methods (Behaviors)
    void start() {
        System.out.println("Car is starting...");
    }

    void stop() {
        System.out.println("Car is stopping...");
    }
}
```

#### **9.3 What is an Object?**

An **object** is an instance of a class. It is a real-world entity that has:

- **State** - Represented by attributes (data members)
- **Behavior** - Represented by methods (member functions)
- **Identity** - Unique name to identify the object

**Creating an Object:**

```java
ClassName objectName = new ClassName();
```

**Example:**

```java
Car myCar = new Car();  // Creating object of Car class
```

**Memory Representation:**

```
Stack Memory          Heap Memory
┌──────────┐         ┌─────────────────┐
│  myCar   │────────>│ brand: null     │
└──────────┘         │ model: null     │
(reference)          │ year: 0         │
                     │ start()         │
                     │ stop()          │
                     └─────────────────┘
```

#### **9.4 Components of a Class**

**1. Data Members (Fields/Attributes)**

- Variables that hold the state of an object
- Also called instance variables or properties

**2. Methods (Member Functions)**

- Functions that define the behavior of an object
- Operate on the data members

**3. Constructors**

- Special methods to initialize objects
- Same name as class, no return type

**4. Blocks**

- Instance initialization blocks
- Static initialization blocks

**5. Nested Classes**

- Classes defined within another class

#### **9.5 Accessing Class Members**

**Syntax:**

```java
objectName.dataMember;    // Access data member
objectName.method();      // Call method
```

**Example:**

```java
Car myCar = new Car();
myCar.brand = "Toyota";   // Set attribute
myCar.start();            // Call method
```

#### **9.6 Types of Variables in a Class**

**1. Instance Variables (Non-Static)**

- Belong to objects (each object has its own copy)
- Created when object is created
- Destroyed when object is destroyed
- Accessed using object reference

```java
class Student {
    String name;  // Instance variable
    int age;      // Instance variable
}
```

**2. Static Variables (Class Variables)**

- Belong to class (shared by all objects)
- Created when class is loaded
- Only one copy exists
- Accessed using class name

```java
class Student {
    static String schoolName;  // Static variable (shared)
    String name;               // Instance variable (unique)
}
```

**3. Local Variables**

- Declared inside methods
- Scope limited to the method
- Must be initialized before use

```java
void display() {
    int x = 10;  // Local variable
    System.out.println(x);
}
```

**Comparison:**

| Feature       | Instance Variable    | Static Variable    | Local Variable       |
| ------------- | -------------------- | ------------------ | -------------------- |
| Belongs to    | Object               | Class              | Method               |
| Memory        | Heap                 | Method Area        | Stack                |
| Default Value | Yes (0, null, false) | Yes                | No (must initialize) |
| Access        | object.variable      | ClassName.variable | Direct               |
| Lifetime      | Object lifetime      | Program lifetime   | Method execution     |

#### **9.7 The `this` Keyword**

**Definition:** `this` is a reference variable that refers to the current object - the object whose method or constructor is being called.

**What is `this`?**

The `this` keyword is an implicit reference to the current object. It holds the memory address of the current object and can be used to access instance variables and methods of the current class.

**Real-World Analogy:**
Think of `this` like saying "myself" or "my own":

- "I will do **my** work" - `this.work()`
- "This is **my** name" - `this.name`
- "I am referring to **myself**" - `this`

**Uses of `this` Keyword:**

**1. Differentiate between instance variables and local variables/parameters**

When parameter names are same as instance variable names, `this` is used to distinguish between them.

```java
class Student {
    String name;  // Instance variable
    int age;      // Instance variable

    Student(String name, int age) {  // Parameters have same names
        this.name = name;  // this.name = instance variable, name = parameter
        this.age = age;    // this.age = instance variable, age = parameter
    }

    void setName(String name) {
        this.name = name;  // Resolve naming conflict
    }
}
```

**Without `this`:**

```java
Student(String name, int age) {
    name = name;  // Assigns parameter to itself - WRONG!
    age = age;    // Instance variables remain uninitialized
}
```

**2. Call current class method**

You can use `this` to call another method of the current class (though it's optional).

```java
class Calculator {
    void add(int a, int b) {
        System.out.println(a + b);
    }

    void calculate() {
        this.add(5, 10);  // Calling add() method using this
        add(5, 10);       // Same as above (this is implicit)
    }
}
```

**3. Call current class constructor (Constructor Chaining)**

`this()` is used to call another constructor of the same class. This is called constructor chaining.

```java
class Student {
    String name;
    int age;
    String course;

    // Constructor 1
    Student() {
        this("Unknown", 0, "Not Assigned");  // Calls Constructor 3
    }

    // Constructor 2
    Student(String name, int age) {
        this(name, age, "Not Assigned");  // Calls Constructor 3
    }

    // Constructor 3
    Student(String name, int age, String course) {
        this.name = name;
        this.age = age;
        this.course = course;
    }
}
```

**Important Rules for `this()` in constructor:**

- Must be the **first statement** in constructor
- Cannot use two `this()` calls in same constructor
- Prevents code duplication

**4. Pass current object as parameter to a method**

You can pass the current object to another method using `this`.

```java
class Student {
    String name;

    void display() {
        System.out.println("Name: " + name);
    }

    void passObject() {
        processStudent(this);  // Passing current object
    }

    void processStudent(Student s) {
        s.display();
    }
}
```

**Real-world use case:**

```java
class Button {
    void onClick() {
        EventHandler handler = new EventHandler();
        handler.handleClick(this);  // Pass button object to handler
    }
}
```

**5. Return current object from a method**

Useful for method chaining (calling multiple methods in sequence).

```java
class Student {
    String name;
    int age;

    Student setName(String name) {
        this.name = name;
        return this;  // Return current object
    }

    Student setAge(int age) {
        this.age = age;
        return this;  // Return current object
    }

    void display() {
        System.out.println("Name: " + name + ", Age: " + age);
    }
}

// Usage - Method Chaining
Student s = new Student();
s.setName("John").setAge(25).display();  // Chaining methods
```

**Summary of `this` Keyword:**

| Use Case                 | Syntax              | Purpose                   |
| ------------------------ | ------------------- | ------------------------- |
| Access instance variable | `this.variableName` | Resolve naming conflicts  |
| Call instance method     | `this.methodName()` | Call current class method |
| Call constructor         | `this()`            | Constructor chaining      |
| Pass current object      | `method(this)`      | Pass object as parameter  |
| Return current object    | `return this;`      | Method chaining           |

**Important Points:**

- `this` is a reference to the current object
- Cannot be used in static context (static methods/blocks)
- `this()` must be first statement in constructor
- Helps in method chaining (builder pattern)
- Makes code more readable and explicit

#### **9.8 Object Creation Process**

**What happens when you create an object?**

```java
Car myCar = new Car();
```

**Step-by-Step:**

1. **Class Loading** - Car class is loaded into memory (if not already)
2. **Memory Allocation** - Memory is allocated in heap for the object
3. **Initialization** - Instance variables are initialized with default values
4. **Constructor Execution** - Constructor is called to initialize object
5. **Reference Assignment** - Reference is assigned to the variable `myCar`

#### **9.9 Anonymous Objects**

**Definition:** Objects without a reference variable.

**Syntax:**

```java
new ClassName().method();
```

**Example:**

```java
new Car().start();  // Anonymous object
```

**Use Case:**

- When object is needed only once
- Saves memory (garbage collected immediately after use)

#### **9.10 Multiple Objects**

You can create multiple objects of the same class:

```java
Car car1 = new Car();
Car car2 = new Car();
Car car3 = new Car();
```

Each object has its own copy of instance variables but shares static variables.

### 💻 Practical Examples

**Example 9.1: Basic Class and Object**

```java
// Student.java
class Student {
    // Instance variables
    String name;
    int rollNo;
    int marks;

    // Method to display student details
    void display() {
        System.out.println("Name: " + name);
        System.out.println("Roll No: " + rollNo);
        System.out.println("Marks: " + marks);
        System.out.println("-------------------");
    }
}

public class StudentDemo {
    public static void main(String[] args) {
        // Creating objects
        Student s1 = new Student();
        Student s2 = new Student();

        // Setting values for s1
        s1.name = "Alice";
        s1.rollNo = 101;
        s1.marks = 85;

        // Setting values for s2
        s2.name = "Bob";
        s2.rollNo = 102;
        s2.marks = 92;

        // Displaying details
        System.out.println("=== Student Details ===");
        s1.display();
        s2.display();
    }
}
```

**Output:**

```
=== Student Details ===
Name: Alice
Roll No: 101
Marks: 85
-------------------
Name: Bob
Roll No: 102
Marks: 92
-------------------
```

**Example 9.2: Instance vs Static Variables**

```java
// Counter.java
class Counter {
    int instanceCount = 0;      // Instance variable (each object has own copy)
    static int staticCount = 0; // Static variable (shared by all objects)

    Counter() {
        instanceCount++;
        staticCount++;
    }

    void display() {
        System.out.println("Instance Count: " + instanceCount);
        System.out.println("Static Count: " + staticCount);
        System.out.println("-------------------");
    }
}

public class CounterDemo {
    public static void main(String[] args) {
        Counter c1 = new Counter();
        Counter c2 = new Counter();
        Counter c3 = new Counter();

        System.out.println("=== Counter Demo ===");
        System.out.println("\nObject 1:");
        c1.display();

        System.out.println("Object 2:");
        c2.display();

        System.out.println("Object 3:");
        c3.display();
    }
}
```

**Output:**

```
=== Counter Demo ===

Object 1:
Instance Count: 1
Static Count: 3
-------------------
Object 2:
Instance Count: 1
Static Count: 3
-------------------
Object 3:
Instance Count: 1
Static Count: 3
-------------------
```

**Example 9.3: Using `this` Keyword**

```java
// Rectangle.java
class Rectangle {
    int length;
    int width;

    // Using this to differentiate between instance and local variables
    void setDimensions(int length, int width) {
        this.length = length;  // this.length = instance variable
        this.width = width;    // length = parameter
    }

    int getArea() {
        return this.length * this.width;
    }

    int getPerimeter() {
        return 2 * (this.length + this.width);
    }

    void display() {
        System.out.println("Length: " + this.length);
        System.out.println("Width: " + this.width);
        System.out.println("Area: " + this.getArea());
        System.out.println("Perimeter: " + this.getPerimeter());
    }
}

public class RectangleDemo {
    public static void main(String[] args) {
        Rectangle rect = new Rectangle();
        rect.setDimensions(10, 5);

        System.out.println("=== Rectangle Details ===");
        rect.display();
    }
}
```

**Output:**

```
=== Rectangle Details ===
Length: 10
Width: 5
Area: 50
Perimeter: 30
```

**Example 9.4: Bank Account System**

```java
// BankAccount.java
class BankAccount {
    // Instance variables
    String accountNumber;
    String accountHolder;
    double balance;

    // Static variable (shared by all accounts)
    static String bankName = "ABC Bank";
    static int totalAccounts = 0;

    // Method to create account
    void createAccount(String accNo, String holder, double initialBalance) {
        this.accountNumber = accNo;
        this.accountHolder = holder;
        this.balance = initialBalance;
        totalAccounts++;
        System.out.println("Account created successfully!");
    }

    // Method to deposit money
    void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            System.out.println("Deposited: ₹" + amount);
            System.out.println("New Balance: ₹" + balance);
        } else {
            System.out.println("Invalid amount!");
        }
    }

    // Method to withdraw money
    void withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            System.out.println("Withdrawn: ₹" + amount);
            System.out.println("New Balance: ₹" + balance);
        } else {
            System.out.println("Insufficient balance or invalid amount!");
        }
    }

    // Method to display account details
    void displayDetails() {
        System.out.println("\n=== Account Details ===");
        System.out.println("Bank: " + bankName);
        System.out.println("Account Number: " + accountNumber);
        System.out.println("Account Holder: " + accountHolder);
        System.out.println("Balance: ₹" + balance);
        System.out.println("Total Accounts: " + totalAccounts);
    }
}

public class BankDemo {
    public static void main(String[] args) {
        // Creating first account
        BankAccount acc1 = new BankAccount();
        acc1.createAccount("ACC001", "John Doe", 5000);
        acc1.deposit(2000);
        acc1.withdraw(1500);
        acc1.displayDetails();

        // Creating second account
        BankAccount acc2 = new BankAccount();
        acc2.createAccount("ACC002", "Jane Smith", 10000);
        acc2.deposit(3000);
        acc2.displayDetails();
    }
}
```

**Output:**

```
Account created successfully!
Deposited: ₹2000.0
New Balance: ₹7000.0
Withdrawn: ₹1500.0
New Balance: ₹5500.0

=== Account Details ===
Bank: ABC Bank
Account Number: ACC001
Account Holder: John Doe
Balance: ₹5500.0
Total Accounts: 2
Account created successfully!
Deposited: ₹3000.0
New Balance: ₹13000.0

=== Account Details ===
Bank: ABC Bank
Account Number: ACC002
Account Holder: Jane Smith
Balance: ₹13000.0
Total Accounts: 2
```

### 🎯 Key Takeaways

- Class is a blueprint, object is an instance of a class
- Instance variables belong to objects, static variables belong to class
- `this` keyword refers to the current object
- Each object has its own copy of instance variables
- Static variables are shared by all objects
- Objects are created in heap memory
- Use dot (.) operator to access class members

### 📝 Practice Questions

1. What is the difference between a class and an object?
2. What is the difference between instance and static variables?
3. When should you use the `this` keyword?
4. Write a class `Book` with attributes title, author, price and methods to display details.
5. What happens when you create an object using `new` keyword?

---

## Chapter 10: Constructors

### 📘 Theory

#### **10.1 What is a Constructor?**

A **constructor** is a special method that is automatically called when an object is created. It is used to initialize the object's state (assign values to instance variables).

**Key Characteristics:**

- **Same name as class** - Constructor name must match class name exactly
- **No return type** - Not even void
- **Called automatically** - Invoked when object is created using `new`
- **Cannot be static, final, or abstract**
- **Can be overloaded** - Multiple constructors with different parameters

**Purpose:**

- Initialize instance variables
- Allocate resources
- Perform setup operations
- Ensure object is in valid state

**Real-World Analogy:**
Think of a constructor like **setting up a new phone**:

- When you buy a phone (create object), it automatically runs setup (constructor)
- You configure settings (initialize variables)
- Phone is ready to use (object is initialized)

#### **10.2 Types of Constructors**

**1. Default Constructor (No-Argument Constructor)**

A constructor with **no parameters**.

**Syntax:**

```java
class ClassName {
    ClassName() {
        // Initialization code
    }
}
```

**Example:**

```java
class Student {
    String name;
    int age;

    // Default constructor
    Student() {
        name = "Unknown";
        age = 0;
        System.out.println("Default constructor called");
    }
}
```

**2. Parameterized Constructor**

A constructor with **parameters** to initialize object with specific values.

**Syntax:**

```java
class ClassName {
    ClassName(parameters) {
        // Initialization code
    }
}
```

**Example:**

```java
class Student {
    String name;
    int age;

    // Parameterized constructor
    Student(String n, int a) {
        name = n;
        age = a;
        System.out.println("Parameterized constructor called");
    }
}
```

**3. Copy Constructor**

A constructor that creates a new object by copying values from another object.

**Example:**

```java
class Student {
    String name;
    int age;

    // Copy constructor
    Student(Student s) {
        this.name = s.name;
        this.age = s.age;
        System.out.println("Copy constructor called");
    }
}
```

#### **10.3 Default Constructor Provided by Java**

If you **don't define any constructor**, Java automatically provides a **default constructor** that:

- Has no parameters
- Has empty body
- Initializes instance variables with default values (0, null, false)

**Example:**

```java
class Student {
    String name;
    int age;
    // Java automatically provides:
    // Student() { }
}

Student s = new Student();  // Calls Java's default constructor
```

**Important:** If you define **any constructor** (even parameterized), Java will **NOT** provide the default constructor.

#### **10.4 Constructor Overloading**

Having **multiple constructors** with different parameter lists in the same class.

**Example:**

```java
class Student {
    String name;
    int age;

    // Constructor 1 - No parameters
    Student() {
        name = "Unknown";
        age = 0;
    }

    // Constructor 2 - One parameter
    Student(String n) {
        name = n;
        age = 0;
    }

    // Constructor 3 - Two parameters
    Student(String n, int a) {
        name = n;
        age = a;
    }
}
```

**Benefits:**

- Flexibility in object creation
- Different ways to initialize objects
- Improves code readability

#### **10.5 Constructor Chaining**

Calling one constructor from another constructor using `this()`.

**Rules:**

- `this()` must be the **first statement** in constructor
- Cannot call two constructors simultaneously
- Prevents code duplication

**Example:**

```java
class Student {
    String name;
    int age;
    String course;

    // Constructor 1
    Student() {
        this("Unknown", 0, "Not Assigned");  // Calls Constructor 3
    }

    // Constructor 2
    Student(String n, int a) {
        this(n, a, "Not Assigned");  // Calls Constructor 3
    }

    // Constructor 3
    Student(String n, int a, String c) {
        name = n;
        age = a;
        course = c;
    }
}
```

#### **10.6 Constructor vs Method**

| Feature     | Constructor                                 | Method                          |
| ----------- | ------------------------------------------- | ------------------------------- |
| Name        | Same as class name                          | Any valid identifier            |
| Return Type | No return type                              | Must have return type (or void) |
| Invocation  | Called automatically when object is created | Called explicitly using object  |
| Purpose     | Initialize object                           | Perform operations              |
| Inheritance | Not inherited                               | Inherited by subclass           |
| `this()`    | Can call another constructor                | Cannot call constructor         |

#### **10.7 Private Constructor**

A constructor with **private** access modifier.

**Uses:**

- **Singleton Pattern** - Ensure only one instance of class
- **Utility Classes** - Prevent instantiation (e.g., Math class)
- **Factory Methods** - Control object creation

**Example (Singleton):**

```java
class Singleton {
    private static Singleton instance;

    // Private constructor
    private Singleton() {
        System.out.println("Singleton instance created");
    }

    // Public method to get instance
    public static Singleton getInstance() {
        if (instance == null) {
            instance = new Singleton();
        }
        return instance;
    }
}
```

### 💻 Practical Examples

**Example 10.1: Default Constructor**

```java
// DefaultConstructorDemo.java
class Book {
    String title;
    String author;
    double price;

    // Default constructor
    Book() {
        title = "Unknown";
        author = "Unknown";
        price = 0.0;
        System.out.println("Default constructor called");
    }

    void display() {
        System.out.println("Title: " + title);
        System.out.println("Author: " + author);
        System.out.println("Price: ₹" + price);
        System.out.println("-------------------");
    }
}

public class DefaultConstructorDemo {
    public static void main(String[] args) {
        System.out.println("Creating book with default constructor:");
        Book b1 = new Book();
        b1.display();
    }
}
```

**Output:**

```
Creating book with default constructor:
Default constructor called
Title: Unknown
Author: Unknown
Price: ₹0.0
-------------------
```

**Example 10.2: Parameterized Constructor**

```java
// ParameterizedConstructorDemo.java
class Employee {
    int id;
    String name;
    double salary;

    // Parameterized constructor
    Employee(int empId, String empName, double empSalary) {
        id = empId;
        name = empName;
        salary = empSalary;
        System.out.println("Employee object created");
    }

    void display() {
        System.out.println("ID: " + id);
        System.out.println("Name: " + name);
        System.out.println("Salary: ₹" + salary);
        System.out.println("-------------------");
    }
}

public class ParameterizedConstructorDemo {
    public static void main(String[] args) {
        System.out.println("=== Employee Details ===\n");

        Employee e1 = new Employee(101, "John Doe", 50000);
        e1.display();

        Employee e2 = new Employee(102, "Jane Smith", 60000);
        e2.display();
    }
}
```

**Output:**

```
=== Employee Details ===

Employee object created
ID: 101
Name: John Doe
Salary: ₹50000.0
-------------------
Employee object created
ID: 102
Name: Jane Smith
Salary: ₹60000.0
-------------------
```

**Example 10.3: Constructor Overloading**

```java
// ConstructorOverloadingDemo.java
class Rectangle {
    int length;
    int width;

    // Constructor 1 - No parameters (Square with side 1)
    Rectangle() {
        length = 1;
        width = 1;
        System.out.println("Default constructor: Square with side 1");
    }

    // Constructor 2 - One parameter (Square)
    Rectangle(int side) {
        length = side;
        width = side;
        System.out.println("Constructor with 1 parameter: Square with side " + side);
    }

    // Constructor 3 - Two parameters (Rectangle)
    Rectangle(int l, int w) {
        length = l;
        width = w;
        System.out.println("Constructor with 2 parameters: Rectangle " + l + "x" + w);
    }

    void display() {
        System.out.println("Length: " + length + ", Width: " + width);
        System.out.println("Area: " + (length * width));
        System.out.println("-------------------\n");
    }
}

public class ConstructorOverloadingDemo {
    public static void main(String[] args) {
        System.out.println("=== Constructor Overloading Demo ===\n");

        Rectangle r1 = new Rectangle();
        r1.display();

        Rectangle r2 = new Rectangle(5);
        r2.display();

        Rectangle r3 = new Rectangle(10, 6);
        r3.display();
    }
}
```

**Output:**

```
=== Constructor Overloading Demo ===

Default constructor: Square with side 1
Length: 1, Width: 1
Area: 1
-------------------

Constructor with 1 parameter: Square with side 5
Length: 5, Width: 5
Area: 25
-------------------

Constructor with 2 parameters: Rectangle 10x6
Length: 10, Width: 6
Area: 60
-------------------
```

**Example 10.4: Constructor Chaining**

```java
// ConstructorChainingDemo.java
class Student {
    int rollNo;
    String name;
    String course;
    double fees;

    // Constructor 1 - Calls Constructor 4
    Student() {
        this(0, "Unknown", "Not Assigned", 0.0);
        System.out.println("Constructor 1 called");
    }

    // Constructor 2 - Calls Constructor 4
    Student(int r, String n) {
        this(r, n, "Not Assigned", 0.0);
        System.out.println("Constructor 2 called");
    }

    // Constructor 3 - Calls Constructor 4
    Student(int r, String n, String c) {
        this(r, n, c, 0.0);
        System.out.println("Constructor 3 called");
    }

    // Constructor 4 - Main constructor
    Student(int r, String n, String c, double f) {
        rollNo = r;
        name = n;
        course = c;
        fees = f;
        System.out.println("Constructor 4 (Main) called");
    }

    void display() {
        System.out.println("Roll No: " + rollNo);
        System.out.println("Name: " + name);
        System.out.println("Course: " + course);
        System.out.println("Fees: ₹" + fees);
        System.out.println("-------------------\n");
    }
}

public class ConstructorChainingDemo {
    public static void main(String[] args) {
        System.out.println("=== Constructor Chaining Demo ===\n");

        System.out.println("Creating student with default constructor:");
        Student s1 = new Student();
        s1.display();

        System.out.println("Creating student with 2 parameters:");
        Student s2 = new Student(101, "Alice");
        s2.display();

        System.out.println("Creating student with 3 parameters:");
        Student s3 = new Student(102, "Bob", "Computer Science");
        s3.display();

        System.out.println("Creating student with all parameters:");
        Student s4 = new Student(103, "Charlie", "Electronics", 50000);
        s4.display();
    }
}
```

**Output:**

```
=== Constructor Chaining Demo ===

Creating student with default constructor:
Constructor 4 (Main) called
Constructor 1 called
Roll No: 0
Name: Unknown
Course: Not Assigned
Fees: ₹0.0
-------------------

Creating student with 2 parameters:
Constructor 4 (Main) called
Constructor 2 called
Roll No: 101
Name: Alice
Course: Not Assigned
Fees: ₹0.0
-------------------

Creating student with 3 parameters:
Constructor 4 (Main) called
Constructor 3 called
Roll No: 102
Name: Bob
Course: Computer Science
Fees: ₹0.0
-------------------

Creating student with all parameters:
Constructor 4 (Main) called
Roll No: 103
Name: Charlie
Course: Electronics
Fees: ₹50000.0
-------------------
```

**Example 10.5: Copy Constructor**

```java
// CopyConstructorDemo.java
class Point {
    int x;
    int y;

    // Parameterized constructor
    Point(int x, int y) {
        this.x = x;
        this.y = y;
        System.out.println("Parameterized constructor called");
    }

    // Copy constructor
    Point(Point p) {
        this.x = p.x;
        this.y = p.y;
        System.out.println("Copy constructor called");
    }

    void display() {
        System.out.println("Point(" + x + ", " + y + ")");
    }
}

public class CopyConstructorDemo {
    public static void main(String[] args) {
        System.out.println("=== Copy Constructor Demo ===\n");

        System.out.println("Creating original point:");
        Point p1 = new Point(10, 20);
        p1.display();

        System.out.println("\nCreating copy of point:");
        Point p2 = new Point(p1);  // Copy constructor
        p2.display();

        System.out.println("\nModifying original point:");
        p1.x = 100;
        p1.y = 200;

        System.out.println("Original point:");
        p1.display();
        System.out.println("Copied point (unchanged):");
        p2.display();
    }
}
```

**Output:**

```
=== Copy Constructor Demo ===

Creating original point:
Parameterized constructor called
Point(10, 20)

Creating copy of point:
Copy constructor called
Point(10, 20)

Modifying original point:
Original point:
Point(100, 200)
Copied point (unchanged):
Point(10, 20)
```

### 🎯 Key Takeaways

- Constructors initialize objects when created
- Constructor name must match class name exactly
- Constructors have no return type (not even void)
- Default constructor is provided by Java if no constructor is defined
- Constructors can be overloaded like methods
- Use `this()` for constructor chaining (must be first statement)
- Private constructors prevent direct instantiation

### 📝 Practice Questions

1. What is the difference between a constructor and a method?
2. What happens if you don't define any constructor in a class?
3. Can a constructor be private? If yes, why would you make it private?
4. Write a class with constructor overloading for a `Car` class.
5. What is constructor chaining and why is it useful?

---

## Chapter 11: Inheritance

### 📘 Theory

#### **11.1 What is Inheritance?**

**Inheritance** is a mechanism where a new class (child/subclass) acquires the properties and behaviors of an existing class (parent/superclass). It is one of the four pillars of Object-Oriented Programming.

**Real-World Analogy:**
Think of inheritance like **family traits**:

- A child inherits features from parents (eye color, height, etc.)
- Child has its own unique features too
- Similarly, a subclass inherits from superclass and can add its own features

**Key Terms:**

- **Superclass (Parent/Base Class)** - Class being inherited from
- **Subclass (Child/Derived Class)** - Class that inherits
- **extends** - Keyword used to inherit a class
- **Reusability** - Main advantage of inheritance

**Syntax:**

```java
class Superclass {
    // Superclass members
}

class Subclass extends Superclass {
    // Subclass members + inherited members
}
```

**Benefits of Inheritance:**

- ✅ **Code Reusability** - Reuse existing code
- ✅ **Method Overriding** - Runtime polymorphism
- ✅ **Extensibility** - Easy to add new features
- ✅ **Data Hiding** - Through access modifiers
- ✅ **Hierarchical Classification** - Organize classes

#### **11.2 Types of Inheritance**

**1. Single Inheritance**
One subclass inherits from one superclass.

```
    ┌─────────┐
    │  Animal │ (Superclass)
    └────┬────┘
         │
    ┌────▼────┐
    │   Dog   │ (Subclass)
    └─────────┘
```

```java
class Animal {
    void eat() {
        System.out.println("Animal is eating");
    }
}

class Dog extends Animal {
    void bark() {
        System.out.println("Dog is barking");
    }
}
```

**2. Multilevel Inheritance**
A class inherits from a subclass (chain of inheritance).

```
    ┌─────────┐
    │  Animal │
    └────┬────┘
         │
    ┌────▼────┐
    │   Dog   │
    └────┬────┘
         │
    ┌────▼────────┐
    │  BabyDog    │
    └─────────────┘
```

```java
class Animal {
    void eat() { }
}

class Dog extends Animal {
    void bark() { }
}

class BabyDog extends Dog {
    void weep() { }
}
```

**3. Hierarchical Inheritance**
Multiple subclasses inherit from one superclass.

```
         ┌─────────┐
         │  Animal │
         └────┬────┘
              │
      ┌───────┼───────┐
      │       │       │
  ┌───▼──┐ ┌──▼──┐ ┌─▼───┐
  │ Dog  │ │ Cat │ │ Cow │
  └──────┘ └─────┘ └─────┘
```

```java
class Animal {
    void eat() { }
}

class Dog extends Animal {
    void bark() { }
}

class Cat extends Animal {
    void meow() { }
}
```

**4. Multiple Inheritance (NOT Supported in Java)**
One class inherits from multiple classes - **NOT allowed in Java** (to avoid ambiguity).

```
  ┌─────┐   ┌─────┐
  │  A  │   │  B  │
  └──┬──┘   └──┬──┘
     └────┬────┘
          │
      ┌───▼───┐
      │   C   │  ❌ Not allowed in Java
      └───────┘
```

**Note:** Java achieves multiple inheritance through **interfaces**.

**5. Hybrid Inheritance (NOT Supported in Java)**
Combination of multiple and multilevel inheritance - **NOT allowed in Java**.

#### **11.3 The `super` Keyword**

`super` is a reference variable that refers to the immediate parent class object. It is used to access parent class members (variables, methods, constructors) from the child class.

**What is `super`?**

The `super` keyword is a reference to the parent class. It allows the child class to access members of its parent class, especially when there is a naming conflict or when you want to explicitly call parent class methods or constructors.

**Real-World Analogy:**
Think of `super` like referring to your parent:

- "My **parent's** house" - `super.house`
- "My **parent's** method of doing things" - `super.method()`
- "Call my **parent** first" - `super()`

**Uses of `super` Keyword:**

**1. Access parent class variables**

When both parent and child classes have variables with the same name, `super` is used to access the parent class variable.

```java
class Parent {
    int x = 10;
}

class Child extends Parent {
    int x = 20;  // Same variable name as parent

    void display() {
        System.out.println(super.x);  // 10 (parent's x)
        System.out.println(this.x);   // 20 (child's x)
        System.out.println(x);        // 20 (child's x - default)
    }
}
```

**Why use `super` for variables?**

- Resolve naming conflicts between parent and child variables
- Access hidden parent class variables
- Make code more explicit and readable

**Example - Practical Use:**

```java
class Vehicle {
    String type = "Vehicle";
}

class Car extends Vehicle {
    String type = "Car";

    void showTypes() {
        System.out.println("Parent type: " + super.type);  // Vehicle
        System.out.println("Child type: " + this.type);    // Car
    }
}
```

**2. Call parent class methods**

When a child class overrides a parent class method, `super` can be used to call the parent's version of the method.

```java
class Parent {
    void display() {
        System.out.println("Parent display");
    }
}

class Child extends Parent {
    void display() {
        super.display();  // Call parent's display() first
        System.out.println("Child display");
    }
}
```

**Why use `super` for methods?**

- Call parent's method even after overriding
- Extend parent's functionality instead of replacing it
- Reuse parent's code

**Example - Practical Use:**

```java
class Employee {
    void calculateSalary() {
        System.out.println("Calculating basic salary...");
    }
}

class Manager extends Employee {
    void calculateSalary() {
        super.calculateSalary();  // Calculate basic salary first
        System.out.println("Adding manager bonus...");
    }
}
```

**3. Call parent class constructor**

`super()` is used to call the parent class constructor from the child class constructor.

```java
class Parent {
    Parent() {
        System.out.println("Parent constructor");
    }

    Parent(String name) {
        System.out.println("Parent constructor: " + name);
    }
}

class Child extends Parent {
    Child() {
        super();  // Call parent's no-arg constructor (must be first statement)
        System.out.println("Child constructor");
    }

    Child(String name) {
        super(name);  // Call parent's parameterized constructor
        System.out.println("Child constructor: " + name);
    }
}
```

**Important Rules for `super()` in constructor:**

- Must be the **first statement** in child constructor
- If not explicitly called, Java automatically calls `super()` (no-arg constructor)
- Cannot use both `this()` and `super()` in same constructor
- Used to initialize parent class members

**Example - Constructor Chaining:**

```java
class Person {
    String name;
    int age;

    Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
}

class Student extends Person {
    int rollNo;

    Student(String name, int age, int rollNo) {
        super(name, age);  // Initialize parent class members
        this.rollNo = rollNo;  // Initialize child class member
    }
}
```

**Comparison: `this` vs `super`**

| Feature              | `this`                                     | `super`                                       |
| -------------------- | ------------------------------------------ | --------------------------------------------- |
| **Refers to**        | Current class object                       | Parent class object                           |
| **Access variables** | Current class variables                    | Parent class variables                        |
| **Call methods**     | Current class methods                      | Parent class methods                          |
| **Call constructor** | Current class constructor                  | Parent class constructor                      |
| **Usage**            | `this.variable`, `this.method()`, `this()` | `super.variable`, `super.method()`, `super()` |
| **Context**          | Any class                                  | Only in inheritance                           |

**Important Points:**

- `super` is used only in inheritance (child class)
- `super()` must be first statement in constructor
- Cannot use `super` in static context
- If parent constructor is not called explicitly, Java calls `super()` automatically
- `super` helps in code reusability and extending parent functionality

**Common Use Cases:**

1. **Access hidden parent variables:**

   ```java
   super.variableName
   ```

2. **Call overridden parent methods:**

   ```java
   super.methodName()
   ```

3. **Initialize parent class in child constructor:**

   ```java
   super(parameters)
   ```

4. **Extend parent functionality:**
   ```java
   void method() {
       super.method();  // Call parent's version
       // Add child-specific code
   }
   ```

#### **11.4 Method Overriding**

**Definition:** Method overriding occurs when a subclass provides a specific implementation of a method that is already defined in its superclass. The child class method replaces the parent class method.

**What is Method Overriding?**

Method overriding is a feature that allows a child class to provide its own implementation of a method that is already provided by its parent class. This is used to achieve runtime polymorphism.

**Real-World Analogy:**
Think of method overriding like customizing inherited behavior:

- **Parent's way:** "I cook food by boiling"
- **Child's way:** "I cook food by frying" (overriding parent's method)
- Same action (cooking), different implementation

**Rules for Method Overriding:**

1. **Method name must be same** - Exact same name as parent method
2. **Parameters must be same** - Same number, type, and order of parameters
3. **Return type must be same or covariant** - Same type or subtype of parent's return type
4. **Access modifier cannot be more restrictive** - Can be same or less restrictive
   - If parent method is `protected`, child can be `protected` or `public` (NOT `private`)
5. **Cannot override static methods** - Static methods are hidden, not overridden
6. **Cannot override final methods** - `final` methods cannot be changed
7. **Cannot override private methods** - Private methods are not visible to child class
8. **Must have IS-A relationship** - Inheritance must exist

**Example:**

```java
class Animal {
    void sound() {
        System.out.println("Animal makes sound");
    }
}

class Dog extends Animal {
    @Override  // Annotation (optional but recommended)
    void sound() {
        System.out.println("Dog barks");
    }
}

class Cat extends Animal {
    @Override
    void sound() {
        System.out.println("Cat meows");
    }
}

// Usage
Animal a1 = new Dog();
a1.sound();  // Output: Dog barks (child's method is called)

Animal a2 = new Cat();
a2.sound();  // Output: Cat meows
```

**@Override Annotation:**

The `@Override` annotation is used to indicate that a method is overriding a parent class method.

**Benefits:**

- Helps catch errors at compile-time
- Makes code more readable
- If parent method signature changes, compiler will show error

**Example:**

```java
class Parent {
    void display() {
        System.out.println("Parent");
    }
}

class Child extends Parent {
    @Override
    void display() {  // Correct - overriding parent's method
        System.out.println("Child");
    }

    @Override
    void show() {  // Compile error - no such method in parent
        System.out.println("Show");
    }
}
```

**Access Modifier Rules in Overriding:**

```java
class Parent {
    protected void method1() { }
    public void method2() { }
}

class Child extends Parent {
    // VALID - same access level
    protected void method1() { }

    // VALID - less restrictive (public > protected)
    public void method1() { }

    // INVALID - more restrictive (private < protected)
    // private void method1() { }  // Compilation error

    // VALID - same access level
    public void method2() { }

    // INVALID - more restrictive (protected < public)
    // protected void method2() { }  // Compilation error
}
```

**Covariant Return Type (Java 5+):**

The overriding method can return a subtype of the type returned by the parent method.

```java
class Animal {
    Animal getAnimal() {
        return new Animal();
    }
}

class Dog extends Animal {
    @Override
    Dog getAnimal() {  // Covariant return type (Dog is subtype of Animal)
        return new Dog();
    }
}
```

**Why Method Overriding is Important:**

1. **Runtime Polymorphism** - Decide which method to call at runtime
2. **Specific Implementation** - Child class can provide specific behavior
3. **Code Flexibility** - Same interface, different implementations
4. **Extensibility** - Easy to add new classes with different behaviors

**Method Overloading vs Method Overriding:**

| Feature     | Overloading                            | Overriding                                |
| ----------- | -------------------------------------- | ----------------------------------------- |
| Definition  | Same method name, different parameters | Same method signature in parent and child |
| Class       | Same class                             | Different classes (inheritance)           |
| Parameters  | Must be different                      | Must be same                              |
| Return Type | Can be different                       | Must be same (or covariant)               |
| Binding     | Compile-time (static)                  | Runtime (dynamic)                         |
| Purpose     | Increase readability                   | Runtime polymorphism                      |

#### **11.5 Constructor in Inheritance**

**Key Points:**

- Constructors are **NOT inherited**
- Parent constructor is called **before** child constructor
- Use `super()` to call parent constructor explicitly
- If not specified, Java automatically calls parent's default constructor

**Example:**

```java
class Parent {
    Parent() {
        System.out.println("Parent constructor");
    }
}

class Child extends Parent {
    Child() {
        // super(); is automatically added by Java
        System.out.println("Child constructor");
    }
}

// Output:
// Parent constructor
// Child constructor
```

#### **11.6 The `final` Keyword with Inheritance**

The `final` keyword is used to restrict the user from modifying variables, methods, or classes. It provides immutability and security in inheritance.

**What is `final`?**

The `final` keyword can be applied to variables, methods, and classes to prevent modification, overriding, or inheritance respectively.

**Real-World Analogy:**
Think of `final` like a "sealed" or "locked" item:

- **Final variable:** A sealed envelope - cannot change contents
- **Final method:** A locked recipe - cannot modify the recipe
- **Final class:** A sealed box - cannot extend or open

**Uses of `final` Keyword:**

**1. final Variable - Cannot be changed (constant)**

A `final` variable can be assigned only once. Once initialized, its value cannot be changed.

```java
final int MAX = 100;
MAX = 200;  // Compilation error - cannot reassign
```

**Types of final variables:**

**a) Final instance variable:**

```java
class Student {
    final int rollNo;  // Must be initialized

    Student(int rollNo) {
        this.rollNo = rollNo;  // Initialize in constructor
    }

    void changeRollNo() {
        // rollNo = 100;  // Error - cannot change
    }
}
```

**b) Final static variable (Constant):**

```java
class MathConstants {
    final static double PI = 3.14159;  // Class-level constant
    final static int MAX_VALUE = 100;
}
```

**c) Final local variable:**

```java
void method() {
    final int x = 10;
    // x = 20;  // Error - cannot change
}
```

**Benefits of final variables:**

- Create constants
- Prevent accidental modification
- Thread-safe (immutable)
- Better performance (compiler optimization)

**2. final Method - Cannot be overridden**

A `final` method cannot be overridden by child classes. This ensures the method's behavior remains consistent across inheritance.

```java
class Parent {
    final void display() {
        System.out.println("This method cannot be overridden");
    }

    void show() {
        System.out.println("This method can be overridden");
    }
}

class Child extends Parent {
    // Cannot override final method
    // void display() {  // Compilation error
    //     System.out.println("Trying to override");
    // }

    // Can override non-final method
    void show() {
        System.out.println("Overridden show method");
    }
}
```

**Why use final methods?**

- Prevent child classes from changing critical behavior
- Security - ensure method implementation is not altered
- Performance - compiler can inline final methods
- Design - enforce specific implementation

**Example - Real-world use:**

```java
class BankAccount {
    private double balance;

    // Final method - security critical, cannot be overridden
    final void deductTax() {
        balance = balance * 0.9;  // 10% tax
    }

    // Non-final method - can be customized
    void calculateInterest() {
        balance = balance * 1.05;  // 5% interest
    }
}

class SavingsAccount extends BankAccount {
    // Cannot override deductTax() - it's final

    // Can override calculateInterest()
    void calculateInterest() {
        // Custom interest calculation for savings account
    }
}
```

**3. final Class - Cannot be inherited**

A `final` class cannot be extended (subclassed). No class can inherit from a final class.

```java
final class ImmutableClass {
    private final int value;

    ImmutableClass(int value) {
        this.value = value;
    }

    int getValue() {
        return value;
    }
}

// Cannot extend final class
// class SubClass extends ImmutableClass {  // Compilation error
//     // Cannot inherit from final class
// }
```

**Why use final classes?**

- Create immutable classes (like String, Integer, etc.)
- Security - prevent inheritance and modification
- Design - class is complete and should not be extended
- Performance - compiler optimizations

**Example - Real-world use:**

```java
// String class in Java is final
final class String {
    // Cannot be extended
}

// Wrapper classes are final
final class Integer {
    // Cannot be extended
}

final class Double {
    // Cannot be extended
}
```

**Summary of `final` Keyword:**

| Type               | Syntax                    | Effect                | Use Case                    |
| ------------------ | ------------------------- | --------------------- | --------------------------- |
| **final variable** | `final int x = 10;`       | Cannot reassign value | Constants, immutability     |
| **final method**   | `final void method() { }` | Cannot override       | Security, critical methods  |
| **final class**    | `final class MyClass { }` | Cannot inherit        | Immutable classes, security |

**Important Points:**

- `final` variable must be initialized (in declaration, constructor, or initializer block)
- `final` method can be inherited but not overridden
- `final` class cannot have subclasses
- All methods in a `final` class are implicitly `final`
- `final` with `static` creates class-level constants
- `final` parameters cannot be modified inside method

**final vs finally vs finalize:**

| Keyword      | Purpose                                                | Usage                       |
| ------------ | ------------------------------------------------------ | --------------------------- |
| **final**    | Restriction (constant, no override, no inheritance)    | Variables, methods, classes |
| **finally**  | Exception handling (always executes)                   | try-catch-finally block     |
| **finalize** | Garbage collection (cleanup before object destruction) | Method in Object class      |

**Common Use Cases:**

1. **Constants:**

   ```java
   final double PI = 3.14159;
   ```

2. **Prevent method overriding:**

   ```java
   final void criticalMethod() { }
   ```

3. **Immutable classes:**

   ```java
   final class ImmutablePerson {
       private final String name;
       // ...
   }
   ```

4. **Security:**
   ```java
   final class SecurityManager {
       // Cannot be extended for security reasons
   }
   ```

#### **11.7 Access Modifiers in Inheritance**

| Modifier  | Same Class | Same Package | Subclass (Different Package) | Other Package |
| --------- | ---------- | ------------ | ---------------------------- | ------------- |
| private   | ✅         | ❌           | ❌                           | ❌            |
| default   | ✅         | ✅           | ❌                           | ❌            |
| protected | ✅         | ✅           | ✅                           | ❌            |
| public    | ✅         | ✅           | ✅                           | ✅            |

**Inheritance Access:**

- **private** members are NOT inherited
- **default** members are inherited only in same package
- **protected** members are inherited in subclass
- **public** members are always inherited

### 💻 Practical Examples

**Example 11.1: Single Inheritance**

```java
// SingleInheritanceDemo.java
class Vehicle {
    String brand;
    int speed;

    void displayInfo() {
        System.out.println("Brand: " + brand);
        System.out.println("Speed: " + speed + " km/h");
    }

    void start() {
        System.out.println("Vehicle is starting...");
    }
}

class Car extends Vehicle {
    int numberOfDoors;

    void displayCarInfo() {
        displayInfo();  // Inherited method
        System.out.println("Number of Doors: " + numberOfDoors);
    }

    void honk() {
        System.out.println("Car is honking: Beep! Beep!");
    }
}

public class SingleInheritanceDemo {
    public static void main(String[] args) {
        System.out.println("=== Single Inheritance Demo ===\n");

        Car myCar = new Car();
        myCar.brand = "Toyota";      // Inherited field
        myCar.speed = 120;           // Inherited field
        myCar.numberOfDoors = 4;     // Own field

        myCar.start();               // Inherited method
        myCar.honk();                // Own method
        System.out.println();
        myCar.displayCarInfo();
    }
}
```

**Output:**

```
=== Single Inheritance Demo ===

Vehicle is starting...
Car is honking: Beep! Beep!

Brand: Toyota
Speed: 120 km/h
Number of Doors: 4
```

**Example 11.2: Multilevel Inheritance**

```java
// MultilevelInheritanceDemo.java
class Animal {
    void eat() {
        System.out.println("Animal is eating");
    }
}

class Dog extends Animal {
    void bark() {
        System.out.println("Dog is barking");
    }
}

class BabyDog extends Dog {
    void weep() {
        System.out.println("Baby dog is weeping");
    }
}

public class MultilevelInheritanceDemo {
    public static void main(String[] args) {
        System.out.println("=== Multilevel Inheritance Demo ===\n");

        BabyDog puppy = new BabyDog();

        puppy.eat();    // From Animal (grandparent)
        puppy.bark();   // From Dog (parent)
        puppy.weep();   // Own method
    }
}
```

**Output:**

```
=== Multilevel Inheritance Demo ===

Animal is eating
Dog is barking
Baby dog is weeping
```

**Example 11.3: Hierarchical Inheritance**

```java
// HierarchicalInheritanceDemo.java
class Shape {
    void draw() {
        System.out.println("Drawing a shape");
    }
}

class Circle extends Shape {
    void draw() {
        System.out.println("Drawing a circle");
    }
}

class Rectangle extends Shape {
    void draw() {
        System.out.println("Drawing a rectangle");
    }
}

class Triangle extends Shape {
    void draw() {
        System.out.println("Drawing a triangle");
    }
}

public class HierarchicalInheritanceDemo {
    public static void main(String[] args) {
        System.out.println("=== Hierarchical Inheritance Demo ===\n");

        Circle c = new Circle();
        Rectangle r = new Rectangle();
        Triangle t = new Triangle();

        c.draw();
        r.draw();
        t.draw();
    }
}
```

**Output:**

```
=== Hierarchical Inheritance Demo ===

Drawing a circle
Drawing a rectangle
Drawing a triangle
```

**Example 11.4: Using `super` Keyword**

```java
// SuperKeywordDemo.java
class Parent {
    int x = 100;

    Parent() {
        System.out.println("Parent constructor called");
    }

    void display() {
        System.out.println("Parent display method");
    }
}

class Child extends Parent {
    int x = 200;

    Child() {
        super();  // Call parent constructor
        System.out.println("Child constructor called");
    }

    void display() {
        super.display();  // Call parent method
        System.out.println("Child display method");
    }

    void showValues() {
        System.out.println("Parent x: " + super.x);  // 100
        System.out.println("Child x: " + this.x);    // 200
    }
}

public class SuperKeywordDemo {
    public static void main(String[] args) {
        System.out.println("=== super Keyword Demo ===\n");

        Child obj = new Child();
        System.out.println();

        obj.display();
        System.out.println();

        obj.showValues();
    }
}
```

**Output:**

```
=== super Keyword Demo ===

Parent constructor called
Child constructor called

Parent display method
Child display method

Parent x: 100
Child x: 200
```

**Example 11.5: Method Overriding**

```java
// MethodOverridingDemo.java
class Bank {
    double getRateOfInterest() {
        return 0.0;
    }
}

class SBI extends Bank {
    @Override
    double getRateOfInterest() {
        return 7.5;
    }
}

class HDFC extends Bank {
    @Override
    double getRateOfInterest() {
        return 8.0;
    }
}

class ICICI extends Bank {
    @Override
    double getRateOfInterest() {
        return 7.8;
    }
}

public class MethodOverridingDemo {
    public static void main(String[] args) {
        System.out.println("=== Method Overriding Demo ===\n");

        Bank sbi = new SBI();
        Bank hdfc = new HDFC();
        Bank icici = new ICICI();

        System.out.println("SBI Rate of Interest: " + sbi.getRateOfInterest() + "%");
        System.out.println("HDFC Rate of Interest: " + hdfc.getRateOfInterest() + "%");
        System.out.println("ICICI Rate of Interest: " + icici.getRateOfInterest() + "%");
    }
}
```

**Output:**

```
=== Method Overriding Demo ===

SBI Rate of Interest: 7.5%
HDFC Rate of Interest: 8.0%
ICICI Rate of Interest: 7.8%
```

### 🎯 Key Takeaways

- Inheritance promotes code reusability
- Use `extends` keyword to inherit a class
- Java supports single, multilevel, and hierarchical inheritance
- Java does NOT support multiple inheritance (use interfaces instead)
- `super` keyword accesses parent class members
- Method overriding enables runtime polymorphism
- Constructors are not inherited but parent constructor is called first
- `final` class cannot be inherited, `final` method cannot be overridden

### 📝 Practice Questions

1. What is inheritance and why is it useful?
2. What are the types of inheritance supported in Java?
3. Why doesn't Java support multiple inheritance?
4. What is the difference between method overloading and method overriding?
5. Write a program demonstrating multilevel inheritance with Employee → Manager → Director.

---

## Chapter 12: Polymorphism

### 📘 Theory

#### **12.1 What is Polymorphism?**

**Polymorphism** means "many forms". It is the ability of an object to take many forms. In Java, polymorphism allows us to perform a single action in different ways.

**Real-World Analogy:**
Think of a **person** who can be:

- A student in college
- A son/daughter at home
- An employee at work
- A customer in a shop

Same person, different roles (forms) - that's polymorphism!

**Types of Polymorphism in Java:**

1. **Compile-Time Polymorphism (Static Binding)** - Method Overloading
2. **Runtime Polymorphism (Dynamic Binding)** - Method Overriding

#### **12.2 Compile-Time Polymorphism (Method Overloading)**

**Definition:** Multiple methods with the **same name** but **different parameters** in the same class.

**Achieved by:**

- Different number of parameters
- Different types of parameters
- Different order of parameters

**Example:**

```java
class Calculator {
    // Method 1
    int add(int a, int b) {
        return a + b;
    }

    // Method 2 - Different number of parameters
    int add(int a, int b, int c) {
        return a + b + c;
    }

    // Method 3 - Different type of parameters
    double add(double a, double b) {
        return a + b;
    }
}
```

**Key Points:**

- Resolved at **compile time**
- Also called **static polymorphism**
- Increases code readability
- Return type alone is NOT sufficient for overloading

#### **12.3 Runtime Polymorphism (Method Overriding)**

**Definition:** When a subclass provides a specific implementation of a method that is already defined in its parent class.

**Achieved by:**

- Inheritance (IS-A relationship)
- Method overriding
- Upcasting (parent reference, child object)

**Example:**

```java
class Animal {
    void sound() {
        System.out.println("Animal makes sound");
    }
}

class Dog extends Animal {
    @Override
    void sound() {
        System.out.println("Dog barks");
    }
}

class Cat extends Animal {
    @Override
    void sound() {
        System.out.println("Cat meows");
    }
}

// Usage
Animal a;
a = new Dog();
a.sound();  // Dog barks (runtime decision)

a = new Cat();
a.sound();  // Cat meows (runtime decision)
```

**Key Points:**

- Resolved at **runtime**
- Also called **dynamic polymorphism**
- Enables **dynamic method dispatch**
- Requires inheritance

#### **12.4 Upcasting and Downcasting**

Type casting in Java allows you to convert one type to another. In the context of inheritance, we have two types of casting: upcasting and downcasting.

**What is Type Casting in Inheritance?**

Type casting is the process of converting a reference of one class type to another class type within an inheritance hierarchy.

**Real-World Analogy:**
Think of casting like categorizing objects:

- **Upcasting:** "This Golden Retriever is an Animal" (specific → general)
- **Downcasting:** "This Animal is a Golden Retriever" (general → specific, needs verification)

---

**Upcasting (Implicit/Automatic)**

Upcasting is the process of converting a subclass reference to a superclass reference. It happens automatically.

**Syntax:**

```java
SuperClass ref = new SubClass();  // Automatic upcasting
```

**Example:**

```java
class Animal {
    void eat() {
        System.out.println("Animal is eating");
    }
}

class Dog extends Animal {
    void bark() {
        System.out.println("Dog is barking");
    }

    void eat() {
        System.out.println("Dog is eating");
    }
}

// Upcasting
Animal a = new Dog();  // Dog object referenced by Animal type
a.eat();    // Works - calls Dog's eat() method (runtime polymorphism)
// a.bark();  // Error - Animal reference cannot access Dog-specific methods
```

**Key Points about Upcasting:**

1. **Automatic** - No explicit casting required
2. **Safe** - Always succeeds, no exceptions
3. **Restricts access** - Can only access superclass members
4. **Enables polymorphism** - Allows runtime method dispatch

**Benefits of Upcasting:**

- **Achieve runtime polymorphism** - Call overridden methods dynamically
- **Write generic code** - Work with parent type, handle multiple child types
- **Flexibility in method parameters** - Accept any subclass as parameter
- **Code reusability** - Single method can work with multiple subclasses

**Example - Generic Method:**

```java
void feedAnimal(Animal a) {  // Accepts any Animal subclass
    a.eat();
}

feedAnimal(new Dog());   // Upcasting Dog to Animal
feedAnimal(new Cat());   // Upcasting Cat to Animal
feedAnimal(new Lion());  // Upcasting Lion to Animal
```

**Memory Representation:**

```
Animal a = new Dog();

Stack:                  Heap:
┌─────────┐            ┌──────────────┐
│ a (ref) │───────────>│ Dog Object   │
│ (Animal)│            │ - eat()      │
└─────────┘            │ - bark()     │
                       └──────────────┘

Reference type: Animal (can access only Animal methods)
Object type: Dog (actual object in memory)
```

---

**Downcasting (Explicit/Manual)**

Downcasting is the process of converting a superclass reference to a subclass reference. It must be done explicitly.

**Syntax:**

```java
SubClass ref = (SubClass) superClassRef;  // Manual downcasting
```

**Example:**

```java
Animal a = new Dog();  // Upcasting
Dog d = (Dog) a;       // Downcasting (explicit)
d.bark();              // Now can access Dog-specific methods
```

**Key Points about Downcasting:**

1. **Manual** - Requires explicit casting
2. **Risky** - Can throw `ClassCastException` at runtime
3. **Expands access** - Can access subclass-specific members
4. **Requires verification** - Should check type before casting

**When to use Downcasting:**

- When you need to access subclass-specific methods
- When you're certain about the actual object type
- When you need to restore full functionality of the object

**Example - Downcasting:**

```java
class Animal {
    void eat() {
        System.out.println("Eating...");
    }
}

class Dog extends Animal {
    void bark() {
        System.out.println("Barking...");
    }
}

class Cat extends Animal {
    void meow() {
        System.out.println("Meowing...");
    }
}

// Upcasting
Animal a1 = new Dog();
Animal a2 = new Cat();

// Downcasting
Dog d = (Dog) a1;  // Valid - a1 actually holds Dog object
d.bark();          // Works

Cat c = (Cat) a2;  // Valid - a2 actually holds Cat object
c.meow();          // Works

// Invalid downcasting
// Dog d2 = (Dog) a2;  // Runtime error - ClassCastException
                       // a2 holds Cat, not Dog
```

**ClassCastException:**

Occurs when you try to cast an object to a type it's not compatible with.

```java
Animal a = new Cat();
Dog d = (Dog) a;  // ClassCastException at runtime
                  // Cat cannot be cast to Dog
```

**Safe Downcasting using `instanceof`:**

Always check the type before downcasting to avoid `ClassCastException`.

```java
Animal a = new Dog();

// Check before downcasting
if (a instanceof Dog) {
    Dog d = (Dog) a;  // Safe downcasting
    d.bark();
} else {
    System.out.println("Not a Dog");
}
```

**Example - Safe Downcasting:**

```java
void processAnimal(Animal a) {
    a.eat();  // Common method

    // Check and downcast
    if (a instanceof Dog) {
        Dog d = (Dog) a;
        d.bark();
    } else if (a instanceof Cat) {
        Cat c = (Cat) a;
        c.meow();
    }
}
```

**Comparison: Upcasting vs Downcasting**

| Feature       | Upcasting                          | Downcasting                           |
| ------------- | ---------------------------------- | ------------------------------------- |
| **Direction** | Subclass → Superclass              | Superclass → Subclass                 |
| **Casting**   | Implicit (automatic)               | Explicit (manual)                     |
| **Safety**    | Always safe                        | Risky (can throw exception)           |
| **Syntax**    | `SuperClass ref = new SubClass();` | `SubClass ref = (SubClass) superRef;` |
| **Access**    | Only superclass members            | All subclass members                  |
| **Use case**  | Polymorphism, generic code         | Access subclass-specific features     |
| **Exception** | Never throws exception             | Can throw `ClassCastException`        |

**Important Rules:**

1. **Upcasting is always safe** - Child IS-A Parent
2. **Downcasting needs verification** - Use `instanceof` operator
3. **Cannot cast unrelated classes** - Must have inheritance relationship
4. **Actual object type matters** - Not the reference type

**Best Practices:**

1. **Always use `instanceof` before downcasting:**

   ```java
   if (obj instanceof Dog) {
       Dog d = (Dog) obj;
   }
   ```

2. **Prefer upcasting for polymorphism:**

   ```java
   List<Animal> animals = new ArrayList<>();
   animals.add(new Dog());  // Upcasting
   animals.add(new Cat());  // Upcasting
   ```

3. **Avoid unnecessary downcasting:**
   - Design code to work with parent type when possible
   - Use polymorphism instead of type checking

#### **12.5 Dynamic Method Dispatch**

**Definition:** Dynamic Method Dispatch is the mechanism by which a call to an overridden method is resolved at runtime rather than compile time. It is the foundation of runtime polymorphism in Java.

**What is Dynamic Method Dispatch?**

Dynamic Method Dispatch is Java's mechanism for supporting runtime polymorphism. When a method is called on a parent class reference that holds a child class object, the JVM determines which version of the method to execute based on the actual object type (not the reference type).

**Real-World Analogy:**
Think of dynamic method dispatch like a remote control:

- **Remote (Reference):** Universal remote (Parent type)
- **Device (Object):** TV, AC, or Fan (Child types)
- **Button Press (Method Call):** Power button
- **Action (Method Execution):** Different devices respond differently to the same button

**How it works:**

1. **Parent reference holds child object** - Upcasting occurs
2. **Method call is made** - Call method on parent reference
3. **JVM determines which method to call at runtime** - Based on actual object type
4. **Calls the overridden method in child class** - Child's version executes

**Step-by-Step Process:**

```java
Animal a = new Dog();  // Step 1: Parent reference, child object
a.sound();             // Step 2: Method call
                       // Step 3: JVM checks actual object type (Dog)
                       // Step 4: Calls Dog's sound() method
```

**Example:**

```java
class Shape {
    void draw() {
        System.out.println("Drawing shape");
    }
}

class Circle extends Shape {
    @Override
    void draw() {
        System.out.println("Drawing circle");
    }
}

class Rectangle extends Shape {
    @Override
    void draw() {
        System.out.println("Drawing rectangle");
    }
}

class Triangle extends Shape {
    @Override
    void draw() {
        System.out.println("Drawing triangle");
    }
}

// Dynamic method dispatch
Shape s;  // Parent reference

s = new Circle();
s.draw();  // Output: Drawing circle (decided at runtime)

s = new Rectangle();
s.draw();  // Output: Drawing rectangle (decided at runtime)

s = new Triangle();
s.draw();  // Output: Drawing triangle (decided at runtime)
```

**Why is it called "Dynamic"?**

- The method to be called is determined **at runtime** (dynamically)
- Not determined at compile time (statically)
- Depends on the actual object type, not reference type

**Compile-Time vs Runtime:**

```java
Shape s = new Circle();
s.draw();

// Compile time:
// - Compiler checks: Does Shape class have draw() method? YES ✓
// - Compiler allows the call

// Runtime:
// - JVM checks: What is the actual object type? Circle
// - JVM calls: Circle's draw() method
```

**Example - Practical Use:**

```java
class Employee {
    void calculateSalary() {
        System.out.println("Calculating employee salary");
    }
}

class Manager extends Employee {
    @Override
    void calculateSalary() {
        System.out.println("Calculating manager salary with bonus");
    }
}

class Developer extends Employee {
    @Override
    void calculateSalary() {
        System.out.println("Calculating developer salary with incentives");
    }
}

class Intern extends Employee {
    @Override
    void calculateSalary() {
        System.out.println("Calculating intern stipend");
    }
}

// Dynamic method dispatch in action
class PayrollSystem {
    void processSalary(Employee emp) {  // Accepts any Employee type
        emp.calculateSalary();  // Calls appropriate method at runtime
    }
}

// Usage
PayrollSystem payroll = new PayrollSystem();
payroll.processSalary(new Manager());    // Manager's method called
payroll.processSalary(new Developer());  // Developer's method called
payroll.processSalary(new Intern());     // Intern's method called
```

**Benefits of Dynamic Method Dispatch:**

1. **Flexibility** - Same code works with different object types
2. **Extensibility** - Easy to add new subclasses without changing existing code
3. **Loose Coupling** - Code depends on parent type, not specific child types
4. **Code Reusability** - Single method handles multiple types

**Example - Array of Parent Type:**

```java
Shape[] shapes = new Shape[3];
shapes[0] = new Circle();
shapes[1] = new Rectangle();
shapes[2] = new Triangle();

// Dynamic method dispatch in loop
for (Shape s : shapes) {
    s.draw();  // Calls appropriate draw() method for each object
}

// Output:
// Drawing circle
// Drawing rectangle
// Drawing triangle
```

**Important Points:**

1. **Works only with instance methods** - Not with static methods or variables
2. **Requires method overriding** - Child must override parent's method
3. **Based on object type** - Not reference type
4. **Happens at runtime** - JVM decides which method to call
5. **Enables polymorphism** - Core mechanism for runtime polymorphism

**What is NOT dispatched dynamically:**

**1. Static methods:**

```java
class Parent {
    static void display() {
        System.out.println("Parent static");
    }
}

class Child extends Parent {
    static void display() {
        System.out.println("Child static");
    }
}

Parent p = new Child();
p.display();  // Output: Parent static (no dynamic dispatch for static methods)
```

**2. Variables:**

```java
class Parent {
    int x = 10;
}

class Child extends Parent {
    int x = 20;
}

Parent p = new Child();
System.out.println(p.x);  // Output: 10 (parent's variable, no dynamic dispatch)
```

**3. Private methods:**

```java
class Parent {
    private void display() {
        System.out.println("Parent");
    }
}

class Child extends Parent {
    private void display() {  // Not overriding, just hiding
        System.out.println("Child");
    }
}
```

**Memory Representation:**

```
Shape s = new Circle();
s.draw();

┌─────────────────┐
│ Compile Time    │
│ Reference: Shape│ ──> Checks if Shape has draw() method ✓
└─────────────────┘

┌─────────────────┐
│ Runtime         │
│ Object: Circle  │ ──> Calls Circle's draw() method
└─────────────────┘
```

**Real-World Application:**

```java
// Payment processing system
class Payment {
    void processPayment() {
        System.out.println("Processing payment");
    }
}

class CreditCardPayment extends Payment {
    @Override
    void processPayment() {
        System.out.println("Processing credit card payment");
    }
}

class DebitCardPayment extends Payment {
    @Override
    void processPayment() {
        System.out.println("Processing debit card payment");
    }
}

class UPIPayment extends Payment {
    @Override
    void processPayment() {
        System.out.println("Processing UPI payment");
    }
}

// Single method handles all payment types
void checkout(Payment payment) {
    payment.processPayment();  // Dynamic method dispatch
}

// Usage
checkout(new CreditCardPayment());  // Credit card processing
checkout(new DebitCardPayment());   // Debit card processing
checkout(new UPIPayment());         // UPI processing
```

#### **12.6 Rules for Method Overriding (Runtime Polymorphism)**

**Must Follow:**

- Method name must be **same**
- Parameters must be **same**
- Return type must be **same** (or covariant)
- Access modifier cannot be **more restrictive**
- Must have **IS-A relationship** (inheritance)

**Cannot Override:**

- **static** methods (they are hidden, not overridden)
- **final** methods
- **private** methods
- **constructors**

#### **12.7 Compile-Time vs Runtime Polymorphism**

| Feature           | Compile-Time                       | Runtime                   |
| ----------------- | ---------------------------------- | ------------------------- |
| **Also Known As** | Static Polymorphism                | Dynamic Polymorphism      |
| **Achieved By**   | Method Overloading                 | Method Overriding         |
| **Binding**       | Early Binding (Compile time)       | Late Binding (Runtime)    |
| **Inheritance**   | Not required                       | Required                  |
| **Performance**   | Faster                             | Slightly slower           |
| **Flexibility**   | Less flexible                      | More flexible             |
| **Example**       | add(int, int), add(double, double) | Parent ref = new Child(); |

#### **12.8 instanceof Operator**

Used to check if an object is an instance of a specific class or interface.

**Syntax:**

```java
object instanceof ClassName
```

**Example:**

```java
Dog d = new Dog();
System.out.println(d instanceof Dog);     // true
System.out.println(d instanceof Animal);  // true
System.out.println(d instanceof Object);  // true
```

**Use Case:**
Safe downcasting to avoid `ClassCastException`.

```java
Animal a = new Dog();
if (a instanceof Dog) {
    Dog d = (Dog) a;  // Safe downcasting
    d.bark();
}
```

### 💻 Practical Examples

**Example 12.1: Compile-Time Polymorphism (Method Overloading)**

```java
// CompileTimePolymorphism.java
class MathOperations {
    // Method 1 - Two integers
    int multiply(int a, int b) {
        return a * b;
    }

    // Method 2 - Three integers
    int multiply(int a, int b, int c) {
        return a * b * c;
    }

    // Method 3 - Two doubles
    double multiply(double a, double b) {
        return a * b;
    }

    // Method 4 - Different order
    String multiply(String str, int times) {
        String result = "";
        for (int i = 0; i < times; i++) {
            result += str;
        }
        return result;
    }
}

public class CompileTimePolymorphism {
    public static void main(String[] args) {
        System.out.println("=== Compile-Time Polymorphism Demo ===\n");

        MathOperations math = new MathOperations();

        System.out.println("multiply(5, 3): " + math.multiply(5, 3));
        System.out.println("multiply(2, 3, 4): " + math.multiply(2, 3, 4));
        System.out.println("multiply(2.5, 3.5): " + math.multiply(2.5, 3.5));
        System.out.println("multiply(\"Hello\", 3): " + math.multiply("Hello", 3));
    }
}
```

**Output:**

```
=== Compile-Time Polymorphism Demo ===

multiply(5, 3): 15
multiply(2, 3, 4): 24
multiply(2.5, 3.5): 8.75
multiply("Hello", 3): HelloHelloHello
```

**Example 12.2: Runtime Polymorphism (Method Overriding)**

```java
// RuntimePolymorphism.java
class Animal {
    void sound() {
        System.out.println("Animal makes a sound");
    }

    void sleep() {
        System.out.println("Animal is sleeping");
    }
}

class Dog extends Animal {
    @Override
    void sound() {
        System.out.println("Dog barks: Woof! Woof!");
    }
}

class Cat extends Animal {
    @Override
    void sound() {
        System.out.println("Cat meows: Meow! Meow!");
    }
}

class Cow extends Animal {
    @Override
    void sound() {
        System.out.println("Cow moos: Moo! Moo!");
    }
}

public class RuntimePolymorphism {
    public static void main(String[] args) {
        System.out.println("=== Runtime Polymorphism Demo ===\n");

        // Parent reference, child objects (Upcasting)
        Animal animal;

        animal = new Dog();
        System.out.println("Dog:");
        animal.sound();  // Dog's sound (runtime decision)
        animal.sleep();  // Inherited method
        System.out.println();

        animal = new Cat();
        System.out.println("Cat:");
        animal.sound();  // Cat's sound (runtime decision)
        animal.sleep();  // Inherited method
        System.out.println();

        animal = new Cow();
        System.out.println("Cow:");
        animal.sound();  // Cow's sound (runtime decision)
        animal.sleep();  // Inherited method
    }
}
```

**Output:**

```
=== Runtime Polymorphism Demo ===

Dog:
Dog barks: Woof! Woof!
Animal is sleeping

Cat:
Cat meows: Meow! Meow!
Animal is sleeping

Cow:
Cow moos: Moo! Moo!
Animal is sleeping
```

**Example 12.3: Dynamic Method Dispatch**

```java
// DynamicMethodDispatch.java
class Shape {
    void draw() {
        System.out.println("Drawing a shape");
    }

    void erase() {
        System.out.println("Erasing a shape");
    }
}

class Circle extends Shape {
    @Override
    void draw() {
        System.out.println("Drawing a Circle ⭕");
    }
}

class Rectangle extends Shape {
    @Override
    void draw() {
        System.out.println("Drawing a Rectangle ▭");
    }
}

class Triangle extends Shape {
    @Override
    void draw() {
        System.out.println("Drawing a Triangle △");
    }
}

public class DynamicMethodDispatch {
    public static void main(String[] args) {
        System.out.println("=== Dynamic Method Dispatch Demo ===\n");

        Shape shape;  // Parent reference

        // Array of shapes
        Shape[] shapes = new Shape[3];
        shapes[0] = new Circle();
        shapes[1] = new Rectangle();
        shapes[2] = new Triangle();

        // Dynamic method dispatch in loop
        for (int i = 0; i < shapes.length; i++) {
            shapes[i].draw();  // Method decided at runtime
        }

        System.out.println("\n--- Changing shapes dynamically ---\n");

        shape = new Circle();
        shape.draw();

        shape = new Rectangle();
        shape.draw();

        shape = new Triangle();
        shape.draw();
    }
}
```

**Output:**

```
=== Dynamic Method Dispatch Demo ===

Drawing a Circle ⭕
Drawing a Rectangle ▭
Drawing a Triangle △

--- Changing shapes dynamically ---

Drawing a Circle ⭕
Drawing a Rectangle ▭
Drawing a Triangle △
```

**Example 12.4: instanceof Operator and Safe Downcasting**

```java
// InstanceofDemo.java
class Vehicle {
    void start() {
        System.out.println("Vehicle is starting");
    }
}

class Car extends Vehicle {
    void playMusic() {
        System.out.println("Playing music in car 🎵");
    }
}

class Bike extends Vehicle {
    void wheelie() {
        System.out.println("Doing a wheelie on bike 🏍️");
    }
}

public class InstanceofDemo {
    public static void main(String[] args) {
        System.out.println("=== instanceof Operator Demo ===\n");

        Vehicle v1 = new Car();
        Vehicle v2 = new Bike();

        // Check instance and perform safe downcasting
        System.out.println("v1 instanceof Car: " + (v1 instanceof Car));
        System.out.println("v1 instanceof Bike: " + (v1 instanceof Bike));
        System.out.println("v1 instanceof Vehicle: " + (v1 instanceof Vehicle));
        System.out.println();

        // Safe downcasting for Car
        if (v1 instanceof Car) {
            Car c = (Car) v1;
            c.start();
            c.playMusic();
        }
        System.out.println();

        // Safe downcasting for Bike
        if (v2 instanceof Bike) {
            Bike b = (Bike) v2;
            b.start();
            b.wheelie();
        }
        System.out.println();

        // Unsafe downcasting (will cause ClassCastException)
        System.out.println("--- Demonstrating unsafe cast ---");
        try {
            Bike b = (Bike) v1;  // v1 is actually a Car!
            b.wheelie();
        } catch (ClassCastException e) {
            System.out.println("Error: Cannot cast Car to Bike!");
        }
    }
}
```

**Output:**

```
=== instanceof Operator Demo ===

v1 instanceof Car: true
v1 instanceof Bike: false
v1 instanceof Vehicle: true

Vehicle is starting
Playing music in car 🎵

Vehicle is starting
Doing a wheelie on bike 🏍️

--- Demonstrating unsafe cast ---
Error: Cannot cast Car to Bike!
```

**Example 12.5: Real-World Polymorphism - Payment System**

```java
// PaymentSystemDemo.java
abstract class Payment {
    abstract void processPayment(double amount);

    void printReceipt() {
        System.out.println("Payment receipt generated");
    }
}

class CreditCardPayment extends Payment {
    @Override
    void processPayment(double amount) {
        System.out.println("Processing Credit Card payment of ₹" + amount);
        System.out.println("Card charged successfully 💳");
    }
}

class DebitCardPayment extends Payment {
    @Override
    void processPayment(double amount) {
        System.out.println("Processing Debit Card payment of ₹" + amount);
        System.out.println("Amount debited from account 💳");
    }
}

class UPIPayment extends Payment {
    @Override
    void processPayment(double amount) {
        System.out.println("Processing UPI payment of ₹" + amount);
        System.out.println("Payment sent via UPI 📱");
    }
}

class CashPayment extends Payment {
    @Override
    void processPayment(double amount) {
        System.out.println("Processing Cash payment of ₹" + amount);
        System.out.println("Cash received 💵");
    }
}

public class PaymentSystemDemo {
    // Polymorphic method - accepts any Payment type
    static void makePayment(Payment payment, double amount) {
        payment.processPayment(amount);
        payment.printReceipt();
        System.out.println("-------------------");
    }

    public static void main(String[] args) {
        System.out.println("=== Payment System (Polymorphism) ===\n");

        // Different payment methods
        Payment payment;

        payment = new CreditCardPayment();
        makePayment(payment, 5000);

        payment = new DebitCardPayment();
        makePayment(payment, 3000);

        payment = new UPIPayment();
        makePayment(payment, 1500);

        payment = new CashPayment();
        makePayment(payment, 500);
    }
}
```

**Output:**

```
=== Payment System (Polymorphism) ===

Processing Credit Card payment of ₹5000.0
Card charged successfully 💳
Payment receipt generated
-------------------
Processing Debit Card payment of ₹3000.0
Amount debited from account 💳
Payment receipt generated
-------------------
Processing UPI payment of ₹1500.0
Payment sent via UPI 📱
Payment receipt generated
-------------------
Processing Cash payment of ₹500.0
Cash received 💵
Payment receipt generated
-------------------
```

### 🎯 Key Takeaways

- Polymorphism means "many forms" - one interface, multiple implementations
- Compile-time polymorphism achieved through method overloading
- Runtime polymorphism achieved through method overriding
- Dynamic method dispatch resolves method calls at runtime
- Upcasting is automatic, downcasting requires explicit casting
- Use `instanceof` operator for safe downcasting
- Polymorphism enables writing flexible and maintainable code

### 📝 Practice Questions

1. What is the difference between compile-time and runtime polymorphism?
2. Can we achieve polymorphism without inheritance?
3. What is dynamic method dispatch?
4. Write a program demonstrating polymorphism with Employee hierarchy.
5. Why is runtime polymorphism slower than compile-time polymorphism?

---

## Chapter 13: Encapsulation

### 📘 Theory

#### **13.1 What is Encapsulation?**

**Encapsulation** is the process of wrapping data (variables) and code (methods) together as a single unit, and restricting direct access to some of the object's components. It is one of the four fundamental pillars of Object-Oriented Programming (OOP).

**Detailed Explanation:**

Encapsulation is a protective mechanism that prevents the data from being accessed by code outside the class. It binds the data and the methods that manipulate the data together, and keeps both safe from outside interference and misuse.

The main idea behind encapsulation is to hide the internal state of an object and require all interaction to be performed through an object's methods. This is also known as **data hiding**.

**Real-World Analogy:**

Think of a **capsule** (medicine):

- The medicine (data) is wrapped inside the capsule (class)
- You don't see what's inside the capsule
- You can't directly access or modify the medicine
- You just swallow it and it works
- The capsule protects the medicine from external factors
- Similarly, data is hidden inside a class and accessed only through controlled methods

**Another Analogy - ATM Machine:**

- **Internal mechanism** (private data) - You can't see or access the cash storage, card reader mechanism
- **Interface** (public methods) - You interact through buttons, screen (withdraw, deposit, check balance)
- **Controlled access** - You can only perform allowed operations
- **Security** - Your account details are protected

**Key Concepts:**

**1. Data Hiding:**

- Hide internal details from the outside world
- Make variables private
- Prevent direct access to data

**2. Controlled Access:**

- Provide public methods (getters/setters) to access private data
- Add validation and business logic in these methods
- Control how data is read and modified

**3. Abstraction:**

- Show only essential features
- Hide implementation details
- Provide a clean interface

**Why Encapsulation is Important:**

**1. Data Security and Protection:**

```java
class BankAccount {
    private double balance;  // Protected from direct access

    public void deposit(double amount) {
        if (amount > 0) {  // Validation
            balance += amount;
        }
    }

    public boolean withdraw(double amount) {
        if (amount > 0 && amount <= balance) {  // Validation
            balance -= amount;
            return true;
        }
        return false;
    }
}

// Without encapsulation (BAD):
// account.balance = -1000;  // Can set invalid value!

// With encapsulation (GOOD):
// account.withdraw(1000);  // Validated withdrawal
```

**2. Flexibility and Maintainability:**

```java
class Employee {
    private double salary;

    // Can change implementation without affecting users
    public double getSalary() {
        // Version 1: return salary;
        // Version 2: return salary with tax deduction
        return salary * 0.9;  // 10% tax
    }
}
```

**3. Control Over Data:**

```java
class Student {
    private int age;

    public void setAge(int age) {
        // Validation - age must be between 5 and 100
        if (age >= 5 && age <= 100) {
            this.age = age;
        } else {
            System.out.println("Invalid age!");
        }
    }
}
```

**Benefits of Encapsulation:**

- ✅ **Data Security** - Protect data from unauthorized access and modification
- ✅ **Flexibility** - Change implementation without affecting code that uses the class
- ✅ **Maintainability** - Easy to maintain and modify code
- ✅ **Reusability** - Encapsulated code can be reused in different contexts
- ✅ **Testing** - Easy to test individual components in isolation
- ✅ **Control** - Full control over what values can be stored in fields
- ✅ **Read-Only/Write-Only** - Can create read-only or write-only properties
- ✅ **Debugging** - Easier to track where data is being modified

**Encapsulation vs Data Hiding:**

| Aspect             | Encapsulation                            | Data Hiding             |
| ------------------ | ---------------------------------------- | ----------------------- |
| **Definition**     | Bundling data and methods                | Hiding internal details |
| **Scope**          | Broader concept                          | Part of encapsulation   |
| **Purpose**        | Organize code, control access            | Protect data            |
| **Implementation** | Class with private data + public methods | Private access modifier |

**Real-World Examples:**

**1. Television:**

- **Hidden:** Internal circuits, components
- **Exposed:** Remote control buttons (power, volume, channel)
- You don't need to know how TV works internally

**2. Car:**

- **Hidden:** Engine mechanics, transmission system
- **Exposed:** Steering wheel, pedals, gear shift
- You drive without knowing engine details

**3. Mobile Phone:**

- **Hidden:** Hardware components, OS internals
- **Exposed:** Touchscreen, apps, buttons
- You use apps without knowing how they work internally

#### **13.2 How to Achieve Encapsulation?**

**Steps:**

1. Declare variables as **private**
2. Provide **public getter** methods to read values
3. Provide **public setter** methods to write values
4. Add validation logic in setter methods

**Example:**

```java
class Student {
    // Private variables (data hiding)
    private int rollNo;
    private String name;
    private int age;

    // Public getter for rollNo
    public int getRollNo() {
        return rollNo;
    }

    // Public setter for rollNo
    public void setRollNo(int rollNo) {
        this.rollNo = rollNo;
    }

    // Public getter for name
    public String getName() {
        return name;
    }

    // Public setter for name with validation
    public void setName(String name) {
        if (name != null && !name.isEmpty()) {
            this.name = name;
        }
    }

    // Public getter for age
    public int getAge() {
        return age;
    }

    // Public setter for age with validation
    public void setAge(int age) {
        if (age > 0 && age < 100) {
            this.age = age;
        }
    }
}
```

#### **13.3 Access Modifiers**

Access modifiers control the visibility of classes, variables, methods, and constructors.

**Four Types:**

| Modifier                  | Class | Package | Subclass | World |
| ------------------------- | ----- | ------- | -------- | ----- |
| **public**                | ✅    | ✅      | ✅       | ✅    |
| **protected**             | ✅    | ✅      | ✅       | ❌    |
| **default** (no modifier) | ✅    | ✅      | ❌       | ❌    |
| **private**               | ✅    | ❌      | ❌       | ❌    |

**Detailed Explanation:**

**1. public**

- Accessible from anywhere
- No restrictions

```java
public class MyClass {
    public int x = 10;
    public void display() { }
}
```

**2. private**

- Accessible only within the same class
- Most restrictive

```java
class MyClass {
    private int x = 10;
    private void display() { }
}
```

**3. protected**

- Accessible within same package
- Accessible in subclasses (even in different packages)

```java
class MyClass {
    protected int x = 10;
    protected void display() { }
}
```

**4. default (package-private)**

- No modifier specified
- Accessible only within same package

```java
class MyClass {
    int x = 10;  // default access
    void display() { }  // default access
}
```

#### **13.4 Getter and Setter Methods**

**Getter Methods (Accessors):**

- Used to **read** private variables
- Naming convention: `get` + VariableName
- Return type: Same as variable type

```java
public int getAge() {
    return age;
}
```

**Setter Methods (Mutators):**

- Used to **write** private variables
- Naming convention: `set` + VariableName
- Return type: void
- Can include validation logic

```java
public void setAge(int age) {
    if (age > 0) {
        this.age = age;
    }
}
```

**Why Use Getters and Setters?**

- **Validation** - Check data before setting
- **Read-only** - Provide getter without setter
- **Write-only** - Provide setter without getter
- **Computed values** - Calculate value in getter
- **Debugging** - Add logging in getters/setters

#### **13.5 Read-Only and Write-Only Classes**

**Read-Only Class:**
Only getters, no setters (immutable after creation).

```java
class ReadOnlyStudent {
    private final int rollNo;
    private final String name;

    public ReadOnlyStudent(int rollNo, String name) {
        this.rollNo = rollNo;
        this.name = name;
    }

    public int getRollNo() {
        return rollNo;
    }

    public String getName() {
        return name;
    }

    // No setters - read-only
}
```

**Write-Only Class:**
Only setters, no getters (rare in practice).

```java
class WriteOnlyLogger {
    private String message;

    public void setMessage(String message) {
        this.message = message;
        // Log to file
    }

    // No getter - write-only
}
```

#### **13.6 Advantages of Encapsulation**

1. **Data Hiding** - Internal implementation is hidden
2. **Increased Flexibility** - Change implementation without affecting users
3. **Reusability** - Encapsulated code can be reused
4. **Easy Testing** - Test individual components
5. **Security** - Protect data from unauthorized access
6. **Maintainability** - Easy to maintain and modify

#### **13.7 Encapsulation vs Abstraction**

| Feature            | Encapsulation                      | Abstraction                   |
| ------------------ | ---------------------------------- | ----------------------------- |
| **Definition**     | Wrapping data and methods          | Hiding implementation details |
| **Focus**          | Data hiding                        | Implementation hiding         |
| **Implementation** | Private variables + public methods | Abstract classes/interfaces   |
| **Level**          | Class level                        | Design level                  |
| **Purpose**        | Data security                      | Reduce complexity             |
| **Example**        | Getters/Setters                    | Abstract methods              |

### 💻 Practical Examples

**Example 13.1: Basic Encapsulation**

```java
// BasicEncapsulation.java
class BankAccount {
    // Private variables (data hiding)
    private String accountNumber;
    private String accountHolder;
    private double balance;

    // Constructor
    public BankAccount(String accountNumber, String accountHolder, double initialBalance) {
        this.accountNumber = accountNumber;
        this.accountHolder = accountHolder;
        this.balance = initialBalance;
    }

    // Getter for accountNumber
    public String getAccountNumber() {
        return accountNumber;
    }

    // Getter for accountHolder
    public String getAccountHolder() {
        return accountHolder;
    }

    // Getter for balance
    public double getBalance() {
        return balance;
    }

    // Method to deposit money (controlled access)
    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            System.out.println("Deposited: ₹" + amount);
        } else {
            System.out.println("Invalid deposit amount");
        }
    }

    // Method to withdraw money (controlled access with validation)
    public void withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            System.out.println("Withdrawn: ₹" + amount);
        } else {
            System.out.println("Invalid withdrawal amount or insufficient balance");
        }
    }

    // Display account details
    public void displayAccountInfo() {
        System.out.println("Account Number: " + accountNumber);
        System.out.println("Account Holder: " + accountHolder);
        System.out.println("Balance: ₹" + balance);
    }
}

public class BasicEncapsulation {
    public static void main(String[] args) {
        System.out.println("=== Basic Encapsulation Demo ===\n");

        BankAccount account = new BankAccount("ACC001", "Rajesh Kumar", 10000);

        account.displayAccountInfo();
        System.out.println();

        account.deposit(5000);
        account.withdraw(3000);
        System.out.println();

        account.displayAccountInfo();
        System.out.println();

        // Try invalid operations
        account.deposit(-500);
        account.withdraw(20000);
    }
}
```

**Output:**

```
=== Basic Encapsulation Demo ===

Account Number: ACC001
Account Holder: Rajesh Kumar
Balance: ₹10000.0

Deposited: ₹5000.0
Withdrawn: ₹3000.0

Account Number: ACC001
Account Holder: Rajesh Kumar
Balance: ₹12000.0

Invalid deposit amount
Invalid withdrawal amount or insufficient balance
```

**Example 13.2: Encapsulation with Validation**

```java
// EncapsulationWithValidation.java
class Employee {
    private int empId;
    private String name;
    private int age;
    private double salary;

    // Getter and Setter for empId
    public int getEmpId() {
        return empId;
    }

    public void setEmpId(int empId) {
        if (empId > 0) {
            this.empId = empId;
        } else {
            System.out.println("Invalid Employee ID");
        }
    }

    // Getter and Setter for name
    public String getName() {
        return name;
    }

    public void setName(String name) {
        if (name != null && !name.trim().isEmpty()) {
            this.name = name;
        } else {
            System.out.println("Invalid Name");
        }
    }

    // Getter and Setter for age
    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        if (age >= 18 && age <= 65) {
            this.age = age;
        } else {
            System.out.println("Invalid Age (must be between 18 and 65)");
        }
    }

    // Getter and Setter for salary
    public double getSalary() {
        return salary;
    }

    public void setSalary(double salary) {
        if (salary >= 0) {
            this.salary = salary;
        } else {
            System.out.println("Invalid Salary");
        }
    }

    // Display employee details
    public void displayEmployee() {
        System.out.println("Employee ID: " + empId);
        System.out.println("Name: " + name);
        System.out.println("Age: " + age);
        System.out.println("Salary: ₹" + salary);
    }
}

public class EncapsulationWithValidation {
    public static void main(String[] args) {
        System.out.println("=== Encapsulation with Validation Demo ===\n");

        Employee emp = new Employee();

        // Valid data
        emp.setEmpId(101);
        emp.setName("Amit Sharma");
        emp.setAge(30);
        emp.setSalary(50000);

        emp.displayEmployee();
        System.out.println();

        // Invalid data
        System.out.println("--- Testing Validation ---");
        emp.setEmpId(-5);
        emp.setName("");
        emp.setAge(70);
        emp.setSalary(-1000);
    }
}
```

**Output:**

```
=== Encapsulation with Validation Demo ===

Employee ID: 101
Name: Amit Sharma
Age: 30
Salary: ₹50000.0

--- Testing Validation ---
Invalid Employee ID
Invalid Name
Invalid Age (must be between 18 and 65)
Invalid Salary
```

### 🎯 Key Takeaways

- Encapsulation wraps data and methods together as a single unit
- Achieved by making variables private and providing public getters/setters
- Access modifiers control visibility: public, private, protected, default
- Getters read data, setters write data with validation
- Encapsulation provides data security, flexibility, and maintainability
- Read-only classes have only getters, write-only classes have only setters

### 📝 Practice Questions

1. What is encapsulation and why is it important?
2. What are the four access modifiers in Java?
3. What is the difference between encapsulation and abstraction?
4. Write a class `Product` with private fields and public getters/setters.
5. How can you create a read-only class in Java?

---

## Chapter 14: Abstraction

### 📘 Theory

#### **14.1 What is Abstraction?**

**Abstraction** is the process of hiding implementation details and showing only essential features and functionality to the user. It is one of the four fundamental pillars of Object-Oriented Programming (OOP), along with Encapsulation, Inheritance, and Polymorphism.

**Detailed Explanation:**

Abstraction focuses on **what** an object does rather than **how** it does it. It allows you to create a simple interface for complex systems by hiding the internal complexity and exposing only the necessary parts.

In Java, abstraction is achieved through:

1. **Abstract Classes** - Classes that cannot be instantiated and may contain abstract methods
2. **Interfaces** - Contracts that define what a class must do, but not how

**Real-World Analogy:**

Think of a **car**:

- **What you see (Abstract Interface):**

  - Steering wheel - Turn left/right
  - Accelerator pedal - Speed up
  - Brake pedal - Slow down/stop
  - Gear shift - Change gears

- **What you don't see (Hidden Implementation):**
  - How the engine combusts fuel
  - How the transmission works
  - How the braking system operates
  - How the steering mechanism functions

You know **what** each control does, but you don't need to know **how** it works internally. This is abstraction!

**Another Analogy - Mobile Phone:**

- **Abstract Interface:** Touch screen, buttons, apps
- **Hidden Implementation:** Circuit boards, processors, memory chips, operating system code

You use apps without knowing how they're programmed internally.

**Another Analogy - ATM Machine:**

- **What you do:** Insert card, enter PIN, select transaction, withdraw money
- **What's hidden:** Database queries, network communication, cash dispensing mechanism, security protocols

**Programming Example:**

```java
// Abstract concept: "Payment"
// You know you can make a payment, but implementation varies

abstract class Payment {
    abstract void processPayment(double amount);  // What to do
    // How to do it? - Implemented by subclasses
}

class CreditCardPayment extends Payment {
    void processPayment(double amount) {
        // HOW: Credit card processing logic
        System.out.println("Processing credit card payment: $" + amount);
    }
}

class UPIPayment extends Payment {
    void processPayment(double amount) {
        // HOW: UPI processing logic
        System.out.println("Processing UPI payment: $" + amount);
    }
}

// User knows WHAT (processPayment), not HOW (implementation details)
```

**Key Concepts:**

**1. Abstract Class:**

- A class declared with `abstract` keyword
- Cannot be instantiated (cannot create objects)
- May contain abstract methods (without body)
- May contain concrete methods (with body)
- Used to define common behavior for subclasses

**2. Abstract Method:**

- A method declared without implementation (no body)
- Must be implemented by subclasses
- Declared with `abstract` keyword
- Ends with semicolon (no curly braces)

**3. Interface:**

- A contract that defines what a class must do
- 100% abstract (before Java 8)
- All methods are public and abstract by default
- Can have default and static methods (Java 8+)

**4. Concrete Class:**

- A regular class that provides implementation
- Can be instantiated
- Must implement all abstract methods from parent

**Abstraction vs Encapsulation:**

| Aspect          | Abstraction                  | Encapsulation                         |
| --------------- | ---------------------------- | ------------------------------------- |
| **Focus**       | Hide complexity (HOW)        | Hide data (WHAT)                      |
| **Purpose**     | Show only essential features | Protect data from unauthorized access |
| **Level**       | Design level                 | Implementation level                  |
| **Achieved by** | Abstract classes, Interfaces | Private variables, public methods     |
| **Example**     | Car interface (drive, brake) | BankAccount (private balance)         |

**Why Abstraction is Important:**

**1. Reduces Complexity:**

```java
// User doesn't need to know complex sorting algorithm
List<Integer> numbers = new ArrayList<>();
Collections.sort(numbers);  // Simple interface, complex implementation hidden
```

**2. Increases Security:**

```java
// Database connection details are hidden
abstract class Database {
    abstract void connect();  // User knows what, not how
}
```

**3. Code Reusability:**

```java
// Common behavior defined once, reused by many
abstract class Shape {
    abstract double area();  // All shapes have area, but calculated differently
}
```

**4. Flexibility:**

```java
// Easy to add new payment methods without changing existing code
abstract class Payment {
    abstract void pay();
}
// Add new: BitcoinPayment, PayPalPayment, etc.
```

**Benefits of Abstraction:**

- ✅ **Reduces Complexity** - Hide unnecessary details, show only what's needed
- ✅ **Increases Security** - Hide sensitive implementation details
- ✅ **Code Reusability** - Define common behavior once, use in multiple places
- ✅ **Flexibility** - Easy to change implementation without affecting users
- ✅ **Maintainability** - Easier to maintain and update code
- ✅ **Loose Coupling** - Reduces dependencies between components
- ✅ **Focus on Interface** - Developers focus on what to do, not how
- ✅ **Parallel Development** - Multiple teams can work on different implementations

**Real-World Examples:**

**1. Email System:**

- **Abstract:** Send email, receive email, delete email
- **Hidden:** SMTP protocol, server communication, encryption

**2. Database:**

- **Abstract:** Insert, update, delete, select
- **Hidden:** File storage, indexing, query optimization

**3. Operating System:**

- **Abstract:** Open file, save file, print document
- **Hidden:** Disk I/O, memory management, device drivers

**4. Web Browser:**

- **Abstract:** Enter URL, click links, view pages
- **Hidden:** HTTP requests, HTML parsing, rendering engine

**Levels of Abstraction:**

```
High Level (More Abstract)
    ↑
    │  User Interface (What user sees)
    │  Application Layer (Business logic)
    │  Service Layer (Abstract operations)
    │  Data Access Layer (Database operations)
    │  Database (Storage details)
    ↓
Low Level (More Concrete)
```

**When to Use Abstraction:**

1. **Common behavior across multiple classes**

   - Define abstract class with common methods

2. **Multiple implementations of same concept**

   - Use interface or abstract class

3. **Hide complex implementation**

   - Provide simple abstract interface

4. **Future extensibility**
   - Design for adding new implementations later

#### **14.2 Abstract Class**

**Definition:** A class declared with `abstract` keyword that cannot be instantiated and may contain abstract methods.

**Syntax:**

```java
abstract class ClassName {
    // Abstract method (no body)
    abstract void methodName();

    // Concrete method (with body)
    void concreteMethod() {
        // Implementation
    }
}
```

**Key Points:**

- Cannot create objects of abstract class
- Can have abstract and non-abstract methods
- Can have constructors
- Can have instance variables
- Can have static methods
- Must be inherited by subclass
- Subclass must implement all abstract methods (or be abstract itself)

**Example:**

```java
abstract class Animal {
    String name;

    // Constructor
    Animal(String name) {
        this.name = name;
    }

    // Abstract method
    abstract void sound();

    // Concrete method
    void sleep() {
        System.out.println(name + " is sleeping");
    }
}

class Dog extends Animal {
    Dog(String name) {
        super(name);
    }

    // Must implement abstract method
    void sound() {
        System.out.println(name + " barks");
    }
}
```

#### **14.3 Abstract Methods**

**Definition:** A method declared with `abstract` keyword that has no body (no implementation).

**Rules:**

- Must be declared in abstract class or interface
- Cannot be `private`, `final`, or `static`
- Must be overridden in subclass
- No curly braces `{}`

**Syntax:**

```java
abstract returnType methodName(parameters);
```

**Example:**

```java
abstract class Shape {
    abstract double calculateArea();  // No implementation
    abstract double calculatePerimeter();  // No implementation
}

class Circle extends Shape {
    double radius;

    Circle(double radius) {
        this.radius = radius;
    }

    // Implement abstract methods
    double calculateArea() {
        return Math.PI * radius * radius;
    }

    double calculatePerimeter() {
        return 2 * Math.PI * radius;
    }
}
```

#### **14.4 Interface**

**Definition:** A reference type that contains only abstract methods and constants. It is a blueprint of a class.

**Syntax:**

```java
interface InterfaceName {
    // Abstract methods (public abstract by default)
    void method1();
    void method2();

    // Constants (public static final by default)
    int CONSTANT = 100;
}
```

**Key Points:**

- All methods are `public abstract` by default (before Java 8)
- All variables are `public static final` by default (constants)
- Cannot have constructors
- Cannot be instantiated
- Implemented using `implements` keyword
- A class can implement multiple interfaces (multiple inheritance)
- From Java 8: Can have default and static methods
- From Java 9: Can have private methods

**Example:**

```java
interface Drawable {
    void draw();  // public abstract by default
}

class Circle implements Drawable {
    public void draw() {
        System.out.println("Drawing Circle");
    }
}

class Rectangle implements Drawable {
    public void draw() {
        System.out.println("Drawing Rectangle");
    }
}
```

#### **14.5 Abstract Class vs Interface**

| Feature                  | Abstract Class                         | Interface                                    |
| ------------------------ | -------------------------------------- | -------------------------------------------- |
| **Keyword**              | `abstract`                             | `interface`                                  |
| **Methods**              | Can have abstract and concrete methods | Only abstract methods (before Java 8)        |
| **Variables**            | Can have any type of variables         | Only constants (public static final)         |
| **Constructor**          | Can have constructors                  | Cannot have constructors                     |
| **Access Modifiers**     | Can have any access modifier           | Methods are public by default                |
| **Multiple Inheritance** | Not supported (single inheritance)     | Supported (multiple interfaces)              |
| **Implementation**       | `extends` keyword                      | `implements` keyword                         |
| **When to Use**          | When classes share common behavior     | When unrelated classes share common behavior |
| **Speed**                | Faster                                 | Slower (requires extra indirection)          |

#### **14.6 Multiple Inheritance with Interfaces**

Java doesn't support multiple inheritance with classes (to avoid ambiguity), but supports it with interfaces.

**Example:**

```java
interface Printable {
    void print();
}

interface Showable {
    void show();
}

// Multiple inheritance
class Document implements Printable, Showable {
    public void print() {
        System.out.println("Printing document");
    }

    public void show() {
        System.out.println("Showing document");
    }
}
```

#### **14.7 Interface Inheritance**

An interface can extend another interface using `extends` keyword.

**Example:**

```java
interface Animal {
    void eat();
}

interface Mammal extends Animal {
    void walk();
}

class Dog implements Mammal {
    public void eat() {
        System.out.println("Dog is eating");
    }

    public void walk() {
        System.out.println("Dog is walking");
    }
}
```

#### **14.8 Default Methods in Interface (Java 8+)**

From Java 8, interfaces can have default methods with implementation.

**Syntax:**

```java
interface MyInterface {
    // Abstract method
    void abstractMethod();

    // Default method
    default void defaultMethod() {
        System.out.println("Default implementation");
    }
}
```

**Benefits:**

- Add new methods without breaking existing implementations
- Provide default behavior

**Example:**

```java
interface Vehicle {
    void start();

    default void stop() {
        System.out.println("Vehicle stopped");
    }
}

class Car implements Vehicle {
    public void start() {
        System.out.println("Car started");
    }

    // Can override default method (optional)
    public void stop() {
        System.out.println("Car stopped");
    }
}
```

#### **14.9 Static Methods in Interface (Java 8+)**

From Java 8, interfaces can have static methods.

**Example:**

```java
interface MathOperations {
    static int add(int a, int b) {
        return a + b;
    }

    static int multiply(int a, int b) {
        return a * b;
    }
}

// Usage
int sum = MathOperations.add(5, 3);
```

#### **14.10 When to Use Abstract Class vs Interface**

**Use Abstract Class When:**

- Classes share common code
- Need to declare non-static or non-final fields
- Need constructors
- Want to provide default behavior
- Related classes (IS-A relationship)

**Use Interface When:**

- Unrelated classes need to implement same methods
- Want to achieve multiple inheritance
- Want to specify behavior without implementation
- Define a contract (CAN-DO relationship)

### 💻 Practical Examples

**Example 14.1: Abstract Class**

```java
// AbstractClassDemo.java
abstract class BankAccount {
    protected String accountNumber;
    protected String accountHolder;
    protected double balance;

    // Constructor
    public BankAccount(String accountNumber, String accountHolder, double balance) {
        this.accountNumber = accountNumber;
        this.accountHolder = accountHolder;
        this.balance = balance;
    }

    // Abstract methods
    abstract void deposit(double amount);
    abstract void withdraw(double amount);
    abstract double calculateInterest();

    // Concrete method
    void displayBalance() {
        System.out.println("Account: " + accountNumber);
        System.out.println("Holder: " + accountHolder);
        System.out.println("Balance: ₹" + balance);
    }
}

class SavingsAccount extends BankAccount {
    private double interestRate = 4.5;

    public SavingsAccount(String accountNumber, String accountHolder, double balance) {
        super(accountNumber, accountHolder, balance);
    }

    @Override
    void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            System.out.println("Deposited ₹" + amount + " to Savings Account");
        }
    }

    @Override
    void withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            System.out.println("Withdrawn ₹" + amount + " from Savings Account");
        } else {
            System.out.println("Insufficient balance");
        }
    }

    @Override
    double calculateInterest() {
        return balance * interestRate / 100;
    }
}

class CurrentAccount extends BankAccount {
    private double overdraftLimit = 10000;

    public CurrentAccount(String accountNumber, String accountHolder, double balance) {
        super(accountNumber, accountHolder, balance);
    }

    @Override
    void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            System.out.println("Deposited ₹" + amount + " to Current Account");
        }
    }

    @Override
    void withdraw(double amount) {
        if (amount > 0 && amount <= (balance + overdraftLimit)) {
            balance -= amount;
            System.out.println("Withdrawn ₹" + amount + " from Current Account");
        } else {
            System.out.println("Exceeds overdraft limit");
        }
    }

    @Override
    double calculateInterest() {
        return 0;  // No interest for current account
    }
}

public class AbstractClassDemo {
    public static void main(String[] args) {
        System.out.println("=== Abstract Class Demo ===\n");

        BankAccount savings = new SavingsAccount("SA001", "Rajesh Kumar", 50000);
        savings.displayBalance();
        savings.deposit(10000);
        savings.withdraw(5000);
        System.out.println("Interest: ₹" + savings.calculateInterest());
        savings.displayBalance();

        System.out.println("\n" + "=".repeat(40) + "\n");

        BankAccount current = new CurrentAccount("CA001", "Priya Sharma", 20000);
        current.displayBalance();
        current.deposit(5000);
        current.withdraw(30000);  // Uses overdraft
        System.out.println("Interest: ₹" + current.calculateInterest());
        current.displayBalance();
    }
}
```

**Output:**

```
=== Abstract Class Demo ===

Account: SA001
Holder: Rajesh Kumar
Balance: ₹50000.0
Deposited ₹10000.0 to Savings Account
Withdrawn ₹5000.0 from Savings Account
Interest: ₹2475.0
Account: SA001
Holder: Rajesh Kumar
Balance: ₹55000.0

========================================

Account: CA001
Holder: Priya Sharma
Balance: ₹20000.0
Deposited ₹5000.0 to Current Account
Withdrawn ₹30000.0 from Current Account
Interest: ₹0.0
Account: CA001
Holder: Priya Sharma
Balance: ₹-5000.0
```

**Example 14.2: Interface**

```java
// InterfaceDemo.java
interface Drawable {
    void draw();
}

interface Colorable {
    void setColor(String color);
}

class Circle implements Drawable, Colorable {
    private String color;
    private double radius;

    public Circle(double radius) {
        this.radius = radius;
    }

    @Override
    public void draw() {
        System.out.println("Drawing a circle with radius " + radius);
    }

    @Override
    public void setColor(String color) {
        this.color = color;
        System.out.println("Circle color set to " + color);
    }
}

class Rectangle implements Drawable, Colorable {
    private String color;
    private double length, width;

    public Rectangle(double length, double width) {
        this.length = length;
        this.width = width;
    }

    @Override
    public void draw() {
        System.out.println("Drawing a rectangle " + length + "x" + width);
    }

    @Override
    public void setColor(String color) {
        this.color = color;
        System.out.println("Rectangle color set to " + color);
    }
}

public class InterfaceDemo {
    public static void main(String[] args) {
        System.out.println("=== Interface Demo ===\n");

        Circle circle = new Circle(5.0);
        circle.setColor("Red");
        circle.draw();

        System.out.println();

        Rectangle rectangle = new Rectangle(10.0, 5.0);
        rectangle.setColor("Blue");
        rectangle.draw();
    }
}
```

**Output:**

```
=== Interface Demo ===

Circle color set to Red
Drawing a circle with radius 5.0

Rectangle color set to Blue
Drawing a rectangle 10.0x5.0
```

### 🎯 Key Takeaways

- Abstraction hides implementation details and shows only essential features
- Abstract class cannot be instantiated and may contain abstract methods
- Abstract methods have no body and must be implemented by subclass
- Interface is a blueprint containing only abstract methods and constants
- A class can implement multiple interfaces (multiple inheritance)
- Use abstract class for related classes, interface for unrelated classes
- Java 8+ allows default and static methods in interfaces

### 📝 Practice Questions

1. What is abstraction and why is it important?
2. What is the difference between abstract class and interface?
3. Can an abstract class have a constructor? Why or why not?
4. Write an interface `Playable` with methods `play()` and `pause()`.
5. When should you use an abstract class vs an interface?

---

## Chapter 15: String Handling

### 📘 Theory

#### **15.1 What is a String?**

**String** is a sequence of characters. In Java, String is a class (not a primitive data type) that represents character strings. All string literals (like "Hello", "Java", "123") are implemented as instances of the String class.

**Detailed Explanation:**

A String is an object that represents a sequence of characters. Unlike primitive data types (int, char, boolean), String is a reference type that belongs to the `java.lang` package. Strings are one of the most commonly used classes in Java programming.

**Characteristics of String:**

1. **Immutable** - Once created, cannot be modified
2. **Final** - String class is declared as final (cannot be inherited)
3. **Implements Serializable** - Can be serialized
4. **Implements Comparable** - Can be compared with other strings
5. **Implements CharSequence** - Represents a sequence of characters

**Real-World Analogy:**

Think of a **string** like a **necklace of beads**:

- Each bead is a character ('H', 'e', 'l', 'l', 'o')
- The entire necklace is the string ("Hello")
- You can't change individual beads once the necklace is made (immutable)
- If you want different beads, you create a new necklace (new String object)
- Multiple people can look at the same necklace without changing it (thread-safe)

**Another Analogy - Printed Book:**

- Once a book is printed, you can't change the text (immutable)
- You can read it multiple times (reusable)
- If you want different content, you print a new book (new String)

**String in Memory:**

```
Memory Representation:
┌─────────────────────────────┐
│  String str = "Hello";      │
└─────────────────────────────┘
         │
         ↓
┌─────────────────────────────┐
│  String Pool (Heap Memory)  │
│  ┌─────────────────────┐    │
│  │  "Hello"            │    │
│  │  [H][e][l][l][o]    │    │
│  └─────────────────────┘    │
└─────────────────────────────┘
```

**Key Points:**

- **Package:** String is a class in `java.lang` package (automatically imported)
- **Immutable:** Strings are **immutable** (cannot be changed after creation)
- **String Pool:** String literals are stored in a special memory area called **String Pool**
- **Creation:** Strings can be created using literals or `new` keyword
- **Thread-Safe:** Immutability makes strings thread-safe
- **Most Used:** One of the most frequently used classes in Java

**Creating Strings:**

Java provides multiple ways to create String objects:

**1. Using String Literal (Recommended):**

```java
String str1 = "Hello";
String str2 = "Java";
String str3 = "Hello";  // Reuses existing "Hello" from String Pool
```

**Benefits:**

- Stored in String Pool (memory efficient)
- Reuses existing strings
- Faster creation

**2. Using `new` Keyword:**

```java
String str1 = new String("Hello");
String str2 = new String("Hello");  // Creates new object (not reused)
```

**Note:**

- Creates object in heap memory (not in String Pool)
- Always creates new object (even if same value exists)
- Less memory efficient

**3. Using Character Array:**

```java
char[] chars = {'H', 'e', 'l', 'l', 'o'};
String str = new String(chars);
System.out.println(str);  // Output: Hello
```

**4. Using Byte Array:**

```java
byte[] bytes = {72, 101, 108, 108, 111};  // ASCII values
String str = new String(bytes);
System.out.println(str);  // Output: Hello
```

**5. Using StringBuilder/StringBuffer:**

```java
StringBuilder sb = new StringBuilder("Hello");
String str = sb.toString();
```

**String Literal vs new String():**

| Aspect          | String Literal               | new String()                        |
| --------------- | ---------------------------- | ----------------------------------- |
| **Syntax**      | `String s = "Hello";`        | `String s = new String("Hello");`   |
| **Storage**     | String Pool                  | Heap Memory                         |
| **Memory**      | Efficient (reuses)           | Less efficient (creates new)        |
| **Performance** | Faster                       | Slower                              |
| **Comparison**  | `==` works for same literals | `==` doesn't work (use `.equals()`) |
| **Recommended** | ✅ Yes                       | ❌ Rarely needed                    |

**Example - String Pool:**

```java
String s1 = "Hello";        // Stored in String Pool
String s2 = "Hello";        // Reuses same object from pool
String s3 = new String("Hello");  // New object in heap

System.out.println(s1 == s2);      // true (same reference)
System.out.println(s1 == s3);      // false (different references)
System.out.println(s1.equals(s3)); // true (same content)
```

**Why Use Strings?**

1. **Text Processing** - Manipulate text data
2. **User Input** - Store user input from keyboard
3. **File Operations** - Read/write file paths and content
4. **Network Communication** - Send/receive data
5. **Database Operations** - Store and query text data
6. **Display Output** - Show messages to users

#### **15.2 String Immutability**

**Immutable** means once a String object is created, it cannot be changed. Any modification creates a new String object.

**Why Strings are Immutable?**

1. **Security** - Strings are used in network connections, file paths, etc.
2. **Thread Safety** - Immutable objects are thread-safe
3. **String Pool** - Allows string reuse and memory optimization
4. **Hashcode Caching** - Hashcode is cached for better performance

**Example:**

```java
String str = "Hello";
str.concat(" World");  // Creates new string, doesn't modify original
System.out.println(str);  // Output: Hello (unchanged)

str = str.concat(" World");  // Assign to variable to use new string
System.out.println(str);  // Output: Hello World
```

#### **15.3 String Pool (String Constant Pool)**

**String Pool** is a special memory region in the heap where Java stores string literals.

**How it works:**

1. When you create a string literal, JVM checks the pool
2. If string exists, reference is returned
3. If not, new string is created in pool

**Example:**

```java
String s1 = "Hello";  // Created in string pool
String s2 = "Hello";  // Reuses from pool
String s3 = new String("Hello");  // Created in heap (not pool)

System.out.println(s1 == s2);  // true (same reference)
System.out.println(s1 == s3);  // false (different reference)
System.out.println(s1.equals(s3));  // true (same content)
```

**Memory Diagram:**

```
String Pool (Heap):
┌─────────┐
│ "Hello" │ ← s1, s2 point here
└─────────┘

Heap:
┌─────────┐
│ "Hello" │ ← s3 points here (separate object)
└─────────┘
```

#### **15.4 String Comparison**

**Two ways to compare strings:**

**1. Using `==` operator**

- Compares **references** (memory addresses)
- Returns true only if both references point to same object

**2. Using `equals()` method**

- Compares **content** (character sequence)
- Returns true if content is same

**Example:**

```java
String s1 = "Hello";
String s2 = "Hello";
String s3 = new String("Hello");

System.out.println(s1 == s2);        // true (same reference)
System.out.println(s1 == s3);        // false (different reference)
System.out.println(s1.equals(s3));   // true (same content)
```

**Other Comparison Methods:**

```java
String s1 = "Hello";
String s2 = "hello";

s1.equals(s2);              // false (case-sensitive)
s1.equalsIgnoreCase(s2);    // true (case-insensitive)
s1.compareTo(s2);           // negative (s1 < s2 lexicographically)
s1.compareToIgnoreCase(s2); // 0 (equal ignoring case)
```

#### **15.5 Important String Methods**

**1. Length and Character Access:**

```java
String str = "Hello World";

str.length();           // 11
str.charAt(0);          // 'H'
str.charAt(6);          // 'W'
```

**2. String Searching:**

```java
String str = "Hello World";

str.indexOf('o');       // 4 (first occurrence)
str.lastIndexOf('o');   // 7 (last occurrence)
str.indexOf("World");   // 6
str.contains("World");  // true
str.startsWith("Hello"); // true
str.endsWith("World");  // true
```

**3. String Extraction:**

```java
String str = "Hello World";

str.substring(0, 5);    // "Hello"
str.substring(6);       // "World"
```

**4. String Modification (creates new string):**

```java
String str = "Hello World";

str.toLowerCase();      // "hello world"
str.toUpperCase();      // "HELLO WORLD"
str.trim();            // Removes leading/trailing spaces
str.replace('o', 'a'); // "Hella Warld"
str.replace("World", "Java"); // "Hello Java"
```

**5. String Splitting:**

```java
String str = "Java,Python,C++";
String[] languages = str.split(",");
// languages = ["Java", "Python", "C++"]
```

**6. String Concatenation:**

```java
String s1 = "Hello";
String s2 = "World";

s1 + " " + s2;          // "Hello World"
s1.concat(" ").concat(s2); // "Hello World"
```

**7. String Conversion:**

```java
String.valueOf(123);    // "123"
String.valueOf(true);   // "true"
String.valueOf(45.67);  // "45.67"

int num = Integer.parseInt("123");  // 123
double d = Double.parseDouble("45.67"); // 45.67
```

#### **15.6 StringBuilder Class**

**StringBuilder** is a mutable sequence of characters. Used when you need to modify strings frequently.

**Key Points:**

- **Mutable** - Can be modified without creating new objects
- **Not thread-safe** - Faster but not synchronized
- **Better performance** - For string concatenation in loops

**Common Methods:**

```java
StringBuilder sb = new StringBuilder("Hello");

sb.append(" World");     // "Hello World"
sb.insert(5, ",");       // "Hello, World"
sb.delete(5, 6);         // "Hello World"
sb.reverse();            // "dlroW olleH"
sb.replace(0, 5, "Hi");  // "Hi olleH"
sb.toString();           // Convert to String
```

**Example:**

```java
// Bad practice (creates many String objects)
String str = "";
for (int i = 0; i < 1000; i++) {
    str += i;  // Creates 1000 String objects
}

// Good practice (modifies same StringBuilder)
StringBuilder sb = new StringBuilder();
for (int i = 0; i < 1000; i++) {
    sb.append(i);  // Modifies same object
}
String result = sb.toString();
```

#### **15.7 StringBuffer Class**

**StringBuffer** is similar to StringBuilder but **thread-safe** (synchronized).

**Key Points:**

- **Mutable** - Can be modified
- **Thread-safe** - Synchronized methods
- **Slower** than StringBuilder due to synchronization

**When to use:**

- Use **StringBuilder** in single-threaded applications (faster)
- Use **StringBuffer** in multi-threaded applications (thread-safe)

**Example:**

```java
StringBuffer sb = new StringBuffer("Hello");
sb.append(" World");
sb.insert(5, ",");
String result = sb.toString();
```

#### **15.8 String vs StringBuilder vs StringBuffer**

| Feature           | String                     | StringBuilder                      | StringBuffer                      |
| ----------------- | -------------------------- | ---------------------------------- | --------------------------------- |
| **Mutability**    | Immutable                  | Mutable                            | Mutable                           |
| **Thread Safety** | Thread-safe (immutable)    | Not thread-safe                    | Thread-safe                       |
| **Performance**   | Slow (creates new objects) | Fast                               | Slower than StringBuilder         |
| **Memory**        | Uses more memory           | Uses less memory                   | Uses less memory                  |
| **When to Use**   | Few modifications          | Many modifications (single-thread) | Many modifications (multi-thread) |
| **Storage**       | String Pool + Heap         | Heap only                          | Heap only                         |

#### **15.9 String Formatting**

**Using `format()` method:**

```java
String name = "John";
int age = 25;
double salary = 50000.50;

String formatted = String.format("Name: %s, Age: %d, Salary: %.2f", name, age, salary);
// Output: Name: John, Age: 25, Salary: 50000.50
```

**Format Specifiers:**

- `%s` - String
- `%d` - Integer
- `%f` - Floating point
- `%c` - Character
- `%b` - Boolean
- `%n` - New line

#### **15.10 Common String Operations**

**1. Check if string is empty:**

```java
String str = "";
str.isEmpty();          // true
str.isBlank();          // true (Java 11+, checks whitespace too)
```

**2. Repeat string (Java 11+):**

```java
String str = "Hello";
str.repeat(3);          // "HelloHelloHello"
```

**3. Join strings:**

```java
String result = String.join(", ", "Java", "Python", "C++");
// "Java, Python, C++"
```

**4. Convert to character array:**

```java
String str = "Hello";
char[] chars = str.toCharArray();
// ['H', 'e', 'l', 'l', 'o']
```

### 💻 Practical Examples

**Example 15.1: String Basics and Comparison**

```java
// StringBasics.java
public class StringBasics {
    public static void main(String[] args) {
        System.out.println("=== String Basics Demo ===\n");

        // Creating strings
        String s1 = "Hello";              // String literal
        String s2 = "Hello";              // Reuses from pool
        String s3 = new String("Hello");  // New object in heap

        System.out.println("--- String Creation ---");
        System.out.println("s1: " + s1);
        System.out.println("s2: " + s2);
        System.out.println("s3: " + s3);
        System.out.println();

        // Reference comparison (==)
        System.out.println("--- Reference Comparison (==) ---");
        System.out.println("s1 == s2: " + (s1 == s2));  // true (same reference)
        System.out.println("s1 == s3: " + (s1 == s3));  // false (different reference)
        System.out.println();

        // Content comparison (equals)
        System.out.println("--- Content Comparison (equals) ---");
        System.out.println("s1.equals(s2): " + s1.equals(s2));  // true
        System.out.println("s1.equals(s3): " + s1.equals(s3));  // true
        System.out.println();

        // Case-insensitive comparison
        String s4 = "hello";
        System.out.println("--- Case-Insensitive Comparison ---");
        System.out.println("s1.equals(s4): " + s1.equals(s4));  // false
        System.out.println("s1.equalsIgnoreCase(s4): " + s1.equalsIgnoreCase(s4));  // true
        System.out.println();

        // Lexicographic comparison
        System.out.println("--- Lexicographic Comparison ---");
        System.out.println("s1.compareTo(s4): " + s1.compareTo(s4));  // negative
        System.out.println("s4.compareTo(s1): " + s4.compareTo(s1));  // positive
        System.out.println("s1.compareTo(s2): " + s1.compareTo(s2));  // 0
    }
}
```

**Output:**

```
=== String Basics Demo ===

--- String Creation ---
s1: Hello
s2: Hello
s3: Hello

--- Reference Comparison (==) ---
s1 == s2: true
s1 == s3: false

--- Content Comparison (equals) ---
s1.equals(s2): true
s1.equals(s3): true

--- Case-Insensitive Comparison ---
s1.equals(s4): false
s1.equalsIgnoreCase(s4): true

--- Lexicographic Comparison ---
s1.compareTo(s4): -32
s4.compareTo(s1): 32
s1.compareTo(s2): 0
```

**Example 15.2: String Methods**

```java
// StringMethods.java
public class StringMethods {
    public static void main(String[] args) {
        System.out.println("=== String Methods Demo ===\n");

        String str = "  Hello World from Java  ";

        // Length and character access
        System.out.println("--- Length and Character Access ---");
        System.out.println("Original: '" + str + "'");
        System.out.println("Length: " + str.length());
        System.out.println("Character at index 7: " + str.charAt(7));
        System.out.println();

        // Trimming
        System.out.println("--- Trimming ---");
        String trimmed = str.trim();
        System.out.println("Trimmed: '" + trimmed + "'");
        System.out.println("Length after trim: " + trimmed.length());
        System.out.println();

        // Case conversion
        System.out.println("--- Case Conversion ---");
        System.out.println("Uppercase: " + trimmed.toUpperCase());
        System.out.println("Lowercase: " + trimmed.toLowerCase());
        System.out.println();

        // Searching
        System.out.println("--- Searching ---");
        System.out.println("Contains 'World': " + trimmed.contains("World"));
        System.out.println("Starts with 'Hello': " + trimmed.startsWith("Hello"));
        System.out.println("Ends with 'Java': " + trimmed.endsWith("Java"));
        System.out.println("Index of 'World': " + trimmed.indexOf("World"));
        System.out.println("Index of 'o': " + trimmed.indexOf('o'));
        System.out.println("Last index of 'o': " + trimmed.lastIndexOf('o'));
        System.out.println();

        // Substring
        System.out.println("--- Substring ---");
        System.out.println("Substring(0, 5): " + trimmed.substring(0, 5));
        System.out.println("Substring(6): " + trimmed.substring(6));
        System.out.println();

        // Replacement
        System.out.println("--- Replacement ---");
        System.out.println("Replace 'World' with 'Universe': " + trimmed.replace("World", "Universe"));
        System.out.println("Replace 'o' with 'a': " + trimmed.replace('o', 'a'));
        System.out.println();

        // Splitting
        System.out.println("--- Splitting ---");
        String[] words = trimmed.split(" ");
        System.out.println("Words:");
        for (String word : words) {
            System.out.println("  - " + word);
        }
    }
}
```

**Output:**

```
=== String Methods Demo ===

--- Length and Character Access ---
Original: '  Hello World from Java  '
Length: 26
Character at index 7: o

--- Trimming ---
Trimmed: 'Hello World from Java'
Length after trim: 21

--- Case Conversion ---
Uppercase: HELLO WORLD FROM JAVA
Lowercase: hello world from java

--- Searching ---
Contains 'World': true
Starts with 'Hello': true
Ends with 'Java': true
Index of 'World': 6
Index of 'o': 4
Last index of 'o': 13

--- Substring ---
Substring(0, 5): Hello
Substring(6): World from Java

--- Replacement ---
Replace 'World' with 'Universe': Hello Universe from Java
Replace 'o' with 'a': Hella Warld fram Java

--- Splitting ---
Words:
  - Hello
  - World
  - from
  - Java
```

**Example 15.3: StringBuilder Performance**

```java
// StringBuilderDemo.java
public class StringBuilderDemo {
    public static void main(String[] args) {
        System.out.println("=== StringBuilder Demo ===\n");

        // Performance comparison
        System.out.println("--- Performance Test ---");

        // Using String concatenation (slow)
        long startTime = System.currentTimeMillis();
        String str = "";
        for (int i = 0; i < 10000; i++) {
            str += i;
        }
        long endTime = System.currentTimeMillis();
        System.out.println("String concatenation time: " + (endTime - startTime) + " ms");

        // Using StringBuilder (fast)
        startTime = System.currentTimeMillis();
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < 10000; i++) {
            sb.append(i);
        }
        String result = sb.toString();
        endTime = System.currentTimeMillis();
        System.out.println("StringBuilder time: " + (endTime - startTime) + " ms");
        System.out.println();

        // StringBuilder methods
        System.out.println("--- StringBuilder Methods ---");
        StringBuilder builder = new StringBuilder("Hello");
        System.out.println("Initial: " + builder);

        builder.append(" World");
        System.out.println("After append: " + builder);

        builder.insert(5, ",");
        System.out.println("After insert: " + builder);

        builder.delete(5, 6);
        System.out.println("After delete: " + builder);

        builder.reverse();
        System.out.println("After reverse: " + builder);

        builder.reverse();  // Reverse back
        builder.replace(0, 5, "Hi");
        System.out.println("After replace: " + builder);

        System.out.println("Length: " + builder.length());
        System.out.println("Capacity: " + builder.capacity());
    }
}
```

**Output:**

```
=== StringBuilder Demo ===

--- Performance Test ---
String concatenation time: 245 ms
StringBuilder time: 2 ms

--- StringBuilder Methods ---
Initial: Hello
After append: Hello World
After insert: Hello, World
After delete: Hello World
After reverse: dlroW olleH
After replace: Hi World
Length: 8
Capacity: 21
```

### 🎯 Key Takeaways

- Strings are immutable - any modification creates a new String object
- String literals are stored in String Pool for memory optimization
- Use `==` to compare references, `equals()` to compare content
- StringBuilder is mutable and faster for frequent modifications
- StringBuffer is thread-safe version of StringBuilder
- Use StringBuilder for single-threaded, StringBuffer for multi-threaded applications
- String class provides many useful methods for manipulation

### 📝 Practice Questions

1. What is String immutability and why are Strings immutable in Java?
2. What is the difference between `==` and `equals()` for String comparison?
3. Explain String Pool and how it works.
4. When should you use StringBuilder vs StringBuffer?
5. Write a program to reverse a string without using `reverse()` method.

---

## Chapter 16: Exception Handling

### 📘 Theory

#### **16.1 What is an Exception?**

**Exception** is an abnormal condition or unexpected event that disrupts the normal flow of program execution. When an exception occurs during runtime, the program terminates abnormally unless the exception is properly handled.

**Detailed Explanation:**

An exception is an object that represents an error or unexpected situation that occurs during program execution. When an exceptional condition arises, an exception object is created and "thrown" by the method where the error occurred. This exception can be "caught" and handled to prevent the program from crashing.

**Real-World Analogy:**

Think of **driving a car**:

- **Normal flow:** Drive smoothly on the road from point A to point B
- **Exception:** Flat tire, traffic jam, road block, engine failure
- **Exception handling:** Pull over safely, fix the tire, find alternate route, call mechanic
- **Without handling:** Crash or get stuck (program terminates)
- **With handling:** Resolve the issue and continue journey (program continues)

**Another Analogy - Restaurant Order:**

- **Normal flow:** Customer orders food → Chef cooks → Waiter serves
- **Exception:** Ingredient not available, chef is sick, power outage
- **Exception handling:** Suggest alternative dish, call backup chef, use generator
- **Result:** Customer still gets served (program continues)

**Why Do Exceptions Occur?**

1. **Invalid User Input** - User enters text instead of number
2. **Resource Unavailability** - File not found, network down, database offline
3. **Programming Errors** - Division by zero, null pointer access
4. **Hardware Failures** - Disk full, memory exhausted
5. **External Factors** - Network timeout, server not responding

**Types of Errors in Java:**

**1. Compile-Time Errors (Syntax Errors):**

- Caught by the compiler before program runs
- Must be fixed before compilation succeeds
- Examples: Missing semicolon, typos, wrong syntax

```java
// Compile-time error
int x = 10
System.out.println(x);  // Error: missing semicolon
```

**2. Runtime Errors (Exceptions):**

- Occur during program execution
- Can be handled using exception handling
- Examples: Division by zero, file not found

```java
// Runtime error
int x = 10 / 0;  // ArithmeticException at runtime
```

**3. Logical Errors:**

- Program compiles and runs but produces wrong results
- Hardest to detect and fix
- Examples: Wrong formula, incorrect algorithm

```java
// Logical error
int average = (a + b + c) / 2;  // Should divide by 3, not 2
```

**Common Exceptions in Java:**

| Exception                        | Description           | Example                        |
| -------------------------------- | --------------------- | ------------------------------ |
| `ArithmeticException`            | Division by zero      | `int x = 10 / 0;`              |
| `NullPointerException`           | Using null reference  | `String s = null; s.length();` |
| `ArrayIndexOutOfBoundsException` | Invalid array index   | `int[] arr = {1,2}; arr[5];`   |
| `NumberFormatException`          | Invalid number format | `Integer.parseInt("abc");`     |
| `FileNotFoundException`          | File not found        | `new FileReader("xyz.txt");`   |
| `IOException`                    | Input/Output error    | File read/write errors         |
| `ClassNotFoundException`         | Class not found       | `Class.forName("ABC");`        |
| `SQLException`                   | Database error        | Database connection issues     |

**What Happens When Exception Occurs?**

**Without Exception Handling:**

```java
public class Test {
    public static void main(String[] args) {
        System.out.println("Start");
        int result = 10 / 0;  // ArithmeticException
        System.out.println("End");  // This line never executes
    }
}

// Output:
// Start
// Exception in thread "main" java.lang.ArithmeticException: / by zero
// Program terminates abnormally
```

**With Exception Handling:**

```java
public class Test {
    public static void main(String[] args) {
        System.out.println("Start");
        try {
            int result = 10 / 0;  // Exception caught
        } catch (ArithmeticException e) {
            System.out.println("Cannot divide by zero");
        }
        System.out.println("End");  // This line executes
    }
}

// Output:
// Start
// Cannot divide by zero
// End
// Program continues normally
```

**Benefits of Exception Handling:**

1. **Prevents Program Crash** - Program continues execution
2. **Separates Error Handling Code** - Clean and readable code
3. **Provides Meaningful Error Messages** - Better debugging
4. **Maintains Normal Flow** - Program flow is not disrupted
5. **Centralized Error Handling** - Handle errors in one place
6. **Graceful Degradation** - Provide alternative solutions

**Exception vs Error:**

| Aspect            | Exception                 | Error                                |
| ----------------- | ------------------------- | ------------------------------------ |
| **Recoverable**   | Yes (can be handled)      | No (cannot be handled)               |
| **Caused by**     | Application logic         | System/JVM issues                    |
| **Examples**      | IOException, SQLException | OutOfMemoryError, StackOverflowError |
| **Should handle** | Yes                       | No (let JVM handle)                  |
| **Severity**      | Less severe               | Very severe                          |

#### **16.2 Exception Hierarchy**

All exception classes are subtypes of `java.lang.Exception` class.

```
                    Object
                      |
                  Throwable
                   /     \
              Error     Exception
                        /        \
                RuntimeException  IOException
                    |                  |
        (Unchecked Exceptions)  (Checked Exceptions)
```

**Key Classes:**

- **Throwable** - Root class for all errors and exceptions
- **Error** - Serious problems (OutOfMemoryError, StackOverflowError)
- **Exception** - Conditions that programs should catch
- **RuntimeException** - Unchecked exceptions
- **IOException** - Checked exceptions

#### **16.3 Types of Exceptions**

**1. Checked Exceptions**

- Checked at **compile-time**
- Must be handled using try-catch or throws
- Examples: IOException, SQLException, ClassNotFoundException

**2. Unchecked Exceptions (Runtime Exceptions)**

- Checked at **runtime**
- Not mandatory to handle
- Examples: NullPointerException, ArithmeticException, ArrayIndexOutOfBoundsException

**3. Errors**

- Serious problems beyond program control
- Should not be caught
- Examples: OutOfMemoryError, StackOverflowError

**Comparison:**

| Feature        | Checked Exception                | Unchecked Exception                       | Error             |
| -------------- | -------------------------------- | ----------------------------------------- | ----------------- |
| **Check Time** | Compile-time                     | Runtime                                   | Runtime           |
| **Handling**   | Mandatory                        | Optional                                  | Should not handle |
| **Examples**   | IOException, SQLException        | NullPointerException, ArithmeticException | OutOfMemoryError  |
| **Extends**    | Exception (not RuntimeException) | RuntimeException                          | Error             |

#### **16.4 Exception Handling Keywords**

Java provides five keywords for exception handling:

**1. try** - Block of code to monitor for exceptions
**2. catch** - Block to handle the exception
**3. finally** - Block that always executes
**4. throw** - Explicitly throw an exception
**5. throws** - Declare exceptions that method might throw

#### **16.5 try-catch Block**

**Syntax:**

```java
try {
    // Code that might throw exception
} catch (ExceptionType e) {
    // Handle exception
}
```

**Example:**

```java
try {
    int result = 10 / 0;  // ArithmeticException
} catch (ArithmeticException e) {
    System.out.println("Cannot divide by zero");
}
```

**Multiple catch blocks:**

```java
try {
    // Code
} catch (ArithmeticException e) {
    System.out.println("Arithmetic error");
} catch (NullPointerException e) {
    System.out.println("Null pointer error");
} catch (Exception e) {
    System.out.println("General error");
}
```

**Rules:**

- Specific exceptions must come before general exceptions
- Only one catch block executes
- Parent exception class should be at the end

#### **16.6 finally Block**

**finally** block always executes whether exception occurs or not. Used for cleanup code (closing files, database connections).

**Syntax:**

```java
try {
    // Code
} catch (Exception e) {
    // Handle exception
} finally {
    // Always executes
    // Cleanup code
}
```

**Example:**

```java
try {
    int result = 10 / 2;
    System.out.println("Result: " + result);
} catch (ArithmeticException e) {
    System.out.println("Error occurred");
} finally {
    System.out.println("Finally block always executes");
}
```

**When finally doesn't execute:**

- System.exit() is called
- Fatal error occurs (JVM crash)
- Thread is killed

#### **16.7 throw Keyword**

**throw** is used to explicitly throw an exception.

**Syntax:**

```java
throw new ExceptionType("Error message");
```

**Example:**

```java
public void checkAge(int age) {
    if (age < 18) {
        throw new ArithmeticException("Age must be 18 or above");
    } else {
        System.out.println("Valid age");
    }
}
```

**Key Points:**

- Can throw only one exception at a time
- Used with unchecked exceptions or custom exceptions
- Followed by exception object

#### **16.8 throws Keyword**

**throws** is used to declare exceptions that a method might throw. It delegates exception handling to the caller.

**Syntax:**

```java
returnType methodName() throws ExceptionType1, ExceptionType2 {
    // Code
}
```

**Example:**

```java
public void readFile() throws IOException {
    FileReader file = new FileReader("test.txt");
    // File operations
}

public void caller() {
    try {
        readFile();
    } catch (IOException e) {
        System.out.println("File error: " + e.getMessage());
    }
}
```

**throw vs throws:**

| Feature      | throw                      | throws              |
| ------------ | -------------------------- | ------------------- |
| **Purpose**  | Throw exception explicitly | Declare exception   |
| **Location** | Inside method body         | Method signature    |
| **Syntax**   | `throw new Exception()`    | `throws Exception`  |
| **Number**   | Single exception           | Multiple exceptions |
| **Type**     | Exception object           | Exception class     |

#### **16.9 Custom Exceptions**

You can create your own exception classes by extending `Exception` or `RuntimeException`.

**Syntax:**

```java
class CustomException extends Exception {
    public CustomException(String message) {
        super(message);
    }
}
```

**Example:**

```java
class InvalidAgeException extends Exception {
    public InvalidAgeException(String message) {
        super(message);
    }
}

public void validateAge(int age) throws InvalidAgeException {
    if (age < 18) {
        throw new InvalidAgeException("Age must be 18 or above");
    }
}
```

**When to create custom exceptions:**

- Business logic validation
- Domain-specific errors
- Better error messages
- Specific exception handling

#### **16.10 try-with-resources (Java 7+)**

Automatically closes resources that implement `AutoCloseable` interface.

**Syntax:**

```java
try (ResourceType resource = new ResourceType()) {
    // Use resource
} catch (Exception e) {
    // Handle exception
}
// Resource automatically closed
```

**Example:**

```java
try (FileReader fr = new FileReader("test.txt");
     BufferedReader br = new BufferedReader(fr)) {
    String line = br.readLine();
    System.out.println(line);
} catch (IOException e) {
    System.out.println("Error: " + e.getMessage());
}
// Files automatically closed
```

**Benefits:**

- Automatic resource management
- No need for finally block
- Cleaner code
- Prevents resource leaks

#### **16.11 Exception Propagation**

When an exception is not caught in a method, it propagates to the caller method.

**Example:**

```java
void method1() {
    int result = 10 / 0;  // Exception occurs
}

void method2() {
    method1();  // Exception propagates here
}

void method3() {
    try {
        method2();  // Exception caught here
    } catch (ArithmeticException e) {
        System.out.println("Exception handled");
    }
}
```

**Flow:**

1. Exception occurs in method1
2. Propagates to method2
3. Propagates to method3
4. Caught in method3's catch block

#### **16.12 Best Practices**

1. **Catch specific exceptions** - Don't catch generic Exception
2. **Don't ignore exceptions** - Always handle or log
3. **Use finally for cleanup** - Close resources
4. **Don't catch Error** - Let JVM handle
5. **Use custom exceptions** - For business logic
6. **Log exceptions** - For debugging
7. **Don't use exceptions for control flow** - Use if-else
8. **Provide meaningful messages** - Help debugging

### 💻 Practical Examples

**Example 16.1: Basic Exception Handling**

```java
// BasicExceptionHandling.java
public class BasicExceptionHandling {
    public static void main(String[] args) {
        System.out.println("=== Basic Exception Handling ===\n");

        // Example 1: ArithmeticException
        System.out.println("--- ArithmeticException ---");
        try {
            int result = 10 / 0;
            System.out.println("Result: " + result);
        } catch (ArithmeticException e) {
            System.out.println("Error: Cannot divide by zero");
            System.out.println("Exception: " + e.getMessage());
        }
        System.out.println();

        // Example 2: NullPointerException
        System.out.println("--- NullPointerException ---");
        try {
            String str = null;
            System.out.println(str.length());
        } catch (NullPointerException e) {
            System.out.println("Error: String is null");
            System.out.println("Exception: " + e.getMessage());
        }
        System.out.println();

        // Example 3: ArrayIndexOutOfBoundsException
        System.out.println("--- ArrayIndexOutOfBoundsException ---");
        try {
            int[] arr = {1, 2, 3};
            System.out.println(arr[5]);
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("Error: Invalid array index");
            System.out.println("Exception: " + e.getMessage());
        }
        System.out.println();

        // Example 4: NumberFormatException
        System.out.println("--- NumberFormatException ---");
        try {
            String str = "abc";
            int num = Integer.parseInt(str);
            System.out.println("Number: " + num);
        } catch (NumberFormatException e) {
            System.out.println("Error: Invalid number format");
            System.out.println("Exception: " + e.getMessage());
        }

        System.out.println("\nProgram continues after exception handling");
    }
}
```

**Output:**

```
=== Basic Exception Handling ===

--- ArithmeticException ---
Error: Cannot divide by zero
Exception: / by zero

--- NullPointerException ---
Error: String is null
Exception: null

--- ArrayIndexOutOfBoundsException ---
Error: Invalid array index
Exception: Index 5 out of bounds for length 3

--- NumberFormatException ---
Error: Invalid number format
Exception: For input string: "abc"

Program continues after exception handling
```

**Example 16.2: Multiple catch and finally**

```java
// MultipleCatchFinally.java
public class MultipleCatchFinally {
    public static void main(String[] args) {
        System.out.println("=== Multiple catch and finally ===\n");

        testException(1);  // ArithmeticException
        System.out.println();
        testException(2);  // NullPointerException
        System.out.println();
        testException(3);  // No exception
    }

    static void testException(int testCase) {
        System.out.println("Test Case: " + testCase);
        try {
            if (testCase == 1) {
                int result = 10 / 0;
            } else if (testCase == 2) {
                String str = null;
                str.length();
            } else {
                System.out.println("No exception");
            }
        } catch (ArithmeticException e) {
            System.out.println("Caught ArithmeticException: " + e.getMessage());
        } catch (NullPointerException e) {
            System.out.println("Caught NullPointerException");
        } catch (Exception e) {
            System.out.println("Caught general exception");
        } finally {
            System.out.println("Finally block always executes");
        }
    }
}
```

**Output:**

```
=== Multiple catch and finally ===

Test Case: 1
Caught ArithmeticException: / by zero
Finally block always executes

Test Case: 2
Caught NullPointerException
Finally block always executes

Test Case: 3
No exception
Finally block always executes
```

**Example 16.3: throw and throws**

```java
// ThrowThrowsDemo.java
public class ThrowThrowsDemo {

    // Method that throws exception
    static void checkAge(int age) throws Exception {
        if (age < 18) {
            throw new Exception("Age must be 18 or above");
        } else {
            System.out.println("Valid age: " + age);
        }
    }

    // Method that throws unchecked exception
    static void checkBalance(double balance) {
        if (balance < 1000) {
            throw new ArithmeticException("Insufficient balance");
        } else {
            System.out.println("Sufficient balance: ₹" + balance);
        }
    }

    public static void main(String[] args) {
        System.out.println("=== throw and throws Demo ===\n");

        // Example 1: throws with checked exception
        System.out.println("--- Checked Exception (throws) ---");
        try {
            checkAge(25);
            checkAge(15);
        } catch (Exception e) {
            System.out.println("Exception: " + e.getMessage());
        }
        System.out.println();

        // Example 2: throw with unchecked exception
        System.out.println("--- Unchecked Exception (throw) ---");
        try {
            checkBalance(5000);
            checkBalance(500);
        } catch (ArithmeticException e) {
            System.out.println("Exception: " + e.getMessage());
        }
    }
}
```

**Output:**

```
=== throw and throws Demo ===

--- Checked Exception (throws) ---
Valid age: 25
Exception: Age must be 18 or above

--- Unchecked Exception (throw) ---
Sufficient balance: ₹5000.0
Exception: Insufficient balance
```

**Example 16.4: Custom Exception**

```java
// CustomExceptionDemo.java

// Custom Exception Class
class InvalidAgeException extends Exception {
    public InvalidAgeException(String message) {
        super(message);
    }
}

class InsufficientBalanceException extends Exception {
    private double balance;
    private double required;

    public InsufficientBalanceException(double balance, double required) {
        super("Insufficient balance. Available: ₹" + balance + ", Required: ₹" + required);
        this.balance = balance;
        this.required = required;
    }

    public double getShortfall() {
        return required - balance;
    }
}

class BankAccount {
    private String accountNumber;
    private String holder;
    private double balance;

    public BankAccount(String accountNumber, String holder, double balance) {
        this.accountNumber = accountNumber;
        this.holder = holder;
        this.balance = balance;
    }

    public void withdraw(double amount) throws InsufficientBalanceException {
        if (amount > balance) {
            throw new InsufficientBalanceException(balance, amount);
        }
        balance -= amount;
        System.out.println("Withdrawn: ₹" + amount);
        System.out.println("Remaining balance: ₹" + balance);
    }

    public void displayBalance() {
        System.out.println("Account: " + accountNumber);
        System.out.println("Holder: " + holder);
        System.out.println("Balance: ₹" + balance);
    }
}

public class CustomExceptionDemo {

    static void validateAge(String name, int age) throws InvalidAgeException {
        if (age < 18) {
            throw new InvalidAgeException(name + " is underage. Age: " + age);
        }
        System.out.println(name + " is eligible. Age: " + age);
    }

    public static void main(String[] args) {
        System.out.println("=== Custom Exception Demo ===\n");

        // Example 1: InvalidAgeException
        System.out.println("--- Age Validation ---");
        try {
            validateAge("Rahul", 25);
            validateAge("Priya", 16);
        } catch (InvalidAgeException e) {
            System.out.println("Error: " + e.getMessage());
        }
        System.out.println();

        // Example 2: InsufficientBalanceException
        System.out.println("--- Bank Account ---");
        BankAccount account = new BankAccount("ACC001", "Amit Kumar", 5000);
        account.displayBalance();
        System.out.println();

        try {
            account.withdraw(3000);
            System.out.println();
            account.withdraw(5000);  // Will throw exception
        } catch (InsufficientBalanceException e) {
            System.out.println("Error: " + e.getMessage());
            System.out.println("Shortfall: ₹" + e.getShortfall());
        }
    }
}
```

**Output:**

```
=== Custom Exception Demo ===

--- Age Validation ---
Rahul is eligible. Age: 25
Error: Priya is underage. Age: 16

--- Bank Account ---
Account: ACC001
Holder: Amit Kumar
Balance: ₹5000.0

Withdrawn: ₹3000.0
Remaining balance: ₹2000.0

Error: Insufficient balance. Available: ₹2000.0, Required: ₹5000.0
Shortfall: ₹3000.0
```

### 🎯 Key Takeaways

- Exception is an abnormal event that disrupts program flow
- Checked exceptions must be handled, unchecked exceptions are optional
- try-catch-finally is used for exception handling
- throw is used to explicitly throw exception, throws declares exceptions
- finally block always executes (cleanup code)
- Custom exceptions provide domain-specific error handling
- try-with-resources automatically manages resources
- Always catch specific exceptions and provide meaningful messages

### 📝 Practice Questions

1. What is the difference between checked and unchecked exceptions?
2. Explain the difference between throw and throws keywords.
3. When does the finally block not execute?
4. How do you create a custom exception in Java?
5. Write a program to handle multiple exceptions using try-catch.

---

## Chapter 17: Collections Framework

### 📘 Theory

#### **17.1 What is Collections Framework?**

**Collections Framework** is a unified architecture for representing and manipulating collections (groups) of objects. It provides a set of interfaces, implementations (classes), and algorithms to store, retrieve, manipulate, and communicate aggregate data efficiently.

**Detailed Explanation:**

The Java Collections Framework is a comprehensive system that provides:

1. **Interfaces** - Abstract data types (List, Set, Map, Queue)
2. **Implementations** - Concrete classes (ArrayList, HashSet, HashMap)
3. **Algorithms** - Methods for searching, sorting, shuffling, etc.

Before the Collections Framework (Java 1.2), developers had to use arrays or legacy classes like Vector and Hashtable. The Collections Framework provides a modern, efficient, and standardized way to work with groups of objects.

**What is a Collection?**

A collection is simply a group of objects represented as a single unit. For example:

- A list of students
- A set of unique IDs
- A map of employee names and salaries
- A queue of print jobs

**Real-World Analogies:**

Think of **organizing items in different ways**:

**1. List (ArrayList, LinkedList):**

- **Shopping list** - Items in order, can have duplicates
- **To-do list** - Tasks in sequence
- **Playlist** - Songs in order, same song can appear multiple times
- **Characteristics:** Ordered, allows duplicates, index-based access

**2. Set (HashSet, TreeSet):**

- **Unique ID cards** - No two people have same ID
- **Set of playing cards** - Each card is unique
- **Email addresses** - No duplicate emails
- **Characteristics:** No duplicates, no guaranteed order (except TreeSet)

**3. Map (HashMap, TreeMap):**

- **Phone directory** - Name → Phone number
- **Dictionary** - Word → Definition
- **Student records** - Roll number → Student details
- **Characteristics:** Key-value pairs, unique keys, fast lookup

**4. Queue (PriorityQueue, LinkedList):**

- **Line at ticket counter** - First come, first served (FIFO)
- **Print queue** - Documents printed in order
- **Customer service queue** - Serve customers in sequence
- **Characteristics:** FIFO (First In First Out), ordered processing

**Why Use Collections Framework?**

**Before Collections (Using Arrays):**

```java
// Fixed size, manual resizing needed
String[] names = new String[10];
names[0] = "John";
names[1] = "Alice";
// What if we need to add 11th name? Create new array!
```

**With Collections (Using ArrayList):**

```java
// Dynamic size, automatic resizing
ArrayList<String> names = new ArrayList<>();
names.add("John");
names.add("Alice");
names.add("Bob");  // Can add unlimited items
```

**Benefits of Collections Framework:**

**1. Reduces Programming Effort:**

- Ready-to-use data structures
- No need to implement from scratch
- Focus on business logic, not data structure implementation

**2. Increases Performance:**

- Highly optimized implementations
- Efficient algorithms (sorting, searching)
- Better than custom implementations

**3. Provides Interoperability:**

- Common interface for different implementations
- Easy to switch between implementations
- Code works with any implementation

**4. Reduces Learning Effort:**

- Standard API across all collections
- Learn once, use everywhere
- Consistent method names and behavior

**5. Promotes Reusability:**

- Use existing implementations
- Don't reinvent the wheel
- Tested and proven code

**6. Type Safety (Generics):**

```java
// Type-safe collection
ArrayList<String> names = new ArrayList<>();
names.add("John");     // OK
// names.add(123);     // Compile error - only String allowed
```

**7. Rich Functionality:**

- Sorting, searching, shuffling
- Filtering, mapping, reducing
- Thread-safe versions available

**Collections Framework Components:**

**1. Interfaces (Contracts):**

- Define what operations are available
- Examples: List, Set, Map, Queue

**2. Implementations (Classes):**

- Provide actual functionality
- Examples: ArrayList, HashSet, HashMap

**3. Algorithms (Utility Methods):**

- Provided by Collections class
- Examples: sort(), shuffle(), reverse()

**Comparison: Array vs Collection:**

| Aspect            | Array                  | Collection                       |
| ----------------- | ---------------------- | -------------------------------- |
| **Size**          | Fixed                  | Dynamic (grows/shrinks)          |
| **Type**          | Primitive + Object     | Only Objects                     |
| **Performance**   | Faster (direct access) | Slightly slower                  |
| **Functionality** | Limited                | Rich (add, remove, search, sort) |
| **Type Safety**   | No generics            | Generics support                 |
| **Memory**        | Contiguous             | May be scattered                 |
| **Flexibility**   | Less flexible          | Highly flexible                  |

**When to Use Collections:**

1. **Unknown size** - Don't know how many elements
2. **Dynamic data** - Frequent additions/removals
3. **Rich operations** - Need sorting, searching, filtering
4. **Type safety** - Want compile-time type checking
5. **Standard API** - Want consistent interface

**Common Operations:**

```java
// Create collection
List<String> list = new ArrayList<>();

// Add elements
list.add("Apple");
list.add("Banana");

// Access elements
String first = list.get(0);

// Remove elements
list.remove("Apple");

// Check size
int size = list.size();

// Check if empty
boolean empty = list.isEmpty();

// Check if contains
boolean has = list.contains("Banana");

// Iterate
for (String item : list) {
    System.out.println(item);
}
```

#### **17.2 Collections Hierarchy**

```
                    Collection (Interface)
                    /        |         \
                   /         |          \
              List         Set          Queue
               |            |             |
          ArrayList    HashSet      PriorityQueue
          LinkedList   TreeSet      LinkedList
          Vector       LinkedHashSet

                    Map (Interface)
                         |
                    -----------
                   /     |     \
              HashMap  TreeMap  LinkedHashMap
              Hashtable
```

**Key Interfaces:**

- **Collection** - Root interface
- **List** - Ordered collection (allows duplicates)
- **Set** - Unordered collection (no duplicates)
- **Queue** - FIFO collection
- **Map** - Key-value pairs

#### **17.3 List Interface**

**List** is an ordered collection that allows duplicate elements. Elements can be accessed by index.

**Key Features:**

- Maintains insertion order
- Allows duplicate elements
- Allows null elements
- Index-based access (0, 1, 2, ...)

**Common Implementations:**

1. **ArrayList** - Dynamic array
2. **LinkedList** - Doubly linked list
3. **Vector** - Synchronized ArrayList

**Common Methods:**

```java
List<String> list = new ArrayList<>();

list.add("Apple");           // Add element
list.add(0, "Banana");       // Add at index
list.get(0);                 // Get element at index
list.set(0, "Mango");        // Replace element
list.remove(0);              // Remove by index
list.remove("Apple");        // Remove by object
list.size();                 // Get size
list.contains("Apple");      // Check if exists
list.clear();                // Remove all elements
```

#### **17.4 ArrayList**

**ArrayList** is a resizable array implementation of List interface.

**Key Features:**

- Dynamic size (grows automatically)
- Fast random access (O(1))
- Slow insertion/deletion in middle (O(n))
- Not synchronized (not thread-safe)
- Allows null elements

**Example:**

```java
ArrayList<String> fruits = new ArrayList<>();
fruits.add("Apple");
fruits.add("Banana");
fruits.add("Orange");

System.out.println(fruits.get(0));  // Apple
System.out.println(fruits.size());  // 3

for (String fruit : fruits) {
    System.out.println(fruit);
}
```

**When to use:**

- Frequent access by index
- Less insertion/deletion in middle
- Single-threaded environment

#### **17.5 LinkedList**

**LinkedList** is a doubly linked list implementation of List and Queue interfaces.

**Key Features:**

- Fast insertion/deletion (O(1) at ends)
- Slow random access (O(n))
- More memory (stores references)
- Not synchronized

**Example:**

```java
LinkedList<String> list = new LinkedList<>();
list.add("First");
list.addFirst("Start");
list.addLast("End");
list.removeFirst();
list.removeLast();
```

**When to use:**

- Frequent insertion/deletion
- Queue/Deque operations
- Less random access

**ArrayList vs LinkedList:**

| Feature                | ArrayList     | LinkedList                  |
| ---------------------- | ------------- | --------------------------- |
| **Structure**          | Dynamic array | Doubly linked list          |
| **Access Time**        | O(1)          | O(n)                        |
| **Insertion/Deletion** | O(n)          | O(1) at ends                |
| **Memory**             | Less          | More (stores references)    |
| **Use Case**           | Random access | Frequent insertion/deletion |

#### **17.6 Set Interface**

**Set** is a collection that does not allow duplicate elements.

**Key Features:**

- No duplicate elements
- At most one null element
- No index-based access
- Unordered (except TreeSet, LinkedHashSet)

**Common Implementations:**

1. **HashSet** - Hash table (unordered)
2. **LinkedHashSet** - Hash table + linked list (insertion order)
3. **TreeSet** - Red-black tree (sorted)

**Common Methods:**

```java
Set<String> set = new HashSet<>();

set.add("Apple");            // Add element
set.remove("Apple");         // Remove element
set.contains("Apple");       // Check if exists
set.size();                  // Get size
set.clear();                 // Remove all
```

#### **17.7 HashSet**

**HashSet** uses hash table for storage. Elements are unordered.

**Key Features:**

- No duplicates
- Unordered
- Fast operations (O(1))
- Allows one null
- Not synchronized

**Example:**

```java
HashSet<Integer> set = new HashSet<>();
set.add(10);
set.add(20);
set.add(10);  // Duplicate, not added

System.out.println(set);  // [20, 10] (unordered)
System.out.println(set.size());  // 2
```

**When to use:**

- Need unique elements
- Order doesn't matter
- Fast operations

#### **17.8 TreeSet**

**TreeSet** uses red-black tree. Elements are sorted in natural order or by Comparator.

**Key Features:**

- No duplicates
- Sorted order
- Slower than HashSet (O(log n))
- No null elements
- Not synchronized

**Example:**

```java
TreeSet<Integer> set = new TreeSet<>();
set.add(30);
set.add(10);
set.add(20);

System.out.println(set);  // [10, 20, 30] (sorted)
```

**When to use:**

- Need sorted elements
- Range operations (subSet, headSet, tailSet)

#### **17.9 Map Interface**

**Map** stores key-value pairs. Each key maps to exactly one value.

**Key Features:**

- Stores key-value pairs
- No duplicate keys
- Each key maps to one value
- Not part of Collection interface

**Common Implementations:**

1. **HashMap** - Hash table (unordered)
2. **LinkedHashMap** - Hash table + linked list (insertion order)
3. **TreeMap** - Red-black tree (sorted by keys)
4. **Hashtable** - Synchronized HashMap (legacy)

**Common Methods:**

```java
Map<String, Integer> map = new HashMap<>();

map.put("Apple", 100);       // Add key-value
map.get("Apple");            // Get value by key
map.remove("Apple");         // Remove by key
map.containsKey("Apple");    // Check if key exists
map.containsValue(100);      // Check if value exists
map.size();                  // Get size
map.keySet();                // Get all keys
map.values();                // Get all values
map.entrySet();              // Get all entries
```

#### **17.10 HashMap**

**HashMap** uses hash table for storage. Keys are unordered.

**Key Features:**

- Fast operations (O(1))
- Unordered
- Allows one null key
- Allows multiple null values
- Not synchronized

**Example:**

```java
HashMap<String, Integer> map = new HashMap<>();
map.put("Apple", 100);
map.put("Banana", 200);
map.put("Orange", 150);

System.out.println(map.get("Apple"));  // 100

// Iterate over entries
for (Map.Entry<String, Integer> entry : map.entrySet()) {
    System.out.println(entry.getKey() + ": " + entry.getValue());
}
```

**When to use:**

- Fast key-value lookup
- Order doesn't matter
- Single-threaded environment

#### **17.11 TreeMap**

**TreeMap** uses red-black tree. Keys are sorted.

**Key Features:**

- Sorted by keys
- Slower than HashMap (O(log n))
- No null keys
- Not synchronized

**Example:**

```java
TreeMap<String, Integer> map = new TreeMap<>();
map.put("Banana", 200);
map.put("Apple", 100);
map.put("Orange", 150);

System.out.println(map);  // {Apple=100, Banana=200, Orange=150} (sorted)
```

**When to use:**

- Need sorted keys
- Range operations

#### **17.12 Queue Interface**

**Queue** is a collection for holding elements before processing (FIFO - First In First Out).

**Key Features:**

- FIFO order
- Add at tail, remove from head
- Used for task scheduling

**Common Implementations:**

1. **LinkedList** - General purpose queue
2. **PriorityQueue** - Priority-based ordering

**Common Methods:**

```java
Queue<String> queue = new LinkedList<>();

queue.offer("First");        // Add element
queue.poll();                // Remove and return head
queue.peek();                // Return head without removing
queue.isEmpty();             // Check if empty
```

#### **17.13 Iterator**

**Iterator** is used to traverse collections.

**Methods:**

```java
Iterator<String> iterator = list.iterator();

while (iterator.hasNext()) {
    String element = iterator.next();
    System.out.println(element);
}
```

**Key Points:**

- `hasNext()` - Check if more elements
- `next()` - Get next element
- `remove()` - Remove current element

#### **17.14 Collections Class**

**Collections** is a utility class with static methods for collections.

**Common Methods:**

```java
List<Integer> list = new ArrayList<>(Arrays.asList(3, 1, 4, 1, 5));

Collections.sort(list);              // Sort
Collections.reverse(list);           // Reverse
Collections.shuffle(list);           // Shuffle
Collections.max(list);               // Get max
Collections.min(list);               // Get min
Collections.frequency(list, 1);      // Count occurrences
Collections.binarySearch(list, 3);   // Binary search
```

### 💻 Practical Examples

**Example 17.1: ArrayList Operations**

```java
// ArrayListDemo.java
import java.util.ArrayList;
import java.util.Collections;

public class ArrayListDemo {
    public static void main(String[] args) {
        System.out.println("=== ArrayList Demo ===\n");

        // Create ArrayList
        ArrayList<String> fruits = new ArrayList<>();

        // Add elements
        System.out.println("--- Adding Elements ---");
        fruits.add("Apple");
        fruits.add("Banana");
        fruits.add("Orange");
        fruits.add("Mango");
        fruits.add("Apple");  // Duplicate allowed
        System.out.println("Fruits: " + fruits);
        System.out.println("Size: " + fruits.size());
        System.out.println();

        // Access elements
        System.out.println("--- Accessing Elements ---");
        System.out.println("First fruit: " + fruits.get(0));
        System.out.println("Third fruit: " + fruits.get(2));
        System.out.println();

        // Modify elements
        System.out.println("--- Modifying Elements ---");
        fruits.set(1, "Grapes");
        System.out.println("After modification: " + fruits);
        System.out.println();

        // Search elements
        System.out.println("--- Searching Elements ---");
        System.out.println("Contains 'Mango': " + fruits.contains("Mango"));
        System.out.println("Index of 'Orange': " + fruits.indexOf("Orange"));
        System.out.println("Last index of 'Apple': " + fruits.lastIndexOf("Apple"));
        System.out.println();

        // Remove elements
        System.out.println("--- Removing Elements ---");
        fruits.remove(0);  // Remove by index
        System.out.println("After removing index 0: " + fruits);
        fruits.remove("Mango");  // Remove by object
        System.out.println("After removing 'Mango': " + fruits);
        System.out.println();

        // Sort
        System.out.println("--- Sorting ---");
        Collections.sort(fruits);
        System.out.println("Sorted: " + fruits);
        System.out.println();

        // Iterate
        System.out.println("--- Iteration ---");
        for (String fruit : fruits) {
            System.out.println("  - " + fruit);
        }
    }
}
```

**Output:**

```
=== ArrayList Demo ===

--- Adding Elements ---
Fruits: [Apple, Banana, Orange, Mango, Apple]
Size: 5

--- Accessing Elements ---
First fruit: Apple
Third fruit: Orange

--- Modifying Elements ---
After modification: [Apple, Grapes, Orange, Mango, Apple]

--- Searching Elements ---
Contains 'Mango': true
Index of 'Orange': 2
Last index of 'Apple': 4

--- Removing Elements ---
After removing index 0: [Grapes, Orange, Mango, Apple]
After removing 'Mango': [Grapes, Orange, Apple]

--- Sorting ---
Sorted: [Apple, Grapes, Orange]

--- Iteration ---
  - Apple
  - Grapes
  - Orange
```

**Example 17.2: HashSet and TreeSet**

```java
// SetDemo.java
import java.util.HashSet;
import java.util.TreeSet;

public class SetDemo {
    public static void main(String[] args) {
        System.out.println("=== Set Demo ===\n");

        // HashSet - Unordered, no duplicates
        System.out.println("--- HashSet ---");
        HashSet<Integer> hashSet = new HashSet<>();
        hashSet.add(30);
        hashSet.add(10);
        hashSet.add(20);
        hashSet.add(10);  // Duplicate, not added
        hashSet.add(40);

        System.out.println("HashSet: " + hashSet);
        System.out.println("Size: " + hashSet.size());
        System.out.println("Contains 20: " + hashSet.contains(20));
        System.out.println();

        // TreeSet - Sorted, no duplicates
        System.out.println("--- TreeSet ---");
        TreeSet<Integer> treeSet = new TreeSet<>();
        treeSet.add(30);
        treeSet.add(10);
        treeSet.add(20);
        treeSet.add(10);  // Duplicate, not added
        treeSet.add(40);

        System.out.println("TreeSet: " + treeSet);
        System.out.println("First element: " + treeSet.first());
        System.out.println("Last element: " + treeSet.last());
        System.out.println();

        // Set operations
        System.out.println("--- Set Operations ---");
        HashSet<String> set1 = new HashSet<>();
        set1.add("Java");
        set1.add("Python");
        set1.add("C++");

        HashSet<String> set2 = new HashSet<>();
        set2.add("Python");
        set2.add("JavaScript");
        set2.add("C++");

        System.out.println("Set 1: " + set1);
        System.out.println("Set 2: " + set2);

        // Union
        HashSet<String> union = new HashSet<>(set1);
        union.addAll(set2);
        System.out.println("Union: " + union);

        // Intersection
        HashSet<String> intersection = new HashSet<>(set1);
        intersection.retainAll(set2);
        System.out.println("Intersection: " + intersection);

        // Difference
        HashSet<String> difference = new HashSet<>(set1);
        difference.removeAll(set2);
        System.out.println("Difference (Set1 - Set2): " + difference);
    }
}
```

**Output:**

```
=== Set Demo ===

--- HashSet ---
HashSet: [40, 20, 10, 30]
Size: 4
Contains 20: true

--- TreeSet ---
TreeSet: [10, 20, 30, 40]
First element: 10
Last element: 40

--- Set Operations ---
Set 1: [Java, C++, Python]
Set 2: [JavaScript, C++, Python]
Union: [Java, JavaScript, C++, Python]
Intersection: [C++, Python]
Difference (Set1 - Set2): [Java]
```

**Example 17.3: HashMap Operations**

```java
// HashMapDemo.java
import java.util.HashMap;
import java.util.Map;

public class HashMapDemo {
    public static void main(String[] args) {
        System.out.println("=== HashMap Demo ===\n");

        // Create HashMap
        HashMap<String, Integer> studentMarks = new HashMap<>();

        // Add key-value pairs
        System.out.println("--- Adding Elements ---");
        studentMarks.put("Rahul", 85);
        studentMarks.put("Priya", 92);
        studentMarks.put("Amit", 78);
        studentMarks.put("Sneha", 95);

        System.out.println("Student Marks: " + studentMarks);
        System.out.println("Size: " + studentMarks.size());
        System.out.println();

        // Access values
        System.out.println("--- Accessing Values ---");
        System.out.println("Rahul's marks: " + studentMarks.get("Rahul"));
        System.out.println("Priya's marks: " + studentMarks.get("Priya"));
        System.out.println();

        // Check existence
        System.out.println("--- Checking Existence ---");
        System.out.println("Contains key 'Amit': " + studentMarks.containsKey("Amit"));
        System.out.println("Contains value 95: " + studentMarks.containsValue(95));
        System.out.println();

        // Update value
        System.out.println("--- Updating Values ---");
        studentMarks.put("Rahul", 90);  // Update existing key
        System.out.println("After update: " + studentMarks);
        System.out.println();

        // Iterate over entries
        System.out.println("--- Iteration ---");
        System.out.println("Using entrySet():");
        for (Map.Entry<String, Integer> entry : studentMarks.entrySet()) {
            System.out.println("  " + entry.getKey() + ": " + entry.getValue());
        }
        System.out.println();

        System.out.println("Using keySet():");
        for (String name : studentMarks.keySet()) {
            System.out.println("  " + name + ": " + studentMarks.get(name));
        }
        System.out.println();

        // Remove entry
        System.out.println("--- Removing Entry ---");
        studentMarks.remove("Amit");
        System.out.println("After removing 'Amit': " + studentMarks);
    }
}
```

**Output:**

```
=== HashMap Demo ===

--- Adding Elements ---
Student Marks: {Rahul=85, Priya=92, Amit=78, Sneha=95}
Size: 4

--- Accessing Values ---
Rahul's marks: 85
Priya's marks: 92

--- Checking Existence ---
Contains key 'Amit': true
Contains value 95: true

--- Updating Values ---
After update: {Rahul=90, Priya=92, Amit=78, Sneha=95}

--- Iteration ---
Using entrySet():
  Rahul: 90
  Priya: 92
  Amit: 78
  Sneha: 95

Using keySet():
  Rahul: 90
  Priya: 92
  Amit: 78
  Sneha: 95

--- Removing Entry ---
After removing 'Amit': {Rahul=90, Priya=92, Sneha=95}
```

### 🎯 Key Takeaways

- Collections Framework provides ready-to-use data structures
- List allows duplicates and maintains order (ArrayList, LinkedList)
- Set doesn't allow duplicates (HashSet, TreeSet)
- Map stores key-value pairs (HashMap, TreeMap)
- ArrayList is fast for access, LinkedList is fast for insertion/deletion
- HashSet is unordered and fast, TreeSet is sorted
- HashMap is unordered and fast, TreeMap is sorted by keys
- Use Collections class for utility operations (sort, reverse, etc.)

### 📝 Practice Questions

1. What is the difference between ArrayList and LinkedList?
2. What is the difference between HashSet and TreeSet?
3. How does HashMap work internally?
4. When should you use List vs Set vs Map?
5. Write a program to find duplicate elements in an ArrayList.

---

## Chapter 18: File I/O (Input/Output)

### 📘 Theory

#### **18.1 What is File I/O?**

**File I/O** (Input/Output) refers to reading data from files and writing data to files. Java provides comprehensive support for file operations through various classes in `java.io` package.

**Real-World Analogy:**
Think of **file operations** like working with physical documents:

- **Reading a file** - Reading a book page by page
- **Writing to a file** - Writing in a notebook
- **Appending to a file** - Adding new pages to an existing notebook
- **Deleting a file** - Throwing away a document

**Why File I/O?**

- ✅ **Persistent storage** - Data survives program termination
- ✅ **Data sharing** - Share data between programs
- ✅ **Large data handling** - Process data too large for memory
- ✅ **Configuration** - Store application settings
- ✅ **Logging** - Record program activities

#### **18.2 File Class**

**File** class represents a file or directory path. It provides methods to work with files and directories.

**Key Features:**

- Create, delete, rename files/directories
- Check file properties (exists, readable, writable)
- Get file information (size, path, name)
- List directory contents

**Common Methods:**

```java
File file = new File("example.txt");

file.exists();           // Check if file exists
file.isFile();           // Check if it's a file
file.isDirectory();      // Check if it's a directory
file.getName();          // Get file name
file.getPath();          // Get file path
file.getAbsolutePath();  // Get absolute path
file.length();           // Get file size in bytes
file.canRead();          // Check if readable
file.canWrite();         // Check if writable
file.delete();           // Delete file
file.mkdir();            // Create directory
file.mkdirs();           // Create directory with parents
file.list();             // List files in directory
```

**Example:**

```java
File file = new File("data.txt");

if (file.exists()) {
    System.out.println("File exists");
    System.out.println("Size: " + file.length() + " bytes");
} else {
    System.out.println("File does not exist");
}
```

#### **18.3 Streams in Java**

**Stream** is a sequence of data. Java uses streams to perform I/O operations.

**Types of Streams:**

1. **Byte Streams** - Handle binary data (images, videos, etc.)

   - `InputStream` and `OutputStream` (abstract classes)
   - `FileInputStream`, `FileOutputStream`

2. **Character Streams** - Handle text data (characters)
   - `Reader` and `Writer` (abstract classes)
   - `FileReader`, `FileWriter`

**Stream Hierarchy:**

```
InputStream                    Reader
    |                             |
FileInputStream              FileReader
BufferedInputStream          BufferedReader

OutputStream                   Writer
    |                             |
FileOutputStream             FileWriter
BufferedOutputStream         BufferedWriter
```

**When to use:**

- **Byte Streams** - For binary files (images, audio, video)
- **Character Streams** - For text files (txt, csv, json)

#### **18.4 FileWriter and FileReader**

**FileWriter** writes character data to files.
**FileReader** reads character data from files.

**FileWriter:**

```java
FileWriter writer = new FileWriter("output.txt");
writer.write("Hello, World!");
writer.close();  // Important: Always close
```

**FileWriter with append mode:**

```java
FileWriter writer = new FileWriter("output.txt", true);  // true = append
writer.write("New line\n");
writer.close();
```

**FileReader:**

```java
FileReader reader = new FileReader("input.txt");
int character;
while ((character = reader.read()) != -1) {
    System.out.print((char) character);
}
reader.close();
```

**Key Points:**

- Always close streams to free resources
- Use try-catch for exception handling
- FileWriter overwrites by default (use append mode to add)

#### **18.5 BufferedReader and BufferedWriter**

**BufferedReader** and **BufferedWriter** provide buffering for efficient reading/writing.

**Benefits:**

- ✅ **Faster** - Reduces disk access by buffering
- ✅ **Line-by-line reading** - `readLine()` method
- ✅ **Efficient** - Reads/writes in chunks

**BufferedWriter:**

```java
BufferedWriter writer = new BufferedWriter(new FileWriter("output.txt"));
writer.write("Line 1");
writer.newLine();  // Platform-independent newline
writer.write("Line 2");
writer.close();
```

**BufferedReader:**

```java
BufferedReader reader = new BufferedReader(new FileReader("input.txt"));
String line;
while ((line = reader.readLine()) != null) {
    System.out.println(line);
}
reader.close();
```

**FileReader vs BufferedReader:**

| Feature        | FileReader             | BufferedReader    |
| -------------- | ---------------------- | ----------------- |
| **Speed**      | Slower                 | Faster (buffered) |
| **Reading**    | Character by character | Line by line      |
| **Efficiency** | Less efficient         | More efficient    |
| **Use Case**   | Small files            | Large files       |

#### **18.6 FileInputStream and FileOutputStream**

**FileInputStream** reads binary data from files.
**FileOutputStream** writes binary data to files.

**FileOutputStream:**

```java
FileOutputStream fos = new FileOutputStream("data.bin");
fos.write(65);  // Writes byte value 65 (ASCII 'A')
fos.close();
```

**FileInputStream:**

```java
FileInputStream fis = new FileInputStream("data.bin");
int data;
while ((data = fis.read()) != -1) {
    System.out.print((char) data);
}
fis.close();
```

**Use Cases:**

- Copy files (images, videos, executables)
- Read/write binary data
- Network data transfer

#### **18.7 Try-with-Resources**

**Try-with-resources** automatically closes resources (introduced in Java 7).

**Syntax:**

```java
try (ResourceType resource = new ResourceType()) {
    // Use resource
} catch (Exception e) {
    // Handle exception
}
// Resource automatically closed
```

**Example:**

```java
try (BufferedReader reader = new BufferedReader(new FileReader("input.txt"))) {
    String line;
    while ((line = reader.readLine()) != null) {
        System.out.println(line);
    }
} catch (IOException e) {
    e.printStackTrace();
}
// No need to explicitly close reader
```

**Benefits:**

- ✅ **Automatic resource management** - No need to call close()
- ✅ **Cleaner code** - Less boilerplate
- ✅ **Exception safe** - Closes even if exception occurs

#### **18.8 Serialization**

**Serialization** is the process of converting an object into a byte stream for storage or transmission.
**Deserialization** is the reverse process.

**Why Serialization?**

- Save object state to file
- Send objects over network
- Cache objects in memory

**Serializable Interface:**

```java
import java.io.Serializable;

class Student implements Serializable {
    private static final long serialVersionUID = 1L;
    String name;
    int age;

    public Student(String name, int age) {
        this.name = name;
        this.age = age;
    }
}
```

**Serialization (Writing Object):**

```java
try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("student.ser"))) {
    Student student = new Student("Rahul", 20);
    oos.writeObject(student);
} catch (IOException e) {
    e.printStackTrace();
}
```

**Deserialization (Reading Object):**

```java
try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream("student.ser"))) {
    Student student = (Student) ois.readObject();
    System.out.println(student.name + ", " + student.age);
} catch (IOException | ClassNotFoundException e) {
    e.printStackTrace();
}
```

**Key Points:**

- Class must implement `Serializable` interface
- `serialVersionUID` ensures version compatibility
- `transient` keyword prevents field serialization
- Static fields are not serialized

#### **18.9 File Operations**

**Common File Operations:**

**1. Create File:**

```java
File file = new File("newfile.txt");
if (file.createNewFile()) {
    System.out.println("File created");
} else {
    System.out.println("File already exists");
}
```

**2. Delete File:**

```java
File file = new File("oldfile.txt");
if (file.delete()) {
    System.out.println("File deleted");
} else {
    System.out.println("Failed to delete");
}
```

**3. Rename File:**

```java
File oldFile = new File("old.txt");
File newFile = new File("new.txt");
if (oldFile.renameTo(newFile)) {
    System.out.println("File renamed");
}
```

**4. Create Directory:**

```java
File dir = new File("mydir");
if (dir.mkdir()) {
    System.out.println("Directory created");
}
```

**5. List Files in Directory:**

```java
File dir = new File("mydir");
String[] files = dir.list();
for (String file : files) {
    System.out.println(file);
}
```

#### **18.10 Exception Handling in File I/O**

**Common Exceptions:**

- `FileNotFoundException` - File not found
- `IOException` - General I/O error
- `EOFException` - End of file reached unexpectedly

**Best Practice:**

```java
try (BufferedReader reader = new BufferedReader(new FileReader("data.txt"))) {
    String line;
    while ((line = reader.readLine()) != null) {
        System.out.println(line);
    }
} catch (FileNotFoundException e) {
    System.out.println("File not found: " + e.getMessage());
} catch (IOException e) {
    System.out.println("I/O error: " + e.getMessage());
}
```

### 💻 Practical Examples

**Example 18.1: Writing and Reading Text Files**

```java
// FileWriteReadDemo.java
import java.io.*;

public class FileWriteReadDemo {
    public static void main(String[] args) {
        System.out.println("=== File Write and Read Demo ===\n");

        String filename = "student_data.txt";

        // Writing to file
        System.out.println("--- Writing to File ---");
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename))) {
            writer.write("Student Records");
            writer.newLine();
            writer.write("================");
            writer.newLine();
            writer.write("Name: Rahul Kumar");
            writer.newLine();
            writer.write("Roll No: 101");
            writer.newLine();
            writer.write("Marks: 85");
            writer.newLine();
            writer.write("Grade: A");

            System.out.println("Data written to file successfully!");
        } catch (IOException e) {
            System.out.println("Error writing to file: " + e.getMessage());
        }

        System.out.println();

        // Reading from file
        System.out.println("--- Reading from File ---");
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        } catch (FileNotFoundException e) {
            System.out.println("File not found: " + e.getMessage());
        } catch (IOException e) {
            System.out.println("Error reading file: " + e.getMessage());
        }

        System.out.println();

        // Appending to file
        System.out.println("--- Appending to File ---");
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(filename, true))) {
            writer.newLine();
            writer.write("--- Additional Info ---");
            writer.newLine();
            writer.write("City: Mumbai");

            System.out.println("Data appended successfully!");
        } catch (IOException e) {
            System.out.println("Error appending to file: " + e.getMessage());
        }

        System.out.println();

        // Reading updated file
        System.out.println("--- Reading Updated File ---");
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
        } catch (IOException e) {
            System.out.println("Error reading file: " + e.getMessage());
        }
    }
}
```

**Output:**

```
=== File Write and Read Demo ===

--- Writing to File ---
Data written to file successfully!

--- Reading from File ---
Student Records
================
Name: Rahul Kumar
Roll No: 101
Marks: 85
Grade: A

--- Appending to File ---
Data appended successfully!

--- Reading Updated File ---
Student Records
================
Name: Rahul Kumar
Roll No: 101
Marks: 85
Grade: A
--- Additional Info ---
City: Mumbai
```

**Example 18.2: File Operations**

```java
// FileOperationsDemo.java
import java.io.*;

public class FileOperationsDemo {
    public static void main(String[] args) {
        System.out.println("=== File Operations Demo ===\n");

        // Create file
        System.out.println("--- Creating File ---");
        File file = new File("test.txt");
        try {
            if (file.createNewFile()) {
                System.out.println("File created: " + file.getName());
            } else {
                System.out.println("File already exists");
            }
        } catch (IOException e) {
            System.out.println("Error creating file: " + e.getMessage());
        }

        System.out.println();

        // File information
        System.out.println("--- File Information ---");
        if (file.exists()) {
            System.out.println("File Name: " + file.getName());
            System.out.println("Absolute Path: " + file.getAbsolutePath());
            System.out.println("Writable: " + file.canWrite());
            System.out.println("Readable: " + file.canRead());
            System.out.println("File Size: " + file.length() + " bytes");
            System.out.println("Is File: " + file.isFile());
            System.out.println("Is Directory: " + file.isDirectory());
        }

        System.out.println();

        // Write to file
        System.out.println("--- Writing to File ---");
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(file))) {
            writer.write("This is a test file.");
            writer.newLine();
            writer.write("File operations in Java.");
            System.out.println("Content written to file");
        } catch (IOException e) {
            System.out.println("Error writing: " + e.getMessage());
        }

        System.out.println();

        // File size after writing
        System.out.println("--- File Size After Writing ---");
        System.out.println("File Size: " + file.length() + " bytes");

        System.out.println();

        // Create directory
        System.out.println("--- Creating Directory ---");
        File dir = new File("testdir");
        if (dir.mkdir()) {
            System.out.println("Directory created: " + dir.getName());
        } else {
            System.out.println("Directory already exists or failed to create");
        }

        System.out.println();

        // Rename file
        System.out.println("--- Renaming File ---");
        File newFile = new File("renamed_test.txt");
        if (file.renameTo(newFile)) {
            System.out.println("File renamed to: " + newFile.getName());
        } else {
            System.out.println("Failed to rename file");
        }

        System.out.println();

        // Delete file
        System.out.println("--- Deleting File ---");
        if (newFile.delete()) {
            System.out.println("File deleted: " + newFile.getName());
        } else {
            System.out.println("Failed to delete file");
        }

        // Delete directory
        if (dir.delete()) {
            System.out.println("Directory deleted: " + dir.getName());
        }
    }
}
```

**Output:**

```
=== File Operations Demo ===

--- Creating File ---
File created: test.txt

--- File Information ---
File Name: test.txt
Absolute Path: C:\Users\...\test.txt
Writable: true
Readable: true
File Size: 0 bytes
Is File: true
Is Directory: false

--- Writing to File ---
Content written to file

--- File Size After Writing ---
File Size: 44 bytes

--- Creating Directory ---
Directory created: testdir

--- Renaming File ---
File renamed to: renamed_test.txt

--- Deleting File ---
File deleted: renamed_test.txt
Directory deleted: testdir
```

**Example 18.3: Copying Files**

```java
// FileCopyDemo.java
import java.io.*;

public class FileCopyDemo {
    public static void main(String[] args) {
        System.out.println("=== File Copy Demo ===\n");

        String sourceFile = "source.txt";
        String destFile = "destination.txt";

        // Create source file
        System.out.println("--- Creating Source File ---");
        try (BufferedWriter writer = new BufferedWriter(new FileWriter(sourceFile))) {
            writer.write("This is the original file.");
            writer.newLine();
            writer.write("It contains some sample data.");
            writer.newLine();
            writer.write("We will copy this file.");
            System.out.println("Source file created");
        } catch (IOException e) {
            System.out.println("Error creating source file: " + e.getMessage());
            return;
        }

        System.out.println();

        // Copy file using character streams
        System.out.println("--- Copying File ---");
        try (BufferedReader reader = new BufferedReader(new FileReader(sourceFile));
             BufferedWriter writer = new BufferedWriter(new FileWriter(destFile))) {

            String line;
            int lineCount = 0;
            while ((line = reader.readLine()) != null) {
                writer.write(line);
                writer.newLine();
                lineCount++;
            }

            System.out.println("File copied successfully!");
            System.out.println("Lines copied: " + lineCount);

        } catch (IOException e) {
            System.out.println("Error copying file: " + e.getMessage());
        }

        System.out.println();

        // Verify copied file
        System.out.println("--- Verifying Copied File ---");
        try (BufferedReader reader = new BufferedReader(new FileReader(destFile))) {
            String line;
            System.out.println("Content of destination file:");
            while ((line = reader.readLine()) != null) {
                System.out.println("  " + line);
            }
        } catch (IOException e) {
            System.out.println("Error reading destination file: " + e.getMessage());
        }

        System.out.println();

        // File sizes
        System.out.println("--- File Sizes ---");
        File src = new File(sourceFile);
        File dest = new File(destFile);
        System.out.println("Source file size: " + src.length() + " bytes");
        System.out.println("Destination file size: " + dest.length() + " bytes");

        // Cleanup
        src.delete();
        dest.delete();
    }
}
```

**Output:**

```
=== File Copy Demo ===

--- Creating Source File ---
Source file created

--- Copying File ---
File copied successfully!
Lines copied: 3

--- Verifying Copied File ---
Content of destination file:
  This is the original file.
  It contains some sample data.
  We will copy this file.

--- File Sizes ---
Source file size: 85 bytes
Destination file size: 85 bytes
```

### 🎯 Key Takeaways

- File class represents files and directories
- Use character streams (Reader/Writer) for text files
- Use byte streams (InputStream/OutputStream) for binary files
- BufferedReader/BufferedWriter provide efficient buffered I/O
- Try-with-resources automatically closes resources
- Always handle IOException when working with files
- Serialization converts objects to byte streams for storage
- Common operations: create, read, write, delete, rename files

### 📝 Practice Questions

1. What is the difference between FileReader and BufferedReader?
2. What is the purpose of try-with-resources statement?
3. How does serialization work in Java?
4. What is the difference between byte streams and character streams?
5. Write a program to count the number of words in a text file.

---

## Chapter 19: Multithreading

### 📘 Theory

#### **19.1 What is Multithreading?**

**Multithreading** is a Java feature that allows concurrent execution of two or more parts of a program for maximum utilization of CPU resources. Each part of such a program is called a **thread**, which is a lightweight sub-process and the smallest unit of processing.

**Detailed Explanation:**

Multithreading enables a program to perform multiple tasks simultaneously. Instead of executing tasks one after another (sequential execution), multithreading allows multiple tasks to run at the same time (concurrent execution), making better use of CPU time and improving overall program performance.

**What is a Thread?**

A thread is:

- A lightweight process
- An independent path of execution within a program
- The smallest unit of processing
- A way to achieve multitasking within a single program

**Real-World Analogies:**

**1. Restaurant Kitchen:**

- **Single-threaded (Sequential):**

  - One chef does everything: chop vegetables → cook → plate → clean → serve
  - Next order starts only after first is complete
  - Slow and inefficient

- **Multithreaded (Concurrent):**
  - Chef 1: Chops vegetables
  - Chef 2: Cooks food
  - Chef 3: Plates dishes
  - Chef 4: Cleans utensils
  - All work simultaneously on different orders
  - Fast and efficient

**2. Bank with Multiple Counters:**

- **Single-threaded:** One counter serving customers one by one (slow)
- **Multithreaded:** Multiple counters serving customers simultaneously (fast)

**3. Web Browser:**

- **Thread 1:** Downloads a file
- **Thread 2:** Plays a video
- **Thread 3:** Loads a webpage
- **Thread 4:** Responds to user clicks
- All happen simultaneously without blocking each other

**4. Text Editor:**

- **Thread 1:** Accepts user typing
- **Thread 2:** Auto-saves document
- **Thread 3:** Spell-checks in background
- **Thread 4:** Formats text
- User can type while auto-save and spell-check run in background

**Single-threaded vs Multithreaded Execution:**

**Single-threaded:**

```
Task 1 → Task 2 → Task 3 → Task 4
[====] [====] [====] [====]
Total time: 16 seconds
```

**Multithreaded:**

```
Task 1 [====]
Task 2 [====]
Task 3 [====]
Task 4 [====]
Total time: 4 seconds (all run simultaneously)
```

**How Multithreading Works:**

```
Program
   │
   ├─ Thread 1 (Main Thread)
   │     └─ Executes main() method
   │
   ├─ Thread 2 (Worker Thread)
   │     └─ Downloads file
   │
   ├─ Thread 3 (Worker Thread)
   │     └─ Processes data
   │
   └─ Thread 4 (Worker Thread)
         └─ Updates UI

All threads share the same memory space
```

**Benefits of Multithreading:**

**1. Better CPU Utilization:**

- CPU doesn't sit idle
- Multiple tasks use CPU time efficiently
- Maximizes processor usage

**2. Improved Performance:**

- Faster execution for independent tasks
- Parallel processing of operations
- Reduced total execution time

**3. Responsiveness:**

- UI remains responsive while background tasks run
- User can interact while processing happens
- No freezing or hanging

**4. Resource Sharing:**

- Threads share memory and resources
- No need for separate memory allocation
- Efficient memory usage

**5. Simplified Program Structure:**

- Complex tasks divided into simpler threads
- Each thread handles one specific task
- Easier to understand and maintain

**6. Concurrent Operations:**

- Multiple operations happen simultaneously
- Better user experience
- Efficient multitasking

**7. Asynchronous Processing:**

- Long-running tasks don't block main program
- Background processing while user continues work
- Non-blocking I/O operations

**Real-World Use Cases:**

**1. Web Servers:**

- Each client request handled by separate thread
- Thousands of users served simultaneously
- No waiting for previous request to complete

**2. Gaming:**

- Thread 1: Renders graphics
- Thread 2: Handles user input
- Thread 3: Plays background music
- Thread 4: Manages AI opponents
- Thread 5: Network communication

**3. Video Players:**

- Thread 1: Decodes video
- Thread 2: Decodes audio
- Thread 3: Displays frames
- Thread 4: Handles user controls

**4. Database Systems:**

- Multiple queries processed simultaneously
- Each transaction in separate thread
- Concurrent read/write operations

**5. GUI Applications:**

- Main thread: Handles UI events
- Worker threads: Perform background tasks
- UI stays responsive during heavy operations

**When to Use Multithreading:**

1. **Independent tasks** - Tasks that don't depend on each other
2. **I/O operations** - File reading, network calls, database queries
3. **Background processing** - Auto-save, spell-check, data sync
4. **Parallel computations** - Image processing, data analysis
5. **Responsive UI** - Keep interface responsive during long operations

**Challenges of Multithreading:**

1. **Complexity** - Harder to design and debug
2. **Synchronization** - Need to coordinate thread access to shared resources
3. **Deadlocks** - Threads waiting for each other indefinitely
4. **Race conditions** - Unpredictable results when threads access shared data
5. **Thread overhead** - Creating too many threads can slow down program

#### **19.2 Process vs Thread**

Understanding the difference between processes and threads is crucial for effective multithreading programming.

**What is a Process?**

A **process** is an independent program in execution. It is a self-contained execution environment with its own memory space, resources, and system state.

**Characteristics of Process:**

- Independent program running in memory
- Has its own memory space (code, data, heap, stack)
- Heavy-weight (requires more system resources)
- Isolated from other processes
- Inter-process communication (IPC) is complex and expensive
- Creating a process is slower
- Context switching between processes is expensive

**Example:** Running multiple applications:

- Chrome browser (Process 1)
- Microsoft Word (Process 2)
- Music player (Process 3)
- Each runs independently with separate memory

**What is a Thread?**

A **thread** is a lightweight sub-process, the smallest unit of processing. It is an independent path of execution within a process.

**Characteristics of Thread:**

- Lightweight sub-process within a program
- Shares memory with other threads of same process
- Light-weight (requires fewer resources)
- Shares resources with other threads
- Inter-thread communication is easy (shared memory)
- Creating a thread is faster
- Context switching between threads is faster

**Example:** Within a web browser (single process):

- Thread 1: Renders webpage
- Thread 2: Downloads files
- Thread 3: Plays video
- Thread 4: Handles user input
- All share the same memory space

**Real-World Analogy:**

**Process = House:**

- Each house is independent
- Has its own rooms, furniture, utilities
- Residents of one house can't directly access another house
- Communication between houses requires phone calls, visits (expensive)

**Thread = Rooms in a House:**

- Multiple rooms in the same house
- Share common resources (kitchen, bathroom, living room)
- People in different rooms can easily communicate
- All rooms are part of the same house (process)

**Another Analogy:**

**Process = Company:**

- Each company is independent
- Has its own office, employees, resources
- Companies don't share resources

**Thread = Departments in Company:**

- HR, Sales, IT departments
- All part of same company
- Share common resources (building, cafeteria, meeting rooms)
- Easy communication between departments

**Memory Representation:**

**Process:**

```
┌─────────────────────┐
│   Process 1         │
│  ┌───────────────┐  │
│  │ Code Section  │  │
│  ├───────────────┤  │
│  │ Data Section  │  │
│  ├───────────────┤  │
│  │ Heap          │  │
│  ├───────────────┤  │
│  │ Stack         │  │
│  └───────────────┘  │
└─────────────────────┘

┌─────────────────────┐
│   Process 2         │
│  ┌───────────────┐  │
│  │ Code Section  │  │
│  ├───────────────┤  │
│  │ Data Section  │  │
│  ├───────────────┤  │
│  │ Heap          │  │
│  ├───────────────┤  │
│  │ Stack         │  │
│  └───────────────┘  │
└─────────────────────┘
Separate memory spaces
```

**Thread:**

```
┌─────────────────────────────┐
│   Process (Shared Memory)   │
│  ┌───────────────┐          │
│  │ Code Section  │ (Shared) │
│  ├───────────────┤          │
│  │ Data Section  │ (Shared) │
│  ├───────────────┤          │
│  │ Heap          │ (Shared) │
│  ├───────────────┤          │
│  │ Thread 1 Stack│          │
│  ├───────────────┤          │
│  │ Thread 2 Stack│          │
│  ├───────────────┤          │
│  │ Thread 3 Stack│          │
│  └───────────────┘          │
└─────────────────────────────┘
Shared memory, separate stacks
```

**Detailed Comparison:**

| Feature                   | Process                                 | Thread                                |
| ------------------------- | --------------------------------------- | ------------------------------------- |
| **Definition**            | Independent program in execution        | Lightweight sub-process               |
| **Memory**                | Separate memory space                   | Shared memory space                   |
| **Weight**                | Heavy-weight (more resources)           | Light-weight (fewer resources)        |
| **Creation Time**         | Slower (more overhead)                  | Faster (less overhead)                |
| **Termination Time**      | Slower                                  | Faster                                |
| **Communication**         | Expensive (IPC - pipes, sockets, files) | Easy (shared memory, variables)       |
| **Context Switching**     | Slower (more state to save/restore)     | Faster (less state to save/restore)   |
| **Independence**          | Completely independent                  | Part of a process                     |
| **Resource Sharing**      | No sharing (isolated)                   | Share code, data, heap                |
| **Crash Impact**          | Doesn't affect other processes          | May crash entire process              |
| **Security**              | More secure (isolated)                  | Less secure (shared memory)           |
| **Overhead**              | High                                    | Low                                   |
| **Example**               | Chrome, Word, Excel (separate programs) | Multiple tabs in Chrome               |
| **Operating System View** | Separate entities                       | Parts of same entity                  |
| **Process ID**            | Each has unique PID                     | Share same PID                        |
| **Address Space**         | Separate address space                  | Shared address space                  |
| **Data Sharing**          | Difficult (requires IPC)                | Easy (direct access to shared memory) |

**When to Use Process:**

1. **Complete isolation needed** - Security-critical applications
2. **Independent applications** - Separate programs
3. **Fault tolerance** - One failure shouldn't affect others
4. **Different programming languages** - Each process can use different language

**When to Use Thread:**

1. **Shared data** - Multiple tasks need to access same data
2. **Lightweight tasks** - Quick, frequent task switching
3. **Responsive UI** - Keep interface responsive
4. **Parallel processing** - Divide work among threads
5. **Resource efficiency** - Save memory and resources

**Example Code Comparison:**

**Creating Process (Not in Java, conceptual):**

```java
// Java doesn't directly create processes like this
// But can execute external programs
ProcessBuilder pb = new ProcessBuilder("notepad.exe");
Process process = pb.start();  // New process created
```

**Creating Thread (Java):**

```java
// Creating thread is simple and lightweight
Thread thread = new Thread(() -> {
    System.out.println("Thread running");
});
thread.start();  // New thread created
```

#### **19.3 Thread Lifecycle**

A thread goes through various states during its lifetime:

```
        NEW
         |
         | start()
         ↓
      RUNNABLE ←──────────┐
         |                 |
         | (CPU scheduler) |
         ↓                 |
      RUNNING             |
         |                 |
    ┌────┼────┐           |
    |    |    |           |
sleep() wait() I/O        |
    |    |    |           |
    ↓    ↓    ↓           |
  TIMED_WAITING/WAITING   |
         |                 |
         | notify()/time expires
         └─────────────────┘
         |
         | completes
         ↓
     TERMINATED
```

**Thread States:**

1. **NEW** - Thread is created but not started
2. **RUNNABLE** - Thread is ready to run (waiting for CPU)
3. **RUNNING** - Thread is executing
4. **BLOCKED/WAITING** - Thread is waiting for a resource or notification
5. **TIMED_WAITING** - Thread is waiting for a specified time
6. **TERMINATED** - Thread has completed execution

#### **19.4 Creating Threads**

There are two ways to create threads in Java:

**Method 1: Extending Thread Class**

```java
class MyThread extends Thread {
    public void run() {
        // Code to be executed by thread
        System.out.println("Thread is running");
    }
}

// Usage
MyThread t = new MyThread();
t.start();  // Starts the thread
```

**Method 2: Implementing Runnable Interface**

```java
class MyRunnable implements Runnable {
    public void run() {
        // Code to be executed by thread
        System.out.println("Thread is running");
    }
}

// Usage
MyRunnable r = new MyRunnable();
Thread t = new Thread(r);
t.start();  // Starts the thread
```

**Thread vs Runnable:**

| Feature           | Extending Thread          | Implementing Runnable  |
| ----------------- | ------------------------- | ---------------------- |
| **Inheritance**   | Cannot extend other class | Can extend other class |
| **Flexibility**   | Less flexible             | More flexible          |
| **Reusability**   | Less reusable             | More reusable          |
| **Best Practice** | Not recommended           | Recommended ✅         |

**Why Runnable is preferred:**

- Java doesn't support multiple inheritance
- Separates task from thread mechanism
- Better object-oriented design

#### **19.5 Thread Methods**

**Common Thread Methods:**

```java
Thread t = new Thread();

t.start();              // Start the thread
t.run();                // Execute thread's code (don't call directly)
t.sleep(1000);          // Sleep for 1000ms (static method)
t.join();               // Wait for thread to complete
t.getName();            // Get thread name
t.setName("MyThread");  // Set thread name
t.getPriority();        // Get thread priority (1-10)
t.setPriority(5);       // Set thread priority
t.isAlive();            // Check if thread is alive
t.interrupt();          // Interrupt the thread
Thread.currentThread(); // Get current thread (static)
Thread.yield();         // Hint to scheduler to give up CPU (static)
```

**Important Notes:**

- Always call `start()`, not `run()` directly
- `start()` creates new thread and calls `run()`
- Calling `run()` directly executes in same thread

#### **19.6 Thread Priority**

Threads have priorities from 1 (MIN_PRIORITY) to 10 (MAX_PRIORITY). Default is 5 (NORM_PRIORITY).

```java
Thread t = new Thread();
t.setPriority(Thread.MAX_PRIORITY);  // 10
t.setPriority(Thread.NORM_PRIORITY); // 5
t.setPriority(Thread.MIN_PRIORITY);  // 1
```

**Key Points:**

- Higher priority threads get preference
- Priority is just a hint to scheduler
- Doesn't guarantee execution order
- Platform-dependent behavior

#### **19.7 Synchronization**

**Synchronization** is the capability to control access to shared resources by multiple threads.

**Why Synchronization?**

- Prevents **thread interference** (data corruption)
- Prevents **memory consistency errors**
- Ensures **thread safety**

**Problem without Synchronization:**

```java
class Counter {
    int count = 0;

    void increment() {
        count++;  // Not atomic! (read, increment, write)
    }
}

// Two threads calling increment() simultaneously can cause data loss
```

**Solution: Synchronized Method**

```java
class Counter {
    int count = 0;

    synchronized void increment() {
        count++;  // Now thread-safe
    }
}
```

**Synchronized Block:**

```java
class Counter {
    int count = 0;

    void increment() {
        synchronized(this) {
            count++;
        }
    }
}
```

**Synchronized Method vs Block:**

| Feature         | Synchronized Method          | Synchronized Block      |
| --------------- | ---------------------------- | ----------------------- |
| **Syntax**      | `synchronized void method()` | `synchronized(obj) { }` |
| **Lock**        | Locks entire object          | Locks specific object   |
| **Granularity** | Coarse-grained               | Fine-grained            |
| **Performance** | Slower (locks more)          | Faster (locks less)     |

#### **19.8 Inter-Thread Communication**

Threads can communicate using `wait()`, `notify()`, and `notifyAll()` methods.

**Methods (must be called inside synchronized block):**

```java
wait();        // Release lock and wait
notify();      // Wake up one waiting thread
notifyAll();   // Wake up all waiting threads
```

**Producer-Consumer Problem:**

```java
class SharedResource {
    synchronized void produce() {
        // Produce item
        notify();  // Notify consumer
    }

    synchronized void consume() {
        wait();    // Wait for producer
        // Consume item
    }
}
```

#### **19.9 Deadlock**

**Deadlock** occurs when two or more threads are blocked forever, waiting for each other.

**Example:**

```java
// Thread 1 locks A, waits for B
synchronized(A) {
    synchronized(B) {
        // ...
    }
}

// Thread 2 locks B, waits for A
synchronized(B) {
    synchronized(A) {
        // ...
    }
}
// DEADLOCK! Both threads wait forever
```

**How to Avoid Deadlock:**

- ✅ Avoid nested locks
- ✅ Lock ordering (always acquire locks in same order)
- ✅ Use timeout (tryLock with timeout)
- ✅ Deadlock detection algorithms

#### **19.10 Daemon Threads**

**Daemon threads** are low-priority threads that run in background to perform tasks like garbage collection.

```java
Thread t = new Thread();
t.setDaemon(true);  // Make it daemon thread
t.start();
```

**Characteristics:**

- JVM terminates when only daemon threads remain
- Used for background supporting tasks
- Examples: Garbage collector, finalizer

**Daemon vs User Thread:**

| Feature      | User Thread | Daemon Thread    |
| ------------ | ----------- | ---------------- |
| **Priority** | High        | Low              |
| **JVM Exit** | JVM waits   | JVM doesn't wait |
| **Purpose**  | Main tasks  | Background tasks |
| **Default**  | User thread | -                |

#### **19.11 Thread Pool**

**Thread Pool** is a collection of pre-initialized threads ready to perform tasks.

**Benefits:**

- ✅ Reuses threads (no creation overhead)
- ✅ Limits number of threads
- ✅ Better resource management
- ✅ Improved performance

**Using ExecutorService:**

```java
import java.util.concurrent.*;

ExecutorService executor = Executors.newFixedThreadPool(5);

executor.execute(() -> {
    System.out.println("Task executed");
});

executor.shutdown();  // Shutdown after tasks complete
```

**Types of Thread Pools:**

```java
Executors.newFixedThreadPool(n);      // Fixed number of threads
Executors.newCachedThreadPool();      // Creates threads as needed
Executors.newSingleThreadExecutor();  // Single thread
Executors.newScheduledThreadPool(n);  // Scheduled tasks
```

#### **19.12 Volatile Keyword**

**volatile** keyword ensures that changes to a variable are visible to all threads.

```java
class SharedData {
    volatile boolean flag = false;

    void setFlag() {
        flag = true;  // Visible to all threads immediately
    }
}
```

**When to use:**

- Variable is accessed by multiple threads
- One thread modifies, others read
- No compound operations (like count++)

**volatile vs synchronized:**

| Feature        | volatile     | synchronized       |
| -------------- | ------------ | ------------------ |
| **Atomicity**  | No           | Yes                |
| **Visibility** | Yes          | Yes                |
| **Locking**    | No           | Yes                |
| **Use Case**   | Simple flags | Complex operations |

### 💻 Practical Examples

**Example 19.1: Creating Threads**

```java
// ThreadCreationDemo.java

// Method 1: Extending Thread class
class MyThread extends Thread {
    private String threadName;

    MyThread(String name) {
        this.threadName = name;
    }

    public void run() {
        System.out.println(threadName + " started");
        for (int i = 1; i <= 5; i++) {
            System.out.println(threadName + ": " + i);
            try {
                Thread.sleep(500);  // Sleep for 500ms
            } catch (InterruptedException e) {
                System.out.println(threadName + " interrupted");
            }
        }
        System.out.println(threadName + " finished");
    }
}

// Method 2: Implementing Runnable interface
class MyRunnable implements Runnable {
    private String threadName;

    MyRunnable(String name) {
        this.threadName = name;
    }

    public void run() {
        System.out.println(threadName + " started");
        for (int i = 1; i <= 5; i++) {
            System.out.println(threadName + ": " + i);
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                System.out.println(threadName + " interrupted");
            }
        }
        System.out.println(threadName + " finished");
    }
}

public class ThreadCreationDemo {
    public static void main(String[] args) {
        System.out.println("=== Thread Creation Demo ===\n");

        // Method 1: Using Thread class
        System.out.println("--- Method 1: Extending Thread ---");
        MyThread t1 = new MyThread("Thread-1");
        t1.start();

        try {
            Thread.sleep(100);  // Small delay
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        // Method 2: Using Runnable interface
        System.out.println("\n--- Method 2: Implementing Runnable ---");
        MyRunnable r1 = new MyRunnable("Runnable-1");
        Thread t2 = new Thread(r1);
        t2.start();

        // Using lambda expression (Java 8+)
        System.out.println("\n--- Method 3: Using Lambda ---");
        Thread t3 = new Thread(() -> {
            System.out.println("Lambda-Thread started");
            for (int i = 1; i <= 5; i++) {
                System.out.println("Lambda-Thread: " + i);
                try {
                    Thread.sleep(500);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            System.out.println("Lambda-Thread finished");
        });
        t3.start();

        System.out.println("\nMain thread continues...");
    }
}
```

**Output:**

```
=== Thread Creation Demo ===

--- Method 1: Extending Thread ---
Thread-1 started
Thread-1: 1

--- Method 2: Implementing Runnable ---
Runnable-1 started
Runnable-1: 1

--- Method 3: Using Lambda ---
Lambda-Thread started
Lambda-Thread: 1

Main thread continues...
Thread-1: 2
Runnable-1: 2
Lambda-Thread: 2
Thread-1: 3
Runnable-1: 3
Lambda-Thread: 3
Thread-1: 4
Runnable-1: 4
Lambda-Thread: 4
Thread-1: 5
Runnable-1: 5
Lambda-Thread: 5
Thread-1 finished
Runnable-1 finished
Lambda-Thread finished
```

**Example 19.2: Synchronization**

```java
// SynchronizationDemo.java

// Without synchronization - causes data inconsistency
class Counter {
    private int count = 0;

    // Synchronized method
    synchronized void increment() {
        count++;
    }

    int getCount() {
        return count;
    }
}

class CounterThread extends Thread {
    private Counter counter;

    CounterThread(Counter counter) {
        this.counter = counter;
    }

    public void run() {
        for (int i = 0; i < 1000; i++) {
            counter.increment();
        }
    }
}

public class SynchronizationDemo {
    public static void main(String[] args) {
        System.out.println("=== Synchronization Demo ===\n");

        Counter counter = new Counter();

        // Create multiple threads
        CounterThread t1 = new CounterThread(counter);
        CounterThread t2 = new CounterThread(counter);
        CounterThread t3 = new CounterThread(counter);

        // Start threads
        t1.start();
        t2.start();
        t3.start();

        // Wait for all threads to complete
        try {
            t1.join();
            t2.join();
            t3.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("Final count: " + counter.getCount());
        System.out.println("Expected count: 3000");

        if (counter.getCount() == 3000) {
            System.out.println("✅ Synchronization working correctly!");
        } else {
            System.out.println("❌ Data inconsistency (remove synchronized to see this)");
        }
    }
}
```

**Output:**

```
=== Synchronization Demo ===

Final count: 3000
Expected count: 3000
✅ Synchronization working correctly!
```

**Example 19.3: Producer-Consumer Problem**

```java
// ProducerConsumerDemo.java
import java.util.LinkedList;
import java.util.Queue;

class SharedBuffer {
    private Queue<Integer> buffer = new LinkedList<>();
    private int capacity = 5;

    // Producer adds items
    synchronized void produce(int item) throws InterruptedException {
        while (buffer.size() == capacity) {
            System.out.println("Buffer full. Producer waiting...");
            wait();  // Wait until consumer consumes
        }

        buffer.add(item);
        System.out.println("Produced: " + item + " | Buffer size: " + buffer.size());

        notify();  // Notify consumer
        Thread.sleep(500);
    }

    // Consumer removes items
    synchronized int consume() throws InterruptedException {
        while (buffer.isEmpty()) {
            System.out.println("Buffer empty. Consumer waiting...");
            wait();  // Wait until producer produces
        }

        int item = buffer.poll();
        System.out.println("Consumed: " + item + " | Buffer size: " + buffer.size());

        notify();  // Notify producer
        Thread.sleep(1000);

        return item;
    }
}

class Producer extends Thread {
    private SharedBuffer buffer;

    Producer(SharedBuffer buffer) {
        this.buffer = buffer;
    }

    public void run() {
        try {
            for (int i = 1; i <= 10; i++) {
                buffer.produce(i);
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}

class Consumer extends Thread {
    private SharedBuffer buffer;

    Consumer(SharedBuffer buffer) {
        this.buffer = buffer;
    }

    public void run() {
        try {
            for (int i = 1; i <= 10; i++) {
                buffer.consume();
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}

public class ProducerConsumerDemo {
    public static void main(String[] args) {
        System.out.println("=== Producer-Consumer Demo ===\n");

        SharedBuffer buffer = new SharedBuffer();

        Producer producer = new Producer(buffer);
        Consumer consumer = new Consumer(buffer);

        producer.start();
        consumer.start();

        try {
            producer.join();
            consumer.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("\n✅ Producer-Consumer completed successfully!");
    }
}
```

**Output:**

```
=== Producer-Consumer Demo ===

Produced: 1 | Buffer size: 1
Produced: 2 | Buffer size: 2
Consumed: 1 | Buffer size: 1
Produced: 3 | Buffer size: 2
Produced: 4 | Buffer size: 3
Consumed: 2 | Buffer size: 2
Produced: 5 | Buffer size: 3
Produced: 6 | Buffer size: 4
Consumed: 3 | Buffer size: 3
Produced: 7 | Buffer size: 4
Produced: 8 | Buffer size: 5
Buffer full. Producer waiting...
Consumed: 4 | Buffer size: 4
Produced: 9 | Buffer size: 5
Buffer full. Producer waiting...
Consumed: 5 | Buffer size: 4
Produced: 10 | Buffer size: 5
Consumed: 6 | Buffer size: 4
Consumed: 7 | Buffer size: 3
Consumed: 8 | Buffer size: 2
Consumed: 9 | Buffer size: 1
Consumed: 10 | Buffer size: 0

✅ Producer-Consumer completed successfully!
```

**Example 19.4: Thread Pool with ExecutorService**

```java
// ThreadPoolDemo.java
import java.util.concurrent.*;

class Task implements Runnable {
    private int taskId;

    Task(int id) {
        this.taskId = id;
    }

    public void run() {
        System.out.println("Task " + taskId + " started by " +
                          Thread.currentThread().getName());
        try {
            Thread.sleep(2000);  // Simulate work
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        System.out.println("Task " + taskId + " completed by " +
                          Thread.currentThread().getName());
    }
}

public class ThreadPoolDemo {
    public static void main(String[] args) {
        System.out.println("=== Thread Pool Demo ===\n");

        // Create thread pool with 3 threads
        ExecutorService executor = Executors.newFixedThreadPool(3);

        System.out.println("Submitting 6 tasks to thread pool with 3 threads\n");

        // Submit 6 tasks
        for (int i = 1; i <= 6; i++) {
            executor.execute(new Task(i));
        }

        // Shutdown executor
        executor.shutdown();

        try {
            // Wait for all tasks to complete
            if (executor.awaitTermination(1, TimeUnit.MINUTES)) {
                System.out.println("\n✅ All tasks completed!");
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```

**Output:**

```
=== Thread Pool Demo ===

Submitting 6 tasks to thread pool with 3 threads

Task 1 started by pool-1-thread-1
Task 2 started by pool-1-thread-2
Task 3 started by pool-1-thread-3
Task 1 completed by pool-1-thread-1
Task 4 started by pool-1-thread-1
Task 2 completed by pool-1-thread-2
Task 5 started by pool-1-thread-2
Task 3 completed by pool-1-thread-3
Task 6 started by pool-1-thread-3
Task 4 completed by pool-1-thread-1
Task 5 completed by pool-1-thread-2
Task 6 completed by pool-1-thread-3

✅ All tasks completed!
```

### 🎯 Key Takeaways

- Multithreading allows concurrent execution of multiple threads
- Create threads by extending Thread class or implementing Runnable interface
- Runnable interface is preferred (better design, flexibility)
- Use synchronization to prevent thread interference
- wait(), notify(), notifyAll() enable inter-thread communication
- Avoid deadlock by proper lock ordering
- Thread pools improve performance by reusing threads
- volatile ensures visibility, synchronized ensures atomicity
- Daemon threads run in background and don't prevent JVM exit

### 📝 Practice Questions

1. What is the difference between process and thread?
2. Why is implementing Runnable preferred over extending Thread?
3. What is synchronization and why is it needed?
4. Explain the producer-consumer problem.
5. Write a program to demonstrate deadlock and how to avoid it.

---

## Chapter 20: Java 8 Features

### 📘 Theory

#### **20.1 What's New in Java 8?**

**Java 8** (released in March 2014) was a major release that introduced several revolutionary features to make Java more functional, concise, and expressive.

**Major Features:**

- ✅ **Lambda Expressions** - Functional programming support
- ✅ **Functional Interfaces** - Single abstract method interfaces
- ✅ **Stream API** - Process collections declaratively
- ✅ **Method References** - Shorthand for lambda expressions
- ✅ **Default Methods** - Interface methods with implementation
- ✅ **Optional Class** - Handle null values elegantly
- ✅ **Date/Time API** - New comprehensive date-time library
- ✅ **forEach() Method** - Iterate collections easily

**Why Java 8?**

- More concise and readable code
- Better support for parallel processing
- Functional programming paradigm
- Improved performance

#### **20.2 Lambda Expressions**

**Lambda Expression** is an anonymous function (function without name) that can be passed as an argument or stored in a variable.

**Syntax:**

```java
(parameters) -> expression
// or
(parameters) -> { statements; }
```

**Examples:**

```java
// No parameters
() -> System.out.println("Hello")

// One parameter (parentheses optional)
x -> x * x
(x) -> x * x

// Multiple parameters
(x, y) -> x + y

// Multiple statements
(x, y) -> {
    int sum = x + y;
    return sum;
}
```

**Before Java 8 (Anonymous Class):**

```java
Runnable r = new Runnable() {
    public void run() {
        System.out.println("Running");
    }
};
```

**After Java 8 (Lambda):**

```java
Runnable r = () -> System.out.println("Running");
```

**Benefits:**

- ✅ Less boilerplate code
- ✅ More readable
- ✅ Enables functional programming
- ✅ Better support for parallel processing

#### **20.3 Functional Interfaces**

**Functional Interface** is an interface with exactly one abstract method. It can have multiple default or static methods.

**@FunctionalInterface Annotation:**

```java
@FunctionalInterface
interface Calculator {
    int calculate(int a, int b);  // Single abstract method

    // Can have default methods
    default void print() {
        System.out.println("Calculator");
    }

    // Can have static methods
    static void info() {
        System.out.println("Performs calculations");
    }
}
```

**Built-in Functional Interfaces (java.util.function):**

| Interface               | Method                | Description                        |
| ----------------------- | --------------------- | ---------------------------------- |
| **Predicate\<T>**       | `boolean test(T t)`   | Tests a condition                  |
| **Function<T, R>**      | `R apply(T t)`        | Transforms input to output         |
| **Consumer\<T>**        | `void accept(T t)`    | Consumes input (no return)         |
| **Supplier\<T>**        | `T get()`             | Supplies a value (no input)        |
| **BiFunction<T, U, R>** | `R apply(T t, U u)`   | Two inputs, one output             |
| **UnaryOperator\<T>**   | `T apply(T t)`        | Single input/output (same type)    |
| **BinaryOperator\<T>**  | `T apply(T t1, T t2)` | Two inputs, one output (same type) |

**Examples:**

```java
// Predicate - test condition
Predicate<Integer> isEven = x -> x % 2 == 0;
System.out.println(isEven.test(4));  // true

// Function - transform
Function<String, Integer> length = s -> s.length();
System.out.println(length.apply("Hello"));  // 5

// Consumer - consume
Consumer<String> print = s -> System.out.println(s);
print.accept("Hello");  // Hello

// Supplier - supply
Supplier<Double> random = () -> Math.random();
System.out.println(random.get());  // Random number
```

#### **20.4 Stream API**

**Stream** is a sequence of elements that supports sequential and parallel aggregate operations.

**Key Features:**

- Not a data structure (doesn't store data)
- Functional in nature (doesn't modify source)
- Lazy evaluation (intermediate operations)
- Can be consumed only once

**Creating Streams:**

```java
// From collection
List<String> list = Arrays.asList("a", "b", "c");
Stream<String> stream1 = list.stream();

// From array
String[] array = {"a", "b", "c"};
Stream<String> stream2 = Arrays.stream(array);

// Using Stream.of()
Stream<String> stream3 = Stream.of("a", "b", "c");

// Infinite stream
Stream<Integer> stream4 = Stream.iterate(0, n -> n + 1);
```

**Stream Operations:**

**1. Intermediate Operations (return Stream):**

- `filter()` - Filter elements
- `map()` - Transform elements
- `flatMap()` - Flatten nested streams
- `distinct()` - Remove duplicates
- `sorted()` - Sort elements
- `limit()` - Limit size
- `skip()` - Skip elements

**2. Terminal Operations (return result):**

- `forEach()` - Iterate elements
- `collect()` - Collect to collection
- `reduce()` - Reduce to single value
- `count()` - Count elements
- `anyMatch()` - Check if any match
- `allMatch()` - Check if all match
- `noneMatch()` - Check if none match
- `findFirst()` - Find first element
- `findAny()` - Find any element

**Example:**

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

// Filter even numbers, square them, and collect
List<Integer> result = numbers.stream()
    .filter(n -> n % 2 == 0)      // 2, 4, 6, 8, 10
    .map(n -> n * n)              // 4, 16, 36, 64, 100
    .collect(Collectors.toList());

System.out.println(result);  // [4, 16, 36, 64, 100]
```

#### **20.5 Method References**

**Method Reference** is a shorthand notation of a lambda expression to call a method.

**Types of Method References:**

**1. Static Method Reference:**

```java
// Lambda
Function<String, Integer> f1 = s -> Integer.parseInt(s);

// Method reference
Function<String, Integer> f2 = Integer::parseInt;
```

**2. Instance Method Reference (on particular object):**

```java
String str = "Hello";

// Lambda
Supplier<Integer> s1 = () -> str.length();

// Method reference
Supplier<Integer> s2 = str::length;
```

**3. Instance Method Reference (on arbitrary object):**

```java
// Lambda
Function<String, String> f1 = s -> s.toUpperCase();

// Method reference
Function<String, String> f2 = String::toUpperCase;
```

**4. Constructor Reference:**

```java
// Lambda
Supplier<ArrayList<String>> s1 = () -> new ArrayList<>();

// Constructor reference
Supplier<ArrayList<String>> s2 = ArrayList::new;
```

**Syntax:**

```
ClassName::methodName
objectName::methodName
ClassName::new
```

#### **20.6 Default Methods in Interfaces**

**Default methods** allow you to add new methods to interfaces without breaking existing implementations.

**Syntax:**

```java
interface MyInterface {
    // Abstract method
    void abstractMethod();

    // Default method
    default void defaultMethod() {
        System.out.println("Default implementation");
    }
}
```

**Example:**

```java
interface Vehicle {
    void start();

    default void stop() {
        System.out.println("Vehicle stopped");
    }
}

class Car implements Vehicle {
    public void start() {
        System.out.println("Car started");
    }
    // Can use default stop() or override it
}
```

**Why Default Methods?**

- ✅ Backward compatibility (add methods without breaking code)
- ✅ Optional methods (provide default implementation)
- ✅ Multiple inheritance of behavior

#### **20.7 Optional Class**

**Optional** is a container object that may or may not contain a non-null value. It helps avoid NullPointerException.

**Creating Optional:**

```java
// Empty optional
Optional<String> empty = Optional.empty();

// Optional with value
Optional<String> opt1 = Optional.of("Hello");

// Optional with nullable value
Optional<String> opt2 = Optional.ofNullable(null);
```

**Common Methods:**

```java
Optional<String> opt = Optional.of("Hello");

// Check if value present
opt.isPresent();  // true
opt.isEmpty();    // false (Java 11+)

// Get value
opt.get();  // "Hello" (throws exception if empty)

// Get with default
opt.orElse("Default");  // "Hello"
opt.orElseGet(() -> "Default");  // "Hello"

// Execute if present
opt.ifPresent(s -> System.out.println(s));  // Hello

// Map value
opt.map(String::toUpperCase);  // Optional["HELLO"]

// Filter
opt.filter(s -> s.length() > 3);  // Optional["Hello"]
```

**Example:**

```java
// Before Java 8
public String getName(User user) {
    if (user != null) {
        return user.getName();
    }
    return "Unknown";
}

// After Java 8
public String getName(Optional<User> user) {
    return user.map(User::getName)
               .orElse("Unknown");
}
```

#### **20.8 forEach() Method**

**forEach()** method iterates over collections using lambda expressions.

**Syntax:**

```java
collection.forEach(element -> {
    // Process element
});
```

**Examples:**

```java
List<String> list = Arrays.asList("A", "B", "C");

// Using forEach with lambda
list.forEach(s -> System.out.println(s));

// Using forEach with method reference
list.forEach(System.out::println);

// Map forEach
Map<String, Integer> map = new HashMap<>();
map.put("A", 1);
map.put("B", 2);

map.forEach((key, value) -> {
    System.out.println(key + ": " + value);
});
```

#### **20.9 New Date/Time API (java.time)**

Java 8 introduced a new comprehensive Date/Time API to replace the old `java.util.Date` and `java.util.Calendar`.

**Main Classes:**

| Class             | Description                             |
| ----------------- | --------------------------------------- |
| **LocalDate**     | Date without time (2024-01-15)          |
| **LocalTime**     | Time without date (10:30:45)            |
| **LocalDateTime** | Date and time (2024-01-15T10:30:45)     |
| **ZonedDateTime** | Date, time with timezone                |
| **Instant**       | Timestamp (seconds since epoch)         |
| **Duration**      | Time-based amount (hours, minutes)      |
| **Period**        | Date-based amount (years, months, days) |

**Examples:**

```java
// Current date
LocalDate today = LocalDate.now();
System.out.println(today);  // 2024-01-15

// Specific date
LocalDate date = LocalDate.of(2024, 1, 15);

// Current time
LocalTime time = LocalTime.now();
System.out.println(time);  // 10:30:45.123

// Current date-time
LocalDateTime dateTime = LocalDateTime.now();

// Parse date
LocalDate parsed = LocalDate.parse("2024-01-15");

// Date arithmetic
LocalDate tomorrow = today.plusDays(1);
LocalDate nextMonth = today.plusMonths(1);

// Get components
int year = today.getYear();
int month = today.getMonthValue();
int day = today.getDayOfMonth();

// Format date
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd-MM-yyyy");
String formatted = today.format(formatter);
```

**Benefits:**

- ✅ Immutable and thread-safe
- ✅ Clear and expressive API
- ✅ Better timezone support
- ✅ No more confusion with months (1-12, not 0-11)

#### **20.10 Collectors**

**Collectors** are used with Stream API to collect results into collections or other data structures.

**Common Collectors:**

```java
List<String> list = Arrays.asList("A", "B", "C", "A");

// To List
List<String> result1 = list.stream()
    .collect(Collectors.toList());

// To Set (removes duplicates)
Set<String> result2 = list.stream()
    .collect(Collectors.toSet());

// To Map
Map<String, Integer> result3 = list.stream()
    .collect(Collectors.toMap(s -> s, s -> s.length()));

// Joining strings
String result4 = list.stream()
    .collect(Collectors.joining(", "));  // "A, B, C, A"

// Counting
long count = list.stream()
    .collect(Collectors.counting());

// Grouping
Map<Integer, List<String>> grouped = list.stream()
    .collect(Collectors.groupingBy(String::length));

// Partitioning
Map<Boolean, List<Integer>> partitioned =
    Arrays.asList(1, 2, 3, 4, 5).stream()
    .collect(Collectors.partitioningBy(n -> n % 2 == 0));
```

### 💻 Practical Examples

**Example 20.1: Lambda Expressions**

```java
// LambdaDemo.java
import java.util.*;

@FunctionalInterface
interface Calculator {
    int calculate(int a, int b);
}

public class LambdaDemo {
    public static void main(String[] args) {
        System.out.println("=== Lambda Expressions Demo ===\n");

        // Lambda expressions for different operations
        Calculator add = (a, b) -> a + b;
        Calculator subtract = (a, b) -> a - b;
        Calculator multiply = (a, b) -> a * b;
        Calculator divide = (a, b) -> a / b;

        int x = 10, y = 5;

        System.out.println("--- Basic Operations ---");
        System.out.println(x + " + " + y + " = " + add.calculate(x, y));
        System.out.println(x + " - " + y + " = " + subtract.calculate(x, y));
        System.out.println(x + " * " + y + " = " + multiply.calculate(x, y));
        System.out.println(x + " / " + y + " = " + divide.calculate(x, y));

        System.out.println();

        // Lambda with Runnable
        System.out.println("--- Lambda with Runnable ---");
        Runnable task = () -> {
            System.out.println("Task running in thread: " +
                             Thread.currentThread().getName());
        };

        Thread thread = new Thread(task);
        thread.start();

        System.out.println();

        // Lambda with Comparator
        System.out.println("--- Lambda with Comparator ---");
        List<String> names = Arrays.asList("John", "Alice", "Bob", "Charlie");

        System.out.println("Original: " + names);

        // Sort by length
        names.sort((s1, s2) -> s1.length() - s2.length());
        System.out.println("Sorted by length: " + names);

        // Sort alphabetically
        names.sort((s1, s2) -> s1.compareTo(s2));
        System.out.println("Sorted alphabetically: " + names);
    }
}
```

**Output:**

```
=== Lambda Expressions Demo ===

--- Basic Operations ---
10 + 5 = 15
10 - 5 = 5
10 * 5 = 50
10 / 5 = 2

--- Lambda with Runnable ---
Task running in thread: Thread-0

--- Lambda with Comparator ---
Original: [John, Alice, Bob, Charlie]
Sorted by length: [Bob, John, Alice, Charlie]
Sorted alphabetically: [Alice, Bob, Charlie, John]
```

**Example 20.2: Stream API**

```java
// StreamAPIDemo.java
import java.util.*;
import java.util.stream.*;

public class StreamAPIDemo {
    public static void main(String[] args) {
        System.out.println("=== Stream API Demo ===\n");

        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        // Filter even numbers
        System.out.println("--- Filter Even Numbers ---");
        List<Integer> evenNumbers = numbers.stream()
            .filter(n -> n % 2 == 0)
            .collect(Collectors.toList());
        System.out.println("Even numbers: " + evenNumbers);

        System.out.println();

        // Map - square each number
        System.out.println("--- Map - Square Numbers ---");
        List<Integer> squares = numbers.stream()
            .map(n -> n * n)
            .collect(Collectors.toList());
        System.out.println("Squares: " + squares);

        System.out.println();

        // Filter and Map combined
        System.out.println("--- Filter + Map ---");
        List<Integer> evenSquares = numbers.stream()
            .filter(n -> n % 2 == 0)
            .map(n -> n * n)
            .collect(Collectors.toList());
        System.out.println("Even number squares: " + evenSquares);

        System.out.println();

        // Reduce - sum of all numbers
        System.out.println("--- Reduce - Sum ---");
        int sum = numbers.stream()
            .reduce(0, (a, b) -> a + b);
        System.out.println("Sum: " + sum);

        System.out.println();

        // Count
        System.out.println("--- Count ---");
        long count = numbers.stream()
            .filter(n -> n > 5)
            .count();
        System.out.println("Numbers greater than 5: " + count);

        System.out.println();

        // Min and Max
        System.out.println("--- Min and Max ---");
        Optional<Integer> min = numbers.stream().min(Integer::compareTo);
        Optional<Integer> max = numbers.stream().max(Integer::compareTo);
        System.out.println("Min: " + min.orElse(0));
        System.out.println("Max: " + max.orElse(0));

        System.out.println();

        // Distinct
        System.out.println("--- Distinct ---");
        List<Integer> duplicates = Arrays.asList(1, 2, 2, 3, 3, 3, 4, 4, 5);
        List<Integer> unique = duplicates.stream()
            .distinct()
            .collect(Collectors.toList());
        System.out.println("Original: " + duplicates);
        System.out.println("Unique: " + unique);

        System.out.println();

        // Sorted
        System.out.println("--- Sorted ---");
        List<Integer> unsorted = Arrays.asList(5, 2, 8, 1, 9, 3);
        List<Integer> sorted = unsorted.stream()
            .sorted()
            .collect(Collectors.toList());
        System.out.println("Unsorted: " + unsorted);
        System.out.println("Sorted: " + sorted);

        System.out.println();

        // anyMatch, allMatch, noneMatch
        System.out.println("--- Match Operations ---");
        boolean anyEven = numbers.stream().anyMatch(n -> n % 2 == 0);
        boolean allPositive = numbers.stream().allMatch(n -> n > 0);
        boolean noneNegative = numbers.stream().noneMatch(n -> n < 0);

        System.out.println("Any even? " + anyEven);
        System.out.println("All positive? " + allPositive);
        System.out.println("None negative? " + noneNegative);
    }
}
```

**Output:**

```
=== Stream API Demo ===

--- Filter Even Numbers ---
Even numbers: [2, 4, 6, 8, 10]

--- Map - Square Numbers ---
Squares: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

--- Filter + Map ---
Even number squares: [4, 16, 36, 64, 100]

--- Reduce - Sum ---
Sum: 55

--- Count ---
Numbers greater than 5: 5

--- Min and Max ---
Min: 1
Max: 10

--- Distinct ---
Original: [1, 2, 2, 3, 3, 3, 4, 4, 5]
Unique: [1, 2, 3, 4, 5]

--- Sorted ---
Unsorted: [5, 2, 8, 1, 9, 3]
Sorted: [1, 2, 3, 5, 8, 9]

--- Match Operations ---
Any even? true
All positive? true
None negative? true
```

**Example 20.3: Optional Class**

```java
// OptionalDemo.java
import java.util.*;

class User {
    private String name;
    private String email;

    public User(String name, String email) {
        this.name = name;
        this.email = email;
    }

    public String getName() { return name; }
    public String getEmail() { return email; }
}

public class OptionalDemo {
    public static void main(String[] args) {
        System.out.println("=== Optional Class Demo ===\n");

        // Creating Optional
        System.out.println("--- Creating Optional ---");
        Optional<String> opt1 = Optional.of("Hello");
        Optional<String> opt2 = Optional.ofNullable(null);
        Optional<String> opt3 = Optional.empty();

        System.out.println("opt1 present: " + opt1.isPresent());
        System.out.println("opt2 present: " + opt2.isPresent());
        System.out.println("opt3 present: " + opt3.isPresent());

        System.out.println();

        // Getting values
        System.out.println("--- Getting Values ---");
        System.out.println("opt1 value: " + opt1.get());
        System.out.println("opt2 with default: " + opt2.orElse("Default"));
        System.out.println("opt3 with supplier: " +
                          opt3.orElseGet(() -> "Generated Default"));

        System.out.println();

        // ifPresent
        System.out.println("--- ifPresent ---");
        opt1.ifPresent(s -> System.out.println("Value: " + s));
        opt2.ifPresent(s -> System.out.println("This won't print"));

        System.out.println();

        // map and filter
        System.out.println("--- map and filter ---");
        Optional<String> upper = opt1.map(String::toUpperCase);
        System.out.println("Uppercase: " + upper.get());

        Optional<String> filtered = opt1.filter(s -> s.length() > 3);
        System.out.println("Filtered (length > 3): " + filtered.orElse("Not found"));

        System.out.println();

        // Practical example - User
        System.out.println("--- Practical Example ---");
        Optional<User> user1 = Optional.of(new User("John", "john@example.com"));
        Optional<User> user2 = Optional.empty();

        String name1 = user1.map(User::getName).orElse("Unknown");
        String name2 = user2.map(User::getName).orElse("Unknown");

        System.out.println("User 1 name: " + name1);
        System.out.println("User 2 name: " + name2);

        // Chain operations
        String email = user1
            .filter(u -> u.getName().startsWith("J"))
            .map(User::getEmail)
            .map(String::toUpperCase)
            .orElse("NO EMAIL");

        System.out.println("User 1 email: " + email);
    }
}
```

**Output:**

```
=== Optional Class Demo ===

--- Creating Optional ---
opt1 present: true
opt2 present: false
opt3 present: false

--- Getting Values ---
opt1 value: Hello
opt2 with default: Default
opt3 with supplier: Generated Default

--- ifPresent ---
Value: Hello

--- map and filter ---
Uppercase: HELLO
Filtered (length > 3): Hello

--- Practical Example ---
User 1 name: John
User 2 name: Unknown
User 1 email: JOHN@EXAMPLE.COM
```

**Example 20.4: Date/Time API**

```java
// DateTimeAPIDemo.java
import java.time.*;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;

public class DateTimeAPIDemo {
    public static void main(String[] args) {
        System.out.println("=== Date/Time API Demo ===\n");

        // LocalDate
        System.out.println("--- LocalDate ---");
        LocalDate today = LocalDate.now();
        LocalDate specificDate = LocalDate.of(2024, 1, 15);

        System.out.println("Today: " + today);
        System.out.println("Specific date: " + specificDate);
        System.out.println("Year: " + today.getYear());
        System.out.println("Month: " + today.getMonth());
        System.out.println("Day: " + today.getDayOfMonth());

        System.out.println();

        // LocalTime
        System.out.println("--- LocalTime ---");
        LocalTime now = LocalTime.now();
        LocalTime specificTime = LocalTime.of(10, 30, 45);

        System.out.println("Current time: " + now);
        System.out.println("Specific time: " + specificTime);

        System.out.println();

        // LocalDateTime
        System.out.println("--- LocalDateTime ---");
        LocalDateTime dateTime = LocalDateTime.now();
        System.out.println("Current date-time: " + dateTime);

        System.out.println();

        // Date arithmetic
        System.out.println("--- Date Arithmetic ---");
        LocalDate tomorrow = today.plusDays(1);
        LocalDate nextWeek = today.plusWeeks(1);
        LocalDate nextMonth = today.plusMonths(1);
        LocalDate nextYear = today.plusYears(1);

        System.out.println("Tomorrow: " + tomorrow);
        System.out.println("Next week: " + nextWeek);
        System.out.println("Next month: " + nextMonth);
        System.out.println("Next year: " + nextYear);

        System.out.println();

        // Period - date-based
        System.out.println("--- Period ---");
        LocalDate birthDate = LocalDate.of(2000, 1, 15);
        Period age = Period.between(birthDate, today);
        System.out.println("Age: " + age.getYears() + " years, " +
                          age.getMonths() + " months, " +
                          age.getDays() + " days");

        System.out.println();

        // Duration - time-based
        System.out.println("--- Duration ---");
        LocalTime start = LocalTime.of(9, 0);
        LocalTime end = LocalTime.of(17, 30);
        Duration duration = Duration.between(start, end);
        System.out.println("Work hours: " + duration.toHours() + " hours");

        System.out.println();

        // Formatting
        System.out.println("--- Formatting ---");
        DateTimeFormatter formatter1 = DateTimeFormatter.ofPattern("dd-MM-yyyy");
        DateTimeFormatter formatter2 = DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm:ss");

        String formatted1 = today.format(formatter1);
        String formatted2 = dateTime.format(formatter2);

        System.out.println("Formatted date: " + formatted1);
        System.out.println("Formatted date-time: " + formatted2);

        System.out.println();

        // Parsing
        System.out.println("--- Parsing ---");
        LocalDate parsed = LocalDate.parse("15-01-2024", formatter1);
        System.out.println("Parsed date: " + parsed);

        System.out.println();

        // Comparison
        System.out.println("--- Comparison ---");
        LocalDate date1 = LocalDate.of(2024, 1, 15);
        LocalDate date2 = LocalDate.of(2024, 1, 20);

        System.out.println("date1 before date2: " + date1.isBefore(date2));
        System.out.println("date1 after date2: " + date1.isAfter(date2));
        System.out.println("date1 equals date2: " + date1.isEqual(date2));
    }
}
```

**Output:**

```
=== Date/Time API Demo ===

--- LocalDate ---
Today: 2024-11-27
Specific date: 2024-01-15
Year: 2024
Month: NOVEMBER
Day: 27

--- LocalTime ---
Current time: 14:30:45.123456
Specific time: 10:30:45

--- LocalDateTime ---
Current date-time: 2024-11-27T14:30:45.123456

--- Date Arithmetic ---
Tomorrow: 2024-11-28
Next week: 2024-12-04
Next month: 2024-12-27
Next year: 2025-11-27

--- Period ---
Age: 24 years, 10 months, 12 days

--- Duration ---
Work hours: 8 hours

--- Formatting ---
Formatted date: 27-11-2024
Formatted date-time: 27/11/2024 14:30:45

--- Parsing ---
Parsed date: 2024-01-15

--- Comparison ---
date1 before date2: true
date1 after date2: false
date1 equals date2: false
```

### 🎯 Key Takeaways

- Lambda expressions enable functional programming in Java
- Functional interfaces have exactly one abstract method
- Stream API provides declarative way to process collections
- Method references are shorthand for lambda expressions
- Default methods allow adding methods to interfaces without breaking code
- Optional helps avoid NullPointerException
- New Date/Time API is immutable, thread-safe, and comprehensive
- Collectors help gather stream results into collections

### 📝 Practice Questions

1. What is a lambda expression and how is it different from anonymous class?
2. What is a functional interface? Name 5 built-in functional interfaces.
3. Explain the difference between intermediate and terminal operations in Stream API.
4. What is the purpose of Optional class?
5. Write a program using Stream API to find sum of squares of even numbers from a list.

---

## Chapter 21: Java 11 Features

### 📘 Theory

#### **21.1 What's New in Java 11?**

**Java 11** (released in September 2018) is a Long-Term Support (LTS) release that introduced several useful features and improvements.

**Major Features:**

- ✅ **Local Variable Syntax for Lambda** - Use `var` in lambda parameters
- ✅ **New String Methods** - isBlank(), lines(), strip(), repeat()
- ✅ **New File Methods** - readString(), writeString()
- ✅ **HTTP Client API** - New standard HTTP client
- ✅ **Running Java Files Directly** - Execute .java files without compilation
- ✅ **Optional Enhancements** - isEmpty() method
- ✅ **Collection to Array** - toArray() with generator
- ✅ **Predicate.not()** - Negate predicates easily

**Why Java 11?**

- Long-Term Support (LTS) version
- Production-ready features
- Better performance
- Simplified development

#### **21.2 Local Variable Syntax for Lambda Parameters**

Java 11 allows using `var` keyword in lambda parameters, enabling annotations on lambda parameters.

**Syntax:**

```java
// Before Java 11
BiFunction<String, String, String> concat = (s1, s2) -> s1 + s2;

// Java 11 - with var
BiFunction<String, String, String> concat = (var s1, var s2) -> s1 + s2;

// With annotations
BiFunction<String, String, String> concat =
    (@NonNull var s1, @NonNull var s2) -> s1 + s2;
```

**Benefits:**

- ✅ Consistent with local variable syntax
- ✅ Allows annotations on lambda parameters
- ✅ Better readability in some cases

**Example:**

```java
List<String> list = Arrays.asList("Java", "Python", "C++");

// Using var in lambda
list.forEach((var item) -> System.out.println(item));

// Can mix with annotations
list.stream()
    .map((@NonNull var s) -> s.toUpperCase())
    .forEach(System.out::println);
```

#### **21.3 New String Methods**

Java 11 added several useful methods to the String class.

**1. isBlank() - Check if string is empty or contains only whitespace**

```java
String str1 = "";
String str2 = "   ";
String str3 = "Hello";

str1.isBlank();  // true
str2.isBlank();  // true
str3.isBlank();  // false
```

**2. lines() - Split string into lines as Stream**

```java
String multiline = "Line 1\nLine 2\nLine 3";

multiline.lines()
    .forEach(System.out::println);
// Output:
// Line 1
// Line 2
// Line 3
```

**3. strip(), stripLeading(), stripTrailing() - Remove whitespace**

```java
String str = "  Hello World  ";

str.strip();          // "Hello World"
str.stripLeading();   // "Hello World  "
str.stripTrailing();  // "  Hello World"

// Difference from trim(): strip() handles Unicode whitespace
String unicode = "\u2000Hello\u2000";
unicode.trim();   // Still has Unicode spaces
unicode.strip();  // Removes Unicode spaces
```

**4. repeat() - Repeat string n times**

```java
String str = "Java";

str.repeat(3);  // "JavaJavaJava"
"*".repeat(10); // "**********"
```

**Comparison Table:**

| Method        | Description                        | Example                   |
| ------------- | ---------------------------------- | ------------------------- |
| **isBlank()** | Check if empty or whitespace       | `"  ".isBlank()` → true   |
| **lines()**   | Split into lines                   | `"a\nb".lines()` → Stream |
| **strip()**   | Remove leading/trailing whitespace | `" Hi ".strip()` → "Hi"   |
| **repeat(n)** | Repeat n times                     | `"ab".repeat(2)` → "abab" |

#### **21.4 New File Methods**

Java 11 added convenient methods to read and write files as strings.

**1. Files.readString() - Read file content as String**

```java
import java.nio.file.*;

// Read entire file as String
String content = Files.readString(Path.of("file.txt"));
System.out.println(content);

// With specific charset
String content = Files.readString(Path.of("file.txt"), StandardCharsets.UTF_8);
```

**2. Files.writeString() - Write String to file**

```java
// Write string to file
Files.writeString(Path.of("output.txt"), "Hello, World!");

// With options
Files.writeString(
    Path.of("output.txt"),
    "Appended text\n",
    StandardOpenOption.APPEND
);
```

**Benefits:**

- ✅ Simpler than BufferedReader/BufferedWriter
- ✅ Less boilerplate code
- ✅ Handles resources automatically

**Before Java 11:**

```java
// Reading file
StringBuilder content = new StringBuilder();
try (BufferedReader reader = new BufferedReader(new FileReader("file.txt"))) {
    String line;
    while ((line = reader.readLine()) != null) {
        content.append(line).append("\n");
    }
}
```

**After Java 11:**

```java
// Reading file
String content = Files.readString(Path.of("file.txt"));
```

#### **21.5 HTTP Client API (Standard)**

Java 11 standardized the HTTP Client API (introduced as incubator in Java 9).

**Key Features:**

- Supports HTTP/1.1 and HTTP/2
- Synchronous and asynchronous requests
- WebSocket support
- Better performance than HttpURLConnection

**Creating HTTP Client:**

```java
import java.net.http.*;
import java.net.*;

HttpClient client = HttpClient.newHttpClient();

// With custom configuration
HttpClient client = HttpClient.newBuilder()
    .version(HttpClient.Version.HTTP_2)
    .connectTimeout(Duration.ofSeconds(10))
    .build();
```

**Synchronous GET Request:**

```java
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/data"))
    .GET()
    .build();

HttpResponse<String> response = client.send(
    request,
    HttpResponse.BodyHandlers.ofString()
);

System.out.println("Status: " + response.statusCode());
System.out.println("Body: " + response.body());
```

**Asynchronous GET Request:**

```java
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/data"))
    .build();

client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
    .thenApply(HttpResponse::body)
    .thenAccept(System.out::println)
    .join();
```

**POST Request:**

```java
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.example.com/data"))
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString("{\"name\":\"John\"}"))
    .build();

HttpResponse<String> response = client.send(
    request,
    HttpResponse.BodyHandlers.ofString()
);
```

#### **21.6 Running Java Files Directly**

Java 11 allows running single-file Java programs without explicit compilation.

**Before Java 11:**

```bash
javac HelloWorld.java
java HelloWorld
```

**Java 11:**

```bash
java HelloWorld.java
```

**Benefits:**

- ✅ Faster for simple scripts
- ✅ No .class files generated
- ✅ Great for learning and testing

**Example:**

```java
// HelloWorld.java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

**Run directly:**

```bash
java HelloWorld.java
# Output: Hello, World!
```

**With arguments:**

```bash
java HelloWorld.java arg1 arg2
```

**Limitations:**

- Only works with single-file programs
- File must contain a main method
- Cannot use external dependencies easily

#### **21.7 Optional Enhancements**

Java 11 added the `isEmpty()` method to Optional class.

**isEmpty() - Check if Optional is empty**

```java
Optional<String> opt1 = Optional.of("Hello");
Optional<String> opt2 = Optional.empty();

// Java 11
opt1.isEmpty();  // false
opt2.isEmpty();  // true

// Before Java 11 (using negation)
!opt1.isPresent();  // false
!opt2.isPresent();  // true
```

**Benefits:**

- ✅ More readable than `!isPresent()`
- ✅ Clearer intent

**Example:**

```java
Optional<String> result = findUser("john");

if (result.isEmpty()) {
    System.out.println("User not found");
} else {
    System.out.println("User: " + result.get());
}
```

#### **21.8 Collection to Array Enhancement**

Java 11 added `toArray(IntFunction)` method to Collection interface.

**Before Java 11:**

```java
List<String> list = Arrays.asList("A", "B", "C");

// Need to specify array size
String[] array = list.toArray(new String[list.size()]);

// Or use zero-length array
String[] array = list.toArray(new String[0]);
```

**Java 11:**

```java
List<String> list = Arrays.asList("A", "B", "C");

// Using method reference
String[] array = list.toArray(String[]::new);
```

**Benefits:**

- ✅ More concise
- ✅ Type-safe
- ✅ Better performance

#### **21.9 Predicate.not() Method**

Java 11 added static `not()` method to Predicate interface for negation.

**Before Java 11:**

```java
List<String> list = Arrays.asList("", "Java", "", "Python", "");

// Filter non-blank strings
list.stream()
    .filter(s -> !s.isBlank())
    .forEach(System.out::println);
```

**Java 11:**

```java
import static java.util.function.Predicate.not;

List<String> list = Arrays.asList("", "Java", "", "Python", "");

// Using Predicate.not()
list.stream()
    .filter(not(String::isBlank))
    .forEach(System.out::println);
```

**Benefits:**

- ✅ More readable with method references
- ✅ Cleaner code
- ✅ Functional style

**More Examples:**

```java
// Filter non-null values
list.stream()
    .filter(not(Objects::isNull))
    .forEach(System.out::println);

// Filter non-empty strings
list.stream()
    .filter(not(String::isEmpty))
    .forEach(System.out::println);
```

#### **21.10 Other Notable Changes**

**1. Epsilon Garbage Collector**

- No-op garbage collector for testing
- Useful for performance testing

**2. Nest-Based Access Control**

- Better support for nested classes
- Improved reflection

**3. Dynamic Class-File Constants**

- Performance improvements
- Better constant pool handling

**4. Removed Modules**

- Java EE and CORBA modules removed
- Need to add as dependencies if needed

### 💻 Practical Examples

**Example 21.1: New String Methods**

```java
// StringMethodsDemo.java
import java.util.stream.Collectors;

public class StringMethodsDemo {
    public static void main(String[] args) {
        System.out.println("=== Java 11 String Methods Demo ===\n");

        // isBlank()
        System.out.println("--- isBlank() ---");
        String str1 = "";
        String str2 = "   ";
        String str3 = "Hello";

        System.out.println("\"\" is blank: " + str1.isBlank());
        System.out.println("\"   \" is blank: " + str2.isBlank());
        System.out.println("\"Hello\" is blank: " + str3.isBlank());

        System.out.println();

        // lines()
        System.out.println("--- lines() ---");
        String multiline = "Java\nPython\nC++\nJavaScript";

        System.out.println("Original string:");
        System.out.println(multiline);
        System.out.println("\nSplit into lines:");
        multiline.lines().forEach(line -> System.out.println("  - " + line));

        // Count lines
        long lineCount = multiline.lines().count();
        System.out.println("Total lines: " + lineCount);

        System.out.println();

        // strip(), stripLeading(), stripTrailing()
        System.out.println("--- strip() Methods ---");
        String str = "   Hello World   ";

        System.out.println("Original: [" + str + "]");
        System.out.println("strip(): [" + str.strip() + "]");
        System.out.println("stripLeading(): [" + str.stripLeading() + "]");
        System.out.println("stripTrailing(): [" + str.stripTrailing() + "]");

        System.out.println();

        // repeat()
        System.out.println("--- repeat() ---");
        String word = "Java";
        String symbol = "*";

        System.out.println(word + " repeated 3 times: " + word.repeat(3));
        System.out.println("Border: " + symbol.repeat(20));

        // Practical use - creating separator
        String separator = "-".repeat(50);
        System.out.println(separator);
        System.out.println("Title".repeat(1));
        System.out.println(separator);

        System.out.println();

        // Combining methods
        System.out.println("--- Combining Methods ---");
        String data = "  Line 1  \n  Line 2  \n  Line 3  ";

        System.out.println("Processing multiline data:");
        String processed = data.lines()
            .map(String::strip)
            .filter(s -> !s.isBlank())
            .collect(Collectors.joining(" | "));

        System.out.println("Result: " + processed);
    }
}
```

**Output:**

```
=== Java 11 String Methods Demo ===

--- isBlank() ---
"" is blank: true
"   " is blank: true
"Hello" is blank: false

--- lines() ---
Original string:
Java
Python
C++
JavaScript

Split into lines:
  - Java
  - Python
  - C++
  - JavaScript
Total lines: 4

--- strip() Methods ---
Original: [   Hello World   ]
strip(): [Hello World]
stripLeading(): [Hello World   ]
stripTrailing(): [   Hello World]

--- repeat() ---
Java repeated 3 times: JavaJavaJava
Border: ********************
--------------------------------------------------
Title
--------------------------------------------------

--- Combining Methods ---
Processing multiline data:
Result: Line 1 | Line 2 | Line 3
```

**Example 21.2: File Methods**

```java
// FileMethodsDemo.java
import java.nio.file.*;
import java.io.IOException;

public class FileMethodsDemo {
    public static void main(String[] args) {
        System.out.println("=== Java 11 File Methods Demo ===\n");

        String filename = "java11_test.txt";

        try {
            // writeString() - Write to file
            System.out.println("--- Writing to File ---");
            String content = "Hello from Java 11!\nThis is line 2.\nThis is line 3.";

            Files.writeString(Path.of(filename), content);
            System.out.println("Content written to file: " + filename);

            System.out.println();

            // readString() - Read from file
            System.out.println("--- Reading from File ---");
            String readContent = Files.readString(Path.of(filename));
            System.out.println("File content:");
            System.out.println(readContent);

            System.out.println();

            // Append to file
            System.out.println("--- Appending to File ---");
            Files.writeString(
                Path.of(filename),
                "\nAppended line 4.",
                StandardOpenOption.APPEND
            );
            System.out.println("Content appended");

            System.out.println();

            // Read updated content
            System.out.println("--- Reading Updated File ---");
            String updatedContent = Files.readString(Path.of(filename));
            System.out.println("Updated file content:");
            System.out.println(updatedContent);

            System.out.println();

            // Process file content
            System.out.println("--- Processing File Content ---");
            long lineCount = updatedContent.lines().count();
            System.out.println("Total lines: " + lineCount);

            System.out.println("\nLines in uppercase:");
            updatedContent.lines()
                .map(String::toUpperCase)
                .forEach(line -> System.out.println("  " + line));

            // Cleanup
            Files.deleteIfExists(Path.of(filename));
            System.out.println("\nFile deleted: " + filename);

        } catch (IOException e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
}
```

**Output:**

```
=== Java 11 File Methods Demo ===

--- Writing to File ---
Content written to file: java11_test.txt

--- Reading from File ---
File content:
Hello from Java 11!
This is line 2.
This is line 3.

--- Appending to File ---
Content appended

--- Reading Updated File ---
Updated file content:
Hello from Java 11!
This is line 2.
This is line 3.
Appended line 4.

--- Processing File Content ---
Total lines: 4

Lines in uppercase:
  HELLO FROM JAVA 11!
  THIS IS LINE 2.
  THIS IS LINE 3.
  APPENDED LINE 4.

File deleted: java11_test.txt
```

**Example 21.3: Collection and Predicate Enhancements**

```java
// CollectionPredicateDemo.java
import java.util.*;
import java.util.stream.Collectors;
import static java.util.function.Predicate.not;

public class CollectionPredicateDemo {
    public static void main(String[] args) {
        System.out.println("=== Collection & Predicate Enhancements Demo ===\n");

        // Collection.toArray() with generator
        System.out.println("--- toArray() Enhancement ---");
        List<String> languages = Arrays.asList("Java", "Python", "C++", "JavaScript");

        // Java 11 way
        String[] array = languages.toArray(String[]::new);

        System.out.println("List: " + languages);
        System.out.println("Array: " + Arrays.toString(array));

        System.out.println();

        // Predicate.not()
        System.out.println("--- Predicate.not() ---");
        List<String> mixedList = Arrays.asList(
            "Java", "", "Python", "   ", "C++", "", "JavaScript"
        );

        System.out.println("Original list: " + mixedList);

        // Filter non-blank strings
        List<String> nonBlank = mixedList.stream()
            .filter(not(String::isBlank))
            .collect(Collectors.toList());

        System.out.println("Non-blank strings: " + nonBlank);

        System.out.println();

        // More Predicate.not() examples
        System.out.println("--- More Predicate.not() Examples ---");

        List<String> words = Arrays.asList("apple", "banana", "apricot", "cherry", "avocado");

        System.out.println("Original words: " + words);

        // Words not starting with 'a'
        List<String> notStartingWithA = words.stream()
            .filter(not(s -> s.startsWith("a")))
            .collect(Collectors.toList());

        System.out.println("Not starting with 'a': " + notStartingWithA);

        // Words not containing 'e'
        List<String> notContainingE = words.stream()
            .filter(not(s -> s.contains("e")))
            .collect(Collectors.toList());

        System.out.println("Not containing 'e': " + notContainingE);

        System.out.println();

        // Optional.isEmpty()
        System.out.println("--- Optional.isEmpty() ---");
        Optional<String> opt1 = Optional.of("Hello");
        Optional<String> opt2 = Optional.empty();

        System.out.println("opt1.isEmpty(): " + opt1.isEmpty());
        System.out.println("opt2.isEmpty(): " + opt2.isEmpty());

        // Practical use
        Optional<String> result = findUser("john");
        if (result.isEmpty()) {
            System.out.println("User not found");
        } else {
            System.out.println("User found: " + result.get());
        }
    }

    static Optional<String> findUser(String name) {
        // Simulate user search
        return name.equals("admin") ? Optional.of("Admin User") : Optional.empty();
    }
}
```

**Output:**

```
=== Collection & Predicate Enhancements Demo ===

--- toArray() Enhancement ---
List: [Java, Python, C++, JavaScript]
Array: [Java, Python, C++, JavaScript]

--- Predicate.not() ---
Original list: [Java, , Python,    , C++, , JavaScript]
Non-blank strings: [Java, Python, C++, JavaScript]

--- More Predicate.not() Examples ---
Original words: [apple, banana, apricot, cherry, avocado]
Not starting with 'a': [banana, cherry]
Not containing 'e': [banana, avocado]

--- Optional.isEmpty() ---
opt1.isEmpty(): false
opt2.isEmpty(): true
User not found
```

### 🎯 Key Takeaways

- Java 11 is a Long-Term Support (LTS) release
- New String methods: isBlank(), lines(), strip(), repeat()
- Simplified file I/O with Files.readString() and Files.writeString()
- Standard HTTP Client API for modern HTTP communication
- Can run single-file Java programs directly without compilation
- Optional.isEmpty() for better readability
- Collection.toArray() with method reference
- Predicate.not() for cleaner negation in streams

### 📝 Practice Questions

1. What is the difference between trim() and strip() methods?
2. How does Files.readString() simplify file reading compared to BufferedReader?
3. What are the benefits of the new HTTP Client API over HttpURLConnection?
4. When would you use Predicate.not() instead of lambda negation?
5. Write a program to read a file, filter non-blank lines, and write to another file using Java 11 features.
