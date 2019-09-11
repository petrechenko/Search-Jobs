from flask import Flask, abort, redirect, render_template, request
import urllib.request
from bs4 import BeautifulSoup
import re

# You could change the information here you want to search, or if you want
# not to use some of it, you can delete it from the webUrl below
# if the job name is 2 words - use +
job = 'jr+developer'
location = 'Seattle'
fullTime = 'fulltime'
experience = 'entry_level'

# List of words to avoid
redFlags = ["senior", "intern", "revature"]


def checkRedFlags(title):
    for word in redFlags:
        if word in title:
            return False
    return True


# Configure application
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    titles = []
    # while loop finds all the results, not only from the first page
    pageNum = 0
    while pageNum < 100:
        page = str(pageNum)

        # if you don't want some dependencies in search-delete them
        webUrl = urllib.request.urlopen(
            'https://www.indeed.com/jobs?q='+job+'&l='+location+'&jt='+fullTime+'&explvl='+experience+'&start='+page)
        data = webUrl.read()
        soup = BeautifulSoup(data, 'html.parser')

        # Error check
        if soup.find(class_='bad_query'):
            titles.append(
                ["The search didn't match any jobs or the URL is not correct"])

        for i in soup.find_all(class_='result'):
            link = i.find(class_='turnstileLink')

            # Find a title
            title = link.get('title')

            # Check for redFlaged words
            lowerTitle = title.lower()
            if not checkRedFlags(lowerTitle):
                continue

            # Find a link
            href = link.get('href')
            site = "http://indeed.com"+href

            town = i.find(class_='location').text

            company = i.find(class_='company').text
            lowerCompany = company.lower()
            if not checkRedFlags(lowerCompany):
                continue

            summary = i.find(class_='summary').text

            # Create a separate list to show all the information
            val = []
            val.append(str(title))
            val.append(str(site))
            val.append(str(town))
            val.append(str(company))
            val.append(str(summary))

            # Add a local list to the general list
            titles.append(val)
        pageNum += 10
    return render_template("index.html", titles=titles)


if __name__ == '__main__':
    app.run()
