ALTER TABLE location_slice
ADD CONSTRAINT valid_closed_crest_line
CHECK (
    (layer <> 2)
    OR (
        ST_IsClosed(geom)
            AND ST_IsValid(ST_MakePolygon(ST_Force2D(geom)))
    )
);
