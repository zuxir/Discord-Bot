# Execute this script in the forked directory to create a db table for the "Levels" cog

import sqlite3

cnn = sqlite3.connect('levels.db')
mycursor = cnn.cursor()

# create table
sql_new_table = '''CREATE TABLE "Users" ( "guild_id" INTEGER, "user_id" INTEGER, "level" INTEGER, "xp" INTEGER, "level_up_xp" INTEGER )'''
mycursor.execute(sql_new_table)

cnn.commit()
mycursor.close()