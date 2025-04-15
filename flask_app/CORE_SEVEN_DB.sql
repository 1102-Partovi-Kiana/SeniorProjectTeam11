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
15	44	lw7oWCzb
\.


--
-- Data for Name: classes; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.classes (class_id, class_course_code, class_section_number, user_id, created_at, expired_at) FROM stdin;
44	CS101	1001	93	2025-04-14	2025-04-30
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
242	f	1.11	94
243	f	1.12	94
244	f	1.13	94
245	f	1.14	94
246	f	1.15	94
247	f	1.16	94
248	f	1.17	94
249	f	1.18	94
250	f	1.19	94
251	f	1.21	94
252	f	1.9	94
253	f	1.91	94
254	f	1.11	95
255	f	1.12	95
256	f	1.13	95
257	f	1.14	95
258	f	1.15	95
259	f	1.16	95
260	f	1.17	95
261	f	1.18	95
262	f	1.19	95
263	f	1.21	95
264	f	1.9	95
265	f	1.91	95
266	f	1.11	96
267	f	1.12	96
268	f	1.13	96
269	f	1.14	96
270	f	1.15	96
271	f	1.16	96
272	f	1.17	96
273	f	1.18	96
274	f	1.19	96
275	f	1.21	96
276	f	1.9	96
277	f	1.91	96
278	f	1.11	97
279	f	1.12	97
280	f	1.13	97
281	f	1.14	97
282	f	1.15	97
283	f	1.16	97
284	f	1.17	97
285	f	1.18	97
286	f	1.19	97
287	f	1.21	97
288	f	1.9	97
289	f	1.91	97
290	f	1.11	98
291	f	1.12	98
292	f	1.13	98
293	f	1.14	98
294	f	1.15	98
295	f	1.16	98
296	f	1.17	98
297	f	1.18	98
298	f	1.19	98
299	f	1.21	98
300	f	1.9	98
301	f	1.91	98
302	f	1.11	99
303	f	1.12	99
304	f	1.13	99
305	f	1.14	99
306	f	1.15	99
307	f	1.16	99
308	f	1.17	99
309	f	1.18	99
310	f	1.19	99
311	f	1.21	99
312	f	1.9	99
313	f	1.91	99
314	f	1.11	100
315	f	1.12	100
316	f	1.13	100
317	f	1.14	100
318	f	1.15	100
319	f	1.16	100
320	f	1.17	100
321	f	1.18	100
322	f	1.19	100
323	f	1.21	100
324	f	1.9	100
325	f	1.91	100
326	f	1.11	101
327	f	1.12	101
328	f	1.13	101
329	f	1.14	101
330	f	1.15	101
331	f	1.16	101
332	f	1.17	101
333	f	1.18	101
334	f	1.19	101
335	f	1.21	101
336	f	1.9	101
337	f	1.91	101
338	f	1.11	102
339	f	1.12	102
340	f	1.13	102
341	f	1.14	102
342	f	1.15	102
343	f	1.16	102
344	f	1.17	102
345	f	1.18	102
346	f	1.19	102
347	f	1.21	102
348	f	1.9	102
349	f	1.91	102
350	f	1.11	103
351	f	1.12	103
352	f	1.13	103
353	f	1.14	103
354	f	1.15	103
355	f	1.16	103
356	f	1.17	103
357	f	1.18	103
358	f	1.19	103
359	f	1.21	103
360	f	1.9	103
361	f	1.91	103
362	f	1.11	104
363	f	1.12	104
364	f	1.13	104
365	f	1.14	104
366	f	1.15	104
367	f	1.16	104
368	f	1.17	104
369	f	1.18	104
370	f	1.19	104
371	f	1.21	104
372	f	1.9	104
373	f	1.91	104
374	f	1.11	105
375	f	1.12	105
376	f	1.13	105
377	f	1.14	105
378	f	1.15	105
379	f	1.16	105
380	f	1.17	105
381	f	1.18	105
382	f	1.19	105
383	f	1.21	105
384	f	1.9	105
385	f	1.91	105
386	f	1.11	106
387	f	1.12	106
388	f	1.13	106
389	f	1.14	106
390	f	1.15	106
391	f	1.16	106
392	f	1.17	106
393	f	1.18	106
394	f	1.19	106
395	f	1.21	106
396	f	1.9	106
397	f	1.91	106
398	f	1.11	107
399	f	1.12	107
400	f	1.13	107
401	f	1.14	107
402	f	1.15	107
403	f	1.16	107
404	f	1.17	107
405	f	1.18	107
406	f	1.19	107
407	f	1.21	107
408	f	1.9	107
409	f	1.91	107
410	f	1.11	108
411	f	1.12	108
412	f	1.13	108
413	f	1.14	108
414	f	1.15	108
415	f	1.16	108
416	f	1.17	108
417	f	1.18	108
418	f	1.19	108
419	f	1.21	108
420	f	1.9	108
421	f	1.91	108
422	f	1.11	109
423	f	1.12	109
424	f	1.13	109
425	f	1.14	109
426	f	1.15	109
427	f	1.16	109
428	f	1.17	109
429	f	1.18	109
430	f	1.19	109
431	f	1.21	109
432	f	1.9	109
433	f	1.91	109
434	f	1.11	110
435	f	1.12	110
436	f	1.13	110
437	f	1.14	110
438	f	1.15	110
439	f	1.16	110
440	f	1.17	110
441	f	1.18	110
442	f	1.19	110
443	f	1.21	110
444	f	1.9	110
445	f	1.91	110
446	f	1.11	111
447	f	1.12	111
448	f	1.13	111
449	f	1.14	111
450	f	1.15	111
451	f	1.16	111
452	f	1.17	111
453	f	1.18	111
454	f	1.19	111
455	f	1.21	111
456	f	1.9	111
457	f	1.91	111
458	f	1.11	112
459	f	1.12	112
460	f	1.13	112
461	f	1.14	112
462	f	1.15	112
463	f	1.16	112
464	f	1.17	112
465	f	1.18	112
466	f	1.19	112
467	f	1.21	112
468	f	1.9	112
469	f	1.91	112
470	f	1.11	113
471	f	1.12	113
472	f	1.13	113
473	f	1.14	113
474	f	1.15	113
475	f	1.16	113
476	f	1.17	113
477	f	1.18	113
478	f	1.19	113
479	f	1.21	113
480	f	1.9	113
481	f	1.91	113
482	f	1.11	114
483	f	1.12	114
484	f	1.13	114
485	f	1.14	114
486	f	1.15	114
487	f	1.16	114
488	f	1.17	114
489	f	1.18	114
490	f	1.19	114
491	f	1.21	114
492	f	1.9	114
493	f	1.91	114
494	f	1.11	115
495	f	1.12	115
496	f	1.13	115
497	f	1.14	115
498	f	1.15	115
499	f	1.16	115
500	f	1.17	115
501	f	1.18	115
502	f	1.19	115
503	f	1.21	115
504	f	1.9	115
505	f	1.91	115
506	f	1.11	116
507	f	1.12	116
508	f	1.13	116
509	f	1.14	116
510	f	1.15	116
511	f	1.16	116
512	f	1.17	116
513	f	1.18	116
514	f	1.19	116
515	f	1.21	116
516	f	1.9	116
517	f	1.91	116
518	f	1.11	117
519	f	1.12	117
520	f	1.13	117
521	f	1.14	117
522	f	1.15	117
523	f	1.16	117
524	f	1.17	117
525	f	1.18	117
526	f	1.19	117
527	f	1.21	117
528	f	1.9	117
529	f	1.91	117
530	f	1.11	118
531	f	1.12	118
532	f	1.13	118
533	f	1.14	118
534	f	1.15	118
535	f	1.16	118
536	f	1.17	118
537	f	1.18	118
538	f	1.19	118
539	f	1.21	118
540	f	1.9	118
541	f	1.91	118
542	f	1.11	119
543	f	1.12	119
544	f	1.13	119
545	f	1.14	119
546	f	1.15	119
547	f	1.16	119
548	f	1.17	119
549	f	1.18	119
550	f	1.19	119
551	f	1.21	119
552	f	1.9	119
553	f	1.91	119
554	f	1.11	120
555	f	1.12	120
556	f	1.13	120
557	f	1.14	120
558	f	1.15	120
559	f	1.16	120
560	f	1.17	120
561	f	1.18	120
562	f	1.19	120
563	f	1.21	120
564	f	1.9	120
565	f	1.91	120
566	f	1.11	121
567	f	1.12	121
568	f	1.13	121
569	f	1.14	121
570	f	1.15	121
571	f	1.16	121
572	f	1.17	121
573	f	1.18	121
574	f	1.19	121
575	f	1.21	121
576	f	1.9	121
577	f	1.91	121
578	f	1.11	122
579	f	1.12	122
580	f	1.13	122
581	f	1.14	122
582	f	1.15	122
583	f	1.16	122
584	f	1.17	122
585	f	1.18	122
586	f	1.19	122
587	f	1.21	122
588	f	1.9	122
589	f	1.91	122
\.


