# B.Tech DevOps Laboratory

A twelve-experiment laboratory series covering the core tools and practices of DevOps: web development, version control, CI/CD pipelines, containerization, container orchestration, and automated browser testing. Each experiment builds on the one before it, using a common event registration application as the subject throughout.

## Experiments

| # | Experiment | Technologies |
|---|---|---|
| 01 | Event Registration Web Application | HTML, CSS, JavaScript |
| 02 | Explore Git and GitHub Commands | Git, GitHub |
| 03 | Practice Source Code Management on GitHub | Git branches, Pull Requests |
| 04 | Jenkins Installation and Setup | Jenkins, systemd |
| 05 | Demonstrate CI/CD Using Jenkins | Jenkins Pipeline, Jenkinsfile, ngrok |
| 06 | Explore Docker Commands for Content Management | Docker CLI |
| 07 | Build and Run an Application Using a Dockerfile | Docker, Dockerfile |
| 08 | Deploy the Dockerized Application to Kubernetes | Kubernetes, kubectl, Kind |
| 09 | Automate Running the Containerized Application Using Kubernetes | Kubernetes Deployments, Services |
| 10 | Selenium Automated Testing | Selenium WebDriver, Python |
| 11 | JavaScript Calculator Selenium Automated Testing | Selenium WebDriver, Python |
| 12 | Develop Test Cases for the Containerized Application Using Selenium | Selenium, Docker, Kubernetes |

## Repository Structure

```
experiment-01/        — HTML/CSS/JS event registration application
experiment-02/        — Git and GitHub experiment notes and README
experiment-03/        — Source code management (no separate source files)
experiment-04/        — Jenkins setup notes
experiment-05/        — Jenkinsfile for the CI/CD pipeline
experiment-06/        — Docker content management notes
experiment-07/        — Dockerfile and application image definition
experiment-08/        — Kubernetes manifests (Deployment, Service)
experiment-09/        — Kubernetes automation manifests
experiment-10/        — Selenium test scripts
experiment-11/        — Selenium calculator test scripts
experiment-12/        — Selenium test cases for the containerized application
DevOps_Laboratory_Manual.pdf   — Complete compiled laboratory manual
DevOps_Laboratory_Manual.md    — Manual source (Markdown)
build_pdf.py                   — Script to regenerate the PDF from Markdown
```

## Usage

The laboratory manual (`DevOps_Laboratory_Manual.pdf`) contains step-by-step instructions for each experiment. Students create their own GitHub repository when they reach Experiment 02 and use it as their working environment throughout the series. This repository serves as a reference for expected file structure, pipeline configuration, and test scripts.

## Platform

All experiments target an Ubuntu/Debian Linux environment. Windows users should run commands from a WSL2 (Windows Subsystem for Linux 2) terminal.

## Reference

`https://github.com/ManishGantyala/btech-devops-labs`
