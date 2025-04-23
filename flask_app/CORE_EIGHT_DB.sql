--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8 (Ubuntu 16.8-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.8 (Ubuntu 16.8-0ubuntu0.24.04.1)

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
    user_id integer NOT NULL,
    completion_status boolean DEFAULT false
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
-- Name: student_grades; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.student_grades (
    student_grades_id integer NOT NULL,
    student_id integer NOT NULL,
    percentage_grade double precision NOT NULL,
    course_subsection_id integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.student_grades OWNER TO testuser;

--
-- Name: student_grades_student_grades_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.student_grades_student_grades_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.student_grades_student_grades_id_seq OWNER TO testuser;

--
-- Name: student_grades_student_grades_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.student_grades_student_grades_id_seq OWNED BY public.student_grades.student_grades_id;


--
-- Name: user_code_logs; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.user_code_logs (
    user_log_id integer NOT NULL,
    code character varying(50000),
    error character varying(10000),
    hints character varying(10000),
    page_context character varying(10000),
    static_issues character varying(10000),
    created_at timestamp without time zone,
    user_id integer
);


ALTER TABLE public.user_code_logs OWNER TO testuser;

--
-- Name: user_code_logs_user_log_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.user_code_logs_user_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_code_logs_user_log_id_seq OWNER TO testuser;

--
-- Name: user_code_logs_user_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.user_code_logs_user_log_id_seq OWNED BY public.user_code_logs.user_log_id;


--
-- Name: user_points; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.user_points (
    user_points_id integer NOT NULL,
    num_points double precision NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.user_points OWNER TO testuser;

--
-- Name: user_points_user_points_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.user_points_user_points_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_points_user_points_id_seq OWNER TO testuser;

--
-- Name: user_points_user_points_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.user_points_user_points_id_seq OWNED BY public.user_points.user_points_id;


--
-- Name: user_time_logs; Type: TABLE; Schema: public; Owner: testuser
--

CREATE TABLE public.user_time_logs (
    time_log_id integer NOT NULL,
    page_context character varying(1000),
    start_time timestamp without time zone,
    end_time timestamp without time zone,
    duration double precision,
    user_id integer NOT NULL
);


ALTER TABLE public.user_time_logs OWNER TO testuser;

--
-- Name: user_time_logs_user_time_id_seq; Type: SEQUENCE; Schema: public; Owner: testuser
--

CREATE SEQUENCE public.user_time_logs_user_time_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_time_logs_user_time_id_seq OWNER TO testuser;

--
-- Name: user_time_logs_user_time_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: testuser
--

ALTER SEQUENCE public.user_time_logs_user_time_id_seq OWNED BY public.user_time_logs.time_log_id;


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
-- Name: student_grades student_grades_id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.student_grades ALTER COLUMN student_grades_id SET DEFAULT nextval('public.student_grades_student_grades_id_seq'::regclass);


--
-- Name: user_code_logs user_log_id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.user_code_logs ALTER COLUMN user_log_id SET DEFAULT nextval('public.user_code_logs_user_log_id_seq'::regclass);


--
-- Name: user_points user_points_id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.user_points ALTER COLUMN user_points_id SET DEFAULT nextval('public.user_points_user_points_id_seq'::regclass);


--
-- Name: user_time_logs time_log_id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.user_time_logs ALTER COLUMN time_log_id SET DEFAULT nextval('public.user_time_logs_user_time_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: class_codes; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.class_codes (class_code_id, class_id, class_code) FROM stdin;
15	44	lw7oWCzb
\.


--
-- Data for Name: classes; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.classes (class_id, class_course_code, class_section_number, user_id, created_at, expired_at) FROM stdin;
44	CS101	1001	93	2025-04-14	2025-04-30
45	CS102	1001	93	2025-04-21	2025-04-30
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
23	1.91	C1 Quiz Two
24	2.11	Introduction of Mobile Robotics
25	2.12	Industrial Robots
26	2.13	Service Robots
27	2.14	Mobile Robots
28	2.15	Humanoid Robots
29	2.16	Agricultural Robots
30	2.17	Medical Robots
32	2.18	Certificate
33	5.11	Objectives
34	5.12	Naming Conventions
35	5.13	Commenting
36	5.14	Indentation
37	5.15	Variables
38	5.16	Control Flow
39	5.17	Loops
40	5.18	Functions
41	5.19	Debugging Techniques
42	5.9	C5 Quiz One
43	5.2	Cheat Sheet
44	5.21	Certificate
31	2.9	C2 Quiz One
45	6.11	Objectives
46	6.12	About
47	6.13	Environment
48	6.14	Coding Logic
49	6.9	C6 Quiz One
50	6.15	Cheat Sheet
51	6.16	Time to Code
52	6.17	Certificate
53	7.11	Objectives
54	7.12	About
55	7.13	Environment
56	7.14	Coding Logic
57	7.9	C7 Quiz One
58	7.15	Cheat Sheet
59	7.16	Time to Code
60	7.17	Certificate
61	8.11	Objectives
62	8.12	About
63	8.13	Environment
64	8.14	Coding Logic
65	8.9	C8 Quiz One
66	8.15	Cheat Sheet
67	8.16	Time to Code
68	8.17	Certificate
69	9.11	Objectives
70	9.12	About
71	9.13	Environment
72	9.14	Coding Logic
73	9.9	C9 Quiz One
74	9.15	Cheat Sheet
75	9.16	Time to Code
76	9.17	Certificate
77	10.11	Objectives
78	10.12	About
79	10.13	Environment
80	10.14	Coding Logic
81	10.9	C10 Quiz One
82	10.15	Cheat Sheet
83	10.16	Time to Code
84	10.17	Certificate
85	11.11	Objectives
86	11.12	About
87	11.13	Environment
88	11.14	Coding Logic
89	11.9	C11 Quiz One
90	11.15	Cheat Sheet
91	11.16	Time to Code
92	11.17	Certificate
\.


--
-- Data for Name: courses; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.courses (course_id, course_name, course_desc, section_number, level, certificate, length, route) FROM stdin;
21	Introduction to Robotics	Learn the basics of robotics, from robot anatomy to robot programming.	1	Beginner Friendly	t	1 hour	course1_card
22	Types of Robots	Gain an insight into how different robots serve unique purposes with their different functionality.	2	Beginner Friendly	t	1 hour	course2_card
23	Robots in CORE	Discover the heart of CORE: meet our virtual robots, designed for you.	3	Beginner Friendly	t	30 minutes	course3_card
24	How to Use the Lab	Get familiar with CORE's Virtual Robotics Lab and explore live simulations, an interactive, hands-on learning experience, and coding feedback.	4	Beginner Friendly	t	1 hour	course1_card
25	Basic Coding Practices	Master the basics of coding, building yourself a strong foundation, involving a review of common coding practices and debugging techniques.	5	Beginner Friendly	t	1 hour	course4_card
27	Fetch Reach Robot	Master control and precision as you learn to code the Fetch Reach Robot.	6	Beginner Friendly	t	2 hours	course6_card
30	Fetch Pick & Place Robot	Become proficient in robotic object manipulation with the Fetch Pick and Place Robot.	7	Intermediate	t	2 hours	course7_card
31	Fetch Stack Blocks Robot	Hone the precision of stacking blocks using the Fetch Robot and improve your spatial manipulation.	8	Intermediate	t	1 hour	course8_card
32	Fetch Color Sort Robot	Learn to algorithmically move the Fetch Robot to sort and organize objects based on their colors.	9	Intermediate	t	2 hours	course9_card
33	Fetch Robot w/ Sensors	Unlock the power of sensors by teaching the Fetch Robot to detect, classify, and organize objects.	10	Intermediate	t	2 hours	course10_card
37	Autonomous Car w/ Sensors	Learn about Deep Q-Learning algorithms to create a self-driving car.	11	Advanced	t	2 hours	course11_card
\.


--
-- Data for Name: enrollment; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.enrollment (enrollment_id, user_id, class_id) FROM stdin;
19	94	44
20	95	44
21	96	44
22	97	44
23	98	44
24	99	44
25	100	44
26	101	44
27	102	44
28	103	44
29	104	44
30	105	44
31	106	44
32	107	44
33	108	44
34	109	44
35	110	44
36	111	44
37	112	44
38	113	44
39	114	44
40	115	44
41	116	44
42	117	44
43	118	44
44	119	44
45	120	44
46	121	44
47	122	44
48	125	44
81	127	44
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
602	f	2.11	94
603	f	2.12	94
604	f	2.13	94
605	f	2.14	94
606	f	2.15	94
607	f	2.16	94
608	f	2.17	94
609	f	2.18	94
610	f	2.9	94
611	f	5.11	94
612	f	5.12	94
613	f	5.13	94
614	f	5.14	94
615	f	5.15	94
616	f	5.16	94
617	f	5.17	94
618	f	5.18	94
619	f	5.19	94
620	f	5.9	94
621	f	5.2	94
622	f	5.21	94
623	f	6.11	94
624	f	6.12	94
625	f	6.13	94
626	f	6.14	94
627	f	6.9	94
628	f	6.15	94
629	f	6.16	94
630	f	6.17	94
631	f	7.11	94
632	f	7.12	94
633	f	7.13	94
634	f	7.14	94
635	f	7.9	94
636	f	7.15	94
637	f	7.16	94
638	f	7.17	94
639	f	8.11	94
640	f	8.12	94
641	f	8.13	94
642	f	8.14	94
643	f	8.9	94
644	f	8.15	94
645	f	8.16	94
646	f	8.17	94
647	f	9.11	94
648	f	9.12	94
649	f	9.13	94
650	f	9.14	94
651	f	9.9	94
652	f	9.15	94
653	f	9.16	94
654	f	9.17	94
655	f	10.11	94
656	f	10.12	94
657	f	10.13	94
658	f	10.14	94
659	f	10.9	94
660	f	10.15	94
661	f	10.16	94
662	f	10.17	94
663	f	11.11	94
664	f	11.12	94
665	f	11.13	94
666	f	11.14	94
667	f	11.9	94
668	f	11.15	94
669	f	11.16	94
670	f	11.17	94
683	f	2.11	95
684	f	2.12	95
685	f	2.13	95
686	f	2.14	95
687	f	2.15	95
688	f	2.16	95
689	f	2.17	95
690	f	2.18	95
691	f	2.9	95
692	f	5.11	95
693	f	5.12	95
694	f	5.13	95
695	f	5.14	95
696	f	5.15	95
697	f	5.16	95
698	f	5.17	95
699	f	5.18	95
700	f	5.19	95
701	f	5.9	95
702	f	5.2	95
703	f	5.21	95
704	f	6.11	95
705	f	6.12	95
706	f	6.13	95
707	f	6.14	95
708	f	6.9	95
709	f	6.15	95
710	f	6.16	95
711	f	6.17	95
712	f	7.11	95
713	f	7.12	95
714	f	7.13	95
715	f	7.14	95
716	f	7.9	95
717	f	7.15	95
718	f	7.16	95
719	f	7.17	95
720	f	8.11	95
721	f	8.12	95
722	f	8.13	95
723	f	8.14	95
724	f	8.9	95
725	f	8.15	95
726	f	8.16	95
727	f	8.17	95
728	f	9.11	95
729	f	9.12	95
730	f	9.13	95
731	f	9.14	95
732	f	9.9	95
733	f	9.15	95
734	f	9.16	95
735	f	9.17	95
736	f	10.11	95
737	f	10.12	95
738	f	10.13	95
739	f	10.14	95
740	f	10.9	95
741	f	10.15	95
742	f	10.16	95
743	f	10.17	95
744	f	11.11	95
745	f	11.12	95
746	f	11.13	95
591	t	1.12	94
593	t	1.14	94
594	t	1.15	94
600	t	1.9	94
595	t	1.16	94
596	t	1.17	94
597	t	1.18	94
598	t	1.19	94
599	t	1.21	94
601	t	1.91	94
671	t	1.11	95
672	t	1.12	95
673	t	1.13	95
675	t	1.15	95
681	t	1.9	95
676	t	1.16	95
677	t	1.17	95
678	t	1.18	95
679	t	1.19	95
680	t	1.21	95
682	t	1.91	95
747	f	11.14	95
748	f	11.9	95
749	f	11.15	95
750	f	11.16	95
751	f	11.17	95
752	f	1.11	96
753	f	1.12	96
754	f	1.13	96
755	f	1.14	96
756	f	1.15	96
757	f	1.16	96
758	f	1.17	96
759	f	1.18	96
760	f	1.19	96
761	f	1.21	96
762	f	1.9	96
763	f	1.91	96
764	f	2.11	96
765	f	2.12	96
766	f	2.13	96
767	f	2.14	96
768	f	2.15	96
769	f	2.16	96
770	f	2.17	96
771	f	2.18	96
772	f	2.9	96
773	f	5.11	96
774	f	5.12	96
775	f	5.13	96
776	f	5.14	96
777	f	5.15	96
778	f	5.16	96
779	f	5.17	96
780	f	5.18	96
781	f	5.19	96
782	f	5.9	96
783	f	5.2	96
784	f	5.21	96
785	f	6.11	96
786	f	6.12	96
787	f	6.13	96
788	f	6.14	96
789	f	6.9	96
790	f	6.15	96
791	f	6.16	96
792	f	6.17	96
793	f	7.11	96
794	f	7.12	96
795	f	7.13	96
796	f	7.14	96
797	f	7.9	96
798	f	7.15	96
799	f	7.16	96
800	f	7.17	96
801	f	8.11	96
802	f	8.12	96
803	f	8.13	96
804	f	8.14	96
805	f	8.9	96
806	f	8.15	96
807	f	8.16	96
808	f	8.17	96
809	f	9.11	96
810	f	9.12	96
811	f	9.13	96
812	f	9.14	96
813	f	9.9	96
814	f	9.15	96
815	f	9.16	96
816	f	9.17	96
817	f	10.11	96
818	f	10.12	96
819	f	10.13	96
820	f	10.14	96
821	f	10.9	96
822	f	10.15	96
823	f	10.16	96
824	f	10.17	96
825	f	11.11	96
826	f	11.12	96
827	f	11.13	96
828	f	11.14	96
829	f	11.9	96
830	f	11.15	96
831	f	11.16	96
832	f	11.17	96
833	f	1.11	97
834	f	1.12	97
835	f	1.13	97
836	f	1.14	97
837	f	1.15	97
838	f	1.16	97
839	f	1.17	97
840	f	1.18	97
841	f	1.19	97
842	f	1.21	97
843	f	1.9	97
844	f	1.91	97
845	f	2.11	97
846	f	2.12	97
847	f	2.13	97
848	f	2.14	97
849	f	2.15	97
850	f	2.16	97
851	f	2.17	97
852	f	2.18	97
853	f	2.9	97
854	f	5.11	97
855	f	5.12	97
856	f	5.13	97
857	f	5.14	97
858	f	5.15	97
859	f	5.16	97
860	f	5.17	97
861	f	5.18	97
862	f	5.19	97
863	f	5.9	97
864	f	5.2	97
865	f	5.21	97
866	f	6.11	97
867	f	6.12	97
868	f	6.13	97
869	f	6.14	97
870	f	6.9	97
871	f	6.15	97
872	f	6.16	97
873	f	6.17	97
874	f	7.11	97
875	f	7.12	97
876	f	7.13	97
877	f	7.14	97
878	f	7.9	97
879	f	7.15	97
880	f	7.16	97
881	f	7.17	97
882	f	8.11	97
883	f	8.12	97
884	f	8.13	97
885	f	8.14	97
886	f	8.9	97
887	f	8.15	97
888	f	8.16	97
889	f	8.17	97
890	f	9.11	97
891	f	9.12	97
892	f	9.13	97
893	f	9.14	97
894	f	9.9	97
895	f	9.15	97
896	f	9.16	97
897	f	9.17	97
898	f	10.11	97
899	f	10.12	97
900	f	10.13	97
901	f	10.14	97
902	f	10.9	97
903	f	10.15	97
904	f	10.16	97
905	f	10.17	97
906	f	11.11	97
907	f	11.12	97
908	f	11.13	97
909	f	11.14	97
910	f	11.9	97
911	f	11.15	97
912	f	11.16	97
913	f	11.17	97
914	f	1.11	98
915	f	1.12	98
916	f	1.13	98
917	f	1.14	98
918	f	1.15	98
919	f	1.16	98
920	f	1.17	98
921	f	1.18	98
922	f	1.19	98
923	f	1.21	98
924	f	1.9	98
925	f	1.91	98
926	f	2.11	98
927	f	2.12	98
928	f	2.13	98
929	f	2.14	98
930	f	2.15	98
931	f	2.16	98
932	f	2.17	98
933	f	2.18	98
934	f	2.9	98
935	f	5.11	98
936	f	5.12	98
937	f	5.13	98
938	f	5.14	98
939	f	5.15	98
940	f	5.16	98
941	f	5.17	98
942	f	5.18	98
943	f	5.19	98
944	f	5.9	98
945	f	5.2	98
946	f	5.21	98
947	f	6.11	98
948	f	6.12	98
949	f	6.13	98
950	f	6.14	98
951	f	6.9	98
952	f	6.15	98
953	f	6.16	98
954	f	6.17	98
955	f	7.11	98
956	f	7.12	98
957	f	7.13	98
958	f	7.14	98
959	f	7.9	98
960	f	7.15	98
961	f	7.16	98
962	f	7.17	98
963	f	8.11	98
964	f	8.12	98
965	f	8.13	98
966	f	8.14	98
967	f	8.9	98
968	f	8.15	98
969	f	8.16	98
970	f	8.17	98
971	f	9.11	98
972	f	9.12	98
973	f	9.13	98
974	f	9.14	98
975	f	9.9	98
976	f	9.15	98
977	f	9.16	98
978	f	9.17	98
979	f	10.11	98
980	f	10.12	98
981	f	10.13	98
982	f	10.14	98
983	f	10.9	98
984	f	10.15	98
985	f	10.16	98
986	f	10.17	98
987	f	11.11	98
988	f	11.12	98
989	f	11.13	98
990	f	11.14	98
992	f	11.15	98
993	f	11.16	98
994	f	11.17	98
995	f	1.11	99
996	f	1.12	99
997	f	1.13	99
998	f	1.14	99
999	f	1.15	99
1000	f	1.16	99
1001	f	1.17	99
1002	f	1.18	99
1003	f	1.19	99
1004	f	1.21	99
1005	f	1.9	99
1006	f	1.91	99
1007	f	2.11	99
1008	f	2.12	99
1009	f	2.13	99
1010	f	2.14	99
1011	f	2.15	99
1012	f	2.16	99
1013	f	2.17	99
1014	f	2.18	99
1015	f	2.9	99
1016	f	5.11	99
1017	f	5.12	99
1018	f	5.13	99
1019	f	5.14	99
1020	f	5.15	99
1021	f	5.16	99
1022	f	5.17	99
1023	f	5.18	99
1024	f	5.19	99
1025	f	5.9	99
1026	f	5.2	99
1027	f	5.21	99
1028	f	6.11	99
1029	f	6.12	99
1030	f	6.13	99
1031	f	6.14	99
1032	f	6.9	99
1033	f	6.15	99
1034	f	6.16	99
1035	f	6.17	99
1036	f	7.11	99
1037	f	7.12	99
1038	f	7.13	99
1039	f	7.14	99
1040	f	7.9	99
1041	f	7.15	99
1042	f	7.16	99
1043	f	7.17	99
1044	f	8.11	99
1045	f	8.12	99
1046	f	8.13	99
1047	f	8.14	99
1048	f	8.9	99
1049	f	8.15	99
1050	f	8.16	99
1051	f	8.17	99
1052	f	9.11	99
1053	f	9.12	99
1054	f	9.13	99
1055	f	9.14	99
1056	f	9.9	99
1057	f	9.15	99
1058	f	9.16	99
1059	f	9.17	99
1060	f	10.11	99
1061	f	10.12	99
1062	f	10.13	99
1063	f	10.14	99
1064	f	10.9	99
1065	f	10.15	99
1066	f	10.16	99
1067	f	10.17	99
1068	f	11.11	99
1069	f	11.12	99
1070	f	11.13	99
1071	f	11.14	99
1073	f	11.15	99
1074	f	11.16	99
1075	f	11.17	99
1076	f	1.11	100
1077	f	1.12	100
1078	f	1.13	100
1079	f	1.14	100
1080	f	1.15	100
1081	f	1.16	100
1082	f	1.17	100
1083	f	1.18	100
1084	f	1.19	100
1085	f	1.21	100
1086	f	1.9	100
1087	f	1.91	100
1088	f	2.11	100
1089	f	2.12	100
1090	f	2.13	100
1091	f	2.14	100
1092	f	2.15	100
1093	f	2.16	100
1094	f	2.17	100
1095	f	2.18	100
1096	f	2.9	100
1097	f	5.11	100
1098	f	5.12	100
1099	f	5.13	100
1100	f	5.14	100
1101	f	5.15	100
1102	f	5.16	100
1103	f	5.17	100
1104	f	5.18	100
1105	f	5.19	100
1106	f	5.9	100
1107	f	5.2	100
1108	f	5.21	100
1109	f	6.11	100
1110	f	6.12	100
1111	f	6.13	100
1112	f	6.14	100
1113	f	6.9	100
1114	f	6.15	100
1115	f	6.16	100
1116	f	6.17	100
1117	f	7.11	100
1118	f	7.12	100
1119	f	7.13	100
1120	f	7.14	100
1121	f	7.9	100
1122	f	7.15	100
1123	f	7.16	100
1124	f	7.17	100
1125	f	8.11	100
1126	f	8.12	100
1127	f	8.13	100
1128	f	8.14	100
1129	f	8.9	100
1130	f	8.15	100
1131	f	8.16	100
1132	f	8.17	100
1133	f	9.11	100
1134	f	9.12	100
1135	f	9.13	100
1136	f	9.14	100
1137	f	9.9	100
1138	f	9.15	100
1139	f	9.16	100
1140	f	9.17	100
1141	f	10.11	100
1142	f	10.12	100
1143	f	10.13	100
1144	f	10.14	100
1145	f	10.9	100
1146	f	10.15	100
1147	f	10.16	100
1148	f	10.17	100
1149	f	11.11	100
1150	f	11.12	100
1151	f	11.13	100
1152	f	11.14	100
1153	f	11.9	100
1154	f	11.15	100
1155	f	11.16	100
1156	f	11.17	100
1157	f	1.11	101
1158	f	1.12	101
1159	f	1.13	101
1160	f	1.14	101
1161	f	1.15	101
1162	f	1.16	101
1163	f	1.17	101
1164	f	1.18	101
1165	f	1.19	101
1166	f	1.21	101
1167	f	1.9	101
1168	f	1.91	101
1169	f	2.11	101
1170	f	2.12	101
1171	f	2.13	101
1172	f	2.14	101
1173	f	2.15	101
1174	f	2.16	101
1175	f	2.17	101
1176	f	2.18	101
1177	f	2.9	101
1178	f	5.11	101
1179	f	5.12	101
1180	f	5.13	101
1181	f	5.14	101
1182	f	5.15	101
1183	f	5.16	101
1184	f	5.17	101
1185	f	5.18	101
1186	f	5.19	101
1187	f	5.9	101
1188	f	5.2	101
1189	f	5.21	101
1190	f	6.11	101
1191	f	6.12	101
1192	f	6.13	101
1193	f	6.14	101
1194	f	6.9	101
1195	f	6.15	101
1196	f	6.16	101
1197	f	6.17	101
1198	f	7.11	101
1199	f	7.12	101
1200	f	7.13	101
1201	f	7.14	101
1202	f	7.9	101
1203	f	7.15	101
1204	f	7.16	101
1205	f	7.17	101
1206	f	8.11	101
1207	f	8.12	101
1208	f	8.13	101
1209	f	8.14	101
1210	f	8.9	101
1211	f	8.15	101
1212	f	8.16	101
1213	f	8.17	101
1214	f	9.11	101
1215	f	9.12	101
1216	f	9.13	101
1217	f	9.14	101
1218	f	9.9	101
1219	f	9.15	101
1220	f	9.16	101
1221	f	9.17	101
1222	f	10.11	101
1223	f	10.12	101
1224	f	10.13	101
1225	f	10.14	101
1226	f	10.9	101
1227	f	10.15	101
1228	f	10.16	101
1229	f	10.17	101
1230	f	11.11	101
1231	f	11.12	101
1232	f	11.13	101
1233	f	11.14	101
1234	f	11.9	101
1235	f	11.15	101
1236	f	11.16	101
1237	f	11.17	101
1238	f	1.11	102
1239	f	1.12	102
1240	f	1.13	102
1241	f	1.14	102
1242	f	1.15	102
1243	f	1.16	102
1244	f	1.17	102
1245	f	1.18	102
1246	f	1.19	102
1247	f	1.21	102
1248	f	1.9	102
1249	f	1.91	102
1250	f	2.11	102
1251	f	2.12	102
1252	f	2.13	102
1253	f	2.14	102
1254	f	2.15	102
1255	f	2.16	102
1256	f	2.17	102
1257	f	2.18	102
1258	f	2.9	102
1259	f	5.11	102
1260	f	5.12	102
1261	f	5.13	102
1262	f	5.14	102
1263	f	5.15	102
1264	f	5.16	102
1265	f	5.17	102
1266	f	5.18	102
1267	f	5.19	102
1268	f	5.9	102
1269	f	5.2	102
1270	f	5.21	102
1271	f	6.11	102
1272	f	6.12	102
1273	f	6.13	102
1274	f	6.14	102
1275	f	6.9	102
1276	f	6.15	102
1277	f	6.16	102
1278	f	6.17	102
1279	f	7.11	102
1280	f	7.12	102
1281	f	7.13	102
1282	f	7.14	102
1283	f	7.9	102
1284	f	7.15	102
1285	f	7.16	102
1286	f	7.17	102
1287	f	8.11	102
1288	f	8.12	102
1289	f	8.13	102
1290	f	8.14	102
1291	f	8.9	102
1292	f	8.15	102
1293	f	8.16	102
1294	f	8.17	102
1295	f	9.11	102
1296	f	9.12	102
1297	f	9.13	102
1298	f	9.14	102
1299	f	9.9	102
1300	f	9.15	102
1301	f	9.16	102
1302	f	9.17	102
1303	f	10.11	102
1304	f	10.12	102
1305	f	10.13	102
1306	f	10.14	102
1307	f	10.9	102
1308	f	10.15	102
1309	f	10.16	102
1310	f	10.17	102
1311	f	11.11	102
1312	f	11.12	102
1313	f	11.13	102
1314	f	11.14	102
1315	f	11.9	102
1316	f	11.15	102
1317	f	11.16	102
1318	f	11.17	102
1319	f	1.11	103
1320	f	1.12	103
1321	f	1.13	103
1322	f	1.14	103
1323	f	1.15	103
1324	f	1.16	103
1325	f	1.17	103
1326	f	1.18	103
1327	f	1.19	103
1328	f	1.21	103
1329	f	1.9	103
1330	f	1.91	103
1331	f	2.11	103
1332	f	2.12	103
1333	f	2.13	103
1334	f	2.14	103
1335	f	2.15	103
1336	f	2.16	103
1337	f	2.17	103
1338	f	2.18	103
1339	f	2.9	103
1340	f	5.11	103
1341	f	5.12	103
1342	f	5.13	103
1343	f	5.14	103
1344	f	5.15	103
1345	f	5.16	103
1346	f	5.17	103
1347	f	5.18	103
1348	f	5.19	103
1349	f	5.9	103
1350	f	5.2	103
1351	f	5.21	103
1352	f	6.11	103
1353	f	6.12	103
1354	f	6.13	103
1355	f	6.14	103
1356	f	6.9	103
1357	f	6.15	103
1358	f	6.16	103
1359	f	6.17	103
1360	f	7.11	103
1361	f	7.12	103
1362	f	7.13	103
1363	f	7.14	103
1364	f	7.9	103
1365	f	7.15	103
1366	f	7.16	103
1367	f	7.17	103
1368	f	8.11	103
1369	f	8.12	103
1370	f	8.13	103
1371	f	8.14	103
1372	f	8.9	103
1373	f	8.15	103
1374	f	8.16	103
1375	f	8.17	103
1376	f	9.11	103
1377	f	9.12	103
1378	f	9.13	103
1379	f	9.14	103
1380	f	9.9	103
1381	f	9.15	103
1382	f	9.16	103
1383	f	9.17	103
1384	f	10.11	103
1385	f	10.12	103
1386	f	10.13	103
1387	f	10.14	103
1388	f	10.9	103
1389	f	10.15	103
1390	f	10.16	103
1391	f	10.17	103
1392	f	11.11	103
1393	f	11.12	103
1394	f	11.13	103
1395	f	11.14	103
1396	f	11.9	103
1397	f	11.15	103
1398	f	11.16	103
1399	f	11.17	103
1400	f	1.11	104
1401	f	1.12	104
1402	f	1.13	104
1403	f	1.14	104
1404	f	1.15	104
1405	f	1.16	104
1406	f	1.17	104
1407	f	1.18	104
1408	f	1.19	104
1409	f	1.21	104
1410	f	1.9	104
1411	f	1.91	104
1412	f	2.11	104
1413	f	2.12	104
1414	f	2.13	104
1415	f	2.14	104
1416	f	2.15	104
1417	f	2.16	104
1418	f	2.17	104
1419	f	2.18	104
1420	f	2.9	104
1421	f	5.11	104
1422	f	5.12	104
1423	f	5.13	104
1424	f	5.14	104
1425	f	5.15	104
1426	f	5.16	104
1427	f	5.17	104
1428	f	5.18	104
1429	f	5.19	104
1430	f	5.9	104
1431	f	5.2	104
1432	f	5.21	104
1433	f	6.11	104
1434	f	6.12	104
1435	f	6.13	104
1436	f	6.14	104
1437	f	6.9	104
1438	f	6.15	104
1439	f	6.16	104
1440	f	6.17	104
1441	f	7.11	104
1442	f	7.12	104
1443	f	7.13	104
1444	f	7.14	104
1445	f	7.9	104
1446	f	7.15	104
1447	f	7.16	104
1448	f	7.17	104
1449	f	8.11	104
1450	f	8.12	104
1451	f	8.13	104
1452	f	8.14	104
1453	f	8.9	104
1454	f	8.15	104
1455	f	8.16	104
1456	f	8.17	104
1457	f	9.11	104
1458	f	9.12	104
1459	f	9.13	104
1460	f	9.14	104
1461	f	9.9	104
1462	f	9.15	104
1463	f	9.16	104
1464	f	9.17	104
1465	f	10.11	104
1466	f	10.12	104
1467	f	10.13	104
1468	f	10.14	104
1469	f	10.9	104
1470	f	10.15	104
1471	f	10.16	104
1472	f	10.17	104
1473	f	11.11	104
1474	f	11.12	104
1475	f	11.13	104
1476	f	11.14	104
1477	f	11.9	104
1478	f	11.15	104
1479	f	11.16	104
1480	f	11.17	104
1481	f	1.11	105
1482	f	1.12	105
1483	f	1.13	105
1484	f	1.14	105
1485	f	1.15	105
1486	f	1.16	105
1487	f	1.17	105
1488	f	1.18	105
1489	f	1.19	105
1490	f	1.21	105
1491	f	1.9	105
1492	f	1.91	105
1493	f	2.11	105
1494	f	2.12	105
1495	f	2.13	105
1496	f	2.14	105
1497	f	2.15	105
1498	f	2.16	105
1499	f	2.17	105
1500	f	2.18	105
1501	f	2.9	105
1502	f	5.11	105
1503	f	5.12	105
1504	f	5.13	105
1505	f	5.14	105
1506	f	5.15	105
1507	f	5.16	105
1508	f	5.17	105
1509	f	5.18	105
1510	f	5.19	105
1511	f	5.9	105
1512	f	5.2	105
1513	f	5.21	105
1514	f	6.11	105
1515	f	6.12	105
1516	f	6.13	105
1517	f	6.14	105
1518	f	6.9	105
1519	f	6.15	105
1520	f	6.16	105
1521	f	6.17	105
1522	f	7.11	105
1523	f	7.12	105
1524	f	7.13	105
1525	f	7.14	105
1526	f	7.9	105
1527	f	7.15	105
1528	f	7.16	105
1529	f	7.17	105
1530	f	8.11	105
1531	f	8.12	105
1532	f	8.13	105
1533	f	8.14	105
1534	f	8.9	105
1535	f	8.15	105
1536	f	8.16	105
1537	f	8.17	105
1538	f	9.11	105
1539	f	9.12	105
1540	f	9.13	105
1541	f	9.14	105
1542	f	9.9	105
1543	f	9.15	105
1544	f	9.16	105
1545	f	9.17	105
1546	f	10.11	105
1547	f	10.12	105
1548	f	10.13	105
1549	f	10.14	105
1550	f	10.9	105
1551	f	10.15	105
1552	f	10.16	105
1553	f	10.17	105
1554	f	11.11	105
1555	f	11.12	105
1556	f	11.13	105
1557	f	11.14	105
1558	f	11.9	105
1559	f	11.15	105
1560	f	11.16	105
1561	f	11.17	105
1562	f	1.11	106
1563	f	1.12	106
1564	f	1.13	106
1565	f	1.14	106
1566	f	1.15	106
1567	f	1.16	106
1568	f	1.17	106
1569	f	1.18	106
1570	f	1.19	106
1571	f	1.21	106
1572	f	1.9	106
1573	f	1.91	106
1574	f	2.11	106
1575	f	2.12	106
1576	f	2.13	106
1577	f	2.14	106
1578	f	2.15	106
1579	f	2.16	106
1580	f	2.17	106
1581	f	2.18	106
1582	f	2.9	106
1583	f	5.11	106
1584	f	5.12	106
1585	f	5.13	106
1586	f	5.14	106
1587	f	5.15	106
1588	f	5.16	106
1589	f	5.17	106
1590	f	5.18	106
1591	f	5.19	106
1592	f	5.9	106
1593	f	5.2	106
1594	f	5.21	106
1595	f	6.11	106
1596	f	6.12	106
1597	f	6.13	106
1598	f	6.14	106
1599	f	6.9	106
1600	f	6.15	106
1601	f	6.16	106
1602	f	6.17	106
1603	f	7.11	106
1604	f	7.12	106
1605	f	7.13	106
1606	f	7.14	106
1607	f	7.9	106
1608	f	7.15	106
1609	f	7.16	106
1610	f	7.17	106
1611	f	8.11	106
1612	f	8.12	106
1613	f	8.13	106
1614	f	8.14	106
1615	f	8.9	106
1616	f	8.15	106
1617	f	8.16	106
1618	f	8.17	106
1619	f	9.11	106
1620	f	9.12	106
1621	f	9.13	106
1622	f	9.14	106
1623	f	9.9	106
1624	f	9.15	106
1625	f	9.16	106
1626	f	9.17	106
1627	f	10.11	106
1628	f	10.12	106
1629	f	10.13	106
1630	f	10.14	106
1631	f	10.9	106
1632	f	10.15	106
1633	f	10.16	106
1634	f	10.17	106
1635	f	11.11	106
1636	f	11.12	106
1637	f	11.13	106
1638	f	11.14	106
1639	f	11.9	106
1640	f	11.15	106
1641	f	11.16	106
1642	f	11.17	106
1643	f	1.11	107
1644	f	1.12	107
1645	f	1.13	107
1646	f	1.14	107
1647	f	1.15	107
1648	f	1.16	107
1649	f	1.17	107
1650	f	1.18	107
1651	f	1.19	107
1652	f	1.21	107
1653	f	1.9	107
1654	f	1.91	107
1655	f	2.11	107
1656	f	2.12	107
1657	f	2.13	107
1658	f	2.14	107
1659	f	2.15	107
1660	f	2.16	107
1661	f	2.17	107
1662	f	2.18	107
1663	f	2.9	107
1664	f	5.11	107
1665	f	5.12	107
1666	f	5.13	107
1667	f	5.14	107
1668	f	5.15	107
1669	f	5.16	107
1670	f	5.17	107
1671	f	5.18	107
1672	f	5.19	107
1673	f	5.9	107
1674	f	5.2	107
1675	f	5.21	107
1676	f	6.11	107
1677	f	6.12	107
1678	f	6.13	107
1679	f	6.14	107
1680	f	6.9	107
1681	f	6.15	107
1682	f	6.16	107
1683	f	6.17	107
1684	f	7.11	107
1685	f	7.12	107
1686	f	7.13	107
1687	f	7.14	107
1688	f	7.9	107
1689	f	7.15	107
1690	f	7.16	107
1691	f	7.17	107
1692	f	8.11	107
1693	f	8.12	107
1694	f	8.13	107
1695	f	8.14	107
1696	f	8.9	107
1697	f	8.15	107
1698	f	8.16	107
1699	f	8.17	107
1700	f	9.11	107
1701	f	9.12	107
1702	f	9.13	107
1703	f	9.14	107
1704	f	9.9	107
1705	f	9.15	107
1706	f	9.16	107
1707	f	9.17	107
1708	f	10.11	107
1709	f	10.12	107
1710	f	10.13	107
1711	f	10.14	107
1712	f	10.9	107
1713	f	10.15	107
1714	f	10.16	107
1715	f	10.17	107
1716	f	11.11	107
1717	f	11.12	107
1718	f	11.13	107
1719	f	11.14	107
1720	f	11.9	107
1721	f	11.15	107
1722	f	11.16	107
1723	f	11.17	107
1724	f	1.11	108
1725	f	1.12	108
1726	f	1.13	108
1727	f	1.14	108
1728	f	1.15	108
1729	f	1.16	108
1730	f	1.17	108
1731	f	1.18	108
1732	f	1.19	108
1733	f	1.21	108
1734	f	1.9	108
1735	f	1.91	108
1736	f	2.11	108
1737	f	2.12	108
1738	f	2.13	108
1739	f	2.14	108
1740	f	2.15	108
1741	f	2.16	108
1742	f	2.17	108
1743	f	2.18	108
1744	f	2.9	108
1745	f	5.11	108
1746	f	5.12	108
1747	f	5.13	108
1748	f	5.14	108
1749	f	5.15	108
1750	f	5.16	108
1751	f	5.17	108
1752	f	5.18	108
1753	f	5.19	108
1754	f	5.9	108
1755	f	5.2	108
1756	f	5.21	108
1757	f	6.11	108
1758	f	6.12	108
1759	f	6.13	108
1760	f	6.14	108
1761	f	6.9	108
1762	f	6.15	108
1763	f	6.16	108
1764	f	6.17	108
1765	f	7.11	108
1766	f	7.12	108
1767	f	7.13	108
1768	f	7.14	108
1769	f	7.9	108
1770	f	7.15	108
1771	f	7.16	108
1772	f	7.17	108
1773	f	8.11	108
1774	f	8.12	108
1775	f	8.13	108
1776	f	8.14	108
1777	f	8.9	108
1778	f	8.15	108
1779	f	8.16	108
1780	f	8.17	108
1781	f	9.11	108
1782	f	9.12	108
1783	f	9.13	108
1784	f	9.14	108
1785	f	9.9	108
1786	f	9.15	108
1787	f	9.16	108
1788	f	9.17	108
1789	f	10.11	108
1790	f	10.12	108
1791	f	10.13	108
1792	f	10.14	108
1793	f	10.9	108
1794	f	10.15	108
1795	f	10.16	108
1796	f	10.17	108
1797	f	11.11	108
1798	f	11.12	108
1799	f	11.13	108
1800	f	11.14	108
1801	f	11.9	108
1802	f	11.15	108
1803	f	11.16	108
1804	f	11.17	108
1805	f	1.11	109
1806	f	1.12	109
1807	f	1.13	109
1808	f	1.14	109
1809	f	1.15	109
1810	f	1.16	109
1811	f	1.17	109
1812	f	1.18	109
1813	f	1.19	109
1814	f	1.21	109
1815	f	1.9	109
1816	f	1.91	109
1817	f	2.11	109
1818	f	2.12	109
1819	f	2.13	109
1820	f	2.14	109
1821	f	2.15	109
1822	f	2.16	109
1823	f	2.17	109
1824	f	2.18	109
1825	f	2.9	109
1826	f	5.11	109
1827	f	5.12	109
1828	f	5.13	109
1829	f	5.14	109
1830	f	5.15	109
1831	f	5.16	109
1832	f	5.17	109
1833	f	5.18	109
1834	f	5.19	109
1835	f	5.9	109
1836	f	5.2	109
1837	f	5.21	109
1838	f	6.11	109
1839	f	6.12	109
1840	f	6.13	109
1841	f	6.14	109
1842	f	6.9	109
1843	f	6.15	109
1844	f	6.16	109
1845	f	6.17	109
1846	f	7.11	109
1847	f	7.12	109
1848	f	7.13	109
1849	f	7.14	109
1850	f	7.9	109
1851	f	7.15	109
1852	f	7.16	109
1853	f	7.17	109
1854	f	8.11	109
1855	f	8.12	109
1856	f	8.13	109
1857	f	8.14	109
1858	f	8.9	109
1859	f	8.15	109
1860	f	8.16	109
1861	f	8.17	109
1862	f	9.11	109
1863	f	9.12	109
1864	f	9.13	109
1865	f	9.14	109
1866	f	9.9	109
1867	f	9.15	109
1868	f	9.16	109
1869	f	9.17	109
1870	f	10.11	109
1871	f	10.12	109
1872	f	10.13	109
1873	f	10.14	109
1874	f	10.9	109
1875	f	10.15	109
1876	f	10.16	109
1877	f	10.17	109
1878	f	11.11	109
1879	f	11.12	109
1880	f	11.13	109
1881	f	11.14	109
1882	f	11.9	109
1883	f	11.15	109
1884	f	11.16	109
1885	f	11.17	109
1886	f	1.11	110
1887	f	1.12	110
1888	f	1.13	110
1889	f	1.14	110
1890	f	1.15	110
1891	f	1.16	110
1892	f	1.17	110
1893	f	1.18	110
1894	f	1.19	110
1895	f	1.21	110
1896	f	1.9	110
1897	f	1.91	110
1898	f	2.11	110
1899	f	2.12	110
1900	f	2.13	110
1901	f	2.14	110
1902	f	2.15	110
1903	f	2.16	110
1904	f	2.17	110
1905	f	2.18	110
1906	f	2.9	110
1907	f	5.11	110
1908	f	5.12	110
1909	f	5.13	110
1910	f	5.14	110
1911	f	5.15	110
1912	f	5.16	110
1913	f	5.17	110
1914	f	5.18	110
1915	f	5.19	110
1916	f	5.9	110
1917	f	5.2	110
1918	f	5.21	110
1919	f	6.11	110
1920	f	6.12	110
1921	f	6.13	110
1922	f	6.14	110
1923	f	6.9	110
1924	f	6.15	110
1925	f	6.16	110
1926	f	6.17	110
1927	f	7.11	110
1928	f	7.12	110
1929	f	7.13	110
1930	f	7.14	110
1931	f	7.9	110
1932	f	7.15	110
1933	f	7.16	110
1934	f	7.17	110
1935	f	8.11	110
1936	f	8.12	110
1937	f	8.13	110
1938	f	8.14	110
1939	f	8.9	110
1940	f	8.15	110
1941	f	8.16	110
1942	f	8.17	110
1943	f	9.11	110
1944	f	9.12	110
1945	f	9.13	110
1946	f	9.14	110
1947	f	9.9	110
1948	f	9.15	110
1949	f	9.16	110
1950	f	9.17	110
1951	f	10.11	110
1952	f	10.12	110
1953	f	10.13	110
1954	f	10.14	110
1955	f	10.9	110
1956	f	10.15	110
1957	f	10.16	110
1958	f	10.17	110
1959	f	11.11	110
1960	f	11.12	110
1961	f	11.13	110
1962	f	11.14	110
1963	f	11.9	110
1964	f	11.15	110
1965	f	11.16	110
1966	f	11.17	110
1967	f	1.11	111
1968	f	1.12	111
1969	f	1.13	111
1970	f	1.14	111
1971	f	1.15	111
1972	f	1.16	111
1973	f	1.17	111
1974	f	1.18	111
1975	f	1.19	111
1976	f	1.21	111
1977	f	1.9	111
1978	f	1.91	111
1979	f	2.11	111
1980	f	2.12	111
1981	f	2.13	111
1982	f	2.14	111
1983	f	2.15	111
1984	f	2.16	111
1985	f	2.17	111
1986	f	2.18	111
1987	f	2.9	111
1988	f	5.11	111
1989	f	5.12	111
1990	f	5.13	111
1991	f	5.14	111
1992	f	5.15	111
1993	f	5.16	111
1994	f	5.17	111
1995	f	5.18	111
1996	f	5.19	111
1997	f	5.9	111
1998	f	5.2	111
1999	f	5.21	111
2000	f	6.11	111
2001	f	6.12	111
2002	f	6.13	111
2003	f	6.14	111
2004	f	6.9	111
2005	f	6.15	111
2006	f	6.16	111
2007	f	6.17	111
2008	f	7.11	111
2009	f	7.12	111
2010	f	7.13	111
2011	f	7.14	111
2012	f	7.9	111
2013	f	7.15	111
2014	f	7.16	111
2015	f	7.17	111
2016	f	8.11	111
2017	f	8.12	111
2018	f	8.13	111
2019	f	8.14	111
2020	f	8.9	111
2021	f	8.15	111
2022	f	8.16	111
2023	f	8.17	111
2024	f	9.11	111
2025	f	9.12	111
2026	f	9.13	111
2027	f	9.14	111
2028	f	9.9	111
2029	f	9.15	111
2030	f	9.16	111
2031	f	9.17	111
2032	f	10.11	111
2033	f	10.12	111
2034	f	10.13	111
2035	f	10.14	111
2036	f	10.9	111
2037	f	10.15	111
2038	f	10.16	111
2039	f	10.17	111
2040	f	11.11	111
2041	f	11.12	111
2042	f	11.13	111
2043	f	11.14	111
2044	f	11.9	111
2045	f	11.15	111
2046	f	11.16	111
2047	f	11.17	111
2048	f	1.11	112
2049	f	1.12	112
2050	f	1.13	112
2051	f	1.14	112
2052	f	1.15	112
2053	f	1.16	112
2054	f	1.17	112
2055	f	1.18	112
2056	f	1.19	112
2057	f	1.21	112
2058	f	1.9	112
2059	f	1.91	112
2060	f	2.11	112
2061	f	2.12	112
2062	f	2.13	112
2063	f	2.14	112
2064	f	2.15	112
2065	f	2.16	112
2066	f	2.17	112
2067	f	2.18	112
2068	f	2.9	112
2069	f	5.11	112
2070	f	5.12	112
2071	f	5.13	112
2072	f	5.14	112
2073	f	5.15	112
2074	f	5.16	112
2075	f	5.17	112
2076	f	5.18	112
2077	f	5.19	112
2078	f	5.9	112
2079	f	5.2	112
2080	f	5.21	112
2081	f	6.11	112
2082	f	6.12	112
2083	f	6.13	112
2084	f	6.14	112
2085	f	6.9	112
2086	f	6.15	112
2087	f	6.16	112
2088	f	6.17	112
2089	f	7.11	112
2090	f	7.12	112
2091	f	7.13	112
2092	f	7.14	112
2093	f	7.9	112
2094	f	7.15	112
2095	f	7.16	112
2096	f	7.17	112
2097	f	8.11	112
2098	f	8.12	112
2099	f	8.13	112
2100	f	8.14	112
2101	f	8.9	112
2102	f	8.15	112
2103	f	8.16	112
2104	f	8.17	112
2105	f	9.11	112
2106	f	9.12	112
2107	f	9.13	112
2108	f	9.14	112
2109	f	9.9	112
2110	f	9.15	112
2111	f	9.16	112
2112	f	9.17	112
2113	f	10.11	112
2114	f	10.12	112
2115	f	10.13	112
2116	f	10.14	112
2117	f	10.9	112
2118	f	10.15	112
2119	f	10.16	112
2120	f	10.17	112
2121	f	11.11	112
2122	f	11.12	112
2123	f	11.13	112
2124	f	11.14	112
2125	f	11.9	112
2126	f	11.15	112
2127	f	11.16	112
2128	f	11.17	112
2129	f	1.11	113
2130	f	1.12	113
2131	f	1.13	113
2132	f	1.14	113
2133	f	1.15	113
2134	f	1.16	113
2135	f	1.17	113
2136	f	1.18	113
2137	f	1.19	113
2138	f	1.21	113
2139	f	1.9	113
2140	f	1.91	113
2141	f	2.11	113
2142	f	2.12	113
2143	f	2.13	113
2144	f	2.14	113
2145	f	2.15	113
2146	f	2.16	113
2147	f	2.17	113
2148	f	2.18	113
2149	f	2.9	113
2150	f	5.11	113
2151	f	5.12	113
2152	f	5.13	113
2153	f	5.14	113
2154	f	5.15	113
2155	f	5.16	113
2156	f	5.17	113
2157	f	5.18	113
2158	f	5.19	113
2159	f	5.9	113
2160	f	5.2	113
2161	f	5.21	113
2162	f	6.11	113
2163	f	6.12	113
2164	f	6.13	113
2165	f	6.14	113
2166	f	6.9	113
2167	f	6.15	113
2168	f	6.16	113
2169	f	6.17	113
2170	f	7.11	113
2171	f	7.12	113
2172	f	7.13	113
2173	f	7.14	113
2174	f	7.9	113
2175	f	7.15	113
2176	f	7.16	113
2177	f	7.17	113
2178	f	8.11	113
2179	f	8.12	113
2180	f	8.13	113
2181	f	8.14	113
2182	f	8.9	113
2183	f	8.15	113
2184	f	8.16	113
2185	f	8.17	113
2186	f	9.11	113
2187	f	9.12	113
2188	f	9.13	113
2189	f	9.14	113
2190	f	9.9	113
2191	f	9.15	113
2192	f	9.16	113
2193	f	9.17	113
2194	f	10.11	113
2195	f	10.12	113
2196	f	10.13	113
2197	f	10.14	113
2198	f	10.9	113
2199	f	10.15	113
2200	f	10.16	113
2201	f	10.17	113
2202	f	11.11	113
2203	f	11.12	113
2204	f	11.13	113
2205	f	11.14	113
2206	f	11.9	113
2207	f	11.15	113
2208	f	11.16	113
2209	f	11.17	113
2210	f	1.11	114
2211	f	1.12	114
2212	f	1.13	114
2213	f	1.14	114
2214	f	1.15	114
2215	f	1.16	114
2216	f	1.17	114
2217	f	1.18	114
2218	f	1.19	114
2219	f	1.21	114
2220	f	1.9	114
2221	f	1.91	114
2222	f	2.11	114
2223	f	2.12	114
2224	f	2.13	114
2225	f	2.14	114
2226	f	2.15	114
2227	f	2.16	114
2228	f	2.17	114
2229	f	2.18	114
2230	f	2.9	114
2231	f	5.11	114
2232	f	5.12	114
2233	f	5.13	114
2234	f	5.14	114
2235	f	5.15	114
2236	f	5.16	114
2237	f	5.17	114
2238	f	5.18	114
2239	f	5.19	114
2240	f	5.9	114
2241	f	5.2	114
2242	f	5.21	114
2243	f	6.11	114
2244	f	6.12	114
2245	f	6.13	114
2246	f	6.14	114
2247	f	6.9	114
2248	f	6.15	114
2249	f	6.16	114
2250	f	6.17	114
2251	f	7.11	114
2252	f	7.12	114
2253	f	7.13	114
2254	f	7.14	114
2255	f	7.9	114
2256	f	7.15	114
2257	f	7.16	114
2258	f	7.17	114
2259	f	8.11	114
2260	f	8.12	114
2261	f	8.13	114
2262	f	8.14	114
2263	f	8.9	114
2264	f	8.15	114
2265	f	8.16	114
2266	f	8.17	114
2267	f	9.11	114
2268	f	9.12	114
2269	f	9.13	114
2270	f	9.14	114
2271	f	9.9	114
2272	f	9.15	114
2273	f	9.16	114
2274	f	9.17	114
2275	f	10.11	114
2276	f	10.12	114
2277	f	10.13	114
2278	f	10.14	114
2279	f	10.9	114
2280	f	10.15	114
2281	f	10.16	114
2282	f	10.17	114
2283	f	11.11	114
2284	f	11.12	114
2285	f	11.13	114
2286	f	11.14	114
2287	f	11.9	114
2288	f	11.15	114
2289	f	11.16	114
2290	f	11.17	114
2291	f	1.11	115
2292	f	1.12	115
2293	f	1.13	115
2294	f	1.14	115
2295	f	1.15	115
2296	f	1.16	115
2297	f	1.17	115
2298	f	1.18	115
2299	f	1.19	115
2300	f	1.21	115
2301	f	1.9	115
2302	f	1.91	115
2303	f	2.11	115
2304	f	2.12	115
2305	f	2.13	115
2306	f	2.14	115
2307	f	2.15	115
2308	f	2.16	115
2309	f	2.17	115
2310	f	2.18	115
2311	f	2.9	115
2312	f	5.11	115
2313	f	5.12	115
2314	f	5.13	115
2315	f	5.14	115
2316	f	5.15	115
2317	f	5.16	115
2318	f	5.17	115
2319	f	5.18	115
2320	f	5.19	115
2321	f	5.9	115
2322	f	5.2	115
2323	f	5.21	115
2324	f	6.11	115
2325	f	6.12	115
2326	f	6.13	115
2327	f	6.14	115
2328	f	6.9	115
2329	f	6.15	115
2330	f	6.16	115
2331	f	6.17	115
2332	f	7.11	115
2333	f	7.12	115
2334	f	7.13	115
2335	f	7.14	115
2336	f	7.9	115
2337	f	7.15	115
2338	f	7.16	115
2339	f	7.17	115
2340	f	8.11	115
2341	f	8.12	115
2342	f	8.13	115
2343	f	8.14	115
2344	f	8.9	115
2345	f	8.15	115
2346	f	8.16	115
2347	f	8.17	115
2348	f	9.11	115
2349	f	9.12	115
2350	f	9.13	115
2351	f	9.14	115
2352	f	9.9	115
2353	f	9.15	115
2354	f	9.16	115
2355	f	9.17	115
2356	f	10.11	115
2357	f	10.12	115
2358	f	10.13	115
2359	f	10.14	115
2360	f	10.9	115
2361	f	10.15	115
2362	f	10.16	115
2363	f	10.17	115
2364	f	11.11	115
2365	f	11.12	115
2366	f	11.13	115
2367	f	11.14	115
2368	f	11.9	115
2369	f	11.15	115
2370	f	11.16	115
2371	f	11.17	115
2372	f	1.11	116
2373	f	1.12	116
2374	f	1.13	116
2375	f	1.14	116
2376	f	1.15	116
2377	f	1.16	116
2378	f	1.17	116
2379	f	1.18	116
2380	f	1.19	116
2381	f	1.21	116
2382	f	1.9	116
2383	f	1.91	116
2384	f	2.11	116
2385	f	2.12	116
2386	f	2.13	116
2387	f	2.14	116
2388	f	2.15	116
2389	f	2.16	116
2390	f	2.17	116
2391	f	2.18	116
2392	f	2.9	116
2393	f	5.11	116
2394	f	5.12	116
2395	f	5.13	116
2396	f	5.14	116
2397	f	5.15	116
2398	f	5.16	116
2399	f	5.17	116
2400	f	5.18	116
2401	f	5.19	116
2402	f	5.9	116
2403	f	5.2	116
2404	f	5.21	116
2405	f	6.11	116
2406	f	6.12	116
2407	f	6.13	116
2408	f	6.14	116
2409	f	6.9	116
2410	f	6.15	116
2411	f	6.16	116
2412	f	6.17	116
2413	f	7.11	116
2414	f	7.12	116
2415	f	7.13	116
2416	f	7.14	116
2417	f	7.9	116
2418	f	7.15	116
2419	f	7.16	116
2420	f	7.17	116
2421	f	8.11	116
2422	f	8.12	116
2423	f	8.13	116
2424	f	8.14	116
2425	f	8.9	116
2426	f	8.15	116
2427	f	8.16	116
2428	f	8.17	116
2429	f	9.11	116
2430	f	9.12	116
2431	f	9.13	116
2432	f	9.14	116
2433	f	9.9	116
2434	f	9.15	116
2435	f	9.16	116
2436	f	9.17	116
2437	f	10.11	116
2438	f	10.12	116
2439	f	10.13	116
2440	f	10.14	116
2441	f	10.9	116
2442	f	10.15	116
2443	f	10.16	116
2444	f	10.17	116
2445	f	11.11	116
2446	f	11.12	116
2447	f	11.13	116
2448	f	11.14	116
2449	f	11.9	116
2450	f	11.15	116
2451	f	11.16	116
2452	f	11.17	116
2453	f	1.11	117
2454	f	1.12	117
2455	f	1.13	117
2456	f	1.14	117
2457	f	1.15	117
2458	f	1.16	117
2459	f	1.17	117
2460	f	1.18	117
2461	f	1.19	117
2462	f	1.21	117
2463	f	1.9	117
2464	f	1.91	117
2465	f	2.11	117
2466	f	2.12	117
2467	f	2.13	117
2468	f	2.14	117
2469	f	2.15	117
2470	f	2.16	117
2471	f	2.17	117
2472	f	2.18	117
2473	f	2.9	117
2474	f	5.11	117
2475	f	5.12	117
2476	f	5.13	117
2477	f	5.14	117
2478	f	5.15	117
2479	f	5.16	117
2480	f	5.17	117
2481	f	5.18	117
2482	f	5.19	117
2483	f	5.9	117
2484	f	5.2	117
2485	f	5.21	117
2486	f	6.11	117
2487	f	6.12	117
2488	f	6.13	117
2489	f	6.14	117
2490	f	6.9	117
2491	f	6.15	117
2492	f	6.16	117
2493	f	6.17	117
2494	f	7.11	117
2495	f	7.12	117
2496	f	7.13	117
2497	f	7.14	117
2498	f	7.9	117
2499	f	7.15	117
2500	f	7.16	117
2501	f	7.17	117
2502	f	8.11	117
2503	f	8.12	117
2504	f	8.13	117
2505	f	8.14	117
2506	f	8.9	117
2507	f	8.15	117
2508	f	8.16	117
2509	f	8.17	117
2510	f	9.11	117
2511	f	9.12	117
2512	f	9.13	117
2513	f	9.14	117
2514	f	9.9	117
2515	f	9.15	117
2516	f	9.16	117
2517	f	9.17	117
2518	f	10.11	117
2519	f	10.12	117
2520	f	10.13	117
2521	f	10.14	117
2522	f	10.9	117
2523	f	10.15	117
2524	f	10.16	117
2525	f	10.17	117
2526	f	11.11	117
2527	f	11.12	117
2528	f	11.13	117
2529	f	11.14	117
2530	f	11.9	117
2531	f	11.15	117
2532	f	11.16	117
2533	f	11.17	117
2534	f	1.11	118
2535	f	1.12	118
2536	f	1.13	118
2537	f	1.14	118
2538	f	1.15	118
2539	f	1.16	118
2540	f	1.17	118
2541	f	1.18	118
2542	f	1.19	118
2543	f	1.21	118
2544	f	1.9	118
2545	f	1.91	118
2546	f	2.11	118
2547	f	2.12	118
2548	f	2.13	118
2549	f	2.14	118
2550	f	2.15	118
2551	f	2.16	118
2552	f	2.17	118
2553	f	2.18	118
2554	f	2.9	118
2555	f	5.11	118
2556	f	5.12	118
2557	f	5.13	118
2558	f	5.14	118
2559	f	5.15	118
2560	f	5.16	118
2561	f	5.17	118
2562	f	5.18	118
2563	f	5.19	118
2564	f	5.9	118
2565	f	5.2	118
2566	f	5.21	118
2567	f	6.11	118
2568	f	6.12	118
2569	f	6.13	118
2570	f	6.14	118
2571	f	6.9	118
2572	f	6.15	118
2573	f	6.16	118
2574	f	6.17	118
2575	f	7.11	118
2576	f	7.12	118
2577	f	7.13	118
2578	f	7.14	118
2579	f	7.9	118
2580	f	7.15	118
2581	f	7.16	118
2582	f	7.17	118
2583	f	8.11	118
2584	f	8.12	118
2585	f	8.13	118
2586	f	8.14	118
2587	f	8.9	118
2588	f	8.15	118
2589	f	8.16	118
2590	f	8.17	118
2591	f	9.11	118
2592	f	9.12	118
2593	f	9.13	118
2594	f	9.14	118
2595	f	9.9	118
2596	f	9.15	118
2597	f	9.16	118
2598	f	9.17	118
2599	f	10.11	118
2600	f	10.12	118
2601	f	10.13	118
2602	f	10.14	118
2603	f	10.9	118
2604	f	10.15	118
2605	f	10.16	118
2606	f	10.17	118
2607	f	11.11	118
2608	f	11.12	118
2609	f	11.13	118
2610	f	11.14	118
2611	f	11.9	118
2612	f	11.15	118
2613	f	11.16	118
2614	f	11.17	118
2615	f	1.11	119
2616	f	1.12	119
2617	f	1.13	119
2618	f	1.14	119
2619	f	1.15	119
2620	f	1.16	119
2621	f	1.17	119
2622	f	1.18	119
2623	f	1.19	119
2624	f	1.21	119
2625	f	1.9	119
2626	f	1.91	119
2627	f	2.11	119
2628	f	2.12	119
2629	f	2.13	119
2630	f	2.14	119
2631	f	2.15	119
2632	f	2.16	119
2633	f	2.17	119
2634	f	2.18	119
2635	f	2.9	119
2636	f	5.11	119
2637	f	5.12	119
2638	f	5.13	119
2639	f	5.14	119
2640	f	5.15	119
2641	f	5.16	119
2642	f	5.17	119
2643	f	5.18	119
2644	f	5.19	119
2645	f	5.9	119
2646	f	5.2	119
2647	f	5.21	119
2648	f	6.11	119
2649	f	6.12	119
2650	f	6.13	119
2651	f	6.14	119
2652	f	6.9	119
2653	f	6.15	119
2654	f	6.16	119
2655	f	6.17	119
2656	f	7.11	119
2657	f	7.12	119
2658	f	7.13	119
2659	f	7.14	119
2660	f	7.9	119
2661	f	7.15	119
2662	f	7.16	119
2663	f	7.17	119
2664	f	8.11	119
2665	f	8.12	119
2666	f	8.13	119
2667	f	8.14	119
2668	f	8.9	119
2669	f	8.15	119
2670	f	8.16	119
2671	f	8.17	119
2672	f	9.11	119
2673	f	9.12	119
2674	f	9.13	119
2675	f	9.14	119
2676	f	9.9	119
2677	f	9.15	119
2678	f	9.16	119
2679	f	9.17	119
2680	f	10.11	119
2681	f	10.12	119
2682	f	10.13	119
2683	f	10.14	119
2684	f	10.9	119
2685	f	10.15	119
2686	f	10.16	119
2687	f	10.17	119
2688	f	11.11	119
2689	f	11.12	119
2690	f	11.13	119
2691	f	11.14	119
2692	f	11.9	119
2693	f	11.15	119
2694	f	11.16	119
2695	f	11.17	119
2696	f	1.11	120
2697	f	1.12	120
2698	f	1.13	120
2699	f	1.14	120
2700	f	1.15	120
2701	f	1.16	120
2702	f	1.17	120
2703	f	1.18	120
2704	f	1.19	120
2705	f	1.21	120
2706	f	1.9	120
2707	f	1.91	120
2708	f	2.11	120
2709	f	2.12	120
2710	f	2.13	120
2711	f	2.14	120
2712	f	2.15	120
2713	f	2.16	120
2714	f	2.17	120
2715	f	2.18	120
2716	f	2.9	120
2717	f	5.11	120
2718	f	5.12	120
2719	f	5.13	120
2720	f	5.14	120
2721	f	5.15	120
2722	f	5.16	120
2723	f	5.17	120
2724	f	5.18	120
2725	f	5.19	120
2726	f	5.9	120
2727	f	5.2	120
2728	f	5.21	120
2729	f	6.11	120
2730	f	6.12	120
2731	f	6.13	120
2732	f	6.14	120
2733	f	6.9	120
2734	f	6.15	120
2735	f	6.16	120
2736	f	6.17	120
2737	f	7.11	120
2738	f	7.12	120
2739	f	7.13	120
2740	f	7.14	120
2741	f	7.9	120
2742	f	7.15	120
2743	f	7.16	120
2744	f	7.17	120
2745	f	8.11	120
2746	f	8.12	120
2747	f	8.13	120
2748	f	8.14	120
2749	f	8.9	120
2750	f	8.15	120
2751	f	8.16	120
2752	f	8.17	120
2753	f	9.11	120
2754	f	9.12	120
2755	f	9.13	120
2756	f	9.14	120
2757	f	9.9	120
2758	f	9.15	120
2759	f	9.16	120
2760	f	9.17	120
2761	f	10.11	120
2762	f	10.12	120
2763	f	10.13	120
2764	f	10.14	120
2765	f	10.9	120
2766	f	10.15	120
2767	f	10.16	120
2768	f	10.17	120
2769	f	11.11	120
2770	f	11.12	120
2771	f	11.13	120
2772	f	11.14	120
2773	f	11.9	120
2774	f	11.15	120
2775	f	11.16	120
2776	f	11.17	120
2777	f	1.11	121
2778	f	1.12	121
2779	f	1.13	121
2780	f	1.14	121
2781	f	1.15	121
2782	f	1.16	121
2783	f	1.17	121
2784	f	1.18	121
2785	f	1.19	121
2786	f	1.21	121
2787	f	1.9	121
2788	f	1.91	121
2789	f	2.11	121
2790	f	2.12	121
2791	f	2.13	121
2792	f	2.14	121
2793	f	2.15	121
2794	f	2.16	121
2795	f	2.17	121
2796	f	2.18	121
2797	f	2.9	121
2798	f	5.11	121
2799	f	5.12	121
2800	f	5.13	121
2801	f	5.14	121
2802	f	5.15	121
2803	f	5.16	121
2804	f	5.17	121
2805	f	5.18	121
2806	f	5.19	121
2807	f	5.9	121
2808	f	5.2	121
2809	f	5.21	121
2810	f	6.11	121
2811	f	6.12	121
2812	f	6.13	121
2813	f	6.14	121
2814	f	6.9	121
2815	f	6.15	121
2816	f	6.16	121
2817	f	6.17	121
2818	f	7.11	121
2819	f	7.12	121
2820	f	7.13	121
2821	f	7.14	121
2822	f	7.9	121
2823	f	7.15	121
2824	f	7.16	121
2825	f	7.17	121
2826	f	8.11	121
2827	f	8.12	121
2828	f	8.13	121
2829	f	8.14	121
2830	f	8.9	121
2831	f	8.15	121
2832	f	8.16	121
2833	f	8.17	121
2834	f	9.11	121
2835	f	9.12	121
2836	f	9.13	121
2837	f	9.14	121
2838	f	9.9	121
2839	f	9.15	121
2840	f	9.16	121
2841	f	9.17	121
2842	f	10.11	121
2843	f	10.12	121
2844	f	10.13	121
2845	f	10.14	121
2846	f	10.9	121
2847	f	10.15	121
2848	f	10.16	121
2849	f	10.17	121
2850	f	11.11	121
2851	f	11.12	121
2852	f	11.13	121
2853	f	11.14	121
2854	f	11.9	121
2855	f	11.15	121
2856	f	11.16	121
2857	f	11.17	121
2858	f	1.11	122
2859	f	1.12	122
2860	f	1.13	122
2861	f	1.14	122
2862	f	1.15	122
2863	f	1.16	122
2864	f	1.17	122
2865	f	1.18	122
2866	f	1.19	122
2867	f	1.21	122
2868	f	1.9	122
2869	f	1.91	122
2870	f	2.11	122
2871	f	2.12	122
2872	f	2.13	122
2873	f	2.14	122
2874	f	2.15	122
2875	f	2.16	122
2876	f	2.17	122
2877	f	2.18	122
2878	f	2.9	122
2879	f	5.11	122
2880	f	5.12	122
2881	f	5.13	122
2882	f	5.14	122
2883	f	5.15	122
2884	f	5.16	122
2885	f	5.17	122
2886	f	5.18	122
2887	f	5.19	122
2888	f	5.9	122
2889	f	5.2	122
2890	f	5.21	122
2891	f	6.11	122
2892	f	6.12	122
2893	f	6.13	122
2894	f	6.14	122
2895	f	6.9	122
2896	f	6.15	122
2897	f	6.16	122
2898	f	6.17	122
2899	f	7.11	122
2900	f	7.12	122
2901	f	7.13	122
2902	f	7.14	122
2903	f	7.9	122
2904	f	7.15	122
2905	f	7.16	122
2906	f	7.17	122
2907	f	8.11	122
2908	f	8.12	122
2909	f	8.13	122
2910	f	8.14	122
2911	f	8.9	122
2912	f	8.15	122
2913	f	8.16	122
2914	f	8.17	122
2915	f	9.11	122
2916	f	9.12	122
2917	f	9.13	122
2918	f	9.14	122
2919	f	9.9	122
2920	f	9.15	122
2921	f	9.16	122
2922	f	9.17	122
2923	f	10.11	122
2924	f	10.12	122
2925	f	10.13	122
2926	f	10.14	122
2927	f	10.9	122
2928	f	10.15	122
2929	f	10.16	122
2930	f	10.17	122
2931	f	11.11	122
2932	f	11.12	122
2933	f	11.13	122
2934	f	11.14	122
2935	f	11.9	122
2936	f	11.15	122
2937	f	11.16	122
2938	f	11.17	122
590	t	1.11	94
592	t	1.13	94
674	t	1.14	95
2940	t	1.12	125
2951	f	2.11	125
2952	f	2.12	125
2953	f	2.13	125
2954	f	2.14	125
2955	f	2.15	125
2956	f	2.16	125
2957	f	2.17	125
2958	f	2.18	125
2959	f	2.9	125
2960	f	5.11	125
2961	f	5.12	125
2962	f	5.13	125
2963	f	5.14	125
2964	f	5.15	125
2965	f	5.16	125
2966	f	5.17	125
2967	f	5.18	125
2968	f	5.19	125
2969	f	5.9	125
2970	f	5.2	125
2971	f	5.21	125
2972	f	6.11	125
2973	f	6.12	125
2974	f	6.13	125
2975	f	6.14	125
2976	f	6.9	125
2977	f	6.15	125
2978	f	6.16	125
2979	f	6.17	125
2980	f	7.11	125
2981	f	7.12	125
2982	f	7.13	125
2983	f	7.14	125
2984	f	7.9	125
2985	f	7.15	125
2986	f	7.16	125
2987	f	7.17	125
2988	f	8.11	125
2989	f	8.12	125
2990	f	8.13	125
2991	f	8.14	125
2992	f	8.9	125
2993	f	8.15	125
2994	f	8.16	125
2995	f	8.17	125
2996	f	9.11	125
2997	f	9.12	125
2998	f	9.13	125
2999	f	9.14	125
3000	f	9.9	125
3001	f	9.15	125
3002	f	9.16	125
3003	f	9.17	125
3004	f	10.11	125
3005	f	10.12	125
3006	f	10.13	125
3007	f	10.14	125
3008	f	10.9	125
3009	f	10.15	125
3010	f	10.16	125
3011	f	10.17	125
3012	f	11.11	125
3013	f	11.12	125
3014	f	11.13	125
3015	f	11.14	125
3016	f	11.9	125
3017	f	11.15	125
3018	f	11.16	125
3019	f	11.17	125
2939	t	1.11	125
2941	t	1.13	125
2942	t	1.14	125
2943	t	1.15	125
2949	t	1.9	125
2944	t	1.16	125
2945	t	1.17	125
2946	t	1.18	125
2947	t	1.19	125
2948	t	1.21	125
2950	t	1.91	125
3032	f	2.11	127
3033	f	2.12	127
3034	f	2.13	127
3035	f	2.14	127
3036	f	2.15	127
3037	f	2.16	127
3038	f	2.17	127
3039	f	2.18	127
3040	f	2.9	127
3020	t	1.11	127
3021	t	1.12	127
3022	t	1.13	127
3023	t	1.14	127
3024	t	1.15	127
3030	t	1.9	127
3025	t	1.16	127
3026	t	1.17	127
3027	t	1.18	127
3028	t	1.19	127
3029	t	1.21	127
3031	t	1.91	127
3041	f	1.11	128
3042	f	1.12	128
3043	f	1.13	128
3044	f	1.14	128
3045	f	1.15	128
3046	f	1.16	128
3047	f	1.17	128
3048	f	1.18	128
3049	f	1.19	128
3050	f	1.21	128
3051	f	1.9	128
3052	f	1.91	128
3053	f	2.11	128
3054	f	2.12	128
3055	f	2.13	128
3056	f	2.14	128
3057	f	2.15	128
3058	f	2.16	128
3059	f	2.17	128
3060	f	2.18	128
3061	f	2.9	128
991	t	11.9	98
1072	t	11.9	99
\.


--
-- Data for Name: student_assigned_courses; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.student_assigned_courses (student_assigned_courses_id, course_id, user_id, completion_status) FROM stdin;
732	22	125	f
733	23	125	f
734	24	125	f
735	25	125	f
736	27	125	f
737	30	125	f
738	31	125	f
739	32	125	f
740	33	125	f
741	37	125	f
731	21	125	t
413	22	94	f
423	21	95	t
424	22	95	t
745	24	127	f
742	21	127	t
743	22	127	t
744	23	127	t
414	23	94	f
415	24	94	f
416	25	94	f
417	27	94	f
418	30	94	f
419	31	94	f
420	32	94	f
421	33	94	f
422	37	94	f
425	23	95	f
426	24	95	f
427	25	95	f
428	27	95	f
429	30	95	f
430	31	95	f
431	32	95	f
432	33	95	f
433	37	95	f
434	21	96	f
435	22	96	f
436	23	96	f
437	24	96	f
438	25	96	f
439	27	96	f
440	30	96	f
441	31	96	f
442	32	96	f
443	33	96	f
444	37	96	f
445	21	97	f
446	22	97	f
447	23	97	f
448	24	97	f
449	25	97	f
450	27	97	f
451	30	97	f
452	31	97	f
453	32	97	f
454	33	97	f
455	37	97	f
456	21	98	f
457	22	98	f
458	23	98	f
459	24	98	f
460	25	98	f
461	27	98	f
462	30	98	f
463	31	98	f
464	32	98	f
465	33	98	f
466	37	98	f
467	21	99	f
468	22	99	f
469	23	99	f
470	24	99	f
471	25	99	f
472	27	99	f
473	30	99	f
474	31	99	f
475	32	99	f
476	33	99	f
477	37	99	f
478	21	100	f
479	22	100	f
480	23	100	f
481	24	100	f
482	25	100	f
483	27	100	f
484	30	100	f
485	31	100	f
486	32	100	f
487	33	100	f
488	37	100	f
489	21	101	f
490	22	101	f
491	23	101	f
492	24	101	f
493	25	101	f
494	27	101	f
495	30	101	f
496	31	101	f
497	32	101	f
498	33	101	f
499	37	101	f
500	21	102	f
501	22	102	f
502	23	102	f
503	24	102	f
504	25	102	f
505	27	102	f
506	30	102	f
507	31	102	f
508	32	102	f
509	33	102	f
510	37	102	f
511	21	103	f
512	22	103	f
513	23	103	f
514	24	103	f
515	25	103	f
516	27	103	f
517	30	103	f
518	31	103	f
519	32	103	f
520	33	103	f
521	37	103	f
522	21	104	f
523	22	104	f
524	23	104	f
525	24	104	f
526	25	104	f
527	27	104	f
528	30	104	f
529	31	104	f
530	32	104	f
531	33	104	f
532	37	104	f
533	21	105	f
534	22	105	f
535	23	105	f
536	24	105	f
537	25	105	f
538	27	105	f
539	30	105	f
540	31	105	f
541	32	105	f
542	33	105	f
543	37	105	f
544	21	106	f
545	22	106	f
546	23	106	f
547	24	106	f
548	25	106	f
549	27	106	f
550	30	106	f
551	31	106	f
552	32	106	f
553	33	106	f
554	37	106	f
555	21	107	f
556	22	107	f
557	23	107	f
558	24	107	f
559	25	107	f
560	27	107	f
561	30	107	f
562	31	107	f
563	32	107	f
564	33	107	f
565	37	107	f
566	21	108	f
567	22	108	f
568	23	108	f
569	24	108	f
570	25	108	f
571	27	108	f
572	30	108	f
573	31	108	f
574	32	108	f
575	33	108	f
576	37	108	f
577	21	109	f
578	22	109	f
579	23	109	f
580	24	109	f
581	25	109	f
582	27	109	f
583	30	109	f
584	31	109	f
585	32	109	f
586	33	109	f
587	37	109	f
588	21	110	f
589	22	110	f
590	23	110	f
591	24	110	f
592	25	110	f
593	27	110	f
594	30	110	f
595	31	110	f
596	32	110	f
597	33	110	f
598	37	110	f
599	21	111	f
600	22	111	f
601	23	111	f
602	24	111	f
603	25	111	f
604	27	111	f
605	30	111	f
606	31	111	f
607	32	111	f
608	33	111	f
609	37	111	f
610	21	112	f
611	22	112	f
612	23	112	f
613	24	112	f
614	25	112	f
615	27	112	f
616	30	112	f
617	31	112	f
618	32	112	f
619	33	112	f
620	37	112	f
621	21	113	f
622	22	113	f
623	23	113	f
624	24	113	f
625	25	113	f
626	27	113	f
627	30	113	f
628	31	113	f
629	32	113	f
630	33	113	f
631	37	113	f
632	21	114	f
633	22	114	f
634	23	114	f
635	24	114	f
636	25	114	f
637	27	114	f
638	30	114	f
639	31	114	f
640	32	114	f
641	33	114	f
642	37	114	f
643	21	115	f
644	22	115	f
645	23	115	f
646	24	115	f
647	25	115	f
648	27	115	f
649	30	115	f
650	31	115	f
651	32	115	f
652	33	115	f
653	37	115	f
654	21	116	f
655	22	116	f
656	23	116	f
657	24	116	f
658	25	116	f
659	27	116	f
660	30	116	f
661	31	116	f
662	32	116	f
663	33	116	f
664	37	116	f
665	21	117	f
666	22	117	f
667	23	117	f
668	24	117	f
669	25	117	f
670	27	117	f
671	30	117	f
672	31	117	f
673	32	117	f
674	33	117	f
675	37	117	f
676	21	118	f
677	22	118	f
678	23	118	f
679	24	118	f
680	25	118	f
681	27	118	f
682	30	118	f
683	31	118	f
684	32	118	f
685	33	118	f
686	37	118	f
687	21	119	f
688	22	119	f
689	23	119	f
690	24	119	f
691	25	119	f
692	27	119	f
693	30	119	f
694	31	119	f
695	32	119	f
696	33	119	f
697	37	119	f
698	21	120	f
699	22	120	f
700	23	120	f
701	24	120	f
702	25	120	f
703	27	120	f
704	30	120	f
705	31	120	f
706	32	120	f
707	33	120	f
708	37	120	f
709	21	121	f
710	22	121	f
711	23	121	f
712	24	121	f
713	25	121	f
714	27	121	f
715	30	121	f
716	31	121	f
717	32	121	f
718	33	121	f
719	37	121	f
720	21	122	f
721	22	122	f
722	23	122	f
723	24	122	f
724	25	122	f
725	27	122	f
726	30	122	f
727	31	122	f
728	32	122	f
729	33	122	f
730	37	122	f
412	21	94	t
746	21	128	f
747	22	128	f
748	23	128	f
749	24	128	f
\.


--
-- Data for Name: student_grades; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.student_grades (student_grades_id, student_id, percentage_grade, course_subsection_id, created_at) FROM stdin;
87	94	50	21	2025-04-21 09:28:11.653771
88	94	70	21	2025-04-21 09:28:17.988819
89	94	30	23	2025-04-21 09:45:19.971378
90	94	70	23	2025-04-21 09:45:28.021633
91	95	70	21	2025-04-21 20:20:16.881212
92	95	90	23	2025-04-21 20:20:32.333014
93	125	80	21	2025-04-21 21:48:10.064224
94	125	70	23	2025-04-21 21:48:44.440488
95	127	60	21	2025-04-21 22:52:56.493496
96	127	70	21	2025-04-21 22:53:00.090612
97	127	110	23	2025-04-21 22:53:32.39705
98	127	90	23	2025-04-21 22:53:53.334594
99	93	60	21	2025-04-21 23:51:16.64844
100	93	60	21	2025-04-21 23:51:28.532433
101	93	70	21	2025-04-21 23:51:33.034144
102	98	160	89	2025-04-22 17:49:57.623467
103	99	180	89	2025-04-22 18:19:12.021192
\.


--
-- Data for Name: user_code_logs; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.user_code_logs (user_log_id, code, error, hints, page_context, static_issues, created_at, user_id) FROM stdin;
120	# Autonomous Car Robot Task: Implement an autonomous movement algorithm for a robot car.\r\n# The car continuously moves using sensor data and makes real-time decisions on direction.\r\n\r\n# Given: The infinite while loop to move the car in an autonomous manner\r\nwhile True:\r\n    # Given: The action vector [linear velocity, angular veloctiy]\r\n    # - Linear velocity controls the car's forward/backward movement.\r\n    # - Angular velocity controls the turning angle (left/right).\r\n    action = [0.00, 0.000] # Default: No movement initially\r\n\r\n    # TODO: Retrive the forward sensors value and store it in a variable\r\n    \r\n    \r\n    # TODO: Retrive the right sensors value and store it in a variable\r\n   \r\n    \r\n    # TODO: Retrive the left sensors value and store it in a variable\r\n    \r\n\r\n    # TODO: Fill in the dictionary withe the variables you just created to store the sensor values\r\n    sensor_readings = {\r\n        "Forward": env.get_forward_sensor,\r\n        "Right": env.get_right_sensor,\r\n        "Left": env.get_left_sensor\r\n    }\r\n    \r\n    # TODO: Determine which direction has the highest sensor value\r\n    # - Use `max()` to find the key (direction) in `sensor_readings` with the greatest value.\r\n    # - The `key=sensor_readings.get` argument ensures that the maximum is selected based on the sensor reading values.\r\n    # - Store the result in a variable named greatest_direction to decide the car's movement direction.\r\n    \r\n    \r\n    # TODO: Fill in the if else statement below with the greatest direction variable you just stored the greatest direction in on each fill in the blank line\r\n    if max(sensor_readings, key = sensor_readings.get) == "Forward":\r\n        action = [0.01, 0.0]   # Move forward\r\n    elif max(sensor_readings, key = sensor_readings.get) == "Right":\r\n        action = [0.005, -0.007]  # Turn right\r\n    elif max(sensor_readings, key = sensor_readings.get) == "Left":\r\n        action = [0.005, 0.007]  # Turn Left\r\n\r\n    # TODO: Apply the action we have defined in the if else statement to the environment\r\n\r\n\r\n    # **IGNORE: This is here to prevent infinite loops**\r\n    success = False\r\n    for contact in env.sim.data.contact:\r\n        geom1 = env.sim.model.geom_id2name(contact.geom1)\r\n        geom2 = env.sim.model.geom_id2name(contact.geom2)\r\n\r\n        if geom1 is not None and geom2 is not None:\r\n            if "chasis" in geom1 or "chasis" in geom2:\r\n                if "chasis" not in geom1:\r\n                    other_geom = geom1 \r\n                else:\r\n                    other_geom = geom2\r\n\r\n                geom_id = env.sim.model.geom_name2id(other_geom)\r\n                rgba = env.sim.model.geom_rgba[geom_id]\r\n                color = rgba[:3]\r\n                target_color = [0, 0, 1]  # RGB for blue\r\n                if np.array_equal(color, target_color):  # Exact match comparison\r\n                    success = True\r\n                    break\r\n    if success:\r\n        break\r\n    # **STOP IGNORING: Continue coding as normal**\r\n\r\n    # Given: For the loop to run like a real-world autonomous car\r\n    time.sleep(0.00001) \r\n                    \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n	\N	["1. You need to retrieve sensor values using the provided `env.get_sensor_forward_value()`, `env.get_sensor_right_value()`, and `env.get_sensor_left_value()` functions and store them in variables within the while loop.  Also, ensure you use these values in your `sensor_readings` dictionary and that you call `env.step(action)` to make the car move."]	Car	[{"message": "Missing call to `env.get_sensor_forward_value()`. This function needs to be called inside the infinite while loop to retrieve the forward sensor value of the car.", "line": 58}, {"message": "Missing call to `env.get_sensor_right_value()`. This function needs to be called inside the infinite while loop to retrieve the right sensor value for the car.", "line": 58}, {"message": "Missing call to `env.get_sensor_left_value()`. This function needs to be called inside the infinite while loop to retrieve the left sensor value for the car.", "line": 58}, {"message": "The `Forward` sensor reading is missing a value in `sensor_readings`. Please assign a variable.", "line": 21}, {"message": "The `Right` sensor reading is missing a value in `sensor_readings`. Please assign a variable.", "line": 21}, {"message": "The `Left` sensor reading is missing a value in `sensor_readings`. Please assign a variable.", "line": 21}, {"message": "A variable must be assigned using `max(sensor_readings, key=sensor_readings.get)`. Check `max()` is applied correctly.", "line": 9}, {"message": "Missing required call to `env.step(action)` is missing. The simulation may not function correctly. Check that it is called inside the infinite loop to execute movement.", "line": 58}]	2025-04-22 17:51:37.548669	98
122	# Autonomous Car Robot Task: Implement an autonomous movement algorithm for a robot car.\r\n# The car continuously moves using sensor data and makes real-time decisions on direction.\r\n\r\n# Given: The infinite while loop to move the car in an autonomous manner\r\nwhile True:\r\n    # Given: The action vector [linear velocity, angular veloctiy]\r\n    # - Linear velocity controls the car's forward/backward movement.\r\n    # - Angular velocity controls the turning angle (left/right).\r\n    action = [0.00, 0.000] # Default: No movement initially\r\n\r\n    # TODO: Retrive the forward sensors value and store it in a variable\r\n    \r\n    \r\n    # TODO: Retrive the right sensors value and store it in a variable\r\n   \r\n    \r\n    # TODO: Retrive the left sensors value and store it in a variable\r\n    \r\n\r\n    # TODO: Fill in the dictionary withe the variables you just created to store the sensor values\r\n    sensor_readings = {\r\n        "Forward": env.get_forward_sensor_value(),\r\n        "Right": env.get_right_sensor_value(),\r\n        "Left": env.get_left_sensor_value()\r\n    }\r\n    \r\n    # TODO: Determine which direction has the highest sensor value\r\n    # - Use `max()` to find the key (direction) in `sensor_readings` with the greatest value.\r\n    # - The `key=sensor_readings.get` argument ensures that the maximum is selected based on the sensor reading values.\r\n    # - Store the result in a variable named greatest_direction to decide the car's movement direction.\r\n    \r\n    \r\n    # TODO: Fill in the if else statement below with the greatest direction variable you just stored the greatest direction in on each fill in the blank line\r\n    if max(sensor_readings, key = sensor_readings.get) == "Forward":\r\n        action = [0.01, 0.0]   # Move forward\r\n    elif max(sensor_readings, key = sensor_readings.get) == "Right":\r\n        action = [0.005, -0.007]  # Turn right\r\n    elif max(sensor_readings, key = sensor_readings.get) == "Left":\r\n        action = [0.005, 0.007]  # Turn Left\r\n\r\n    # TODO: Apply the action we have defined in the if else statement to the environment\r\n\r\n\r\n    # **IGNORE: This is here to prevent infinite loops**\r\n    success = False\r\n    for contact in env.sim.data.contact:\r\n        geom1 = env.sim.model.geom_id2name(contact.geom1)\r\n        geom2 = env.sim.model.geom_id2name(contact.geom2)\r\n\r\n        if geom1 is not None and geom2 is not None:\r\n            if "chasis" in geom1 or "chasis" in geom2:\r\n                if "chasis" not in geom1:\r\n                    other_geom = geom1 \r\n                else:\r\n                    other_geom = geom2\r\n\r\n                geom_id = env.sim.model.geom_name2id(other_geom)\r\n                rgba = env.sim.model.geom_rgba[geom_id]\r\n                color = rgba[:3]\r\n                target_color = [0, 0, 1]  # RGB for blue\r\n                if np.array_equal(color, target_color):  # Exact match comparison\r\n                    success = True\r\n                    break\r\n    if success:\r\n        break\r\n    # **STOP IGNORING: Continue coding as normal**\r\n\r\n    # Given: For the loop to run like a real-world autonomous car\r\n    time.sleep(0.00001) \r\n                    \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n	\N	["1. Inside the `while True` loop, add these three lines before the `sensor_readings` dictionary assignment: `forward_sensor = env.get_sensor_forward_value()`, `right_sensor = env.get_sensor_right_value()`, `left_sensor = env.get_sensor_left_value()`.  Then, use these variables in your `sensor_readings` dictionary:  `sensor_readings = {\\"Forward\\": forward_sensor, \\"Right\\": right_sensor, \\"Left\\": left_sensor}`. Finally, add `env.step(action)` after the `if/elif/else` block to apply the chosen action."]	Car	[{"message": "Missing call to `env.get_sensor_forward_value()`. This function needs to be called inside the infinite while loop to retrieve the forward sensor value of the car.", "line": 58}, {"message": "Missing call to `env.get_sensor_right_value()`. This function needs to be called inside the infinite while loop to retrieve the right sensor value for the car.", "line": 58}, {"message": "Missing call to `env.get_sensor_left_value()`. This function needs to be called inside the infinite while loop to retrieve the left sensor value for the car.", "line": 58}, {"message": "The `Forward` sensor reading is missing a value in `sensor_readings`. Please assign a variable.", "line": 21}, {"message": "The `Right` sensor reading is missing a value in `sensor_readings`. Please assign a variable.", "line": 21}, {"message": "The `Left` sensor reading is missing a value in `sensor_readings`. Please assign a variable.", "line": 21}, {"message": "A variable must be assigned using `max(sensor_readings, key=sensor_readings.get)`. Check `max()` is applied correctly.", "line": 9}, {"message": "Missing required call to `env.step(action)` is missing. The simulation may not function correctly. Check that it is called inside the infinite loop to execute movement.", "line": 58}]	2025-04-22 17:52:03.83468	98
124	# Autonomous Car Robot Task: Implement an autonomous movement algorithm for a robot car.\r\n# The car continuously moves using sensor data and makes real-time decisions on direction.\r\n\r\n# Given: The infinite while loop to move the car in an autonomous manner\r\nwhile True:\r\n    # Given: The action vector [linear velocity, angular veloctiy]\r\n    # - Linear velocity controls the car's forward/backward movement.\r\n    # - Angular velocity controls the turning angle (left/right).\r\n    action = [0.00, 0.000] # Default: No movement initially\r\n\r\n    # TODO: Retrive the forward sensors value and store it in a variable\r\n    \r\n    \r\n    # TODO: Retrive the right sensors value and store it in a variable\r\n   \r\n    \r\n    # TODO: Retrive the left sensors value and store it in a variable\r\n    \r\n\r\n    # TODO: Fill in the dictionary withe the variables you just created to store the sensor values\r\n    sensor_readings = {\r\n        "Forward": env.get_sensor_forward_value(),\r\n        "Right": env.get_sensor_right_value(),\r\n        "Left": env.get_sensor_left_value()\r\n    }\r\n    \r\n    # TODO: Determine which direction has the highest sensor value\r\n    # - Use `max()` to find the key (direction) in `sensor_readings` with the greatest value.\r\n    # - The `key=sensor_readings.get` argument ensures that the maximum is selected based on the sensor reading values.\r\n    # - Store the result in a variable named greatest_direction to decide the car's movement direction.\r\n    \r\n    \r\n    # TODO: Fill in the if else statement below with the greatest direction variable you just stored the greatest direction in on each fill in the blank line\r\n    if max(sensor_readings, key=sensor_readings.get) == "Forward":\r\n        action = [0.01, 0.0]   # Move forward\r\n    elif max(sensor_readings, key=sensor_readings.get) == "Right":\r\n        action = [0.005, -0.007]  # Turn right\r\n    elif max(sensor_readings, key=sensor_readings.get) == "Left":\r\n        action = [0.005, 0.007]  # Turn Left\r\n\r\n    # TODO: Apply the action we have defined in the if else statement to the environment\r\n    env.step(action)\r\n\r\n    # **IGNORE: This is here to prevent infinite loops**\r\n    success = False\r\n    for contact in env.sim.data.contact:\r\n        geom1 = env.sim.model.geom_id2name(contact.geom1)\r\n        geom2 = env.sim.model.geom_id2name(contact.geom2)\r\n\r\n        if geom1 is not None and geom2 is not None:\r\n            if "chasis" in geom1 or "chasis" in geom2:\r\n                if "chasis" not in geom1:\r\n                    other_geom = geom1 \r\n                else:\r\n                    other_geom = geom2\r\n\r\n                geom_id = env.sim.model.geom_name2id(other_geom)\r\n                rgba = env.sim.model.geom_rgba[geom_id]\r\n                color = rgba[:3]\r\n                target_color = [0, 0, 1]  # RGB for blue\r\n                if np.array_equal(color, target_color):  # Exact match comparison\r\n                    success = True\r\n                    break\r\n    if success:\r\n        break\r\n    # **STOP IGNORING: Continue coding as normal**\r\n\r\n    # Given: For the loop to run like a real-world autonomous car\r\n    time.sleep(0.00001) \r\n                    \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n	\N	\N	Car	\N	2025-04-22 17:53:50.523076	98
121	# Autonomous Car Robot Task: Implement an autonomous movement algorithm for a robot car.\r\n# The car continuously moves using sensor data and makes real-time decisions on direction.\r\n\r\n# Given: The infinite while loop to move the car in an autonomous manner\r\nwhile True:\r\n    # Given: The action vector [linear velocity, angular veloctiy]\r\n    # - Linear velocity controls the car's forward/backward movement.\r\n    # - Angular velocity controls the turning angle (left/right).\r\n    action = [0.00, 0.000] # Default: No movement initially\r\n\r\n    # TODO: Retrive the forward sensors value and store it in a variable\r\n    \r\n    \r\n    # TODO: Retrive the right sensors value and store it in a variable\r\n   \r\n    \r\n    # TODO: Retrive the left sensors value and store it in a variable\r\n    \r\n\r\n    # TODO: Fill in the dictionary withe the variables you just created to store the sensor values\r\n    sensor_readings = {\r\n        "Forward": env.get_forward_sensor_value,\r\n        "Right": env.get_right_sensor_value,\r\n        "Left": env.get_left_sensor_value\r\n    }\r\n    \r\n    # TODO: Determine which direction has the highest sensor value\r\n    # - Use `max()` to find the key (direction) in `sensor_readings` with the greatest value.\r\n    # - The `key=sensor_readings.get` argument ensures that the maximum is selected based on the sensor reading values.\r\n    # - Store the result in a variable named greatest_direction to decide the car's movement direction.\r\n    \r\n    \r\n    # TODO: Fill in the if else statement below with the greatest direction variable you just stored the greatest direction in on each fill in the blank line\r\n    if max(sensor_readings, key = sensor_readings.get) == "Forward":\r\n        action = [0.01, 0.0]   # Move forward\r\n    elif max(sensor_readings, key = sensor_readings.get) == "Right":\r\n        action = [0.005, -0.007]  # Turn right\r\n    elif max(sensor_readings, key = sensor_readings.get) == "Left":\r\n        action = [0.005, 0.007]  # Turn Left\r\n\r\n    # TODO: Apply the action we have defined in the if else statement to the environment\r\n\r\n\r\n    # **IGNORE: This is here to prevent infinite loops**\r\n    success = False\r\n    for contact in env.sim.data.contact:\r\n        geom1 = env.sim.model.geom_id2name(contact.geom1)\r\n        geom2 = env.sim.model.geom_id2name(contact.geom2)\r\n\r\n        if geom1 is not None and geom2 is not None:\r\n            if "chasis" in geom1 or "chasis" in geom2:\r\n                if "chasis" not in geom1:\r\n                    other_geom = geom1 \r\n                else:\r\n                    other_geom = geom2\r\n\r\n                geom_id = env.sim.model.geom_name2id(other_geom)\r\n                rgba = env.sim.model.geom_rgba[geom_id]\r\n                color = rgba[:3]\r\n                target_color = [0, 0, 1]  # RGB for blue\r\n                if np.array_equal(color, target_color):  # Exact match comparison\r\n                    success = True\r\n                    break\r\n    if success:\r\n        break\r\n    # **STOP IGNORING: Continue coding as normal**\r\n\r\n    # Given: For the loop to run like a real-world autonomous car\r\n    time.sleep(0.00001) \r\n                    \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n	\N	["1.  You need to call the sensor functions (`env.get_sensor_forward_value()`, `env.get_sensor_right_value()`, `env.get_sensor_left_value()`) inside the `while` loop to get the up-to-date sensor readings.  Also, make sure to assign the returned values to variables before using them in `sensor_readings` and ensure `env.step(action)` is called within the loop to apply the chosen action to the environment."]	Car	[{"message": "Missing call to `env.get_sensor_forward_value()`. This function needs to be called inside the infinite while loop to retrieve the forward sensor value of the car.", "line": 58}, {"message": "Missing call to `env.get_sensor_right_value()`. This function needs to be called inside the infinite while loop to retrieve the right sensor value for the car.", "line": 58}, {"message": "Missing call to `env.get_sensor_left_value()`. This function needs to be called inside the infinite while loop to retrieve the left sensor value for the car.", "line": 58}, {"message": "The `Forward` sensor reading is missing a value in `sensor_readings`. Please assign a variable.", "line": 21}, {"message": "The `Right` sensor reading is missing a value in `sensor_readings`. Please assign a variable.", "line": 21}, {"message": "The `Left` sensor reading is missing a value in `sensor_readings`. Please assign a variable.", "line": 21}, {"message": "A variable must be assigned using `max(sensor_readings, key=sensor_readings.get)`. Check `max()` is applied correctly.", "line": 9}, {"message": "Missing required call to `env.step(action)` is missing. The simulation may not function correctly. Check that it is called inside the infinite loop to execute movement.", "line": 58}]	2025-04-22 17:51:55.691602	98
118	# Fetch Reach Robot Task: Guide the robot's gripper to the ball's position\r\n\r\n# Given: Set a distance threshold to determine when the gripper is close enough to the ball.\r\ndistance_threshold = 0.01\r\n\r\n# Given: Define a step size for each movement iteration.\r\nstep_size = 0.05\r\n\r\n# TODO: Use the environment's method to get the ball's position and store it in a variable.\r\nball_position = env.get_ball_position()\r\n\r\n# TODO: Use the environment's method to get the gripper's position and store it in a variable.\r\ngripper_position = env.get_gripper_position()\r\n\r\n# TODO: Calculate the direction vector from the gripper to the ball\r\n# *Remember*: Subtract the gripper position from the ball position \r\ndirection = np.array(ball_position) - np.array(gripper_position)\r\n\r\n# TODO: Normalize the direction vector to get its magnitude, a scalar value to later compare to another scalar value, the distance_threshold\r\ndirection_normalized = np.linalg.norm(direction)\r\n\r\n# TODO: Fill in the while loop to move the gripper toward the ball, keep moving the gripper until the distance is less than the threshold.\r\n# *Remeber*: Utilize the normalized direction vector you just caclulated to compare to the distance_threshold\r\nwhile direction_normalized > distance_threshold:\r\n\r\n    # Given: Calculate the action to move the gripper in the direction of the ball.\r\n    action = np.append(direction / direction_normalized * step_size, [1])\r\n\r\n    # TODO: Apply the action to the environment.\r\n    env.step(action)\r\n\r\n    # TODO: Update the gripper's position. \r\n    # *Remember*: You have done this before. Get the grippers position from the environment. \r\n    gripper_position = env.get_gripper_position()\r\n\r\n    # TODO: Update the gripper's direction.\r\n    # *Remember*: You have calculated the direction before. This is the new distance from the gripper to the ball (hence the gripper's position).\r\n    direction = np.array(ball_position) - np.array(gripper_position)\r\n\r\n    #TODO: Normalize the direction vector\r\n    # *Remember*: You have done this before.\r\n    direction_normalized = np.linalg.norm(direction)\r\n\r\n                    \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n	\N	\N	Fetch Reach	\N	2025-04-21 20:29:46.494256	94
119	# Fetch Reach Robot Task: Guide the robot's gripper to the ball's position\r\n\r\n# Given: Set a distance threshold to determine when the gripper is close enough to the ball.\r\ndistance_threshold = 0.01\r\n\r\n# Given: Define a step size for each movement iteration.\r\nstep_size = 0.05\r\n\r\n# TODO: Use the environment's method to get the ball's position and store it in a variable.\r\nball_position = env.get_ball_position()\r\n\r\n# TODO: Use the environment's method to get the gripper's position and store it in a variable.\r\ngripper_position = env.get_gripper_position()\r\n\r\n# TODO: Calculate the direction vector from the gripper to the ball\r\n# *Remember*: Subtract the gripper position from the ball position \r\ndirection = np.array(ball_position) - np.array(gripper_position)\r\n\r\n# TODO: Normalize the direction vector to get its magnitude, a scalar value to later compare to another scalar value, the distance_threshold\r\ndirection_normalized = np.linalg.norm(direction)\r\n\r\n# TODO: Fill in the while loop to move the gripper toward the ball, keep moving the gripper until the distance is less than the threshold.\r\n# *Remeber*: Utilize the normalized direction vector you just caclulated to compare to the distance_threshold\r\nwhile direction_normalized > distance_threshold:\r\n\r\n    # Given: Calculate the action to move the gripper in the direction of the ball.\r\n    action = np.append(direction / direction_normalized * step_size, [1])\r\n\r\n    # TODO: Apply the action to the environment.\r\n    env.step(action)\r\n\r\n    # TODO: Update the gripper's position. \r\n    # *Remember*: You have done this before. Get the grippers position from the environment. \r\n    gripper_position = env.get_gripper_position()\r\n\r\n    # TODO: Update the gripper's direction.\r\n    # *Remember*: You have calculated the direction before. This is the new distance from the gripper to the ball (hence the gripper's position).\r\n    direction = np.array(ball_position) - np.array(gripper_position)\r\n\r\n    #TODO: Normalize the direction vector\r\n    # *Remember*: You have done this before.\r\n    direction_normalized = np.linalg.norm(direction)\r\n\r\n                    \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n	\N	\N	Fetch Reach	\N	2025-04-21 20:29:46.503032	94
111	# Fetch Reach Robot Task: Guide the robot's gripper to the ball's position\r\n\r\n# Given: Set a distance threshold to determine when the gripper is close enough to the ball.\r\ndistance_threshold = 0.01\r\n\r\n# Given: Define a step size for each movement iteration.\r\nstep_size = 0.05\r\n\r\n# TODO: Use the environment's method to get the ball's position and store it in a variable.\r\n\r\n\r\n# TODO: Use the environment's method to get the gripper's position and store it in a variable.\r\n\r\n\r\n# TODO: Calculate the direction vector from the gripper to the ball\r\n# *Remember*: Subtract the gripper position from the ball position \r\n\r\n\r\n# TODO: Normalize the direction vector to get its magnitude, a scalar value to later compare to another scalar value, the distance_threshold\r\n\r\n\r\n# TODO: Fill in the while loop to move the gripper toward the ball, keep moving the gripper until the distance is less than the threshold.\r\n# *Remeber*: Utilize the normalized direction vector you just caclulated to compare to the distance_threshold\r\nwhile ____________________ > distance_threshold:\r\n\r\n    # Given: Calculate the action to move the gripper in the direction of the ball.\r\n    action = np.append(direction / direction_normalized * step_size, [1])\r\n\r\n    # TODO: Apply the action to the environment.\r\n\r\n\r\n    # TODO: Update the gripper's position. \r\n    # *Remember*: You have done this before. Get the grippers position from the environment. \r\n\r\n\r\n    # TODO: Update the gripper's direction.\r\n    # *Remember*: You have calculated the direction before. This is the new distance from the gripper to the ball (hence the gripper's position).\r\n\r\n\r\n    #TODO: Normalize the direction vector\r\n    # *Remember*: You have done this before.\r\n\r\n                    \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n	\N	["1. The main loop should continue as long as the distance between the gripper and the ball is greater than the `distance_threshold`.  You need to calculate this distance and use it in your `while` loop condition.  Remember to use the appropriate environment functions to get the necessary positions."]	Fetch Reach	[{"message": "No call to env.step() was found.", "line": 27}, {"message": "Missing call to `env.get_ball_position()`. This function needs to be called somewhere in the code to retrieve the ball position from the environment.", "line": 27}, {"message": "Missing call to `env.get_gripper_position()`. This function needs to be called somewhere in the code to retrieve the gripper position from the environment.", "line": 27}, {"message": "Missing computation of direction. Make sure you define `direction = np.array(None) - np.array(None)`.", "line": 27}, {"message": "Missing computation of direction normalization. Expected np.linalg.norm(None).", "line": 27}, {"message": "The variable used in the while loop condition ('____________________') is not computed using np.linalg.norm(...).", "line": 24}]	2025-04-21 20:28:09.428623	94
112	# Fetch Reach Robot Task: Guide the robot's gripper to the ball's position\r\n\r\n# Given: Set a distance threshold to determine when the gripper is close enough to the ball.\r\ndistance_threshold = 0.01\r\n\r\n# Given: Define a step size for each movement iteration.\r\nstep_size = 0.05\r\n\r\n# TODO: Use the environment's method to get the ball's position and store it in a variable.\r\nball_position = env.get_ball_position()\r\n\r\n# TODO: Use the environment's method to get the gripper's position and store it in a variable.\r\n\r\n\r\n# TODO: Calculate the direction vector from the gripper to the ball\r\n# *Remember*: Subtract the gripper position from the ball position \r\n\r\n\r\n# TODO: Normalize the direction vector to get its magnitude, a scalar value to later compare to another scalar value, the distance_threshold\r\n\r\n\r\n# TODO: Fill in the while loop to move the gripper toward the ball, keep moving the gripper until the distance is less than the threshold.\r\n# *Remeber*: Utilize the normalized direction vector you just caclulated to compare to the distance_threshold\r\nwhile ____________________ > distance_threshold:\r\n\r\n    # Given: Calculate the action to move the gripper in the direction of the ball.\r\n    action = np.append(direction / direction_normalized * step_size, [1])\r\n\r\n    # TODO: Apply the action to the environment.\r\n\r\n\r\n    # TODO: Update the gripper's position. \r\n    # *Remember*: You have done this before. Get the grippers position from the environment. \r\n\r\n\r\n    # TODO: Update the gripper's direction.\r\n    # *Remember*: You have calculated the direction before. This is the new distance from the gripper to the ball (hence the gripper's position).\r\n\r\n\r\n    #TODO: Normalize the direction vector\r\n    # *Remember*: You have done this before.\r\n\r\n                    \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n	\N	["1.  Focus on completing the missing code sections related to obtaining the gripper position (`env.get_gripper_position()`), calculating the direction vector (subtracting gripper position from ball position), normalizing this vector using `np.linalg.norm()`, and using the norm of the direction vector as the condition in your `while` loop.  Remember to update the gripper's position and recalculate the direction vector inside the loop after each `env.step()` call."]	Fetch Reach	[{"message": "No call to env.step() was found.", "line": 27}, {"message": "Missing call to `env.get_gripper_position()`. This function needs to be called somewhere in the code to retrieve the gripper position from the environment.", "line": 27}, {"message": "Missing computation of direction. Make sure you define `direction = np.array(ball_position) - np.array(None)`.", "line": 27}, {"message": "Missing computation of direction normalization. Expected np.linalg.norm(None).", "line": 27}, {"message": "The variable used in the while loop condition ('____________________') is not computed using np.linalg.norm(...).", "line": 24}]	2025-04-21 20:28:32.02098	94
113	# Fetch Reach Robot Task: Guide the robot's gripper to the ball's position\r\n\r\n# Given: Set a distance threshold to determine when the gripper is close enough to the ball.\r\ndistance_threshold = 0.01\r\n\r\n# Given: Define a step size for each movement iteration.\r\nstep_size = 0.05\r\n\r\n# TODO: Use the environment's method to get the ball's position and store it in a variable.\r\nball_position = env.get_ball_position()\r\n\r\n# TODO: Use the environment's method to get the gripper's position and store it in a variable.\r\ngripper_position = env.get_gripper_position()\r\n\r\n# TODO: Calculate the direction vector from the gripper to the ball\r\n# *Remember*: Subtract the gripper position from the ball position \r\n\r\n\r\n# TODO: Normalize the direction vector to get its magnitude, a scalar value to later compare to another scalar value, the distance_threshold\r\n\r\n\r\n# TODO: Fill in the while loop to move the gripper toward the ball, keep moving the gripper until the distance is less than the threshold.\r\n# *Remeber*: Utilize the normalized direction vector you just caclulated to compare to the distance_threshold\r\nwhile ____________________ > distance_threshold:\r\n\r\n    # Given: Calculate the action to move the gripper in the direction of the ball.\r\n    action = np.append(direction / direction_normalized * step_size, [1])\r\n\r\n    # TODO: Apply the action to the environment.\r\n\r\n\r\n    # TODO: Update the gripper's position. \r\n    # *Remember*: You have done this before. Get the grippers position from the environment. \r\n\r\n\r\n    # TODO: Update the gripper's direction.\r\n    # *Remember*: You have calculated the direction before. This is the new distance from the gripper to the ball (hence the gripper's position).\r\n\r\n\r\n    #TODO: Normalize the direction vector\r\n    # *Remember*: You have done this before.\r\n\r\n                    \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n	\N	["1.  Replace `____________________` in the `while` loop condition with `np.linalg.norm(np.array(ball_position) - np.array(gripper_position))`.  Then, add the lines `direction = np.array(ball_position) - np.array(gripper_position)` and `direction_normalized = np.linalg.norm(direction)` before the loop to calculate and normalize the direction vector.  Finally, add `env.step(action)` after calculating the `action`."]	Fetch Reach	[{"message": "No call to env.step() was found.", "line": 27}, {"message": "Missing computation of direction. Make sure you define `direction = np.array(ball_position) - np.array(gripper_position)`.", "line": 27}, {"message": "Missing computation of direction normalization. Expected np.linalg.norm(None).", "line": 27}, {"message": "The variable used in the while loop condition ('____________________') is not computed using np.linalg.norm(...).", "line": 24}]	2025-04-21 20:28:33.942222	94
114	# Fetch Reach Robot Task: Guide the robot's gripper to the ball's position\r\n\r\n# Given: Set a distance threshold to determine when the gripper is close enough to the ball.\r\ndistance_threshold = 0.01\r\n\r\n# Given: Define a step size for each movement iteration.\r\nstep_size = 0.05\r\n\r\n# TODO: Use the environment's method to get the ball's position and store it in a variable.\r\nball_position = env.get_ball_position()\r\n\r\n# TODO: Use the environment's method to get the gripper's position and store it in a variable.\r\ngripper_position = env.get_gripper_position()\r\n\r\n# TODO: Calculate the direction vector from the gripper to the ball\r\n# *Remember*: Subtract the gripper position from the ball position \r\ndirection = np.array(ball_position) - np.array(gripper_position)\r\n\r\n# TODO: Normalize the direction vector to get its magnitude, a scalar value to later compare to another scalar value, the distance_threshold\r\n\r\n\r\n# TODO: Fill in the while loop to move the gripper toward the ball, keep moving the gripper until the distance is less than the threshold.\r\n# *Remeber*: Utilize the normalized direction vector you just caclulated to compare to the distance_threshold\r\nwhile ____________________ > distance_threshold:\r\n\r\n    # Given: Calculate the action to move the gripper in the direction of the ball.\r\n    action = np.append(direction / direction_normalized * step_size, [1])\r\n\r\n    # TODO: Apply the action to the environment.\r\n\r\n\r\n    # TODO: Update the gripper's position. \r\n    # *Remember*: You have done this before. Get the grippers position from the environment. \r\n\r\n\r\n    # TODO: Update the gripper's direction.\r\n    # *Remember*: You have calculated the direction before. This is the new distance from the gripper to the ball (hence the gripper's position).\r\n\r\n\r\n    #TODO: Normalize the direction vector\r\n    # *Remember*: You have done this before.\r\n\r\n                    \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n	\N	["1. The while loop condition should check if the distance between the gripper and the ball is greater than the `distance_threshold`.  This distance is calculated using the Euclidean norm (magnitude) of the `direction` vector.  Therefore, the blank should be filled with `np.linalg.norm(direction)`.  The complete corrected code section is:", "```python", "direction_normalized = np.linalg.norm(direction)  #compute direction normalization", "while np.linalg.norm(direction) > distance_threshold:", "action = np.append(direction / direction_normalized * step_size, [1])", "env.step(action)", "gripper_position = env.get_gripper_position()", "direction = np.array(ball_position) - np.array(gripper_position)", "direction_normalized = np.linalg.norm(direction)", "```", "Remember to include `direction_normalized = np.linalg.norm(direction)` before the while loop to compute the normalization.  Also,  the `env.step(action)` line is crucial for applying the calculated action to the environment.  Finally, after each step, the gripper's position and direction must be updated accordingly."]	Fetch Reach	[{"message": "No call to env.step() was found.", "line": 27}, {"message": "Missing computation of direction normalization. Expected np.linalg.norm(direction).", "line": 27}, {"message": "The variable used in the while loop condition ('____________________') is not computed using np.linalg.norm(...).", "line": 24}]	2025-04-21 20:28:40.30654	94
115	# Fetch Reach Robot Task: Guide the robot's gripper to the ball's position\r\n\r\n# Given: Set a distance threshold to determine when the gripper is close enough to the ball.\r\ndistance_threshold = 0.01\r\n\r\n# Given: Define a step size for each movement iteration.\r\nstep_size = 0.05\r\n\r\n# TODO: Use the environment's method to get the ball's position and store it in a variable.\r\nball_position = env.get_ball_position()\r\n\r\n# TODO: Use the environment's method to get the gripper's position and store it in a variable.\r\ngripper_position = env.get_gripper_position()\r\n\r\n# TODO: Calculate the direction vector from the gripper to the ball\r\n# *Remember*: Subtract the gripper position from the ball position \r\ndirection = np.array(ball_position) - np.array(gripper_position)\r\n\r\n# TODO: Normalize the direction vector to get its magnitude, a scalar value to later compare to another scalar value, the distance_threshold\r\ndirection_normalized = np.linalg.norm(direction)\r\n\r\n# TODO: Fill in the while loop to move the gripper toward the ball, keep moving the gripper until the distance is less than the threshold.\r\n# *Remeber*: Utilize the normalized direction vector you just caclulated to compare to the distance_threshold\r\nwhile ____________________ > distance_threshold:\r\n\r\n    # Given: Calculate the action to move the gripper in the direction of the ball.\r\n    action = np.append(direction / direction_normalized * step_size, [1])\r\n\r\n    # TODO: Apply the action to the environment.\r\n\r\n\r\n    # TODO: Update the gripper's position. \r\n    # *Remember*: You have done this before. Get the grippers position from the environment. \r\n\r\n\r\n    # TODO: Update the gripper's direction.\r\n    # *Remember*: You have calculated the direction before. This is the new distance from the gripper to the ball (hence the gripper's position).\r\n\r\n\r\n    #TODO: Normalize the direction vector\r\n    # *Remember*: You have done this before.\r\n\r\n                    \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n	\N	["1. The while loop condition should check if the distance between the gripper and the ball, calculated using `np.linalg.norm(env.get_gripper_position() - env.get_ball_position())`, is greater than `distance_threshold`.  Remember to update `gripper_position` and `direction` inside the loop after each `env.step()` call."]	Fetch Reach	[{"message": "No call to env.step() was found.", "line": 27}, {"message": "The variable used in the while loop condition ('____________________') is not computed using np.linalg.norm(...).", "line": 24}]	2025-04-21 20:28:46.148598	94
116	# Fetch Reach Robot Task: Guide the robot's gripper to the ball's position\r\n\r\n# Given: Set a distance threshold to determine when the gripper is close enough to the ball.\r\ndistance_threshold = 0.01\r\n\r\n# Given: Define a step size for each movement iteration.\r\nstep_size = 0.05\r\n\r\n# TODO: Use the environment's method to get the ball's position and store it in a variable.\r\nball_position = env.get_ball_position()\r\n\r\n# TODO: Use the environment's method to get the gripper's position and store it in a variable.\r\ngripper_position = env.get_gripper_position()\r\n\r\n# TODO: Calculate the direction vector from the gripper to the ball\r\n# *Remember*: Subtract the gripper position from the ball position \r\ndirection = np.array(ball_position) - np.array(gripper_position)\r\n\r\n# TODO: Normalize the direction vector to get its magnitude, a scalar value to later compare to another scalar value, the distance_threshold\r\ndirection_normalized = np.linalg.norm(direction)\r\n\r\n# TODO: Fill in the while loop to move the gripper toward the ball, keep moving the gripper until the distance is less than the threshold.\r\n# *Remeber*: Utilize the normalized direction vector you just caclulated to compare to the distance_threshold\r\nwhile direction_normalized > distance_threshold:\r\n\r\n    # Given: Calculate the action to move the gripper in the direction of the ball.\r\n    action = np.append(direction / direction_normalized * step_size, [1])\r\n\r\n    # TODO: Apply the action to the environment.\r\n\r\n\r\n    # TODO: Update the gripper's position. \r\n    # *Remember*: You have done this before. Get the grippers position from the environment. \r\n\r\n\r\n    # TODO: Update the gripper's direction.\r\n    # *Remember*: You have calculated the direction before. This is the new distance from the gripper to the ball (hence the gripper's position).\r\n\r\n\r\n    #TODO: Normalize the direction vector\r\n    # *Remember*: You have done this before.\r\n\r\n                    \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n	\N	["1.  Inside your `while` loop, after calculating the `action`, you need to use `env.step(action)` to apply the action to the environment.  Then, update `gripper_position` and `direction_normalized` using `env.get_gripper_position()` and the same calculations you performed outside the loop."]	Fetch Reach	[{"message": "No call to env.step() was found.", "line": 27}]	2025-04-21 20:28:53.155946	94
117	# Fetch Reach Robot Task: Guide the robot's gripper to the ball's position\r\n\r\n# Given: Set a distance threshold to determine when the gripper is close enough to the ball.\r\ndistance_threshold = 0.01\r\n\r\n# Given: Define a step size for each movement iteration.\r\nstep_size = 0.05\r\n\r\n# TODO: Use the environment's method to get the ball's position and store it in a variable.\r\nball_position = env.get_ball_position()\r\n\r\n# TODO: Use the environment's method to get the gripper's position and store it in a variable.\r\ngripper_position = env.get_gripper_position()\r\n\r\n# TODO: Calculate the direction vector from the gripper to the ball\r\n# *Remember*: Subtract the gripper position from the ball position \r\ndirection = np.array(ball_position) - np.array(gripper_position)\r\n\r\n# TODO: Normalize the direction vector to get its magnitude, a scalar value to later compare to another scalar value, the distance_threshold\r\ndirection_normalized = np.linalg.norm(direction)\r\n\r\n# TODO: Fill in the while loop to move the gripper toward the ball, keep moving the gripper until the distance is less than the threshold.\r\n# *Remeber*: Utilize the normalized direction vector you just calculated to compare to the distance_threshold\r\nwhile direction_normalized > distance_threshold:\r\n\r\n    # Given: Calculate the action to move the gripper in the direction of the ball.\r\n    action = np.append(direction / direction_normalized * step_size, [1])\r\n\r\n    # TODO: Apply the action to the environment.\r\n    env.step(action)\r\n\r\n    # TODO: Update the gripper's position. \r\n    # *Remember*: You have done this before. Get the grippers position from the environment. \r\n    gripper_position = env.get_gripper_position()\r\n\r\n    # TODO: Update the gripper's direction.\r\n    # *Remember*: You have calculated the direction before. This is the new distance from the gripper to the ball (hence the gripper's position).\r\n    direction = np.array(ball_position) - np.array(gripper_position)\r\n\r\n    #TODO: Normalize the direction vector\r\n    # *Remember*: You have done this before.\r\n    direction_normalized = np.linalg.norm(direction)\r\n\r\n                    \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n	\N	\N	Fetch Reach	\N	2025-04-21 20:29:46.493054	94
123	# Autonomous Car Robot Task: Implement an autonomous movement algorithm for a robot car.\r\n# The car continuously moves using sensor data and makes real-time decisions on direction.\r\n\r\n# Given: The infinite while loop to move the car in an autonomous manner\r\nwhile True:\r\n    # Given: The action vector [linear velocity, angular veloctiy]\r\n    # - Linear velocity controls the car's forward/backward movement.\r\n    # - Angular velocity controls the turning angle (left/right).\r\n    action = [0.00, 0.000] # Default: No movement initially\r\n\r\n    # TODO: Retrive the forward sensors value and store it in a variable\r\n    \r\n    \r\n    # TODO: Retrive the right sensors value and store it in a variable\r\n   \r\n    \r\n    # TODO: Retrive the left sensors value and store it in a variable\r\n    \r\n\r\n    # TODO: Fill in the dictionary withe the variables you just created to store the sensor values\r\n    sensor_readings = {\r\n        "Forward": env.get_sensor_forward_value(),\r\n        "Right": env.get_sensor_right_value(),\r\n        "Left": env.get_sensor_left_value()\r\n    }\r\n    \r\n    # TODO: Determine which direction has the highest sensor value\r\n    # - Use `max()` to find the key (direction) in `sensor_readings` with the greatest value.\r\n    # - The `key=sensor_readings.get` argument ensures that the maximum is selected based on the sensor reading values.\r\n    # - Store the result in a variable named greatest_direction to decide the car's movement direction.\r\n    \r\n    \r\n    # TODO: Fill in the if else statement below with the greatest direction variable you just stored the greatest direction in on each fill in the blank line\r\n    if max(sensor_readings, key = sensor_readings.get) == "Forward":\r\n        action = [0.01, 0.0]   # Move forward\r\n    elif max(sensor_readings, key = sensor_readings.get) == "Right":\r\n        action = [0.005, -0.007]  # Turn right\r\n    elif max(sensor_readings, key = sensor_readings.get) == "Left":\r\n        action = [0.005, 0.007]  # Turn Left\r\n\r\n    # TODO: Apply the action we have defined in the if else statement to the environment\r\n\r\n\r\n    # **IGNORE: This is here to prevent infinite loops**\r\n    success = False\r\n    for contact in env.sim.data.contact:\r\n        geom1 = env.sim.model.geom_id2name(contact.geom1)\r\n        geom2 = env.sim.model.geom_id2name(contact.geom2)\r\n\r\n        if geom1 is not None and geom2 is not None:\r\n            if "chasis" in geom1 or "chasis" in geom2:\r\n                if "chasis" not in geom1:\r\n                    other_geom = geom1 \r\n                else:\r\n                    other_geom = geom2\r\n\r\n                geom_id = env.sim.model.geom_name2id(other_geom)\r\n                rgba = env.sim.model.geom_rgba[geom_id]\r\n                color = rgba[:3]\r\n                target_color = [0, 0, 1]  # RGB for blue\r\n                if np.array_equal(color, target_color):  # Exact match comparison\r\n                    success = True\r\n                    break\r\n    if success:\r\n        break\r\n    # **STOP IGNORING: Continue coding as normal**\r\n\r\n    # Given: For the loop to run like a real-world autonomous car\r\n    time.sleep(0.00001) \r\n                    \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n	\N	["1. To fix the issues, you need to store the return values of `env.get_sensor_forward_value()`, `env.get_sensor_right_value()`, and `env.get_sensor_left_value()` in variables.  Then, use these variables to populate the `sensor_readings` dictionary. Finally, call `env.step(action)` after determining the action. Here's the corrected code:", "```python", "import time", "import numpy as np", "# Autonomous Car Robot Task: Implement an autonomous movement algorithm for a robot car.", "# The car continuously moves using sensor data and makes real-time decisions on direction.", "# Given: The infinite while loop to move the car in an autonomous manner", "while True:", "# Given: The action vector [linear velocity, angular veloctiy]", "# - Linear velocity controls the car's forward/backward movement.", "# - Angular velocity controls the turning angle (left/right).", "action = [0.00, 0.000] # Default: No movement initially", "forward_sensor_value = env.get_sensor_forward_value()", "right_sensor_value = env.get_sensor_right_value()", "left_sensor_value = env.get_sensor_left_value()", "sensor_readings = {", "\\"Forward\\": forward_sensor_value,", "\\"Right\\": right_sensor_value,", "\\"Left\\": left_sensor_value", "}", "greatest_direction = max(sensor_readings, key=sensor_readings.get)", "if greatest_direction == \\"Forward\\":", "action = [0.01, 0.0]   # Move forward", "elif greatest_direction == \\"Right\\":", "action = [0.005, -0.007]  # Turn right", "elif greatest_direction == \\"Left\\":", "action = [0.005, 0.007]  # Turn Left", "env.step(action) # Apply the action", "# **IGNORE: This is here to prevent infinite loops**", "success = False", "for contact in env.sim.data.contact:", "geom1 = env.sim.model.geom_id2name(contact.geom1)", "geom2 = env.sim.model.geom_id2name(contact.geom2)", "if geom1 is not None and geom2 is not None:", "if \\"chasis\\" in geom1 or \\"chasis\\" in geom2:", "if \\"chasis\\" not in geom1:", "other_geom = geom1", "else:", "other_geom = geom2", "geom_id = env.sim.model.geom_name2id(other_geom)", "rgba = env.sim.model.geom_rgba[geom_id]", "color = rgba[:3]", "target_color = [0, 0, 1]  # RGB for blue", "if np.array_equal(color, target_color):  # Exact match comparison", "success = True", "break", "if success:", "break", "# **STOP IGNORING: Continue coding as normal**", "# Given: For the loop to run like a real-world autonomous car", "time.sleep(0.00001)", "```"]	Car	[{"message": "The return value of `env.get_sensor_forward_value()` should be stored in a variable.", "line": 58}, {"message": "The return value of `env.get_sensor_right_value()` should be stored in a variable.", "line": 58}, {"message": "The return value of `env.get_sensor_left_value()` should be stored in a variable.", "line": 58}, {"message": "The `Forward` sensor reading is missing a value in `sensor_readings`. Please assign a variable.", "line": 21}, {"message": "The `Right` sensor reading is missing a value in `sensor_readings`. Please assign a variable.", "line": 21}, {"message": "The `Left` sensor reading is missing a value in `sensor_readings`. Please assign a variable.", "line": 21}, {"message": "A variable must be assigned using `max(sensor_readings, key=sensor_readings.get)`. Check `max()` is applied correctly.", "line": 9}, {"message": "Missing required call to `env.step(action)` is missing. The simulation may not function correctly. Check that it is called inside the infinite loop to execute movement.", "line": 58}]	2025-04-22 17:52:39.325234	98
125	# Autonomous Car Robot Task: Implement an autonomous movement algorithm for a robot car.\r\n# The car continuously moves using sensor data and makes real-time decisions on direction.\r\n\r\n# Given: The infinite while loop to move the car in an autonomous manner\r\nwhile True:\r\n    # Given: The action vector [linear velocity, angular veloctiy]\r\n    # - Linear velocity controls the car's forward/backward movement.\r\n    # - Angular velocity controls the turning angle (left/right).\r\n    action = [0.00, 0.000] # Default: No movement initially\r\n\r\n    # TODO: Retrive the forward sensors value and store it in a variable\r\n    forward_val = env.get_sensor\r\n    \r\n    # TODO: Retrive the right sensors value and store it in a variable\r\n   \r\n    \r\n    # TODO: Retrive the left sensors value and store it in a variable\r\n    \r\n\r\n    # TODO: Fill in the dictionary withe the variables you just created to store the sensor values\r\n    sensor_readings = {\r\n        "Forward": _______,\r\n        "Right": _____,\r\n        "Left": ____\r\n    }\r\n    \r\n    # TODO: Determine which direction has the highest sensor value\r\n    # - Use `max()` to find the key (direction) in `sensor_readings` with the greatest value.\r\n    # - The `key=sensor_readings.get` argument ensures that the maximum is selected based on the sensor reading values.\r\n    # - Store the result in a variable named greatest_direction to decide the car's movement direction.\r\n    \r\n    \r\n    # TODO: Fill in the if else statement below with the greatest direction variable you just stored the greatest direction in on each fill in the blank line\r\n    if __________________ == "Forward":\r\n        action = [0.01, 0.0]   # Move forward\r\n    elif __________________ == "Right":\r\n        action = [0.005, -0.007]  # Turn right\r\n    elif __________________ == "Left":\r\n        action = [0.005, 0.007]  # Turn Left\r\n\r\n    # TODO: Apply the action we have defined in the if else statement to the environment\r\n\r\n\r\n    # **IGNORE: This is here to prevent infinite loops**\r\n    success = False\r\n    for contact in env.sim.data.contact:\r\n        geom1 = env.sim.model.geom_id2name(contact.geom1)\r\n        geom2 = env.sim.model.geom_id2name(contact.geom2)\r\n\r\n        if geom1 is not None and geom2 is not None:\r\n            if "chasis" in geom1 or "chasis" in geom2:\r\n                if "chasis" not in geom1:\r\n                    other_geom = geom1 \r\n                else:\r\n                    other_geom = geom2\r\n\r\n                geom_id = env.sim.model.geom_name2id(other_geom)\r\n                rgba = env.sim.model.geom_rgba[geom_id]\r\n                color = rgba[:3]\r\n                target_color = [0, 0, 1]  # RGB for blue\r\n                if np.array_equal(color, target_color):  # Exact match comparison\r\n                    success = True\r\n                    break\r\n    if success:\r\n        break\r\n    # **STOP IGNORING: Continue coding as normal**\r\n\r\n    # Given: For the loop to run like a real-world autonomous car\r\n    time.sleep(0.00001) \r\n                    \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n	\N	["1. Make sure you are retrieving sensor values using the `env.get_sensor_forward_value()`, `env.get_sensor_right_value()`, and `env.get_sensor_left_value()` functions, and that you are using the `env.step(action)` function to apply actions within the main loop.  Also, ensure all variables used are defined.  Pay close attention to the use of `None` in the sensor readings and if/else statements.  Finally, correctly apply the `max()` function to determine the greatest sensor reading."]	Car	[{"message": "Missing call to `env.get_sensor_forward_value()`. This function needs to be called inside the infinite while loop to retrieve the forward sensor value of the car.", "line": 58}, {"message": "Missing call to `env.get_sensor_right_value()`. This function needs to be called inside the infinite while loop to retrieve the right sensor value for the car.", "line": 58}, {"message": "Missing call to `env.get_sensor_left_value()`. This function needs to be called inside the infinite while loop to retrieve the left sensor value for the car.", "line": 58}, {"message": "The `Forward` sensor reading should use the variable `None`, but `_______` was used instead.", "line": 21}, {"message": "The `Right` sensor reading should use the variable `None`, but `_____` was used instead.", "line": 21}, {"message": "The `Left` sensor reading should use the variable `None`, but `____` was used instead.", "line": 21}, {"message": "A variable must be assigned using `max(sensor_readings, key=sensor_readings.get)`. Check `max()` is applied correctly.", "line": 9}, {"message": "The if-else statement should use `None`, but `__________________` was used instead.", "line": 34}, {"message": "The if-else statement should use `None`, but `__________________` was used instead.", "line": 36}, {"message": "The if-else statement should use `None`, but `__________________` was used instead.", "line": 38}, {"message": "Missing required call to `env.step(action)` is missing. The simulation may not function correctly. Check that it is called inside the infinite loop to execute movement.", "line": 58}, {"message": "Variable '_______' is used but not defined.", "line": 58}, {"message": "Variable '____' is used but not defined.", "line": 58}, {"message": "Variable '_____' is used but not defined.", "line": 58}, {"message": "Variable '__________________' is used but not defined.", "line": 58}]	2025-04-22 18:21:30.124956	99
126	# Autonomous Car Robot Task: Implement an autonomous movement algorithm for a robot car.\r\n# The car continuously moves using sensor data and makes real-time decisions on direction.\r\n\r\n# Given: The infinite while loop to move the car in an autonomous manner\r\nwhile True:\r\n    # Given: The action vector [linear velocity, angular veloctiy]\r\n    # - Linear velocity controls the car's forward/backward movement.\r\n    # - Angular velocity controls the turning angle (left/right).\r\n    action = [0.00, 0.000] # Default: No movement initially\r\n\r\n    # TODO: Retrive the forward sensors value and store it in a variable\r\n    forward_val = env.get_sensor_forward_value()\r\n    \r\n    # TODO: Retrive the right sensors value and store it in a variable\r\n    right_val = env.get_sensor_right_value()\r\n    \r\n    # TODO: Retrive the left sensors value and store it in a variable\r\n    left_val = env.get_sensor_left_value()\r\n\r\n    # TODO: Fill in the dictionary withe the variables you just created to store the sensor values\r\n    sensor_readings = {\r\n        "Forward": forward_val,\r\n        "Right": right_val,\r\n        "Left": left_val\r\n    }\r\n    \r\n    # TODO: Determine which direction has the highest sensor value\r\n    # - Use `max()` to find the key (direction) in `sensor_readings` with the greatest value.\r\n    # - The `key=sensor_readings.get` argument ensures that the maximum is selected based on the sensor reading values.\r\n    # - Store the result in a variable named greatest_direction to decide the car's movement direction.\r\n    max_value = max(sensor_readings, key = sensor_readings.get())\r\n    \r\n    # TODO: Fill in the if else statement below with the greatest direction variable you just stored the greatest direction in on each fill in the blank line\r\n    if max_value == "Forward":\r\n        action = [0.01, 0.0]   # Move forward\r\n    elif max_value == "Right":\r\n        action = [0.005, -0.007]  # Turn right\r\n    elif max_value == "Left":\r\n        action = [0.005, 0.007]  # Turn Left\r\n\r\n    # TODO: Apply the action we have defined in the if else statement to the environment\r\n\t\r\n\r\n    # **IGNORE: This is here to prevent infinite loops**\r\n    success = False\r\n    for contact in env.sim.data.contact:\r\n        geom1 = env.sim.model.geom_id2name(contact.geom1)\r\n        geom2 = env.sim.model.geom_id2name(contact.geom2)\r\n\r\n        if geom1 is not None and geom2 is not None:\r\n            if "chasis" in geom1 or "chasis" in geom2:\r\n                if "chasis" not in geom1:\r\n                    other_geom = geom1 \r\n                else:\r\n                    other_geom = geom2\r\n\r\n                geom_id = env.sim.model.geom_name2id(other_geom)\r\n                rgba = env.sim.model.geom_rgba[geom_id]\r\n                color = rgba[:3]\r\n                target_color = [0, 0, 1]  # RGB for blue\r\n                if np.array_equal(color, target_color):  # Exact match comparison\r\n                    success = True\r\n                    break\r\n    if success:\r\n        break\r\n    # **STOP IGNORING: Continue coding as normal**\r\n\r\n    # Given: For the loop to run like a real-world autonomous car\r\n    time.sleep(0.00001) \r\n                    \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n	\N	["1. Review each TODO comment and ensure you've correctly implemented the instructions provided. Pay close attention to variable assignments and conditional statements.  Also, make sure you're using the correct function calls to interact with the simulation environment."]	Car	[{"message": "A variable must be assigned using `max(sensor_readings, key=sensor_readings.get)`. Check `max()` is applied correctly.", "line": 9}, {"message": "The if-else statement should use `None`, but `max_value` was used instead.", "line": 34}, {"message": "The if-else statement should use `None`, but `max_value` was used instead.", "line": 36}, {"message": "The if-else statement should use `None`, but `max_value` was used instead.", "line": 38}, {"message": "Missing required call to `env.step(action)` is missing. The simulation may not function correctly. Check that it is called inside the infinite loop to execute movement.", "line": 58}]	2025-04-22 18:24:16.58429	99
127	# Autonomous Car Robot Task: Implement an autonomous movement algorithm for a robot car.\r\n# The car continuously moves using sensor data and makes real-time decisions on direction.\r\n\r\n# Given: The infinite while loop to move the car in an autonomous manner\r\nwhile True:\r\n    # Given: The action vector [linear velocity, angular veloctiy]\r\n    # - Linear velocity controls the car's forward/backward movement.\r\n    # - Angular velocity controls the turning angle (left/right).\r\n    action = [0.00, 0.000] # Default: No movement initially\r\n\r\n    # TODO: Retrive the forward sensors value and store it in a variable\r\n    forward_val = env.get_sensor_forward_value()\r\n    \r\n    # TODO: Retrive the right sensors value and store it in a variable\r\n    right_val = env.get_sensor_right_value()\r\n    \r\n    # TODO: Retrive the left sensors value and store it in a variable\r\n    left_val = env.get_sensor_left_value()\r\n\r\n    # TODO: Fill in the dictionary withe the variables you just created to store the sensor values\r\n    sensor_readings = {\r\n        "Forward": forward_val,\r\n        "Right": right_val,\r\n        "Left": left_val\r\n    }\r\n    \r\n    # TODO: Determine which direction has the highest sensor value\r\n    # - Use `max()` to find the key (direction) in `sensor_readings` with the greatest value.\r\n    # - The `key=sensor_readings.get` argument ensures that the maximum is selected based on the sensor reading values.\r\n    # - Store the result in a variable named greatest_direction to decide the car's movement direction.\r\n    max_value = max(sensor_readings, key = sensor_readings.get())\r\n    \r\n    # TODO: Fill in the if else statement below with the greatest direction variable you just stored the greatest direction in on each fill in the blank line\r\n    if max_value == "Forward":\r\n        action = [0.01, 0.0]   # Move forward\r\n    elif max_value == "Right":\r\n        action = [0.005, -0.007]  # Turn right\r\n    elif max_value == "Left":\r\n        action = [0.005, 0.007]  # Turn Left\r\n\r\n    # TODO: Apply the action we have defined in the if else statement to the environment\r\n    env.step(action)\r\n\r\n    # **IGNORE: This is here to prevent infinite loops**\r\n    success = False\r\n    for contact in env.sim.data.contact:\r\n        geom1 = env.sim.model.geom_id2name(contact.geom1)\r\n        geom2 = env.sim.model.geom_id2name(contact.geom2)\r\n\r\n        if geom1 is not None and geom2 is not None:\r\n            if "chasis" in geom1 or "chasis" in geom2:\r\n                if "chasis" not in geom1:\r\n                    other_geom = geom1 \r\n                else:\r\n                    other_geom = geom2\r\n\r\n                geom_id = env.sim.model.geom_name2id(other_geom)\r\n                rgba = env.sim.model.geom_rgba[geom_id]\r\n                color = rgba[:3]\r\n                target_color = [0, 0, 1]  # RGB for blue\r\n                if np.array_equal(color, target_color):  # Exact match comparison\r\n                    success = True\r\n                    break\r\n    if success:\r\n        break\r\n    # **STOP IGNORING: Continue coding as normal**\r\n\r\n    # Given: For the loop to run like a real-world autonomous car\r\n    time.sleep(0.00001) \r\n                    \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n	get expected at least 1 argument, got 0	\N	Car	\N	2025-04-22 18:25:15.477086	99
128	# Autonomous Car Robot Task: Implement an autonomous movement algorithm for a robot car.\r\n# The car continuously moves using sensor data and makes real-time decisions on direction.\r\n\r\n# Given: The infinite while loop to move the car in an autonomous manner\r\nwhile True:\r\n    # Given: The action vector [linear velocity, angular veloctiy]\r\n    # - Linear velocity controls the car's forward/backward movement.\r\n    # - Angular velocity controls the turning angle (left/right).\r\n    action = [0.00, 0.000] # Default: No movement initially\r\n\r\n    # TODO: Retrive the forward sensors value and store it in a variable\r\n    forward_val = env.get_sensor_forward_value()\r\n    \r\n    # TODO: Retrive the right sensors value and store it in a variable\r\n    right_val = env.get_sensor_right_value()\r\n    \r\n    # TODO: Retrive the left sensors value and store it in a variable\r\n    left_val = env.get_sensor_left_value()\r\n\r\n    # TODO: Fill in the dictionary withe the variables you just created to store the sensor values\r\n    sensor_readings = {\r\n        "Forward": forward_val,\r\n        "Right": right_val,\r\n        "Left": left_val\r\n    }\r\n    \r\n    # TODO: Determine which direction has the highest sensor value\r\n    # - Use `max()` to find the key (direction) in `sensor_readings` with the greatest value.\r\n    # - The `key=sensor_readings.get` argument ensures that the maximum is selected based on the sensor reading values.\r\n    # - Store the result in a variable named greatest_direction to decide the car's movement direction.\r\n    max_value = max(sensor_readings, key = sensor_readings.get())\r\n    \r\n    # TODO: Fill in the if else statement below with the greatest direction variable you just stored the greatest direction in on each fill in the blank line\r\n    if max_value == "Forward":\r\n        action = [0.01, 0.0]   # Move forward\r\n    elif max_value == "Right":\r\n        action = [0.005, -0.007]  # Turn right\r\n    elif max_value == "Left":\r\n        action = [0.005, 0.007]  # Turn Left\r\n\r\n    # TODO: Apply the action we have defined in the if else statement to the environment\r\n    env.step(action)\r\n\r\n    # **IGNORE: This is here to prevent infinite loops**\r\n    success = False\r\n    for contact in env.sim.data.contact:\r\n        geom1 = env.sim.model.geom_id2name(contact.geom1)\r\n        geom2 = env.sim.model.geom_id2name(contact.geom2)\r\n\r\n        if geom1 is not None and geom2 is not None:\r\n            if "chasis" in geom1 or "chasis" in geom2:\r\n                if "chasis" not in geom1:\r\n                    other_geom = geom1 \r\n                else:\r\n                    other_geom = geom2\r\n\r\n                geom_id = env.sim.model.geom_name2id(other_geom)\r\n                rgba = env.sim.model.geom_rgba[geom_id]\r\n                color = rgba[:3]\r\n                target_color = [0, 0, 1]  # RGB for blue\r\n                if np.array_equal(color, target_color):  # Exact match comparison\r\n                    success = True\r\n                    break\r\n    if success:\r\n        break\r\n    # **STOP IGNORING: Continue coding as normal**\r\n\r\n    # Given: For the loop to run like a real-world autonomous car\r\n    time.sleep(0.00001) \r\n                    \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n	get expected at least 1 argument, got 0	\N	Car	\N	2025-04-22 18:25:24.686225	99
129	# Autonomous Car Robot Task: Implement an autonomous movement algorithm for a robot car.\r\n# The car continuously moves using sensor data and makes real-time decisions on direction.\r\n\r\n# Given: The infinite while loop to move the car in an autonomous manner\r\nwhile True:\r\n    # Given: The action vector [linear velocity, angular veloctiy]\r\n    # - Linear velocity controls the car's forward/backward movement.\r\n    # - Angular velocity controls the turning angle (left/right).\r\n    action = [0.00, 0.000] # Default: No movement initially\r\n\r\n    # TODO: Retrive the forward sensors value and store it in a variable\r\n    forward_val = env.get_sensor_forward_value()\r\n    \r\n    # TODO: Retrive the right sensors value and store it in a variable\r\n    right_val = env.get_sensor_right_value()\r\n    \r\n    # TODO: Retrive the left sensors value and store it in a variable\r\n    left_val = env.get_sensor_left_value()\r\n\r\n    # TODO: Fill in the dictionary withe the variables you just created to store the sensor values\r\n    sensor_readings = {\r\n        "Forward": forward_val,\r\n        "Right": right_val,\r\n        "Left": left_val\r\n    }\r\n    \r\n    # TODO: Determine which direction has the highest sensor value\r\n    # - Use `max()` to find the key (direction) in `sensor_readings` with the greatest value.\r\n    # - The `key=sensor_readings.get` argument ensures that the maximum is selected based on the sensor reading values.\r\n    # - Store the result in a variable named greatest_direction to decide the car's movement direction.\r\n    max_value = max(sensor_readings, key = sensor_readings.get(sensor_readings))\r\n    \r\n    # TODO: Fill in the if else statement below with the greatest direction variable you just stored the greatest direction in on each fill in the blank line\r\n    if max_value == "Forward":\r\n        action = [0.01, 0.0]   # Move forward\r\n    elif max_value == "Right":\r\n        action = [0.005, -0.007]  # Turn right\r\n    elif max_value == "Left":\r\n        action = [0.005, 0.007]  # Turn Left\r\n\r\n    # TODO: Apply the action we have defined in the if else statement to the environment\r\n    env.step(action)\r\n\r\n    # **IGNORE: This is here to prevent infinite loops**\r\n    success = False\r\n    for contact in env.sim.data.contact:\r\n        geom1 = env.sim.model.geom_id2name(contact.geom1)\r\n        geom2 = env.sim.model.geom_id2name(contact.geom2)\r\n\r\n        if geom1 is not None and geom2 is not None:\r\n            if "chasis" in geom1 or "chasis" in geom2:\r\n                if "chasis" not in geom1:\r\n                    other_geom = geom1 \r\n                else:\r\n                    other_geom = geom2\r\n\r\n                geom_id = env.sim.model.geom_name2id(other_geom)\r\n                rgba = env.sim.model.geom_rgba[geom_id]\r\n                color = rgba[:3]\r\n                target_color = [0, 0, 1]  # RGB for blue\r\n                if np.array_equal(color, target_color):  # Exact match comparison\r\n                    success = True\r\n                    break\r\n    if success:\r\n        break\r\n    # **STOP IGNORING: Continue coding as normal**\r\n\r\n    # Given: For the loop to run like a real-world autonomous car\r\n    time.sleep(0.00001) \r\n                    \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n	unhashable type: 'dict'	\N	Car	\N	2025-04-22 18:26:22.259795	99
131	# Autonomous Car Robot Task: Implement an autonomous movement algorithm for a robot car.\r\n# The car continuously moves using sensor data and makes real-time decisions on direction.\r\n\r\n# Given: The infinite while loop to move the car in an autonomous manner\r\nwhile True:\r\n    # Given: The action vector [linear velocity, angular veloctiy]\r\n    # - Linear velocity controls the car's forward/backward movement.\r\n    # - Angular velocity controls the turning angle (left/right).\r\n    action = [0.00, 0.000] # Default: No movement initially\r\n\r\n    # TODO: Retrive the forward sensors value and store it in a variable\r\n    forward_val = env.get_sensor_forward_value()\r\n    \r\n    # TODO: Retrive the right sensors value and store it in a variable\r\n    right_val = env.get_sensor_right_value()\r\n    \r\n    # TODO: Retrive the left sensors value and store it in a variable\r\n    left_val = env.get_sensor_left_value()\r\n\r\n    # TODO: Fill in the dictionary withe the variables you just created to store the sensor values\r\n    sensor_readings = {\r\n        "Forward": forward_val,\r\n        "Right": right_val,\r\n        "Left": left_val\r\n    }\r\n    \r\n    # TODO: Determine which direction has the highest sensor value\r\n    # - Use `max()` to find the key (direction) in `sensor_readings` with the greatest value.\r\n    # - The `key=sensor_readings.get` argument ensures that the maximum is selected based on the sensor reading values.\r\n    # - Store the result in a variable named greatest_direction to decide the car's movement direction.\r\n    max_value = max(sensor_readings, key = sensor_readings.get)\r\n    \r\n    # TODO: Fill in the if else statement below with the greatest direction variable you just stored the greatest direction in on each fill in the blank line\r\n    if max_value == "Forward":\r\n        action = [0.01, 0.0]   # Move forward\r\n    elif max_value == "Right":\r\n        action = [0.005, -0.007]  # Turn right\r\n    elif max_value == "Left":\r\n        action = [0.005, 0.007]  # Turn Left\r\n\r\n    # TODO: Apply the action we have defined in the if else statement to the environment\r\n    env.step(action)\r\n\r\n    # **IGNORE: This is here to prevent infinite loops**\r\n    success = False\r\n    for contact in env.sim.data.contact:\r\n        geom1 = env.sim.model.geom_id2name(contact.geom1)\r\n        geom2 = env.sim.model.geom_id2name(contact.geom2)\r\n\r\n        if geom1 is not None and geom2 is not None:\r\n            if "chasis" in geom1 or "chasis" in geom2:\r\n                if "chasis" not in geom1:\r\n                    other_geom = geom1 \r\n                else:\r\n                    other_geom = geom2\r\n\r\n                geom_id = env.sim.model.geom_name2id(other_geom)\r\n                rgba = env.sim.model.geom_rgba[geom_id]\r\n                color = rgba[:3]\r\n                target_color = [0, 0, 1]  # RGB for blue\r\n                if np.array_equal(color, target_color):  # Exact match comparison\r\n                    success = True\r\n                    break\r\n    if success:\r\n        break\r\n    # **STOP IGNORING: Continue coding as normal**\r\n\r\n    # Given: For the loop to run like a real-world autonomous car\r\n    time.sleep(0.00001) \r\n                    \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n	\N	\N	Car	\N	2025-04-22 18:27:49.254836	99
130	# Autonomous Car Robot Task: Implement an autonomous movement algorithm for a robot car.\r\n# The car continuously moves using sensor data and makes real-time decisions on direction.\r\n\r\n# Given: The infinite while loop to move the car in an autonomous manner\r\nwhile True:\r\n    # Given: The action vector [linear velocity, angular veloctiy]\r\n    # - Linear velocity controls the car's forward/backward movement.\r\n    # - Angular velocity controls the turning angle (left/right).\r\n    action = [0.00, 0.000] # Default: No movement initially\r\n\r\n    # TODO: Retrive the forward sensors value and store it in a variable\r\n    forward_val = env.get_sensor_forward_value()\r\n    \r\n    # TODO: Retrive the right sensors value and store it in a variable\r\n    right_val = env.get_sensor_right_value()\r\n    \r\n    # TODO: Retrive the left sensors value and store it in a variable\r\n    left_val = env.get_sensor_left_value()\r\n\r\n    # TODO: Fill in the dictionary withe the variables you just created to store the sensor values\r\n    sensor_readings = {\r\n        "Forward": forward_val,\r\n        "Right": right_val,\r\n        "Left": left_val\r\n    }\r\n    \r\n    # TODO: Determine which direction has the highest sensor value\r\n    # - Use `max()` to find the key (direction) in `sensor_readings` with the greatest value.\r\n    # - The `key=sensor_readings.get` argument ensures that the maximum is selected based on the sensor reading values.\r\n    # - Store the result in a variable named greatest_direction to decide the car's movement direction.\r\n    max_value = max(sensor_readings, key = sensor_readings.get())\r\n    \r\n    # TODO: Fill in the if else statement below with the greatest direction variable you just stored the greatest direction in on each fill in the blank line\r\n    if max_value == "Forward":\r\n        action = [0.01, 0.0]   # Move forward\r\n    elif max_value == "Right":\r\n        action = [0.005, -0.007]  # Turn right\r\n    elif max_value == "Left":\r\n        action = [0.005, 0.007]  # Turn Left\r\n\r\n    # TODO: Apply the action we have defined in the if else statement to the environment\r\n    env.step(action)\r\n\r\n    # **IGNORE: This is here to prevent infinite loops**\r\n    success = False\r\n    for contact in env.sim.data.contact:\r\n        geom1 = env.sim.model.geom_id2name(contact.geom1)\r\n        geom2 = env.sim.model.geom_id2name(contact.geom2)\r\n\r\n        if geom1 is not None and geom2 is not None:\r\n            if "chasis" in geom1 or "chasis" in geom2:\r\n                if "chasis" not in geom1:\r\n                    other_geom = geom1 \r\n                else:\r\n                    other_geom = geom2\r\n\r\n                geom_id = env.sim.model.geom_name2id(other_geom)\r\n                rgba = env.sim.model.geom_rgba[geom_id]\r\n                color = rgba[:3]\r\n                target_color = [0, 0, 1]  # RGB for blue\r\n                if np.array_equal(color, target_color):  # Exact match comparison\r\n                    success = True\r\n                    break\r\n    if success:\r\n        break\r\n    # **STOP IGNORING: Continue coding as normal**\r\n\r\n    # Given: For the loop to run like a real-world autonomous car\r\n    time.sleep(0.00001) \r\n                    \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n	get expected at least 1 argument, got 0	\N	Car	\N	2025-04-22 18:26:48.400682	99
\.


--
-- Data for Name: user_points; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.user_points (user_points_id, num_points, user_id) FROM stdin;
1	1000	94
2	2000	95
3	1000	125
4	3000	127
\.


--
-- Data for Name: user_time_logs; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.user_time_logs (time_log_id, page_context, start_time, end_time, duration, user_id) FROM stdin;
19	Fetch Reach	2025-04-21 20:28:03.571996	2025-04-21 13:29:51.162	106.2	94
20	Fetch Reach	2025-04-22 00:04:48.626161	2025-04-21 17:05:23.387	31.914	93
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.users (user_id, username, first_name, last_name, email, password, role_id, created_at) FROM stdin;
124	TestStudent	Test	Test	testtest@gmail.com	\\x243262243132246e792e5577373433707330683766685057572f4676754a4a782f76364c524e7934555932557537363565562f57516b76526e687065	1	2025-04-21 20:47:04.10132
125	TS	Test	Student	tests@gmail.com	\\x243262243132246f7a6365354d522e4f6e794f46714a49422e4167596530415731336e7a786371335476794d53796742792e42674a774e4378357743	2	2025-04-21 20:47:32.380386
92	admin	Admin	One	admin@example.com	\\x243262243132247a57614b616b48304d4f7844393969624e52416f317565416f56494d336570526c2e3364306d6461702f5573315a54646f50356469	3	2025-04-14 01:23:07.514598
93	InstructorOne	Instructor	One	instructorone@gmail.com	\\x24326224313224696f56645274706d5a5742327847704c61756439666567506e4f36512f664f682f655445694a64766977624e635752337270527365	1	2025-04-14 08:24:41.28865
94	DemoOne	Demo	One	demoone@gmail.com	\\x2432622431322434444e37623079475638466d613745334d6a384a6e2e643078666a75717946777349792e6f624f7338487a467179796c735666314f	2	2025-04-14 08:31:25.739567
95	DemoTwo	Demo	Two	demotwo@gmail.com	\\x2432622431322439424b595471366e38597a783031654253356a696b2e4c65522e4e35467478572e346e58674b75374f57335649336e4d72656d4536	2	2025-04-14 01:38:32.089689
96	DemoThree	Demo	Three	demothree@gmail.com	\\x24326224313224546167484a577847366d7a6b6d7166645878546e5275437a5571372e4d31372f6635796c4b30755078477773366d4e66503866466d	2	2025-04-14 01:38:32.089689
97	DemoFour	Demo	Four	demofour@gmail.com	\\x243262243132245978512f6e7439415435306f65454e7771764866706539386c653552466459586342693346784e715362734f7a77325a443934624b	2	2025-04-14 01:38:32.089689
98	DemoFive	Demo	Five	demofive@gmail.com	\\x2432622431322478446e6968745a4c38694b67372e357a5933555953756a69544865764e4f434e6f4b44303871756f7559555a7141416b73676d5153	2	2025-04-14 01:38:32.089689
99	DemoSix	Demo	Six	demosix@gmail.com	\\x2432622431322454795034775155464d754d596175587369366270642e346272642f5a694f416b384c4561776739316f4a4f345479422e6b61464447	2	2025-04-14 01:38:32.089689
100	DemoSeven	Demo	Seven	demoseven@gmail.com	\\x2432622431322474474443626d5469372e714d7556396e734b4243776564616d6b644c2e76597246386b59796c5a666d6e732e6e684938615a554153	2	2025-04-14 01:38:32.089689
101	DemoEight	Demo	Eight	demoeight@gmail.com	\\x243262243132245230423271647568427838652f6a3164623476334f4f6931442f687a706b62784d797562374f38744a69506351636b534f5a307975	2	2025-04-14 01:38:32.089689
102	DemoNine	Demo	Nine	demonine@gmail.com	\\x24326224313224534e5057596a4b48313879674d7874585746796d622e61524e6234647a6f58477a354e6142326d50484f514e53756b754179725271	2	2025-04-14 01:38:32.089689
103	DemoTen	Demo	Ten	demoten@gmail.com	\\x243262243132243173786e646a434e637a486553524176587867624575336d6e4269663550466a77366f44513749666d452f69796749666e73705053	2	2025-04-14 01:38:32.089689
104	DemoEleven	Demo	Eleven	demoeleven@gmail.com	\\x24326224313224556d795969436e4a71324b642e61324f564637354c2e6f4670544855652f306a673456616f33683944664343647563696a4b43564b	2	2025-04-14 01:38:32.089689
105	DemoTwelve	Demo	Twelve	demotwelve@gmail.com	\\x243262243132245146472f612e6a4a7276766e5148745234516272372e5931414c306e67547646696566543249587156756b746747636e7154512f47	2	2025-04-14 01:38:32.089689
106	DemoThirteen	Demo	Thirteen	demothirteen@gmail.com	\\x24326224313224734f7557506a32417846394574344c43392e692e33656d464d2e464e4e4b6261586f75462e4b79473044756a54375041433933754f	2	2025-04-14 01:38:32.089689
107	DemoFourteen	Demo	Fourteen	demofourteen@gmail.com	\\x2432622431322469495533663777376c7230467579544a30425061324f346b2e634f6865316e6573353242416f73344d636d3556634e425439625979	2	2025-04-14 01:38:32.089689
108	DemoFifteen	Demo	Fifteen	demofifteen@gmail.com	\\x243262243132245a574c7839736d4a78787773562f3866567757706c754b6a4470354353696d78675541787934616a574946796f7a4f704d636f5975	2	2025-04-14 01:38:32.089689
109	DemoSixteen	Demo	Sixteen	demosixteen@gmail.com	\\x243262243132246b564d337041487748435241694e766f552e6531494f724f536e534731425536446a56426b6e7a44465375356c37476661644c7275	2	2025-04-14 01:38:32.089689
110	DemoSeventeen	Demo	Seventeen	demoseventeen@gmail.com	\\x24326224313224655870745957306c2f522e49674d54354c33705131756e61346b7a55413874726d617049463677356d507162586a57705437654236	2	2025-04-14 01:38:32.089689
111	DemoEighteen	Demo	Eighteen	demoeighteen@gmail.com	\\x243262243132244e71366c57797950682e47584f59785062347271782e73644a4845594277626d696d5a59376c505535577175544c3247372e385536	2	2025-04-14 01:38:32.089689
112	DemoNineteen	Demo	Nineteen	demonineteen@gmail.com	\\x243262243132246a357265733846436a77566c4d515a692e766a5a617545416645556d764d4f4b526c537877415874342e535a6374577a376554544b	2	2025-04-14 01:38:32.089689
113	DemoTwenty	Demo	Twenty	demotwenty@gmail.com	\\x2432622431322477536e346665524741336f367a65585451734a446c756246764a6f4e4b494b7335515935306a6962666c444a47614b4137617a3732	2	2025-04-14 01:38:32.089689
126	TS2	Test	Student	test2@gmail.com	\\x243262243132242f74326e75336a7855695669514c497354795a784165665849534a704a565a706f56786b47576d75564d434677636f695868706c69	2	2025-04-21 22:50:50.294475
127	TS3	Test	Student	test3@gmail.com	\\x2432622431322467356d6463444c625567415464524270746e556c654f4a786c4c707653517a34783047453763667a4b42436a6379777153594d6447	2	2025-04-21 22:52:33.104583
114	DemoTwentyOne	Demo	TwentyOne	demotwentyone@gmail.com	\\x24326224313224662e3864516b69635239526b72793572646648776b6574797662566a506f4c7752752e3266374b50723077487a6333544c532f6375	2	2025-04-14 01:38:32.089689
115	DemoTwentyTwo	Demo	TwentyTwo	demotwentytwo@gmail.com	\\x2432622431322454446b4a42577a4c7337715a634a44564452654a492e41635a6f49747978726b4b7461632e554d4c64456952554e46664472563175	2	2025-04-14 01:38:32.089689
116	DemoTwentyThree	Demo	TwentyThree	demotwentythree@gmail.com	\\x2432622431322445654e632f51726e57343676504b7078464b4a42562e4a626c39387253435a483539382e647063557077394c4262594731495a6c53	2	2025-04-14 01:38:32.089689
117	DemoTwentyFour	Demo	TwentyFour	demotwentyfour@gmail.com	\\x243262243132244e454941314c386962337373496247716779305a4c4f384e356138546d6a4d3371643178446f4e486876586d65487633316e42664b	2	2025-04-14 01:38:32.089689
118	DemoTwentyFive	Demo	TwentyFive	demotwentyfive@gmail.com	\\x243262243132244d2f58496f597944496a65542f6549474f2e2e7035754c7344344a66566957747044634d6d64533646314e7a4d724a634f586d7747	2	2025-04-14 01:38:32.089689
128	COREmail	Core	Email	officialwarerecovery@gmail.com	\\x2432622431322438536557426a30753753586b6b374c5669313933722e4a5737622e4c4869572f6b5a4741652e74364a2f6e434b4a796b476b415157	2	2025-04-21 23:13:47.718315
119	DemoTwentySix	Demo	TwentySix	demotwentysix@gmail.com	\\x24326224313224314a37566575507a39726b445253746c6436554e3175594f2e546a66506e554f4850627370326176676b69326a4f494e6973346661	2	2025-04-14 01:38:32.089689
120	DemoTwentySeven	Demo	TwentySeven	demotwentyseven@gmail.com	\\x243262243132247464576b65793452686a656a714a796a4f6f59667475564533676f367141456f57457430544a616748397272304b4c755334676953	2	2025-04-14 01:38:32.089689
121	DemoTwentyEight	Demo	TwentyEight	demotwentyeight@gmail.com	\\x243262243132247562695769303637494e45546241784f796b56774675674a4835674332743979726e51513548743270394e646f67705561424e6a75	2	2025-04-14 01:38:32.089689
122	DemoTwentyNine	Demo	TwentyNine	demotwentynine@gmail.com	\\x24326224313224674661466c696a6d723071387a46725a4d455943444f4e584359307a3763633965664f414c6c3631325363635432654c2e6830374b	2	2025-04-14 01:38:32.089689
\.


--
-- Name: class_codes_class_code_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.class_codes_class_code_id_seq', 15, true);


--
-- Name: classes_class_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.classes_class_id_seq', 45, true);


--
-- Name: course_subsections_course_subsection_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.course_subsections_course_subsection_id_seq', 92, true);


--
-- Name: courses_course_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.courses_course_id_seq', 38, true);


--
-- Name: enrollment_enrollment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.enrollment_enrollment_id_seq', 81, true);


--
-- Name: feedback_feedback_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.feedback_feedback_id_seq', 1, true);


--
-- Name: permissions_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.permissions_permission_id_seq', 1, true);


--
-- Name: roles_role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.roles_role_id_seq', 4, true);


--
-- Name: scoreboard_scoreboard_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.scoreboard_scoreboard_id_seq', 1, true);


--
-- Name: student_assigned_course_subse_assigned_course_subsection_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.student_assigned_course_subse_assigned_course_subsection_id_seq', 3061, true);


--
-- Name: student_assigned_courses_student_assigned_courses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.student_assigned_courses_student_assigned_courses_id_seq', 749, true);


--
-- Name: student_grades_student_grades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.student_grades_student_grades_id_seq', 103, true);


--
-- Name: user_code_logs_user_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.user_code_logs_user_log_id_seq', 131, true);


--
-- Name: user_points_user_points_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.user_points_user_points_id_seq', 4, true);


--
-- Name: user_time_logs_user_time_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.user_time_logs_user_time_id_seq', 20, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.users_user_id_seq', 128, true);


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
-- Name: student_grades student_grades_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.student_grades
    ADD CONSTRAINT student_grades_pkey PRIMARY KEY (student_grades_id);


--
-- Name: user_code_logs user_code_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.user_code_logs
    ADD CONSTRAINT user_code_logs_pkey PRIMARY KEY (user_log_id);


--
-- Name: user_points user_points_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.user_points
    ADD CONSTRAINT user_points_pkey PRIMARY KEY (user_points_id);


--
-- Name: user_time_logs user_time_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.user_time_logs
    ADD CONSTRAINT user_time_logs_pkey PRIMARY KEY (time_log_id);


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
-- Name: user_code_logs fk_user; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.user_code_logs
    ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE SET NULL;


--
-- Name: user_time_logs fk_user; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.user_time_logs
    ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


--
-- Name: user_points fk_user; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.user_points
    ADD CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE;


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
-- Name: student_grades student_grades_course_subsection_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.student_grades
    ADD CONSTRAINT student_grades_course_subsection_id_fkey FOREIGN KEY (course_subsection_id) REFERENCES public.course_subsections(course_subsection_id);


--
-- Name: student_grades student_grades_student_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.student_grades
    ADD CONSTRAINT student_grades_student_id_fkey FOREIGN KEY (student_id) REFERENCES public.users(user_id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: testuser
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;


--
-- PostgreSQL database dump complete
--

