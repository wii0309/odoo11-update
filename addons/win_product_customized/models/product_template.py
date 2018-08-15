# -*- coding: utf-8 -*-
from odoo import api, fields, models,tools
from os import listdir
import base64
import imghdr
from odoo.exceptions import UserError,ValidationError
import os
import glob


class Addproductinfo(models.Model):
    _inherit = 'product.template'
    org_image=fields.Binary()
    major_manufactor=fields.Many2one('res.partner', string='主要廠商')
    brand=fields.Many2one('brand.info', string='品牌')
    brand_type=fields.Many2one('brand.type', string='品牌系列')
    year_season=fields.Many2one('year.season', string='年季')
    category=fields.Many2one('category.name', string='類別(字頭)')
    inventory_place=fields.Many2one('inventory.place', string='倉儲位置')
    man_type=fields.Many2one('man.type', string='設計師')
    big_type=fields.Many2one('big.type', string='大類')
    mid_type=fields.Many2one('mid.type', string='中類')
    sml_type=fields.Many2one('sml.type', string='小類')
    color_name = fields.Many2many(comodel_name='color.table', string='色別碼')
    size = fields.Many2many(comodel_name='size.table', string='尺寸碼')
    cloth=fields.Char(string='布料')
    wholesale_price=fields.Float(string='批價')
    quotation_price=fields.Float(string='貨品牌價')
    files = fields.Binary(string="上傳產品照片壓縮檔")
    filename = fields.Char()
    upload_no=fields.Char(string='上傳批次號')

    region_code = fields.Many2many(comodel_name='region.name', string='區域')
    gift_code = fields.Many2one(comodel_name='gift.code', string='贈品')
    additional_code=fields.Many2one(comodel_name='additional.code', string='追加碼')
    new_brand=fields.Char(string='品牌')
    product_class=fields.Many2one(comodel_name='product.class', string='品項')


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





    @api.onchange('major_manufactor')  #Dynamic domain solution
    def onchange_brand(self):
        res = {}
        if self.major_manufactor:
            res['domain'] = {'brand': [('manuf', '=', self.major_manufactor.id)]}
        return res


