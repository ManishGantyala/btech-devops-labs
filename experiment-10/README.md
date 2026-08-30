# Experiment 10 – Selenium Automated Testing

## Objective

To install and use Selenium WebDriver for automated browser testing, first with a basic browser automation check, and then to automate and verify submission of the TechFest event registration form (from Experiments 01/07).

## Concept

### What Is Selenium

Selenium is an open-source framework for automating web browsers. It allows a program — in this experiment, a Python script — to control a real browser and interact with a web page the same way a person would: opening a URL, filling in form fields, clicking buttons, and reading back what the page displays.

### What Is Selenium WebDriver

**Selenium WebDriver** is the specific part of Selenium used in this experiment — the API (`from selenium import webdriver`) that a program uses to create and control a browser session: navigating to a page, locating elements on it, and interacting with them. In both test scripts here, `webdriver.Chrome(options=options)` is what creates this controlled browser session.

### Why Selenium Is Used in This Experiment

Earlier experiments produced a real, working web application — the TechFest registration form (Experiments 01/07). Verifying that it works by opening it, filling in the fields by hand, clicking submit, and checking the result is something a person can do, but it isn't repeatable without doing it again each time. Selenium is used here to automate exactly that sequence of actions and check the result programmatically, which is the basic idea behind automated browser/UI testing.

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

- Python 3.12 (virtual environment: `experiment-10/.venv`)
- Selenium **4.47.0**
- Chromium, installed on WSL/Linux
- Chromium version used during successful testing: **151.0.7922.108**
- ChromeDriver version used: **151.0.7922.108**

## Environment / Setup

A Python virtual environment was created at `experiment-10/.venv`, with Selenium 4.47.0 installed into it. This entire setup runs on the **WSL/Linux side**: Chromium (version 151.0.7922.108) and a matching ChromeDriver (151.0.7922.108) are both installed on WSL/Linux, so that Selenium, ChromeDriver, and Chromium are all operating within the same Linux environment rather than crossing into the Windows host.

Rather than have Selenium launch and manage its own Chromium process, both test scripts connect to an **already-running** Chromium instance via Selenium's `debuggerAddress` option (`127.0.0.1:9222`). See [Our debuggerAddress Approach](#our-debuggeraddress-approach) below.

`.venv/` is excluded from version control via `experiment-10/.gitignore`.

## Our debuggerAddress Approach

Both scripts use:

```python
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
```

instead of having Selenium start and manage its own browser process. This means:

- A Chromium instance must already be running with remote debugging enabled on port `9222` **before** either script is run — the scripts attach to that existing session rather than launching a new one.
- Selenium is not responsible for starting or stopping Chromium in this setup; `driver.quit()` ends the WebDriver session but does not necessarily close a browser it didn't launch.
- This differs from Selenium's more common pattern of letting `webdriver.Chrome()` start its own managed browser instance — the `debuggerAddress` approach was used here to connect to an already-running Chromium instead.

## Complete Testing Flow

The actual flow followed in this experiment, from starting Chromium through verifying the result, was:

```text
Chromium started with remote debugging
        ↓
Selenium attaches to 127.0.0.1:9222
        ↓
Open application (URL)
        ↓
Locate elements
        ↓
Enter data
        ↓
Select values
        ↓
Submit
        ↓
Read message
        ↓
Assert expected result
        ↓
Test passes
```

This flow describes the setup and execution used by both scripts, with `test_browser.py` following a simpler version of it (open page, read title — no form interaction) and `test_techfest.py` following the full sequence, described next.

## Project Structure

```text
experiment-10/
├── test_browser.py
├── test_techfest.py
├── .gitignore
└── README.md
```

*(`.venv/` exists locally as the Python virtual environment but is git-ignored and not treated as a tracked project file.)*

## `test_browser.py`

**Purpose:** a basic Selenium connectivity check, confirming Selenium can attach to the running Chromium session and control it, before attempting the more complete form-automation test.

It connects to the running Chromium session via `debuggerAddress`, navigates to `https://example.com`, and prints the page title:

```python
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(options=options)
driver.get("https://example.com")
print("Title:", driver.title)
driver.quit()
```

## `test_techfest.py`

**Purpose:** to automate and verify the full registration flow of the TechFest form (Experiments 01/07), following the complete testing flow described above.

Automates the TechFest registration form at `http://localhost:8082`. It:

1. Connects to the running Chromium session via `debuggerAddress`.
2. Navigates to `http://localhost:8082`.
3. Fills in the form:
   - `name` = `Test Student`
   - `email` = `test@example.com`
   - `phone` = `9876543210`
4. Selects:
   - `department` = `cse`
   - `year` = `3`
   - `event` = `web-development`
5. Clicks the submit button.
6. Reads the resulting `#message` text and asserts it equals `"Registration successful!"`.

## Actual Commands and Verification Performed

1. Activate the virtual environment:

   ```bash
   source .venv/bin/activate
   ```

2. Start Chromium with remote debugging enabled on port `9222`, so it is listening at `127.0.0.1:9222` (required, since both scripts connect via `debuggerAddress` rather than launching their own browser).

3. For `test_techfest.py`, ensure the TechFest registration app is being served at `http://localhost:8082`.

4. Run either script directly:

   ```bash
   python test_browser.py
   python test_techfest.py
   ```

## Verification / Results

**`test_browser.py` – successful output:**

```text
Title: Example Domain
```

**`test_techfest.py` – successful output:**

```text
Registration message: Registration successful!
Selenium test passed successfully.
```

Both results confirm Selenium was able to attach to the running Chromium session via `debuggerAddress`, interact with a real page (or the TechFest form), and correctly read back the resulting state — completing the flow described in [Complete Testing Flow](#complete-testing-flow) above.

## Conclusion

Selenium 4.47.0 was installed and used, via Selenium WebDriver and ChromeDriver, to automate two browser test scenarios against a running Chromium instance (151.0.7922.108) on WSL/Linux, connected to via its remote debugging address (`127.0.0.1:9222`): a basic page-title check against `https://example.com`, and an end-to-end form submission check against the TechFest registration app at `http://localhost:8082`. Both scripts executed successfully, with `test_browser.py` printing the expected page title and `test_techfest.py` confirming the registration form correctly returned `"Registration successful!"`.
