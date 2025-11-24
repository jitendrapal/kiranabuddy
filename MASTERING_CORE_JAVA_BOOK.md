# 📘 MASTERING CORE JAVA

## A Complete Guide with Practical Examples

**Author:** [Your Name]  
**Edition:** First Edition  
**Copyright © 2024**

---

## 📖 TABLE OF CONTENTS

### PART I: JAVA FUNDAMENTALS

**Chapter 1:** Introduction to Java Programming  
**Chapter 2:** Variables, Data Types, and Operators  
**Chapter 3:** Control Flow Statements  
**Chapter 4:** Arrays and Strings

### PART II: OBJECT-ORIENTED PROGRAMMING

**Chapter 5:** Classes and Objects  
**Chapter 6:** Constructors and Methods  
**Chapter 7:** Inheritance  
**Chapter 8:** Polymorphism  
**Chapter 9:** Abstraction  
**Chapter 10:** Encapsulation  
**Chapter 11:** Interfaces

### PART III: ADVANCED CONCEPTS

**Chapter 12:** Exception Handling  
**Chapter 13:** Collections Framework  
**Chapter 14:** Multithreading  
**Chapter 15:** File I/O Operations  
**Chapter 16:** Generics  
**Chapter 17:** Lambda Expressions and Streams

### PART IV: PRACTICAL PROJECTS

**Chapter 18:** Banking System Application  
**Chapter 19:** Student Management System  
**Chapter 20:** Library Management System

---

# PART I: JAVA FUNDAMENTALS

---

# Chapter 1: Introduction to Java Programming

## 1.1 What is Java?

Java is a high-level, object-oriented programming language developed by **James Gosling** at Sun Microsystems (now owned by Oracle Corporation) in **1995**. It was originally designed for interactive television but was too advanced for the digital cable industry at that time.

### The Philosophy: "Write Once, Run Anywhere" (WORA)

Java's core philosophy is platform independence. This means you can write Java code on Windows, compile it, and run the same compiled code on Linux, Mac, or any other platform that has a Java Virtual Machine (JVM).

**Example Scenario:**

```
Developer writes code on Windows → Compiles to bytecode
→ Bytecode runs on Linux, Mac, Windows, Android, etc.
```

### Key Characteristics of Java

**1. Simple and Easy to Learn**

- Syntax similar to C/C++ but removes complex features like pointers
- Automatic memory management (Garbage Collection)
- Rich set of built-in libraries

**2. Object-Oriented**

- Everything is an object (except primitive types)
- Promotes code reusability through inheritance
- Encapsulation for data security

**3. Platform Independent**

- Compiled code (bytecode) runs on any platform with JVM
- No need to recompile for different operating systems

**4. Secure**

- No explicit pointers
- Programs run inside JVM sandbox
- Bytecode verification before execution
- Security manager for access control

**5. Robust (Reliable)**

- Strong type checking at compile-time
- Exception handling mechanism
- Automatic garbage collection
- Eliminates memory leaks

**6. Multithreaded**

- Built-in support for concurrent programming
- Can execute multiple tasks simultaneously
- Useful for responsive applications

**7. High Performance**

- Just-In-Time (JIT) compiler improves performance
- Bytecode is close to native code
- Optimized for speed

### Real-World Applications of Java

**1. Android Mobile Applications**

- 90% of Android apps are built using Java
- Examples: WhatsApp, Instagram, Spotify

**2. Enterprise Applications**

- Banking systems (HDFC, ICICI online banking)
- E-commerce platforms (Amazon, Flipkart backend)
- ERP systems (SAP, Oracle)

**3. Web Applications**

- Server-side applications using Spring, Hibernate
- Examples: LinkedIn, eBay

**4. Desktop Applications**

- IntelliJ IDEA, Eclipse IDE
- Media players, antivirus software

**5. Big Data Technologies**

- Apache Hadoop
- Apache Spark
- Apache Kafka

**6. Cloud-Based Applications**

- Microservices architecture
- AWS, Google Cloud applications

**7. Scientific Applications**

- MATLAB uses Java for UI
- NASA uses Java for various projects

## 1.2 Understanding JDK, JRE, and JVM

To understand Java's architecture, you need to know three key components:

### JVM (Java Virtual Machine)

**What is JVM?**

- An abstract machine that provides runtime environment for Java bytecode
- Platform-dependent (different JVM for Windows, Linux, Mac)
- Responsible for converting bytecode to machine code

**Functions of JVM:**

