# class Hotel_filters():
def normalize_path_params(cidade=None, estrelas_min=0, estrelas_max=5, diaria_min=0, diaria_max=10000, limit=50, offset=0, **kwargs):
    result = {
        "cidade": cidade,
        "estrelas_min": estrelas_min,
        "estrelas_max": estrelas_max,
        "diaria_min": diaria_min,
        "diaria_max": diaria_max,
        "limit": limit,
        "offset": offset
    }
    if cidade is None:
        del(result['cidade'])

    return result


def create_sql(**kwargs):
    if kwargs.get('cidade') is None:
        return "SELECT * FROM hoteis \
                WHERE (estrelas >= ? AND estrelas <= ?)\
                    AND (diaria > ? AND diaria <= ?)\
                        LIMIT ? OFFSET ?"
    return "SELECT * FROM hoteis \
                WHERE cidade = ?\
                    AND (estrelas >= ? AND estrelas <= ?)\
                    AND (diaria > ? AND diaria <= ?)\
                        LIMIT ? OFFSET ?"
