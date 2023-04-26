/* When a row is added in organization_division, organization_department or
 * organization_section, a new row must also be added to
 * organization_organizationunit
 */

CREATE OR REPLACE FUNCTION insert_organization_organizationunit()
RETURNS trigger AS
$BODY$
BEGIN
    IF (NEW.name NOT ILIKE 'ind%') THEN
        INSERT INTO organization_organizationunit (uid, name, abbreviation)
        VALUES (TG_ARGV[0] || NEW.id, NEW.name, NEW.abbreviation);
    END IF;
    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION insert_organization_organizationunit_section()
RETURNS trigger AS
$BODY$
BEGIN
    IF (NEW.name NOT ILIKE 'ind%') THEN
        INSERT INTO organization_organizationunit (uid, name, abbreviation)
        VALUES ('section' || NEW.id, NEW.name, NEW.name);
    END IF;
    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS organization_organizationunit_insert_department
ON organization_department;
CREATE TRIGGER organization_organizationunit_insert_department
AFTER INSERT ON organization_department
FOR EACH ROW EXECUTE PROCEDURE insert_organization_organizationunit('department');

DROP TRIGGER IF EXISTS organization_organizationunit_insert_division
ON organization_division;
CREATE TRIGGER organization_organizationunit_insert_division
AFTER INSERT ON organization_division
FOR EACH ROW EXECUTE PROCEDURE insert_organization_organizationunit('division');

DROP TRIGGER IF EXISTS organization_organizationunit_insert_section
ON organization_section;
CREATE TRIGGER organization_organizationunit_insert_section
AFTER INSERT ON organization_section
FOR EACH ROW EXECUTE PROCEDURE insert_organization_organizationunit_section();
