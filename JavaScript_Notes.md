# JavaScript_Notes

### Basic Syntax:

#### Variabels
```js
// Variabels
// Using let (block-scoped)
let x = 10;

// Using const (block-scoped and immutable)
const y = 20;

// Using var (function-scoped)
var z = 30;
```

#### Data Types:
```js
let number = 42;             // Number
let string = "Hello World";  // String
let boolean = true;          // Boolean
let array = [1, 2, 3];       // Array
let object = {               // Object
    name: "Alice",
    age: 25
};
let undefinedVar;            // Undefined
let nullVar = null;          // Null
```

#### Functions:
```js
// Function Declaration
function greet(name) {
    return "Hello, " + name;
}

// Function Expression
const greet = function(name) {
    return "Hello, " + name;
};

// Arrow Function
const greet = (name) => {
    return "Hello, " + name;
};

// Arrow Function (concise syntax)
const greet = name => "Hello, " + name;

```

#### Control Structures:
```js
// If-Else
if (x > 10) {
    console.log("x is greater than 10");
} else {
    console.log("x is not greater than 10");
}

// Switch
switch (day) {
    case 1:
        console.log("Monday");
        break;
    case 2:
        console.log("Tuesday");
        break;
    default:
        console.log("Other day");
}

// For Loop
for (let i = 0; i < 5; i++) {
    console.log(i);
}

// While Loop
let i = 0;
while (i < 5) {
    console.log(i);
    i++;
}

```

#### Arrays:
```js
let fruits = ["Apple", "Banana", "Cherry"];

// Accessing elements
console.log(fruits[0]); // Apple

// Looping through array
fruits.forEach(fruit => {
    console.log(fruit);
});

// Adding an element
fruits.push("Durian");

// Removing an element
fruits.pop(); // Removes last element

```

#### Objects:
```js
let person = {
    firstName: "John",
    lastName: "Doe",
    age: 30,
    fullName: function() {
        return this.firstName + " " + this.lastName;
    }
};

// Accessing properties
console.log(person.firstName); // John

// Accessing methods
console.log(person.fullName()); // John Doe

// Adding a new property
person.gender = "male";

// Deleting a property
delete person.age;

```

#### Events:
```js
// Adding an event listener
document.getElementById("myButton").addEventListener("click", function() {
    alert("Button clicked!");
});

```

#### Promises (for asynchronous code):
```js
let promise = new Promise((resolve, reject) => {
    // Simulate an async operation (e.g., network request)
    setTimeout(() => {
        resolve("Success!");
    }, 1000);
});

promise.then(result => {
    console.log(result); // Success!
}).catch(error => {
    console.error(error);
});

```

#### Example:
```html
<!DOCTYPE html>
<html>
<head>
    <title>JavaScript Example</title>
    <script>
        function changeText() {
            document.getElementById("myParagraph").innerText = "Text changed!";
        }
    </script>
</head>
<body>
    <p id="myParagraph">Original text</p>
    <button onclick="changeText()">Click me</button>
</body>
</html>

```
