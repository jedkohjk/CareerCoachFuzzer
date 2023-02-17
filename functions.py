# Functions used in main

# Finds the From, To and Total entries based on the string
def get_num(string: str) -> tuple:
    if string[:5] == 'Items':
        return [int(i) for i in string.split('\n')[-1].split() if i.isnumeric()]
    return [1] + ([int(string[:string.find(' ')])] * 2)

# Puts the entries in a table format with each entry as a row
def format_table(string: str) -> list:
    op = []
    for i, j in enumerate(string.split('\n')):
        if not i%4:
            op.append([])
        op[-1].append(j)
    return op

class AC:

    def __init__(self, num):
        self.num = num
        self.state = 0
        # 0 for unknown; 1 for passed; 2 for failed

    def update(self, n):
        if n > self.state:
            self.state = n
            if n == 1:
                print('AC' + str(self.num) + ' passed so far\n')
            else:
                print('AC' + str(self.num) + ' failed\n')
