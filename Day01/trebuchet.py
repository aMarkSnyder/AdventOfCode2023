# Star 1
line_digits = []
with open('input.txt','r') as input:
    for line in input:
        digits = []
        for char in line:
            if char.isdigit():
                digits.append(char)
        line_digits.append(digits)

cal_vals = []
for digits in line_digits:
    cal_vals.append(int(digits[0]+digits[-1]))

print(sum(cal_vals))

# Star 2
digit_strings = ['zero','one','two','three','four','five','six','seven','eight','nine']

line_digits = []
with open('input.txt','r') as input:
    for line in input:
        digits = []
        for idx in range(len(line)):
            if line[idx].isdigit():
                digits.append(int(line[idx]))
            else:
                for digit, text in enumerate(digit_strings):
                    if line[idx:].startswith(text):
                        digits.append(digit)
        line_digits.append(digits)

cal_vals = []
for digits in line_digits:
    cal_vals.append(10*digits[0]+digits[-1])

print(sum(cal_vals))