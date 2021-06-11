import xlrd

workbook = xlrd.open_workbook("Tests.xlsx")
sheet = workbook.sheet_by_index(0)

def get_cell_range(start_col, start_row, end_col, end_row):
    return [sheet.row_slice(row, start_colx=start_col, end_colx=end_col+1) for row in xrange(start_row, end_row+1)]

data = get_cell_range(0, 0, 4, 9)   # A3 to D7
print(data)