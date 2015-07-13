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

class purchase_order(osv.osv):
    
    _inherit = 'purchase.order'
    
    def _get_deferred_analytic_lines(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        for po in self.browse(cr, uid, ids):
            analytic_lines = []
            for line in po.order_line:
                try:
                    if line.deferred_line_ids:
                        analytic_lines.extend([x.id for x in line.deferred_line_ids])
                except orm.except_orm, e:
                    if e.name != 'AccessError':
                        raise e
            res[po.id] = analytic_lines
        return res
    
    _columns={
        'deferred_analytics_id': fields.many2one('account.analytic.plan.instance', 'Deferred Analytic Distribution'),
        'deferred_line_ids': fields.function(_get_deferred_analytic_lines, type='one2many',
            obj='account.analytic.line', method=True, string='Analytic Lines'),
        }

    def delete_analytic_lines(self, cr, uid, ids, context=None):
        analytic_line_obj = self.pool.get('account.analytic.line')
        for po in self.browse(cr, uid, ids):
            for line in po.deferred_line_ids:
                line.unlink()
        return True

    def create_analytic_lines(self, cr, uid, ids, context=None):
        analytic_line_obj = self.pool.get('account.analytic.line')
        journal_obj = self.pool.get('account.journal')
        po_line_obj = self.pool.get('purchase.order.line')
        for po in self.browse(cr, uid, ids):
            journal_ids = journal_obj.search(cr, uid, [
                ('type', '=','purchase'),('company_id', '=', po.company_id.id)], limit=1)
            if not journal_ids:
                raise osv.except_osv(_('Error !'),
                    _('There is no purchase journal defined for this company: "%s" (id:%d)')
                        % (po.company_id.name, po.company_id.id))
            journal  = journal_obj.browse(cr, uid, journal_ids[0])
            if not journal.analytic_journal_id:
                raise osv.except_osv(_('No Analytic Journal !'),
                    _("You have to define an analytic journal on the '%s' journal!") % (journal.name))
            if not journal.default_debit_account_id:
                raise osv.except_osv(_('No Debit Account !'),
                    _("You have to define a default debit account on the '%s' journal!") % (journal.name))
            if po.deferred_line_ids:
                raise osv.except_osv(_('Error'),
                    _('Analytic lines yet generated for order %s. Remove them first') % po.name)
            for po_line in po.order_line:
                if not po_line.deferred_analytics_id and not po.deferred_analytics_id:
                    raise osv.except_osv(_('Error'),_('Order %s and line %s have no Deferred Analytic Distribution')
                        % (po.name or '', po_line.name))
                if po_line.deferred_analytics_id:
                    deferred_analytics_id = po_line.deferred_analytics_id
                else:
                    deferred_analytics_id = po.deferred_analytics_id
                for plan_line in deferred_analytics_id.account_ids:
                    amount = - po_line.price_subtotal * (plan_line.rate / 100)
                    al_vals={
                        'name': po_line.name,
                        'account_id': plan_line.analytic_account_id.id,
                        'unit_amount': po_line.product_qty,
                        'product_id': po_line.product_id and po_line.product_id.id or False,
                        'product_uom_id': po_line.product_uom and po_line.product_uom.id or False,
                        'amount': amount,
                        'journal_id': journal.analytic_journal_id.id,
                        'percentage': plan_line.rate,
                        'deferred_purchase_order_line_id': po_line.id,
                        'general_account_id': journal.default_debit_account_id.id,
                    }
                    al_id = analytic_line_obj.create(cr, uid, al_vals, context=context)
        return True
        
purchase_order()

class purchase_order_line(osv.osv):
    
    _inherit = 'purchase.order.line'
    
    _columns={
        'deferred_analytics_id': fields.many2one('account.analytic.plan.instance', 'Deferred Analytic Distribution'),
        'deferred_line_ids': fields.one2many('account.analytic.line', 'deferred_purchase_order_line_id',
            'Analytic Lines'),
        }
        
purchase_order_line()
