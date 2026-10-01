# string = 'H ello'
# for i in string:
#     print(i)
# print(f"string[0], ({string[0]}), string[1], ({string[1]})")
table =[]
row1 = ['$ TIME = Range time', ' reference to nearest integer second before IU']
row2 = ['$     umbilical disconnect']
row3 = ['$     site to the subvehicle point']
row4 =['$']
row5 = ['sucess']
table.append(row1)
table.append(row2)
table.append(row3)
table.append(row4)
table.append(row5)
print(table)
# for row in table:
#     print(row)

# for row in table:
#    for i, entry in enumerate(row):
#        print(f"{i}. string[0], ({entry[0]}), string[1], ({entry[1]}), string[2], ({entry[2]}), string[3], ({entry[3]})")

table = [row for row in table if all(entry[0] != "$" for entry in row)]
print(table)