--
-- Data for Name: student_assigned_courses; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.student_assigned_courses (student_assigned_courses_id, course_id, user_id) FROM stdin;
93	21	94
94	22	94
95	23	94
96	24	94
97	25	94
98	27	94
99	30	94
100	31	94
101	32	94
102	33	94
103	37	94
104	21	95
105	22	95
106	23	95
107	24	95
108	25	95
109	27	95
110	30	95
111	31	95
112	32	95
113	33	95
114	37	95
115	21	96
116	22	96
117	23	96
118	24	96
119	25	96
120	27	96
121	30	96
122	31	96
123	32	96
124	33	96
125	37	96
126	21	97
127	22	97
128	23	97
129	24	97
130	25	97
131	27	97
132	30	97
133	31	97
134	32	97
135	33	97
136	37	97
137	21	98
138	22	98
139	23	98
140	24	98
141	25	98
142	27	98
143	30	98
144	31	98
145	32	98
146	33	98
147	37	98
148	21	99
149	22	99
150	23	99
151	24	99
152	25	99
153	27	99
154	30	99
155	31	99
156	32	99
157	33	99
158	37	99
159	21	100
160	22	100
161	23	100
162	24	100
163	25	100
164	27	100
165	30	100
166	31	100
167	32	100
168	33	100
169	37	100
170	21	101
171	22	101
172	23	101
173	24	101
174	25	101
175	27	101
176	30	101
177	31	101
178	32	101
179	33	101
180	37	101
181	21	102
182	22	102
183	23	102
184	24	102
185	25	102
186	27	102
187	30	102
188	31	102
189	32	102
190	33	102
191	37	102
192	21	103
193	22	103
194	23	103
195	24	103
196	25	103
197	27	103
198	30	103
199	31	103
200	32	103
201	33	103
202	37	103
203	21	104
204	22	104
205	23	104
206	24	104
207	25	104
208	27	104
209	30	104
210	31	104
211	32	104
212	33	104
213	37	104
214	21	105
215	22	105
216	23	105
217	24	105
218	25	105
219	27	105
220	30	105
221	31	105
222	32	105
223	33	105
224	37	105
225	21	106
226	22	106
227	23	106
228	24	106
229	25	106
230	27	106
231	30	106
232	31	106
233	32	106
234	33	106
235	37	106
236	21	107
237	22	107
238	23	107
239	24	107
240	25	107
241	27	107
242	30	107
243	31	107
244	32	107
245	33	107
246	37	107
247	21	108
248	22	108
249	23	108
250	24	108
251	25	108
252	27	108
253	30	108
254	31	108
255	32	108
256	33	108
257	37	108
258	21	109
259	22	109
260	23	109
261	24	109
262	25	109
263	27	109
264	30	109
265	31	109
266	32	109
267	33	109
268	37	109
269	21	110
270	22	110
271	23	110
272	24	110
273	25	110
274	27	110
275	30	110
276	31	110
277	32	110
278	33	110
279	37	110
280	21	111
281	22	111
282	23	111
283	24	111
284	25	111
285	27	111
286	30	111
287	31	111
288	32	111
289	33	111
290	37	111
291	21	112
292	22	112
293	23	112
294	24	112
295	25	112
296	27	112
297	30	112
298	31	112
299	32	112
300	33	112
301	37	112
302	21	113
303	22	113
304	23	113
305	24	113
306	25	113
307	27	113
308	30	113
309	31	113
310	32	113
311	33	113
312	37	113
313	21	114
314	22	114
315	23	114
316	24	114
317	25	114
318	27	114
319	30	114
320	31	114
321	32	114
322	33	114
323	37	114
324	21	115
325	22	115
326	23	115
327	24	115
328	25	115
329	27	115
330	30	115
331	31	115
332	32	115
333	33	115
334	37	115
335	21	116
336	22	116
337	23	116
338	24	116
339	25	116
340	27	116
341	30	116
342	31	116
343	32	116
344	33	116
345	37	116
346	21	117
347	22	117
348	23	117
349	24	117
350	25	117
351	27	117
352	30	117
353	31	117
354	32	117
355	33	117
356	37	117
357	21	118
358	22	118
359	23	118
360	24	118
361	25	118
362	27	118
363	30	118
364	31	118
365	32	118
366	33	118
367	37	118
368	21	119
369	22	119
370	23	119
371	24	119
372	25	119
373	27	119
374	30	119
375	31	119
376	32	119
377	33	119
378	37	119
379	21	120
380	22	120
381	23	120
382	24	120
383	25	120
384	27	120
385	30	120
386	31	120
387	32	120
388	33	120
389	37	120
390	21	121
391	22	121
392	23	121
393	24	121
394	25	121
395	27	121
396	30	121
397	31	121
398	32	121
399	33	121
400	37	121
401	21	122
402	22	122
403	23	122
404	24	122
405	25	122
406	27	122
407	30	122
408	31	122
409	32	122
410	33	122
411	37	122
\.


