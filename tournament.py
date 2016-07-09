#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tournament_1;')
    conn.commit()
    conn.close()
    return

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
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
    QUERY = 'insert into players values (%s);'
    data = (name,)
    cursor.execute(QUERY, data)
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
    cursor.execute('SELECT id, name, wins, games FROM players LEFT JOIN players_scores ON players.name = players_scores.player order by wins;')
    return cursor.fetchall()



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    cursor = conn.cursor()
    QUERY = ('INSERT INTO tournament_1 (player_1, player_2, winner_1) values (%s, %s, %s);' )
    data = (winner, loser, winner_1)
    cursor.execute(QUERY, data)
    conn.commit()
    conn.close()
    return
 
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


