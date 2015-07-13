# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv

class hr_expense_line(osv.osv):
    _inherit='hr.expense.line'
    _columns = {
         'distribution_id':fields.many2one('account.analytic.plan.instance','Analytic Distribution'),
    }
hr_expense_line()

class hr_expense_expense(osv.osv):
    _inherit = "hr.expense.expense"
    
    def action_invoice_create(self, cr, uid, ids):
        res = super(hr_expense_expense, self).action_invoice_create(cr, uid, ids)
        for exp in self.browse(cr, uid, ids):
            if exp.invoice_id:
                for exp_line in exp.line_ids:
                    for inv_line in exp.invoice_id.invoice_line:
                        if inv_line.name == exp_line.name and inv_line.price_unit == exp_line.unit_amount \
                            and inv_line.quantity == exp_line.unit_quantity and inv_line.uos_id.id == exp_line.uom_id.id:
                            inv_line.write({'analytics_id': exp_line.distribution_id.id})

hr_expense_expense()
