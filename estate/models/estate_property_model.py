from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError



# from . import estate_property_offer_model  # Import the new model


class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "Model for Real-Estate Properties"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float(string="Garden Area (sqm)")
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], string="Garden Orientation")

    # Add a state field with default value 'New', required, and not copied
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], string="State", default='new', required=True, copy=False)

    # added a new "state" field to the model with the specified values,
    # making it required, not copied, and having a default value of 'New'.

    # SQL constraint to enforce that expected_price must be strictly positive
    _sql_constraints = [
        (
            'check_expected_price_positive',
            'CHECK(expected_price >= 0)',
            'Expected price must be strictly positive.'
        ),
        (
            'check_selling_price_positive',
            'CHECK(selling_price >= 0)',
            'Selling price must be positive.'
        ),
    ]

    # Override create method to set default values for bedrooms and availability date

    def create(self, vals):
        if 'bedrooms' not in vals:
            vals['bedrooms'] = 2
        if 'date_availability' not in vals:
            vals['date_availability'] = fields.Date.today() + timedelta(days=90)
        return super(EstateProperties, self).create(vals)

    # Add a Many2one field linking to the estate.property.type model
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user.id)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags", widget="many2many_tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area", store=True, string="Total Area")
    best_price = fields.Float(compute="_compute_best_price", store=True, string="Best Price")

    # Add the methods for the buttons
    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Cannot cancel a sold property.")
            record.state = 'canceled'
        return True

    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Cannot mark a canceled property as sold.")
            record.state = 'sold'
        return True
    # Define the compute methods for the computed fields
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    # Add onchange method for the 'garden' field
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10.0
            self.garden_orientation = "north"
        else:
            self.garden_area = 0.0
            self.garden_orientation = False
    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0.9 * record.expected_price:
                raise ValidationError("Selling price cannot be lower than 90% of the expected price.")
