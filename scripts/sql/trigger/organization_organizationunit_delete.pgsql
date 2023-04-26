/* When a row is deleted in organization_division, organization_department or
 * organization_section, the a corresponding row must also be added in
 * organization_organizationunit
 */

CREATE OR REPLACE FUNCTION delete_organization_organizationunit()
RETURNS trigger AS
$BODY$
BEGIN
    IF (OLD.name NOT ILIKE 'ind%') THEN
        DELETE FROM organization_organizationunit
        WHERE uid = TG_ARGV[0] || OLD.id;
    END IF;
    RETURN OLD;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS organization_organizationunit_delete_department
ON organization_department;
CREATE TRIGGER organization_organizationunit_delete_department
AFTER DELETE ON organization_department
FOR EACH ROW EXECUTE PROCEDURE delete_organization_organizationunit('department');

DROP TRIGGER IF EXISTS organization_organizationunit_delete_division
ON organization_division;
CREATE TRIGGER organization_organizationunit_delete_division
AFTER DELETE ON organization_division
FOR EACH ROW EXECUTE PROCEDURE delete_organization_organizationunit('division');

DROP TRIGGER IF EXISTS organization_organizationunit_delete_section
ON organization_section;
CREATE TRIGGER organization_organizationunit_delete_section
AFTER DELETE ON organization_section
FOR EACH ROW EXECUTE PROCEDURE delete_organization_organizationunit('section');
