# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012 VRT Systems (<http://www.vrt.com.au>).
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

class crm_lead(osv.osv):
    """ CRM Lead Case """
    _name = "crm.lead"
    _inherit = 'crm.lead'

    def _name_get_full(self, cr, uid, ids, prop, unknow_none, context=None):
        """ Calculate full name """
        result = {}
        for rec in self.browse(cr, uid, ids, context=context):
            name_parts = []

            if(rec.contact_first_name):
                name_parts.append(rec.contact_first_name)

            if(rec.contact_last_name):
                name_parts.append(rec.contact_last_name)

            if name_parts:
                result[rec.id] = ' '.join(name_parts)
            else:
                result[rec.id] = False

        return result

    _columns = {
        'contact_last_name': fields.char('Contact Last Name', size=64),
        'contact_first_name': fields.char('Contact First Name', size=64),
        'contact_name': fields.function(_name_get_full, string='Contact Name', size=64,
                type="char", store=False),
    }

    def _lead_create_partner_location(self, cr, uid, lead, context=None):
        location = self.pool.get('res.partner.location')
        return location.create(cr, uid, {
                    'street': lead.street,
                    'street2': lead.street2,
                    'zip': lead.zip,
                    'city': lead.city,
                    'state_id': lead.state_id and lead.state_id.id or False,
                    'country_id': lead.country_id and lead.country_id.id or False,
                })

    def _lead_create_partner_contact(self, cr, uid, lead, context=None):
        location = self.pool.get('res.partner.contact')
        return location.create(cr, uid, {
                    'first_name': lead.contact_first_name,
                    'last_name': lead.contact_last_name,
                    'mobile': lead.mobile,
                    'title': lead.title and lead.title.id or False,
                })

    def _lead_create_partner_address(self, cr, uid, lead, partner_id, context=None):
        address_id = super(crm_lead, self)._lead_create_partner_address(cr, uid, lead, partner_id, context=context)
        location_id = self._lead_create_partner_location(cr, uid, lead, context=context)
        contact_id = self._lead_create_partner_contact(cr, uid, lead, context=context)

        address = self.pool.get('res.partner.address')
        address.write(cr, uid, [address_id], {
                    'location_id': location_id,
                    'contact_id': contact_id,
                })
        return address_id

crm_lead()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
