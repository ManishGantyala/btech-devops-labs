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

## 4. Project Structure

```text
experiment-01/
├── index.html
├── style.css
├── script.js
└── README.md
```

## 5. Application Description

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

## 6. Implementation

### 6.1 HTML Implementation

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

### 6.2 CSS Implementation

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

### 6.3 JavaScript Implementation

The `script.js` file provides client-side functionality.

The Full Name field removes characters other than letters and spaces.

The Phone Number field removes characters other than numbers.

When the registration form is submitted, the default form submission is prevented and the following message is displayed:

```text
Registration successful!
```

## 7. Source Code

### 7.1 index.html

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

### 7.2 style.css

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

### 7.3 script.js

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

## 8. Procedure

### Step 1: Create the Experiment Directory

The experiment was organized inside the `experiment-01` directory.

### Step 2: Create the HTML File

The `index.html` file was created to define the structure of the event registration form.

### Step 3: Create the CSS File

The `style.css` file was created to provide styling for the registration page and form elements.

### Step 4: Create the JavaScript File

The `script.js` file was created to provide input handling and form submission functionality.

### Step 5: Link the Files

The HTML file links the CSS stylesheet and JavaScript file:

```html
<link rel="stylesheet" href="style.css">
```

and:

```html
<script src="script.js"></script>
```

## 9. Application Features

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

## 10. Verification

The implementation can be verified by opening the event registration page and checking the registration form fields and JavaScript functionality.

The expected registration message after form submission is:

```text
Registration successful!
```

## 11. Result

The simple user registration form for the TechFest 2026 event was developed using HTML, CSS, and JavaScript.
