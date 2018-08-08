# -*- coding: utf-8 -*-
from odoo import api, fields, models
from os import listdir
from os.path import isfile, isdir, join
import base64
import imghdr
from odoo.exceptions import UserError,ValidationError
import os
import glob
import xlrd
from odoo import http
XL_CELL_EMPTY = 0
XL_CELL_TEXT = 1
XL_CELL_NUMBER = 2
XL_CELL_DATE = 3
XL_CELL_BOOLEAN = 4
XL_CELL_ERROR = 5
XL_CELL_BLANK = 6
class Addproductinfo(models.Model):
    _inherit = 'product.template'

    major_manufactor=fields.Many2one('mm.info', string='主要廠商')
    brand=fields.Many2one('brand.info', string='品牌')
    brand_type=fields.Many2one('brand.type', string='品牌系列')
    year_season=fields.Many2one('year.season', string='年季')
    category=fields.Many2one('category.name', string='品別')
    inventory_place=fields.Many2one('inventory.place', string='倉儲位置')
    man_type=fields.Many2one('man.type', string='設計師')
    big_type=fields.Many2one('big.type', string='大類')
    mid_type=fields.Many2one('mid.type', string='中類')
    sml_type=fields.Many2one('sml.type', string='小類')
    color_name = fields.Many2many(comodel_name='color.table', string='顏色')
    # color_name = fields.Char(string='顏色')
    size = fields.Many2many(comodel_name='size.table', string='尺寸')
    cloth=fields.Char(string='布料')
    wholesale_price=fields.Float(string='批價')
    quotation_price=fields.Float(string='貨品牌價')
    files = fields.Binary(string="上傳產品照片壓縮檔")
    filename = fields.Char()
    excel_file = fields.Binary(string=u"上傳EXCEL檔案")
    start_row = fields.Integer(size=3, string=u"啟始ROW", default=2)
    end_row = fields.Integer(size=3, string=u"結止ROW", default=2)
    product_class=fields.Many2one('product.class', string='品名')

    def partner_action_import(self):

        if self.start_row == 1:
            raise UserError(u"數值錯誤,ROW啟始數值從 2 開始")
        if self.start_row < 0 or self.end_row < 0:
            raise UserError(u"數值錯誤,ROW數值不能小於0")
        if self.start_row > self.end_row:
            raise UserError(u"數值錯誤,啟始ROW數值大於結止ROW")

        if not self.excel_file:
            raise UserError(u"檔案錯誤,沒有上傳正確的Excel File")

        xls = xlrd.open_workbook(file_contents=base64.decodebytes(self.excel_file))
        sheet = xls.sheet_by_index(0)
        if self.start_row > 0 or self.end_row > 0:
            nstartrow = self.start_row
            if self.end_row > sheet.nrows:
                nendrow = sheet.nrows
            else:
                nendrow = self.end_row
        else:
            nstartrow = 2
            nendrow = sheet.nrows

        self.ensure_one()
        product_rec = self.env['product.template']

        if not self.excel_file:
            raise UserError(u"沒有上傳正確的Excel File")

        xls = xlrd.open_workbook(file_contents=base64.decodebytes(self.excel_file))
        sheet = xls.sheet_by_index(0)

        for row in range(nstartrow - 1, nendrow):

            cell = sheet.cell(row, 0) #貨組代號
            xname = 0
            if cell.ctype == XL_CELL_EMPTY:
                continue
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xname = u'' + str((cell.value))
                same_check = self.env['product.template'].search([('name', '=', xname)]) #做重複檔名的排除
                if same_check:
                    break

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

            cell = sheet.cell(row, 18) #顏色     需要做分割s.p.l.i.t
            xcolor_name = '-'
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xcolor_name = u'' + str((cell.value))

            cell = sheet.cell(row, 6)  #品名
            if cell.ctype in (XL_CELL_TEXT, XL_CELL_NUMBER):
                xproduct_class = u'' + str((cell.value))
            else:
                xproduct_class = 0

            #以下是做判斷屬性是否存在，若無，可自動新增每一個

            brand_check = self.env['brand.info'].search([('name', '=', xbrand)])

            if not brand_check:
                brand_check = self.env['brand.info'].create({'name': xbrand})

            brand_type_check = self.env['brand.type'].search([('name', '=', xbrand_type)])

            if not brand_type_check:
                brand_type_check = self.env['brand.type'].create({'name': xbrand_type})

            year_season_check = self.env['year.season'].search([('name', '=', xyear_season)])

            if not year_season_check:
                year_season_check = self.env['year.season'].create({'name': xyear_season})

            category_check = self.env['category.name'].search([('name', '=', xcategory)])

            if not category_check:
                category_check = self.env['category.name'].create({'name': xcategory})

            man_type_check = self.env['man.type'].search([('name', '=', xman_type)])

            if not man_type_check:
                man_type_check = self.env['man.type'].create({'name': xman_type})

            big_type_check = self.env['big.type'].search([('name', '=', xbig_type)])

            if not big_type_check:
                big_type_check = self.env['big.type'].create({'name': xbig_type})

            mid_type_check = self.env['mid.type'].search([('name', '=', xmid_type)])

            if not mid_type_check:
                mid_type_check = self.env['mid.type'].create({'name': xmid_type})

            sml_type_check = self.env['sml.type'].search([('name', '=', xsml_type)])

            if not sml_type_check:
                sml_type_check = self.env['sml.type'].create({'name': xsml_type})

            mm_check=self.env['mm.info'].search([('name','=',xmajor_manufactor)])

            if not mm_check:
                mm_check=self.env['mm.info'].create({'name': xmajor_manufactor})


            color_check=self.env['color.table'].search([('name','=',xcolor_name)])

            if not color_check:
                color_check=self.env['color.table'].create({'name':xcolor_name})

            size_check = self.env['size.table'].search([('name', '=', xsize)])

            if not size_check:
                size_check = self.env['size.table'].create({'name': xsize})

            product_class_check = self.env['product.class'].search([('name', '=', xproduct_class)])

            if not product_class_check:
                product_class_check = self.env['product.class'].create({'name': xproduct_class})

            #開始做產品
            myparid = product_rec.create({'name': xname,
                                          'major_manufactor': mm_check.id,
                                          'brand_type': brand_type_check.id,
                                          'brand': brand_check.id,
                                          'category': category_check.id,
                                          'year_season': year_season_check.id,
                                          'man_type': man_type_check.id,
                                          'sml_type': sml_type_check.id,
                                          'mid_type': mid_type_check.id,
                                          'big_type': big_type_check.id,
                                          'size': [(4,size_check.id)],
                                          'product_class': product_class_check.id,
                                          'quotation_price': xquotation_price,
                                          'color_name':[(4,color_check.id)]})

    def click_to_add_attribute(self):
        print('nobug')


    @api.onchange('files')
    def _check_filename(self):
        if self.files:
            if not self.filename:
                raise ValidationError(u'沒有檔案')
            else:
                tmp = self.filename.split('.')
                ext = tmp[len(tmp) - 1]
                if ext != 'rar' and ext != 'zip':
                    self.files = None
                    raise ValidationError(u'上傳檔案並非壓縮檔')
        elif not self.files:
            pass

    def batch_upload(self):
        # mypath = "/odoo/product_image"
        mypath = "//192.168.1.7/文件/python 測試用"
        files = listdir(mypath)
        tmp = []
        for f in files:
            if imghdr.what(mypath + '/' + f):
                str = f.split("_")
                if str[0] not in tmp:
                    tmp.append(str[0])
        for product_code in tmp:
            product_id = self.env['product.template'].search([('name','=',product_code)])
            if product_id:
                for fullpath in glob.glob(mypath + '/' + product_id.name + '_*'):
                    image_type = imghdr.what(fullpath)
                    if image_type:
                        with open(fullpath, "rb") as imageFile:
                            image = base64.b64encode(imageFile.read())
                            filename = os.path.basename(fullpath).split(".")[0]
                            existed = self.env['product.image'].search([('name', '=', filename)])
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
            else:
                raise ValidationError(u'產品 %s 未建立' % product_code)


    @api.onchange('major_manufactor')  #Dynamic domain solution
    def onchange_brand(self):
        res = {}
        if self.major_manufactor:
            res['domain'] = {'brand': [('manuf', '=', self.major_manufactor.id)]}
        return res

