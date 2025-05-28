from flask import current_app

def allowed_file(filename):
    """
    Comprueba que el nombre de archivo tiene una extensión permitida
    según current_app.config['ALLOWED_EXTENSIONS'].
    """
    return (
        filename
        and '.' in filename
        and filename.rsplit('.', 1)[1].lower()
        in current_app.config['ALLOWED_EXTENSIONS']
    )
