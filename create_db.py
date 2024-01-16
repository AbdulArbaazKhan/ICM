import sqlite3


def create_db():
    conct = sqlite3.connect(database=r'icm.db')
    cursr = conct.cursor()
    cursr.execute("""CREATE TABLE IF NOT EXISTS employee( `eid` INT PRIMARY KEY,  `name` TEXT NOT NULL ,  `email` TEXT,  `passw` TEXT NOT NULL ,  `contact` TEXT NOT NULL ,  `dob` DATE,  `address` TEXT ,  `doj` DATE DEFAULT CURRENT_TIMESTAMP ,  `gender` TEXT ,  `usertype` TEXT )""")
    conct.commit()
    cursr.execute("""CREATE TABLE IF NOT EXISTS supplier( `invoice` INT PRIMARY KEY,  `name` TEXT NOT NULL ,  `contact` TEXT, `desc` TEXT )""")
    conct.commit()

    cursr.execute(
        """CREATE TABLE IF NOT EXISTS category( `cid` INTEGER PRIMARY KEY AUTOINCREMENT,  `name` TEXT NOT NULL)""")
    conct.commit()

create_db()