class Mminfo(models.Model):
    _name = 'mm.info'

    name = fields.Char(string='廠商名',required=True)
    address= fields.Char(string='地址')


class Brand_info(models.Model):
    _name = 'brand.info'

    name = fields.Char(string='品牌')
    manuf=major_manufactor=fields.Many2one('mm.info', string='主要廠商')

class Brand_type(models.Model):
    _name = 'brand.type'

    name = fields.Char(string='名稱')
    tag=fields.Char(string='標籤')

class Year_season(models.Model):
    _name = 'year.season'

    name = fields.Char(string='年季')

class Category(models.Model):
    _name = 'category.name'

    name = fields.Char(string='種類名')

class Inventory_place(models.Model):
    _name = 'inventory.place'

    name = fields.Char(string='倉庫名')

class Man_type(models.Model):
    _name = 'man.type'

    name = fields.Char(string='名')

class Big_type(models.Model):
    _name = 'big.type'

    name = fields.Char(string='大類標籤')


class Mid_type(models.Model):
    _name = 'mid.type'

    name = fields.Char(string='中類標籤')


class Sml_type(models.Model):
    _name = 'sml.type'

    name = fields.Char(string='小類標籤')

class Color_table(models.Model):
    _name = 'color.table'

    name = fields.Char(string='主要顏色')
    color_num=fields.Char(string='色號')

class Size_table(models.Model):
    _name = 'size.table'

    name = fields.Char(string='所有尺寸(s,m,l)')
    size_num=fields.Char(string='尺寸號(s,m,f)')

class Product_class(models.Model):
    _name = 'product.class'

    name = fields.Char(string='品名')
