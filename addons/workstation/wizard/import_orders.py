# -*- coding: utf-8 -*-
from odoo import api, fields, models
import xlrd
import base64
from odoo.exceptions import UserError,ValidationError


XL_CELL_EMPTY = 0
XL_CELL_TEXT = 1
XL_CELL_NUMBER = 2
XL_CELL_DATE = 3
XL_CELL_BOOLEAN = 4
XL_CELL_ERROR = 5
XL_CELL_BLANK = 6

class click_to_import_orders(models.Model):
    _name = 'click_to_import.orders'

    excel_file = fields.Binary(string=u"上傳EXCEL檔案")

    def button_import(self):
        if not self.excel_file:
            raise UserError(u"檔案錯誤,沒有上傳正確的Excel File")

        xls = xlrd.open_workbook(file_contents=base64.decodebytes(self.excel_file))
        # sheet = xls.sheet_by_index(0)
        sheet = xls.sheets()[1] #可選Sheet

        order_rec = self.env['sale.order']
        order_chec = self.env['sale.order'].search([])
        all_order_name = []
        xname=''
        xquotation_price=''
        xman_name=''
        man_name_check = ''


        for r in order_chec:    #撈出所有產品名
            if r.name :
                all_order_name.append(r.name)

        for row in range(1, 3):

            cell = sheet.cell(row, 0)  # 貨號
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xname = u'' + str(cell.value)
                product_name_check = self.env['product.template'].search([('name', '=', xname)])

            cell = sheet.cell(row, 2)  # 牌價
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xquotation_price = u'' + str((cell.value))

            cell = sheet.cell(row, 4)  # 收件人
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xman_name = u'' + str(cell.value)
                man_name_check = self.env['res.partner'].search([('name', '=', xman_name)])


            if xname not in all_order_name:
                r = []
                r.append([0, 0, {
                    'price_unit': xquotation_price,
                    'product_id':product_name_check.id

                }])

                print(xname)
                print(xman_name)
                print(man_name_check.id)
                print(r)

                product_data = order_rec.create({
                    'partner_id': man_name_check.id,
                    'order_line':r})

