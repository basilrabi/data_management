/* When a row is updated in organization_division, organization_department and
 * organization_section, a new row must also be added to
 * organization_organizationunit
 */

CREATE OR REPLACE FUNCTION update_organization_organizationunit()
RETURNS trigger AS
$BODY$
BEGIN
    IF (NEW.name ILIKE 'ind%' AND OLD.name NOT ILIKE 'ind%') THEN
        DELETE FROM organization_organizationunit
        WHERE uid = TG_ARGV[0] || OLD.id;
    ELSIF (NEW.name NOT ILIKE 'ind%' AND OLD.name ILIKE 'ind%') THEN
        INSERT INTO organization_organizationunit (uid, name, abbreviation)
        VALUES (TG_ARGV[0] || NEW.id, NEW.name, NEW.abbreviation);
    ELSE
        UPDATE organization_organizationunit
        SET name = NEW.name,
            abbreviation = NEW.abbreviation
        WHERE uid = TG_ARGV[0] || NEW.id;
    END IF;
    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION update_organization_organizationunit_section()
RETURNS trigger AS
$BODY$
BEGIN
    IF (NEW.name NOT ILIKE 'ind%' AND OLD.name ILIKE 'ind%') THEN
        DELETE FROM organization_organizationunit
        WHERE uid = 'section' || OLD.id;
    ELSIF (NEW.name ILIKE 'ind%' AND OLD.name NOT ILIKE 'ind%') THEN
        INSERT INTO organization_organizationunit (uid, name, abbreviation)
        VALUES ('section' || NEW.id, NEW.name, NEW.name);
    ELSE
        UPDATE organization_organizationunit
        SET name = NEW.name,
            abbreviation = NEW.name
        WHERE uid = 'section' || NEW.id;
    END IF;
    RETURN NEW;
END;
$BODY$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS organization_organizationunit_update_department
ON organization_department;
CREATE TRIGGER organization_organizationunit_update_department
AFTER UPDATE ON organization_department
FOR EACH ROW EXECUTE PROCEDURE update_organization_organizationunit('department');

DROP TRIGGER IF EXISTS organization_organizationunit_update_division
ON organization_division;
CREATE TRIGGER organization_organizationunit_update_division
AFTER UPDATE ON organization_division
FOR EACH ROW EXECUTE PROCEDURE update_organization_organizationunit('division');

DROP TRIGGER IF EXISTS organization_organizationunit_update_section
ON organization_section;
CREATE TRIGGER organization_organizationunit_update_section
AFTER UPDATE ON organization_section
FOR EACH ROW EXECUTE PROCEDURE update_organization_organizationunit_section();
