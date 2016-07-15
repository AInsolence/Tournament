#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
# master branch

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tournament_1;')
    cursor.execute('UPDATE players_scores SET games = 0, wins = 0, loses = 0, draws = 0, scores = 0;')
    conn.commit()
    conn.close()
    return

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM players_scores;')
    cursor.execute('DELETE FROM players;')
    conn.commit()
    conn.close()
    return

def countPlayers():
    """Returns the number of players currently registered."""
    cursor = connect().cursor()
    cursor.execute('SELECT count(id) FROM players;')
    res = cursor.fetchone()
    return res[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    QUERY = 'INSERT INTO players values (%s) RETURNING id;'
    data = (name,)
    cursor.execute(QUERY, data)
    conn.commit()
    id_of_new_row = (cursor.fetchone()[0],)
    QUERY2 = ('insert into players_scores values (%s, 0, 0, 0, 0, 0);') 
    ### inserting new player(id) with clean statistic to players_scores table ###
    cursor.execute(QUERY2, id_of_new_row)
    conn.commit()
    conn.close()
    return


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, wins, games FROM players LEFT JOIN players_scores ON players.id = players_scores.player order by wins desc;')
    return cursor.fetchall()



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    QUERY = 'INSERT INTO tournament_1 (player_1, player_2, winner, draw) values (%s, %s, %s, 0);'
    QUERY2 = 'UPDATE players_scores SET games = games + 1, wins = wins + 1 where player = %s;'
    QUERY3 = 'UPDATE players_scores SET games = games + 1, loses = loses + 1 where player = %s;'
    data = (winner, loser, winner)
    data2 = [(winner,), (loser,)]
    cursor.execute(QUERY, data)
    cursor.execute(QUERY2, data2[0])
    cursor.execute(QUERY3, data2[1])
    conn.commit()
    conn.close()
    return "Match is record!"
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    players = playerStandings()
    pairings = []
    n = 0
    if len(players) % 2 == 0:
        while n != len(players):
            pair = (players[n][0], players[n][1], players[n + 1][0], players[n + 1][1])
            pairings.append(pair)
            n += 2
    else:
        while n != len(players) - 1:
            pair = (players[n][0], players[n][1], players[n + 1][0], players[n + 1][1])
            pairings.append(pair)
            n += 2
        single_player = (players[-1][0], players[-1][1], 'id', 'buy win in this tour')
        pairings.append(single_player)

    return pairings