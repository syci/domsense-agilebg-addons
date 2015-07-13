# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2011 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2011 Domsense srl (<http://www.domsense.com>)
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################

from osv import fields, osv

class email_hosting_transport(osv.osv):
    _name = 'email.hosting.transport'
    _description = 'Transport'

    _rec_name = 'domain'
    _columns = {
        'domain': fields.char('Domain',size=128),
        'transport': fields.char('Transport',size=128),
    }
    
email_hosting_transport()

class email_hosting_users(osv.osv):
    _name = 'email.hosting.users'
    _description = 'Users'

    _rec_name = 'userid'
    _columns = {
        'userid': fields.char('User ID',size=128),
        'password': fields.char('Password',size=128),
        'realname': fields.char('Realname',size=128),
        'uid': fields.integer('UID'),
		'gid': fields.integer('GID'),    
		'home': fields.char('Home',size=128),
		'mail': fields.char('Mail',size=255),
	}
    
email_hosting_users()

class email_hosting_virtual(osv.osv):
    _name = 'email.hosting.virtual'
    _description = 'Virtual'

    _rec_name = 'address'
    _columns = {
        'address': fields.char('Address',size=128),
        'userid': fields.char('User ID',size=128),
	}
    
email_hosting_virtual()

class email_hosting_postfix_mailboxes(osv.osv):
    _name = 'email.hosting.postfix_mailboxes'
    _description = 'Postfix Mailboxes View'
    _auto = False
    _rec_name = "userid"
    _columns = {
        'userid': fields.char('User ID',size=128),
        'mailbox': fields.text('Mailbox'),
    }
    def init (self, cr) :
        cr.execute("""DROP VIEW IF EXISTS email_hosting_postfix_mailboxes""")
        cr.execute("""
                create view email_hosting_postfix_mailboxes as
  				select userid, home||'/' as mailbox from email_hosting_users
  				union all
  				select domain as userid, 'dummy' as mailbox from email_hosting_transport;
  				""")
email_hosting_postfix_mailboxes()

class email_hosting_postfix_virtual(osv.osv):
    _name = 'email.hosting.postfix_virtual'
    _description = 'Postfix Virtual View'
    _auto = False
    _rec_name = "userid"
    _columns = {
        'userid': fields.char('User ID',size=128),
        'address': fields.char('Address',size=128),
    }
    def init (self, cr) :
        cr.execute("""DROP VIEW IF EXISTS email_hosting_postfix_virtual""")
        cr.execute("""
                create view email_hosting_postfix_virtual as
  				select userid, userid as address from email_hosting_users
  				union all
  				select userid, address from email_hosting_virtual;
  				""")
email_hosting_postfix_virtual()
