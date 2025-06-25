from database.DB_connect import DBConnect
from model.album import Album


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getNodes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select a.*, sum(t.Milliseconds/1000/60) as durata
                    from album a, track t 
                    where a.AlbumId = t.AlbumId 
                    group by a.AlbumId"""
            cursor.execute(query)

            for row in cursor:
                result.append((Album(**row)))
            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def getEdges(idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select a.AlbumId as id1, a2.AlbumId as id2
            from album a, album a2, track t, track t2, playlisttrack p, playlisttrack p2 
            where a.AlbumId = t.AlbumId 
            and a2.AlbumId = t2.AlbumId 
            and p.TrackId =t.TrackId
            and p2.TrackId =t2.TrackId 
            and p2.PlaylistId = p.PlaylistId
            and a2.AlbumId > a.AlbumId
            group by a.AlbumId, a2.AlbumId """
            cursor.execute(query)

            for row in cursor:
                if row["id1"] in idMap and row["id2"] in idMap:
                    id1 = idMap[row["id1"]]
                    id2 = idMap[row["id2"]]
                    result.append((id1, id2))
            cursor.close()
            cnx.close()
        return result
