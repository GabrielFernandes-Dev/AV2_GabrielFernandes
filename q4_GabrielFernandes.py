VIDEOGAMES = lambda : ("VIDEOGAMES", {"id_console": "int", "name": "varchar (100)", "id_company": "int", "release_date": "date"})
GAMES = lambda : ("GAMES", {"id_game": "int", "title": "varchar (100)", "genre": "varchar (100)", "release_date": "date", "id_console": "int"})
COMPANY = lambda : ("COMPANY", {"id_company": "int", "name": "varchar (100)", "country": "varchar (100)"})

gen_inner_join = lambda tables: (
    f"{tables[0][0][0]} {tables[0][1]}" + 
    "".join(
        f" INNER JOIN {tables[i][0][0]} {tables[i][1]} ON " +
        " AND ".join([f"{tables[i-1][1]}.{e} = {tables[i][1]}.{e}" for e in 
                      [e for e in tables[i-1][0][1].keys() if e in tables[i][0][1].keys()]])
        for i in range(1, len(tables))
    )
)

generate_select = lambda tables, columns: (
    lambda join_query: (
        f"SELECT {', '.join(columns)} FROM {join_query}"
    )
)(gen_inner_join(tables))

print(generate_select([[VIDEOGAMES(), "v"], [GAMES(), "g"]], ["*"]))
print(generate_select([[COMPANY(), "c"], [VIDEOGAMES(), "v"], [GAMES(), "g"]], ["*"]))
