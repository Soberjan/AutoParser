CREATE TABLE IF NOT EXISTS public.files (
	id serial4 NOT NULL,
	filename text NOT NULL,
	file_data bytea NOT NULL,
	CONSTRAINT files_pk PRIMARY KEY (id)
);