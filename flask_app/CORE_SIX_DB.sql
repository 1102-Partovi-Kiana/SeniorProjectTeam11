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
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: testuser
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: class_codes; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.class_codes (class_code_id, class_id, class_code) FROM stdin;
12	35	h8wZCvkZ
14	43	ccXwQnbR
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
41	CS205	1001	39	2025-03-31	2025-03-31
42	TST101	1001	39	2025-04-07	2025-04-14
43	TST102	1001	39	2025-04-07	2025-04-07
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
23	Robots in CORE	Discover the heart of CORE: meet our virtual robots, designed for you.	3	Beginner Friendly	t	30 minutes	course3_card
24	How to Use the Lab	Get familiar with CORE's Virtual Robotics Lab and explore live simulations, an interactive, hands-on learning experience, and coding feedback.	4	Beginner Friendly	t	1 hour	course1_card
25	Basic Coding Practices	Master the basics of coding, building yourself a strong foundation, involving a review of common coding practices and debugging techniques.	5	Beginner Friendly	t	1 hour	course4_card
27	Fetch Reach Robot	Master control and precision as you learn to code the Fetch Reach Robot.	7	Beginner Friendly	t	2 hours	course6_card
30	Fetch Pick & Place Robot	Become proficient in robotic object manipulation with the Fetch Pick and Place Robot.	8	Intermediate	t	2 hours	course7_card
31	Fetch Stack Blocks Robot	Hone the precision of stacking blocks using the Fetch Robot and improve your spatial manipulation.	9	Intermediate	t	1 hour	course8_card
32	Fetch Color Sort Robot	Learn to algorithmically move the Fetch Robot to sort and organize objects based on their colors.	10	Intermediate	t	2 hours	course9_card
33	Fetch Robot w/ Sensors	Unlock the power of sensors by teaching the Fetch Robot to detect, classify, and organize objects.	11	Intermediate	t	2 hours	course10_card
37	Autonomous Car w/ Sensors	Learn about Deep Q-Learning algorithms to create a self-driving car.	12	Advanced	t	2 hours	course11_card
\.


--
-- Data for Name: enrollment; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.enrollment (enrollment_id, user_id, class_id) FROM stdin;
12	37	35
14	91	35
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
144	f	1.17	56
145	f	1.18	56
146	f	1.19	56
147	f	1.21	56
138	t	1.11	56
139	t	1.12	56
140	t	1.13	56
141	t	1.14	56
142	t	1.15	56
148	t	1.9	56
143	t	1.16	56
177	f	1.17	89
178	f	1.18	89
179	f	1.19	89
180	f	1.21	89
171	t	1.11	89
172	t	1.12	89
173	t	1.13	89
174	t	1.14	89
175	t	1.15	89
181	t	1.9	89
176	t	1.16	89
188	f	1.16	91
189	f	1.17	91
190	f	1.18	91
191	f	1.19	91
192	f	1.21	91
193	f	1.9	91
127	f	1.11	54
128	f	1.12	54
129	f	1.13	54
130	f	1.14	54
131	f	1.15	54
132	f	1.16	54
137	f	1.9	54
133	f	1.17	54
134	f	1.18	54
135	f	1.19	54
136	f	1.21	54
183	t	1.11	91
184	t	1.12	91
185	t	1.13	91
186	t	1.14	91
187	t	1.15	91
\.


--
-- Data for Name: student_assigned_courses; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.student_assigned_courses (student_assigned_courses_id, course_id, user_id) FROM stdin;
3	21	54
4	22	54
5	23	54
6	24	54
7	21	56
8	22	56
9	23	56
10	24	56
40	21	89
41	22	89
42	23	89
43	24	89
45	21	91
46	22	91
47	23	91
48	24	91
\.


--
-- Data for Name: student_grades; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.student_grades (student_grades_id, student_id, percentage_grade, course_subsection_id, created_at) FROM stdin;
5	56	90	21	2025-03-17 21:08:37.295375
38	89	80	21	2025-03-17 21:35:13.363922
40	91	60	21	2025-04-07 06:07:59.17246
41	91	70	21	2025-04-07 06:08:07.073826
42	39	50	21	2025-04-11 02:37:30.726475
\.


