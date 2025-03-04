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
    user_id integer
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
    role_id integer
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
7	27	Kina7OUv
8	28	9BWRIwZD
9	29	NGpJ0A5h
10	30	p6STzElr
11	31	Y1EzP1cE
\.


--
-- Data for Name: classes; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.classes (class_id, class_course_code, class_section_number, user_id) FROM stdin;
27	CS101	1001	31
28	CS101	1002	31
29	CS102	1002	31
30	CS101	1001	37
31	CS103	1001	31
32	CS101	1001	42
33	CS101	1001	48
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
7	32	27
8	34	27
9	35	27
10	36	27
11	38	30
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
1	student	Regular user role with access to courses and basic platform features	\N
2	instructor	Instructor role with access to course assignment and student management	\N
3	admin	Administrator role with full platform access and management tools	\N
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
110	f	1.16	34
111	f	1.17	34
112	f	1.18	34
113	f	1.19	34
114	f	1.21	34
115	f	1.9	34
105	t	1.11	34
106	t	1.12	34
107	t	1.13	34
108	t	1.14	34
109	t	1.15	34
119	f	1.14	35
120	f	1.15	35
121	f	1.16	35
122	f	1.17	35
123	f	1.18	35
124	f	1.19	35
125	f	1.21	35
126	f	1.9	35
116	t	1.11	35
117	t	1.12	35
118	t	1.13	35
\.


--
-- Data for Name: student_assigned_courses; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.student_assigned_courses (student_assigned_courses_id, course_id, user_id) FROM stdin;
28	21	34
29	21	35
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.users (user_id, username, first_name, last_name, email, password, role_id) FROM stdin;
31	TestAccount	John	Doe	test@email.com	\\x243262243132244c33707343767a4251467857534d6e366f587a704e2e6b756a755a72394845305252527874653137626c415a354479354359507469	1
32	TestAccountTwo	Jane	Dane	testtwo@email.com	\\x243262243132243045347556485770364832723238472e666951677475654f7a45744968427651755362646c4e574f36437334304a31334f4273334b	2
33	Iamcool123	Blake	Lively	blakelively@gmail.com	\\x2432622431322457694a6b3876594a454b4d59366c643778395567654f686738726c46483634626b424e70774b39547552536d724a71336c2f653369	1
34	StudentOne	John	Carry	studentOne@gmail.com	\\x243262243132243169456230512e30627230546f705a4a67657350372e704457432f794b7376632e79427175685a6e72766c35435075464a304e4265	2
35	StudentTwo	Alvin	Cook	studentTwo@gmail.com	\\x24326224313224325571392e41755a6f48326f312e72534d795163762e4b45575361792f69692e7743562e4f6b4f506b6d61654d537963707231564f	2
36	StudentThree	Jerry	Smith	studentThree@gmail.com	\\x243262243132246577644f552f7a62384257466f614e2f77685862706562396453715a782f47325272344948764778477a6d4e50513831786a494336	2
37	InstructorDemo	Terry	Smith	instructordemo@gmail.com	\\x243262243132244e4176784230645149705a736635546a356e2f6e366570792e7148494b577a32556673566a6c41376c5462554f6f6c56444e554261	1
38	StudentDemo	Jeff	CoolGuy	studentdemo@gmail.com	\\x2432622431322432566a3570764c73796273312f76546362505074722e5733374663546b3274512f66655a4a747335766f44737951314e4b776b4871	2
39	StudentDemoOne	Henry	Calvin	testemailone@gmail.com	\\x243262243132246f6b794d796e2f71535347364b78456d6774672e792e374e4943685362596a453246626e71314c41644a784b7570684a694e534b4b	2
40	practiceuser	practice	user	practiceuser@gmail.com	\\x2432622431322458387655632e4b6e48694b3068486c666b386f6c6675783574706b71493946304731716a55374e686d364d4b2e4f5a742f476a3743	1
41	LilyPartovi	Lily	Partovi	lilypartovi04@gmail.com	\\x2432622431322438764f6d483748446e417241683834446c41696567756f454242565851327a3369695a2f7538616a723431705276336366644c4d61	1
42	doglover123	Addy	Cook	addycook@gmail.com	\\x243262243132245342556f387073646845324247393547466d32706c2e654f557332377a2e595043565357414d735536503044545050783974713475	1
43	Adele	Adele	Cook	adelecook@gmail.com	\\x243262243132244545476c584d534c49386b524f3768795a6d394767755062623867443968787a746f38454e643443585a583345566346374442744b	1
44	Computerengineer	Sutter	Reynolds	sutter@gmail.com	\\x243262243132246168724f78745855684e30635067792f7a34787170656b682e563839514d5759637847366e2f62446d73447a463278397754667775	1
45	TaylorSwift	Taylor	Swift	ts@gmail.com	\\x24326224313224474753504f685030665a5252693952525976366a322e31332f62756150662f63614b41742e544d6b45366c68634c7a56466d394179	1
46	Chapel Roan	Chapel	Roan	cr@gmail.com	\\x24326224313224357563736a634c5149367762344779716e6b6c4d632e4f5532416945486f724335647a527375395242784458343561356552776c2e	1
47	John Doe	John	Doe	johndoe@gmail.com	\\x243262243132247450517658767878305a4f5347463252782e6e79774f44656b4956733966696941694b325274724c65544574445154657252644457	2
48	JohnDoe	John	Doe	johndoee@gmail.com	\\x243262243132246c652f655067484a626b63345a4464485350646a4a6569776d506d492e4e64655337537a574879766671534164766474636a4b4436	1
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

SELECT pg_catalog.setval('public.courses_course_id_seq', 38, false);


--
-- Name: enrollment_enrollment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.enrollment_enrollment_id_seq', 12, false);


--
-- Name: feedback_feedback_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.feedback_feedback_id_seq', 2, false);


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

SELECT pg_catalog.setval('public.student_assigned_courses_student_assigned_courses_id_seq', 29, true);


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
    ADD CONSTRAINT fk_class FOREIGN KEY (class_id) REFERENCES public.classes(class_id);


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
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.users(user_id);


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

