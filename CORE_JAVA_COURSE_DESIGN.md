# 🎓 Complete Core Java Course Design

## 📚 Course Overview

**Duration:** 8-10 Weeks  
**Level:** Beginner to Intermediate  
**Prerequisites:** Basic computer knowledge  
**Goal:** Master Core Java fundamentals and build real-world applications

---

## 📋 Course Structure

### **Module 1: Java Fundamentals (Week 1)**

#### **1.1 Introduction to Java**

- **What is Java?**
  - Platform-independent programming language
  - "Write Once, Run Anywhere" (WORA)
  - Used for web, mobile (Android), desktop, enterprise applications
- **Java Features:**

  - Object-Oriented
  - Platform Independent (JVM)
  - Secure
  - Multithreaded
  - Robust (strong memory management)

- **JDK, JRE, JVM:**

  - **JDK (Java Development Kit):** Tools to develop Java programs (compiler, debugger)
  - **JRE (Java Runtime Environment):** Environment to run Java programs
  - **JVM (Java Virtual Machine):** Executes Java bytecode

- **Setting up Java:**
  - Install JDK
  - Set PATH and JAVA_HOME
  - Install IDE (Eclipse, IntelliJ IDEA, VS Code)

#### **1.2 First Java Program**

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```

**Explanation:**

- `public class HelloWorld`: Class declaration
- `public static void main(String[] args)`: Entry point of program
- `System.out.println()`: Print to console

#### **1.3 Java Syntax Basics**

- **Comments:**

  ```java
  // Single line comment
  /* Multi-line comment */
  /** Documentation comment */
  ```

- **Variables:**

  ```java
  int age = 25;
  String name = "John";
  double salary = 50000.50;
  boolean isActive = true;
  ```

- **Data Types:**

  - **Primitive:** int, long, float, double, char, boolean, byte, short
  - **Non-Primitive:** String, Arrays, Classes

- **Naming Conventions:**
  - Classes: PascalCase (e.g., `StudentRecord`)
  - Variables/Methods: camelCase (e.g., `studentName`)
  - Constants: UPPER_CASE (e.g., `MAX_VALUE`)

#### **1.4 Operators**

- **Arithmetic:** `+, -, *, /, %`
- **Relational:** `==, !=, >, <, >=, <=`
- **Logical:** `&&, ||, !`
- **Assignment:** `=, +=, -=, *=, /=`
- **Increment/Decrement:** `++, --`

**Practice:**

- Write a calculator program
- Convert temperature (Celsius to Fahrenheit)
- Calculate simple interest

---

### **Module 2: Control Flow (Week 1-2)**

#### **2.1 Conditional Statements**

**if-else:**

```java
int age = 18;
if (age >= 18) {
    System.out.println("Adult");
} else {
    System.out.println("Minor");
}
```

**if-else-if ladder:**

```java
int marks = 85;
if (marks >= 90) {
    System.out.println("Grade A");
} else if (marks >= 75) {
    System.out.println("Grade B");
} else if (marks >= 60) {
    System.out.println("Grade C");
} else {
    System.out.println("Fail");
}
```

**switch-case:**

```java
int day = 3;
switch (day) {
    case 1:
        System.out.println("Monday");
        break;
    case 2:
        System.out.println("Tuesday");
        break;
    case 3:
        System.out.println("Wednesday");
        break;
    default:
        System.out.println("Invalid day");
}
```

#### **2.2 Loops**

**for loop:**

```java
for (int i = 1; i <= 5; i++) {
    System.out.println("Count: " + i);
}
```

**while loop:**

```java
int i = 1;
while (i <= 5) {
    System.out.println("Count: " + i);
    i++;
}
```

**do-while loop:**

```java
int i = 1;
do {
    System.out.println("Count: " + i);
    i++;
} while (i <= 5);
```

**Enhanced for loop (for-each):**

```java
int[] numbers = {1, 2, 3, 4, 5};
for (int num : numbers) {
    System.out.println(num);
}
```

**Practice:**

- Print multiplication table
- Find factorial of a number
- Print Fibonacci series
- Check if number is prime

---

### **Module 3: Arrays (Week 2)**

#### **3.1 Single Dimensional Arrays**

**Declaration and Initialization:**

```java
// Method 1
int[] numbers = new int[5];
numbers[0] = 10;
numbers[1] = 20;
numbers[2] = 30;
numbers[3] = 40;
numbers[4] = 50;

// Method 2
int[] scores = {85, 90, 78, 92, 88};

