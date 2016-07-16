-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- This file create PSQL database structure to store information about players, match results and scores.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament

CREATE TABLE players (
	name text , id serial PRIMARY KEY
	);

CREATE TABLE matches (
	match_number serial PRIMARY KEY,
	player_1 integer REFERENCES players(id),
	player_2 integer REFERENCES players(id),
	winner integer, draw integer);

CREATE TABLE players_scores (
	player integer REFERENCES players(id),
	games integer, wins integer, loses integer, draws integer, scores integer);