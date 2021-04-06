declaration_insert_schema = {
    'type': 'object',
    'required': ['no_declaration', 'date_declaration', 'date_insp_vispre', 'nbr_extermin',
                 'date_debut_trait', 'date_fin_trait','nom_qr', 'nom_arr', 'coord_x', 
                 'coord_y', 'longitude', 'latitude'],
    'properties': {
        'no_declaration': {
            'type': 'number'
        },
        'date_declaration': {
            'type': 'date'
        },
        'date_insp_vispre': {
            'type': 'date'
        },
        'nbr_extermin': {
            'type': 'number'
        },
        'date_debut_trait': {
            'type': 'date'
        },
        'date_fin_trait': {
            'type': 'date'
        },
        'no_qr': {
            'type': 'string'
        },
        'nom_qr': {
            'type': 'string'
        },
        'nom_arr': {
            'type': 'string'
        },
        'coord_x': {
            'type': 'number'
        },
        'coord_y': {
            'type': 'number'
        },
        'longitude': {
            'type': 'number'
        },
        'latitude': {
            'type': 'number'
        }
    },
    'additionalProperties': False
}