--
-- Data for Name: student_grades; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.student_grades (student_grades_id, student_id, percentage_grade, course_subsection_id, created_at) FROM stdin;
\.


--
-- Data for Name: user_code_logs; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.user_code_logs (user_log_id, code, error, hints, page_context, static_issues, created_at, user_id) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: testuser
--

COPY public.users (user_id, username, first_name, last_name, email, password, role_id, created_at) FROM stdin;
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
114	DemoTwentyOne	Demo	TwentyOne	demotwentyone@gmail.com	\\x24326224313224662e3864516b69635239526b72793572646648776b6574797662566a506f4c7752752e3266374b50723077487a6333544c532f6375	2	2025-04-14 01:38:32.089689
115	DemoTwentyTwo	Demo	TwentyTwo	demotwentytwo@gmail.com	\\x2432622431322454446b4a42577a4c7337715a634a44564452654a492e41635a6f49747978726b4b7461632e554d4c64456952554e46664472563175	2	2025-04-14 01:38:32.089689
116	DemoTwentyThree	Demo	TwentyThree	demotwentythree@gmail.com	\\x2432622431322445654e632f51726e57343676504b7078464b4a42562e4a626c39387253435a483539382e647063557077394c4262594731495a6c53	2	2025-04-14 01:38:32.089689
117	DemoTwentyFour	Demo	TwentyFour	demotwentyfour@gmail.com	\\x243262243132244e454941314c386962337373496247716779305a4c4f384e356138546d6a4d3371643178446f4e486876586d65487633316e42664b	2	2025-04-14 01:38:32.089689
118	DemoTwentyFive	Demo	TwentyFive	demotwentyfive@gmail.com	\\x243262243132244d2f58496f597944496a65542f6549474f2e2e7035754c7344344a66566957747044634d6d64533646314e7a4d724a634f586d7747	2	2025-04-14 01:38:32.089689
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

SELECT pg_catalog.setval('public.classes_class_id_seq', 44, true);


--
-- Name: course_subsections_course_subsection_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.course_subsections_course_subsection_id_seq', 23, true);


--
-- Name: courses_course_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.courses_course_id_seq', 38, true);


--
-- Name: enrollment_enrollment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.enrollment_enrollment_id_seq', 47, true);


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

SELECT pg_catalog.setval('public.student_assigned_course_subse_assigned_course_subsection_id_seq', 589, true);


--
-- Name: student_assigned_courses_student_assigned_courses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.student_assigned_courses_student_assigned_courses_id_seq', 411, true);


--
-- Name: student_grades_student_grades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.student_grades_student_grades_id_seq', 52, true);


--
-- Name: user_code_logs_user_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.user_code_logs_user_log_id_seq', 78, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: testuser
--

SELECT pg_catalog.setval('public.users_user_id_seq', 123, true);


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

