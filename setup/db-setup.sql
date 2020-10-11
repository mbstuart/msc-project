--
-- PostgreSQL database dump
--

-- Dumped from database version 12.3
-- Dumped by pg_dump version 12.3

-- Started on 2020-10-11 13:03:01

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
-- TOC entry 9 (class 2615 OID 59986)
-- Name: DE; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA "DE";


ALTER SCHEMA "DE" OWNER TO postgres;

--
-- TOC entry 2860 (class 0 OID 0)
-- Dependencies: 9
-- Name: SCHEMA "DE"; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA "DE" IS 'Document extraction';


--
-- TOC entry 8 (class 2615 OID 16394)
-- Name: TE; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA "TE";


ALTER SCHEMA "TE" OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 207 (class 1259 OID 59996)
-- Name: ArticleLoad; Type: TABLE; Schema: DE; Owner: postgres
--

CREATE TABLE "DE"."ArticleLoad" (
    "Id" uuid NOT NULL,
    "StartTime" timestamp with time zone NOT NULL,
    "Active" boolean DEFAULT false NOT NULL
);


ALTER TABLE "DE"."ArticleLoad" OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 59988)
-- Name: Articles; Type: TABLE; Schema: DE; Owner: postgres
--

CREATE TABLE "DE"."Articles" (
    "PublishDate" timestamp with time zone NOT NULL,
    "Id" text NOT NULL,
    "Body" text NOT NULL,
    "Title" text NOT NULL,
    "ArticleLoadId" uuid NOT NULL,
    "SourceTags" text[]
);


ALTER TABLE "DE"."Articles" OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 278845)
-- Name: ProcessedArticles; Type: TABLE; Schema: TE; Owner: postgres
--

CREATE TABLE "TE"."ProcessedArticles" (
    "Id" text NOT NULL,
    "ArticleLoadId" uuid NOT NULL,
    "Words" text[] NOT NULL,
    "TitleWords" text[]
);


ALTER TABLE "TE"."ProcessedArticles" OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 372826)
-- Name: ThemeArticleMapping; Type: TABLE; Schema: TE; Owner: postgres
--

CREATE TABLE "TE"."ThemeArticleMapping" (
    "ThemeId" bigint NOT NULL,
    "ArticleId" text NOT NULL,
    "ArticleLoadId" uuid NOT NULL
);


ALTER TABLE "TE"."ThemeArticleMapping" OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 372805)
-- Name: Themes; Type: TABLE; Schema: TE; Owner: postgres
--

CREATE TABLE "TE"."Themes" (
    "ThemeId" integer NOT NULL,
    "ArticleLoadId" uuid NOT NULL,
    "ThemeName" text NOT NULL,
    "ThemeWords" text[]
);


ALTER TABLE "TE"."Themes" OWNER TO postgres;

--
-- TOC entry 2716 (class 2606 OID 60000)
-- Name: ArticleLoad ArticleLoad_pkey; Type: CONSTRAINT; Schema: DE; Owner: postgres
--

ALTER TABLE ONLY "DE"."ArticleLoad"
    ADD CONSTRAINT "ArticleLoad_pkey" PRIMARY KEY ("Id");


--
-- TOC entry 2714 (class 2606 OID 60002)
-- Name: Articles pk_Articles; Type: CONSTRAINT; Schema: DE; Owner: postgres
--

ALTER TABLE ONLY "DE"."Articles"
    ADD CONSTRAINT "pk_Articles" PRIMARY KEY ("Id", "ArticleLoadId");


--
-- TOC entry 2719 (class 2606 OID 278852)
-- Name: ProcessedArticles ProcessedArticles_pkey; Type: CONSTRAINT; Schema: TE; Owner: postgres
--

ALTER TABLE ONLY "TE"."ProcessedArticles"
    ADD CONSTRAINT "ProcessedArticles_pkey" PRIMARY KEY ("Id", "ArticleLoadId");


--
-- TOC entry 2724 (class 2606 OID 372833)
-- Name: ThemeArticleMapping ThemeArticleMapping_pkey; Type: CONSTRAINT; Schema: TE; Owner: postgres
--

ALTER TABLE ONLY "TE"."ThemeArticleMapping"
    ADD CONSTRAINT "ThemeArticleMapping_pkey" PRIMARY KEY ("ThemeId", "ArticleId", "ArticleLoadId");


--
-- TOC entry 2721 (class 2606 OID 372812)
-- Name: Themes Themes_pkey; Type: CONSTRAINT; Schema: TE; Owner: postgres
--

ALTER TABLE ONLY "TE"."Themes"
    ADD CONSTRAINT "Themes_pkey" PRIMARY KEY ("ThemeId", "ArticleLoadId");


--
-- TOC entry 2712 (class 1259 OID 76018)
-- Name: idx_Articles; Type: INDEX; Schema: DE; Owner: postgres
--

CREATE INDEX "idx_Articles" ON "DE"."Articles" USING btree ("ArticleLoadId", "PublishDate" DESC NULLS LAST);

ALTER TABLE "DE"."Articles" CLUSTER ON "idx_Articles";


