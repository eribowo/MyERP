# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2016 Tiny SPRL (<http://tiny.be>). & eri Solutions.
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

import logging
import openerp

from openerp import tools
from openerp import fields, osv, models, api
from openerp.tools.translate import _

_logger = logging.getLogger(__name__)

class loyalty_program(models.Model):
    _name = 'loyalty.program'

    name = fields.Char('Loyalty Program Name', size=32, index=1, required=True, help="An internal identification for the loyalty program configuration")
    pp_currency =  fields.Float('Points per currency',help="How many loyalty points are given to the customer by sold currency")
    pp_product =   fields.Float('Points per product',help="How many loyalty points are given to the customer by product sold")
    pp_order =     fields.Float('Points per order',help="How many loyalty points are given to the customer for each sale or order")
    rounding =     fields.Float('Points Rounding', help="The loyalty point amounts are rounded to multiples of this value.", default=1)
    rule_ids =     fields.One2many('loyalty.rule','loyalty_program_id','Rules')
    reward_ids =   fields.One2many('loyalty.reward','loyalty_program_id','Rewards')

class loyalty_rule(models.Model):
    _name = 'loyalty.rule'

    name =                fields.Char('Name', size=32, index=1, required=True, help="An internal identification for this loyalty program rule")
    loyalty_program_id =  fields.Many2one('loyalty.program', 'Loyalty Program', help='The Loyalty Program this exception belongs to')
    rule_type =           fields.Selection((('product','Product'),('category','Category')), 'Type', required=True, help='Does this rule affects products, or a category of products ?', default='product')
    product_id =          fields.Many2one('product.product','Target Product',  help='The product affected by the rule')
    category_id =         fields.Many2one('pos.category',   'Target Category', help='The category affected by the rule')
    cumulative =          fields.Boolean('Cumulative',        help='The points won from this rule will be won in addition to other rules')
    pp_product =          fields.Float('Points per product',  help='How many points the product will earn per product ordered')
    pp_currency =  fields.Float('Points per currency', help='How many points the product will earn per value sold')


class loyalty_reward(models.Model):
    _name = 'loyalty.reward'

    name =                 fields.Char('Name', size=32, index=1, required=True, help='An internal identification for this loyalty reward')
    loyalty_program_id =   fields.Many2one('loyalty.program', 'Loyalty Program', help='The Loyalty Program this reward belongs to')
    minimum_points =       fields.Float('Minimum Points', help='The minimum amount of points the customer must have to qualify for this reward')
    reward_type =          fields.Selection((('gift','Gift'),('discount','Discount'),('resale','Resale')), 'Type', required=True, help='The type of the reward')
    gift_product_id =      fields.Many2one('product.product','Gift Product', help='The product given as a reward')
    point_cost =           fields.Float('Point Cost', help='The cost of the reward')
    discount_product_id =  fields.Many2one('product.product','Discount Product', help='The product used to apply discounts')
    discount =             fields.Float('Discount',help='The discount percentage')
    point_product_id =     fields.Many2one('product.product', 'Point Product', help='The product that represents a point that is sold by the customer')

    @api.multi
    def _check_gift_product(self):
        if self.reward_type == 'gift':
            return bool(self.gift_product_id)
        else:
            return True
    
    @api.multi
    def _check_discount_product(self):
        if self.reward_type == 'discount':
            return bool(self.discount_product_id)
        else:
            return True
    
    @api.multi
    def _check_point_product(self):
        if self.reward_type == 'resale':
            return bool(self.point_product_id)
        else:
            return True

    _constraints = [
        (_check_gift_product,     "The gift product field is mandatory for gift rewards",         ["reward_type","gift_product_id"]),
        (_check_discount_product, "The discount product field is mandatory for discount rewards", ["reward_type","discount_product_id"]),
        (_check_point_product,    "The point product field is mandatory for point resale rewards", ["reward_type","discount_product_id"]),
    ]

class PosConfig(models.Model):
    _inherit = 'pos.config' 

    loyalty_id = fields.Many2one('loyalty.program','Loyalty Program', help='The loyalty program used by this point_of_sale')

class res_partner(models.Model):
    _inherit = 'res.partner'
    loyalty_points = fields.Float('Loyalty Points', help='The loyalty points the user won as part of a Loyalty Program')


class PosOrder(models.Model):
    _inherit = 'pos.order'
    
    
    @api.model
    def _order_fields(self, ui_order):
        fields = super(PosOrder,self)._order_fields(ui_order)
        fields['loyalty_points'] = ui_order['loyalty_points'] or 0
        return fields
    
    loyalty_points = fields.Float('Loyalty Points', help='The amount of Loyalty points the customer won or lost with this order')
    
    @api.model
    def create_from_ui(self, orders):
        ids = super(PosOrder,self).create_from_ui(orders)
        for order in orders:
            if 'loyalty_points' in order['data'] and order['data']['loyalty_points'] != 0 and order['data']['partner_id']:
                partner_obj = self.partner_id
                partner = partner_obj.browse(order['data']['partner_id'])
                partner.write({'loyalty_points': partner['loyalty_points'] + order['data']['loyalty_points']})

        return ids
            
             
    
