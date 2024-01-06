import alch
from sqlalchemy import Column, Integer, String, Numeric


class festival(alch.Base):
    __tablename__ = 'Festival'
    Festival_ID = Column(Integer, primary_key=True)
    Fest_name = Column(String, nullable=False)
    Price = Column(Numeric(10, 2), nullable=False)
    City = Column(String, nullable=False)

class ModelFestival:
    def __init__(self, db_model):
        self.conn = db_model.conn
        self.engine = alch.create_engine(alch.DATABASE_URL)
        self.session = alch.Session.configure(bind=self.engine)
        self.session = alch.Session()

    def add_Festival(self, Festival_ID, Fest_name, Price, City):
        try:
            new_festival = festival(
                Festival_ID=Festival_ID,
                Fest_name=Fest_name,
                Price=Price,
                City=City
            )
            self.session.add(new_festival)
            self.session.commit()
            return True  # Returns True if the update was successful
        except Exception as e:
            self.session.rollback()
            print(f"Error With Adding A Festival: {str(e)}")
            return False  # Returns False if insertion fails

    def get_all_Festivals(self):
        c = self.conn.cursor()
        c.execute('SELECT * FROM "Festival"')
        return c.fetchall()

    def update_Festival(self, Festival_ID, Fest_name, Price, City):
        try:
            Festival = self.session.query(festival).filter_by(Festival_ID=Festival_ID).first()

            if Festival:
                Festival.Festival_ID = Festival_ID
                Festival.Fest_name = Fest_name
                Festival.Price = Price
                Festival.City = City

                self.session.commit()
                return True  # Returns True if the update was successful
            else:
                return False
        except Exception as e:
            self.session.rollback()
            print(f"Error With A Festival Updating: {str(e)}")
            return False   # Returns False if insertion fails

    def delete_Festival(self, Festival_ID):
        try:
            Festival = self.session.query(festival).filter_by(Festival_ID=Festival_ID).first()

            if Festival:
                self.session.delete(Festival)
                self.session.commit()
                return True  # Returns True if the update was successful
            else:
                return False
        except Exception as e:
            self.session.rollback()
            print(f"Error With Deleting A Festival Violates A Foreign Key Constraint: {str(e)}")
            return False   # Returns False if insertion fails

    def check_Festival_existence(self, Festival_ID):
        c = self.conn.cursor()
        c.execute('SELECT 1 FROM "Festival" WHERE "Festival_ID" = %s', (Festival_ID,))
        return bool(c.fetchone())

    def create_Festival_sequence(self):
        # Check for the existence of a sequence
        c = self.conn.cursor()
        c.execute("""
        DO $$
           BEGIN
               IF NOT EXISTS (SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = 'festival_id_seq') THEN
                   CREATE SEQUENCE festival_id_seq;
               ELSE
                   DROP SEQUENCE festival_id_seq;
                   CREATE SEQUENCE festival_id_seq;
               END IF;
           END $$;
        """)
        self.conn.commit()

    def generate_rand_Festival_data(self, number_of_operations):
        c = self.conn.cursor()
        try:
            # Insert data
            c.execute("""
            INSERT INTO "Festival" ("Festival_ID", "Fest_name", "Price", "City")
            SELECT
                nextval('festival_id_seq'), 
                (array['Fire', 'Dance', 'Loud', 'Music', 'Instrumental', 'Box'])[floor(random() * 6) + 1], 
                random() * 1000 ,
                (array['London', 'Lviv', 'Paris', 'Berlin', 'Stockholm'])[floor(random() * 5) + 1]  
            FROM generate_series(1, %s);
            """, (number_of_operations,))
            self.conn.commit()
            return True  # Returns True if the update was successful
        except Exception as e:
            self.conn.rollback()
            print(f"Error With Adding The Festivals: {str(e)}")
            return False   # Returns False if insertion fails


    def truncate_Festival_table(self):
        c = self.conn.cursor()
        try:
            # Insert data
            c.execute("""DELETE FROM "Festival" """)
            self.conn.commit()
            return True  # Returns True if the update was successful
        except Exception as e:
            self.conn.rollback()
            print(f"Error With Deleting All Festival`s Data: {str(e)}")
            return False   # Returns False if insertion fails