--
-- TOC entry 2717 (class 1259 OID 2819347)
-- Name: ProcessedArticles_IDX; Type: INDEX; Schema: TE; Owner: postgres
--

CREATE INDEX "ProcessedArticles_IDX" ON "TE"."ProcessedArticles" USING btree ("ArticleLoadId", "Id");

ALTER TABLE "TE"."ProcessedArticles" CLUSTER ON "ProcessedArticles_IDX";


--
-- TOC entry 2722 (class 1259 OID 2819346)
-- Name: TAM_idx; Type: INDEX; Schema: TE; Owner: postgres
--

CREATE INDEX "TAM_idx" ON "TE"."ThemeArticleMapping" USING btree ("ArticleLoadId");

ALTER TABLE "TE"."ThemeArticleMapping" CLUSTER ON "TAM_idx";


--
-- TOC entry 2725 (class 2606 OID 60003)
-- Name: Articles fk_ArticleLoadId; Type: FK CONSTRAINT; Schema: DE; Owner: postgres
--

ALTER TABLE ONLY "DE"."Articles"
    ADD CONSTRAINT "fk_ArticleLoadId" FOREIGN KEY ("ArticleLoadId") REFERENCES "DE"."ArticleLoad"("Id") NOT VALID;


--
-- TOC entry 2726 (class 2606 OID 278853)
-- Name: ProcessedArticles fk_ProcessedArticles; Type: FK CONSTRAINT; Schema: TE; Owner: postgres
--

ALTER TABLE ONLY "TE"."ProcessedArticles"
    ADD CONSTRAINT "fk_ProcessedArticles" FOREIGN KEY ("Id", "ArticleLoadId") REFERENCES "DE"."Articles"("Id", "ArticleLoadId");


--
-- TOC entry 2728 (class 2606 OID 372839)
-- Name: ThemeArticleMapping fk_ThemeArticle_Article; Type: FK CONSTRAINT; Schema: TE; Owner: postgres
--

ALTER TABLE ONLY "TE"."ThemeArticleMapping"
    ADD CONSTRAINT "fk_ThemeArticle_Article" FOREIGN KEY ("ArticleId", "ArticleLoadId") REFERENCES "TE"."ProcessedArticles"("Id", "ArticleLoadId");


--
-- TOC entry 2727 (class 2606 OID 372834)
-- Name: ThemeArticleMapping fk_ThemeArticle_Theme; Type: FK CONSTRAINT; Schema: TE; Owner: postgres
--

ALTER TABLE ONLY "TE"."ThemeArticleMapping"
    ADD CONSTRAINT "fk_ThemeArticle_Theme" FOREIGN KEY ("ThemeId", "ArticleLoadId") REFERENCES "TE"."Themes"("ThemeId", "ArticleLoadId");


--
-- TOC entry 2861 (class 0 OID 0)
-- Dependencies: 9
-- Name: SCHEMA "DE"; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA "DE" TO "theme-extractor";


--
-- TOC entry 2862 (class 0 OID 0)
-- Dependencies: 8
-- Name: SCHEMA "TE"; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA "TE" TO "theme-extractor";


--
-- TOC entry 2863 (class 0 OID 0)
-- Dependencies: 207
-- Name: TABLE "ArticleLoad"; Type: ACL; Schema: DE; Owner: postgres
--

GRANT ALL ON TABLE "DE"."ArticleLoad" TO "theme-extractor";


--
-- TOC entry 2864 (class 0 OID 0)
-- Dependencies: 206
-- Name: TABLE "Articles"; Type: ACL; Schema: DE; Owner: postgres
--

GRANT ALL ON TABLE "DE"."Articles" TO "theme-extractor" WITH GRANT OPTION;


--
-- TOC entry 2865 (class 0 OID 0)
-- Dependencies: 208
-- Name: TABLE "ProcessedArticles"; Type: ACL; Schema: TE; Owner: postgres
--

GRANT ALL ON TABLE "TE"."ProcessedArticles" TO "theme-extractor";


--
-- TOC entry 2866 (class 0 OID 0)
-- Dependencies: 210
-- Name: TABLE "ThemeArticleMapping"; Type: ACL; Schema: TE; Owner: postgres
--

GRANT ALL ON TABLE "TE"."ThemeArticleMapping" TO "theme-extractor";


--
-- TOC entry 2867 (class 0 OID 0)
-- Dependencies: 209
-- Name: TABLE "Themes"; Type: ACL; Schema: TE; Owner: postgres
--

GRANT ALL ON TABLE "TE"."Themes" TO "theme-extractor";


--
-- TOC entry 1712 (class 826 OID 59987)
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: DE; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA "DE" REVOKE ALL ON TABLES  FROM postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA "DE" GRANT ALL ON TABLES  TO "theme-extractor";


--
-- TOC entry 1711 (class 826 OID 16404)
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: -; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres GRANT ALL ON TABLES  TO "theme-extractor";


-- Completed on 2020-10-11 13:03:02

--
-- PostgreSQL database dump complete
--

