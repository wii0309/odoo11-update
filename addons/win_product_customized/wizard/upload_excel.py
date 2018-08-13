# -*- coding: utf-8 -*-
from odoo import api, fields, models

from os import listdir
import base64
import imghdr
from odoo.exceptions import UserError,ValidationError
import os
import glob
import xlrd
import datetime;
import random;

XL_CELL_EMPTY = 0
XL_CELL_TEXT = 1
XL_CELL_NUMBER = 2
XL_CELL_DATE = 3
XL_CELL_BOOLEAN = 4
XL_CELL_ERROR = 5
XL_CELL_BLANK = 6


class Upload_excel(models.TransientModel):
    _name = 'upload.excel'

    excel_file = fields.Binary(string=u"上傳EXCEL檔案")
    upload_sequence=fields.Char(string='上傳批次號')
    delete_sequence=fields.Char(string='欲刪除批次號')




    def partner_action_import(self):
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        randomNum = random.randint(0, 100)
        if randomNum <= 10:
            randomNum = str(0) + str(randomNum)
        uniqueNum = str(nowTime) + str(randomNum)

        upload_sequence = uniqueNum

        if not self.excel_file:
            raise UserError(u"檔案錯誤,沒有上傳正確的Excel File")

        xls = xlrd.open_workbook(file_contents=base64.decodebytes(self.excel_file))
        sheet = xls.sheet_by_index(0)

        self.ensure_one()
        product_rec = self.env['product.template']

        for row in range(1, sheet.nrows):
            same_check=''
            cell = sheet.cell(row, 0) #貨組代號
            xname = 0
            if cell.ctype == XL_CELL_EMPTY:
                continue
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xname = u'' + str(cell.value)
                same_check = self.env['product.template'].search([('name', '=', xname)]) #做重複檔名的排除

            if not same_check:
                cell = sheet.cell(row, 2) #廠商
                xmajor_manufactor = '-'
                if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                    xmajor_manufactor = u'' + str((cell.value))

                cell = sheet.cell(row, 22) #牌價
                if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                    xquotation_price = u'' + str((cell.value))
                else:
                    xquotation_price = 0

                cell = sheet.cell(row, 3)  # 品牌系列
                if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                    xbrand_type= u'' + str((cell.value))
                else:
                    xbrand_type= 0

                cell = sheet.cell(row, 4)  #品牌
                if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                    xbrand = u'' + str((cell.value))
                else:
                    xbrand = 0

                cell = sheet.cell(row, 5)  #品別
                if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                    xcategory = u'' + str((cell.value))
                else:
                    xcategory = 0

                cell = sheet.cell(row,7 )  #年季
                if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                    xyear_season = u'' + str((cell.value))
                else:
                    xyear_season = 0

                cell = sheet.cell(row,8 )  #設計師
                if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                    xman_type = u'' + str((cell.value))
                else:
                    xman_type = 0

                cell = sheet.cell(row, 9)  # 小類
                if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                    xsml_type = u'' + str((cell.value))
                else:
                    xsml_type = 0

                cell = sheet.cell(row,10 )  #中類
                if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                    xmid_type = u'' + str((cell.value))
                else:
                    xmid_type = 0

                cell = sheet.cell(row, 11)  #大類
                if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                    xbig_type = u'' + str((cell.value))
                else:
                    xbig_type = 0

                cell = sheet.cell(row, 19)  # 尺寸
                if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                    xsize = u'' + str((cell.value))
                else:
                    xsize = 0

                cell = sheet.cell(row, 18) #顏色
                xcolor_name = '-'
                if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                    xcolor_name = u'' + str((cell.value))


                cell = sheet.cell(row, 6)  #品名
                if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                    xproduct_class = u'' + str((cell.value))
                else:
                    xproduct_class = 0

                #以下是做判斷屬性是否存在，若無，可自動新增每一個

                # brand_check = self.env['brand.info'].search([('name', '=', xbrand)])
                #
                # if not brand_check:
                #     brand_check = self.env['brand.info'].create({'name': xbrand})
                #
                # brand_type_check = self.env['brand.type'].search([('name', '=', xbrand_type)])
                #
                # if not brand_type_check:
                #     brand_type_check = self.env['brand.type'].create({'name': xbrand_type})
                #
                # year_season_check = self.env['year.season'].search([('name', '=', xyear_season)])
                #
                # if not year_season_check:
                #     year_season_check = self.env['year.season'].create({'name': xyear_season})
                #
                # category_check = self.env['category.name'].search([('name', '=', xcategory)])
                #
                # if not category_check:
                #     category_check = self.env['category.name'].create({'name': xcategory})
                #
                # man_type_check = self.env['man.type'].search([('name', '=', xman_type)])
                #
                # if not man_type_check:
                #     man_type_check = self.env['man.type'].create({'name': xman_type})
                #
                # big_type_check = self.env['big.type'].search([('name', '=', xbig_type)])
                #
                # if not big_type_check:
                #     big_type_check = self.env['big.type'].create({'name': xbig_type})
                #
                # mid_type_check = self.env['mid.type'].search([('name', '=', xmid_type)])
                #
                # if not mid_type_check:
                #     mid_type_check = self.env['mid.type'].create({'name': xmid_type})
                #
                # sml_type_check = self.env['sml.type'].search([('name', '=', xsml_type)])
                #
                # if not sml_type_check:
                #     sml_type_check = self.env['sml.type'].create({'name': xsml_type})
                #
                # mm_check=self.env['res.partner'].search([('name','=',xmajor_manufactor)])
                #
                # if not mm_check:
                #     mm_check=self.env['res.partner'].create({'name': xmajor_manufactor})

                color_str = xcolor_name.split(',')
                color_r=[]
                for color_num in color_str:
                    color_check=self.env['color.table'].search([('color_num','=',color_num)])
                    if color_check:
                        color_r.append([4,color_check.id])
                    if not color_check:
                        raise ValidationError(u'錯誤！第%s列的色號:%s，未建立色號及顏色' (row,color_num))

                size_str = xsize.split(',')
                size_r=[]
                for size_type in size_str:
                    size_check = self.env['size.table'].search([('size_type', '=', size_type)])
                    if size_check:
                        size_r.append([4,size_check.id])
                    else:
                        raise ValidationError(u'錯誤！第%s列的尺寸:%s，未建立' % (row, size_type))


                # product_class_check = self.env['product.class'].search([('name', '=', xproduct_class)])
                #
                # if not product_class_check:
                #     product_class_check = self.env['product.class'].create({'name': xproduct_class})

                #開始做產品
                product_data = product_rec.create({
                    'name': xname,
                    # 'major_manufactor': mm_check.id,
                    # 'brand_type': brand_type_check.id,
                    # 'brand': brand_check.id,
                    # 'category': category_check.id,
                    # 'year_season': year_season_check.id,
                    # 'man_type': man_type_check.id,
                    # 'sml_type': sml_type_check.id,
                    # 'mid_type': mid_type_check.id,
                    # 'big_type': big_type_check.id,
                    'size': size_r,
                    # 'product_class': product_class_check.id,
                    'quotation_price': xquotation_price,
                    'color_name':color_r,
                    'upload_no':upload_sequence})
                self.click_to_add_attribute(product_data)


    def click_to_add_attribute(self, line):
        for color_number in line.color_name:
            r = []
            if not line.attribute_line_ids:
                r.append([0, 0, {
                    'attribute_id': 1,
                    'value_ids': [(4, color_number.product_attribute_id.id)]
                }])
                line.update({
                    'attribute_line_ids': r
                })
            elif line.attribute_line_ids:
                for records in line.attribute_line_ids:
                    if records.attribute_id.id == 1:
                        records.write({
                            'value_ids':[(4,color_number.product_attribute_id.id)]
                        })
            line.create_variant_ids()
        for size_type in line.size:
            r = []
            for records in line.attribute_line_ids:
                if len(line.attribute_line_ids.mapped('attribute_id')) == 1 and records.attribute_id.id != 2:
                    r.append([0, 0, {
                        'attribute_id': 2,
                        'value_ids': [(4, size_type.product_attribute_id.id)]
                    }])
                    line.update({
                        'attribute_line_ids': r
                    })
                elif records.attribute_id.id == 2:
                    records.write({
                        'value_ids':[(4,size_type.product_attribute_id.id)]
                    })
            line.create_variant_ids()
        return True

    # def override_main_image(self):








    @api.multi
    def delete_by_upload_no(self):
        if  self.env["product.template"].search([('upload_no', '=', self.delete_sequence)]):
            self.env["product.template"].search([('upload_no', '=', self.delete_sequence)]).unlink()
        else:
            raise ValidationError(u"查無此批次號，請重新輸入")

