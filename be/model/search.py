from be.model import db_conn

class SearchBooks(db_conn.DBConn):
    def __init__(self):
        db_conn.DBConn.__init__(self)
    def get_books(self, search_query, search_scopes):
        cursor = None
        try:
            # 构建查询条件
            query = ""
            params = []  # 用于保存查询参数

            if search_scopes:
                if 'title' in search_scopes:
                    query += "title LIKE %s OR "
                    params.append(f"%{search_query}%")

                if 'tags' in search_scopes:
                    query += "tags LIKE %s OR "
                    params.append(f"%{search_query}%")

                if 'book_intro' in search_scopes:
                    query += "book_intro LIKE %s OR "
                    params.append(f"%{search_query}%")

                if 'content' in search_scopes:
                    query += "content LIKE %s OR "
                    params.append(f"%{search_query}%")

                if params:  # 如果有参数，去掉最后一个 "OR"
                    query = query.rstrip(" OR ")

            cursor = self.conn.cursor()

            if not search_scopes and not search_query:
                return 200, {"titles": 'titles', "num": '100'}

            # 如果 search_scopes 为空，则显示所有满足 search_query 条件的数据
            if not query and search_query:
                query = "title LIKE %s OR tags LIKE %s OR book_intro LIKE %s OR content LIKE %s"
                params = [f"%{search_query}%" for _ in range(4)]


            # 获取总结果数
            cursor.execute(f"SELECT COUNT(*) FROM books WHERE {query}", tuple(params))
            total_results = cursor.fetchone()[0]

            cursor.execute(f"SELECT title FROM books WHERE {query}", tuple(params))
            book_titles = [book[0] for book in cursor.fetchall()]

            if total_results == 0:
                return 404, "Not Found"
            else:
                return 200, {"titles": book_titles, "num": total_results}


        finally:
            cursor.close()

    def get_stores(self, store_name, search_query, search_scopes):
        cursor = None
        try:
            # 初始化结果列表
            cursor = self.conn.cursor()
            # cursor.execute("SELECT * FROM store WHERE store_id = %s", (store_name,))
            # stores = cursor.fetchall()

            query = "SELECT * FROM store WHERE store_id = %s AND ("
            params = [store_name]  # store_id 参数

            if 'title' in search_scopes:
                query += "title LIKE %s OR "
                params.append(f"%{search_query}%")

            if 'tags' in search_scopes:
                query += "tags LIKE %s OR "
                params.append(f"%{search_query}%")

            if 'book_intro' in search_scopes:
                query += "book_intro LIKE %s OR "
                params.append(f"%{search_query}%")

            if 'content' in search_scopes:
                query += "content LIKE %s OR "
                params.append(f"%{search_query}%")

            query = query.rstrip(" OR ") + ")"

            cursor.execute(query, tuple(params))
            results = cursor.fetchall()

            if not results:  # 如果没有匹配的店铺，设置一个默认的查询条件
                query = "SELECT * FROM store WHERE store_id = 'non_existent_store_id'"
                cursor.execute(query)
                results = cursor.fetchall()

            total_results = len(results)
            book_titles = [result[2] for result in results]

            if total_results == 0:
                return 404, "Not Found"
            else:
                return 200, {"titles": book_titles, "num": total_results}

        finally:
            cursor.close()
