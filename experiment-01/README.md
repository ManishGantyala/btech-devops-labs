# Experiment 01 - Event Registration Web Application

## 1. Aim

To write code for a simple user registration form for an event.

## 2. Objective

- Create a simple user registration form for an event.
- Design the registration form using HTML and CSS.
- Provide input fields for user registration details.
- Use JavaScript for client-side input handling.
- Display a registration success message after form submission.

## 3. Requirements

The following technologies were used:

- HTML
- CSS
- JavaScript

## 4. Concept

### What Are HTML, CSS, and JavaScript?

A web page is built from three technologies, each handling a different concern:

| Technology | File | Role |
|---|---|---|
| HTML | `index.html` | Defines the **structure** — the elements on the page: headings, labels, input fields, buttons |
| CSS | `style.css` | Defines the **appearance** — colours, font sizes, spacing, borders, layout |
| JavaScript | `script.js` | Defines the **behaviour** — what the page does when a user types or clicks: filtering input, displaying messages |

The browser loads all three files together. `index.html` connects to the other two using standard HTML tags:

```html
<link rel="stylesheet" href="style.css">   <!-- loads the CSS -->
<script src="script.js"></script>           <!-- loads the JavaScript -->
```

### Why a Web Form?

Collecting event registrations on paper or by email is error-prone: entries arrive in different formats, required fields get skipped, and the data is hard to process consistently. A web form enforces structure — every submission provides the same fields in the same order. The browser's built-in input types (`email`, `tel`, `required`) catch formatting mistakes immediately. JavaScript adds a second layer by filtering invalid characters from the name and phone fields as the user types, before the form is ever submitted.

### What "Client-Side" Means

This application is **client-side only**: all logic runs inside the visitor's browser. There is no server and no database. When the form is submitted, `script.js` calls `event.preventDefault()`, which stops the browser's default form-submission behaviour (which would normally send data to a server) and instead shows the success message locally. Because nothing is transmitted over a network, the form works by opening `index.html` directly as a local file — no installation or running server is required.

## 5. Project Structure

```text
experiment-01/
├── index.html
├── style.css
├── script.js
└── README.md
```

## 6. Application Description

The application is a TechFest 2026 event registration form.

The registration form contains the following fields:

- Full Name
- Email
- Phone Number
- Department
- Year of Study
- Event Selection

A Register button is provided to submit the form.

JavaScript is used to:

- Restrict the Full Name field to alphabetic characters and spaces.
- Restrict the Phone Number field to numeric characters.
- Display a "Registration successful!" message when the form is submitted.

## 7. Implementation

### 7.1 HTML Implementation

The `index.html` file defines the structure of the TechFest 2026 event registration form.

The page contains:

- Page heading
- Event description heading
- Registration form
- Full Name input
- Email input
- Phone Number input
- Department selection
- Year of Study selection
- Event selection
- Register button
- Registration message

### 7.2 CSS Implementation

The `style.css` file is used to style the registration page.

The styling includes:

- Page background
- Heading alignment
- Registration form container
- Form labels
- Input fields
- Selection fields
- Register button
- Button hover effect
- Input and select focus styling

### 7.3 JavaScript Implementation

The `script.js` file provides client-side functionality.

The Full Name field removes characters other than letters and spaces.

The Phone Number field removes characters other than numbers.

When the registration form is submitted, `event.preventDefault()` stops the browser from its default behaviour of navigating to a new page or sending a network request. Instead, the success message is written directly into the `#message` element on the same page:

```text
Registration successful!
```

## 8. Source Code

### 8.1 index.html

```html
<!DOCTYPE html>
<html>

<head>
    <title>TechFest 2026 - Event Registration</title>
    <link rel="stylesheet" href="style.css">
</head>

<body>
    <h1>TechFest 2026 - Event Registration</h1>
    <h2>Register for the upcoming events</h2>

    <div class="form-container">

        <form id="registrationForm">

            <label for="name">Full Name:</label>
            <input
                type="text"
                id="name"
                name="name"
                required
            >

            <label for="email">Email:</label>
            <input
                type="email"
                id="email"
                name="email"
                required
            >

            <label for="phone">Phone Number:</label>
            <input
                type="tel"
                id="phone"
                name="phone"
                maxlength="10"
                inputmode="numeric"
                required
            >

            <label for="department">Department:</label>
            <select id="department" name="department" required>
                <option value="">Select Department</option>
                <option value="cse">Computer Science and Engineering</option>
                <option value="ece">Electronics and Communication Engineering</option>
                <option value="eee">Electrical and Electronics Engineering</option>
                <option value="mech">Mechanical Engineering</option>
                <option value="civil">Civil Engineering</option>
            </select>

            <label for="year">Year of Study:</label>
            <select id="year" name="year" required>
                <option value="">Select Year</option>
                <option value="1">First Year</option>
                <option value="2">Second Year</option>
                <option value="3">Third Year</option>
                <option value="4">Fourth Year</option>
            </select>

            <label for="event">Select Event:</label>
            <select id="event" name="event" required>
                <option value="">Select Event</option>
                <option value="web-development">
                    Web Development Workshop
                </option>
                <option value="cloud-computing">
                    Cloud Computing Workshop
                </option>
                <option value="ai-ml">
                    AI and Machine Learning Seminar
                </option>
            </select>

            <button type="submit">Register</button>

        </form>

        <p id="message"></p>
    </div>

    <script src="script.js"></script>
</body>

</html>
```

