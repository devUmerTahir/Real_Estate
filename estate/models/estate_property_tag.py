from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tags"

    name = fields.Char(required=True)
    _sql_constraints = [
        (
            'uniq_name',
            'UNIQUE(name)',
            'Property tag name must be unique.'
        ),
    ]
