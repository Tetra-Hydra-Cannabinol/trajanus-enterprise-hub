# CODING QUICK REFERENCE CHEAT SHEET
**Keep this handy while learning!**

---

## 🎯 LEARNING ORDER
1. **HTML** (2 weeks) → Structure
2. **CSS** (2 weeks) → Styling  
3. **JavaScript** (3 weeks) → Interactivity
4. **Python** (4 weeks) → Automation

---

## 📘 HTML ESSENTIALS

### Basic Structure
```html
<!DOCTYPE html>
<html>
<head>
    <title>Page Title</title>
</head>
<body>
    <h1>Main Heading</h1>
    <p>Paragraph text here</p>
</body>
</html>
```

### Most-Used Tags
```html
<h1> to <h6>         Headings
<p>                  Paragraph
<a href="url">       Link
<img src="path">     Image
<div>                Container
<span>               Inline container
<ul> <li>            Unordered list
<ol> <li>            Ordered list
<form>               Form
<input>              Form input
<button>             Button
```

### Common Attributes
```html
class="name"         CSS class
id="name"            Unique ID
style="css"          Inline style
href="url"           Link destination
src="path"           Image/script source
onclick="func()"     JavaScript function
```

---

## 🎨 CSS ESSENTIALS

### How to Apply CSS
```html
<!-- In HTML file -->
<style>
    selector { property: value; }
</style>

<!-- Inline -->
<div style="color: red;">Text</div>

<!-- External file -->
<link rel="stylesheet" href="style.css">
```

### Selectors
```css
element         All <element> tags
.class          All with class="class"
#id             One with id="id"
element.class   <element> with that class
*               Everything
```

### Box Model
```css
margin          Space outside
border          Border line
padding         Space inside
width/height    Content size
```

### Colors
```css
color: red;              Named color
color: #ff0000;          Hex code
color: rgb(255,0,0);     RGB
color: rgba(255,0,0,0.5); RGBA (with transparency)
```

### Layout - Flexbox
```css
.container {
    display: flex;
    justify-content: center;  /* horizontal */
    align-items: center;      /* vertical */
    gap: 10px;               /* spacing */
}
```

### Common Properties
```css
color               Text color
background-color    Background color
font-size           Text size
font-family         Font
margin              Outer spacing
padding             Inner spacing
border              Border
display             Layout type
width/height        Dimensions
```

---

## ⚡ JAVASCRIPT ESSENTIALS

### Variables
```javascript
let name = "Bill";        // Can change
const age = 67;           // Cannot change
var old = "avoid";        // Old way
```

### Functions
```javascript
function greet(name) {
    return "Hello " + name;
}

// Arrow function (modern)
const greet = (name) => {
    return "Hello " + name;
};
```

### DOM Manipulation
```javascript
// Get element
let element = document.getElementById("myId");
let element = document.querySelector(".myClass");

// Change content
element.innerHTML = "New content";
element.textContent = "Text only";

// Change style
element.style.color = "red";

// Add event
element.addEventListener("click", function() {
    console.log("Clicked!");
});
```

### Conditionals
```javascript
if (condition) {
    // do this
} else if (otherCondition) {
    // do that
} else {
    // do something else
}
```

### Loops
```javascript
// For loop
for (let i = 0; i < 10; i++) {
    console.log(i);
}

// For each
array.forEach(item => {
    console.log(item);
});
```

### Arrays
```javascript
let array = [1, 2, 3];
array.push(4);          // Add to end
array.pop();            // Remove from end
array.length;           // Number of items
array[0];               // First item
```

### Objects
```javascript
let person = {
    name: "Bill",
    age: 67,
    greet: function() {
        console.log("Hi!");
    }
};

person.name;            // Access property
person.greet();         // Call method
```

---

## 🐍 PYTHON ESSENTIALS

### Variables
```python
name = "Bill"           # String
age = 67                # Integer
price = 19.99          # Float
is_active = True       # Boolean
```

### Print & Input
```python
print("Hello")          # Output
name = input("Name: ")  # Input
```

### Functions
```python
def greet(name):
    return f"Hello {name}"

result = greet("Bill")
```

