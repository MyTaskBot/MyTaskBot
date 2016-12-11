--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: list_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE list_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.list_id_seq OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: List; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "List" (
    id integer DEFAULT nextval('list_id_seq'::regclass) NOT NULL,
    name character varying(255),
    "user" integer
);


ALTER TABLE public."List" OWNER TO postgres;

--
-- Name: target_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE target_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.target_id_seq OWNER TO postgres;

--
-- Name: Target; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "Target" (
    id integer DEFAULT nextval('target_id_seq'::regclass) NOT NULL,
    text character varying(1000),
    list integer,
    user_t integer,
    is_deleted smallint DEFAULT 0
);


ALTER TABLE public."Target" OWNER TO postgres;

--
-- Name: task_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE task_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.task_id_seq OWNER TO postgres;

--
-- Name: Task; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "Task" (
    id integer DEFAULT nextval('task_id_seq'::regclass) NOT NULL,
    list integer,
    user_t integer,
    text character varying(1000),
    "time" character varying(100),
    repeat integer,
    is_done smallint DEFAULT 0,
    is_deleted smallint DEFAULT 0
);


ALTER TABLE public."Task" OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO postgres;

--
-- Name: User; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE "User" (
    id integer DEFAULT nextval('user_id_seq'::regclass) NOT NULL,
    chat integer,
    name character varying(255),
    user_id smallint
);


ALTER TABLE public."User" OWNER TO postgres;

--
-- Data for Name: List; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "List" (id, name, "user") FROM stdin;
\.


--
-- Data for Name: Target; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "Target" (id, text, list, user_t, is_deleted) FROM stdin;
2731403	sdds	\N	\N	0
1	Ggfty	\N	273143403	0
2	Dtudf	\N	273143403	0
3	Dhdg	\N	273143403	0
4	тестовое1	\N	32208604	0
5	12344	\N	32208604	0
6	43343	\N	32208604	0
7	7889999	\N	32208604	0
8	цель!	\N	206759060	0
\.


--
-- Data for Name: Task; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "Task" (id, list, user_t, text, "time", repeat, is_done, is_deleted) FROM stdin;
1	\N	32208604	test1	2016-12-04 23:15:00	\N	0	0
2	\N	32208604	test2	2016-12-04 23:19:00	\N	0	0
3	\N	206759060	сделать то-то и то-то	2016-12-12 04:20:00	\N	0	0
4	\N	206759060	таск	2016-12-05 01:15:00	\N	0	0
\.


--
-- Data for Name: User; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY "User" (id, chat, name, user_id) FROM stdin;
1	13	igor	\N
2	32208604	Igor	\N
4	273143403	Svyatoslav	\N
5	206759060	Serebrennikova	\N
\.


--
-- Name: list_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('list_id_seq', 1, false);


--
-- Name: target_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('target_id_seq', 8, true);


--
-- Name: task_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('task_id_seq', 4, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('user_id_seq', 5, true);


--
-- Name: List_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "List"
    ADD CONSTRAINT "List_pkey" PRIMARY KEY (id);


--
-- Name: pk; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "Task"
    ADD CONSTRAINT pk PRIMARY KEY (id);


--
-- Name: pk_id; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "User"
    ADD CONSTRAINT pk_id PRIMARY KEY (id);


--
-- Name: pk_target; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY "Target"
    ADD CONSTRAINT pk_target PRIMARY KEY (id);


--
-- Name: fki_user; Type: INDEX; Schema: public; Owner: postgres; Tablespace: 
--

CREATE INDEX fki_user ON "List" USING btree ("user");


--
-- Name: fk_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY "List"
    ADD CONSTRAINT fk_user FOREIGN KEY ("user") REFERENCES "User"(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

