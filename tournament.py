#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
# master branch
# Python module to manage tournament database.
# Use PosrgreSQL DOCUMENTATION ## https://www.postgresql.org/docs/9.3/static/index.html ##
# Use psycopg2 module to work with Postgre SQL. DOCUMENTATION ## http://initd.org/psycopg/docs/usage.html ##

import psycopg2


def connect(database_name="tournament"):
    """Connect to tournament database"""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("Unfortunately its impossible to connect to tournament database.")



def deleteMatches():
    """Remove all the match records from the database."""
    db, cursor = connect()
    cursor.execute('TRUNCATE matches CASCADE;')
    db.commit()
    db.close()
    return

def deletePlayers():
    """Remove all the player records from the database."""
    db, cursor = connect()
    cursor.execute('TRUNCATE players CASCADE;')
    db.commit()
    db.close()
    return

def countPlayers():
    """Returns the number of players currently registered."""
    db, cursor = connect()
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
    db, cursor = connect()
    QUERY = 'INSERT INTO players VALUES (%s);'
    data = (name,)
    cursor.execute(QUERY, data)
    db.commit()
    db.close()
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
    db, cursor = connect()
    cursor.execute('SELECT players.id, name, wins, games FROM players LEFT JOIN players_scores ON players.id = players_scores.id ORDER BY wins DESC;')
    return cursor.fetchall()



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db, cursor = connect()
    QUERY = 'INSERT INTO matches VALUES (%s, %s);'
    data = (winner, loser)
    cursor.execute(QUERY, data)
    db.commit()
    db.close()
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
        ### create pairings list if we have an even number of players ###
        while n != len(players):
            pair = (players[n][0], players[n][1], players[n + 1][0], players[n + 1][1])
            pairings.append(pair)
            n += 2
    else:
        ### create pairings list if we have odd number of players ###
        while n != len(players) - 1:
            pair = (players[n][0], players[n][1], players[n + 1][0], players[n + 1][1])
            pairings.append(pair)
            n += 2
        single_player = (players[-1][0], players[-1][1], 'id', 'buy win in this tour')
        pairings.append(single_player)

    return pairings