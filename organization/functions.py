from django.db import connection

def refresh_organizationunit() -> None:
    """
    Refresh the view organizationunit.
    """
    with connection.cursor() as cursor:
        cursor.execute('REFRESH MATERIALIZED VIEW CONCURRENTLY organization_organizationunit')
