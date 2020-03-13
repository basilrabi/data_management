--
-- PostgreSQL database dump
--

-- Dumped from database version 11.7 (Debian 11.7-2.pgdg100+1)
-- Dumped by pg_dump version 11.7

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: topography; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA topography;


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';


--
-- Name: postgis_sfcgal; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis_sfcgal WITH SCHEMA public;


--
-- Name: EXTENSION postgis_sfcgal; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION postgis_sfcgal IS 'PostGIS SFCGAL functions';


--
-- Name: end_2016_id_seq; Type: SEQUENCE; Schema: topography; Owner: -
--

CREATE SEQUENCE topography.end_2016_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: end_2016; Type: TABLE; Schema: topography; Owner: -
--

CREATE TABLE topography.end_2016 (
    id integer DEFAULT nextval('topography.end_2016_id_seq'::regclass) NOT NULL,
    ridge character(2),
    geom public.geometry(PolygonZ,3125)
);


--
-- Name: end_2017_id_seq; Type: SEQUENCE; Schema: topography; Owner: -
--

CREATE SEQUENCE topography.end_2017_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: end_2017; Type: TABLE; Schema: topography; Owner: -
--

CREATE TABLE topography.end_2017 (
    id integer DEFAULT nextval('topography.end_2017_id_seq'::regclass) NOT NULL,
    ridge character(2),
    geom public.geometry(PolygonZ,3125)
);


--
-- Name: end_2018_id_seq; Type: SEQUENCE; Schema: topography; Owner: -
--

CREATE SEQUENCE topography.end_2018_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: end_2018; Type: TABLE; Schema: topography; Owner: -
--

CREATE TABLE topography.end_2018 (
    id integer DEFAULT nextval('topography.end_2018_id_seq'::regclass) NOT NULL,
    ridge character(2),
    geom public.geometry(PolygonZ,3125)
);


--
-- Name: end_2019_id_seq; Type: SEQUENCE; Schema: topography; Owner: -
--

CREATE SEQUENCE topography.end_2019_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: end_2019; Type: TABLE; Schema: topography; Owner: -
--

CREATE TABLE topography.end_2019 (
    id integer DEFAULT nextval('topography.end_2019_id_seq'::regclass) NOT NULL,
    geom public.geometry(PolygonZ,3125)
);


--
-- Name: green_id_seq; Type: SEQUENCE; Schema: topography; Owner: -
--

CREATE SEQUENCE topography.green_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: green; Type: TABLE; Schema: topography; Owner: -
--

CREATE TABLE topography.green (
    id integer DEFAULT nextval('topography.green_id_seq'::regclass) NOT NULL,
    geom public.geometry(PolygonZ,3125),
    ridge character(2)
);


--
-- Name: green_union; Type: TABLE; Schema: topography; Owner: -
--

CREATE TABLE topography.green_union (
    ridge character(2) NOT NULL,
    geom public.geometry(Polygon,3125)
);


--
-- Name: end_2016 topo_end_2016_pkey; Type: CONSTRAINT; Schema: topography; Owner: -
--

ALTER TABLE ONLY topography.end_2016
    ADD CONSTRAINT topo_end_2016_pkey PRIMARY KEY (id);


--
-- Name: end_2017 topo_end_2017_pkey; Type: CONSTRAINT; Schema: topography; Owner: -
--

ALTER TABLE ONLY topography.end_2017
    ADD CONSTRAINT topo_end_2017_pkey PRIMARY KEY (id);


--
-- Name: end_2018 topo_end_2018_pkey; Type: CONSTRAINT; Schema: topography; Owner: -
--

ALTER TABLE ONLY topography.end_2018
    ADD CONSTRAINT topo_end_2018_pkey PRIMARY KEY (id);


--
-- Name: end_2019 topo_end_2019_pkey; Type: CONSTRAINT; Schema: topography; Owner: -
--

ALTER TABLE ONLY topography.end_2019
    ADD CONSTRAINT topo_end_2019_pkey PRIMARY KEY (id);


--
-- Name: green topo_green_pkey; Type: CONSTRAINT; Schema: topography; Owner: -
--

ALTER TABLE ONLY topography.green
    ADD CONSTRAINT topo_green_pkey PRIMARY KEY (id);


--
-- Name: green_union topo_green_union_pkey; Type: CONSTRAINT; Schema: topography; Owner: -
--

ALTER TABLE ONLY topography.green_union
    ADD CONSTRAINT topo_green_union_pkey PRIMARY KEY (ridge);


--
-- Name: end_2016_gix; Type: INDEX; Schema: topography; Owner: -
--

CREATE INDEX end_2016_gix ON topography.end_2016 USING gist (geom) WITH (fillfactor='100');

ALTER TABLE topography.end_2016 CLUSTER ON end_2016_gix;


--
-- Name: end_2017_gix; Type: INDEX; Schema: topography; Owner: -
--

CREATE INDEX end_2017_gix ON topography.end_2017 USING gist (geom) WITH (fillfactor='100');

ALTER TABLE topography.end_2017 CLUSTER ON end_2017_gix;


--
-- Name: end_2018_gix; Type: INDEX; Schema: topography; Owner: -
--

CREATE INDEX end_2018_gix ON topography.end_2018 USING gist (geom) WITH (fillfactor='100');

ALTER TABLE topography.end_2018 CLUSTER ON end_2018_gix;


--
-- Name: end_2019_gix; Type: INDEX; Schema: topography; Owner: -
--

CREATE INDEX end_2019_gix ON topography.end_2019 USING gist (geom) WITH (fillfactor='100');

ALTER TABLE topography.end_2019 CLUSTER ON end_2019_gix;


--
-- Name: green_gix; Type: INDEX; Schema: topography; Owner: -
--

CREATE INDEX green_gix ON topography.green USING gist (geom) WITH (fillfactor='100');

ALTER TABLE topography.green CLUSTER ON green_gix;


--
-- PostgreSQL database dump complete
--

