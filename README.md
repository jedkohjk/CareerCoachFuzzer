# Career Coach Fuzzer
A fuzzer for search queries on the Career Coach site.  
This was tested on a Windows laptop.
## Pre-requisites
* Have Google Chrome installed
* Have Python 3 installed
* Have the selenium library for Python installed
* Have the webdriver-manager library for Python installed

To install the relevant libraries for Python on Windows using pip, type the following in the command line:
```bash
pip3 install selenium
pip3 install webdriver-manager
```
## Run
Ensure you have a stable internet connection.  
Download the files and run main.py.  
To stop the execution, hold Ctrl + C.
## Interpretation of Results
The results will be printed to stdout.  

Results may be in the format 'AC_ passed so far' or 'AC_ failed'. These refer to the acceptance criteria described in the assessment documents. We cannot be entirely sure that the code works, only that it works from the limited amount we have seen. Hence, 'AC_ passed so far' is printed when we have sufficient reason to believe that the code fulfils a given criterion. However, after further testing, it may be updated to 'AC_ failed'.  

For cases that fail within expectation, the query that caused the failure will be printed, followed by a short explanation.  

However, if the query produces an error (like error 403), the program will print the query and exit.
## Assumptions & Interpretations
* 'Alphabetical order' for sorting names is interpreted as ASCII order. Lower-case letters are treated as equivalent to upper-case letters (using the ASCII values of the upper-case letters).
* It is assumed that no one is named -.
* Exact searches are assumed to be case insensitive.
* Partial searches are interpreted to be case-insensitive searches where the query is a continuous substring of the result.
* NRICs need not follow the checksum used in Singapore (many entries did not), and phone numbers may not be from Singapore (so there isn't a fixed format). However, phone numbers are strictly numerical.
* The local part of email addresses only contain numbers, upper- or lower-case letters, and any of the following characters !#$%&'*+-/=?^_`{|}~. Dots cannot appear consecutively.
* The domain of an email can only contain numbers, upper- or lower-letters, hyphens, and dots. Dots cannot appear consecutively.
* The search bar automatically removes non-printable characters, and lone spaces. It is assumed that this is a feature, not a bug.
* The code locates the web elements by XPath. It is assumed that the XPaths will not change.
* The default page (before search is performed) is assumed to always show the message 'No items available'.
* It is assumed that pages will not take more than 20 seconds to load. (The maximum waiting time for a page can be adjusted in constants.py if pages take more than 20 seconds to load on your machine.)
* The program only works if the service is available (no error 503), the server is not under maintenance, and it is allowed to log in (for there is a limit to the number of concurrent logins).
## Findings
* The message in the assessment document for AC5 is 'Please provide at least one input to start searching.', with a full-stop, but the message on the website is 'Please provide at least one input to start searching', without a full-stop. I assumed this was intentional and updated the code to reflect not having a full-stop.
* The following query causes an access denied error: `8+E#U@
* The page fails the AC 2 criteria that it should be sorted in alphabetical order. The entry ['Trim Client profile', 'S5610485B', '98578197', '-'] appears before entries starting with the letter 'A' with the following queries:
  * c
  * i
  * R
  * 1
  * 8
  * 57
  * 98
* Not a bug but the entry ['Test Sanitisating !"#$%&'()*+,-./:;@^P', 'S5443476F', '-', '-'] was found with the following query: "
* The rest of the acceptance criteria outlined in the document passed 
## Future Improvements
* The fuzzer should aim to maximise grammar coverage. Currently inputs generated do not account for previous queries.
* For the most part, all valid characters are equally likely to be in the string generated by the fuzzer. This does not reflect the nature of the data stored.
