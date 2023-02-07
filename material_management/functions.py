from csv import DictReader
from pathlib import Path

from comptrollership.models import GeneralLedgerAccount
from custom.models import Log
from material_management.models import (
    Material,
    MaterialGroup,
    MaterialType,
    UnitOfMeasure,
    Valuation
)


def import_material(csv_path: Path, enable_log: bool) -> None:
    """
    Imports the file with the exact column names in http://datamanagement.tmc.nickelasia.com:81/static/TMC/material.csv
    """
    with csv_path.open(newline='') as csvfile:
        reader = DictReader(csvfile)
        for row in reader:

            # Check Valuation first
            try:
                valuation_name = int(row['valuation'])
            except ValueError:
                valuation_name = None

            valuation = None
            if valuation_name:
                try:
                    gl = GeneralLedgerAccount.objects.get(code=int(row['gl mapping']))
                except Exception as e:
                    log = f'Exception:\nGL {row["gl mapping"]}\n{e}'
                    if enable_log:
                        Log(log=log).save()
                    else:
                        print(log)
                    return
                valuation = Valuation.objects.filter(name=valuation_name)

                if not valuation.exists():
                    valuation = Valuation(
                        name=int(row['valuation']),
                        description=row['valuation class'],
                        gl=gl
                    )
                    try:
                        valuation.clean()
                        valuation.save()
                        log = f'valuation {valuation} added.'
                        if enable_log:
                            Log(log=log).save()
                        else:
                            print(log)
                    except KeyboardInterrupt:
                        log = 'Uploading materials interrupted.'
                        if enable_log:
                            Log(log=log).save()
                        else:
                            print(log)
                        return
                    except Exception as e:
                        log = f'Valuation {valuation} was not saved.\n{e}'
                        if enable_log:
                            Log(log=log).save()
                        else:
                            print(log)
                        return
                else:
                    valuation = valuation.first()
                    for_update = False
                    log = []
                    if valuation.gl != gl:
                        log += [f'Valuation {valuation} GL mapping to be updated from {valuation.gl} to {gl}.']
                        valuation.gl = gl
                        for_update = True
                    if valuation.description != row['valuation class']:
                        log += [f'Valuation {valuation} description to be updated from {valuation.description} to {row["valuation class"]}.']
                        valuation.description = row['valuation class']
                        for_update = True
                    if for_update:
                        try:
                            valuation.clean()
                            valuation.save()
                            log += [f'Valuation {valuation} updated.']
                            if enable_log:
                                Log(log='\n'.join(log)).save()
                            else:
                                print('\n'.join(log))
                        except KeyboardInterrupt:
                            log = 'Uploading materials interrupted.'
                            if enable_log:
                                Log(log=log).save()
                            else:
                                print(log)
                            return
                        except Exception as e:
                            log = f'Valuation {valuation} was not updated.\n{e}'
                            if enable_log:
                                Log(log=log).save()
                            else:
                                print(log)
                            return
                valuation.refresh_from_db()

            try:
                material_type = MaterialType.objects.get(name=row['material type'])
                unit_of_measure = UnitOfMeasure.objects.get(unit=row['unit of measure'])
                material_group = None
                if row['material group'] and row['material group'] != '#N/A':
                    material_group = MaterialGroup.objects.get(name=row['material group'])
            except Exception as e:
                log = f'TYPE: {row["material type"]}\nUOM: {row["unit of measure"]}\nGROUP: {row["material group"]}\n{e}'
                if enable_log:
                    Log(log=log).save()
                else:
                    print(log)
                return

            material = Material.objects.filter(name=row['material'])
            if not material.exists():
                material = Material(
                    name=row['material'],
                    description=row['description'],
                    type=material_type,
                    group=material_group,
                    unit_of_measure=unit_of_measure,
                    part_number=row['part number'] or None,
                    valuation=valuation
                )
                try:
                    material.clean()
                    material.save()
                    log = f'Material {material} added.'
                    if enable_log:
                        Log(log=log).save()
                    else:
                        print(log)
                except KeyboardInterrupt:
                    log = 'Uploading materials interrupted.'
                    if enable_log:
                        Log(log=log).save()
                    else:
                        print(log)
                    return
                except Exception as e:
                    log = f'Material {material} was not saved.\n{e}'
                    if enable_log:
                        Log(log=log).save()
                    else:
                        print(log)
                    return
            else:
                material = material.first()
                for_update = False
                log = []
                if material.description != row['description']:
                    log += [f'Material {material} description to be updated from {material.description} to {row["description"]}.']
                    material.description = row['description']
                    for_update = True
                if material.part_number != (row['part number'] or None):
                    log += [f'Material {material} part number to be updated from {material.part_number} to {row["part number"]}.']
                    material.part_number = row['part number'] or None
                    for_update = True
                if material.type != material_type:
                    log += [f'Material {material} material_type to be updated from {material.type} to {material_type}.']
                    material.type = material_type
                    for_update = True
                if material.group != material_group:
                    log += [f'Material {material} material_group to be updated from {material.group} to {material_group}.']
                    material.group = material_group
                    for_update = True
                if for_update:
                    material.save()
                    log += ['Material {material} updated.']
                    if enable_log:
                        Log(log='\n'.join(log)).save()
                    else:
                        print('\n'.join(log))
                else:
                    print(f'Skipping {row["description"]}.')
