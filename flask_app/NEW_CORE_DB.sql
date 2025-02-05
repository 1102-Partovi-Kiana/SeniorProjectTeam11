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
7	27	D6zDy166
\.


--
-- Data for Name: classes; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.classes (class_id, class_course_code, class_section_number, user_id) FROM stdin;
27	CS101	1001	31
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
23	Robots in CORE	Discover the heart of CORE: meet our virtual robots, designed for you.	3	Beginner Friendly	t	30 minutes	course1_card
24	How to Use the Lab	Get familiar with CORE's Virtual Robotics Lab and explore live simulations, an interactive, hands-on learning experience, and coding feedback.	4	Beginner Friendly	t	1 hour	course1_card
25	Basic Coding Practices	Master the basics of coding, building yourself a strong foundation, involving a review of common coding practices and debugging techniques.	5	Beginner Friendly	t	1 hour	course1_card
26	Fetch Robot	Acquire the skills required to program and control the Fetch Robot to complete different tasks including reaching, pushing, and sliding.	6	Beginner Friendly	t	1 hour	course1_card
27	Fetch Reach Robot	Master control and precision as you learn to code the Fetch Reach Robot.	7	Beginner Friendly	t	2 hours	course1_card
30	Fetch Pick & Place Robot	Become proficient in robotic object manipulation with the Fetch Pick and Place Robot.	8	Intermediate	t	2 hours	course1_card
31	Fetch Stack Blocks Robot	Hone the precision of stacking blocks using the Fetch Robot and improve your spatial manipulation.	9	Intermediate	t	1 hour	course1_card
32	Fetch Color Sort Robot	Learn to algorithmically move the Fetch Robot to sort and organize objects based on their colors.	10	Intermediate	t	2 hours	course1_card
33	Fetch Robot w/ Sensors	Unlock the power of sensors by teaching the Fetch Robot to detect, classify, and organize objects.	11	Intermediate	t	2 hours	course1_card
37	Autonomous Car w/ Sensors	Learn about Deep Q-Learning algorithms to create a self-driving car.	12	Advanced	t	2 hours	course1_card
\.


--
-- Data for Name: enrollment; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.enrollment (enrollment_id, user_id, class_id) FROM stdin;
7	34	27
8	35	27
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
94	t	1.11	34
95	t	1.12	34
96	t	1.13	34
97	t	1.14	34
98	t	1.15	34
104	t	1.9	34
99	t	1.16	34
100	t	1.17	34
101	t	1.18	34
102	t	1.19	34
103	t	1.21	34
\.


--
-- Data for Name: student_assigned_courses; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.student_assigned_courses (student_assigned_courses_id, course_id, user_id) FROM stdin;
26	21	34
27	21	35
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.users (user_id, username, first_name, last_name, email, password, role_id) FROM stdin;
31	TestAccount	TestFirst	TestLast	test@gmail.com	\\x243262243132243958435463626e2f77567831594a545065522e6a4e2e334d785348393041553238566662732f70424b3268486b4552577a63532f2e	1
32	TestAccountTwo	TestFirst	TestLast	testaccount@gmail.com	\\x2432622431322448336479724f364f4736593159354c324c457675312e6654424236714e5067327957377255594b4a73426b4d536e64735a2f525832	1
33	TestAccountThree	TestFirst	TestLast	testaccountthree@gmail.com	\\x243262243132244d4e69506f6c6c70622e69664f6d61762e32715638752e4a4b43366a646f7466714c2e614163453552346f59543830486c62717057	2
34	Student1	Student	One	studentone@gmail.com	\\x243262243132245054383571703378504a5655345370654241437445757a6b48634f7a583878557a6a5a75745869534d4c62514a6c7835395355792e	2
35	Student2	Student	Two	studenttwo@gmail.com	\\x243262243132247564526c4a6a753079735958642f30566f4e535447756c31374336485a6d523765666b356143717954307362592f706f45636f3375	2
\.


--
-- Name: class_codes_class_code_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.class_codes_class_code_id_seq', 7, true);


--
-- Name: classes_class_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.classes_class_id_seq', 27, true);


--
-- Name: course_subsections_course_subsection_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.course_subsections_course_subsection_id_seq', 21, true);


--
-- Name: courses_course_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.courses_course_id_seq', 37, true);


--
-- Name: enrollment_enrollment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.enrollment_enrollment_id_seq', 8, true);


--
-- Name: feedback_feedback_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.feedback_feedback_id_seq', 1, false);


--
-- Name: permissions_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.permissions_permission_id_seq', 1, false);


--
-- Name: roles_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.roles_role_id_seq', 3, true);


--
-- Name: scoreboard_scoreboard_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.scoreboard_scoreboard_id_seq', 1, false);


--
-- Name: student_assigned_course_subse_assigned_course_subsection_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.student_assigned_course_subse_assigned_course_subsection_id_seq', 104, true);


--
-- Name: student_assigned_courses_student_assigned_courses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.student_assigned_courses_student_assigned_courses_id_seq', 27, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.users_user_id_seq', 35, true);


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
-- PostgreSQL database dump complete
--