1. **Loads** the .class file
2. **Verifies** bytecode for security
3. **Executes** bytecode
4. **Provides** runtime environment

**JVM Architecture:**

```
┌─────────────────────────────────────┐
│         Class Loader                │
├─────────────────────────────────────┤
│         Memory Areas                │
│  - Method Area                      │
│  - Heap                             │
│  - Stack                            │
│  - PC Register                      │
│  - Native Method Stack              │
├─────────────────────────────────────┤
│      Execution Engine               │
│  - Interpreter                      │
│  - JIT Compiler                     │
│  - Garbage Collector                │
└─────────────────────────────────────┘
```

### JRE (Java Runtime Environment)

**What is JRE?**

- Set of software tools for running Java applications
- Includes JVM + Library classes (rt.jar) + Other files

**Components:**

- JVM
- Core libraries (java.lang, java.util, etc.)
- Supporting files

**When to use JRE?**

- If you only want to **run** Java applications
- End users need only JRE installed

### JDK (Java Development Kit)

**What is JDK?**

- Complete development kit for Java
- Includes JRE + Development tools

**Components:**

- JRE (JVM + Libraries)
- Compiler (javac)
- Debugger (jdb)
- Documentation generator (javadoc)
- Archive tool (jar)
- Other development tools

**When to use JDK?**

- If you want to **develop** Java applications
- Programmers need JDK installed

**Relationship Diagram:**

```
┌─────────────────────────────────────────┐
│              JDK                        │
│  ┌──────────────────────────────────┐  │
│  │           JRE                    │  │
│  │  ┌────────────────────────────┐ │  │
│  │  │         JVM                │ │  │
│  │  │  - Class Loader            │ │  │
│  │  │  - Memory Management       │ │  │
│  │  │  - Execution Engine        │ │  │
│  │  └────────────────────────────┘ │  │
│  │  + Library Classes (rt.jar)    │  │
│  │  + java.lang, java.util, etc.  │  │
│  └──────────────────────────────────┘  │
│  + Development Tools                   │
│    - javac (Compiler)                  │
│    - java (Launcher)                   │
│    - javadoc (Documentation)           │
│    - jar (Archive tool)                │
└─────────────────────────────────────────┘
```

**Summary Table:**

| Component | Purpose            | Who Needs It? | Contains         |
| --------- | ------------------ | ------------- | ---------------- |
| **JVM**   | Executes bytecode  | Everyone      | Execution engine |
| **JRE**   | Runs Java apps     | End users     | JVM + Libraries  |
| **JDK**   | Develops Java apps | Developers    | JRE + Dev tools  |

## 1.3 Setting Up Java Development Environment

### Step 1: Download and Install JDK

**For Windows:**

1. Visit Oracle's official website: https://www.oracle.com/java/technologies/downloads/
2. Download JDK (Latest LTS version recommended, e.g., JDK 17 or JDK 21)
3. Run the installer (.exe file)
4. Follow installation wizard
5. Note the installation path (e.g., `C:\Program Files\Java\jdk-17`)

**For Linux (Ubuntu/Debian):**

```bash
# Update package index
sudo apt update

# Install OpenJDK
sudo apt install openjdk-17-jdk

# Verify installation
java -version
javac -version
```

**For macOS:**

```bash
# Using Homebrew
brew install openjdk@17

# Or download from Oracle website
```

### Step 2: Set Environment Variables

**Why set environment variables?**

- To run Java commands from any directory
- To help IDEs locate Java installation

**For Windows:**

1. Right-click on "This PC" or "My Computer"
2. Select "Properties"
3. Click "Advanced system settings"
4. Click "Environment Variables"

**Set JAVA_HOME:**

- Click "New" under System Variables
- Variable name: `JAVA_HOME`
- Variable value: `C:\Program Files\Java\jdk-17` (your JDK path)

**Update PATH:**

- Find "Path" in System Variables
- Click "Edit"
- Click "New"
- Add: `%JAVA_HOME%\bin`
- Click OK

**For Linux/Mac:**

Add to `~/.bashrc` or `~/.zshrc`:

```bash
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$JAVA_HOME/bin:$PATH
```

Apply changes:

```bash
source ~/.bashrc
```

### Step 3: Verify Installation

Open Command Prompt (Windows) or Terminal (Linux/Mac):

```bash
# Check Java version
java -version

# Expected output:
# java version "17.0.1" 2021-10-19 LTS
# Java(TM) SE Runtime Environment (build 17.0.1+12-LTS-39)
# Java HotSpot(TM) 64-Bit Server VM (build 17.0.1+12-LTS-39, mixed mode)

# Check compiler version
javac -version

# Expected output:
# javac 17.0.1
```