### 8.2 style.css

```css
body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
}

h1 {
    text-align: center;
    margin-top: 30px;
}

h2 {
    text-align: center;
    margin-bottom: 20px;
}

.form-container {
    width: 400px;
    margin: 40px auto;
    padding: 20px;
    background-color: white;
    border-radius: 8px;
    border: 1px solid #ddd;
}

.form-container label {
    display: block;
    margin-bottom: 6px;
    font-weight: bold;
}

.form-container input {
    width: 100%;
    padding: 10px;
    margin-bottom: 15px;
    box-sizing: border-box;
}

.form-container select {
    width: 100%;
    padding: 10px;
    margin-bottom: 15px;
    box-sizing: border-box;
}

.form-container button {
    width: 100%;
    padding: 10px;
    margin-top: 10px;
    cursor: pointer;
}

.form-container button:hover {
    opacity: 0.9;
}

.form-container input:focus,
.form-container select:focus {
    outline: 2px solid #333;
}
```

### 8.3 script.js

```javascript
const nameInput = document.getElementById("name");
const phoneInput = document.getElementById("phone");

nameInput.addEventListener("input", function () {
    this.value = this.value.replace(/[^A-Za-z ]/g, "");
});

phoneInput.addEventListener("input", function () {
    this.value = this.value.replace(/[^0-9]/g, "");
});

const registrationForm = document.getElementById("registrationForm");
const message = document.getElementById("message");

registrationForm.addEventListener("submit", function (event) {
    event.preventDefault();

    message.textContent = "Registration successful!";
});
```

## 9. Procedure

### Step 1: Open the Experiment Directory

The experiment files are in the `experiment-01/` directory. Three files are present: `index.html`, `style.css`, and `script.js`.

### Step 2: Review the HTML File

Open `index.html` in a text editor. Observe how the form structure is defined — each `<label>` paired with an `<input>` or `<select>` corresponds to one field on the registration form. The `id` attribute on each field is what JavaScript uses to locate and interact with that element.

### Step 3: Review the CSS File

Open `style.css` in a text editor. Observe how the `.form-container` class and its nested selectors control the appearance of the form box, labels, inputs, and button.

### Step 4: Review the JavaScript File

Open `script.js` in a text editor. Observe the three event listeners: one on the name input (removes non-letter characters on every keystroke), one on the phone input (removes non-digit characters on every keystroke), and one on the form's `submit` event (`event.preventDefault()` stops the browser from sending a network request; `message.textContent` sets the confirmation text).

### Step 5: Observe How the Files Are Linked

The HTML file connects to the CSS in the `<head>` section:

```html
<link rel="stylesheet" href="style.css">
```

and to the JavaScript at the bottom of `<body>`:

```html
<script src="script.js"></script>
```

Placing the `<script>` tag at the bottom of `<body>` ensures all HTML elements exist before JavaScript tries to find them by their `id`.

### Step 6: Open the Application in a Browser

Open `index.html` directly in a web browser — no web server is required.

**Option 1 — File manager:** Navigate to the `experiment-01/` folder and double-click `index.html`.

**Option 2 — Terminal (Linux / WSL):**

```bash
xdg-open experiment-01/index.html
```

**Observe:** The TechFest 2026 Event Registration form loads in the browser, showing all six fields and the Register button.

## 10. Application Features

### User Registration Fields

The form provides fields for:

- Full Name
- Email
- Phone Number
- Department
- Year of Study
- Event

### Name Input Handling

The JavaScript implementation removes characters other than letters and spaces from the Full Name field.

### Phone Number Input Handling

The JavaScript implementation removes characters other than numeric characters from the Phone Number field.

### Registration Message

After submitting the form, the application displays:

```text
Registration successful!
```

## 11. Verification

Open `experiment-01/index.html` in a browser using Step 6 above. Verify the following:

| Check | How to verify | Expected result |
|---|---|---|
| Form loads correctly | Open the page | All six fields and the Register button are visible |
| Name filtering | Type `"Test123 Student!"` into Full Name | Field shows only `"Test Student"` — digits and `!` removed immediately |
| Phone filtering | Type `"98765abc"` into Phone Number | Field shows only `"98765"` — letters removed immediately |
| Form submission | Fill all fields and click Register | `"Registration successful!"` appears below the form |
| Required field validation | Leave a field empty and click Register | Browser highlights the empty field and blocks submission; no success message appears |

## 12. Result

The simple user registration form for the TechFest 2026 event was developed using HTML, CSS, and JavaScript.
