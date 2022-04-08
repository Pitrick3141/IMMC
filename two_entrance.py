import random
import openpyxl

output = [["interval_sum","interval","time_row","time_column","coordinate"]]
def write_excel_xlsx(path, sheet_name, value):
    index = len(value)
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = sheet_name
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.cell(row=i+1, column=j+1, value=str(value[i][j]))
    workbook.save(path)
def interval(row,lane):
    return (0.75 + 0.25 * lane) * (((row + 2) % 3) + 1)
def moving_in_row(row):
    return row / (1.23 - 0.2 * (((row + 2) % 3) + 1))
def moving_in_column(row,column,people_in_way):
    return int(abs(column - 3.5) + 0.5) * 0.43 * (people_in_way + 3) / (1.23 - 0.2 * (((row + 2) % 3) + 1))
def column_dis(column):
    return int(abs(column - 3.5) + 0.5)

def method1():
    result1 = 0
    used = []
    P = [[],[]]
    interval_sum = [0,0]
    for i in range(105):
        row = random.randint(1,21)
        column = random.randint(1,5)
        while((row,column) in used):
            row = random.randint(1,21)
            column = random.randint(1,5)
        used.append((row,column))  
        people_in_way = 0
        if(column > 2):
            for col in range(3,column):
                if((row,col) in used):
                    people_in_way += 1
        else:
            for col in range(2,column,-1):
                if((row,col) in used):
                    people_in_way += 1
        #print("interval = {0}, time_row = {1}, time_column = {2}, time_total = {3} ({4},{5})".format(interval(row),moving_in_row(row),moving_in_column(row,column,people_in_way),interval(row) + moving_in_row(row) + moving_in_column(row,column,people_in_way),row,column))
        P[1].append(interval_sum[1] + interval(row,1) + moving_in_row(row) + moving_in_column(row,column,people_in_way))
        #print("({0},{1}) interval_sum = {2}, interval = {3}, time_r = {4}, time_c = {5}, in lane {6}".format(row,column,interval_sum[lane],interval(row,lane),moving_in_row(row),moving_in_column(row,((column + 5)%6)+1,people_in_way),lane))
        #output.append([interval_sum,interval(row),round(moving_in_row(row),2),round(moving_in_column(row,column,people_in_way),2),(row,column)])
        interval_sum[1] += interval(row,1)
    for i in P[1]:
        if i > result1:
            result1 = i
    #print(result1)
    
    #write_excel_xlsx("output.xlsx", "sheet1", output)
    return result1
#Random method

def method2():
#Section method
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
        
        people_in_way = 0
        if(column > 3):
            for col in range(4,column):
                if((row,col) in used):
                    people_in_way += 1
        else:
            for col in range(3,column,-1):
                if((row,col) in used):
                    people_in_way += 1
        P.append(interval_sum + interval(row) + moving_in_row(row) + moving_in_column(row,column,people_in_way))
        #output.append([interval_sum,interval(row),round(moving_in_row(row),2),round(moving_in_column(row,column,people_in_way),2),(row,column)])
        interval_sum += interval(row)
    for i in range(66):
        row = random.randint(12,22)
        column = random.randint(1,6)
        while((row,column) in used):
            row = random.randint(12,22)
            column = random.randint(1,6)
        used.append((row,column))
        
        people_in_way = 0
        if(column > 3):
            for col in range(4,column):
                if((row,col) in used):
                    people_in_way += 1
        else:
            for col in range(3,column,-1):
                if((row,col) in used):
                    people_in_way += 1
        P.append(interval_sum + interval(row) + moving_in_row(row) + moving_in_column(row,column,people_in_way))
        #output.append([interval_sum,interval(row),round(moving_in_row(row),2),round(moving_in_column(row,column,people_in_way),2),(row,column)])
        interval_sum += interval(row)
    for i in range(63):
        row = random.randint(1,11)
        column = random.randint(1,6)
        while((row,column) in used):
            row = random.randint(1,11)
            column = random.randint(1,6)
        used.append((row,column))
        
        people_in_way = 0
        if(column > 3):
            for col in range(4,column):
                if((row,col) in used):
                    people_in_way += 1
        else:
            for col in range(3,column,-1):
                if((row,col) in used):
                    people_in_way += 1
        P.append(interval_sum + interval(row) + moving_in_row(row) + moving_in_column(row,column,people_in_way))
        #output.append([interval_sum,interval(row),round(moving_in_row(row),2),round(moving_in_column(row,column,people_in_way),2),(row,column)])
        interval_sum += interval(row)
    for i in P:
        if i > result2:
            result2 = i
    #print(result2)
    #write_excel_xlsx("output.xlsx", "sheet2", output)
    return result2

def method3():
    #Seat method
    result3 = 0
    used = [(1,4),(1,5),(1,6)]
    P = []
    interval_sum = 0
    row = 32
    for i in range(189):
        if(i % 2 == 0):
            column = int(6 - (i % 6) / 2)
        else:
            column = int(((i % 6) + 1) / 2)
        if(row == 1):
            column = (i % 6) + 1
        #print((row,column))
        used.append((row,column))
        
        people_in_way = 0
        if(column > 3):
            for col in range(4,column):
                if((row,col) in used):
                    people_in_way += 1
        else:
            for col in range(3,column,-1):
                if((row,col) in used):
                    people_in_way += 1
        P.append(interval_sum + interval(row) + moving_in_row(row) + moving_in_column(row,column,people_in_way))
        #output.append([interval_sum,interval(row),round(moving_in_row(row),2),round(moving_in_column(row,column,people_in_way),2),(row,column)])
        interval_sum += interval(row)
        #print(people_in_way)
        if(column == 3 and row > 1):
            row -= 1

    for i in P:
        if i > result3:
            result3 = i

    #print(result3)
    #write_excel_xlsx("output.xlsx", "sheet3", output)
    return result3

'''
total_result = [0,0,0]
num = 30
for i in range(num):
    total_result[0] += method1()
    total_result[1] += method2()
    total_result[2] += method3()
print("Random method using {0} seconds".format(total_result[0] / num))
print("Section method using {0} seconds".format(total_result[1] / num))
print("Seat method using {0} seconds".format(total_result[2] / num))
'''
for i in range(100):
    output.append([round(method1(),2)])
write_excel_xlsx("output.xlsx", "sheet1", output)