// Method 3
String[] names = new String[] {"Alice", "Bob", "Charlie"};
```

**Example: Find Maximum in Array**

```java
public class ArrayExample {
    public static void main(String[] args) {
        int[] numbers = {45, 23, 67, 12, 89, 34};

        int max = numbers[0];
        for (int i = 1; i < numbers.length; i++) {
            if (numbers[i] > max) {
                max = numbers[i];
            }
        }

        System.out.println("Maximum value: " + max);
    }
}
```

**Example: Calculate Average**

```java
public class AverageCalculator {
    public static void main(String[] args) {
        int[] marks = {85, 90, 78, 92, 88};

        int sum = 0;
        for (int mark : marks) {
            sum += mark;
        }

        double average = (double) sum / marks.length;
        System.out.println("Average marks: " + average);
    }
}
```

#### **3.2 Multi-Dimensional Arrays**

**2D Array Example:**

```java
public class MatrixExample {
    public static void main(String[] args) {
        // 3x3 matrix
        int[][] matrix = {
            {1, 2, 3},
            {4, 5, 6},
            {7, 8, 9}
        };

        // Print matrix
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[i].length; j++) {
                System.out.print(matrix[i][j] + " ");
            }
            System.out.println();
        }
    }
}
```

**Example: Add Two Matrices**

```java
public class MatrixAddition {
    public static void main(String[] args) {
        int[][] matrix1 = {{1, 2}, {3, 4}};
        int[][] matrix2 = {{5, 6}, {7, 8}};
        int[][] result = new int[2][2];

        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 2; j++) {
                result[i][j] = matrix1[i][j] + matrix2[i][j];
            }
        }

        System.out.println("Result:");
        for (int i = 0; i < 2; i++) {
            for (int j = 0; j < 2; j++) {
                System.out.print(result[i][j] + " ");
            }
            System.out.println();
        }
    }
}
```

**Practice:**

- Reverse an array
- Sort an array (bubble sort)
- Search element in array (linear search)
- Find second largest element

---

### **Module 4: Object-Oriented Programming - Part 1 (Week 3)**

#### **4.1 Classes and Objects**

**What is a Class?**

- Blueprint/template for creating objects
- Contains data (fields) and behavior (methods)

**What is an Object?**

- Instance of a class
- Has state (values) and behavior (methods)

**Example: Student Class**

```java
public class Student {
    // Fields (attributes)
    String name;
    int rollNumber;
    int age;
    double marks;

    // Method to display student details
    void displayInfo() {
        System.out.println("Name: " + name);
        System.out.println("Roll Number: " + rollNumber);
        System.out.println("Age: " + age);
        System.out.println("Marks: " + marks);
    }

    // Method to check if student passed
    boolean hasPassed() {
        return marks >= 40;
    }
}

// Main class
public class Main {
    public static void main(String[] args) {
        // Creating object
        Student student1 = new Student();
        student1.name = "Alice";
        student1.rollNumber = 101;
        student1.age = 20;
        student1.marks = 85.5;

        // Calling methods
        student1.displayInfo();

        if (student1.hasPassed()) {
            System.out.println("Result: PASS");
        } else {
            System.out.println("Result: FAIL");
        }
    }
}
```

#### **4.2 Constructors**

**What is a Constructor?**

- Special method to initialize objects
- Same name as class
- No return type
- Called automatically when object is created

**Example: Constructor Types**

```java
public class Employee {
    String name;
    int id;
    double salary;

    // Default Constructor
    public Employee() {
        name = "Unknown";
        id = 0;
        salary = 0.0;
    }

    // Parameterized Constructor
    public Employee(String name, int id, double salary) {
        this.name = name;
        this.id = id;
        this.salary = salary;
    }

    // Constructor Overloading
    public Employee(String name, int id) {
        this.name = name;
        this.id = id;
        this.salary = 30000.0; // Default salary
    }

    void displayInfo() {
        System.out.println("Name: " + name);
        System.out.println("ID: " + id);
        System.out.println("Salary: " + salary);
    }
}

public class Main {
    public static void main(String[] args) {
        Employee emp1 = new Employee(); // Default constructor
        Employee emp2 = new Employee("John", 101, 50000); // Parameterized
        Employee emp3 = new Employee("Alice", 102); // Overloaded

        emp1.displayInfo();
        System.out.println();
        emp2.displayInfo();
        System.out.println();
        emp3.displayInfo();
    }
}
```

---