If you see version information, installation is successful!

### Step 4: Choose and Install an IDE

**What is an IDE?**

- Integrated Development Environment
- Provides code editor, debugger, compiler in one tool
- Makes development easier and faster

**Popular Java IDEs:**

**1. IntelliJ IDEA (Recommended)**

- **Pros:** Intelligent code completion, powerful refactoring, excellent debugging
- **Cons:** Heavy on system resources
- **Best for:** Professional development
- **Download:** https://www.jetbrains.com/idea/download/
- **Versions:** Community (Free) and Ultimate (Paid)

**2. Eclipse**

- **Pros:** Free, open-source, extensive plugins
- **Cons:** Can be slow, complex UI
- **Best for:** Enterprise applications
- **Download:** https://www.eclipse.org/downloads/

**3. Visual Studio Code**

- **Pros:** Lightweight, fast, customizable
- **Cons:** Requires extensions for full Java support
- **Best for:** Beginners, small projects
- **Download:** https://code.visualstudio.com/
- **Required Extensions:** Java Extension Pack

**4. NetBeans**

- **Pros:** Easy to use, good for beginners
- **Cons:** Slower than others
- **Best for:** Learning Java
- **Download:** https://netbeans.apache.org/

**Recommendation for Beginners:**
Start with **Visual Studio Code** (lightweight) or **IntelliJ IDEA Community Edition** (feature-rich).

### Step 5: Create Your First Project

**Using Command Line:**

```bash
# Create a directory
mkdir MyFirstJavaProject
cd MyFirstJavaProject

# Create a Java file
notepad HelloWorld.java  # Windows
nano HelloWorld.java     # Linux/Mac
```

**Using IntelliJ IDEA:**

1. Open IntelliJ IDEA
2. Click "New Project"
3. Select "Java"
4. Choose JDK version
5. Name your project
6. Click "Create"

## 1.4 Your First Java Program

Let's write our first Java program that displays "Hello, World!" on the screen.

### Example 1.1: Hello World Program

**HelloWorld.java**

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

### Understanding the Code Line by Line

**Line 1: `public class HelloWorld {`**

- `public`: Access modifier

  - Makes the class accessible from anywhere
  - Other options: private, protected, default

- `class`: Keyword to define a class

  - Everything in Java is inside a class
  - Class is a blueprint for objects

- `HelloWorld`: Name of the class

  - Must match the filename (HelloWorld.java)
  - Follows PascalCase naming convention
  - Should be meaningful and descriptive

- `{`: Opening brace
  - Marks the beginning of class body
  - Must have a matching closing brace

**Line 2: `public static void main(String[] args) {`**

This is the **main method** - the entry point of every Java application.

- `public`: Method is accessible from anywhere

  - JVM needs to access it to start the program

- `static`: Method belongs to the class, not to objects

  - Can be called without creating an object
  - JVM calls it without creating an instance

- `void`: Method doesn't return any value

  - If it returned something, we'd specify the type (int, String, etc.)

- `main`: Name of the method

  - Special name recognized by JVM
  - Must be exactly "main" (case-sensitive)

- `String[] args`: Parameter
  - Array of strings
  - Stores command-line arguments
  - Can be named anything, but "args" is convention

**Line 3: `System.out.println("Hello, World!");`**

This line prints text to the console.

- `System`: Built-in Java class

  - Part of java.lang package
  - Provides system-related functionality

- `out`: Static member of System class

  - Object of PrintStream class
  - Represents standard output (console)

- `println`: Method of PrintStream

  - Prints text and moves to next line
  - "print line"

- `"Hello, World!"`: String literal
  - Text enclosed in double quotes
  - Will be displayed on console

**Line 4-5: Closing braces**

- First `}` closes the main method
- Second `}` closes the HelloWorld class

### Compiling and Running the Program

**Step 1: Save the file**

- Filename must be `HelloWorld.java` (matches class name)
- Save in a directory you can access via command line

**Step 2: Open Command Prompt/Terminal**

```bash
# Navigate to the directory
cd path/to/your/file
```

**Step 3: Compile the program**

```bash
javac HelloWorld.java
```

**What happens?**

- `javac` is the Java compiler
- It reads `HelloWorld.java`
- Checks for syntax errors
- Creates `HelloWorld.class` (bytecode file)
- If errors exist, compilation fails with error messages

