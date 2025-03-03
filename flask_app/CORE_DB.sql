--
-- PostgreSQL database dump
--

-- Dumped from database version 16.6 (Ubuntu 16.6-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.6 (Ubuntu 16.6-0ubuntu0.24.04.1)

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
-- Name: public; Type: SCHEMA; Schema: -; Owner: testuser
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO testuser;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: testuser
--

COMMENT ON SCHEMA public IS '';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: class_codes; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.class_codes (
    class_code_id integer NOT NULL,
    class_id integer NOT NULL,
    class_code character varying(15)
);


ALTER TABLE public.class_codes OWNER TO testuser;

--
-- Name: class_codes_class_code_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.class_codes_class_code_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.class_codes_class_code_id_seq OWNER TO testuser;

--
-- Name: class_codes_class_code_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.class_codes_class_code_id_seq OWNED BY public.class_codes.class_code_id;


--
-- Name: classes; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.classes (
    class_id integer NOT NULL,
    class_course_code character varying(100) NOT NULL,
    class_section_number integer NOT NULL,
    user_id integer,
    created_at date DEFAULT CURRENT_DATE NOT NULL,
    expired_at date
);


ALTER TABLE public.classes OWNER TO testuser;

--
-- Name: classes_class_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.classes_class_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.classes_class_id_seq OWNER TO testuser;

--
-- Name: classes_class_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.classes_class_id_seq OWNED BY public.classes.class_id;


--
-- Name: course_subsections; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.course_subsections (
    course_subsection_id integer NOT NULL,
    course_subsection_number double precision,
    course_subsection_name character varying(100)
);


ALTER TABLE public.course_subsections OWNER TO testuser;

--
-- Name: course_subsections_course_subsection_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.course_subsections_course_subsection_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.course_subsections_course_subsection_id_seq OWNER TO testuser;

--
-- Name: course_subsections_course_subsection_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.course_subsections_course_subsection_id_seq OWNED BY public.course_subsections.course_subsection_id;


--
-- Name: courses; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.courses (
    course_id integer NOT NULL,
    course_name character varying(100),
    course_desc character varying(1000),
    section_number double precision,
    level character varying(50),
    certificate boolean,
    length character varying(50),
    route character varying(50)
);


ALTER TABLE public.courses OWNER TO testuser;

--
-- Name: courses_course_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.courses_course_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.courses_course_id_seq OWNER TO testuser;

--
-- Name: courses_course_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.courses_course_id_seq OWNED BY public.courses.course_id;


--
-- Name: enrollment; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.enrollment (
    enrollment_id integer NOT NULL,
    user_id integer,
    class_id integer
);


ALTER TABLE public.enrollment OWNER TO testuser;

--
-- Name: enrollment_enrollment_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.enrollment_enrollment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.enrollment_enrollment_id_seq OWNER TO testuser;

--
-- Name: enrollment_enrollment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.enrollment_enrollment_id_seq OWNED BY public.enrollment.enrollment_id;


--
-- Name: feedback; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.feedback (
    feedback_id integer NOT NULL,
    feedback_desc character varying(1000),
    rating integer,
    course_id integer,
    user_id integer,
    CONSTRAINT feedback_rating_check CHECK (((rating >= 1) AND (rating <= 5)))
);


ALTER TABLE public.feedback OWNER TO testuser;

--
-- Name: feedback_feedback_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.feedback_feedback_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.feedback_feedback_id_seq OWNER TO testuser;

--
-- Name: feedback_feedback_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.feedback_feedback_id_seq OWNED BY public.feedback.feedback_id;


--
-- Name: permissions; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.permissions (
    permission_id integer NOT NULL,
    permission_name character varying(100),
    permission_desc character varying(1000)
);


ALTER TABLE public.permissions OWNER TO testuser;

--
-- Name: permissions_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.permissions_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.permissions_permission_id_seq OWNER TO testuser;

--
-- Name: permissions_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.permissions_permission_id_seq OWNED BY public.permissions.permission_id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.roles (
    role_id integer NOT NULL,
    role_name character varying(100),
    role_desc character varying(1000),
    permission_id integer
);


ALTER TABLE public.roles OWNER TO testuser;

--
-- Name: roles_role_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.roles_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_role_id_seq OWNER TO testuser;

--
-- Name: roles_role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.roles_role_id_seq OWNED BY public.roles.role_id;


--
-- Name: scoreboard; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.scoreboard (
    scoreboard_id integer NOT NULL,
    score integer,
    user_id integer
);


ALTER TABLE public.scoreboard OWNER TO testuser;

--
-- Name: scoreboard_scoreboard_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.scoreboard_scoreboard_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.scoreboard_scoreboard_id_seq OWNER TO testuser;

--
-- Name: scoreboard_scoreboard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.scoreboard_scoreboard_id_seq OWNED BY public.scoreboard.scoreboard_id;


--
-- Name: student_assigned_course_subsections; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.student_assigned_course_subsections (
    assigned_course_subsection_id integer NOT NULL,
    completion_status boolean,
    course_subsection_number double precision,
    user_id integer
);


ALTER TABLE public.student_assigned_course_subsections OWNER TO testuser;

--
-- Name: student_assigned_course_subse_assigned_course_subsection_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.student_assigned_course_subse_assigned_course_subsection_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.student_assigned_course_subse_assigned_course_subsection_id_seq OWNER TO testuser;

--
-- Name: student_assigned_course_subse_assigned_course_subsection_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.student_assigned_course_subse_assigned_course_subsection_id_seq OWNED BY public.student_assigned_course_subsections.assigned_course_subsection_id;


--
-- Name: student_assigned_courses; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.student_assigned_courses (
    student_assigned_courses_id integer NOT NULL,
    course_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.student_assigned_courses OWNER TO testuser;

--
-- Name: student_assigned_courses_student_assigned_courses_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.student_assigned_courses_student_assigned_courses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.student_assigned_courses_student_assigned_courses_id_seq OWNER TO testuser;

--
-- Name: student_assigned_courses_student_assigned_courses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.student_assigned_courses_student_assigned_courses_id_seq OWNED BY public.student_assigned_courses.student_assigned_courses_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(100),
    first_name character varying(100),
    last_name character varying(100),
    email character varying(100),
    password bytea,
    role_id integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.users OWNER TO testuser;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO testuser;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: class_codes class_code_id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.class_codes ALTER COLUMN class_code_id SET DEFAULT nextval('public.class_codes_class_code_id_seq'::regclass);


--
-- Name: classes class_id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.classes ALTER COLUMN class_id SET DEFAULT nextval('public.classes_class_id_seq'::regclass);


--
-- Name: course_subsections course_subsection_id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.course_subsections ALTER COLUMN course_subsection_id SET DEFAULT nextval('public.course_subsections_course_subsection_id_seq'::regclass);


--
-- Name: courses course_id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.courses ALTER COLUMN course_id SET DEFAULT nextval('public.courses_course_id_seq'::regclass);


--
-- Name: enrollment enrollment_id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.enrollment ALTER COLUMN enrollment_id SET DEFAULT nextval('public.enrollment_enrollment_id_seq'::regclass);


--
-- Name: feedback feedback_id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.feedback ALTER COLUMN feedback_id SET DEFAULT nextval('public.feedback_feedback_id_seq'::regclass);


--
-- Name: permissions permission_id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.permissions ALTER COLUMN permission_id SET DEFAULT nextval('public.permissions_permission_id_seq'::regclass);


--
-- Name: roles role_id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.roles ALTER COLUMN role_id SET DEFAULT nextval('public.roles_role_id_seq'::regclass);


--
-- Name: scoreboard scoreboard_id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.scoreboard ALTER COLUMN scoreboard_id SET DEFAULT nextval('public.scoreboard_scoreboard_id_seq'::regclass);


--
-- Name: student_assigned_course_subsections assigned_course_subsection_id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.student_assigned_course_subsections ALTER COLUMN assigned_course_subsection_id SET DEFAULT nextval('public.student_assigned_course_subse_assigned_course_subsection_id_seq'::regclass);


--
-- Name: student_assigned_courses student_assigned_courses_id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.student_assigned_courses ALTER COLUMN student_assigned_courses_id SET DEFAULT nextval('public.student_assigned_courses_student_assigned_courses_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: class_codes; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.class_codes (class_code_id, class_id, class_code) FROM stdin;
\.


--
-- Data for Name: classes; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.classes (class_id, class_course_code, class_section_number, user_id, created_at, expired_at) FROM stdin;
34	CPE201	1001	40	2025-02-24	\N
35	CS101	1001	39	2025-02-24	2026-02-24
36	CS222	1001	39	2025-02-23	2026-02-24
37	CS222	1002	39	2025-02-23	2026-02-24
38	CS135	1001	40	2025-02-21	2026-02-24
39	CS302	1001	40	2025-02-20	2026-02-24
\.


--
-- Data for Name: course_subsections; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.course_subsections (course_subsection_id, course_subsection_number, course_subsection_name) FROM stdin;
11	1.11	Objectives
12	1.12	Definition and Overview
13	1.13	History of Robotics
14	1.14	Types of Robots
15	1.15	Importance and Applications
16	1.16	Robot Anatomy
17	1.17	Challenges in Robotics
18	1.18	Robot Programming
19	1.19	Social and Ethical Implications
20	1.21	Future Trends
21	1.9	C1 Quiz One
\.


--
-- Data for Name: courses; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.courses (course_id, course_name, course_desc, section_number, level, certificate, length, route) FROM stdin;
21	Introduction to Robotics	Learn the basics of robotics, from robot anatomy to robot programming.	1	Beginner Friendly	t	1 hour	course1_card
22	Types of Robots	Gain an insight into how different robots serve unique purposes with their different functionality.	2	Beginner Friendly	t	1 hour	course2_card
24	How to Use the Lab	Get familiar with CORE's Virtual Robotics Lab and explore live simulations, an interactive, hands-on learning experience, and coding feedback.	4	Beginner Friendly	t	1 hour	course1_card
26	Fetch Robot	Acquire the skills required to program and control the Fetch Robot to complete different tasks including reaching, pushing, and sliding.	6	Beginner Friendly	t	1 hour	course1_card
23	Robots in CORE	Discover the heart of CORE: meet our virtual robots, designed for you.	3	Beginner Friendly	t	30 minutes	course3_card
25	Basic Coding Practices	Master the basics of coding, building yourself a strong foundation, involving a review of common coding practices and debugging techniques.	5	Beginner Friendly	t	1 hour	course4_card
27	Fetch Reach Robot	Master control and precision as you learn to code the Fetch Reach Robot.	7	Beginner Friendly	t	2 hours	course6_card
30	Fetch Pick & Place Robot	Become proficient in robotic object manipulation with the Fetch Pick and Place Robot.	10	Intermediate	t	2 hours	course7_card
31	Fetch Stack Blocks Robot	Hone the precision of stacking blocks using the Fetch Robot and improve your spatial manipulation.	11	Intermediate	t	1 hour	course8_card
32	Fetch Color Sort Robot	Learn to algorithmically move the Fetch Robot to sort and organize objects based on their colors.	12	Intermediate	t	2 hours	course9_card
33	Fetch Robot w/ Sensors	Unlock the power of sensors by teaching the Fetch Robot to detect, classify, and organize objects.	13	Intermediate	t	2 hours	course10_card
37	Autonomous Car w/ Sensors	Learn about Deep Q-Learning algorithms to create a self-driving car.	17	Advanced	t	2 hours	course11_card
\.


--
-- Data for Name: enrollment; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.enrollment (enrollment_id, user_id, class_id) FROM stdin;
\.


--
-- Data for Name: feedback; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.feedback (feedback_id, feedback_desc, rating, course_id, user_id) FROM stdin;
\.


--
-- Data for Name: permissions; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.permissions (permission_id, permission_name, permission_desc) FROM stdin;
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.roles (role_id, role_name, role_desc, permission_id) FROM stdin;
3	Admin	Administrator role with full platform access and management tools	\N
2	Student	Regular user role with access to courses and basic platform features	\N
1	Instructor	Instructor role with access to course assignment and student management	\N
\.


--
-- Data for Name: scoreboard; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.scoreboard (scoreboard_id, score, user_id) FROM stdin;
\.


--
-- Data for Name: student_assigned_course_subsections; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.student_assigned_course_subsections (assigned_course_subsection_id, completion_status, course_subsection_number, user_id) FROM stdin;
\.


--
-- Data for Name: student_assigned_courses; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.student_assigned_courses (student_assigned_courses_id, course_id, user_id) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.users (user_id, username, first_name, last_name, email, password, role_id, created_at) FROM stdin;
38	StudentTwo	Student	Two	studenttwo@gmail.com	\\x243262243132244e39745877716257452f35512f67756e2f645158582e67565447563948796a5961584b42624a7645355837555a77467456465a3836	2	2025-02-24 01:52:12.475114
40	InstructorTwo	Instructor	Two	instructortwo@gmail.com	\\x243262243132244c6b6f3263422e4e304f7233694f694c307377654f6538715731776a4654516c5967454568734a6d4c696e4e753237675176536969	1	2025-02-24 01:52:12.475114
37	StudentOne	Student	Three	studentone@gmail.com	\\x243262243132245969356b7a2e56314655634a6b4b486752366f54564f6a736464584f4b2f525156624c4c7144766d624c6f77382f5a467835397132	2	2025-02-24 01:52:12.475114
39	InstructorOne	Instructor	One	instructorone@gmail.com	\\x24326224313224485551657561356236613278764562344d684562344f766b6369743131695750757563477669485a3779533073564e504c6d394169	1	2025-02-24 01:52:12.475114
42	admin	Admin	One	admin@gmail.com	\\x24326224313224506c71566574446747544459366565756134727265654e426f76314636656470474e75706d653446717a2e4c4a333770674f5a684b	3	2025-02-24 01:52:12.475114
70	NewStudentOne	Jasmine	Almedo	jalmedo@gmail.com	\\x243262243132243247317741747a4a69724e472f564575724635613975446e564b70386f756474587933756234394e527569684b5a55474e4c722f75	2	2025-02-24 10:54:13.982985
\.


--
-- Name: class_codes_class_code_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.class_codes_class_code_id_seq', 12, false);


--
-- Name: classes_class_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.classes_class_id_seq', 33, true);


--
-- Name: course_subsections_course_subsection_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.course_subsections_course_subsection_id_seq', 22, false);


--
-- Name: courses_course_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.courses_course_id_seq', 1, false);


--
-- Name: enrollment_enrollment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.enrollment_enrollment_id_seq', 12, false);


--
-- Name: feedback_feedback_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.feedback_feedback_id_seq', 1, false);


--
-- Name: permissions_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.permissions_permission_id_seq', 2, false);


--
-- Name: roles_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.roles_role_id_seq', 4, false);


--
-- Name: scoreboard_scoreboard_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.scoreboard_scoreboard_id_seq', 2, false);


--
-- Name: student_assigned_course_subse_assigned_course_subsection_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.student_assigned_course_subse_assigned_course_subsection_id_seq', 126, true);


--
-- Name: student_assigned_courses_student_assigned_courses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.student_assigned_courses_student_assigned_courses_id_seq', 1, false);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.users_user_id_seq', 48, true);


--
-- Name: class_codes class_codes_class_code_key; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.class_codes
    ADD CONSTRAINT class_codes_class_code_key UNIQUE (class_code);


--
-- Name: class_codes class_codes_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.class_codes
    ADD CONSTRAINT class_codes_pkey PRIMARY KEY (class_code_id);


--
-- Name: classes classes_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.classes
    ADD CONSTRAINT classes_pkey PRIMARY KEY (class_id);


--
-- Name: course_subsections course_subsections_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.course_subsections
    ADD CONSTRAINT course_subsections_pkey PRIMARY KEY (course_subsection_id);


--
-- Name: courses courses_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.courses
    ADD CONSTRAINT courses_pkey PRIMARY KEY (course_id);


--
-- Name: enrollment enrollment_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.enrollment
    ADD CONSTRAINT enrollment_pkey PRIMARY KEY (enrollment_id);


--
-- Name: feedback feedback_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_pkey PRIMARY KEY (feedback_id);


--
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (permission_id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (role_id);


--
-- Name: scoreboard scoreboard_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.scoreboard
    ADD CONSTRAINT scoreboard_pkey PRIMARY KEY (scoreboard_id);


--
-- Name: student_assigned_course_subsections student_assigned_course_subsections_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.student_assigned_course_subsections
    ADD CONSTRAINT student_assigned_course_subsections_pkey PRIMARY KEY (assigned_course_subsection_id);


--
-- Name: student_assigned_courses student_assigned_courses_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.student_assigned_courses
    ADD CONSTRAINT student_assigned_courses_pkey PRIMARY KEY (student_assigned_courses_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: class_codes class_codes_class_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.class_codes
    ADD CONSTRAINT class_codes_class_id_fkey FOREIGN KEY (class_id) REFERENCES public.classes(class_id) ON DELETE CASCADE;


--
-- Name: enrollment enrollment_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.enrollment
    ADD CONSTRAINT enrollment_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: feedback feedback_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(course_id);


--
-- Name: feedback feedback_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.feedback
    ADD CONSTRAINT feedback_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: enrollment fk_class; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.enrollment
    ADD CONSTRAINT fk_class FOREIGN KEY (class_id) REFERENCES public.classes(class_id) ON DELETE CASCADE;


--
-- Name: class_codes fk_class_id; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.class_codes
    ADD CONSTRAINT fk_class_id FOREIGN KEY (class_id) REFERENCES public.classes(class_id) ON DELETE CASCADE;


--
-- Name: users fk_role; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT fk_role FOREIGN KEY (role_id) REFERENCES public.roles(role_id);


--
-- Name: classes fk_user; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.classes
    ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE SET NULL;


--
-- Name: classes fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.classes
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: student_assigned_course_subsections fk_user_id; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.student_assigned_course_subsections
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: roles roles_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permissions(permission_id);


--
-- Name: scoreboard scoreboard_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.scoreboard
    ADD CONSTRAINT scoreboard_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: student_assigned_courses student_assigned_courses_course_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.student_assigned_courses
    ADD CONSTRAINT student_assigned_courses_course_id_fkey FOREIGN KEY (course_id) REFERENCES public.courses(course_id) ON DELETE CASCADE;


--
-- Name: student_assigned_courses student_assigned_courses_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.student_assigned_courses
    ADD CONSTRAINT student_assigned_courses_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: testuser
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;


--
-- PostgreSQL database dump complete
--

