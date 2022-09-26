--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.question DROP CONSTRAINT IF EXISTS pk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS pk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS pk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS pk_question_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_question_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.tag DROP CONSTRAINT IF EXISTS pk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.users DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.user DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;


DROP TYPE IF EXISTS user_role CASCADE;
-- CREATE TYPE user_role AS ENUM ( 'classifier', 'moderator', 'insighter' );


DROP TABLE IF EXISTS public.question;
CREATE TABLE question (
    id serial  NOT NULL,
    author_id integer  NOT NULL,
    author_name varchar(200)  NOT NULL,
    submission_time timestamp without time zone  NOT NULL,
    view_number bigint  NOT NULL,
    vote_number int  NOT NULL,
    title varchar(300)  NOT NULL,
    message varchar(4000)  NOT NULL,
    image text  NULL,
    has_accepted_answer boolean  NOT NULL DEFAULT FALSE,
    accepted_answer_id integer  NULL,
    CONSTRAINT pk_question_id PRIMARY KEY (id)
);

DROP TABLE IF EXISTS public.answer;
CREATE TABLE answer (
    id serial  NOT NULL,
    author_id integer  NOT NULL,
    author_name varchar(200) NOT NULL,
    submission_time timestamp without time zone  NOT NULL,
    vote_number integer  NOT NULL,
    question_id integer  NOT NULL,
    message text  NOT NULL,
    image text  NULL,
    is_accepted boolean NOT NULL DEFAULT FALSE,
    CONSTRAINT pk_answer_id PRIMARY KEY (id)
);

DROP TABLE IF EXISTS public.comment;
CREATE TABLE comment (
    id serial  NOT NULL,
    author_id integer  NOT NULL,
    author_name varchar(200) NOT NULL,
    question_id integer  NULL,
    answer_id integer  NULL,
    message text  NOT NULL,
    submission_time timestamp without time zone  NOT NULL,
    edited_count integer  NOT NULL,
    CONSTRAINT pk_comment_id PRIMARY KEY (id)
);


DROP TABLE IF EXISTS public.question_tag;
CREATE TABLE question_tag (
    question_id integer  NOT NULL,
    tag_id integer  NOT NULL,
    CONSTRAINT unique_question_tag_pair UNIQUE (question_id, tag_id) NOT DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT pk_question_tag_id PRIMARY KEY (question_id, tag_id)
);

DROP TABLE IF EXISTS public.tag;
CREATE TABLE tag (
    id serial  NOT NULL,
    name text  NOT NULL,
    CONSTRAINT pk_tag_id PRIMARY KEY (id)
);

DROP TABLE IF EXISTS public.user;
CREATE TABLE public.user (
    id serial  NOT NULL,
    email varchar(254),--https://stackoverflow.com/questions/386294/what-is-the-maximum-length-of-a-valid-email-address?_gl=1*sf2yv5*_ga*MTM5NTkzMTAyMS4xNjU2NjA3OTc5*_ga_S812YQPLT2*MTY2NDEyNTY5OS4xMS4xLjE2NjQxMjYwMjQuMC4wLjA.
    password text  NOT NULL,
    name varchar(200)  NOT NULL,
    role varchar(150)  NULL,
    member_since timestamp  NOT NULL,
    avatar varchar(200)  NULL,
    last_log_in timestamp  NOT NULL,
    location varchar(200)  NULL,
    about_me varchar(1000)  NULL,
    reputation int  NOT NULL,
    CONSTRAINT pk_user PRIMARY KEY (id)
);


ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_author FOREIGN KEY (author_id) REFERENCES public.user(id),
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY comment
    ADD CONSTRAINT fk_author FOREIGN KEY (author_id) REFERENCES public.user(id);

ALTER TABLE ONLY question
    ADD CONSTRAINT fk_author FOREIGN KEY (author_id) REFERENCES public.user(id),
    ADD CONSTRAINT references_answer_id_if_answer_accepted
        CHECK ((has_accepted_answer = TRUE AND accepted_answer_id IS NOT NULL)
                   OR (has_accepted_answer = FALSE AND accepted_answer_id IS NULL));

ALTER TABLE ONLY comment
    ADD CONSTRAINT comment_to_question_or_answer CHECK ((question_id IS NOT NULL AND answer_id IS NULL)
                                                            OR (answer_id IS NOT NULL AND question_id IS NULL)),
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id),
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id),
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id);
