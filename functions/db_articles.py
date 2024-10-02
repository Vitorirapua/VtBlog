from flask_mysqldb import MySQLdb


def get_all(mysql):  # Obtém todos os artigos na página inicial

    sql = '''
        -- Seleciona os campos abaixo
        SELECT art_id, art_title, art_resume, art_thumbnail
        -- desta tabela
        FROM article
        -- art_status é 'on'
        WHERE art_status = 'on'
            -- E art_date é menor ou igual à data atual
            -- Não obtém artigos com data futura (agendados)
            AND art_date <= NOW()
        -- Ordena pela data mais recente  
        ORDER BY art_date DESC;
    '''
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql)
    articles = cur.fetchall()
    cur.close()

    return articles


def get_one(mysql, artid): # Obtém um artigo pelo id

    sql = '''
        SELECT 
            -- Campos do artigo
            art_id, art_date, art_title, art_content,
            -- Campos do autor
            sta_id, sta_name, sta_image, sta_description, sta_type,
            -- Campos especiais
            -- Obtém a data em PT-BR pelo pseudo-campo `art_datebr`
            DATE_FORMAT(art_date, '%%d/%%m/%%Y às %%H:%%i') AS art_datebr,            
            -- Calcula a idade para `sta_age` considerando ano, mês e dia de nascimento
            TIMESTAMPDIFF(YEAR, sta_birth, CURDATE()) - (DATE_FORMAT(CURDATE(), '%%m%%d') < DATE_FORMAT(sta_birth, '%%m%%d')) AS sta_age
        FROM article
        INNER JOIN staff ON art_author = sta_id
        WHERE art_id = %s
            AND art_status = 'on'
            AND art_date <= NOW();
    '''
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, (artid,))
    article = cur.fetchone()
    cur.close()

    return article

def update_views(mysql, artid): # Atualiza as visualizações do artigo

    sql = 'UPDATE article SET art_view = art_view + 1 WHERE art_id = %s'
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, (artid,))
    mysql.connection.commit()
    cur.close()

    return True

def get_author(mysql, staid, artid, limit): # Obtém artigos do author

    sql = '''
        -- Obtém (id, title, thumbnail)
        SELECT art_id, art_title, art_thumbnail
        -- da table `article`
        FROM article
        -- Do author com o id `art_author`
        WHERE art_author = %s
        -- Cujo status é 'on'
            AND art_status = 'on'
            -- Cuja data de publicação está no passado
            AND art_date <= NOW()
            -- Não obtém o artigo atual
            AND art_id != %s
        -- Em ordem aleatória
        ORDER BY RAND()
        -- Até 4 artigos
        LIMIT %s;
    '''
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(sql, (staid, artid, limit, ))
    articles = cur.fetchall()
    cur.close()

    return articles