# Chapter 2 (Continued): Data Types and Operators

## 2.2 Data Types in Java

Java is a **strongly-typed** language, meaning every variable must have a data type.

### Types of Data Types

```
Data Types
    ├── Primitive Types (8 types)
    │   ├── Numeric
    │   │   ├── Integer Types: byte, short, int, long
    │   │   └── Floating-Point Types: float, double
    │   ├── Character: char
    │   └── Boolean: boolean
    └── Non-Primitive Types (Reference Types)
        ├── String
        ├── Arrays
        ├── Classes
        └── Interfaces
```

### Primitive Data Types

#### 1. byte

**Size:** 1 byte (8 bits)  
**Range:** -128 to 127  
**Default Value:** 0  
**Use:** Save memory in large arrays

```java
byte age = 25;
byte temperature = -10;
byte maxValue = 127;
byte minValue = -128;

// Error: Value out of range
// byte invalid = 200; // ❌ Compilation error
```

**Real-world example:**
```java
// Storing age of students (0-100)
byte studentAge = 18;

// Temperature in Celsius (-50 to 50)
byte roomTemp = 25;
```

#### 2. short

**Size:** 2 bytes (16 bits)  
**Range:** -32,768 to 32,767  
**Default Value:** 0  
**Use:** Save memory when int is too large

```java
short year = 2024;
short population = 30000;
short altitude = -500;
```

**Real-world example:**
```java
// Year (1900-2100)
short birthYear = 1995;

// Small city population
short villagePopulation = 5000;
```

#### 3. int

**Size:** 4 bytes (32 bits)  
**Range:** -2,147,483,648 to 2,147,483,647  
**Default Value:** 0  
**Use:** Most commonly used integer type

```java
int salary = 50000;
int population = 1000000;
int distance = -500;
```

**Real-world examples:**
```java
// Bank account balance (in rupees)
int accountBalance = 150000;

// Number of students in a university
int totalStudents = 25000;

// Product price (in paise)
int productPrice = 99900; // ₹999.00
```

#### 4. long

**Size:** 8 bytes (64 bits)  
**Range:** -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807  
**Default Value:** 0L  
**Use:** When int is not large enough

```java
long worldPopulation = 7800000000L; // Note the 'L' suffix
long distanceToSun = 149600000000L;
long nationalDebt = 5000000000000L;
```

**Important:** Always use 'L' or 'l' suffix for long literals (prefer uppercase 'L')

**Real-world examples:**
```java
// Mobile number
long phoneNumber = 9876543210L;

// Credit card number
long cardNumber = 1234567890123456L;

// File size in bytes
long fileSize = 5368709120L; // 5 GB
```

#### 5. float

**Size:** 4 bytes (32 bits)  
**Range:** Approximately ±3.4 × 10³⁸ (6-7 decimal digits precision)  
**Default Value:** 0.0f  
**Use:** Decimal numbers with less precision

```java
float price = 99.99f; // Note the 'f' suffix
float pi = 3.14f;
float temperature = 36.6f;
```

**Important:** Always use 'f' or 'F' suffix for float literals

**Real-world examples:**
```java
// Product price
float itemPrice = 299.50f;

// Body temperature
float bodyTemp = 98.6f;

// Fuel price per liter
float petrolPrice = 105.75f;
```

#### 6. double

**Size:** 8 bytes (64 bits)  
**Range:** Approximately ±1.7 × 10³⁰⁸ (15 decimal digits precision)  
**Default Value:** 0.0d  
**Use:** Default choice for decimal numbers (more precise than float)

```java
double salary = 50000.75;
double pi = 3.14159265359;
double distance = 384400.0; // Distance to moon in km
```

**Real-world examples:**
```java
// Scientific calculations
double gravity = 9.80665;

// Financial calculations
double accountBalance = 1234567.89;

// Geographic coordinates
double latitude = 28.6139;
double longitude = 77.2090;
```

**float vs double:**
```java
float f = 3.14159265359f;
double d = 3.14159265359;

System.out.println("float:  " + f); // 3.1415927 (less precision)
System.out.println("double: " + d); // 3.14159265359 (more precision)
```

#### 7. char

**Size:** 2 bytes (16 bits)  
**Range:** 0 to 65,535 (Unicode characters)  
**Default Value:** '\u0000'  
**Use:** Store single characters

```java
char grade = 'A';
char symbol = '$';
char letter = 'Z';
char digit = '5'; // Character '5', not number 5
```

**Unicode characters:**
```java
char heart = '\u2665';     // ♥
char smiley = '\u263A';    // ☺
char rupee = '\u20B9';     // ₹
char devanagariA = '\u0905'; // अ
```

**Escape sequences:**
```java
char newline = '\n';       // New line
char tab = '\t';           // Tab
char backslash = '\\';     // Backslash
char singleQuote = '\'';   // Single quote
char doubleQuote = '\"';   // Double quote
```

**Real-world examples:**
```java
// Grade system
char studentGrade = 'A';

// Gender
char gender = 'M'; // M for Male, F for Female

// Yes/No responses
char response = 'Y';
```

#### 8. boolean

**Size:** Not precisely defined (typically 1 bit)  
**Values:** true or false  
**Default Value:** false  
**Use:** Logical conditions

```java
boolean isActive = true;
boolean hasLicense = false;
boolean isMarried = true;
```

**Real-world examples:**
```java
// User account status
boolean isLoggedIn = false;
boolean isVerified = true;

// Product availability
boolean inStock = true;

// Eligibility checks
boolean isEligible = (age >= 18);
```

### Data Type Comparison Table

| Type | Size | Range | Default | Example |
|------|------|-------|---------|---------|
| byte | 1 byte | -128 to 127 | 0 | `byte age = 25;` |
| short | 2 bytes | -32,768 to 32,767 | 0 | `short year = 2024;` |
| int | 4 bytes | -2.1B to 2.1B | 0 | `int salary = 50000;` |
| long | 8 bytes | -9.2E18 to 9.2E18 | 0L | `long phone = 9876543210L;` |
| float | 4 bytes | ±3.4E38 | 0.0f | `float price = 99.99f;` |
| double | 8 bytes | ±1.7E308 | 0.0d | `double pi = 3.14159;` |
| char | 2 bytes | 0 to 65,535 | '\u0000' | `char grade = 'A';` |
| boolean | 1 bit | true/false | false | `boolean flag = true;` |

### Example: Using All Primitive Types

```java
public class DataTypesDemo {
    public static void main(String[] args) {
        // Integer types
        byte age = 25;
        short year = 2024;
        int population = 1400000000;
        long phoneNumber = 9876543210L;
        
        // Floating-point types
        float price = 99.99f;
        double pi = 3.14159265359;
        
        // Character type
        char grade = 'A';
        
        // Boolean type
        boolean isActive = true;
        
        // Display all values
        System.out.println("Age (byte): " + age);
        System.out.println("Year (short): " + year);
        System.out.println("Population (int): " + population);
        System.out.println("Phone (long): " + phoneNumber);
        System.out.println("Price (float): " + price);
        System.out.println("Pi (double): " + pi);
        System.out.println("Grade (char): " + grade);
        System.out.println("Active (boolean): " + isActive);
    }
}
```

**Output:**
```
Age (byte): 25
Year (short): 2024
Population (int): 1400000000
Phone (long): 9876543210
Price (float): 99.99
Pi (double): 3.14159265359
Grade (char): A
Active (boolean): true
```


