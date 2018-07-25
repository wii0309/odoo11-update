# -*- coding:utf-8 -*-
from odoo import api, fields, models

class hrexpense_inherit(models.Model):
    _inherit = 'hr.expense'

    supplier = fields.Many2one(comodel_name='res.partner', string='供應商')

    def _prepare_move_line(self, line):
        res = super(hrexpense_inherit, self)._prepare_move_line(line)
        if res['debit'] > 0:
            res['supplier'] = self.supplier.id
            if self.supplier:
                res['name'] = self.supplier.name + ': '+ self.name
        return res
