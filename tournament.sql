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
	name text primary key, id serial
	);

create table players_scores (
	player text REFERENCES players(name),
	games integer, wins integer, loses integer, draws integer, scores integer);

create table tournament_1 (
	player_1 text REFERENCES players(name),
	player_2 text REFERENCES players(name),
	winner_1 integer, winner_2 integer, draw integer);



