# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Addproductinfo(models.Model):

    _inherit = 'product.template'

    major_manufactor=fields.Many2one('mm.info', string='主要廠商')
    brand=fields.Many2one('res.partner', string='品牌')   #要用onchnge domain
    brand_type=fields.Many2one('brand.type', string='品牌系列')
    year_season=fields.Many2one('year.season', string='年季')
    category=fields.Many2one('category.name', string='品別') #下拉固定選項
    cloth=fields.Char(string='布料')
    inventory_placee=fields.Many2one('inventory.place', string='倉儲位置')
    man_type=fields.Many2one('man.type', string='系列')
    big_type=fields.Many2one('big.type', string='大類')
    mid_type=fields.Many2one('mid.type', string='中類')
    sml_type=fields.Many2one('sml.type', string='小類')
    color = fields.Char(string='顏色')
    size = fields.Char(string='尺寸')

class Mminfo(models.Model):
    _name = 'mm.info'

    name = fields.Char(string='廠商名',required=True)
    address= fields.Char(string='地址')


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

    name = fields.Char(string='名子')

class Big_type(models.Model):
    _name = 'big.type'

    name = fields.Char(string='大類標籤')


class Mid_type(models.Model):
    _name = 'mid.type'

    name = fields.Char(string='中類標籤')


class Sml_type(models.Model):
    _name = 'sml.type'

    name = fields.Char(string='小類標籤')


