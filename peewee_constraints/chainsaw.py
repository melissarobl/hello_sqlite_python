from model import ChainsawRecord #, ChainsawRecordValidator
# from peewee_validates import ModelValidator

def main():
    
    ChainsawRecord.delete().execute()

    add_record('a1', 'gb', 1) # ok
    add_record('a2', 'us', 100) # ok

    # name wrong
    add_record(None, 'gb', 1)
    add_record('', 'gb', 1)
    add_record('a1', 'gb', 1)  # no duplicates

    # country wrong
    add_record('c1', '', 1)
    add_record('c2', 'g', 1)
    add_record('c3', None, 1)

    # catches wrong
    add_record('d1', 'us', None)
    add_record('d2', 'us', -10)
    add_record('d2', 'us', 0)
    add_record('d3', 'us', 2000)
    add_record('d4', 'us', 'fish')

    # multiple errors 
    add_record('a1', 'g', 'hat')

    print('\nAll records\n')
    for r in ChainsawRecord.select():
        print(r)


def add_record(name, country, catches):
    record = ChainsawRecord(name=name, catches=catches, country=country)
    try:
        record.save()
        print(f'Added {record}')
    except Exception as e:
        print(f'Not adding {record}, because {e}')

if __name__ == '__main__':
    main()