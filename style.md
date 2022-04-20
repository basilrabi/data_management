# Coding Style

## Python

1. One indentation level is 4 characters.
1. Operators must have 1 space at both left and right sides.
1. The equal sign in a function or object initializer used in argument assigning is not an operator thus it must not have spaces at both left and right side.

### Classes

1. Separate each class definition by 2 empty lines.
1. Separate method definition by 1 empty line.
1. Member order:
    1. Attributes
    1. Methods (alphabetical)
    1. Class Meta (alphabetical)
    1. `__str__()` definition
1. Classes are to be defined in alphabetical order.
    1. In the case of classes definition in an admin module, the following sort-order is applied then alphabetical
        1. import_export.resources.ModelResource derived classes
        1. django.forms.models.BaseInlineFormSet derived classes
        1. AdminInlines derived classes
        1. Parent Admin derived classes

#### Django Admin Classes

For `django.contrib.admin.ModelAdmin` sub-classes, registration is done using the `@register` decorator before the class declaration.

### Delimeters and Contents Spanning Multiple Lines

1. If the content of the delimeter has multiple elements and the line exceeds 80 characters, each element should be on its separate line.
1. If the delimeters are placed on separate lines from the contents:
    1. The opening delimeter and the closing delimeter must be on the same indentation level.
    1. The contents must be indented one more level from the delimeters
1. The content items may be placed on the same line as the delimters if the lines with the delimters do not exceed 80 characters.

```python3
class SomeClass:
    class AnotherClass:

        supervisor = ForeignKey(
            Person,
            on_delete=SET_NULL,
            null=True,
            blank=True,
            related_name='supervisedminingsamplereport'
        )

        wmt = DecimalField(
            'WMT', null=True, blank=True, max_digits=8, decimal_places=3
        )

        trips = TripsPerPile(piling_method=method,
                             effectivity=pd('2019-01-01'),
                             trips=10)
```

### Importation

1. Avoid implicit importation (_e.g._ `from django.contrib import admin` then using `admin.TabularInline`)
1. Explicitly import the Class/objects to be used whenever possible (_e.g._ `from django.contrib.admin import TabularInline`)
1. Limit each line to 80 characters
1. Separate import groups in the following order with each group arranged in alphabetical order:
    1. Direct module import
    1. Importing Class or objects from external modules
    1. Importing Class or objects from internal modules
1. Each import group must be separated by 1 empty line
1. Internal modules starting with `.` must be placed at the last lines
1. When using delimeters (parenthesis), each class/object must be on its own line.

```python3
import ezdxf

from django.http import FileResponse
from tempfile import TemporaryDirectory

from custom.functions import export_sql
from .models.landuse import (
    Facility,
    FacilityClassification,
    FLA,
    MPSA,
    PEZA,
    RoadArea,
    WaterBody
)
```

## PGSQL

1. One indentation level is 4 characters.
1. Use `:=` for assignment while `=` to check for equality.
1. Each clause of a query shall in a separate line.
1. Limit identifiers to 63 characters.

### Comments

1. All comments shall not exceed 80 character per line.
1. If comments are less than 3 lines, use `--` on each line.
1. If comments are more than 2 lines, use

### Identifiers

1. Custom  identifiers shall be in small letters with words separated by underscore
1. Built-in identifiers shall be in capital letters
1. Avoid meaningless identifiers except for using table alias.

### Permissions

1. The permissions file of one role shall be on its own file.
1. The grant permissions shall be grouped in the following order:
    1. Granting role to a role
    1. Granting permission on a schema
    1. Granting permission on a table
    1. Granting permission on a sequence
1. Permissions shall be arranged in alphabetical order.
1. Each privilege type and group shall be separated by 1 line
1. For each grouped permissions with the same privilege type, align all clauses.
1. Each update privilege of a column shall be on its own line and ordered by table first then by columns.

## R and C++

## Identifiers

| Type      | Style      |
| --------- | ---------- |
| Classes   | CamelCase  |
| Functions | camelCase  |
| Methods   | camelCase  |
| Objects   | camel_case |
