from csv import DictReader
from django.core.exceptions import ObjectDoesNotExist
from pathlib import Path

from comptrollership.models import GeneralLedgerAccount
from custom.models import Log

def import_gl_accounts(csv_path: Path, enable_log: bool) -> None:
    """
    Imports the csv of the general ledger account list with the headers: code
    and description.
    """
    with csv_path.open(newline='') as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            log = ''
            try:
                code = int(row['code'].strip())
            except ValueError:
                code = None
            except KeyboardInterrupt:
                log = 'Uploading GL Accounts interrupted.'
                if enable_log:
                    Log(log=log).save()
                else:
                    print(log)
                return

            if code:
                description = row['description'].strip()
                if description:
                    try:
                        gl = GeneralLedgerAccount.objects.get(code=code)
                    except ObjectDoesNotExist:
                        gl = None

                    if gl:
                        if description != gl.description:
                            log = f'Description of {gl.code} updated from {gl.description} to {description}.'
                            gl.description = description
                            gl.save()
                    else:
                        log = f'Added new GL {code}: {description}'
                        GeneralLedgerAccount(code=code, description=description).save()
                    if log != '':
                        if enable_log:
                            Log(log=log).save()
                        else:
                            print(log)
