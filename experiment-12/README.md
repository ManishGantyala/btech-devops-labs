# Experiment 12 – Develop Test Cases for the Containerized Application Using Selenium

## Objective

To develop and execute Selenium test cases against the containerized TechFest 2026 registration application (deployed in Experiment 07/08), covering valid registration, input filtering behavior, and required-field validation.

## Concept

### What Is Selenium

Selenium is an open-source framework for automating web browsers. It allows a program — in this experiment, a Python script — to control a real browser and interact with a web page the same way a person would: opening a URL, filling in form fields, clicking buttons, and reading back what the page displays.

### What Is Selenium WebDriver

**Selenium WebDriver** is the specific part of Selenium used in this experiment — the API (`from selenium import webdriver`) that a program uses to create and control a browser session: navigating to a page, locating elements on it, and interacting with them. In `test_techfest_cases.py`, `webdriver.Chrome(options=options)` is what creates this controlled browser session for each test case.

### Why Selenium Is Used for This Experiment

The containerized TechFest application is a real, running web page — its form validation (name/phone filtering) happens in client-side JavaScript, and its success message is only set after a real form submission. Selenium is used here to drive the actual rendered page — entering data, submitting the form, and reading back what it displays — so each test case verifies the container's real, running behavior rather than the application's source code in isolation.

### How Selenium Interacts with Chromium Through ChromeDriver

Selenium WebDriver does not talk to a browser directly. It sends commands to **ChromeDriver**, a separate program that acts as the bridge between Selenium and Chromium: ChromeDriver receives each command from Selenium (open this URL, find this element, click it, read its text/value) and carries it out in the actual browser, then reports the result back.

```text
Python test
    ↓
Selenium WebDriver
    ↓
ChromeDriver
    ↓
Chromium
    ↓
Containerized TechFest application
```

## Application Under Test

The application under test is the containerized TechFest 2026 event registration application from earlier experiments:

- **Container name:** `techfest-container-v2`
- **Image:** `techfest-app:v2`
- **Application URL:** `http://localhost:8081`
- **Server:** `nginx/1.31.4`

Reachability was confirmed with:

```bash
curl -I http://localhost:8081
```

which returned `HTTP/1.1 200 OK`.

### Relevant Application Behavior

Form elements:

| Field | Identifier |
|---|---|
| Name | `id="name"` |
| Email | `id="email"` |
| Phone | `id="phone"` |
| Department | `id="department"` (select) |
| Year | `id="year"` (select) |
| Event | `id="event"` (select) |
| Submit button | `button[type="submit"]` |
| Result message | `id="message"` |

Select values: `department` — `cse`, `ece`, `eee`, `mech`, `civil`; `year` — `1`, `2`, `3`, `4`; `event` — `web-development`, `cloud-computing`, `ai-ml`.

Client-side JavaScript behavior:

- The **name** input removes any character that is not `A-Z`, `a-z`, or a space.
- The **phone** input removes any character that is not a digit.
- On successful form submission, the message becomes `"Registration successful!"`.

## Tools / Technologies Used

- Python **3.12.3**
- Selenium **4.47.0** (from the existing Experiment 10 virtual environment)
- Chromium **151.0.7922.108**
- ChromeDriver **151.0.7922.108**

## Environment / Setup

This experiment reuses the Python virtual environment already set up in Experiment 10 (`experiment-10/.venv`), which has Selenium 4.47.0 installed. Selenium runs on the WSL/Linux side, with Chromium (151.0.7922.108) and a matching ChromeDriver (151.0.7922.108), the same setup used in Experiments 10 and 11.

