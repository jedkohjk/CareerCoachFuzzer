from constants import *

counts = [0, 0, 0, 0]
# Keeps a count of the number of times each function each type has been found by searches
# For the generator to prioritise generating swarches for less-often found types

ACs = [AC(i+1) for i in range(6)]
# Tracks if each of the ACs passed
# 0 for not known; 1 for passed (so far); 2 for failed

AC2_tracker = [False] * 2
# Tracks if both cases (exceeding 50 and not exceeding 50) are accounted for

# Set up driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(MAX_WAIT)

# Log in
driver.get(SITE)
driver.find_element(By.XPATH, APPIAN_BUTTON).click()
driver.find_element(By.XPATH, USERNAME_FIELD).send_keys(USERNAME)
driver.find_element(By.XPATH, PASSWORD_FIELD).send_keys(PASSWORD)
driver.find_element(By.XPATH, LOGIN_BUTTON).click()
driver.find_element(By.XPATH, SEARCH_FIELD)

# From here, page loads will be dealt with explicitly
driver.implicitly_wait(0)

while True: # The generator can run infinitely long; this can be changed to a for loop too

    # query: what to search
    # expectation: an entry the query was generated from, which we may expect to see in our results
    # expect_type: the specific type from which we got the query
    # If we use records we know exist, we can test for AC1
    query, expectation, expect_type = generate(counts)
    
    # Search
    driver.find_element(By.XPATH, SEARCH_FIELD).send_keys(query)
    driver.find_element(By.XPATH, SEARCH_BUTTON).click()

    # Ensure that page is loaded
    for i in range(MAX_WAIT):
        AC5_lst = driver.find_elements(By.XPATH, AC5)
        tbl = driver.find_elements(By.XPATH, TABLE)
        if tbl:
            table_text = tbl[0].text.strip()
            if tbl[0].text != DEFAULT_TABLE or AC5_lst:
                search_success = True
                break
        sleep(1)
    else:
        search_success = False
        print('query: ' + query)
        print('Timeout when searching for query\n')

    if search_success:

        # The search bar automatically deletes some characters
        # I assume it is a feature, not a bug
        query = driver.find_element(By.XPATH, SEARCH_FIELD).get_attribute('value')

        # Test for AC5, disallowing searching of an empty string
        # The Google Docs had a full stop in the message for AC5 but the website did not
        # I chose to follow the website (this can be changed in constants.py)
        if not query:
            if not AC5_lst or AC5_lst[0].text != AC5_MSG:
                ACs[4].update(2)
                print('No error message for empty query\n')
            if table_text != DEFAULT_TABLE or len(driver.find_elements(By.XPATH, TABLE + '/tr[1]/td[5]')):
                ACs[4].update(2)
                print('Search conducted for empty query\n')
            ACs[4].update(1)
        elif AC5_lst and AC5_lst[0].text == AC5_MSG:
            ACs[4].update(2)
            print('query: ' + query)
            print('Unable to search with non-empty query')

        # The query was derived from an entry we saw in the data; there cannot be no records
        if table_text == NO_RECORDS:
            if expectation is not None:
                ACs[0].update(2)
                print('query: ' + query)
                print('Entry with matching ' + FIELD_ORDER[expect_type] + ' expected: ' + str(expectation))
                print('Not found\n')
            else:
                ACs[5].update(1)

        # Looks for the message that says there are more than 50 search records
        excesses = driver.find_elements(By.XPATH, EXCESS)
        has_excess = bool(excesses and excesses[0].text.strip() == EXCESS_MSG)

        # Beyond a certain number, the item count is reflected
        item_count = driver.find_elements(By.XPATH, ITEM_COUNT)
        if item_count:
            item_nums = get_num(item_count[0].text)
            total_items = item_nums[2]
        else:
            item_nums = []
            total_items = 0

        # Test for AC2
        if has_excess and (not item_nums or item_nums[2] != 50):
            ACs[1].update(2)
            print('query: ' + query)
            print('More than 50 search records but the records shown are not the first 50 records\n')

        if table_text!= DEFAULT_TABLE and table_text!= NO_RECORDS:
            
            previous_name = '' # Used to check that records are sorted by preferred name
            previous_item = 0 # Used to check the pagination is correct
            got_expect = expectation is not None # Used to check if the expectated entry was found
            found = [False] * 4 # Used for updating counts

            while True: # Loops until the last page

                # Gets entries
                entries = format_table(driver.find_element(By.XPATH, TABLE).text)
                if len(entries[-1]) != 4:
                    ACs[2].update(2)
                    print('query: ' + query)
                    print('Missing data in table\n')
                    break

                # Tests that the pagination is correct
                item_count = driver.find_elements(By.XPATH, ITEM_COUNT)
                if item_count:
                    item_nums = get_num(item_count[0].text)
                    if item_nums[0] != previous_item + 1:
                        ACs[1].update(2)
                        print('query: ' + query)
                        print('Index not aligned across pages\n')
                    if not item_nums[0] <= item_nums[1] <= item_nums[2]:
                        ACs[1].update(2)
                        print('query: ' + query)
                        print('Incorrect item numbers\n')
                    if item_nums[1] < item_nums[2] and item_nums[1] % 20:
                        ACs[1].update(2)
                        print('query: ' + query)
                        print('Number of items per page not 20\n')
                    if 1 + item_nums[1] - item_nums[0] != len(entries):
                        ACs[1].update(2)
                        print('query: ' + query)
                        print('Number of items in the table does not tally with the count')
                    if item_nums[2] != total_items:
                        ACs[1].update(2)
                        print('query: ' + query)
                        print('Total items inconsistent across pages\n')
                    previous_item = item_nums[1]
                else:
                    if total_items:
                        ACs[1].update(2)
                        print('query: ' + query)
                        print('Total items inconsistent across pages\n')
                    item_nums = []

                for entry in entries:

                    # Test for AC2
                    # Names must be in alphabetical order
                    if entry[0].upper() < previous_name.upper():
                        ACs[1].update(2)
                        print('query: ' + query)
                        print('Not sorted by name')
                        print('Name 1: ' + previous_name)
                        print('Name 2: ' + entry[0])
                        print()
                    previous_name = entry[0]

                    # Check if the entry was found correctly with AC1
                    # By observation:
                    # Searches are case insensitive
                    # For partial searches, the query is a substring of the entry
                    matched = [] # Tracks which were the potential columns matched (for updating counts)
                    for col, val in enumerate(entry):
                        if val != '-':
                            if col == 1:
                                if query == val:
                                    matched.append(col)
                            elif query.upper() in val.upper():
                                matched.append(col)
                        # Test for AC4, entries should not be blank, if they are, there should be a dash
                        if not val:
                            ACs[3].update(2)
                            print('query: ' + query)
                            print('Blank in entry for ' + FIELD_ORDER[col] + ': ' + str(entry))
                        if val == '-':
                            ACs[3].update(1)
                    
                    # Checks if this is the expected entry from which the query was generated
                    if expectation is not None and entry == expectation:
                        got_expect = False

                    # Test for AC1
                    # If the query matches none of the columns in the entry, it should not have been returned
                    if not matched:
                        ACs[0].update(2)
                        print('query: ' + query)
                        print('Irrelevant entry: ' + str(entry))

                    # If there was only one match, it was definitely responsible for the entry being turned up by the search
                    # The search function for that type worked; increment counts for that type
                    if len(matched) == 1:
                        found[matched[0]] = True

                    # Feed entries to the generator to generate from
                    # Since we want diversity in our generator, do not take entries if:
                    # a) The query itself was generated from existing entries
                    # b) The column matched the query
                    if expectation is None:
                        for i in range(4):
                            if i not in matched:
                                if savers[i].add(entry[i], entry):
                                    break

                # Find the button for the next page, if it exists
                next_lst = driver.find_elements(By.XPATH, NEXT_PAGE)

                # Exit the loop if no next page exists
                if not next_lst or next_lst[0].get_attribute('aria-disabled') == 'true':
                    # The item numbers indicate that there should be a next page, but there is no button to it
                    if item_nums and item_nums[1] != item_nums[2]:
                        ACs[1].update(2)
                        print('query: ' + query)
                        print('Inaccurate item count reflected\n')
                    break

                # There is a next page, but the item numbers do not reflect it
                if not item_nums or item_nums[1] == item_nums[2]:
                    ACs[1].update(2)
                    print('query: ' + query)
                    print('Inaccurate item count reflected\n')

                # Go to the next page
                next_lst[0].click()
                #Ensure the page loads
                for i in range(MAX_WAIT):
                    item_count = driver.find_elements(By.XPATH, ITEM_COUNT)
                    if item_count and get_num(item_count[0].text) != item_nums:
                        break
                    sleep(1)
                else:
                    # Use a different method (table) to check that the page is loaded
                    tbl = driver.find_elements(By.XPATH, TABLE)
                    if tbl and format_table(tbl[0].text) != entries:
                        print('query: ' + query)
                        print('Inaccurate item count reflected\n')
                    else:
                        print('query: ' + query)
                        print('Timeout when moving to next page\n')
                        break

            # Test for AC1
            # If the expected value was not found, the result can be still correct if there were more than 50 entries and it was not included in the top 50
            # Since the items are listed by name, we check to see if it should have been in the top 50 names, if there were indeed more than 50 entries
            if got_expect and (not has_excess or expectation[0].upper() < previous_name.upper()):
                ACs[0].update(2)
                print('query: ' + query)
                print('Entry with matching ' + FIELD_ORDER[expect_type] + ' expected: ' + str(expectation))
                print('Not found\n')

            # Update counts
            for col, val in enumerate(found):
                if val:
                    counts[col] += 1

            if all(counts):
                ACs[0].update(1)

            AC2_tracker[has_excess] = True
            if all(AC2_tracker):
                ACs[1].update(1)

            ACs[2].update(1)

    # Reset page so that the check that the search is loaded will work
    driver.refresh()
    # Ensure that refresh is loaded
    for i in range(MAX_WAIT):
        tbl = driver.find_elements(By.XPATH, TABLE)
        if tbl and tbl[0].text == DEFAULT_TABLE and not driver.find_elements(By.XPATH, AC5):
            break
        sleep(1)
    else:
        print('query: ' + query)
        print('Timeout when refreshing page')
        print('Exiting program')
        break