--
-- Data for Name: user_code_logs; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.user_code_logs (user_log_id, code, error, hints, page_context, static_issues, created_at, user_id) FROM stdin;
39	# Fetch Reach Robot Task: Guide the robot's gripper to the ball's position\r\n\r\n# Given: Set a distance threshold to determine when the gripper is close enough to the ball.\r\ndistance_threshold = 0.01\r\n\r\n# Given: Define a step size for each movement iteration.\r\nstep_size = 0.05\r\n\r\n# TODO: Use the environment's method to get the ball's position and store it in a variable.\r\n\r\n\r\n# TODO: Use the environment's method to get the gripper's position and store it in a variable.\r\n\r\n\r\n# TODO: Calculate the direction vector from the gripper to the ball\r\n# *Remember*: Subtract the gripper position from the ball position \r\n\r\n\r\n# TODO: Normalize the direction vector to get its magnitude, a scalar value to later compare to another scalar value, the distance_threshold\r\n\r\n\r\n# TODO: Fill in the while loop to move the gripper toward the ball, keep moving the gripper until the distance is less than the threshold.\r\n# *Remeber*: Utilize the normalized direction vector you just caclulated to compare to the distance_threshold\r\nwhile ____________________ > distance_threshold:\r\n\r\n    # Given: Calculate the action to move the gripper in the direction of the ball.\r\n    action = np.append(direction / direction_normalized * step_size, [1])\r\n\r\n    # TODO: Apply the action to the environment.\r\n\r\n\r\n    # TODO: Update the gripper's position. \r\n    # *Remember*: You have done this before. Get the grippers position from the environment. \r\n\r\n\r\n    # TODO: Update the gripper's direction.\r\n    # *Remember*: You have calculated the direction before. This is the new distance from the gripper to the ball (hence the gripper's position).\r\n\r\n\r\n    #TODO: Normalize the direction vector\r\n    # *Remember*: You have done this before.\r\n\r\n                    \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n	\N	["1. The main loop should continue as long as the distance between the gripper and the ball is greater than the `distance_threshold`.  You need to calculate this distance and use it in your `while` loop condition.  Remember to use the appropriate environment functions to get the necessary positions."]	Fetch Reach	[{"message": "No call to env.step() was found.", "line": 27}, {"message": "Missing call to `env.get_ball_position()`. This function needs to be called somewhere in the code to retrieve the ball position from the environment.", "line": 27}, {"message": "Missing call to `env.get_gripper_position()`. This function needs to be called somewhere in the code to retrieve the gripper position from the environment.", "line": 27}, {"message": "Missing computation of direction. Make sure you define `direction = np.array(None) - np.array(None)`.", "line": 27}, {"message": "Missing computation of direction normalization. Expected np.linalg.norm(None).", "line": 27}, {"message": "The variable used in the while loop condition ('____________________') is not computed using np.linalg.norm(...).", "line": 24}]	2025-04-11 04:14:37.718501	39
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.users (user_id, username, first_name, last_name, email, password, role_id, created_at) FROM stdin;
38	StudentTwo	Student	Two	studenttwo@gmail.com	\\x243262243132244e39745877716257452f35512f67756e2f645158582e67565447563948796a5961584b42624a7645355837555a77467456465a3836	2	2025-02-24 01:52:12.475114
37	StudentOne	Student	Three	studentone@gmail.com	\\x243262243132245969356b7a2e56314655634a6b4b486752366f54564f6a736464584f4b2f525156624c4c7144766d624c6f77382f5a467835397132	2	2025-02-24 01:52:12.475114
55	StudentNine	Student	Nine	studentnine@gmail.com	\\x243262243132246456686148336638772e434f6e304335656f4d527a2e5045667a3846737a6d696c6b3046686a54444f537a65542e46757262766179	1	2025-03-17 21:07:22.670879
56	StudentTen	Student	Ten	studentten@gmail.com	\\x24326224313224466f2f4a6c3437674e6c6d777a324663784e7356394f4978462e33514f33415738506b386c5a4b6d647a72567633386c59614e5957	2	2025-03-17 21:07:50.244923
89	StudentEleven	Student	Eleven	studenteleven@gmail.com	\\x24326224313224777550464a617a4e32636d543431724269317a30762e7878676d5330654757736d70434766316f4c3266314d644747504268505165	2	2025-03-17 21:31:04.928713
91	S2	Student	Two	studenttwonew@gmail.com	\\x2432622431322458466368356c504b736a305769542e78597a2f616f2e31545045734233652e463047423277736e66362e76746e326d39576b2f4d71	2	2025-04-07 06:07:35.136576
50	existinguser	Johnny	Doe	test@example.com	\\x2432622431322463546453332f3133327776567379533364626c6b3575574838684464586355365367627139554d6c576c545041316f784839764847	2	2025-03-02 18:00:16.874951
51	newuser	John	Doe	existing@example.com	\\x24326224313224512e4858574e30324f756c43384970467359456c514f586b496e4268304c44586a6c4e51537a6253437071575868426b46544e5261	2	2025-03-04 04:40:32.110374
70	NewStudentOne	Jasmine	Almedo	jalmedo@gmail.com	\\x243262243132243247317741747a4a69724e472f564575724635613975446e564b70386f756474587933756234394e527569684b5a55474e4c722f75	2	2025-02-24 10:54:13.982985
39	InstructorOne	Instructor	One	instructorone@gmail.com	\\x24326224313224485551657561356236613278764562344d684562344f766b6369743131695750757563477669485a3779533073564e504c6d394169	1	2025-02-24 01:52:12.475114
42	admin	Admin	One	admin@gmail.com	\\x24326224313224506c71566574446747544459366565756134727265654e426f76314636656470474e75706d653446717a2e4c4a333770674f5a684b	3	2025-02-24 01:52:12.475114
40	InstructorTwo	Instructor	Two	instructorfive@gmail.com	\\x243262243132244c6b6f3263422e4e304f7233694f694c307377654f6538715731776a4654516c5967454568734a6d4c696e4e753237675176536969	1	2025-02-24 01:52:12.475114
52	StudentSix	Student	Six	studentsix@gmail.com	\\x24326224313224627538313869676c595247674754376162627974392e65657653725035547147564b50686577693656455861577554524d4c36342e	2	2025-03-17 07:45:56.042584
53	StudentSeven	Student	Seven	studentseven@gmail.com	\\x24326224313224686d4547303976656e767a48384b7578616b706a644f716f4d745130784c434c4d34353355475a5a677864694d5737573451437047	2	2025-03-17 07:50:47.332446
54	StudentEight	Student	Eight	studenteight@gmail.com	\\x24326224313224653076566d525365334c7a704d4b4c714c47316179654f4b4e6d44556744346d4578622e6b5547554744437a794f74702e462f6171	2	2025-03-17 07:55:55.899432
\.


--
-- Name: class_codes_class_code_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.class_codes_class_code_id_seq', 14, true);


--
-- Name: classes_class_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.classes_class_id_seq', 43, true);


--
-- Name: course_subsections_course_subsection_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.course_subsections_course_subsection_id_seq', 22, true);


--
-- Name: courses_course_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.courses_course_id_seq', 38, true);


--
-- Name: enrollment_enrollment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.enrollment_enrollment_id_seq', 14, true);


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

SELECT pg_catalog.setval('public.student_assigned_course_subse_assigned_course_subsection_id_seq', 193, true);


--
-- Name: student_assigned_courses_student_assigned_courses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.student_assigned_courses_student_assigned_courses_id_seq', 48, true);


--
-- Name: student_grades_student_grades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.student_grades_student_grades_id_seq', 42, true);


--
-- Name: user_code_logs_user_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.user_code_logs_user_log_id_seq', 39, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.users_user_id_seq', 91, true);


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

