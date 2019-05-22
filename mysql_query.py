import MySQLdb


def consulta_acellz(startDate, endDate, cantidad=5000):
    db = MySQLdb.connect("hstech.sinc.cl", "jsanhueza", "Hstech2018.-)", "ssi_mlp_sag2")
    cursor = db.cursor()

    cursor.execute(f"SELECT dataZ , fecha_reg \
        FROM Data_Sensor \
        WHERE (id_sensor_data IN (1) AND estado_data = 134217727 \
        AND (fecha_reg BETWEEN {startDate} AND {endDate}) ) \
        ORDER BY fecha_reg ASC \
        LIMIT {cantidad}")

    results = cursor.fetchall()
    db.close()
    return results
