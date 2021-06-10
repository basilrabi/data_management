# pylint: disable=import-error
# pylint: disable=no-member

from sys import exit

from shipment.models.dso import LayDaysStatement

for statement in LayDaysStatement.objects.all():
    try:
        print(f'Computing statement for {statement.__str__()}...', flush=True)
        statement._compute()
    except KeyboardInterrupt:
        print('\nComputing statement interrupted.', flush=True)
        exit(1)
    print('Done.', flush=True)
