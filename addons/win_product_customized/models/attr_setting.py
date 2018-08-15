
from odoo import api, fields, models

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
    ser_number = fields.Char(string='序號')

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

    size_type = fields.Char(string='尺寸號(OS,OM,OF)')
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
    ser_number = fields.Char(string='序號')

class Region_code(models.Model):
    _name = 'region.name'

    name = fields.Char(string='區域')
    ser_number=fields.Char(string='序號')


class Gift_code(models.Model):
    _name = 'gift.code'

    name = fields.Char(string='贈品')
    ser_number=fields.Char(string='序號')

class Additonal_code(models.Model):
    _name = 'additional.code'

    name = fields.Char(string='追加碼')
    ser_number = fields.Char(string='序號')

class Res_inherit(models.Model):
    _inherit = 'res.partner'

    ser_number = fields.Char(string='序號')