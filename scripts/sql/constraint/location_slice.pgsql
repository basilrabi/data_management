ALTER TABLE location_slice
ADD CONSTRAINT closed_crest_line
CHECK ((layer <> 2) or ST_IsClosed(geom));
