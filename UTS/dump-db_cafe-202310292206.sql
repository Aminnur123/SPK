PGDMP                  	    {            db_cafe    16.0    16.0     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    16398    db_cafe    DATABASE     ~   CREATE DATABASE db_cafe WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'English_Indonesia.1252';
    DROP DATABASE db_cafe;
                postgres    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
                pg_database_owner    false            �           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                   pg_database_owner    false    4            �            1259    16399    tb_cafe    TABLE     �   CREATE TABLE public.tb_cafe (
    id_cafe character varying NOT NULL,
    rating_minuman integer,
    harga character varying,
    kualitas_pelayanan integer,
    suasana character varying,
    rasa character varying
);
    DROP TABLE public.tb_cafe;
       public         heap    postgres    false    4            �          0    16399    tb_cafe 
   TABLE DATA           d   COPY public.tb_cafe (id_cafe, rating_minuman, harga, kualitas_pelayanan, suasana, rasa) FROM stdin;
    public          postgres    false    215          �      x������ � �     