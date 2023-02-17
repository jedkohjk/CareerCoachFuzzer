from .shared import *

# Creates new test cases

def make_ic() -> str:
##    if int(random()*2):
##        first = 'ST'[int(random()*2)]
##        last = 'JZIHGFEDCBA'
##    else:
##        first = 'FG'[int(random()*2)]
##        last = 'XWUTRQPNMLK'
##    weights = (2, 7, 6, 5, 4, 3, 2)
##    nums = [int(random()*10) for i in range(7)]
##    return first + "".join(str(i) for i in nums) + last[sum(weights[i]*nums[i] for i in range(7))%11]

    # I tried generating based on the NRIC checksum used in Singapore at first
    # But it appears that many entries on the site do not follow the checksum rules, so I used this simple version instead
    return 'STFG'[int(random()*4)] + "".join(str(int(random()*10)) for i in range(7)) + chr(65+int(random()*26))

# Makes a random string made of characters from chrs
# Ratio should be between 0 and 1; the higher the ratio the longer the string is likely to be
def make_str(chrs: list, ratio: float) -> str:
    add = 1
    op = []
    while random() < add:
        op.append(chrs[int(random()*len(chrs))])
        add *= ratio
    return ''.join(op)

def make_name() -> str:
    return make_str([chr(i) for i in range(32, 127)], 0.984375).strip()

def make_number() -> str:
    return make_str([str(i) for i in range(10)], 0.875)

def make_email() -> str:
    # Assumes the emails are only made of characters as described in the local and domain assignments
    def make_portion(chrs) -> str:
        add = 1
        op = []
        while random() < add:
            op.append(make_str(chrs, 0.9375))
            add *= 0.9375
        return '.'.join(op)
    local = make_portion([chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + [str(i) for i in range(10)] + [i for i in "!#$%&'*+-/=?^_`{|}~"])
    domain = make_portion([chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + [str(i) for i in range(10)] + ['-'])
    return random_slice(local + '@' + domain)
