# webcrawl
Following is a general crawler that automatically creates an excel sheet and store information in a categorized way and which will needs only two values:

    Domain name
    Excel sheet file name

The crawler also downloads all the webpages to "webpages" folder.
The crawler grabs following information:

    domain name
    IP of the domain
    URL
    Title
    Headings & Sub Headings
    Email Addresses

Following things needs to be validated before running the programme:

    Script is written in Python 2.7.
    Execute the program in Linux to avoid downloading extra libraries.

It also generates a Pie chart based on number of links of each domain present.

Following libraries might be needing an installation:

    xlsxwriter (pip install xlsxwriter)
    urlparse  (pip install urlparse)
