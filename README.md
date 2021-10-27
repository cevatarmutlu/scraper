## Introduction

This project is a simple scrapper.

## Install

To python side:

    pip3 install -r requirenments.txt

To google sheet operations: 

Meet the requirements in the `Prerequisites` section.: [link](https://developers.google.com/sheets/api/quickstart/python#prerequisites)

move `json` file to root directory of this project as `credentials.json`

## Used tech-stack

Tech | What used for
---- | -------------
Pandas | To read excel file and extract URL list.
BeautifulSoup | To scrape required values from the urls.
Google Sheets API | To create sheet from scraped values
Google Apps Script | Sorting and Sending data with an Email

## Description of the challenges

i was know BeautifulSoup and Selenium modules, so to scrape what should i use i was know. I decide to use BeautifulSoup. What I would say as a challenge is to get the required values from the pages.

I was not know to createing google spreadsheet with API. This part of project was challange for me. Firstly i read google document so fastly and i was unsuccessful to create sheet. Then i was calmdown myself and i read document slowly. I was succesfull to create sheet in my gmail account.

I wasn't know that thing Google Apps Script. This was challange for me again. I read the document and open Script editor from Sheet UI. I searched `google app script sort sheet` in google and what i find is `sort` function. Sort function solved the first problem. Second problem is send mail with attachment. For this i searched `google app script send email with attachment` in Google and what i find is to access the sheet file use Drive. I use `DriveApp` to get sheet file. For send mail i use MailApp.

## What did i learn from this project?

use Google app script and Google Sheet API.

## Additional questions

### 1. If I’d have 10.000 urls that I should visit, then it takes hours to finish. What can we make to fasten this process?

Parallelism. For example, the file can be split into parts and each part can be run by a thread.

### 2. What can we make or use to automate this process to run once a day? Write your recommendations.

Crontab or Airflow.

Crontab kullanmadım fakat yazdığımız script' i günde bir kez çalıştırabiliriz.

Airflow creates flows. Flow is a combination of tasks. We can run this project in airflow by dividing it into tasks.

### 3. Please briefly explain what an API is and how it works.

API provides communication between two systems. It uses HTTP requests. For example, when a user registers on the frontend, it sends this information on the backend. In this way, the user is registered in the database.