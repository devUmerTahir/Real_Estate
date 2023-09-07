from odoo import api, fields, models
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Model for Property Offers"

    price = fields.Float()
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string="Status", copy=False)

    # SQL constraint to enforce that offer price must be strictly positive
    _sql_constraints = [
        (
            'check_offer_price_positive',
            'CHECK(price >= 0)',
            'Offer price must be strictly positive.'
        ),
    ]
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    # Existing methods...

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.validity:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = False

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline and offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date).days
