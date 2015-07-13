# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2011 Domsense srl (<http://www.domsense.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv
from tools.translate import _
from osv import orm

class hr_expense(osv.osv):
    
    _inherit = 'hr.expense.expense'
    
    def _get_deferred_analytic_lines(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        for expense in self.browse(cr, uid, ids):
            analytic_lines = []
            for line in expense.line_ids:
                try:
                    if line.deferred_line_ids:
                        analytic_lines.extend([x.id for x in line.deferred_line_ids])
                except orm.except_orm, e:
                    if e.name != 'AccessError':
                        raise e
            res[expense.id] = analytic_lines
        return res
    
    _columns={
        'deferred_analytics_id': fields.many2one('account.analytic.plan.instance', 'Deferred Analytic Distribution'),
        'deferred_line_ids': fields.function(_get_deferred_analytic_lines, type='one2many',
            obj='account.analytic.line', method=True, string='Analytic Lines'),
        }

    def delete_analytic_lines(self, cr, uid, ids, context=None):
        analytic_line_obj = self.pool.get('account.analytic.line')
        for expense in self.browse(cr, uid, ids):
            for line in expense.deferred_line_ids:
                line.unlink()
        return True

    def create_analytic_lines(self, cr, uid, ids, context=None):
        analytic_line_obj = self.pool.get('account.analytic.line')
        journal_obj = self.pool.get('account.journal')
        expense_line_obj = self.pool.get('hr.expense.line')
        for expense in self.browse(cr, uid, ids):
            journal_ids = journal_obj.search(cr, uid, [
                ('type', '=','purchase'),('company_id', '=', expense.company_id.id)], limit=1)
            if not journal_ids:
                raise osv.except_osv(_('Error !'),
                    _('There is no purchase journal defined for this company: "%s" (id:%d)')
                        % (expense.company_id.name, expensecompany_id.id))
            journal  = journal_obj.browse(cr, uid, journal_ids[0])
            if not journal.analytic_journal_id:
                raise osv.except_osv(_('No Analytic Journal !'),
                    _("You have to define an analytic journal on the '%s' journal!") % (journal.name))
            if not journal.default_debit_account_id:
                raise osv.except_osv(_('No Debit Account !'),
                    _("You have to define a default debit account on the '%s' journal!") % (journal.name))
            if expense.deferred_line_ids:
                raise osv.except_osv(_('Error'),
                    _('Analytic lines yet generated for expense %s. Remove them first') % expense.name)
            for line in expense.line_ids:
                if not line.deferred_analytics_id and not expense.deferred_analytics_id:
                    raise osv.except_osv(_('Error'),_('Expense %s and line %s have no Deferred Analytic Distribution')
                        % (expense.name or '', line.name))
                if line.deferred_analytics_id:
                    deferred_analytics_id = line.deferred_analytics_id
                else:
                    deferred_analytics_id = expense.deferred_analytics_id
                for plan_line in deferred_analytics_id.account_ids:
                    amount = - line.total_amount * (plan_line.rate / 100)
                    al_vals={
                        'name': line.name,
                        'account_id': plan_line.analytic_account_id.id,
                        'unit_amount': line.unit_quantity,
                        'product_id': line.product_id and line.product_id.id or False,
                        'product_uom_id': line.uom_id and line.uom_id.id or False,
                        'amount': amount,
                        'journal_id': journal.analytic_journal_id.id,
                        'percentage': plan_line.rate,
                        'deferred_expense_line_id': line.id,
                        'general_account_id': journal.default_debit_account_id.id,
                    }
                    al_id = analytic_line_obj.create(cr, uid, al_vals, context=context)
        return True
        
hr_expense()

class hr_expense_line(osv.osv):
    
    _inherit = 'hr.expense.line'
    
    _columns={
        'deferred_analytics_id': fields.many2one('account.analytic.plan.instance', 'Deferred Analytic Distribution'),
        'deferred_line_ids': fields.one2many('account.analytic.line', 'deferred_expense_line_id',
            'Analytic Lines'),
        }
        
hr_expense_line()
