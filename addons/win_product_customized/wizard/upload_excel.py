# -*- coding: utf-8 -*-
from odoo import api, fields, models
import xlrd
import datetime
import random
from os import listdir
import base64
import imghdr
from odoo.exceptions import UserError,ValidationError
import os
import glob

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

        upload_sequence = uniqueNum #批次上傳碼產生

        if not self.excel_file:
            raise UserError(u"檔案錯誤,沒有上傳正確的Excel File")

        xls = xlrd.open_workbook(file_contents=base64.decodebytes(self.excel_file))
        sheet = xls.sheet_by_index(0)

        self.ensure_one()
        product_rec = self.env['product.template']
        # for row in range(1, sheet.nrows):
        xname = ''
        size_r = []
        color_r = []
        for row in range(1, 5):
            # cell = sheet.cell(row, 0)  #貨源
            # if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
            #     xmajor_manufactor = u'' + str((cell.value))
            #     major_manufactor_ser=self.env['res.partner'].search([('name', '=', xmajor_manufactor)])

            cell = sheet.cell(row, 0)  # 貨號
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xname = u'' + str((cell.value))
                print(xname)

            cell = sheet.cell(row, 1)  # 色號
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xcolor = u'' + str((cell.value))
                color_str = xcolor.split(',')
                color_r = []
                for color_num in color_str:
                    color_ser = self.env['color.table'].search([('color_num', '=', color_num.rstrip('.0'))])
                    if color_ser:
                        color_r.append([4,color_ser.id])
                    else:
                        raise ValidationError(u'錯誤！第%s列的顏色  :%s，未建立' % (row, color_num))

            cell = sheet.cell(row, 2)  # 尺寸
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xsize = u'' + str((cell.value))
                size_str = xsize.split(',')
                size_r = []
                for size_type in size_str:
                    size_check = self.env['size.table'].search([('size_type', '=', size_type)])
                    if size_check:
                        size_r.append([4,size_check.id])
                    else:
                        raise ValidationError(u'錯誤！第%s列的尺寸:%s，未建立' % (row, size_type))
            print(size_r)
            print(color_r)
            product_data = product_rec.create({
                'name': xname,
                # 'major_manufactor': major_manufactor_ser.id,
                'size': size_r,
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

    def batch_upload(self):
        mypath = "C:/test_upload_pic"
        files = listdir(mypath)
        tmp = []
        for f in files:
            if imghdr.what(mypath + '/' + f):
                str = f.split("_")
                if str[0] not in tmp:
                    tmp.append(str[0])

        for product_code in tmp:
            product_id = self.env['product.template'].search([('name', '=', product_code)])
            if product_id:
                for fullpath in glob.glob(mypath + '/' + product_id.name + '_*'):
                    image_type = imghdr.what(fullpath)
                    strs = fullpath.split("_")
                    if image_type:
                        with open(fullpath, "rb") as imageFile:
                            image = base64.b64encode(imageFile.read())
                            filename = os.path.basename(fullpath).split(".")[0]
                            existed = self.env['product.image'].search([('name', '=', filename)])
                            strs_check = strs[0]
                            filename_check = filename.split("_")[0]  # 看產品名
                            filename_check2 = filename.split("_")[1]  # 看編號
                            print(filename_check2)
                            if filename_check2 != '1':
                                if existed:
                                    existed.write({
                                        'image': image
                                    })
                                else:
                                    self.env['product.image'].create({
                                        'image': image,
                                        'name': filename,
                                        'product_tmpl_id': product_id.id
                                    })
                            # os.remove(fullpath)
                            if strs_check.find(filename_check):
                                if filename_check2 == '1':
                                    product_id.write({'image': image})
            else:
                raise ValidationError(u'產品 %s 未建立' % product_code)


    @api.multi
    def delete_by_upload_no(self):
        if  self.env["product.template"].search([('upload_no', '=', self.delete_sequence)]):
            self.env["product.template"].search([('upload_no', '=', self.delete_sequence)]).unlink()
        else:
            raise ValidationError(u"查無此批次號，請重新輸入")