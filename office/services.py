# file: office/services.py

from .models import Email

def send_mail(sender, project_name, content, subject_prefix):
    """
    E-mail küldése imitálva.
    
    :param sender: Az e-mail küldője (Employee objektum).
    :param project_name: A projekt neve, amelyhez az e-mail tartozik.
    :param content: Az e-mail tartalma.
    :param subject_prefix: A tárgy prefixe, amely meghatározza a levél típusát.
    :return: Az elküldött e-mail objektum.
    """
    subject = f'{subject_prefix}: {project_name}'  # Tárgy generálása a prefix alapján
    # E-mail objektum létrehozása
    email = Email(
        sender=sender,
        subject=subject,
        content=content
    )
    # E-mail mentése az adatbázisba
    email.save()

    # Itt imitálhatjuk az e-mail küldését, pl. log üzenet
    print(f'E-mail küldve: {subject} (Küldő: {sender.name})')

    return email
