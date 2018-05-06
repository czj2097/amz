import xlrd
import xlwt
from xlutils.copy import copy

wbk = xlwt.Workbook()
sheet_0 = wbk.add_sheet('Index')
sheet_1 = wbk.add_sheet('ErrorASIN')
sheet_2 = wbk.add_sheet('AllASIN')
wbk.save("ProductDetails.xls")

wbk_rd = xlrd.open_workbook("CategoryID.xls")
sheet_rd = wbk_rd.sheet_by_name('CategoryID')
index_end = sheet_rd.nrows
wbk_wt = copy(wbk_rd)
sheet_wt = wbk_wt.get_sheet('CategoryID')
sheet_wt.write(0,1,0)
sheet_wt.write(1,1,index_end)
sheet_wt.write(2,1,0)
sheet_wt.write(3,1,0)
wbk_wt.add_sheet('ErrorCategory')
wbk_wt.save("CategoryID.xls")
