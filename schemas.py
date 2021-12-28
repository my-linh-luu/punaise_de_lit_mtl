declaration_insert_schema = {
    'type': 'object',
    'required': ['quartier', 'arrondissement', 'adresse', 'dateVisite', 'nom',
                 'prenom', 'description'],
    'properties': {
        'quartier': {
            'type': 'string'
        },
        'arrondissement': {
            'type': 'string'
        },
        'adresse': {
            'type':'string'
        },
        'dateVisite': {
            'type': 'string'
        },
        'nom': {
            'type': 'string'
        },
        'prenom': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        }
    },
    'additionalProperties': False
}

user_insert_schema = {
    'type': 'object',
    'required': ['utilisateur', 'courriel', 'quartiers_a_surveiller',
                 'mot_de_passe'],
    'properties': {
        'utilisateur': {
            'type': 'string'
        },
        'courriel': {
            'type': 'string'
        },
        'quartiers_a_surveiller': {
            'type': 'string'
        },
        'mot_de_passe': {
            'type': 'string'
        }
    },
    'additionalProperties': False
}
