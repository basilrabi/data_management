from csv import DictReader
from django.core.exceptions import ObjectDoesNotExist
from pathlib import Path
from re import search

from comptrollership.models import (
    GeneralLedgerAccount,
    ProfitCenter,
    SapCostCenter
)
from custom.models import Log

def import_cost_centers(csv_path: Path, enable_log: bool) -> None:
    """
    Imports the csv of the cost center list with the headers: name, long_name,
    description, and profit_center.
    """
    with csv_path.open(newline='') as csvfile:
        reader = DictReader(csvfile)
        profit_center_pattern = r'^(.*?)\s*\((.*?)\)$'
        for row in reader:
            regex = search(profit_center_pattern, row['profit_center'].strip())
            log = ''
            try:
                if regex:
                    try:
                        profit_center = ProfitCenter.objects.get(name=regex.group(1))
                        if profit_center.description != regex.group(2):
                            log += f'Description of profit center {profit_center} updated from {profit_center.description} to {regex.group(2)}.\n'
                            profit_center.description = regex.group(2)
                            profit_center.save()
                            profit_center.refresh_from_db()
                    except ObjectDoesNotExist:
                        log += f'Added new profit center: {regex.group(1)}\n'
                        profit_center = ProfitCenter(name=regex.group(1), description=regex.group(2))
                        profit_center.save()
                        profit_center.refresh_from_db()
                else:
                    continue

                cc_description = row['description'].strip()
                cc_long_name = row['long_name'].strip()
                cc_name = row['name'].strip()

                try:
                    cost_center = SapCostCenter.objects.get(name=cc_name)
                except ObjectDoesNotExist:
                    cost_center = None
                if cost_center:
                    if cost_center.description != cc_description:
                        log += f'Description of cost center {cost_center.name} updated from {cost_center.description} to {cc_description}.\n'
                        cost_center.description = cc_description
                        cost_center.save()
                    if cost_center.long_name != cc_long_name:
                        log += f'Long name of cost center {cost_center.name} updated from {cost_center.long_name} to {cc_long_name}.\n'
                        cost_center.long_name = cc_long_name
                        cost_center.save()
                    if cost_center.profit_center != profit_center:
                        log += f'Profit center of cost center {cost_center.name} updated from {cost_center.profit_center} to {profit_center}.\n'
                        cost_center.profit_center = profit_center
                        cost_center.save()
                else:
                    log += f'Added new cost center: {cc_name}\n'
                    SapCostCenter(
                        name=cc_name,
                        long_name=cc_long_name,
                        description=cc_description,
                        profit_center=profit_center
                    ).save()
                if enable_log:
                    Log(log=log).save()
                else:
                    print(log)
            except KeyboardInterrupt:
                log = 'Uploading cost centers interrupted.'
                if enable_log:
                    Log(log=log).save()
                else:
                    print(log)
                return

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
