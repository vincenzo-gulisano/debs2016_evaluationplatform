__author__ = 'vincenzo gulisano'

import pymysql.cursors
from optparse import OptionParser


def open_connection(password):
    connection = pymysql.connect(host='129.16.22.6',
                                 port=8080,
                                 user='root',
                                 password=password,
                                 db='debs_eval',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    return connection


def show_participants(connection):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM participants"
        cursor.execute(sql)

        for row in cursor:
            print(row)


def add_participant(connection, participant, email):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `participants` (`participant_id`, `mail`) VALUES (%s, %s)"
        cursor.execute(sql, (participant, email))
    connection.commit()


def check_if_participant_exists(connection, participant):
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(*) as count FROM participants WHERE participant_id=%s"
        cursor.execute(sql, participant)

    result = cursor.fetchone()
    if int(result['count']) == 1:
        return True

    return False

def is_there_something_to_evaluate(connection):
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(*) as count FROM to_evaluate"
        cursor.execute(sql)

    result = cursor.fetchone()
    if int(result['count']) > 0:
        return True

    return False

def get_next_participant_to_evaluate(connection):
    with connection.cursor() as cursor:
        sql = "SELECT * FROM to_evaluate ORDER BY ts ASC"
        cursor.execute(sql)

    result = cursor.fetchone()
    return result['participant_id']

def check_if_participant_has_pending_evaluation(connection, participant):
    with connection.cursor() as cursor:
        sql = "SELECT COUNT(*) as count FROM to_evaluate WHERE participant_id=%s"
        cursor.execute(sql, participant)

    result = cursor.fetchone()
    if int(result['count']) == 1:
        return True

    return False


def add_participant_to_evaluate(connection, participant, vm_location):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `to_evaluate` (`participant_id`, `vm_location`) VALUES (%s, %s)"
        cursor.execute(sql, (participant, vm_location))
    connection.commit()


def remove_participant_evaluated(connection, participant):
    with connection.cursor() as cursor:
        sql = "DELETE FROM to_evaluate WHERE participant_id=%s"
        cursor.execute(sql, (participant))
    connection.commit()


def add_participant_evaluation(connection, participant, duration, throughput, latency, log):
    with connection.cursor() as cursor:
        sql = "INSERT INTO `evaluated` (`participant_id`, `duration`, `throughput`, `latency`, `log`) " \
              " VALUES (%s,%s,%s,%s,%s)"
        cursor.execute(sql, (participant, duration, throughput, latency, log))
    connection.commit()


def close_connection(connection):
    connection.close()

parser = OptionParser()
parser.add_option("-p", "--password", dest="password",
                  help="DB password", metavar="PASSWORD")

(options, args) = parser.parse_args()

if options.password is None:
    print('A mandatory option (-p, --password) is missing\n')
    parser.print_help()
    exit(-1)

connection = open_connection(options.password)
# add_participant(connection, 'vincenzo', 'vincenzo.gulisano@gmail.com')
show_participants(connection)
print(check_if_participant_exists(connection, 'vincenzo'))
print(check_if_participant_has_pending_evaluation(connection, 'vincenzo'))
add_participant_to_evaluate(connection, 'participant3', 'www.abc.com')
# remove_participant_evaluated(connection, 'participant2')
add_participant_evaluation(connection, 'vincenzo', '132', '12341', '231', 'sda')
print(is_there_something_to_evaluate(connection))
if is_there_something_to_evaluate(connection):
    print(get_next_participant_to_evaluate(connection))
close_connection(connection)
