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
	winner integer REFERENCES players(id),
	loser integer REFERENCES players(id), draw boolean, 
	match_number serial PRIMARY KEY);

CREATE VIEW players_scores AS SELECT id, (SELECT COUNT(winner) AS win FROM matches WHERE winner = id) AS wins, (SELECT COUNT(loser) AS lose FROM matches WHERE loser = id) AS loses, (SELECT COUNT(*) AS games FROM matches WHERE winner = id OR loser = id) AS games FROM players; 




