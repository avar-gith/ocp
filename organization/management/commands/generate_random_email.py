# file: jira/management/commands/generate_random_email.py

import random
from django.core.management.base import BaseCommand
from jira.models import Employee, Task, Sprint  # Importáld a szükséges modelleket
from office.models import Email  # Az Email modellt innen importáljuk
from django.utils import timezone

class Command(BaseCommand):
    help = 'Generál egy véletlenszerű e-mailt különböző feltételek szerint.'

    def handle(self, *args, **options):
        # Kiválasztunk egy véletlenszerű felhasználót, aki nem 1-es
        employees = Employee.objects.exclude(id=1)
        if not employees.exists():
            self.stderr.write(self.style.ERROR('Nincs elérhető felhasználó.'))
            return
        
        current_employee = random.choice(employees)

        # Dobunk egy kockával
        dice_roll = random.randint(1, 6)

        if dice_roll in [1, 2, 3]:
            # 1-3: Új e-mail egy saját feladatáról
            tasks = Task.objects.filter(creator=current_employee)
            if not tasks.exists():
                email_content = f'Szia {current_employee.name},\n\nNincs aktív feladatod.\n\nÜdvözlettel!'
            else:
                task = random.choice(tasks)
                email_content = f'Szia {current_employee.name},\n\nA feladatom: {task.name}. További részletek: {task.description}.\n\nÜdvözlettel!'

            # E-mail mentése
            new_email = Email(
                sender=current_employee,
                subject='Új feladatom',
                sent_at=timezone.now(),
                content=email_content
            )
            new_email.save()

        elif dice_roll == 4:
            # 4: Válasszunk ki egy feladatot és zárjuk le
            tasks = Task.objects.filter(creator=current_employee)
            if tasks.exists():
                task = random.choice(tasks)
                task.status = 'completed'
                task.save()

        elif dice_roll == 5:
            # 5: Válasszunk ki egy másik felhasználót és írjunk neki kedves levelet
            other_employees = employees.exclude(id=current_employee.id)
            if not other_employees.exists():
                self.stderr.write(self.style.ERROR('Nincs elérhető másik felhasználó.'))
                return
            
            other_employee = random.choice(other_employees)
            email_content = f'Szia {other_employee.name},\n\nCsak szeretném megköszönni a kitartó munkádat!\n\nÜdvözlettel!'
            new_email = Email(
                sender=current_employee,
                subject='Kedves üzenet',
                sent_at=timezone.now(),
                content=email_content
            )
            new_email.save()

        elif dice_roll == 6:
            # 6: Válasszunk ki egy feladatot és írjunk róla egy eszkalációt
            tasks = Task.objects.filter(creator=current_employee)
            if not tasks.exists():
                self.stderr.write(self.style.ERROR('Nincs elérhető feladat az eszkalációhoz.'))
                return
            
            task = random.choice(tasks)
            task.status = 'escalation'
            task.save()
            
            email_content = f'Szia {current_employee.name},\n\nAz alábbi feladatom eszkalációra került: {task.name}. Kérlek, vedd figyelembe.\n\nÜdvözlettel!'
            new_email = Email(
                sender=current_employee,
                subject='Feladat eszkaláció',
                sent_at=timezone.now(),
                content=email_content
            )
            new_email.save()

        self.stdout.write(self.style.SUCCESS('Random e-mail sikeresen generálva és elmentve az adatbázisba.'))
