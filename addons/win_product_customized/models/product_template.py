# -*- coding: utf-8 -*-
from odoo import api, fields, models
from os import listdir
import base64
import imghdr
from odoo.exceptions import UserError,ValidationError
import os
import glob

class Addproductinfo(models.Model):
    _inherit = 'product.template'

    major_manufactor=fields.Many2one('res.partner', string='主要廠商')
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
    # size = fields.Char(string='尺寸')
    cloth=fields.Char(string='布料')
    wholesale_price=fields.Float(string='批價')
    quotation_price=fields.Float(string='貨品牌價')
    files = fields.Binary(string="上傳產品照片壓縮檔")
    filename = fields.Char()
    upload_no=fields.Char(string='上傳批次號' )

    product_class=fields.Many2one('product.class', string='品名')


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


class Brand_info(models.Model):
    _name = 'brand.info'

    name = fields.Char(string='品牌')
    major_manufactor=fields.Many2one('res.panter', string='主要廠商')

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

    color_num=fields.Char(string='色號')
    product_attribute_id = fields.Many2one('product.attribute.value',string='顏色')

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record.color_num
            result.append((record.id, name))
        return result

class Size_table(models.Model):
    _name = 'size.table'

    size_type = fields.Char(string='尺寸號(S,M,F)')
    product_attribute_id = fields.Many2one('product.attribute.value', string='尺寸')

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = record.size_type
            result.append((record.id, name))
        return result

class Product_class(models.Model):
    _name = 'product.class'

    name = fields.Char(string='品名')