**Step 4: Run the program**

```bash
java HelloWorld
```

**Note:** Don't include `.class` extension when running!

**What happens?**

- `java` is the Java launcher
- It starts the JVM
- JVM loads `HelloWorld.class`
- Executes the `main` method
- Displays output

**Expected Output:**

```
Hello, World!
```

### Common Errors and Solutions

**Error 1: "javac is not recognized"**

```
Solution: Java is not in PATH. Set environment variables correctly.
```

**Error 2: "class HelloWorld is public, should be declared in a file named HelloWorld.java"**

```
Solution: Filename must match class name exactly (case-sensitive).
```

**Error 3: "Could not find or load main class HelloWorld"**

```
Solution:
- Make sure you're in the correct directory
- Run 'java HelloWorld' not 'java HelloWorld.class'
- Check if .class file was created
```

**Error 4: "Main method not found in class HelloWorld"**

```
Solution: Check main method signature is exactly:
public static void main(String[] args)
```

### Example 1.2: Personalized Greeting

Let's create a program that greets a person by name.

**Greeting.java**

```java
public class Greeting {
    public static void main(String[] args) {
        // Declare variables
        String name = "John";
        int age = 25;
        String city = "New York";

        // Print greeting messages
        System.out.println("===== Welcome =====");
        System.out.println("Hello, " + name + "!");
        System.out.println("You are " + age + " years old.");
        System.out.println("You live in " + city + ".");
        System.out.println("Welcome to Java Programming!");
        System.out.println("===================");
    }
}
```

**Output:**

```
===== Welcome =====
Hello, John!
You are 25 years old.
You live in New York.
Welcome to Java Programming!
===================
```

**Key Concepts:**

- **Variables:** Store data (`name`, `age`, `city`)
- **String concatenation:** Using `+` to join strings
- **Multiple print statements:** Each `println` creates a new line

### Example 1.3: Using Command-Line Arguments

**CommandLineDemo.java**

```java
public class CommandLineDemo {
    public static void main(String[] args) {
        // Check if arguments are provided
        if (args.length > 0) {
            System.out.println("Hello, " + args[0] + "!");

            if (args.length > 1) {
                System.out.println("You are from " + args[1]);
            }
        } else {
            System.out.println("No arguments provided!");
            System.out.println("Usage: java CommandLineDemo <name> <city>");
        }
    }
}
```

**Compile and Run:**

```bash
javac CommandLineDemo.java
java CommandLineDemo John Mumbai
```

**Output:**

```
Hello, John!
You are from Mumbai
```

**Explanation:**

- `args[0]` is the first command-line argument ("John")
- `args[1]` is the second argument ("Mumbai")
- `args.length` tells how many arguments were provided

### Example 1.4: Simple Calculator

**SimpleCalculator.java**

```java
public class SimpleCalculator {
    public static void main(String[] args) {
        // Declare variables
        int num1 = 10;
        int num2 = 5;

        // Perform calculations
        int sum = num1 + num2;
        int difference = num1 - num2;
        int product = num1 * num2;
        int quotient = num1 / num2;
        int remainder = num1 % num2;

        // Display results
        System.out.println("Number 1: " + num1);
        System.out.println("Number 2: " + num2);
        System.out.println("-------------------");
        System.out.println("Sum: " + sum);
        System.out.println("Difference: " + difference);
        System.out.println("Product: " + product);
        System.out.println("Quotient: " + quotient);
        System.out.println("Remainder: " + remainder);
    }
}
```

**Output:**

```
Number 1: 10
Number 2: 5
-------------------
Sum: 15
Difference: 5
Product: 50
Quotient: 2
Remainder: 0
```

## 1.5 Java Program Structure

Every Java program follows a specific structure:

```java
// 1. Package declaration (optional)
package com.mycompany.myapp;

// 2. Import statements (optional)
import java.util.Scanner;
import java.util.ArrayList;

// 3. Class declaration (mandatory)
public class MyProgram {

    // 4. Class variables (optional)
    static int count = 0;

    // 5. Main method (entry point)
    public static void main(String[] args) {
        // 6. Local variables
        int x = 10;

        // 7. Statements
        System.out.println("Value: " + x);
    }

    // 8. Other methods (optional)
    public static void display() {
        System.out.println("Hello");
    }
}
```

**Order is important:**

1. Package declaration (if any) must be first
2. Import statements come next
3. Class declaration
4. Class members (variables, methods)

## 1.6 Comments in Java

Comments are used to explain code and are ignored by the compiler.

