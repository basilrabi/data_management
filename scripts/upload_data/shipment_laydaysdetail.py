# pylint: disable=import-error
# pylint: disable=no-member

import sys
from shipment.models.dso import LayDaysStatement

for statement in LayDaysStatement.objects.all():
    try:
        print(f'Computing statement for {statement.__str__()}...')
        statement._compute()
    except KeyboardInterrupt:
        print('\nComputing statement interrupted.')
        sys.exit(1)
    print('Done.')
    sys.stdout.flush()
    sys.stderr.flush()