### Conditionals
```python
if condition:
    # do this
elif other_condition:
    # do that
else:
    # do something else
```

### Loops
```python
# For loop
for i in range(10):
    print(i)

# For each
for item in list:
    print(item)

# While loop
while condition:
    # do this
```

### Lists
```python
items = [1, 2, 3]
items.append(4)        # Add to end
items.pop()            # Remove from end
len(items)             # Number of items
items[0]               # First item
```

### Dictionaries
```python
person = {
    "name": "Bill",
    "age": 67
}

person["name"]         # Access value
person["city"] = "FL"  # Add new key
```

### File Operations
```python
# Read file
with open("file.txt", "r") as file:
    content = file.read()

# Write file
with open("file.txt", "w") as file:
    file.write("text")
```

### Common Libraries
```python
import os              # File system
import datetime        # Dates/times
import json            # JSON data
from pathlib import Path  # Modern file paths
```

---

## 🛠️ DEBUGGING

### HTML/CSS/JavaScript
1. Open DevTools: **F12**
2. Check **Console** for errors
3. Use **Elements** tab to inspect
4. Add `console.log("test")` to debug JavaScript

### Python
1. Add `print("test")` statements
2. Read error messages carefully
3. Check line numbers in error
4. Use `try/except` to catch errors:
```python
try:
    # risky code
except Exception as e:
    print(f"Error: {e}")
```

---

## 💡 COMMON MISTAKES

### HTML
❌ Forgetting closing tags: `<div>text` 
✅ Close all tags: `<div>text</div>`

❌ Wrong quotes: `href='url"`
✅ Match quotes: `href="url"` or `href='url'`

### CSS
❌ Missing semicolon: `color: red`
✅ End with semicolon: `color: red;`

❌ Wrong selector: `.classname` for id
✅ Match type: `#idname` for id

### JavaScript
❌ Using `=` for comparison
✅ Use `===` for comparison

❌ Forgetting parentheses: `myFunction`
✅ Call with parentheses: `myFunction()`

### Python
❌ Wrong indentation (Python is strict!)
✅ Use consistent spaces (4 spaces)

❌ Using `=` for comparison
✅ Use `==` for comparison

---

## 🚀 QUICK WINS

### Make Page Interactive (JavaScript)
```javascript
document.getElementById("myButton").addEventListener("click", function() {
    alert("Clicked!");
});
```

### Change Styles Dynamically (JavaScript)
```javascript
element.style.backgroundColor = "blue";
element.classList.add("active");
element.classList.remove("hidden");
```

### Read File (Python)
```python
with open("data.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        print(line)
```

### Automate Folder Creation (Python)
```python
import os
folders = ["docs", "images", "scripts"]
for folder in folders:
    os.makedirs(folder, exist_ok=True)
```

---

## 📚 BEST FIRST RESOURCES

**HTML:** W3Schools HTML Tutorial
**CSS:** W3Schools CSS + Flexbox Guide
**JavaScript:** W3Schools JS + JavaScript.info
**Python:** W3Schools Python + Automate the Boring Stuff

**Quick Reference:** Keep cheat sheets open!
**Questions:** Stack Overflow + Claude sessions

---

## ⏱️ DAILY PRACTICE

**15 Minutes/Day:**
- Day 1-2: One W3Schools section
- Day 3: Code along with YouTube tutorial
- Day 4-5: Build something small
- Day 6: Review and experiment
- Day 7: Take a break or work on project

**Stay consistent > Study for hours once**

---

## 🎯 FIRST PROJECTS

1. **HTML Page:** Your resume/bio
2. **CSS Styling:** Make it beautiful
3. **JavaScript:** Add show/hide sections
4. **Python Script:** Organize your downloads folder

**Start small, build confidence!**

---

## 🆘 STUCK? DO THIS

1. Read error message carefully
2. Google the exact error
3. Check Stack Overflow
4. Simplify to smallest version
5. Ask Claude in next session
6. Take a 10-minute break
7. Come back fresh

**Everyone gets stuck. It's normal!**

---

**Print this and keep it near your monitor!**

**Command Center → Learning & Training → Click any language for full resources**