Chromium is already running with remote debugging enabled at `127.0.0.1:9222`. `test_techfest_cases.py` connects to this **already-running** session rather than launching its own browser. See [Our debuggerAddress Approach](#our-debuggeraddress-approach) below.

The application under test runs as the `techfest-container-v2` container, exposing the TechFest registration app at `http://localhost:8081`.

## Our debuggerAddress Approach

`test_techfest_cases.py` defines a shared `create_driver()` helper, used by every test case:

```python
def create_driver():
    options = Options()
    options.add_experimental_option(
        "debuggerAddress",
        "127.0.0.1:9222"
    )
    return webdriver.Chrome(options=options)
```

instead of having Selenium start and manage its own browser process. This means:

- A Chromium instance must already be running with remote debugging enabled on port `9222` **before** the script is run — each test case attaches to that existing session rather than launching a new one.
- Selenium is not responsible for starting or stopping Chromium in this setup; `driver.quit()` at the end of each test ends that test's WebDriver session but does not necessarily close a browser it didn't launch.
- This is the same approach used in Experiments 10 and 11, applied here across four separate test cases, each creating its own driver session via `create_driver()`.

## Complete Testing Flow

The actual flow followed in this experiment, from starting Chromium through verifying all test cases, was:

```text
Chromium started with remote debugging
        ↓
Selenium attaches to 127.0.0.1:9222
        ↓
Open containerized TechFest application at http://localhost:8081
        ↓
Execute Selenium test cases
        ↓
Interact with form elements
        ↓
Verify expected behavior
        ↓
All test cases pass
```

## Project Structure

```text
experiment-12/
├── test_techfest_cases.py
└── README.md
```

## `test_techfest_cases.py`

**Purpose:** to automate and verify four distinct behaviors of the containerized TechFest registration form — valid submission, name filtering, phone filtering, and required-field handling — each as its own test function, following the complete testing flow described above.

The file defines a shared `create_driver()` helper (see [Our debuggerAddress Approach](#our-debuggeraddress-approach)), four test functions — `test_valid_registration()`, `test_name_input_filtering()`, `test_phone_input_filtering()`, `test_required_fields()` — each creating its own driver session, and calls all four directly at the end of the file, followed by a final success message. No test framework such as pytest is used; the functions are plain Python functions invoked directly.

## Test Cases

### TC01 – Valid Registration

- Opens `http://localhost:8081`.
- Enters `name` = `Test Student`, `email` = `test@example.com`, `phone` = `9876543210`.
- Selects `department` = `cse`, `year` = `3`, `event` = `web-development`.
- Submits the form.
- Verifies `message` equals `"Registration successful!"`.

### TC02 – Name Input Filtering

- Enters `Test123@ Student!` into the `name` field.
- Verifies the resulting `name` field value equals `"Test Student"`, confirming characters other than letters and spaces are removed.

### TC03 – Phone Input Filtering

- Enters `987abc654@321` into the `phone` field.
- Verifies the resulting `phone` field value equals `"987654321"`, confirming non-digit characters are removed.

### TC04 – Required Fields

- Opens the application.
- Clicks the submit button with all required fields left empty.
- Verifies the `message` remains empty (no success message is shown).

## Actual Commands and Verification Performed

1. Activate the Experiment 10 virtual environment:

   ```bash
   source ../experiment-10/.venv/bin/activate
   ```

2. Confirm the container is reachable:

   ```bash
   curl -I http://localhost:8081
   ```

3. Ensure Chromium is already running with remote debugging enabled at `127.0.0.1:9222` (required, since the script connects via `debuggerAddress` rather than launching its own browser).

4. Run the test cases:

   ```bash
   python test_techfest_cases.py
   ```

## Verification / Results

**`test_techfest_cases.py` – exact verified output:**

```text
TC01 - Valid registration: Registration successful!
TC02 - Name after filtering: Test Student
TC03 - Phone after filtering: 987654321
TC04 - Message with empty required fields: 
All Selenium test cases passed successfully.
```

This output confirms all four test cases executed successfully against the running `techfest-container-v2` container: a valid registration produced the expected success message, the name and phone fields correctly filtered invalid characters, and submitting with empty required fields correctly left the message blank — completing the flow described in [Complete Testing Flow](#complete-testing-flow) above.

## Conclusion

Selenium 4.47.0, reused from the Experiment 10 virtual environment, was used via Selenium WebDriver and ChromeDriver to develop and execute four test cases against the containerized TechFest registration application (`techfest-container-v2`, image `techfest-app:v2`) at `http://localhost:8081`, connected to a running Chromium instance (151.0.7922.108) on WSL/Linux via its remote debugging address (`127.0.0.1:9222`). All four test cases — valid registration, name input filtering, phone input filtering, and required-field validation — executed successfully, ending with `All Selenium test cases passed successfully.`
