--
-- PostgreSQL database dump
--

\restrict HuhnreCxKSct0DDBhNMz3zaSLdHM5Kr7efWOETyCs3jiyzPw5eVcEqjBSXc3VgY

-- Dumped from database version 14.19 (Ubuntu 14.19-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.19 (Ubuntu 14.19-0ubuntu0.22.04.1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: nilai_siswa; Type: TABLE; Schema: public; Owner: admin_smkn1
--

CREATE TABLE public.nilai_siswa (
    id integer NOT NULL,
    siswa_id integer,
    matematika numeric(4,2),
    bahasa_indonesia numeric(4,2),
    bahasa_inggris numeric(4,2),
    kejuruan numeric(4,2),
    semester integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.nilai_siswa OWNER TO admin_smkn1;

--
-- Name: nilai_siswa_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_smkn1
--

CREATE SEQUENCE public.nilai_siswa_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.nilai_siswa_id_seq OWNER TO admin_smkn1;

--
-- Name: nilai_siswa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_smkn1
--

ALTER SEQUENCE public.nilai_siswa_id_seq OWNED BY public.nilai_siswa.id;


--
-- Name: prediksi_kelulusan; Type: TABLE; Schema: public; Owner: admin_smkn1
--

CREATE TABLE public.prediksi_kelulusan (
    id integer NOT NULL,
    siswa_id integer,
    status_prediksi character varying(20),
    confidence numeric(5,4),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.prediksi_kelulusan OWNER TO admin_smkn1;

--
-- Name: prediksi_kelulusan_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_smkn1
--

CREATE SEQUENCE public.prediksi_kelulusan_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.prediksi_kelulusan_id_seq OWNER TO admin_smkn1;

--
-- Name: prediksi_kelulusan_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_smkn1
--

ALTER SEQUENCE public.prediksi_kelulusan_id_seq OWNED BY public.prediksi_kelulusan.id;


--
-- Name: siswa; Type: TABLE; Schema: public; Owner: admin_smkn1
--

CREATE TABLE public.siswa (
    id integer NOT NULL,
    nis character varying(20) NOT NULL,
    nama character varying(100) NOT NULL,
    kelas character varying(10) NOT NULL,
    jurusan character varying(50) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.siswa OWNER TO admin_smkn1;

--
-- Name: siswa_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_smkn1
--

CREATE SEQUENCE public.siswa_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.siswa_id_seq OWNER TO admin_smkn1;

--
-- Name: siswa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_smkn1
--

ALTER SEQUENCE public.siswa_id_seq OWNED BY public.siswa.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: admin_smkn1
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(255) NOT NULL,
    role character varying(20) DEFAULT 'user'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.users OWNER TO admin_smkn1;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_smkn1
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO admin_smkn1;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_smkn1
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: nilai_siswa id; Type: DEFAULT; Schema: public; Owner: admin_smkn1
--

ALTER TABLE ONLY public.nilai_siswa ALTER COLUMN id SET DEFAULT nextval('public.nilai_siswa_id_seq'::regclass);


--
-- Name: prediksi_kelulusan id; Type: DEFAULT; Schema: public; Owner: admin_smkn1
--

ALTER TABLE ONLY public.prediksi_kelulusan ALTER COLUMN id SET DEFAULT nextval('public.prediksi_kelulusan_id_seq'::regclass);


--
-- Name: siswa id; Type: DEFAULT; Schema: public; Owner: admin_smkn1
--

ALTER TABLE ONLY public.siswa ALTER COLUMN id SET DEFAULT nextval('public.siswa_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: admin_smkn1
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: nilai_siswa; Type: TABLE DATA; Schema: public; Owner: admin_smkn1
--

COPY public.nilai_siswa (id, siswa_id, matematika, bahasa_indonesia, bahasa_inggris, kejuruan, semester, created_at) FROM stdin;
\.


--
-- Data for Name: prediksi_kelulusan; Type: TABLE DATA; Schema: public; Owner: admin_smkn1
--

COPY public.prediksi_kelulusan (id, siswa_id, status_prediksi, confidence, created_at) FROM stdin;
\.


--
-- Data for Name: siswa; Type: TABLE DATA; Schema: public; Owner: admin_smkn1
--

COPY public.siswa (id, nis, nama, kelas, jurusan, created_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: admin_smkn1
--

COPY public.users (id, username, password, role, created_at) FROM stdin;
1	admin	admin123	admin	2025-10-08 11:38:18.506051
\.


--
-- Name: nilai_siswa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_smkn1
--

SELECT pg_catalog.setval('public.nilai_siswa_id_seq', 1, false);


--
-- Name: prediksi_kelulusan_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_smkn1
--

SELECT pg_catalog.setval('public.prediksi_kelulusan_id_seq', 1, false);


--
-- Name: siswa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_smkn1
--

SELECT pg_catalog.setval('public.siswa_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_smkn1
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- Name: nilai_siswa nilai_siswa_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_smkn1
--

ALTER TABLE ONLY public.nilai_siswa
    ADD CONSTRAINT nilai_siswa_pkey PRIMARY KEY (id);


--
-- Name: prediksi_kelulusan prediksi_kelulusan_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_smkn1
--

ALTER TABLE ONLY public.prediksi_kelulusan
    ADD CONSTRAINT prediksi_kelulusan_pkey PRIMARY KEY (id);


--
-- Name: siswa siswa_nis_key; Type: CONSTRAINT; Schema: public; Owner: admin_smkn1
--

ALTER TABLE ONLY public.siswa
    ADD CONSTRAINT siswa_nis_key UNIQUE (nis);


--
-- Name: siswa siswa_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_smkn1
--

ALTER TABLE ONLY public.siswa
    ADD CONSTRAINT siswa_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_smkn1
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: admin_smkn1
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: nilai_siswa nilai_siswa_siswa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_smkn1
--

ALTER TABLE ONLY public.nilai_siswa
    ADD CONSTRAINT nilai_siswa_siswa_id_fkey FOREIGN KEY (siswa_id) REFERENCES public.siswa(id);


--
-- Name: prediksi_kelulusan prediksi_kelulusan_siswa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin_smkn1
--

ALTER TABLE ONLY public.prediksi_kelulusan
    ADD CONSTRAINT prediksi_kelulusan_siswa_id_fkey FOREIGN KEY (siswa_id) REFERENCES public.siswa(id);


--
-- PostgreSQL database dump complete
--

\unrestrict HuhnreCxKSct0DDBhNMz3zaSLdHM5Kr7efWOETyCs3jiyzPw5eVcEqjBSXc3VgY

