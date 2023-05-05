from csv import DictReader
from decimal import Decimal
from django.core.exceptions import ObjectDoesNotExist
from pandas import melt, read_csv
from pathlib import Path
from re import search

from comptrollership.models import (
    GeneralLedgerAccount,
    MonthlyCost,
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
                if log != '':
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

def import_costs(csv_path: Path, year: int, enable_log: bool) -> None:
    """
    Imports the csv of a monthly cost data similar to
    http://datamanagement.tmc.nickelasia.com:81/static/TMC/AvB_2021.csv

    The following headers must be present:
    1. cost_center = MonthlyCost.cost_center
    2. gl = MonthlyCost.gl
    3x. aa n; where:
        aa %in% ['ac', 'ad', 'bu', 'fo']
        n %in% 1:13

    ac = MonthlyCost.actual
    ad = MonthlyCost.adjusted_budget
    bu = budget
    fo = forecast

    n = stands for the month number but it may include 13 which signifies the
        year-end adjustments
    """
    def insert_cost_data(row):
        updating = False
        try:
            cost = MonthlyCost.objects.get(
                year=int(year),
                month=int(row['month']),
                cost_center__name=row['cost_center'].strip(),
                gl__code=int(row['gl'])
            )
            updating = True
            log = f'Updating {cost} with '
        except ObjectDoesNotExist:
            try:
                cc = SapCostCenter.objects.get(name=row['cost_center'].strip())
            except ObjectDoesNotExist:
                log = f'Cost center {row["cost_center"]} does not exist.'
                if enable_log:
                    Log(log=log).save()
                else:
                    print(log)
                return
            try:
                gl = GeneralLedgerAccount.objects.get(code=int(row['gl']))
            except ObjectDoesNotExist:
                log = f'GL {row["gl"]} does not exist.'
                if enable_log:
                    Log(log=log).save()
                else:
                    print(log)
                return
            cost = MonthlyCost(
                year=int(year),
                month=int(row['month']),
                cost_center=cc,
                gl=gl
            )
            log = f'Adding cost {cost}.'

        updated = False

        if row['column'] == 'ac':
            if abs(cost.actual - Decimal(row['value'])) > 0.001:
                if updating:
                    updated = True
                cost.actual = Decimal(row['value'])
                log += f'\nactual={cost.actual:,.2f}'
        elif row['column'] == 'ad':
            if abs(cost.adjusted_budget - Decimal(row['value'])) > 0.001:
                if updating:
                    updated = True
                cost.adjusted_budget = Decimal(row['value'])
                log += f'\nadjusted_budget={cost.adjusted_budget:,.2f}'
        elif row['column'] == 'bu':
            if abs(cost.budget - Decimal(row['value'])) > 0.001:
                if updating:
                    updated = True
                cost.budget = Decimal(row['value'])
                log += f'\nbudget={cost.budget:,.2f}'
        elif row['column'] == 'fo':
            if abs(cost.forecast - Decimal(row['value'])) > 0.001:
                if updating:
                    updated = True
                cost.forecast = Decimal(row['value'])
                log += f'\nforecast={cost.forecast:,.2f}'
        else:
            log = 'Unknown column.'
            if enable_log:
                Log(log=log).save()
            else:
                print(log)
            return

        if updating:
            if updated:
                cost.save()
                if enable_log:
                    Log(log=log).save()
                else:
                    print(log)
        else:
            cost.save()
            if enable_log:
                Log(log=log).save()
            else:
                print(log)

    df = read_csv(csv_path)
    columns = ['cost_center', 'gl'] \
        + [f'ac {i}' for i in range(1, 14)] \
        + [f'ad {i}' for i in range(1, 14)] \
        + [f'bu {i}' for i in range(1, 14)] \
        + [f'fo {i}' for i in range(1, 14)]

    if not set(df.columns).issubset(set(columns)):
        log = 'Invalid columns detected during importation of cost data:'
        for invalid_column in (set(df.columns) - set(columns)):
            log += f' {invalid_column}'
        if enable_log:
            Log(log=log).save()
        else:
            print(log)
        return

    df = df[
        (df['cost_center'].str.contains('Total') == False) & \
        (df['cost_center'].str.contains('#') == False) & \
        (df['gl'].str.contains('Total') == False)
    ]
    df = melt(df, id_vars=['cost_center', 'gl'])
    df = df[(df['value'] != Decimal(0.00))]
    df = df.groupby(['cost_center', 'gl', 'variable'])['value'].sum()
    df = df.reset_index()
    df[['column', 'month']] = df.variable.str.split(' ', expand=True)
    df.apply(insert_cost_data, axis=1)

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
