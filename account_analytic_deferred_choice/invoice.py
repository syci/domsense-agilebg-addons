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

class account_invoice(osv.osv):

    _inherit = 'account.invoice'

    def _get_deferred_analytic_lines(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        for invoice in self.browse(cr, uid, ids):
            analytic_lines = []
            for line in invoice.invoice_line:
                try:
                    if line.deferred_line_ids:
                        analytic_lines.extend([x.id for x in line.deferred_line_ids])
                except orm.except_orm, e:
                    if e.name != 'AccessError':
                        raise e
            res[invoice.id] = analytic_lines
        return res

    _columns={
        'deferred_analytics_id': fields.many2one('account.analytic.plan.instance', 'Deferred Analytic Distribution'),
        'deferred_line_ids': fields.function(_get_deferred_analytic_lines, type='one2many', obj='account.analytic.line', method=True, string='Analytic Lines'),
        }

    def delete_analytic_lines(self, cr, uid, ids, context=None):
        analytic_line_obj = self.pool.get('account.analytic.line')
        for invoice in self.browse(cr, uid, ids):
            for line in invoice.deferred_line_ids:
                line.unlink()
        return True

    def create_analytic_lines(self, cr, uid, ids, context=None):
        analytic_line_obj = self.pool.get('account.analytic.line')
        invoice_line_obj = self.pool.get('account.invoice.line')
        for invoice in self.browse(cr, uid, ids):
            if invoice.deferred_line_ids:
                raise osv.except_osv(_('Error'),
                    _('Analytic lines yet generated for invoice %s. Remove them first') % invoice.name)
            for inv_line in invoice.invoice_line:
                if not inv_line.deferred_analytics_id and not invoice.deferred_analytics_id:
                    raise osv.except_osv(_('Error'),_('Invoice %s and line %s have no Deferred Analytic Distribution')
                        % (invoice.name or '', inv_line.name))
                if not invoice.journal_id.analytic_journal_id:
                   raise osv.except_osv(_('No Analytic Journal !'),_("You have to define an analytic journal on the '%s' journal!") % (invoice.journal_id.name,))
                if inv_line.deferred_analytics_id:
                    deferred_analytics_id = inv_line.deferred_analytics_id
                else:
                    deferred_analytics_id = invoice.deferred_analytics_id
                for plan_line in deferred_analytics_id.account_ids:
                    amount = inv_line.price_subtotal * (plan_line.rate / 100)
                    if invoice.type in ('in_invoice', 'out_refund'):
                        amount = - amount
                    al_vals={
                        'name': inv_line.name,
                        'account_id': plan_line.analytic_account_id.id,
                        'unit_amount': inv_line.quantity,
                        'product_id': inv_line.product_id and inv_line.product_id.id or False,
                        'product_uom_id': inv_line.uos_id and inv_line.uos_id.id or False,
                        'amount': amount,
                        'journal_id': invoice.journal_id.analytic_journal_id.id,
                        'percentage': plan_line.rate,
                        'deferred_invoice_line_id': inv_line.id,
                        'general_account_id': inv_line.account_id.id,
                    }
                    al_id = analytic_line_obj.create(cr, uid, al_vals, context=context)
        return True

account_invoice()

class account_invoice_line(osv.osv):

    _inherit = 'account.invoice.line'

    _columns={
        # TODO is it possible to have editable?
        'deferred_analytics_id': fields.many2one('account.analytic.plan.instance', 'Deferred Analytic Distribution'),
        'deferred_line_ids': fields.one2many('account.analytic.line', 'deferred_invoice_line_id', 'Analytic Lines'),
        }

account_invoice_line()

class account_move(osv.osv):

    _inherit = 'account.move'

    def _get_deferred_analytic_lines(self, cr, uid, ids, field_name, arg, context=None):
        res={}
        for move in self.browse(cr, uid, ids):
            analytic_lines = []
            for line in move.line_id:
                try:
                    if line.deferred_line_ids:
                        analytic_lines.extend([x.id for x in line.deferred_line_ids])
                except orm.except_orm, e:
                    if e.name != 'AccessError':
                        raise e
            res[move.id] = analytic_lines
        return res

    _columns={
        'deferred_analytics_id': fields.many2one('account.analytic.plan.instance', 'Deferred Analytic Distribution'),
        'deferred_line_ids': fields.function(_get_deferred_analytic_lines, type='one2many', obj='account.analytic.line', method=True, string='Analytic Lines'),
        }

    def delete_analytic_lines(self, cr, uid, ids, context=None):
        analytic_line_obj = self.pool.get('account.analytic.line')
        for move in self.browse(cr, uid, ids):
            for line in move.deferred_line_ids:
                line.unlink()
        return True

    def create_analytic_lines(self, cr, uid, ids, context=None):
        analytic_line_obj = self.pool.get('account.analytic.line')
        for move in self.browse(cr, uid, ids):
            if move.deferred_line_ids:
                raise osv.except_osv(_('Error'),
                    _('Analytic lines yet generated for Account Entry %s. Remove them first') % move.name)
            for move_line in move.line_id:
                if not move_line.deferred_analytics_id and not move.deferred_analytics_id:
                    continue
                if not move.journal_id.analytic_journal_id:
                   raise osv.except_osv(_('No Analytic Journal !'),_("You have to define an analytic journal on the '%s' journal!") % (invoice.journal_id.name,))
                if move_line.deferred_analytics_id:
                    deferred_analytics_id = move_line.deferred_analytics_id
                else:
                    deferred_analytics_id = move.deferred_analytics_id
                for plan_line in deferred_analytics_id.account_ids:
                    if move_line.credit:
                        amount = move_line.credit * (plan_line.rate / 100)
                    if move_line.debit:
                        amount = - move_line.debit * (plan_line.rate / 100)
                    al_vals={
                        'name': move_line.name,
                        'account_id': plan_line.analytic_account_id.id,
                        'unit_amount': False,
                        'product_id': False,
                        'product_uom_id': False,
                        'amount': amount,
                        'journal_id': move.journal_id.analytic_journal_id.id,
                        'percentage': plan_line.rate,
                        'deferred_account_move_line_id': move_line.id,
                        'general_account_id': move_line.account_id.id,
                    }
                    al_id = analytic_line_obj.create(cr, uid, al_vals, context=context)
        return True

account_move()

class account_move_line(osv.osv):

    _inherit = 'account.move.line'

    _columns={
        'deferred_analytics_id': fields.many2one('account.analytic.plan.instance', 'Deferred Analytic Distribution'),
        'deferred_line_ids': fields.one2many('account.analytic.line', 'deferred_account_move_line_id', 'Analytic Lines'),
        }

account_move_line()