### Types of Comments

**1. Single-line comments**

```java
// This is a single-line comment
int age = 25; // Age of the person
```

**2. Multi-line comments**

```java
/*
 * This is a multi-line comment
 * It can span multiple lines
 * Useful for longer explanations
 */
int salary = 50000;
```

**3. Documentation comments (Javadoc)**

```java
/**
 * This class demonstrates basic Java concepts.
 * @author John Doe
 * @version 1.0
 * @since 2024
 */
public class Demo {
    /**
     * Calculates the sum of two numbers.
     * @param a First number
     * @param b Second number
     * @return Sum of a and b
     */
    public int add(int a, int b) {
        return a + b;
    }
}
```

**Best Practices:**

- Use comments to explain "why", not "what"
- Keep comments up-to-date with code
- Don't over-comment obvious code
- Use meaningful variable names to reduce need for comments

### Example with Good Comments

```java
public class BankAccount {
    // Account balance in rupees
    private double balance;

    /**
     * Withdraws money from account.
     * Checks if sufficient balance exists before withdrawal.
     * @param amount Amount to withdraw
     * @return true if successful, false otherwise
     */
    public boolean withdraw(double amount) {
        // Prevent withdrawal if insufficient funds
        if (balance < amount) {
            return false;
        }

        balance -= amount;
        return true;
    }
}
```

## 1.7 Practice Exercises

**Exercise 1.1: Personal Information**
Write a program that displays your name, age, city, and favorite hobby.

**Exercise 1.2: Simple Math**
Create a program that calculates the area and perimeter of a rectangle with length 10 and width 5.

**Exercise 1.3: Temperature Converter**
Write a program that converts 100 degrees Celsius to Fahrenheit.
Formula: F = (C × 9/5) + 32

**Exercise 1.4: Command-Line Calculator**
Create a program that takes two numbers as command-line arguments and displays their sum.

**Exercise 1.5: Pattern Printing**
Write a program that prints:

```
*****
*****
*****
```

## 1.8 Chapter Summary

In this chapter, you learned:

✅ What Java is and its key features
✅ Difference between JDK, JRE, and JVM
✅ How to install and set up Java development environment
✅ How to write, compile, and run Java programs
✅ Structure of a Java program
✅ How to use comments effectively
✅ Basic input/output using System.out.println()

**Key Takeaways:**

- Java is platform-independent and object-oriented
- Every Java program must have a class
- The `main` method is the entry point
- Filename must match the public class name
- Use `javac` to compile and `java` to run

**Next Chapter Preview:**
In Chapter 2, we'll dive deep into variables, data types, and operators - the building blocks of Java programming.

---

# Chapter 2: Variables, Data Types, and Operators

## 2.1 Introduction to Variables

A **variable** is a container that holds data that can be changed during program execution.

**Think of it like:**

- A box with a label (variable name)
- The box contains something (value)
- You can change what's in the box

### Variable Declaration and Initialization

**Syntax:**

```java
dataType variableName = value;
```

**Examples:**

```java
int age = 25;              // Integer variable
double salary = 50000.50;  // Decimal variable
String name = "John";      // String variable
boolean isActive = true;   // Boolean variable
```

### Variable Declaration (Without Initialization)

```java
int age;           // Declared but not initialized
age = 25;          // Initialized later
```

### Multiple Variable Declaration

```java
// Same type, separate lines
int x = 10;
int y = 20;
int z = 30;

// Same type, same line
int a = 1, b = 2, c = 3;

// Declare multiple, initialize later
int p, q, r;
p = 100;
q = 200;
r = 300;
```

### Variable Naming Rules

**Rules (Must Follow):**

1. Must start with a letter, underscore (\_), or dollar sign ($)
2. Cannot start with a number
3. Cannot use Java keywords (int, class, public, etc.)
4. Case-sensitive (age and Age are different)
5. No spaces allowed

**Valid Names:**

```java
int age;
int _count;
int $price;
int student1;
int studentAge;
```

**Invalid Names:**

```java
int 1student;    // ❌ Starts with number
int student-age; // ❌ Contains hyphen
int class;       // ❌ Java keyword
int student age; // ❌ Contains space
```

**Naming Conventions (Best Practices):**

```java
// Variables and methods: camelCase
int studentAge;
String firstName;
double accountBalance;

// Constants: UPPER_CASE with underscores
final int MAX_AGE = 100;
final double PI = 3.14159;

// Classes: PascalCase
class StudentRecord { }
class BankAccount { }
```
