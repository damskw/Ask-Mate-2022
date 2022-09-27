--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.question
    DROP CONSTRAINT IF EXISTS pk_question_id CASCADE,
    DROP CONSTRAINT IF EXISTS fk_author CASCADE, --DELETE AFTER RUN (name changed to fk_author_id for consistency w/ rest of the tables ;))
    DROP CONSTRAINT IF EXISTS fk_author_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.answer
    DROP CONSTRAINT IF EXISTS pk_answer_id CASCADE,
    DROP CONSTRAINT IF EXISTS fk_question_id CASCADE,
    DROP CONSTRAINT IF EXISTS fk_author CASCADE, --DELETE AFTER RUN
    DROP CONSTRAINT IF EXISTS fk_author_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.comment
    DROP CONSTRAINT IF EXISTS pk_comment_id CASCADE,
    DROP CONSTRAINT IF EXISTS comment_to_question_or_answer CASCADE,
    DROP CONSTRAINT IF EXISTS fk_question_id CASCADE,
    DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE,
    DROP CONSTRAINT IF EXISTS fk_author CASCADE, --DELETE AFTER RUN
    DROP CONSTRAINT IF EXISTS fk_author_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.question_tag
    DROP CONSTRAINT IF EXISTS pk_question_tag_id CASCADE,
    DROP CONSTRAINT IF EXISTS unique_question_tag_pair CASCADE,
    DROP CONSTRAINT IF EXISTS fk_question_id CASCADE,
    DROP CONSTRAINT IF EXISTS fk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.tag
    DROP CONSTRAINT IF EXISTS pk_tag_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.user
    DROP CONSTRAINT IF EXISTS pk_user_id CASCADE,
    DROP CONSTRAINT IF EXISTS pk_user CASCADE; --DELETE AFTER RUN
ALTER TABLE IF EXISTS ONLY public.vote
    DROP CONSTRAINT IF EXISTS vote_to_which_post_type CASCADE,
    DROP CONSTRAINT IF EXISTS pk_vote_id CASCADE,
    DROP CONSTRAINT IF EXISTS unique_user_post_pair CASCADE,
    DROP CONSTRAINT IF EXISTS fk_user_id CASCADE,
    DROP CONSTRAINT IF EXISTS fk_question_id CASCADE,
    DROP CONSTRAINT IF EXISTS fk_answer_id CASCADE,
    DROP CONSTRAINT IF EXISTS fk_comment_id CASCADE;
ALTER TABLE IF EXISTS ONLY public.subscribed_tag
    DROP CONSTRAINT IF EXISTS pk_user_tag_id CASCADE,
    DROP CONSTRAINT IF EXISTS unique_user_tag_pair CASCADE;


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
    email varchar(254) NOT NULL,--https://stackoverflow.com/questions/386294/what-is-the-maximum-length-of-a-valid-email-address?_gl=1*sf2yv5*_ga*MTM5NTkzMTAyMS4xNjU2NjA3OTc5*_ga_S812YQPLT2*MTY2NDEyNTY5OS4xMS4xLjE2NjQxMjYwMjQuMC4wLjA.
    password text  NOT NULL,
    name varchar(200)  NOT NULL,
    role varchar(150)  NULL,
    member_since timestamp  NOT NULL,
    avatar varchar(200)  NULL,
    last_log_in timestamp  NOT NULL,
    location varchar(200)  NULL,
    about_me varchar(1000)  NULL,
    reputation int  NOT NULL,
    has_been_deleted boolean NULL, -- if user tries to delete their account, the questions, answers, comments and votes of that user stay, their data is not visible publicly under the posts, their data is exported to a separate field in the db, also their account cannot be looked up and this flag is set to False, if the user confirms to delete the account permanently, the flag is set to True and exported data is deleted, otherwise they have possibility to revive their account.
    exported_user_data text NULL,
    CONSTRAINT pk_user_id PRIMARY KEY (id)
);

DROP TABLE IF EXISTS public.vote;
CREATE TABLE public.vote (
    user_id integer  NOT NULL,
    question_id integer  NULL,
    answer_id integer  NULL,
    comment_id integer  NULL,
    vote_value boolean NOT NULL,
    CONSTRAINT unique_user_post_pair UNIQUE (user_id, question_id, answer_id, comment_id) NOT DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT pk_vote_id PRIMARY KEY (user_id, question_id, answer_id, comment_id)
);

DROP TABLE IF EXISTS public.subscribed_tag;
CREATE TABLE public.subscribed_tag (
    user_id integer NOT NULL,
    tag_id integer NOT NULL,
    CONSTRAINT unique_user_tag_pair UNIQUE (user_id, tag_id) NOT DEFERRABLE INITIALLY IMMEDIATE,
    CONSTRAINT pk_user_tag_id PRIMARY KEY (user_id, tag_id)
);

------------------------------------------  CONSTRAINTS ----------------------------------------

ALTER TABLE ONLY question
    ADD CONSTRAINT fk_author FOREIGN KEY (author_id) REFERENCES public.user(id),
    ADD CONSTRAINT references_answer_id_if_answer_accepted
        CHECK ((has_accepted_answer = TRUE AND accepted_answer_id IS NOT NULL)
                   OR (has_accepted_answer = FALSE AND accepted_answer_id IS NULL)
            );

ALTER TABLE ONLY answer
    ADD CONSTRAINT fk_author_id FOREIGN KEY (author_id) REFERENCES public.user(id),
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id) ON DELETE CASCADE;

ALTER TABLE ONLY comment
    ADD CONSTRAINT comment_to_question_or_answer
        CHECK (
            (question_id IS NOT NULL AND answer_id IS NULL)
                OR (answer_id IS NOT NULL AND question_id IS NULL)
            ),
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES answer(id),
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id),
    ADD CONSTRAINT fk_author_id FOREIGN KEY (author_id) REFERENCES public.user(id);

ALTER TABLE ONLY question_tag
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES question(id),
    ADD CONSTRAINT fk_tag_id FOREIGN KEY (tag_id) REFERENCES tag(id);

ALTER TABLE ONLY vote
    ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES public.user(id),
    ADD CONSTRAINT fk_question_id FOREIGN KEY (question_id) REFERENCES public.question(id),
    ADD CONSTRAINT fk_answer_id FOREIGN KEY (answer_id) REFERENCES public.answer(id),
    ADD CONSTRAINT fk_comment_id FOREIGN KEY (comment_id) REFERENCES public.comment(id),
    ADD CONSTRAINT vote_to_which_post_type
        CHECK (
            (question_id IS NOT NULL AND answer_id IS NULL AND comment_id IS NULL)
                OR (answer_id IS NOT NULL AND question_id IS NULL AND comment_id IS NULL)
                OR (comment_id IS NOT NULL AND question_id IS NULL AND answer_id IS NULL)
            );

