# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 Domsense s.r.l. (<http://www.domsense.com>).
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

from osv import osv, fields

class crm_lead2opportunity_partner(osv.osv_memory):

    _inherit = 'crm.lead2opportunity.partner'

    def _create_partner(self, cr, uid, ids, context=None):
        partner_ids = super(crm_lead2opportunity_partner, self)._create_partner(cr, uid, ids, context)
        rec_ids = context and context.get('active_ids', [])
        lead_obj = self.pool.get('crm.lead')
        contact_obj = self.pool.get('res.partner.contact')
        job_obj = self.pool.get('res.partner.address')
        for data in self.browse(cr, uid, ids, context=context):
            for lead in lead_obj.browse(cr, uid, rec_ids, context=context):
                if data.action == 'create':
                    if lead.partner_address_id:
                        contact_id = contact_obj.create(cr, uid, {
                            'last_name': lead.contact_last_name,
                            'first_name': lead.contact_first_name,
                            'mobile': lead.mobile,
                            'title': lead.title and lead.title.id or False,
                            'email': lead.email_from,
                            })
                        job_id = job_obj.create(cr, uid, {
                            'address_id': lead.partner_address_id.id,
                            'contact_id': contact_id,
                            'function': lead.function,
                            'email': lead.email_from,
                            'phone': lead.phone,
                            'fax': lead.fax,
                            })
        return partner_ids

crm_lead2opportunity_partner()
