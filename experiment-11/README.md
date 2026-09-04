# Experiment 11 – JavaScript Calculator Selenium Automated Testing

## Objective

To use Selenium WebDriver to automate and verify a simple JavaScript calculator application — entering two numbers, clicking Add, and asserting the computed result is correct.

## Concept

### What Is Selenium

Selenium is an open-source framework for automating web browsers. It allows a program — in this experiment, a Python script — to control a real browser and interact with a web page the same way a person would: opening a URL, filling in input fields, clicking buttons, and reading back what the page displays.

### What Is Selenium WebDriver

**Selenium WebDriver** is the specific part of Selenium used in this experiment — the API (`from selenium import webdriver`) that a program uses to create and control a browser session: navigating to a page, locating elements on it, and interacting with them. In `test_calculator.py`, `webdriver.Chrome(options=options)` is what creates this controlled browser session.

### Why Selenium Is Used in This Experiment

The calculator application performs its addition entirely in client-side JavaScript (`addNumbers()` in `script.js`) — there is no server-side logic to test directly. Selenium is used here to drive the actual browser UI — entering values, clicking the button, and reading the displayed result — so the test verifies the real, rendered behavior of the page rather than the JavaScript function in isolation.

### How Selenium Interacts with Chromium Through ChromeDriver

Selenium WebDriver does not talk to a browser directly. It sends commands to **ChromeDriver**, a separate program that acts as the bridge between Selenium and Chromium: ChromeDriver receives each command from Selenium (open this URL, find this element, click it, read its text) and carries it out in the actual browser, then reports the result back.

```text
Python test
     ↓
Selenium WebDriver
     ↓
ChromeDriver
     ↓
Chromium
     ↓
Web application
```

## Tools / Technologies Used

- Python **3.12.3**
- Selenium **4.47.0** (from the existing Experiment 10 virtual environment)
- Chromium **151.0.7922.108**
- ChromeDriver **151.0.7922.108**

## Environment / Setup

This experiment reuses the Python virtual environment already set up in Experiment 10 (`experiment-10/.venv`), which has Selenium 4.47.0 installed. Chromium (151.0.7922.108) and a matching ChromeDriver (151.0.7922.108) are installed on the WSL/Linux side, the same setup used in Experiment 10.

As in Experiment 10, Selenium does not launch its own Chromium process. `test_calculator.py` connects to an **already-running** Chromium instance via Selenium's `debuggerAddress` option, at `127.0.0.1:9222`. See [Our debuggerAddress Approach](#our-debuggeraddress-approach) below.

The calculator application is served at `http://localhost:8000`.

## Our debuggerAddress Approach

`test_calculator.py` uses:

```python
options = Options()
options.add_experimental_option(
    "debuggerAddress",
    "127.0.0.1:9222"
)

driver = webdriver.Chrome(options=options)
```

instead of having Selenium start and manage its own browser process. This means:

- A Chromium instance must already be running with remote debugging enabled on port `9222` **before** the script is run — the script attaches to that existing session rather than launching a new one.
- Selenium is not responsible for starting or stopping Chromium in this setup; `driver.quit()` ends the WebDriver session but does not necessarily close a browser it didn't launch.
- This is the same approach used for the tests in Experiment 10, applied here to the calculator application.

## Complete Testing Flow

The actual flow followed in this experiment, from starting Chromium through verifying the result, was:

```text
Chromium started with remote debugging
        ↓
Selenium attaches to 127.0.0.1:9222
        ↓
Open calculator application
        ↓
Locate input elements
        ↓
Enter 10 and 20
        ↓
Click Add
        ↓
JavaScript calculates 30
        ↓
Read #result
        ↓
Assert result == "30"
        ↓
Test passes
```

## Project Structure

```text
experiment-11/
├── index.html
├── script.js
├── test_calculator.py
└── README.md
```

## `index.html`

Defines the calculator page: a `firstNumber` input, a `secondNumber` input, an `addButton` button (calling `addNumbers()` on click), and a `result` element that displays the computed sum:

```html
<label for="firstNumber">First Number:</label>
<input type="number" id="firstNumber">

<label for="secondNumber">Second Number:</label>
<input type="number" id="secondNumber">

<button id="addButton" onclick="addNumbers()">Add</button>

<p>Result: <span id="result"></span></p>
```

## `script.js`

Implements `addNumbers()`, which reads the values of `firstNumber` and `secondNumber`, converts them to numbers, adds them, and writes the result into the `result` element's text content:

```javascript
function addNumbers() {
    const firstNumber = Number(document.getElementById("firstNumber").value);
    const secondNumber = Number(document.getElementById("secondNumber").value);

    const result = firstNumber + secondNumber;

    document.getElementById("result").textContent = result;
}
```

## `test_calculator.py`

**Purpose:** to automate and verify the calculator's addition behavior through the actual rendered page, following the complete testing flow described above.

Automates the calculator application at `http://localhost:8000`. It:

1. Connects to the running Chromium session via `debuggerAddress`.
2. Navigates to `http://localhost:8000`.
3. Enters `10` into `firstNumber` and `20` into `secondNumber`.
4. Clicks `addButton`.
5. Reads the resulting `#result` text and asserts it equals `"30"`.

**Note on the string comparison:** `element.text` in Selenium always returns a Python `str`, not a number. Even though the calculator computes a numeric result (30), the DOM renders it as text. This is why the assertion is `result == "30"` (a string), not `result == 30` (an integer). If you accidentally compare against an integer, the assertion will fail even when the page is showing the correct value.

## Actual Commands and Verification Performed

1. Activate the Experiment 10 virtual environment. **Run this command from inside the `experiment-11/` directory** — the `../` in the path goes up one level to reach `experiment-10/.venv`:

   ```bash
   source ../experiment-10/.venv/bin/activate
   ```

2. Start Chromium with remote debugging enabled on port `9222` (in a separate terminal — keep it running):

   ```bash
   chromium-browser --remote-debugging-port=9222 &
   ```

   If Chromium crashes or fails to start, add `--no-sandbox` to the command — this flag may be needed depending on the WSL2 kernel configuration.

3. Serve the calculator application at `http://localhost:8000` (in a separate terminal, from inside `experiment-11/`):

   ```bash
   python3 -m http.server 8000
   ```

   Keep this server running while the test runs.

4. Run the test:

   ```bash
   python test_calculator.py
   ```

## Verification / Results

**`test_calculator.py` – successful output:**

```text
Calculator result: 30
Selenium test passed successfully.
```

This result confirms Selenium was able to attach to the running Chromium session via `debuggerAddress`, enter `10` and `20` into the calculator's input fields, click `addButton`, and correctly read back `30` as the computed result — completing the flow described in [Complete Testing Flow](#complete-testing-flow) above.

## Conclusion

Selenium 4.47.0, reused from the Experiment 10 virtual environment, was used via Selenium WebDriver and ChromeDriver to automate the JavaScript calculator application on a running Chromium instance (151.0.7922.108) on WSL/Linux, connected to via its remote debugging address (`127.0.0.1:9222`). The test entered `10` and `20`, clicked `addButton`, and asserted the `#result` element showed `"30"`. The script executed successfully, printing `Calculator result: 30` and `Selenium test passed successfully.`
