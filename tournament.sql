-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create database tournament;

\c tournament

create table players (
	name text , id serial primary key
	);

create table players_scores (
	player integer REFERENCES players(id),
	games integer, wins integer, loses integer, draws integer, scores integer);

create table tournament_1 (
	player_1 integer REFERENCES players(id),
	player_2 integer REFERENCES players(id),
	winner integer, draw integer);



