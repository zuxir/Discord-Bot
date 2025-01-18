# import sqlite3

# def get_server_config(guild_id):
#     connection = sqlite3.connect("./src/databases/serversettings.db")
#     cursor = connection.cursor()
#     cursor.execute("SELECT enabled_cogs FROM Guilds WHERE guild_id = ?", (guild_id))
#     result = cursor.fetchone()
#     connection.close()
#     if result:
#         return result[0].split(",") if result[0] else []
#     return []

# def set_server_config(guild_id, enabled_cogs):
#     connection = sqlite3.connect("./src/databases/serversettings.db")
#     cursor = connection.cursor()
#     cogs_str = ",".join(enabled_cogs)
#     cursor.execute("""
#         INSERT INTO Guilds (guild_id, enabled_cogs)
#         VALUES (?, ?)
#         ON CONFLICT(guild_id) DO UPDATE SET enabled_cogs = excluded.enabled_cogs
#     """, (guild_id, cogs_str))
#     connection.commit()
#     connection.close()