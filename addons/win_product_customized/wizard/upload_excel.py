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
        product_chec=self.env['product.template'].search([])  #導向環境後要加入search才能跑每一筆
        product_data=[]
        xname = ''
        xmemo_add=''
        xwave_band=''
        xmanufactor_no=''
        xquotation_price=''
        xcost=''
        xbig_type=''
        size_r = []
        color_r = []
        all_product_name=[]

        for r in product_chec:    #撈出所有產品名
            if r.name :
                all_product_name.append(r.name)


        # for row in range(1, sheet.nrows):
        for row in range(1, 4):
            # cell = sheet.cell(row, 0)  #主要廠商
            # if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
            #     xmajor_manufactor = u'' + str((cell.value))
            #     major_manufactor_ser=self.env['res.partner'].search([('name', '=', xmajor_manufactor)])

            cell = sheet.cell(row, 7)  # 貨號
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xname = u'' + str((cell.value))

            cell = sheet.cell(row, 19)  # 成份
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xmaterial_include= u'' + str((cell.value))

            cell = sheet.cell(row, 18)  #製造地
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xmade_in = u'' + str((cell.value))

            cell = sheet.cell(row, 16)  # 牌價
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xquotation_price = u'' + str((cell.value))

            cell = sheet.cell(row, 13)  #設計師
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xman_type = u'' + str((cell.value))
                man_type_check = self.env['man.type'].create({'name': xman_type})

            cell = sheet.cell(row, 12)  # 品別
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xproduct_class = u'' + str((cell.value))
                product_class_check = self.env['product.class'].create({'name': xproduct_class})

            cell = sheet.cell(row, 11)  # 品牌系列
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xcategory = u'' + str((cell.value))
                category_check = self.env['category.name'].create({'name': xcategory})

            cell = sheet.cell(row, 3)  # 備註
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xmemo_add = u'' + str((cell.value))

            cell = sheet.cell(row, 6)  # 波段
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xwave_band = u'' + str((cell.value))

            cell = sheet.cell(row, 1)  # 商品內碼
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xmanufactor_no = u'' + str((cell.value))

            cell = sheet.cell(row, 15)  # 成本
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xcost = u'' + str((cell.value))

            cell = sheet.cell(row, 5)  # 大類
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xbig_type = u'' + str((cell.value))

            cell = sheet.cell(row, 4)  # 年季
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xyear_season = u'' + str((cell.value))


            cell = sheet.cell(row, 8)  # 色號
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

            cell = sheet.cell(row, 10)  # 尺寸
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


            if xname not in all_product_name:
                product_data = product_rec.create({
                    'name': xname,
                    'memo_add':xmemo_add,
                    'wave_band':xwave_band,
                    'big_type':xbig_type,
                    'manufactor_no':xmanufactor_no,
                    'year_season':xyear_season,
                    'material_include':xmaterial_include,
                    'made_in':xmade_in,
                    'quotation_price':xquotation_price,
                    'man_type':man_type_check.id,
                    'product_class':product_class_check.id,
                    'category':category_check.id,
                    'size': size_r,
                    'color_name':color_r,
                    'upload_no':upload_sequence,
                    'standard_price':xcost,
                    'website_published':True})
                self.click_to_add_attribute(product_data)

            else:#已有該產品 要確認變體是否有增加
                cd_product=self.env['product.template'].search([('name', '=', xname)])
                if len(cd_product) == 1:
                    for row in cd_product.attribute_line_ids.filtered(lambda  x :x.attribute_id==1):
                        color_id_search=self.look_for_color_table(xcolor)
                        if color_id_search.id in row.vaule_ids:
                            continue
                        elif color_id_search.id not in row.vaule_ids:
                            row.write({
                                'value_ids': [(4, color_id_search.id)]
                            })
                            cd_product.create_variant_ids()
                    for row in cd_product.attribute_line_ids.filtered(lambda  x :x.attribute_id==2):
                        size_id_search=self.look_for_size_table(xsize)
                        if size_id_search.id in row.vaule_ids:
                            continue
                        elif size_id_search.id not in row.vaule_ids:
                            row.write({
                                'value_ids': [(4, size_id_search.id)]
                            })
                            cd_product.create_variant_ids()
                    all_product_name.append(xname)
                elif len(cd_product) > 1:
                    raise ValidationError(u'錯誤！產品名稱 :%s 重複' % (xname))

            # Product = self.env["product.product"].search([('name','=',xname)])
            # for line in Product:
            #     line.attribute_value_ids.mapped()
    def look_for_color_table(self,color):
        found_color_id=self.env['color.table'].search([('color_num', '=', color)])
        if found_color_id:
            return found_color_id
        else :
            raise ValidationError(u'錯誤！顏色  :%s，未建立' % (color))


    def look_for_size_table(self,size):
        found_size_id=self.env['size.table'].search([('size_type', '=', size)])
        if found_size_id:
            return found_size_id
        else :
            raise ValidationError(u'錯誤！尺寸:%s，未建立' % (size))


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
        # mypath = "/odoo/product_image"
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