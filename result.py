import random

result1 = 0
used = [(1,4),(1,5),(1,6)]
P = []
interval_sum = 0
for i in range(189):
    row = random.randint(1,32)
    column = random.randint(1,6)
    while((row,column) in used):
        row = random.randint(1,32)
        column = random.randint(1,6)
    used.append((row,column))
    column = int(abs(column - 3.5) + 0.5)
    #print(column)
    interval = 2 * (((row + 2) % 3) + 1)
    moving = (row + 0.43 * column)/(1.23 - 0.2 * (((row + 2) % 3) + 1))
    interval_sum += interval
    #print("P = {0}, interval = {1} , moving = {2}".format(interval_sum + interval + moving,interval,moving))
    P.append(interval_sum + interval + moving)

for i in P:
    if i > result1:
        result1 = i

print(result1)

result2 = 0
used = [(1,4),(1,5),(1,6)]
P = []
interval_sum = 0
for i in range(60):
    row = random.randint(23,32)
    column = random.randint(1,6)
    while((row,column) in used):
        row = random.randint(23,32)
        column = random.randint(1,6)
    used.append((row,column))
    column = int(abs(column - 3.5) + 0.5)
    #print(column)
    interval = 2 * (((row + 2) % 3) + 1)
    moving = (row + 0.43 * column)/(1.23 - 0.2 * (((row + 2) % 3) + 1))
    interval_sum += interval
    #print("P = {0}, interval = {1} , moving = {2},({3},{4})".format(interval_sum + interval + moving,interval,moving,row,column))
    P.append(interval_sum + interval + moving)
for i in range(66):
    row = random.randint(12,22)
    column = random.randint(1,6)
    while((row,column) in used):
        row = random.randint(12,22)
        column = random.randint(1,6)
    used.append((row,column))
    column = int(abs(column - 3.5) + 0.5)
    #print(column)
    interval = 2 * (((row + 2) % 3) + 1)
    moving = (row + 0.43 * column)/(1.23 - 0.2 * (((row + 2) % 3) + 1))
    interval_sum += interval
    #print("P = {0}, interval = {1} , moving = {2}".format(interval_sum + interval + moving,interval,moving))
    P.append(interval_sum + interval + moving)
for i in range(63):
    row = random.randint(1,11)
    column = random.randint(1,6)
    while((row,column) in used):
        row = random.randint(1,11)
        column = random.randint(1,6)
    used.append((row,column))
    column = int(abs(column - 3.5) + 0.5)
    #print(column)
    interval = 2 * (((row + 2) % 3) + 1)
    moving = (row + 0.43 * column)/(1.23 - 0.2 * (((row + 2) % 3) + 1))
    interval_sum += interval
    #print("P = {0}, interval = {1} , moving = {2}".format(interval_sum + interval + moving,interval,moving))
    P.append(interval_sum + interval + moving)
for i in P:
    if i > result2:
        result2 = i

print(result2)